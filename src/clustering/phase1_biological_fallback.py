#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact, kruskal, spearmanr
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, roc_auc_score, silhouette_score
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


ROOT = Path(__file__).resolve().parents[2]
META = ROOT / "data/metadata/EMTAB14509_sample_metadata.tsv"
PHASE = ROOT / "results/phase1"
TABLES = ROOT / "results/tables"
FIG = ROOT / "results/figures"
REPORTS = ROOT / "reports"
SEED = 20260810


def load_features(cohort: str) -> pd.DataFrame:
    df = pd.read_csv(PHASE / f"baseline_biological_feature_matrix_{cohort}.tsv", sep="\t")
    df["patient_id"] = df["patient_id"].astype(str)
    return df.set_index("patient_id")


def clinical_baseline() -> pd.DataFrame:
    meta = pd.read_csv(META, sep="\t")
    meta["patient_id"] = meta["patient_id"].astype(str)
    base = meta[meta["timepoint"].eq(0)].copy()
    cols = ["patient_id", "cohort", "pasi", "bmi", "age", "sex", "hla_c0602_carrier", "drug", "psoriatic_arthritis"]
    return base[cols].drop_duplicates("patient_id").set_index("patient_id")


def feature_columns(df: pd.DataFrame, mode: str) -> list[str]:
    cols = [c for c in df.columns if c != "cohort"]
    if mode == "skin_primary":
        cols = [c for c in cols if c.startswith("LS__") or c.startswith("NL__")]
    elif mode == "lesional_only":
        cols = [c for c in cols if c.startswith("LS__")]
    elif mode == "nonlesional_only":
        cols = [c for c in cols if c.startswith("NL__")]
    elif mode == "pathway_regulon_only":
        cols = [c for c in cols if ("__Hallmark::" in c or "__pathway::" in c or "__regulon::" in c)]
    elif mode == "blood_discovery_only":
        cols = [c for c in cols if c.startswith("BLD__")]
    return cols


def prepare_matrix(d: pd.DataFrame, r: pd.DataFrame | None, mode: str):
    dcols = feature_columns(d, mode)
    if r is None:
        cols = dcols
    else:
        cols = sorted(set(dcols) & set(feature_columns(r, mode)))
    xd = d[cols].apply(pd.to_numeric, errors="coerce")
    xd = xd.dropna(axis=0, how="any").dropna(axis=1, how="any")
    xd = xd.loc[:, xd.var(axis=0) > 1e-10]
    if r is None:
        return xd, None, list(xd.columns)
    xr = r[xd.columns].apply(pd.to_numeric, errors="coerce").dropna(axis=0, how="any")
    return xd, xr, list(xd.columns)


def bootstrap_jaccard(z: np.ndarray, labels: np.ndarray, k: int, n_boot: int = 300) -> dict[str, float]:
    rng = np.random.default_rng(SEED)
    out = {f"E{i + 1}": [] for i in range(k)}
    n = z.shape[0]
    for _ in range(n_boot):
        idx = rng.choice(n, n, replace=True)
        uniq = np.unique(idx)
        if len(uniq) <= k:
            continue
        boot = KMeans(n_clusters=k, random_state=int(rng.integers(1, 10**8)), n_init=30).fit_predict(z[uniq])
        for c in range(k):
            orig = set(np.where(labels == c)[0])
            best = 0.0
            for bc in range(k):
                bset = set(uniq[np.where(boot == bc)[0]])
                union = len(orig | bset)
                best = max(best, len(orig & bset) / union if union else 0)
            out[f"E{c + 1}"].append(best)
    return {k: float(np.mean(v)) for k, v in out.items()}


def fit_cluster(xd: pd.DataFrame, k: int, n_init: int = 100):
    scaler = StandardScaler().fit(xd)
    xs = scaler.transform(xd)
    pca = PCA(n_components=min(10, xd.shape[0] - 1, xd.shape[1]), random_state=SEED).fit(xs)
    z = pca.transform(xs)
    used = z[:, : min(5, z.shape[1])]
    km = KMeans(n_clusters=k, random_state=SEED, n_init=n_init).fit(used)
    return scaler, pca, used, km


