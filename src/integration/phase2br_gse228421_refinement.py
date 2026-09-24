#!/usr/bin/env python3
"""Phase 2B-R one-pass marker/reference refinement for GSE228421."""

from __future__ import annotations

import gzip
import itertools
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse
from scipy.io import mmread
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "external" / "geo" / "GSE228421_10x"
META = ROOT / "results" / "phase2b" / "GSE228421_sample_metadata.tsv"
P2A = ROOT / "results" / "phase2a" / "axis_gene_programs"
OUT = ROOT / "results" / "phase2br"
REPORT = ROOT / "reports" / "PHASE2BR_GSE228421_REFINEMENT.md"

AXES = ["F1", "F2", "F6", "F7"]
PROGRAM_TYPES = ["CORE", "EXTENDED"]

REFINED_MARKERS = {
    "keratinocyte_basal": ["KRT5", "KRT14", "KRT15", "TP63", "ITGA6", "COL17A1"],
    "keratinocyte_spinous_suprabasal": ["KRT1", "KRT10", "DSG1", "DSC1", "FLG", "LOR"],
    "keratinocyte_proliferative": ["MKI67", "TOP2A", "TYMS", "PCNA", "UBE2C", "STMN1"],
    "keratinocyte_inflammatory_T17": ["KRT16", "KRT17", "S100A7", "S100A8", "S100A9", "DEFB4A", "IL36G", "CXCL8"],
    "keratinocyte_IFN_response": ["ISG15", "IFIT1", "IFIT2", "IFIT3", "MX1", "OAS1", "STAT1"],
    "keratinocyte_stress_hypoxia": ["HIF1A", "VEGFA", "DDIT4", "NDRG1", "SLC2A1", "ADM", "BNIP3"],
    "fibroblast_homeostatic_matrix": ["COL1A1", "COL1A2", "COL3A1", "DCN", "LUM", "PDGFRA"],
    "fibroblast_inflammatory": ["CCL19", "CCL13", "CXCL12", "CXCL14", "IL6", "PDPN", "FAP"],
    "endothelial_vascular": ["PECAM1", "VWF", "KDR", "RAMP2", "CLDN5", "ENG"],
    "endothelial_activated": ["ACKR1", "SELE", "ICAM1", "VCAM1", "CCL21", "CLU"],
    "myeloid_monocyte_macrophage": ["LYZ", "LST1", "CTSS", "CD14", "FCGR3A", "TYROBP", "AIF1"],
    "dendritic_LAMP3_CCR7": ["LAMP3", "CCR7", "CCL19", "CD83", "FSCN1", "BIRC3"],
    "T_cell_TRM_T17_like": ["CD3D", "CD3E", "TRAC", "IL7R", "CD69", "CXCR6", "CCR6", "IL23R"],
    "cytotoxic_NK_T": ["NKG7", "GNLY", "PRF1", "GZMB", "KLRD1", "CX3CR1"],
    "B_cell_plasma": ["MS4A1", "CD79A", "CD79B", "BANK1", "MZB1", "JCHAIN"],
    "mast_cell": ["TPSAB1", "TPSB2", "CPA3", "KIT"],
}

COARSE_ALLOWED = {
    "keratinocyte": {
        "keratinocyte_basal",
        "keratinocyte_spinous_suprabasal",
        "keratinocyte_proliferative",
        "keratinocyte_inflammatory_T17",
        "keratinocyte_IFN_response",
        "keratinocyte_stress_hypoxia",
    },
    "fibroblast": {"fibroblast_homeostatic_matrix", "fibroblast_inflammatory"},
    "endothelial": {"endothelial_vascular", "endothelial_activated"},
    "myeloid_monocyte": {"myeloid_monocyte_macrophage", "dendritic_LAMP3_CCR7"},
    "dendritic": {"dendritic_LAMP3_CCR7", "myeloid_monocyte_macrophage"},
    "T_cell": {"T_cell_TRM_T17_like", "cytotoxic_NK_T"},
    "NK_cell": {"cytotoxic_NK_T", "T_cell_TRM_T17_like"},
    "B_cell": {"B_cell_plasma"},
    "mast_cell": {"mast_cell"},
}


