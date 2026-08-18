#!/usr/bin/env python3
"""Phase 2C independent scRNA validation with GSE173706."""

from __future__ import annotations

import itertools
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "external" / "geo" / "GSE173706_csv"
OUT = ROOT / "results" / "phase2c"
REPORT = ROOT / "reports" / "PHASE2C_GSE173706_INDEPENDENT_SCRNA_VALIDATION.md"
META_PATH = OUT / "GSE173706_sample_metadata_audit.tsv"
SUPP_PATH = OUT / "dataset_supplementary_files.tsv"
MAP_PATH = ROOT / "results" / "phase1" / "ensembl_gene_symbol_map.tsv"
P2A = ROOT / "results" / "phase2a" / "axis_gene_programs"

AXES = ["F1", "F2", "F6", "F7"]
PROGRAM_TYPES = ["CORE", "EXTENDED"]

COARSE_MARKERS = {
    "keratinocyte": ["KRT14", "KRT5", "KRT1", "KRT10", "KRT16", "KRT17", "S100A7", "S100A8", "S100A9"],
    "fibroblast": ["COL1A1", "COL1A2", "COL3A1", "DCN", "LUM", "PDGFRA"],
    "endothelial": ["PECAM1", "VWF", "KDR", "CLDN5", "RAMP2"],
    "T_cell": ["CD3D", "CD3E", "TRAC", "CD4", "CD8A", "IL7R"],
    "myeloid_monocyte": ["LYZ", "LST1", "CTSS", "CD14", "FCGR3A", "TYROBP"],
    "dendritic": ["FCER1A", "CLEC10A", "CD1C", "LAMP3", "CCR7"],
    "B_cell": ["MS4A1", "CD79A", "CD79B", "BANK1", "CD74"],
    "NK_cell": ["NKG7", "GNLY", "KLRD1", "PRF1", "GZMB"],
    "mast_cell": ["TPSAB1", "TPSB2", "CPA3", "KIT"],
    "melanocyte": ["PMEL", "MLANA", "TYR", "DCT"],
}

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


def download_inputs() -> pd.DataFrame:
    RAW.mkdir(parents=True, exist_ok=True)
    meta = pd.read_csv(META_PATH, sep="\t")
    supp = pd.read_csv(SUPP_PATH, sep="\t")
    urls = supp[(supp["accession"].eq("GSE173706")) & (supp["level"].eq("sample"))][["sample_accession", "url"]]
    meta = meta.merge(urls, left_on="sample_accession", right_on="sample_accession", how="left")

    def fetch(row: pd.Series) -> dict[str, str | int]:
        url = row["url"].replace("ftp://ftp.ncbi.nlm.nih.gov", "https://ftp.ncbi.nlm.nih.gov")
        dest = RAW / url.rsplit("/", 1)[-1]
        if not dest.exists() or dest.stat().st_size == 0:
            tmp = dest.with_suffix(dest.suffix + ".partial")
            subprocess.run(
                [
                    "curl",
                    "-L",
                    "--fail",
                    "--silent",
                    "--show-error",
                    "--retry",
                    "8",
                    "--retry-all-errors",
                    "--connect-timeout",
                    "60",
                    "--max-time",
                    "300",
                    "--continue-at",
                    "-",
                    "-o",
                    str(tmp),
                    url,
                ],
                check=True,
            )
            tmp.rename(dest)
        return {"sample_accession": row["sample_accession"], "file": str(dest), "bytes": dest.stat().st_size}

    rows = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(fetch, row) for _, row in meta.iterrows()]
        for future in as_completed(futures):
            rows.append(future.result())
            if len(rows) % 5 == 0 or len(rows) == len(futures):
                print(f"Downloaded/checked {len(rows)}/{len(futures)} GSE173706 CSV files", flush=True)
    manifest = pd.DataFrame(rows)
    manifest.to_csv(OUT / "GSE173706_download_manifest.tsv", sep="\t", index=False)
    return meta.merge(manifest, on="sample_accession", how="left")


def load_programs() -> dict[str, dict[str, set[str]]]:
    programs = {}
    for axis in AXES:
        df = pd.read_csv(P2A / f"{axis}_gene_program.tsv", sep="\t")
        programs[axis] = {
            "CORE": set(df.loc[df["leading_edge_status"].eq("CORE"), "gene_symbol"].astype(str).str.upper()),
            "EXTENDED": set(df["gene_symbol"].astype(str).str.upper()),
        }
    return programs


def load_gene_map() -> dict[str, str]:
    df = pd.read_csv(MAP_PATH, sep="\t")
    return dict(zip(df["ensembl_gene"].astype(str), df["gene_symbol"].astype(str).str.upper()))


