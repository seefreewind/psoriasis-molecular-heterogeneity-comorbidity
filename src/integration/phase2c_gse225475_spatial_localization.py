#!/usr/bin/env python3
"""Phase 2C primary spatial localization with GSE225475."""

from __future__ import annotations

import subprocess
import tarfile
from pathlib import Path

import h5py
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.stats import mannwhitneyu, spearmanr


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "external" / "geo" / "GSE225475_visium"
OUT = ROOT / "results" / "phase2c"
REPORT = ROOT / "reports" / "PHASE2C_GSE225475_PRIMARY_SPATIAL_LOCALIZATION.md"
META_PATH = OUT / "GSE225475_sample_metadata_audit.tsv"
SUPP_PATH = OUT / "dataset_supplementary_files.tsv"
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


def download_and_extract() -> pd.DataFrame:
    RAW.mkdir(parents=True, exist_ok=True)
    meta = pd.read_csv(META_PATH, sep="\t")
    urls = pd.read_csv(SUPP_PATH, sep="\t")
    urls = urls[(urls["accession"].eq("GSE225475")) & (urls["level"].eq("sample"))][["sample_accession", "url"]]
    meta = meta.merge(urls, on="sample_accession", how="left")
    rows = []
    for _, row in meta.iterrows():
        url = row["url"].replace("ftp://ftp.ncbi.nlm.nih.gov", "https://ftp.ncbi.nlm.nih.gov")
        tar_path = RAW / url.rsplit("/", 1)[-1]
        sample_dir = RAW / str(row["description"])
        if not tar_path.exists() or tar_path.stat().st_size == 0:
            tmp = tar_path.with_suffix(tar_path.suffix + ".partial")
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
                    "900",
                    "--continue-at",
                    "-",
                    "-o",
                    str(tmp),
                    url,
                ],
                check=True,
            )
            tmp.rename(tar_path)
        if not (sample_dir / "filtered_feature_bc_matrix.h5").exists():
            with tarfile.open(tar_path, "r:gz") as tar:
                tar.extractall(RAW)
        rows.append({"sample_accession": row["sample_accession"], "file": str(tar_path), "bytes": tar_path.stat().st_size})
        print(f"Ready {row['sample_accession']} {row['description']}", flush=True)
    manifest = pd.DataFrame(rows)
    manifest.to_csv(OUT / "GSE225475_download_manifest.tsv", sep="\t", index=False)
    return meta


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
        data = group["data"][:]
        indices = group["indices"][:]
        indptr = group["indptr"][:]
        shape = tuple(group["shape"][:])
        x = sparse.csc_matrix((data, indices, indptr), shape=shape).astype(float)
        barcodes = [b.decode() if isinstance(b, bytes) else str(b) for b in group["barcodes"][:]]
        features = group["features"]
        names = [b.decode() if isinstance(b, bytes) else str(b) for b in features["name"][:]]
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
    sample_name = str(sample["description"])
    h5_path = RAW / sample_name / "filtered_feature_bc_matrix.h5"
    x, genes, barcodes = read_10x_h5(h5_path)
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
    out["sample_name"] = sample_name
    out["disease_group"] = sample["derived_disease_group"]
    out["tissue_state"] = sample["derived_tissue_state"]
    out["n_counts"] = lib
    return out