def read_tsv_gz(path: Path) -> list[list[str]]:
    with gzip.open(path, "rt", errors="replace") as handle:
        return [line.rstrip("\n").split("\t") for line in handle]


def sample_paths(gsm: str) -> tuple[Path, Path, Path]:
    sample_dir = RAW / gsm
    return (
        next(sample_dir.glob("*.barcodes.tsv.gz")),
        next(sample_dir.glob("*.features.tsv.gz")),
        next(sample_dir.glob("*.matrix.mtx.gz")),
    )


def mean_log_cpm_scores(x: sparse.csr_matrix, gene_symbols: list[str], gene_set: set[str], lib: np.ndarray) -> np.ndarray:
    idx = [i for i, gene in enumerate(gene_symbols) if gene in gene_set]
    if len(idx) < 2:
        return np.full(x.shape[1], np.nan)
    sub = x[idx, :].tocsc(copy=True)
    scale = np.divide(10000.0, lib, out=np.zeros_like(lib, dtype=float), where=lib > 0)
    sub = sub @ sparse.diags(scale)
    sub.data = np.log1p(sub.data)
    return np.asarray(sub.sum(axis=0)).ravel() / len(idx)


def load_programs() -> dict[str, dict[str, set[str]]]:
    programs = {}
    for axis in AXES:
        df = pd.read_csv(P2A / f"{axis}_gene_program.tsv", sep="\t")
        programs[axis] = {
            "CORE": set(df.loc[df["leading_edge_status"].eq("CORE"), "gene_symbol"].astype(str).str.upper()),
            "EXTENDED": set(df["gene_symbol"].astype(str).str.upper()),
        }
    return programs


def assign_refined_state(coarse: str, marker_scores: pd.Series) -> tuple[str, float, str, float]:
    if coarse not in COARSE_ALLOWED:
        return f"{coarse}_unresolved", np.nan, "unresolved", np.nan
    allowed = COARSE_ALLOWED[coarse]
    subset = marker_scores.loc[[state for state in marker_scores.index if state in allowed]].dropna()
    if subset.empty or subset.max() <= 0:
        return f"{coarse}_unresolved", np.nan, "unresolved", np.nan
    ranked = subset.sort_values(ascending=False)
    secondary = ranked.index[1] if len(ranked) > 1 else "none"
    secondary_score = float(ranked.iloc[1]) if len(ranked) > 1 else np.nan
    return str(ranked.index[0]), float(ranked.iloc[0]), secondary, secondary_score