def mean_log_cpm(df: pd.DataFrame, genes: set[str], lib: pd.Series) -> np.ndarray:
    overlap = [gene for gene in df.index if gene in genes]
    if len(overlap) < 2:
        return np.full(df.shape[1], np.nan)
    sub = df.loc[overlap]
    vals = np.log1p(sub.div(lib.replace(0, np.nan), axis=1) * 10000)
    return vals.mean(axis=0).to_numpy()


def assign_cell_type(marker_scores: pd.DataFrame) -> pd.Series:
    best = marker_scores.idxmax(axis=1)
    best_score = marker_scores.max(axis=1)
    return best.where(best_score > 0, "unassigned")


def assign_refined_state(cell_type: str, marker_row: pd.Series) -> str:
    if cell_type not in COARSE_ALLOWED:
        return f"{cell_type}_unresolved"
    allowed = [state for state in marker_row.index if state in COARSE_ALLOWED[cell_type]]
    if not allowed:
        return f"{cell_type}_unresolved"
    ranked = marker_row.loc[allowed].dropna().sort_values(ascending=False)
    if ranked.empty or ranked.iloc[0] <= 0:
        return f"{cell_type}_unresolved"
    return str(ranked.index[0])


def process_sample(sample: pd.Series, programs: dict[str, dict[str, set[str]]], gene_map: dict[str, str]) -> pd.DataFrame:
    raw = pd.read_csv(sample["file"], index_col=0)
    raw.index = raw.index.astype(str).str.replace(r"\.\d+$", "", regex=True).map(lambda x: gene_map.get(x, x)).str.upper()
    raw = raw.groupby(raw.index).sum()
    lib = raw.sum(axis=0)
    detected = (raw > 0).sum(axis=0)
    mito_genes = [gene for gene in raw.index if gene.startswith("MT-")]
    pct_mito = raw.loc[mito_genes].sum(axis=0).div(lib.replace(0, np.nan)).fillna(0) * 100 if mito_genes else pd.Series(0, index=raw.columns)
    keep = (lib >= 500) & (detected >= 200) & (pct_mito <= 25)
    raw = raw.loc[:, keep]
    lib = lib.loc[keep]
    detected = detected.loc[keep]
    pct_mito = pct_mito.loc[keep]

    score_data = {}
    for axis, axis_programs in programs.items():
        for program_type, genes in axis_programs.items():
            score_data[f"{axis}_{program_type}"] = mean_log_cpm(raw, genes, lib)
    coarse_scores = pd.DataFrame({label: mean_log_cpm(raw, {g.upper() for g in genes}, lib) for label, genes in COARSE_MARKERS.items()}, index=raw.columns)
    refined_scores = pd.DataFrame({label: mean_log_cpm(raw, {g.upper() for g in genes}, lib) for label, genes in REFINED_MARKERS.items()}, index=raw.columns)
    cell_type = assign_cell_type(coarse_scores)
    refined_state = pd.Series(
        [assign_refined_state(ct, refined_scores.loc[cell]) for cell, ct in cell_type.items()],
        index=raw.columns,
    )

    out = pd.DataFrame(score_data, index=raw.columns)
    out["cell_barcode"] = raw.columns
    out["cell_id"] = sample["sample_accession"] + ":" + out["cell_barcode"].astype(str)
    out["sample_accession"] = sample["sample_accession"]
    out["donor_id"] = sample["derived_donor_id"]
    out["disease_group"] = sample["derived_disease_group"]
    out["tissue_state"] = sample["derived_tissue_state"]
    out["cell_type"] = cell_type.to_numpy()
    out["refined_state"] = refined_state.to_numpy()
    out["n_counts"] = lib.to_numpy()
    out["n_genes"] = detected.to_numpy()
    out["pct_mito"] = pct_mito.to_numpy()
    return out.reset_index(drop=True)


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


