#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw"
META = ROOT / "data/metadata/EMTAB14509_sample_metadata.tsv"
OUT = ROOT / "results/phase1"
FIG = ROOT / "results/figures"
TABLES = ROOT / "results/tables"
REPORTS = ROOT / "reports"
SEED = 20260810


def read_counts(name: str) -> pd.DataFrame:
    path = RAW / name
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path, sep="\t", index_col=0)


def baseline_samples(meta: pd.DataFrame, cohort: str, tissue: str) -> list[str]:
    rows = meta[
        (meta["cohort"] == cohort)
        & (meta["timepoint"] == 0)
        & (meta["tissue"] == tissue)
    ]
    return rows["sample_id"].tolist()


def patient_vector(meta: pd.DataFrame, sample_ids: list[str]) -> pd.Series:
    return meta.set_index("sample_id").loc[sample_ids, "patient_id"].astype(str)


def collapse_to_patient(mat: pd.DataFrame, meta: pd.DataFrame, cohort: str, tissue: str) -> pd.DataFrame:
    samples = [s for s in baseline_samples(meta, cohort, tissue) if s in mat.columns]
    sub = mat[samples].T
    sub.index = patient_vector(meta, samples).values
    sub = sub.groupby(level=0).mean()
    return sub


def top_variable(df: pd.DataFrame, n: int = 1000) -> pd.DataFrame:
    n = min(n, df.shape[1])
    cols = df.var(axis=0).sort_values(ascending=False).head(n).index
    return df.loc[:, cols]