def process_sample(sample: pd.Series, existing: pd.DataFrame, programs: dict[str, dict[str, set[str]]]) -> pd.DataFrame:
    barcodes_path, features_path, matrix_path = sample_paths(sample["gsm"])
    barcodes = [row[0] for row in read_tsv_gz(barcodes_path)]
    features = read_tsv_gz(features_path)
    gene_symbols = [(row[1] if len(row) > 1 else row[0]).upper() for row in features]
    x = mmread(matrix_path).tocsr().astype(float)
    lib = np.asarray(x.sum(axis=0)).ravel()
    detected = np.asarray((x > 0).sum(axis=0)).ravel()
    mito_idx = [i for i, gene in enumerate(gene_symbols) if gene.startswith("MT-")]
    mito = np.asarray(x[mito_idx, :].sum(axis=0)).ravel() if mito_idx else np.zeros(x.shape[1])
    pct_mito = np.divide(mito, lib, out=np.zeros_like(lib), where=lib > 0) * 100
    keep = (lib >= 500) & (detected >= 200) & (pct_mito <= 25)
    x = x[:, keep]
    kept_barcodes = [barcodes[i] for i, flag in enumerate(keep) if flag]
    lib = lib[keep]

    marker_scores = {}
    for state, genes in REFINED_MARKERS.items():
        marker_scores[state] = mean_log_cpm_scores(x, gene_symbols, {g.upper() for g in genes}, lib)
    marker_df = pd.DataFrame(marker_scores)

    axis_scores = {}
    for axis, axis_programs in programs.items():
        for program_type, genes in axis_programs.items():
            axis_scores[f"{axis}_{program_type}"] = mean_log_cpm_scores(x, gene_symbols, genes, lib)
    axis_df = pd.DataFrame(axis_scores)
    axis_df["cell_barcode"] = kept_barcodes
    axis_df["gsm"] = sample["gsm"]
    axis_df["cell_id"] = [f"{sample['gsm']}:{barcode}" for barcode in kept_barcodes]

    base = existing.loc[existing["gsm"].eq(sample["gsm"]), ["cell_id", "cell_type"]].copy()
    axis_df = axis_df.merge(base, on="cell_id", how="left")
    axis_df["cell_type"] = axis_df["cell_type"].fillna("unassigned")

    refined = [assign_refined_state(coarse, marker_df.iloc[i]) for i, coarse in enumerate(axis_df["cell_type"])]
    refined_df = pd.DataFrame(refined, columns=["refined_state", "refined_marker_score", "secondary_refined_state", "secondary_refined_marker_score"])
    marker_df = marker_df.add_prefix("marker_")

    for col in ["donor_id", "timepoint", "tissue_state", "baseline_primary"]:
        axis_df[col] = sample[col]
    return pd.concat([axis_df, refined_df, marker_df.reset_index(drop=True)], axis=1)


def bh_fdr(p: pd.Series) -> pd.Series:
    vals = pd.to_numeric(p, errors="coerce")
    out = pd.Series(np.nan, index=p.index)
    mask = vals.notna()
    if mask.sum() == 0:
        return out
    order = vals[mask].sort_values().index
    ranked = vals.loc[order].to_numpy()
    m = len(ranked)
    adj = np.minimum.accumulate((ranked * m / np.arange(1, m + 1))[::-1])[::-1]
    out.loc[order] = np.clip(adj, 0, 1)
    return out


def paired_signflip_p(diffs: np.ndarray) -> float:
    diffs = diffs[np.isfinite(diffs)]
    if len(diffs) == 0:
        return np.nan
    obs = abs(diffs.mean())
    vals = [abs((diffs * np.array(signs)).mean()) for signs in itertools.product([-1, 1], repeat=len(diffs))]
    return float((np.sum(np.asarray(vals) >= obs) + 1) / (len(vals) + 1))