def summarize(cells: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    score_cols = [f"{axis}_{program_type}" for axis in AXES for program_type in PROGRAM_TYPES]
    donor_state = (
        cells.groupby(["donor_id", "sample_accession", "disease_group", "tissue_state", "cell_type", "refined_state"])[score_cols]
        .agg(["mean", "count"])
        .reset_index()
    )
    donor_state.columns = [f"{a}_{b}" if b else a for a, b in donor_state.columns]

    rows = []
    paired = donor_state[donor_state["disease_group"].eq("PsO")]
    for axis in AXES:
        for program_type in PROGRAM_TYPES:
            col = f"{axis}_{program_type}_mean"
            for refined_state, sub in paired.groupby("refined_state"):
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
                            "n_paired_donors": len(diffs),
                            "mean_LS_minus_NL": float(np.mean(diffs)) if len(diffs) else np.nan,
                            "bootstrap_ci_low": ci_low,
                            "bootstrap_ci_high": ci_high,
                            "signflip_p": paired_signflip_p(diffs),
                        }
                    )
    paired_stats = pd.DataFrame(rows)
    paired_stats["fdr_by_program_type"] = paired_stats.groupby("program_type")["signflip_p"].transform(bh_fdr)

    hv_rows = []
    for axis in AXES:
        for program_type in PROGRAM_TYPES:
            col = f"{axis}_{program_type}_mean"
            for refined_state, sub in donor_state.groupby("refined_state"):
                ps = sub[sub["tissue_state"].eq("lesional")].groupby("donor_id")[col].mean()
                hv = sub[sub["tissue_state"].eq("healthy")].groupby("donor_id")[col].mean()
                if len(ps) >= 3 and len(hv) >= 3:
                    u = mannwhitneyu(ps, hv, alternative="two-sided")
                    hv_rows.append(
                        {
                            "axis": axis,
                            "program_type": program_type,
                            "refined_state": refined_state,
                            "parent_cell_type": sub["cell_type"].mode().iloc[0],
                            "n_lesional_donors": len(ps),
                            "n_healthy_donors": len(hv),
                            "mean_lesional_minus_healthy": float(ps.mean() - hv.mean()),
                            "mannwhitney_p": float(u.pvalue),
                        }
                    )
    healthy_stats = pd.DataFrame(hv_rows)
    if not healthy_stats.empty:
        healthy_stats["fdr_by_program_type"] = healthy_stats.groupby("program_type")["mannwhitney_p"].transform(bh_fdr)

    loc_rows = []
    for axis in AXES:
        for program_type in PROGRAM_TYPES:
            col = f"{axis}_{program_type}"
            means = cells.groupby(["donor_id", "refined_state", "cell_type"])[col].mean().reset_index()
            summary = (
                means.groupby(["refined_state", "cell_type"])[col]
                .agg(["mean", "count"])
                .reset_index()
                .sort_values("mean", ascending=False)
            )
            top = summary.iloc[0]
            loc_rows.append(
                {
                    "axis": axis,
                    "program_type": program_type,
                    "dominant_refined_state": top["refined_state"],
                    "dominant_parent_cell_type": top["cell_type"],
                    "dominant_mean_score": top["mean"],
                    "n_refined_states_observed": len(summary),
                }
            )
    localization = pd.DataFrame(loc_rows)
    return donor_state, paired_stats, healthy_stats, localization