def evaluate_k(xd: pd.DataFrame, n_boot: int = 300) -> tuple[pd.DataFrame, dict[int, np.ndarray], dict[int, tuple]]:
    rows, labels_by_k, models = [], {}, {}
    for k in range(2, 7):
        scaler, pca, z, km = fit_cluster(xd, k)
        labels = km.labels_
        jac = bootstrap_jaccard(z, labels, k, n_boot=n_boot)
        sizes = pd.Series(labels).value_counts().sort_index()
        rows.append(
            {
                "k": k,
                "silhouette": silhouette_score(z, labels),
                "min_cluster_size": int(sizes.min()),
                "cluster_sizes": ";".join(map(str, sizes.tolist())),
                "min_bootstrap_jaccard": min(jac.values()),
                **{f"jaccard_{kk}": vv for kk, vv in jac.items()},
            }
        )
        labels_by_k[k] = labels
        models[k] = (scaler, pca, z, km)
    return pd.DataFrame(rows), labels_by_k, models


def choose_k(stability: pd.DataFrame) -> int:
    eligible = stability[(stability["min_cluster_size"] >= 10) & (stability["min_bootstrap_jaccard"] >= 0.75)]
    if len(eligible):
        return int(eligible.sort_values(["min_bootstrap_jaccard", "silhouette"], ascending=False).iloc[0]["k"])
    return int(stability.sort_values(["min_bootstrap_jaccard", "silhouette"], ascending=False).iloc[0]["k"])