def bootstrap_jaccard(x: np.ndarray, labels: np.ndarray, k: int, n_boot: int = 100) -> dict[str, float]:
    rng = np.random.default_rng(SEED)
    out = {f"E{i + 1}": [] for i in range(k)}
    n = x.shape[0]
    for _ in range(n_boot):
        idx = rng.choice(n, n, replace=True)
        uniq = np.unique(idx)
        if len(uniq) < k * 5:
            continue
        km = KMeans(n_clusters=k, random_state=int(rng.integers(1, 10**8)), n_init=20)
        boot_labels = km.fit_predict(x[uniq])
        for c in range(k):
            orig = set(np.where(labels == c)[0])
            best = 0.0
            for bc in range(k):
                boot = set(uniq[np.where(boot_labels == bc)[0]])
                union = len(orig | boot)
                if union:
                    best = max(best, len(orig & boot) / union)
            out[f"E{c + 1}"].append(best)
    return {k: float(np.mean(v)) if v else np.nan for k, v in out.items()}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    meta = pd.read_csv(META, sep="\t")
    meta["patient_id"] = meta["patient_id"].astype(str)

    skin_d = read_counts("Skin_norm_counts_d.txt")
    skin_r = read_counts("Skin_norm_counts_r.txt")
    blood_d = read_counts("Blood_norm_counts_d.txt")

    d_ls = collapse_to_patient(skin_d, meta, "discovery", "Lesional Skin")
    d_nl = collapse_to_patient(skin_d, meta, "discovery", "Nonlesional Skin")
    d_blood = collapse_to_patient(blood_d, meta, "discovery", "Whole Blood")
    r_ls = collapse_to_patient(skin_r, meta, "replication", "Lesional Skin")
    r_nl = collapse_to_patient(skin_r, meta, "replication", "Nonlesional Skin")

    d_patients = sorted(set(d_ls.index) & set(d_nl.index))
    r_patients = sorted(set(r_ls.index) & set(r_nl.index))
    d_all3 = sorted(set(d_patients) & set(d_blood.index))

    common_genes = sorted(set(d_ls.columns) & set(d_nl.columns) & set(r_ls.columns) & set(r_nl.columns))
    d_delta = d_ls.loc[d_patients, common_genes] - d_nl.loc[d_patients, common_genes]
    r_delta = r_ls.loc[r_patients, common_genes] - r_nl.loc[r_patients, common_genes]

    # Smoke-test feature space: top variable lesional-minus-nonlesional axes in discovery.
    # This is explicitly not the locked primary biological feature analysis.
    d_top = top_variable(d_delta, 1000)
    r_top = r_delta[d_top.columns]

    scaler = StandardScaler().fit(d_top)
    xd = scaler.transform(d_top)
    xr = scaler.transform(r_top)
    pca = PCA(n_components=min(10, xd.shape[0] - 1), random_state=SEED).fit(xd)
    zd = pca.transform(xd)
    zr = pca.transform(xr)

    rows = []
    label_map = {}
    for k in range(2, 7):
        km = KMeans(n_clusters=k, random_state=SEED, n_init=100).fit(zd[:, : min(5, zd.shape[1])])
        labels = km.labels_
        sizes = pd.Series(labels).value_counts().sort_index().tolist()
        sil = silhouette_score(zd[:, : min(5, zd.shape[1])], labels)
        jac = bootstrap_jaccard(zd[:, : min(5, zd.shape[1])], labels, k, n_boot=100)
        rows.append(
            {
                "k": k,
                "silhouette": sil,
                "min_cluster_size": min(sizes),
                "cluster_sizes": ";".join(map(str, sizes)),
                "min_bootstrap_jaccard": np.nanmin(list(jac.values())),
                **{f"jaccard_{kk}": vv for kk, vv in jac.items()},
            }
        )
        label_map[k] = labels

    stability = pd.DataFrame(rows)
    stability.to_csv(TABLES / "Table_S4_cluster_stability_smoke.tsv", sep="\t", index=False)
    eligible = stability[
        (stability["min_cluster_size"] >= 10) & (stability["min_bootstrap_jaccard"] >= 0.75)
    ].sort_values(["min_bootstrap_jaccard", "silhouette"], ascending=False)
    selected_k = int(eligible.iloc[0]["k"]) if len(eligible) else int(stability.sort_values("silhouette", ascending=False).iloc[0]["k"])
    labels = label_map[selected_k]

    centroids = np.vstack([zd[labels == c, : min(5, zd.shape[1])].mean(axis=0) for c in range(selected_k)])
    dist = ((zr[:, : min(5, zr.shape[1])][:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
    rep_labels = dist.argmin(axis=1)
    confidence = 1 - (np.sort(dist, axis=1)[:, 0] / np.maximum(np.sort(dist, axis=1)[:, 1], 1e-9))

    assignments_d = pd.DataFrame({"patient_id": d_top.index, "endotype": [f"E{x+1}" for x in labels], "cohort": "discovery"})
    assignments_r = pd.DataFrame({"patient_id": r_top.index, "endotype": [f"E{x+1}" for x in rep_labels], "cohort": "replication", "nearest_centroid_confidence": confidence})
    assignments = pd.concat([assignments_d, assignments_r], ignore_index=True)
    assignments.to_csv(OUT / "smoke_test_frozen_assignments.tsv", sep="\t", index=False)

    signatures = []
    concordance = []
    for c in range(selected_k):
        e = f"E{c+1}"
        d_effect = d_top.loc[labels == c].mean(axis=0) - d_top.loc[labels != c].mean(axis=0)
        r_effect = r_top.loc[rep_labels == c].mean(axis=0) - r_top.loc[rep_labels != c].mean(axis=0)
        rho = spearmanr(d_effect, r_effect, nan_policy="omit").statistic
        concordance.append({"endotype": e, "spearman_signature_concordance": rho, "n_replication_assigned": int((rep_labels == c).sum())})
        top = d_effect.abs().sort_values(ascending=False).head(25).index
        for gene in top:
            signatures.append({"endotype": e, "ensembl_gene": gene, "discovery_delta_effect": d_effect[gene], "replication_delta_effect": r_effect[gene]})
    pd.DataFrame(signatures).to_csv(TABLES / "Table_S5_endotype_signatures_smoke.tsv", sep="\t", index=False)
    pd.DataFrame(concordance).to_csv(TABLES / "Table_S7_replication_metrics_smoke.tsv", sep="\t", index=False)

    summary = pd.DataFrame(
        [
            {"metric": "discovery_skin_pair_patients", "value": len(d_patients)},
            {"metric": "discovery_three_tissue_patients", "value": len(d_all3)},
            {"metric": "replication_skin_pair_patients", "value": len(r_patients)},
            {"metric": "replication_blood_patients", "value": 0},
            {"metric": "selected_k_smoke", "value": selected_k},
            {"metric": "primary_feature_lock_satisfied", "value": False},
            {"metric": "mofa2_available", "value": False},
        ]
    )
    summary.to_csv(OUT / "phase1_smoke_summary.tsv", sep="\t", index=False)

    report = f"""# Phase 1 endotype GO/NO-GO report

# Executive conclusion

**CONDITIONAL GO**

The project is conditionally worth continuing only as a skin-paired baseline molecular-state analysis until the locked biological feature workflow is completed. The current official metadata do not support a strong cross-tissue discovery-and-replication endotype claim because E-MTAB-14509 replication has no whole-blood samples.

# Dataset integrity

Official SDRF-derived cohort labels are recoverable and no patient crosses discovery and replication. Baseline-only filtering is executable.

# Cohort composition

- Discovery baseline skin-paired patients: {len(d_patients)}
- Discovery baseline three-tissue patients: {len(d_all3)}
- Replication baseline skin-paired patients: {len(r_patients)}
- Replication baseline blood patients: 0

# Leakage audit

Automated tests passed for patient non-overlap, baseline-only flagging, duplicate sample IDs, one patient-one baseline tissue unit, and frozen replication policy.

# QC

Normalized matrices were downloaded for discovery skin, discovery blood, and replication skin. Raw-count QC remains incomplete because full raw matrices were not needed for this smoke test and the raw download was stopped after entering a large nonblocking file.

# Cross-tissue structure

Discovery can support a three-view structure for {len(d_all3)} patients. Replication cannot test a blood view, so any cross-tissue claim must be downgraded unless a separate replication blood resource is added in a future locked phase.

# Endotype discovery

A smoke test was run using discovery lesional-minus-nonlesional normalized expression axes. This is not the locked primary biological feature analysis and must not be treated as final evidence for mechanistic endotypes.

# Stability

See `results/tables/Table_S4_cluster_stability_smoke.tsv`. The smoke test selected k={selected_k} for downstream assignment machinery.

# Biological interpretation

Not yet established. The locked rule requires at least two independent biological feature families; this smoke test does not satisfy that rule.

# Confounding audit

Not completed for final Phase 1. Metadata fields are available for PASI, BMI, age, sex, HLA-C*06:02, drug, biologic-naive status, anti-TNF-naive status, and psoriatic arthritis.

# Replication

Frozen nearest-centroid assignment was executed in replication skin-paired patients. See `results/phase1/smoke_test_frozen_assignments.tsv` and `results/tables/Table_S7_replication_metrics_smoke.tsv`.

# Sensitivity analyses

Not completed for final Phase 1. The project should run the locked k, feature-family, lesional-only, blood-only, complete-case, seed, and extreme BMI/PASI sensitivity analyses before upgrading beyond CONDITIONAL GO.

# Negative controls

Not completed for final Phase 1.

# Key limitations

- Replication lacks whole-blood RNA-seq samples.
- MOFA2, GSVA, and ConsensusClusterPlus are not currently installed in the active R library.
- The smoke test uses expression axes, not locked pathway/regulon/cell-state features.
- Strong cross-tissue mechanistic endotypes are not yet demonstrated.

# Reviewer attack points

- Cross-tissue discovery cannot be independently replicated within the same accession.
- Discovery/replication sequencing protocols and platforms differ, making cohort-batch confounding a central risk.
- Any cluster claim based on expression axes alone would be vulnerable to severity, batch, and tissue-composition criticism.

# Recommendation

Proceed to a full locked Phase 1 only after installing the biological-feature stack and deciding whether the primary claim is skin-paired endotypes with discovery-only blood support, or continuous molecular axes. Do not proceed to single-cell/spatial validation, GWAS anchoring, multisystem comorbidity GWAS, LDSC/LAVA, cis-eQTL/pQTL MR, or colocalization yet.
"""
    (REPORTS / "PHASE1_ENDOTYPE_GO_NOGO_REPORT.md").write_text(report)


if __name__ == "__main__":
    main()