def final_table(cells: pd.DataFrame, paired_stats: pd.DataFrame, healthy_stats: pd.DataFrame, localization: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for axis in AXES:
        core_stats = paired_stats[
            paired_stats["axis"].eq(axis) & paired_stats["program_type"].eq("CORE") & paired_stats["n_paired_donors"].ge(5)
        ].copy()
        if axis == "F7":
            immune = core_stats["parent_cell_type"].isin(["T_cell", "NK_cell", "B_cell", "myeloid_monocyte", "dendritic"])
            if immune.any():
                core_stats = core_stats.loc[immune]
        core_stats = core_stats.sort_values(["mean_LS_minus_NL"], ascending=False)
        best = core_stats.iloc[0] if not core_stats.empty else pd.Series(dtype=object)
        loc = localization[localization["axis"].eq(axis) & localization["program_type"].eq("CORE")].iloc[0]
        core = cells.groupby(["donor_id", "tissue_state", "refined_state"])[f"{axis}_CORE"].mean()
        ext = cells.groupby(["donor_id", "tissue_state", "refined_state"])[f"{axis}_EXTENDED"].mean()
        common = core.dropna().index.intersection(ext.dropna().index)
        rho = spearmanr(core.loc[common], ext.loc[common]).correlation if len(common) >= 5 else np.nan
        confidence = "LOW"
        if pd.notna(best.get("fdr_by_program_type", np.nan)) and best["fdr_by_program_type"] <= 0.20 and best["bootstrap_ci_low"] > 0 and rho >= 0.5:
            confidence = "MODERATE"
        if pd.notna(best.get("fdr_by_program_type", np.nan)) and best["fdr_by_program_type"] <= 0.10 and best["bootstrap_ci_low"] > 0 and rho >= 0.7:
            confidence = "HIGH"
        h = healthy_stats[(healthy_stats["axis"].eq(axis)) & (healthy_stats["program_type"].eq("CORE"))]
        h_best = h.sort_values("mean_lesional_minus_healthy", ascending=False).head(1)
        rows.append(
            {
                "axis": axis,
                "dominant_refined_state_paired": best.get("refined_state", "not_available"),
                "parent_cell_type": best.get("parent_cell_type", loc["dominant_parent_cell_type"]),
                "score_localization": loc["dominant_refined_state"],
                "n_paired_donors": best.get("n_paired_donors", np.nan),
                "paired_LS_minus_NL": best.get("mean_LS_minus_NL", np.nan),
                "paired_ci_low": best.get("bootstrap_ci_low", np.nan),
                "paired_ci_high": best.get("bootstrap_ci_high", np.nan),
                "paired_fdr": best.get("fdr_by_program_type", np.nan),
                "lesional_vs_healthy_top_state": h_best["refined_state"].iloc[0] if not h_best.empty else "not_available",
                "lesional_vs_healthy_effect": h_best["mean_lesional_minus_healthy"].iloc[0] if not h_best.empty else np.nan,
                "core_extended_spearman": rho,
                "independent_scrna_confidence": confidence,
            }
        )
    return pd.DataFrame(rows)


def write_report(cells: pd.DataFrame, paired_stats: pd.DataFrame, healthy_stats: pd.DataFrame, localization: pd.DataFrame, final: pd.DataFrame) -> None:
    go = "NO-GO / SHRINK"
    n_mod = final["independent_scrna_confidence"].isin(["MODERATE", "HIGH"]).sum()
    if n_mod >= 3:
        go = "STRONG GO TO GENETICS"
    elif n_mod >= 2:
        go = "CONDITIONAL GO"
    lines = [
        "# PHASE 2C GSE173706 Independent scRNA Validation",
        "",
        "## 结论",
        "",
        f"{go}. GSE173706 作为独立 scRNA 验证集完成 donor-level marker/reference 定位。分析未使用作者整合注释，采用透明 marker mapping；cell 只作为打分单位，统计解释基于 donor summary。",
        "",
        "## 数据概况",
        "",
        f"- QC-passing cells scored: {cells.shape[0]}",
        f"- Donors with recoverable IDs: {cells['donor_id'].nunique()}",
        f"- Tissue states: {cells['tissue_state'].value_counts().to_dict()}",
        "",
        "## Final independent scRNA localization",
        "",
        final.to_markdown(index=False),
        "",
        "## Paired PsO LS-vs-NL donor statistics",
        "",
        paired_stats.sort_values(["axis", "program_type", "fdr_by_program_type", "mean_LS_minus_NL"]).head(120).to_markdown(index=False),
        "",
        "## Lesional-vs-healthy donor support",
        "",
        healthy_stats.sort_values(["axis", "program_type", "fdr_by_program_type", "mean_lesional_minus_healthy"]).head(120).to_markdown(index=False) if not healthy_stats.empty else "No eligible lesional-vs-healthy rows.",
        "",
        "## Score localization",
        "",
        localization.to_markdown(index=False),
        "",
        "## Interpretation boundary",
        "",
        "This is independent single-cell support, but marker-derived annotations are still less strong than curated author cell-state labels. A mechanism name should be upgraded only if GSE173706 converges with Phase 2B-R and later spatial evidence.",
    ]
    REPORT.write_text("\n".join(lines) + "\n")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = download_inputs()
    programs = load_programs()
    gene_map = load_gene_map()
    frames = []
    for _, sample in meta.iterrows():
        print(f"Processing {sample['sample_accession']} {sample['derived_tissue_state']}", flush=True)
        frames.append(process_sample(sample, programs, gene_map))
    cells = pd.concat(frames, ignore_index=True)
    cells.to_csv(OUT / "GSE173706_cell_axis_scores.tsv.gz", sep="\t", index=False, compression="gzip")
    donor_state, paired_stats, healthy_stats, localization = summarize(cells)
    donor_state.to_csv(OUT / "GSE173706_donor_cellstate_axis_scores.tsv", sep="\t", index=False)
    paired_stats.to_csv(OUT / "GSE173706_LS_vs_NL_donor_statistics.tsv", sep="\t", index=False)
    healthy_stats.to_csv(OUT / "GSE173706_lesional_vs_healthy_statistics.tsv", sep="\t", index=False)
    localization.to_csv(OUT / "GSE173706_score_localization.tsv", sep="\t", index=False)
    final = final_table(cells, paired_stats, healthy_stats, localization)
    final.to_csv(OUT / "GSE173706_independent_scRNA_localization.tsv", sep="\t", index=False)
    write_report(cells, paired_stats, healthy_stats, localization, final)
    print(final.to_string(index=False))


if __name__ == "__main__":
    main()