def bootstrap_ci(diffs: np.ndarray, n_iter: int = 2000, seed: int = 20260811) -> tuple[float, float]:
    diffs = diffs[np.isfinite(diffs)]
    if len(diffs) == 0:
        return np.nan, np.nan
    rng = np.random.default_rng(seed)
    vals = [rng.choice(diffs, size=len(diffs), replace=True).mean() for _ in range(n_iter)]
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def summarize(cells: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    score_cols = [f"{axis}_{program_type}" for axis in AXES for program_type in PROGRAM_TYPES]
    donor_state = (
        cells.groupby(["donor_id", "gsm", "timepoint", "tissue_state", "baseline_primary", "cell_type", "refined_state"])[score_cols]
        .agg(["mean", "count"])
        .reset_index()
    )
    donor_state.columns = [f"{a}_{b}" if b else a for a, b in donor_state.columns]

    baseline = donor_state[donor_state["baseline_primary"].eq(True)]
    rows = []
    for axis in AXES:
        for program_type in PROGRAM_TYPES:
            col = f"{axis}_{program_type}_mean"
            for refined_state, sub in baseline.groupby("refined_state"):
                wide = sub.pivot_table(index="donor_id", columns="tissue_state", values=col, aggfunc="mean")
                if {"lesional", "nonlesional"} <= set(wide.columns):
                    diffs = (wide["lesional"] - wide["nonlesional"]).dropna().to_numpy()
                    ci_low, ci_high = bootstrap_ci(diffs)
                    rows.append(
                        {
                            "axis": axis,
                            "program_type": program_type,
                            "refined_state": refined_state,
                            "parent_cell_type": sub["cell_type"].mode().iloc[0],
                            "n_donors": len(diffs),
                            "mean_LS_minus_NL": float(np.mean(diffs)) if len(diffs) else np.nan,
                            "bootstrap_ci_low": ci_low,
                            "bootstrap_ci_high": ci_high,
                            "signflip_p": paired_signflip_p(diffs),
                            "mean_cells_per_donor_state": float(sub.filter(like="_count").mean().mean()),
                        }
                    )
    stats = pd.DataFrame(rows)
    stats["fdr_by_program_type"] = stats.groupby("program_type")["signflip_p"].transform(bh_fdr)

    loc_rows = []
    base_cells = cells[cells["baseline_primary"].eq(True)]
    for axis in AXES:
        for program_type in PROGRAM_TYPES:
            col = f"{axis}_{program_type}"
            means = base_cells.groupby(["donor_id", "refined_state", "cell_type"])[col].mean().reset_index()
            summary = (
                means.groupby(["refined_state", "cell_type"])[col]
                .agg(["mean", "std", "count"])
                .reset_index()
                .sort_values("mean", ascending=False)
            )
            top = summary.iloc[0]
            second = summary.iloc[1] if len(summary) > 1 else top
            loc_rows.append(
                {
                    "axis": axis,
                    "program_type": program_type,
                    "dominant_refined_state": top["refined_state"],
                    "dominant_parent_cell_type": top["cell_type"],
                    "dominant_mean_score": top["mean"],
                    "secondary_refined_state": second["refined_state"],
                    "secondary_mean_score": second["mean"],
                    "specificity_delta_vs_second": top["mean"] - second["mean"],
                    "n_refined_states_observed": len(summary),
                }
            )
    localization = pd.DataFrame(loc_rows)
    return donor_state, stats, localization


def final_table(stats: pd.DataFrame, localization: pd.DataFrame, cells: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for axis in AXES:
        core_loc = localization[(localization["axis"].eq(axis)) & (localization["program_type"].eq("CORE"))].iloc[0]
        core_stats = stats[(stats["axis"].eq(axis)) & (stats["program_type"].eq("CORE")) & (stats["n_donors"].ge(4))].copy()
        if axis == "F7":
            keep = core_stats["parent_cell_type"].isin(["T_cell", "NK_cell", "B_cell", "myeloid_monocyte", "dendritic"])
            if keep.any():
                core_stats = core_stats.loc[keep]
        core_stats = core_stats.sort_values(["mean_LS_minus_NL", "mean_cells_per_donor_state"], ascending=[False, False])
        best = core_stats.iloc[0] if not core_stats.empty else pd.Series(dtype=object)
        core = cells.groupby(["donor_id", "timepoint", "tissue_state", "refined_state"])[f"{axis}_CORE"].mean()
        ext = cells.groupby(["donor_id", "timepoint", "tissue_state", "refined_state"])[f"{axis}_EXTENDED"].mean()
        common = core.dropna().index.intersection(ext.dropna().index)
        rho = spearmanr(core.loc[common], ext.loc[common]).correlation if len(common) >= 5 else np.nan
        fdr = best.get("fdr_by_program_type", np.nan)
        ci_low = best.get("bootstrap_ci_low", np.nan)
        ci_high = best.get("bootstrap_ci_high", np.nan)
        confidence = "LOW"
        if pd.notna(fdr) and fdr <= 0.20 and pd.notna(rho) and rho >= 0.5 and ci_low > 0:
            confidence = "MODERATE"
        if pd.notna(fdr) and fdr <= 0.10 and pd.notna(rho) and rho >= 0.7 and ci_low > 0:
            confidence = "HIGH"
        rows.append(
            {
                "axis": axis,
                "dominant_refined_state": best.get("refined_state", core_loc["dominant_refined_state"]),
                "parent_cell_type": best.get("parent_cell_type", core_loc["dominant_parent_cell_type"]),
                "localization_by_score": core_loc["dominant_refined_state"],
                "donor_effect_LS_minus_NL": best.get("mean_LS_minus_NL", np.nan),
                "bootstrap_ci_low": ci_low,
                "bootstrap_ci_high": ci_high,
                "fdr": fdr,
                "core_extended_state_spearman": rho,
                "interpretation_after_refinement": "refined directional localization" if confidence == "LOW" else "refined donor-level candidate",
                "confidence": confidence,
            }
        )
    return pd.DataFrame(rows)


def write_report(cells: pd.DataFrame, stats: pd.DataFrame, localization: pd.DataFrame, final: pd.DataFrame) -> None:
    go = "NO-GO / SHRINK"
    if final["confidence"].isin(["MODERATE", "HIGH"]).sum() >= 3:
        go = "STRONG GO TO GENETICS"
    elif final["confidence"].isin(["MODERATE", "HIGH"]).sum() >= 2:
        go = "CONDITIONAL GO"
    lines = [
        "# PHASE 2B-R GSE228421 Refinement",
        "",
        "## 结论",
        "",
        f"{go}. 本轮只做一次 marker/reference 精修：不重新聚类、不重拟合轴、不修改 F1/F2/F6/F7 CORE/EXTENDED gene programs。",
        "",
        "## 分析边界",
        "",
        f"- QC-passing cells scored: {cells.shape[0]}",
        f"- Donors: {cells['donor_id'].nunique()}",
        "- Primary inference: donor-level baseline lesional versus nonlesional summaries.",
        "- Refined states are marker-defined labels within coarse Phase 2B cell types, not newly optimized clusters.",
        "",
        "## Final refined localization",
        "",
        final.to_markdown(index=False),
        "",
        "## Score-based localization",
        "",
        localization.to_markdown(index=False),
        "",
        "## Donor-level refined-state statistics",
        "",
        stats.sort_values(["axis", "program_type", "fdr_by_program_type", "mean_LS_minus_NL"]).head(120).to_markdown(index=False),
        "",
        "## Phase 2B-R decision",
        "",
        "GSE228421 refinement remains bounded by 5 donors. A MODERATE/HIGH call requires donor-level effect, positive bootstrap CI, CORE/EXTENDED concordance, and FDR support. Axes that remain LOW after this refinement should not be rescued by further GSE228421 subclustering.",
    ]
    REPORT.write_text("\n".join(lines) + "\n")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = pd.read_csv(META, sep="\t")
    existing = pd.read_csv(ROOT / "results" / "phase2b" / "GSE228421_cell_axis_scores.tsv.gz", sep="\t", usecols=["cell_id", "gsm", "cell_type"])
    programs = load_programs()
    frames = []
    for _, sample in meta.iterrows():
        frames.append(process_sample(sample, existing, programs))
    cells = pd.concat(frames, ignore_index=True)
    cells.to_csv(OUT / "GSE228421_cell_axis_scores.tsv", sep="\t", index=False)
    donor_state, stats, localization = summarize(cells)
    donor_state.to_csv(OUT / "GSE228421_donor_refined_state_axis_scores.tsv", sep="\t", index=False)
    stats.to_csv(OUT / "GSE228421_refined_state_donor_statistics.tsv", sep="\t", index=False)
    localization.to_csv(OUT / "GSE228421_refined_state_score_localization.tsv", sep="\t", index=False)
    final = final_table(stats, localization, cells)
    final.to_csv(OUT / "GSE228421_refined_axis_localization.tsv", sep="\t", index=False)
    write_report(cells, stats, localization, final)
    print(final.to_string(index=False))


if __name__ == "__main__":
    main()
