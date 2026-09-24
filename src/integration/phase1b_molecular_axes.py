#!/usr/bin/env python3
"""Phase 1B: discovery-only molecular axes with frozen skin projection."""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import h5py
import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from scipy.stats import pearsonr, spearmanr
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]
PHASE1B = ROOT / "results" / "phase1b"
REPORTS = ROOT / "reports"
SEEDS = [20260810, 20260811, 20260812, 20260813, 20260814]
N_FACTORS = 8
TOP_PER_VIEW = 450
MIN_FEATURE_SD = 1e-8


def _safe_corr(x: np.ndarray, y: np.ndarray, method: str = "pearson") -> float:
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() < 3:
        return np.nan
    if np.nanstd(x[mask]) == 0 or np.nanstd(y[mask]) == 0:
        return np.nan
    if method == "spearman":
        return float(spearmanr(x[mask], y[mask]).correlation)
    return float(pearsonr(x[mask], y[mask]).statistic)


def bh_fdr(pvals: pd.Series) -> pd.Series:
    out = pd.Series(np.nan, index=pvals.index, dtype=float)
    mask = pvals.notna()
    p = pvals[mask].astype(float).clip(0, 1).to_numpy()
    if len(p) == 0:
        return out
    order = np.argsort(p)
    ranked = p[order]
    q = ranked * len(p) / (np.arange(len(p)) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    q = np.clip(q, 0, 1)
    tmp = np.empty_like(q)
    tmp[order] = q
    out.loc[mask] = tmp
    return out


def load_feature_matrices() -> tuple[pd.DataFrame, pd.DataFrame]:
    discovery = pd.read_csv(PHASE1B / "phase1b_feature_matrix_discovery.tsv", sep="\t")
    replication = pd.read_csv(PHASE1B / "phase1b_feature_matrix_replication.tsv", sep="\t")
    discovery["patient_id"] = discovery["patient_id"].astype(str)
    replication["patient_id"] = replication["patient_id"].astype(str)
    return discovery, replication


def split_views(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    out = {}
    for view in ["LS", "NL", "BLD"]:
        cols = [c for c in df.columns if c.startswith(f"{view}__")]
        if cols:
            sub = df.set_index("patient_id")[cols].apply(pd.to_numeric, errors="coerce")
            sub.columns = [c.split("__", 1)[1] for c in sub.columns]
            out[view] = sub
    return out


def restrict_to_common_available_patients(views: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    patient_sets = []
    for view in ["LS", "NL", "BLD"]:
        mat = views[view]
        patient_sets.append(set(mat.index[mat.notna().any(axis=1)]))
    common = sorted(set.intersection(*patient_sets))
    return {view: mat.loc[common].copy() for view, mat in views.items()}


def select_features(views: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for view, mat in views.items():
        complete = mat.dropna(axis=1, how="any")
        sd = complete.std(axis=0, ddof=0)
        sd = sd[sd > MIN_FEATURE_SD].sort_values(ascending=False)
        keep = sd.head(TOP_PER_VIEW).index.tolist()
        for feature in keep:
            rows.append(
                {
                    "view": view,
                    "feature": feature,
                    "sd_discovery": sd.loc[feature],
                    "rank_within_view": len(rows) + 1,
                    "selection_rule": f"top_{TOP_PER_VIEW}_within_view_by_discovery_sd_after_complete_case_filter",
                }
            )
    selected = pd.DataFrame(rows)
    selected["rank_within_view"] = selected.groupby("view").cumcount() + 1
    selected.to_csv(PHASE1B / "phase1b_selected_features.tsv", sep="\t", index=False)
    return selected


def scale_discovery_views(
    views: dict[str, pd.DataFrame], selected: pd.DataFrame
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    scaled = {}
    scale_rows = []
    for view in ["LS", "NL", "BLD"]:
        feats = selected.loc[selected["view"] == view, "feature"].tolist()
        mat = views[view][feats].copy()
        means = mat.mean(axis=0)
        sds = mat.std(axis=0, ddof=0).replace(0, np.nan)
        z = (mat - means) / sds
        scaled[view] = z
        scale_rows.extend(
            {
                "view": view,
                "feature": feature,
                "mean_discovery": means.loc[feature],
                "sd_discovery": sds.loc[feature],
            }
            for feature in feats
        )
    scale_df = pd.DataFrame(scale_rows)
    scale_df.to_csv(PHASE1B / "phase1b_feature_scalers.tsv", sep="\t", index=False)
    return scaled, scale_df


def to_mofa_long(scaled: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for view, mat in scaled.items():
        long = mat.reset_index().melt(id_vars="patient_id", var_name="feature", value_name="value")
        long = long.rename(columns={"patient_id": "sample"})
        long["sample"] = long["sample"].astype(str)
        long["view"] = view
        long["group"] = "discovery"
        rows.append(long[["sample", "feature", "view", "group", "value"]])
    out = pd.concat(rows, ignore_index=True)
    if out["value"].isna().any():
        raise ValueError("MOFA input still contains missing values after complete-case feature filtering.")
    return out


def run_mofa_model(long_df: pd.DataFrame, seed: int, outfile: Path) -> None:
    code = f"""
from mofapy2.run.entry_point import entry_point
import pandas as pd
data = pd.read_pickle({str(PHASE1B / '_mofa_long.pkl')!r})
ent = entry_point()
ent.set_data_options(center_groups=True, scale_views=False, use_float32=True)
ent.set_data_df(data)
ent.set_model_options(factors={N_FACTORS}, spikeslab_weights=True, ard_weights=True)
ent.set_train_options(iter=600, startELBO=1, freqELBO=20, convergence_mode='fast',
                      seed={seed}, quiet=True, outfile={str(outfile)!r})
ent.build()
ent.run()
ent.save({str(outfile)!r})
"""
    long_df.to_pickle(PHASE1B / "_mofa_long.pkl")
    subprocess.run([str(ROOT / "environment" / "phase1b_venv" / "bin" / "python"), "-c", code], check=True)


def read_mofa(outfile: Path) -> dict:
    with h5py.File(outfile, "r") as h:
        views = [x.decode() if isinstance(x, bytes) else str(x) for x in h["views/views"][()]]
        samples = [x.decode() if isinstance(x, bytes) else str(x) for x in h["samples/discovery"][()]]
        z = h["expectations/Z/discovery"][()].T
        weights = {}
        features = {}
        for view in views:
            feats = [x.decode() if isinstance(x, bytes) else str(x) for x in h[f"features/{view}"][()]]
            weights[view] = pd.DataFrame(
                h[f"expectations/W/{view}"][()].T,
                index=feats,
                columns=[f"F{i+1}" for i in range(z.shape[1])],
            )
            features[view] = feats
        r2 = pd.DataFrame(
            h["variance_explained/r2_per_factor/discovery"][()],
            index=views,
            columns=[f"F{i+1}" for i in range(z.shape[1])],
        )
        elbo = h["training_stats/elbo"][()]
    scores = pd.DataFrame(z, index=samples, columns=[f"F{i+1}" for i in range(z.shape[1])])
    return {"views": views, "samples": samples, "scores": scores, "weights": weights, "r2": r2, "elbo": elbo}


def align_to_reference(models: dict[int, dict]) -> tuple[dict[int, dict], pd.DataFrame]:
    ref_seed = SEEDS[0]
    ref = models[ref_seed]["scores"]
    rows = []
    aligned = {ref_seed: models[ref_seed]}
    for seed, model in models.items():
        if seed == ref_seed:
            continue
        corr = np.zeros((N_FACTORS, N_FACTORS))
        for i, rf in enumerate(ref.columns):
            for j, sf in enumerate(model["scores"].columns):
                corr[i, j] = abs(_safe_corr(ref[rf].to_numpy(), model["scores"][sf].to_numpy()))
        row_ind, col_ind = linear_sum_assignment(-corr)
        mapping = {model["scores"].columns[j]: ref.columns[i] for i, j in zip(row_ind, col_ind)}
        sign = {}
        for i, j in zip(row_ind, col_ind):
            r = _safe_corr(ref.iloc[:, i].to_numpy(), model["scores"].iloc[:, j].to_numpy())
            sign[model["scores"].columns[j]] = 1 if r >= 0 else -1
            rows.append(
                {
                    "seed": seed,
                    "reference_factor": ref.columns[i],
                    "matched_factor": model["scores"].columns[j],
                    "score_abs_pearson": abs(r),
                    "score_signed_pearson_after_alignment": abs(r),
                }
            )
        new_scores = pd.DataFrame(index=model["scores"].index)
        new_weights = {v: pd.DataFrame(index=w.index) for v, w in model["weights"].items()}
        new_r2 = pd.DataFrame(index=model["r2"].index)
        for source_factor, target_factor in mapping.items():
            s = sign[source_factor]
            new_scores[target_factor] = model["scores"][source_factor] * s
            for view, w in model["weights"].items():
                new_weights[view][target_factor] = w[source_factor] * s
            new_r2[target_factor] = model["r2"][source_factor]
        new_scores = new_scores[ref.columns]
        for view in new_weights:
            new_weights[view] = new_weights[view][ref.columns]
        new_r2 = new_r2[ref.columns]
        aligned[seed] = {**model, "scores": new_scores, "weights": new_weights, "r2": new_r2}
    return aligned, pd.DataFrame(rows)


def summarize_stability(models: dict[int, dict], selected: pd.DataFrame) -> pd.DataFrame:
    ref_seed = SEEDS[0]
    ref = models[ref_seed]
    rows = []
    for factor in [f"F{i+1}" for i in range(N_FACTORS)]:
        score_corrs = []
        loading_corrs = []
        top_overlaps = []
        for seed in SEEDS[1:]:
            score_corrs.append(abs(_safe_corr(ref["scores"][factor].to_numpy(), models[seed]["scores"][factor].to_numpy())))
            for view in ["LS", "NL", "BLD"]:
                a = ref["weights"][view][factor]
                b = models[seed]["weights"][view][factor].reindex(a.index)
                loading_corrs.append(abs(_safe_corr(a.to_numpy(), b.to_numpy(), "spearman")))
                n_top = min(75, len(a))
                atop = set(a.abs().sort_values(ascending=False).head(n_top).index)
                btop = set(b.abs().sort_values(ascending=False).head(n_top).index)
                top_overlaps.append(len(atop & btop) / max(1, len(atop | btop)))
        mean_r2 = ref["r2"][factor].mean()
        median_score = float(np.nanmedian(score_corrs))
        median_loading = float(np.nanmedian(loading_corrs))
        median_overlap = float(np.nanmedian(top_overlaps))
        if median_score >= 0.75 and median_loading >= 0.55 and mean_r2 >= 0.01:
            status = "robust"
        elif median_score >= 0.50 and median_loading >= 0.35 and mean_r2 >= 0.005:
            status = "intermediate"
        else:
            status = "unstable"
        rows.append(
            {
                "factor": factor,
                "median_score_abs_pearson_vs_seed1": median_score,
                "median_loading_abs_spearman_vs_seed1": median_loading,
                "median_top75_jaccard_vs_seed1": median_overlap,
                "mean_view_r2_reference": mean_r2,
                "stability_status": status,
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(PHASE1B / "factor_stability.tsv", sep="\t", index=False)
    return out


def write_scores_and_loadings(model: dict, stability: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    scores = model["scores"].reset_index().rename(columns={"index": "patient_id"})
    scores.to_csv(PHASE1B / "molecular_axis_scores_discovery.tsv", sep="\t", index=False)
    rows = []
    for view, w in model["weights"].items():
        for feature, vals in w.iterrows():
            family = feature.split("::", 1)[0] if "::" in feature else "unknown"
            name = feature.split("::", 1)[1] if "::" in feature else feature
            for factor, loading in vals.items():
                rows.append(
                    {
                        "factor": factor,
                        "view": view,
                        "feature": feature,
                        "feature_family": family,
                        "feature_name": name,
                        "loading": loading,
                        "abs_loading_rank_within_factor_view": np.nan,
                    }
                )
    loadings = pd.DataFrame(rows)
    loadings["abs_loading_rank_within_factor_view"] = (
        loadings.groupby(["factor", "view"])["loading"].transform(lambda s: s.abs().rank(ascending=False, method="first"))
    )
    loadings.to_csv(PHASE1B / "factor_loadings.tsv", sep="\t", index=False)
    return scores, loadings


def annotate_biology(loadings: pd.DataFrame, r2: pd.DataFrame, stability: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for factor in sorted(loadings["factor"].unique(), key=lambda x: int(x[1:])):
        sub = loadings[loadings["factor"] == factor].copy()
        top = sub.sort_values("loading", key=lambda s: s.abs(), ascending=False).head(90)
        fam_counts = top["feature_family"].value_counts().to_dict()
        top_pos = top.sort_values("loading", ascending=False).head(10)
        top_neg = top.sort_values("loading", ascending=True).head(10)
        multi_family = sum(v >= 5 for v in fam_counts.values()) >= 2
        rows.append(
            {
                "factor": factor,
                "stability_status": stability.set_index("factor").loc[factor, "stability_status"],
                "BLD_r2": r2.loc["BLD", factor],
                "LS_r2": r2.loc["LS", factor],
                "NL_r2": r2.loc["NL", factor],
                "dominant_view": r2[factor].idxmax(),
                "top_feature_families": json.dumps(fam_counts, ensure_ascii=False),
                "top_positive_features": "; ".join(top_pos["view"] + "::" + top_pos["feature"]),
                "top_negative_features": "; ".join(top_neg["view"] + "::" + top_neg["feature"]),
                "biology_label_status": "labelable_multifamily" if multi_family else "descriptive_only_single_family_or_diffuse",
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(PHASE1B / "factor_biology.tsv", sep="\t", index=False)
    return out


def project_skin(replication_views: dict[str, pd.DataFrame], scale_df: pd.DataFrame, model: dict) -> pd.DataFrame:
    rows = []
    for cohort, views in [("replication", replication_views)]:
        common_patients = sorted(set(views["LS"].index) & set(views["NL"].index))
        factor_scores = pd.DataFrame(index=common_patients)
        for factor in [f"F{i+1}" for i in range(N_FACTORS)]:
            numer = np.zeros(len(common_patients))
            denom = 0.0
            for view in ["LS", "NL"]:
                scalers = scale_df[scale_df["view"] == view].set_index("feature")
                features = [f for f in model["weights"][view].index if f in views[view].columns and f in scalers.index]
                if not features:
                    continue
                mat = views[view].loc[common_patients, features].astype(float)
                mat = (mat - scalers.loc[features, "mean_discovery"]) / scalers.loc[features, "sd_discovery"]
                weights = model["weights"][view].loc[features, factor].to_numpy()
                numer += mat.to_numpy().dot(weights)
                denom += float(np.sum(np.abs(weights)))
            factor_scores[factor] = numer / denom if denom else np.nan
        factor_scores = factor_scores.reset_index().rename(columns={"index": "patient_id"})
        factor_scores["cohort"] = cohort
        rows.append(factor_scores)
    out = pd.concat(rows, ignore_index=True)
    out.to_csv(PHASE1B / "replication_ETAB14509_axis_projection.tsv", sep="\t", index=False)
    return out


def internal_skin_replication(discovery_views, replication_views, scale_df, model, projected) -> pd.DataFrame:
    rows = []
    for factor in [f"F{i+1}" for i in range(N_FACTORS)]:
        for view in ["LS", "NL"]:
            w = model["weights"][view][factor]
            common = [f for f in w.index if f in replication_views[view].columns and f in discovery_views[view].columns]
            rep_effect = replication_views[view][common].mean(axis=0) - discovery_views[view][common].mean(axis=0)
            rows.append(
                {
                    "factor": factor,
                    "view": view,
                    "n_common_features": len(common),
                    "loading_vs_replication_mean_shift_spearman": _safe_corr(w.loc[common].to_numpy(), rep_effect.to_numpy(), "spearman"),
                    "replication_projected_score_mean": projected[factor].mean(),
                    "replication_projected_score_sd": projected[factor].std(ddof=0),
                }
            )
    out = pd.DataFrame(rows)
    out.to_csv(PHASE1B / "replication_ETAB14509.tsv", sep="\t", index=False)
    return out


def cross_tissue_support(scaled: dict[str, pd.DataFrame], model: dict) -> pd.DataFrame:
    rows = []
    for factor in [f"F{i+1}" for i in range(N_FACTORS)]:
        scores_by_view = {}
        for view in ["LS", "NL", "BLD"]:
            mat = scaled[view][model["weights"][view].index]
            w = model["weights"][view][factor].to_numpy()
            denom = np.sum(np.abs(w))
            scores_by_view[view] = mat.to_numpy().dot(w) / denom if denom else np.repeat(np.nan, mat.shape[0])
        skin_score = (scores_by_view["LS"] + scores_by_view["NL"]) / 2
        rows.append(
            {
                "factor": factor,
                "skin_weighted_score_vs_blood_weighted_score_pearson": _safe_corr(skin_score, scores_by_view["BLD"]),
                "skin_weighted_score_vs_blood_weighted_score_spearman": _safe_corr(skin_score, scores_by_view["BLD"], "spearman"),
                "BLD_view_r2": model["r2"].loc["BLD", factor],
                "LS_view_r2": model["r2"].loc["LS", factor],
                "NL_view_r2": model["r2"].loc["NL", factor],
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(PHASE1B / "cross_tissue_discovery_support.tsv", sep="\t", index=False)
    return out


def confounding(scores: pd.DataFrame) -> pd.DataFrame:
    meta = pd.read_csv(ROOT / "results" / "tables" / "Table_S1_sample_metadata_audit.tsv", sep="\t")
    meta["patient_id"] = meta["patient_id"].astype(str)
    base = meta[(meta["cohort"] == "discovery") & (meta["baseline"] == True)].drop_duplicates("patient_id")
    covars = ["pasi", "bmi", "age", "sex", "hla_c0602_carrier"]
    dat = scores.merge(base[["patient_id"] + covars], on="patient_id", how="left")
    rows = []
    for factor in [c for c in scores.columns if c.startswith("F")]:
        for covar in covars:
            sub = dat[["patient_id", factor] + covars].dropna()
            if sub.shape[0] < 20 or sub[covar].nunique() < 2:
                rows.append({"factor": factor, "covariate": covar, "n": sub.shape[0], "beta": np.nan, "pvalue": np.nan, "partial_r2": np.nan})
                continue
            y = sub[factor].to_numpy(float)
            X_full = sub[covars].to_numpy(float)
            X_full = StandardScaler().fit_transform(X_full)
            y_std = (y - y.mean()) / (y.std(ddof=0) or 1)
            X_design = np.column_stack([np.ones(len(y_std)), X_full])
            beta = np.linalg.lstsq(X_design, y_std, rcond=None)[0]
            pred = X_design.dot(beta)
            sse_full = np.sum((y_std - pred) ** 2)
            sst = np.sum((y_std - y_std.mean()) ** 2)
            r2_full = 1 - sse_full / sst if sst else np.nan
            j = covars.index(covar) + 1
            X_red = np.delete(X_design, j, axis=1)
            beta_red = np.linalg.lstsq(X_red, y_std, rcond=None)[0]
            sse_red = np.sum((y_std - X_red.dot(beta_red)) ** 2)
            partial = max(0.0, (sse_red - sse_full) / sse_red) if sse_red else np.nan
            dof = len(y_std) - X_design.shape[1]
            mse = sse_full / dof if dof > 0 else np.nan
            cov = np.linalg.pinv(X_design.T.dot(X_design)) * mse
            se = math.sqrt(cov[j, j]) if np.isfinite(cov[j, j]) and cov[j, j] >= 0 else np.nan
            t = beta[j] / se if se and np.isfinite(se) else np.nan
            from scipy.stats import t as tdist

            p = 2 * tdist.sf(abs(t), dof) if np.isfinite(t) and dof > 0 else np.nan
            rows.append({"factor": factor, "covariate": covar, "n": len(y_std), "beta": beta[j], "pvalue": p, "partial_r2": partial, "full_model_r2": r2_full})
    out = pd.DataFrame(rows)
    out["fdr"] = bh_fdr(out["pvalue"])
    out.to_csv(PHASE1B / "factor_confounding.tsv", sep="\t", index=False)
    return out


def axes_vs_clusters(scores: pd.DataFrame, stability: pd.DataFrame) -> pd.DataFrame:
    assign = pd.read_csv(ROOT / "results" / "phase1" / "frozen_endotype_assignments.tsv", sep="\t")
    assign["patient_id"] = assign["patient_id"].astype(str)
    dat = scores.merge(assign[assign["cohort"] == "discovery"], on="patient_id", how="inner")
    factor_cols = [c for c in scores.columns if c.startswith("F")]
    rows = []
    y = (dat["endotype"] == sorted(dat["endotype"].unique())[-1]).astype(int).to_numpy()
    if dat["endotype"].nunique() == 2 and len(dat) >= 30:
        clf = LogisticRegression(max_iter=1000, solver="liblinear")
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=20260810)
        prob = cross_val_predict(clf, dat[factor_cols], y, cv=cv, method="predict_proba")[:, 1]
        auc = roc_auc_score(y, prob)
    else:
        auc = np.nan
    for factor in factor_cols:
        g = dat.groupby("endotype")[factor]
        means = g.mean()
        between = means.max() - means.min() if len(means) else np.nan
        total_var = dat[factor].var(ddof=0)
        within = g.var(ddof=0).mean()
        rows.append(
            {
                "factor": factor,
                "cluster_auc_from_all_axes_cv": auc,
                "endotype_mean_range_on_axis": between,
                "within_endotype_variance_mean": within,
                "total_axis_variance": total_var,
                "fraction_axis_variance_left_within_clusters": within / total_var if total_var else np.nan,
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(PHASE1B / "axes_vs_clusters.tsv", sep="\t", index=False)
    return out


def write_report(stability, biology, replication, cross_tissue, confound, axes_clusters) -> None:
    n_modeled = len(pd.read_csv(PHASE1B / "molecular_axis_scores_discovery.tsv", sep="\t"))
    go = (
        (stability["stability_status"].isin(["robust", "intermediate"]).sum() >= 2)
        and (replication["loading_vs_replication_mean_shift_spearman"].abs().max() >= 0.20)
    )
    lines = [
        "# PHASE 1B Molecular Axis Report",
        "",
        "## Executive decision",
        "",
        f"Phase 1B decision: **{'CONDITIONAL GO' if go else 'HOLD / NEEDS REVIEW'}**.",
        "",
        "Discrete k=2 endotypes remain documented as a secondary summary because their bootstrap stability did not meet the prespecified threshold. Continuous discovery-only molecular axes are treated as the primary molecular phenotype for downstream design decisions.",
        "",
        "## Inputs and lock",
        "",
        f"- Discovery patients modeled: {n_modeled}",
        f"- Views: lesional skin, nonlesional skin, blood.",
        f"- Feature filter: top {TOP_PER_VIEW} complete, nonconstant discovery features per view by within-view standard deviation.",
        f"- MOFA seeds: {', '.join(map(str, SEEDS))}; initial factors: {N_FACTORS}.",
        "",
        "## Factor stability",
        "",
        stability.to_markdown(index=False),
        "",
        "## Biological annotation",
        "",
        biology[["factor", "stability_status", "dominant_view", "BLD_r2", "LS_r2", "NL_r2", "biology_label_status", "top_positive_features", "top_negative_features"]].to_markdown(index=False),
        "",
        "## Internal skin replication",
        "",
        replication.to_markdown(index=False),
        "",
        "## Discovery cross-tissue blood support",
        "",
        cross_tissue.to_markdown(index=False),
        "",
        "## Clinical/confounding audit",
        "",
        "Associations are multivariable standardized OLS coefficients for each axis against PASI, BMI, age, sex, and HLA-C*06:02 carrier status. These are not used to choose axes.",
        "",
        confound.sort_values("pvalue").head(20).to_markdown(index=False),
        "",
        "## Axes versus discrete clusters",
        "",
        axes_clusters.to_markdown(index=False),
        "",
        "## Interpretation boundary",
        "",
        "Phase 1B supports axis-based rescue if at least two axes show nontrivial stability and interpretable multi-view biology. Blood support remains discovery-only because E-MTAB-14509 replication lacks blood RNA-seq; external blood datasets require separate platform-specific processing before they can be treated as replication rather than support.",
        "",
    ]
    (REPORTS / "PHASE1B_MOLECULAR_AXIS_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    PHASE1B.mkdir(parents=True, exist_ok=True)
    discovery, replication = load_feature_matrices()
    discovery_views = split_views(discovery)
    discovery_views = restrict_to_common_available_patients(discovery_views)
    replication_views = split_views(replication)
    selected = select_features(discovery_views)
    scaled, scale_df = scale_discovery_views(discovery_views, selected)
    long_df = to_mofa_long(scaled)
    long_df.to_csv(PHASE1B / "mofa_input_long_manifest.tsv", sep="\t", index=False)

    models = {}
    for seed in SEEDS:
        outfile = PHASE1B / f"mofa_seed_{seed}.hdf5"
        if not outfile.exists():
            run_mofa_model(long_df, seed, outfile)
        models[seed] = read_mofa(outfile)
    models, alignment = align_to_reference(models)
    alignment.to_csv(PHASE1B / "factor_seed_alignment.tsv", sep="\t", index=False)
    stability = summarize_stability(models, selected)
    scores, loadings = write_scores_and_loadings(models[SEEDS[0]], stability)
    biology = annotate_biology(loadings, models[SEEDS[0]]["r2"], stability)
    projected = project_skin(replication_views, scale_df, models[SEEDS[0]])
    replication_summary = internal_skin_replication(discovery_views, replication_views, scale_df, models[SEEDS[0]], projected)
    cross_tissue = cross_tissue_support(scaled, models[SEEDS[0]])
    confound = confounding(scores)
    axes_clusters = axes_vs_clusters(scores, stability)
    write_report(stability, biology, replication_summary, cross_tissue, confound, axes_clusters)


if __name__ == "__main__":
    main()
