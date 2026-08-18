#!/usr/bin/env python3
"""Phase 2C external spatial robustness with GSE202011 sample H5 files."""

from __future__ import annotations

import subprocess
from pathlib import Path

import h5py
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.stats import mannwhitneyu, spearmanr


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "external" / "geo" / "GSE202011_h5"
OUT = ROOT / "results" / "phase2c"
REPORT = ROOT / "reports" / "PHASE2C_GSE202011_EXTERNAL_SPATIAL_ROBUSTNESS.md"
META_PATH = OUT / "GSE202011_sample_metadata_audit.tsv"
P2A = ROOT / "results" / "phase2a" / "axis_gene_programs"

AXES = ["F1", "F2", "F6", "F7"]
PROGRAM_TYPES = ["CORE", "EXTENDED"]
SPATIAL_MARKERS = {
    "keratinocyte_basal": ["KRT5", "KRT14", "KRT15", "TP63", "ITGA6"],
    "keratinocyte_spinous_suprabasal": ["KRT1", "KRT10", "DSG1", "DSC1", "FLG", "LOR"],
    "keratinocyte_inflammatory_T17": ["KRT16", "KRT17", "S100A7", "S100A8", "S100A9", "DEFB4A", "IL36G", "CXCL8"],
    "keratinocyte_stress_hypoxia": ["HIF1A", "VEGFA", "DDIT4", "NDRG1", "SLC2A1", "ADM", "BNIP3"],
    "fibroblast_matrix": ["COL1A1", "COL1A2", "COL3A1", "DCN", "LUM", "PDGFRA"],
    "fibroblast_inflammatory": ["CCL19", "CCL13", "CXCL12", "CXCL14", "IL6", "PDPN", "FAP"],
    "endothelial_vascular": ["PECAM1", "VWF", "KDR", "RAMP2", "CLDN5", "ENG"],
    "myeloid_dendritic": ["LYZ", "LST1", "CTSS", "CD14", "LAMP3", "CCR7", "FCER1A"],
    "T_NK_cytotoxic": ["CD3D", "CD3E", "TRAC", "NKG7", "GNLY", "PRF1", "GZMB"],
    "B_plasma": ["MS4A1", "CD79A", "CD79B", "MZB1", "JCHAIN"],
}


def download_inputs() -> pd.DataFrame:
    RAW.mkdir(parents=True, exist_ok=True)
    meta = pd.read_csv(META_PATH, sep="\t")
    rows = []
    for _, row in meta.iterrows():
        url = row["supplementary_file_1"].replace("ftp://ftp.ncbi.nlm.nih.gov", "https://ftp.ncbi.nlm.nih.gov")
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
                    "--connect-timeout",
                    "60",
                    "--max-time",
                    "600",
                    "--continue-at",
                    "-",
                    "-o",
                    str(tmp),
                    url,
                ],
                check=True,
            )
            tmp.rename(dest)
        rows.append({"sample_accession": row["sample_accession"], "file": str(dest), "bytes": dest.stat().st_size})
        print(f"Ready {row['sample_accession']} {row['derived_disease_group']} {row['derived_tissue_state']}", flush=True)
    manifest = pd.DataFrame(rows)
    manifest.to_csv(OUT / "GSE202011_download_manifest.tsv", sep="\t", index=False)
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


def read_10x_h5(path: Path) -> tuple[sparse.csc_matrix, list[str], list[str]]:
    with h5py.File(path, "r") as h5:
        group = h5["matrix"]
        x = sparse.csc_matrix((group["data"][:], group["indices"][:], group["indptr"][:]), shape=tuple(group["shape"][:])).astype(float)
        barcodes = [b.decode() if isinstance(b, bytes) else str(b) for b in group["barcodes"][:]]
        names = [b.decode() if isinstance(b, bytes) else str(b) for b in group["features"]["name"][:]]
    return x, [n.upper() for n in names], barcodes


def mean_log_cpm(x: sparse.csc_matrix, genes: list[str], gene_set: set[str], lib: np.ndarray) -> np.ndarray:
    idx = [i for i, gene in enumerate(genes) if gene in gene_set]
    if len(idx) < 2:
        return np.full(x.shape[1], np.nan)
    sub = x[idx, :].tocsc(copy=True)
    scale = np.divide(10000.0, lib, out=np.zeros_like(lib, dtype=float), where=lib > 0)
    sub = sub @ sparse.diags(scale)
    sub.data = np.log1p(sub.data)
    return np.asarray(sub.sum(axis=0)).ravel() / len(idx)


def process_sample(sample: pd.Series, programs: dict[str, dict[str, set[str]]]) -> pd.DataFrame:
    x, genes, barcodes = read_10x_h5(Path(sample["file"]))
    lib = np.asarray(x.sum(axis=0)).ravel()
    keep = lib > 0
    x = x[:, keep]
    lib = lib[keep]
    barcodes = [barcodes[i] for i, ok in enumerate(keep) if ok]
    data = {}
    for axis, axis_programs in programs.items():
        for program_type, gene_set in axis_programs.items():
            data[f"{axis}_{program_type}"] = mean_log_cpm(x, genes, gene_set, lib)
    for state, marker_genes in SPATIAL_MARKERS.items():
        data[f"marker_{state}"] = mean_log_cpm(x, genes, {g.upper() for g in marker_genes}, lib)
    out = pd.DataFrame(data)
    out["spot_barcode"] = barcodes
    out["spot_id"] = sample["sample_accession"] + ":" + out["spot_barcode"].astype(str)
    out["sample_accession"] = sample["sample_accession"]
    out["donor_id"] = sample["derived_donor_id"]
    out["disease_group"] = sample["derived_disease_group"]
    out["tissue_state"] = sample["derived_tissue_state"]
    out["n_counts"] = lib
    return out


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