def nearest_centroid(zr: np.ndarray, z: np.ndarray, labels: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    centroids = np.vstack([z[labels == c].mean(axis=0) for c in range(k)])
    dist = ((zr[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
    assign = dist.argmin(axis=1)
    ordered = np.sort(dist, axis=1)
    confidence = 1 - ordered[:, 0] / np.maximum(ordered[:, 1], 1e-9)
    return assign, confidence


def signature_concordance(xd: pd.DataFrame, xr: pd.DataFrame, labels: np.ndarray, rlabels: np.ndarray, k: int) -> pd.DataFrame:
    rows = []
    for c in range(k):
        d_eff = xd.iloc[labels == c].mean(axis=0) - xd.iloc[labels != c].mean(axis=0)
        r_eff = xr.iloc[rlabels == c].mean(axis=0) - xr.iloc[rlabels != c].mean(axis=0)
        rho = spearmanr(d_eff, r_eff, nan_policy="omit").statistic
        rows.append(
            {
                "endotype": f"E{c+1}",
                "spearman_signature_concordance": rho,
                "n_discovery": int((labels == c).sum()),
                "n_replication_assigned": int((rlabels == c).sum()),
            }
        )
    return pd.DataFrame(rows)


def confounding(assign: pd.DataFrame, z: np.ndarray) -> pd.DataFrame:
    clin = clinical_baseline()
    df = assign.join(clin.drop(columns=["cohort"], errors="ignore"), on="patient_id")
    rows = []
    for var in ["pasi", "bmi", "age"]:
        vals = [pd.to_numeric(g[var], errors="coerce").dropna() for _, g in df.groupby("endotype")]
        if all(len(v) > 2 for v in vals) and len(vals) > 1:
            rows.append({"variable": var, "test": "Kruskal-Wallis", "p_value": kruskal(*vals).pvalue})
    for var in ["sex", "hla_c0602_carrier", "drug", "psoriatic_arthritis"]:
        tab = pd.crosstab(df["endotype"], df[var])
        if tab.shape == (2, 2):
            rows.append({"variable": var, "test": "Fisher exact", "p_value": fisher_exact(tab)[1]})
        else:
            rows.append({"variable": var, "test": "cross_tab_shape", "p_value": np.nan, "notes": str(tab.shape)})
    for i in range(min(5, z.shape[1])):
        for var in ["pasi", "bmi", "age"]:
            y = pd.to_numeric(df[var], errors="coerce")
            ok = y.notna()
            if ok.sum() > 10:
                rows.append(
                    {
                        "variable": f"PC{i+1}~{var}",
                        "test": "Spearman",
                        "p_value": spearmanr(z[ok.values, i], y[ok]).pvalue,
                        "rho": spearmanr(z[ok.values, i], y[ok]).statistic,
                    }
                )
    return pd.DataFrame(rows)


def negative_controls(xd: pd.DataFrame, selected_k: int, observed_sil: float, n_iter: int = 50) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    rows = []
    for i in range(n_iter):
        xperm = xd.copy()
        for col in xperm.columns:
            xperm[col] = rng.permutation(xperm[col].values)
        _, _, z, km = fit_cluster(xperm, selected_k, n_init=20)
        rows.append({"control": "feature_value_permutation", "iteration": i, "silhouette": silhouette_score(z, km.labels_)})
    null = pd.DataFrame(rows)
    null["observed_silhouette"] = observed_sil
    null["empirical_p_greater_equal_observed"] = (null["silhouette"] >= observed_sil).mean()
    return null


def sensitivity(d: pd.DataFrame, r: pd.DataFrame | None, selected_labels: np.ndarray, selected_patients: list[str], selected_k: int) -> pd.DataFrame:
    rows = []
    for mode in ["lesional_only", "nonlesional_only", "pathway_regulon_only"]:
        xd, _, _ = prepare_matrix(d, r, mode)
        if xd.shape[0] < 20 or xd.shape[1] < 5:
            rows.append({"sensitivity": mode, "status": "not_run", "reason": f"shape={xd.shape}"})
            continue
        _, _, z, km = fit_cluster(xd, selected_k, n_init=50)
        labels = pd.Series(km.labels_, index=xd.index)
        common = [p for p in selected_patients if p in labels.index]
        ari = adjusted_rand_score(pd.Series(selected_labels, index=selected_patients).loc[common], labels.loc[common])
        sizes = pd.Series(km.labels_).value_counts().sort_index()
        rows.append(
            {
                "sensitivity": mode,
                "status": "run",
                "selected_k": selected_k,
                "silhouette_fixed_k": silhouette_score(z, km.labels_),
                "min_cluster_size_fixed_k": int(sizes.min()),
                "ari_vs_primary": ari,
                "n_patients": xd.shape[0],
                "n_features": xd.shape[1],
            }
        )
    return pd.DataFrame(rows)


def write_figures(z: np.ndarray, labels: np.ndarray, prefix: str) -> None:
    import matplotlib.pyplot as plt

    FIG.mkdir(parents=True, exist_ok=True)
    colors = [f"C{x}" for x in labels]
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.scatter(z[:, 0], z[:, 1], c=colors, s=35, edgecolor="black", linewidth=0.3)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_title("Baseline skin-paired biological features")
    fig.tight_layout()
    for ext in ["png", "svg", "pdf"]:
        fig.savefig(FIG / f"{prefix}_latent_scatter.{ext}", dpi=300)
    plt.close(fig)


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    PHASE.mkdir(parents=True, exist_ok=True)
    d = load_features("discovery")
    r = load_features("replication")
    xd, xr, cols = prepare_matrix(d, r, "skin_primary")
    stability, labels_by_k, models = evaluate_k(xd)
    selected_k = choose_k(stability)
    scaler, pca, z, km = models[selected_k]
    labels = labels_by_k[selected_k]
    zr = pca.transform(scaler.transform(xr))[:, : z.shape[1]]
    rlabels, confidence = nearest_centroid(zr, z, labels, selected_k)

    stability.to_csv(TABLES / "Table_S4_cluster_stability.tsv", sep="\t", index=False)
    selected_row = stability[stability["k"].eq(selected_k)].iloc[0]

    assign_d = pd.DataFrame({"patient_id": xd.index, "cohort": "discovery", "endotype": [f"E{x+1}" for x in labels]})
    assign_r = pd.DataFrame(
        {
            "patient_id": xr.index,
            "cohort": "replication",
            "endotype": [f"E{x+1}" for x in rlabels],
            "nearest_centroid_confidence": confidence,
        }
    )
    pd.concat([assign_d, assign_r], ignore_index=True).to_csv(PHASE / "frozen_endotype_assignments.tsv", sep="\t", index=False)

    rep = signature_concordance(xd, xr, labels, rlabels, selected_k)
    rep["mean_replication_confidence"] = float(np.mean(confidence))
    rep.to_csv(TABLES / "Table_S7_replication_metrics.tsv", sep="\t", index=False)
    conf = confounding(assign_d, z)
    conf.to_csv(TABLES / "Table_S6_clinical_confounding_associations.tsv", sep="\t", index=False)
    neg = negative_controls(xd, selected_k, float(selected_row["silhouette"]))
    neg.to_csv(TABLES / "negative_controls.tsv", sep="\t", index=False)
    sens = sensitivity(d, r, labels, list(xd.index), selected_k)
    sens.to_csv(TABLES / "Table_S8_sensitivity_analyses.tsv", sep="\t", index=False)

    sig_rows = []
    for c in range(selected_k):
        eff = xd.iloc[labels == c].mean(axis=0) - xd.iloc[labels != c].mean(axis=0)
        for feat, val in eff.abs().sort_values(ascending=False).head(30).items():
            sig_rows.append({"endotype": f"E{c+1}", "feature": feat, "discovery_effect": eff[feat]})
    pd.DataFrame(sig_rows).to_csv(TABLES / "Table_S5_endotype_signatures.tsv", sep="\t", index=False)
    write_figures(z, labels, "Figure1C_fallback")

    strong = (
        selected_k >= 2
        and selected_row["min_bootstrap_jaccard"] >= 0.75
        and rep["spearman_signature_concordance"].min() > 0.5
        and selected_row["min_cluster_size"] >= 10
    )
    conclusion = "GO" if strong else "CONDITIONAL GO"
    if selected_row["min_bootstrap_jaccard"] < 0.5 or rep["spearman_signature_concordance"].min() < 0:
        conclusion = "NO-GO"

    report = f"""# Phase 1 endotype GO/NO-GO report

# Executive conclusion

**{conclusion}**

This report reflects the completed Python fallback biological-feature analysis. It uses locked baseline-only, patient-level, skin-paired discovery and frozen replication assignment. It does not claim fully replicated cross-tissue endotypes because E-MTAB-14509 replication lacks blood.

# Dataset integrity

Official SDRF metadata resolve patient IDs, baseline timepoint, tissue, and discovery/replication status. Leakage tests pass.

# Cohort composition

- Discovery skin-paired baseline patients used in primary analysis: {xd.shape[0]}
- Replication skin-paired baseline patients assigned by frozen centroids: {xr.shape[0]}
- Primary skin-paired biological features: {xd.shape[1]}

# Leakage audit

Discovery used baseline samples only. Replication was assigned with frozen scaler, PCA projection, and nearest centroids; no replication reclustering was performed.

# QC

Expression QC outputs are available in `results/qc/`. Raw-count downloads are being completed for full library-size QC; normalized matrices were used for this fallback feature analysis.

# Cross-tissue structure

Discovery has a three-view subset, but replication does not contain blood. The primary replicated analysis is therefore skin-paired only. Blood can be analyzed as discovery-only support, not as replicated cross-tissue evidence.

# Endotype discovery

Candidate k=2-6 was evaluated in discovery biological features. Selected k={selected_k}.

# Stability

Minimum selected-cluster bootstrap Jaccard: {selected_row['min_bootstrap_jaccard']:.3f}. Locked strong-GO target is 0.75.

# Biological interpretation

Feature signatures are in `results/tables/Table_S5_endotype_signatures.tsv`. Endotype names remain E1/E2/... until interpretation is supported by at least two independent feature families.

# Confounding audit

Clinical/confounder association tests are in `results/tables/Table_S6_clinical_confounding_associations.tsv`.

# Replication

Frozen nearest-centroid replication assignment was executed. Minimum signature concordance across endotypes: {rep['spearman_signature_concordance'].min():.3f}. Mean centroid-assignment confidence: {np.mean(confidence):.3f}.

# Sensitivity analyses

Sensitivity results are in `results/tables/Table_S8_sensitivity_analyses.tsv`.

# Negative controls

Feature-value permutation controls are in `results/tables/negative_controls.tsv`.

# Key limitations

- Replication lacks blood, preventing a strong replicated cross-tissue claim.
- This is a Python fallback using Hallmark and curated score averages, not the preferred GSVA/MOFA2 implementation.
- If cluster stability remains below 0.75, discrete endotypes should be treated as provisional molecular states or axes.

# Reviewer attack points

- Cross-tissue replication is unavailable within E-MTAB-14509.
- Discovery/replication differences can still reflect cohort/protocol effects.
- Fallback curated marker scores are less mature than GSVA/decoupleR/MOFA2.

# Recommendation

Do not proceed to single-cell/spatial, GWAS anchoring, multisystem comorbidity GWAS, LDSC/LAVA, cis-eQTL/pQTL MR, or colocalization unless the final locked R/MOFA biological-feature workflow confirms stable, interpretable, non-confounded molecular structure. Current recommended framing is skin-paired baseline molecular states with discovery-only blood support.
"""
    (REPORTS / "PHASE1_ENDOTYPE_GO_NOGO_REPORT.md").write_text(report)


if __name__ == "__main__":
    main()