def summarize(spots: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    score_cols = [f"{axis}_{program_type}" for axis in AXES for program_type in PROGRAM_TYPES]
    sample_scores = spots.groupby(["sample_accession", "sample_name", "disease_group", "tissue_state"])[score_cols].mean().reset_index()
    disease_rows = []
    for axis in AXES:
        for program_type in PROGRAM_TYPES:
            col = f"{axis}_{program_type}"
            ps = sample_scores[sample_scores["disease_group"].eq("PsO")][col]
            hv = sample_scores[sample_scores["disease_group"].eq("Healthy")][col]
            p = mannwhitneyu(ps, hv, alternative="two-sided").pvalue if len(ps) >= 2 and len(hv) >= 2 else np.nan
            disease_rows.append(
                {
                    "axis": axis,
                    "program_type": program_type,
                    "n_psoriasis_sections": len(ps),
                    "n_healthy_sections": len(hv),
                    "mean_psoriasis_minus_healthy": float(ps.mean() - hv.mean()) if len(ps) and len(hv) else np.nan,
                    "mannwhitney_p": p,
                }
            )
    disease = pd.DataFrame(disease_rows)

    marker_cols = [c for c in spots.columns if c.startswith("marker_")]
    corr_rows = []
    for sample_name, sub in spots.groupby("sample_name"):
        for axis in AXES:
            for program_type in PROGRAM_TYPES:
                axis_col = f"{axis}_{program_type}"
                for marker_col in marker_cols:
                    valid = sub[[axis_col, marker_col]].dropna()
                    rho = spearmanr(valid[axis_col], valid[marker_col]).correlation if valid.shape[0] >= 10 else np.nan
                    corr_rows.append(
                        {
                            "sample_name": sample_name,
                            "axis": axis,
                            "program_type": program_type,
                            "spatial_program": marker_col.replace("marker_", ""),
                            "spot_spearman": rho,
                            "n_spots": valid.shape[0],
                        }
                    )
    corr = pd.DataFrame(corr_rows)
    loc = (
        corr[corr["program_type"].eq("CORE")]
        .groupby(["axis", "spatial_program"])["spot_spearman"]
        .agg(["median", "mean", "count"])
        .reset_index()
        .sort_values(["axis", "median"], ascending=[True, False])
    )
    top = loc.groupby("axis").head(1).rename(
        columns={"spatial_program": "dominant_spatial_program", "median": "median_spot_spearman"}
    )
    return sample_scores, disease, corr, top


def write_report(spots: pd.DataFrame, sample_scores: pd.DataFrame, disease: pd.DataFrame, corr: pd.DataFrame, top: pd.DataFrame) -> None:
    lines = [
        "# PHASE 2C GSE225475 Primary Spatial Localization",
        "",
        "## 结论",
        "",
        "GSE225475 primary spatial localization completed as supportive spatial co-localization. The dataset has 2 healthy and 4 psoriasis sections without LS/NL pairing, so it cannot provide donor-level paired inference. It is used to test whether frozen axis scores co-vary across Visium spots with predefined spatial marker programs.",
        "",
        "## 数据概况",
        "",
        f"- Sections: {sample_scores.shape[0]}",
        f"- Spots scored: {spots.shape[0]}",
        f"- Groups: {sample_scores['disease_group'].value_counts().to_dict()}",
        "",
        "## Dominant Spatial Programs",
        "",
        top.to_markdown(index=False),
        "",
        "## Section-Level Psoriasis-vs-Healthy Axis Scores",
        "",
        disease.to_markdown(index=False),
        "",
        "## Sample Scores",
        "",
        sample_scores.to_markdown(index=False),
        "",
        "## Boundary",
        "",
        "This dataset supports spatial localization only. Because donor IDs and LS/NL labels are not recoverable from GEO sample metadata, no patient-level paired spatial claim is made.",
    ]
    REPORT.write_text("\n".join(lines) + "\n")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = download_and_extract()
    programs = load_programs()
    frames = [process_sample(sample, programs) for _, sample in meta.iterrows()]
    spots = pd.concat(frames, ignore_index=True)
    spots.to_csv(OUT / "GSE225475_spot_axis_scores.tsv.gz", sep="\t", index=False, compression="gzip")
    sample_scores, disease, corr, top = summarize(spots)
    sample_scores.to_csv(OUT / "GSE225475_sample_axis_scores.tsv", sep="\t", index=False)
    disease.to_csv(OUT / "GSE225475_psoriasis_vs_healthy_axis_scores.tsv", sep="\t", index=False)
    corr.to_csv(OUT / "GSE225475_spot_axis_marker_correlations.tsv", sep="\t", index=False)
    top.to_csv(OUT / "GSE225475_spatial_axis_localization.tsv", sep="\t", index=False)
    write_report(spots, sample_scores, disease, corr, top)
    print(top.to_string(index=False))


if __name__ == "__main__":
    main()