def summarize(spots: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    score_cols = [f"{axis}_{program_type}" for axis in AXES for program_type in PROGRAM_TYPES]
    sample_scores = spots.groupby(["sample_accession", "donor_id", "disease_group", "tissue_state"])[score_cols].mean().reset_index()
    rows = []
    for axis in AXES:
        for program_type in PROGRAM_TYPES:
            col = f"{axis}_{program_type}"
            for group in ["PsO", "PsA"]:
                les = sample_scores[(sample_scores["disease_group"].eq(group)) & (sample_scores["tissue_state"].eq("lesional"))][col]
                nl = sample_scores[(sample_scores["disease_group"].eq(group)) & (sample_scores["tissue_state"].eq("nonlesional"))][col]
                if len(les) >= 3 and len(nl) >= 3:
                    p = mannwhitneyu(les, nl, alternative="two-sided").pvalue
                else:
                    p = np.nan
                rows.append(
                    {
                        "axis": axis,
                        "program_type": program_type,
                        "disease_group": group,
                        "n_lesional_sections": len(les),
                        "n_nonlesional_sections": len(nl),
                        "mean_lesional_minus_nonlesional": float(les.mean() - nl.mean()) if len(les) and len(nl) else np.nan,
                        "mannwhitney_p": p,
                    }
                )
    disease = pd.DataFrame(rows)
    disease["fdr_by_program_type"] = disease.groupby("program_type")["mannwhitney_p"].transform(bh_fdr)

    marker_cols = [c for c in spots.columns if c.startswith("marker_")]
    corr_rows = []
    for sample, sub in spots.groupby("sample_accession"):
        for axis in AXES:
            for program_type in PROGRAM_TYPES:
                axis_col = f"{axis}_{program_type}"
                for marker_col in marker_cols:
                    valid = sub[[axis_col, marker_col]].dropna()
                    rho = spearmanr(valid[axis_col], valid[marker_col]).correlation if valid.shape[0] >= 10 else np.nan
                    corr_rows.append(
                        {
                            "sample_accession": sample,
                            "axis": axis,
                            "program_type": program_type,
                            "spatial_program": marker_col.replace("marker_", ""),
                            "spot_spearman": rho,
                            "n_spots": valid.shape[0],
                        }
                    )
    corr = pd.DataFrame(corr_rows)
    top = (
        corr[corr["program_type"].eq("CORE")]
        .groupby(["axis", "spatial_program"])["spot_spearman"]
        .agg(["median", "mean", "count"])
        .reset_index()
        .sort_values(["axis", "median"], ascending=[True, False])
        .groupby("axis")
        .head(1)
        .rename(columns={"spatial_program": "dominant_spatial_program", "median": "median_spot_spearman"})
    )
    return sample_scores, disease, corr, top


def write_report(spots: pd.DataFrame, sample_scores: pd.DataFrame, disease: pd.DataFrame, top: pd.DataFrame) -> None:
    lines = [
        "# PHASE 2C GSE202011 External Spatial Robustness",
        "",
        "## 结论",
        "",
        "GSE202011 was analyzed as an external spatial robustness dataset using sample-level H5 files. It is not used as a single-cell atlas. Section/spot analyses are interpreted as spatial support, not patient-level replication.",
        "",
        "## 数据概况",
        "",
        f"- Sections: {sample_scores.shape[0]}",
        f"- Spots scored: {spots.shape[0]}",
        f"- Disease groups: {sample_scores['disease_group'].value_counts().to_dict()}",
        f"- Tissue states: {sample_scores['tissue_state'].value_counts().to_dict()}",
        "",
        "## Dominant Spatial Programs",
        "",
        top.to_markdown(index=False),
        "",
        "## Lesional-vs-Nonlesional Section-Level Support",
        "",
        disease.to_markdown(index=False),
        "",
        "## Boundary",
        "",
        "The local `GSE202011_RAW.tar.incomplete` file was not used. All expression scoring used sample-level GEO H5 files audited in Phase 2C.",
    ]
    REPORT.write_text("\n".join(lines) + "\n")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = download_inputs()
    programs = load_programs()
    spots = pd.concat([process_sample(sample, programs) for _, sample in meta.iterrows()], ignore_index=True)
    spots.to_csv(OUT / "GSE202011_spot_axis_scores.tsv.gz", sep="\t", index=False, compression="gzip")
    sample_scores, disease, corr, top = summarize(spots)
    sample_scores.to_csv(OUT / "GSE202011_sample_axis_scores.tsv", sep="\t", index=False)
    disease.to_csv(OUT / "GSE202011_lesional_vs_nonlesional_axis_scores.tsv", sep="\t", index=False)
    corr.to_csv(OUT / "GSE202011_spot_axis_marker_correlations.tsv", sep="\t", index=False)
    top.to_csv(OUT / "GSE202011_spatial_axis_localization.tsv", sep="\t", index=False)
    write_report(spots, sample_scores, disease, top)
    print(top.to_string(index=False))


if __name__ == "__main__":
    main()
