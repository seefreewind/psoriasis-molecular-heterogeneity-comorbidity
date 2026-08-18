#!/usr/bin/env python3
"""Phase 2B donor-level single-cell localization for frozen Phase 2A axis programs."""

from __future__ import annotations

import gzip
import hashlib
import itertools
import math
import re
import shutil
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.io import mmread
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parents[2]
GEO = ROOT / "data" / "external" / "geo"
RAW = GEO / "GSE228421_10x"
P2A = ROOT / "results" / "phase2a"
OUT = ROOT / "results" / "phase2b"
FIG = ROOT / "results" / "figures" / "phase2b"
REPORT = ROOT / "reports" / "PHASE2B_GSE228421_SINGLE_CELL_LOCALIZATION.md"

AXES = ["F1", "F2", "F6", "F7"]
PROGRAM_TYPES = ["CORE", "EXTENDED"]

MARKERS = {
    "keratinocyte": ["KRT14", "KRT5", "KRT1", "KRT10", "KRT16", "KRT17", "DSG1", "DSG3", "S100A7", "S100A8", "S100A9"],
    "fibroblast": ["COL1A1", "COL1A2", "COL3A1", "DCN", "LUM", "COL6A1", "PDGFRA"],
    "endothelial": ["PECAM1", "VWF", "KDR", "CLDN5", "RAMP2", "ENG"],
    "pericyte_smooth_muscle": ["ACTA2", "MYH11", "TAGLN", "RGS5", "MCAM", "PDGFRB"],
    "T_cell": ["CD3D", "CD3E", "TRAC", "TRBC1", "IL7R", "CD8A", "CD4"],
    "myeloid_monocyte": ["LYZ", "LST1", "CTSS", "CD14", "FCGR3A", "S100A8", "S100A9", "TYROBP"],
    "dendritic": ["FCER1A", "CLEC10A", "CD1C", "LAMP3", "CCR7"],
    "B_cell": ["MS4A1", "CD79A", "CD79B", "BANK1", "CD74"],
    "NK_cell": ["NKG7", "GNLY", "KLRD1", "PRF1", "GZMB"],
    "mast_cell": ["TPSAB1", "TPSB2", "CPA3", "KIT"],
    "melanocyte": ["PMEL", "MLANA", "TYR", "DCT"],
}


def mkdirs() -> None:
    for path in [RAW, OUT, FIG]:
        path.mkdir(parents=True, exist_ok=True)


def parse_series_matrix(path: Path) -> tuple[pd.DataFrame, list[str]]:
    rows = {}
    series_lines = []
    with gzip.open(path, "rt", errors="replace") as fh:
        for line in fh:
            if line.startswith("!Series_"):
                series_lines.append(line.rstrip("\n"))
            if line.startswith("!series_matrix_table_begin"):
                break
            if not line.startswith("!Sample_"):
                continue
            parts = [p.strip().strip('"') for p in line.rstrip("\n").split("\t")]
            key = parts[0].replace("!Sample_", "")
            if key in rows:
                key = f"{key}_{sum(k.startswith(key) for k in rows) + 1}"
            rows[key] = parts[1:]
    meta = pd.DataFrame(rows).rename(columns={"geo_accession": "gsm"})
    meta["donor_id"] = meta["title"].str.extract(r"^(P\d+)-", expand=False)
    meta["visit"] = meta["title"].str.extract(r"-(V\d+)", expand=False)
    meta["timepoint"] = meta["visit"].map({"V1": "baseline", "V2": "day3", "V3": "day14"}).fillna("unknown")
    meta["tissue_state"] = np.where(meta["title"].str.contains("Non Lesional", case=False, na=False), "nonlesional", "lesional")
    meta["baseline_primary"] = meta["timepoint"].eq("baseline")
    return meta, series_lines


def url_to_https(url: str) -> str:
    return url.replace("ftp://ftp.ncbi.nlm.nih.gov", "https://ftp.ncbi.nlm.nih.gov")


def download_file(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        return
    tmp = dest.with_suffix(dest.suffix + ".partial")
    https_url = url_to_https(url)
    print(f"Downloading {dest.name}", flush=True)
    if shutil.which("curl"):
        last_error = None
        for attempt in range(1, 21):
            try:
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
                        "--retry-delay",
                        "5",
                        "--connect-timeout",
                        "60",
                        "--continue-at",
                        "-",
                        "-o",
                        str(tmp),
                        https_url,
                    ],
                    check=True,
                )
                last_error = None
                break
            except subprocess.CalledProcessError as exc:
                last_error = exc
                size = tmp.stat().st_size if tmp.exists() else 0
                print(
                    f"Retrying {dest.name} after curl exit {exc.returncode}; partial={size} bytes; attempt={attempt}/20",
                    flush=True,
                )
        if last_error is not None:
            raise last_error
    else:
        with urllib.request.urlopen(https_url, timeout=240) as r, tmp.open("ab") as f:
            while True:
                block = r.read(1024 * 1024)
                if not block:
                    break
                f.write(block)
    tmp.rename(dest)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def download_10x(meta: pd.DataFrame) -> pd.DataFrame:
    tasks = []
    supp_cols = [c for c in meta.columns if c.startswith("supplementary_file")]
    for _, sample in meta.iterrows():
        sample_dir = RAW / sample["gsm"]
        sample_dir.mkdir(parents=True, exist_ok=True)
        for col in supp_cols:
            url = sample[col]
            if not isinstance(url, str) or not url:
                continue
            dest = sample_dir / url.rsplit("/", 1)[-1]
            tasks.append(
                (
                    url,
                    dest,
                    {
                        "gsm": sample["gsm"],
                        "donor_id": sample["donor_id"],
                        "timepoint": sample["timepoint"],
                        "tissue_state": sample["tissue_state"],
                    },
                )
            )

    def fetch(task: tuple[str, Path, dict[str, str]]) -> dict[str, str | int]:
        url, dest, base = task
        download_file(url, dest)
        return {
            **base,
            "file": str(dest),
            "bytes": dest.stat().st_size,
            "sha256": sha256(dest),
        }

    rows = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        future_map = {pool.submit(fetch, task): task for task in tasks}
        for future in as_completed(future_map):
            rows.append(future.result())
            if len(rows) % 10 == 0 or len(rows) == len(tasks):
                print(f"Downloaded {len(rows)}/{len(tasks)} supplementary files", flush=True)
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "GSE228421_download_manifest.tsv", sep="\t", index=False)
    return out


def load_programs() -> dict[str, dict[str, set[str]]]:
    programs = {}
    for axis in AXES:
        df = pd.read_csv(P2A / "axis_gene_programs" / f"{axis}_gene_program.tsv", sep="\t")
        axis_programs = {}
        for status in PROGRAM_TYPES:
            if status == "CORE":
                genes = set(df.loc[df["leading_edge_status"].eq("CORE"), "gene_symbol"].astype(str).str.upper())
            else:
                genes = set(df["gene_symbol"].astype(str).str.upper())
            axis_programs[status] = genes
        programs[axis] = axis_programs
    return programs


def read_tsv_gz(path: Path) -> list[list[str]]:
    with gzip.open(path, "rt", errors="replace") as fh:
        return [line.rstrip("\n").split("\t") for line in fh]


def sample_paths(gsm: str) -> tuple[Path, Path, Path]:
    d = RAW / gsm
    barcodes = next(d.glob("*.barcodes.tsv.gz"))
    features = next(d.glob("*.features.tsv.gz"))
    matrix = next(d.glob("*.matrix.mtx.gz"))
    return barcodes, features, matrix


def mean_log_cpm_scores(x: sparse.csr_matrix, gene_symbols: list[str], gene_set: set[str], lib: np.ndarray) -> np.ndarray:
    idx = [i for i, g in enumerate(gene_symbols) if g in gene_set]
    if len(idx) < 3:
        return np.full(x.shape[1], np.nan)
    sub = x[idx, :].tocsc(copy=True)
    scale = np.divide(10000.0, lib, out=np.zeros_like(lib, dtype=float), where=lib > 0)
    sub = sub @ sparse.diags(scale)
    sub.data = np.log1p(sub.data)
    return np.asarray(sub.sum(axis=0)).ravel() / len(idx)


def process_sample(sample: pd.Series, programs: dict[str, dict[str, set[str]]]) -> tuple[pd.DataFrame, pd.DataFrame]:
    barcodes_path, features_path, matrix_path = sample_paths(sample["gsm"])
    barcodes = [x[0] for x in read_tsv_gz(barcodes_path)]
    features = read_tsv_gz(features_path)
    gene_symbols = [(row[1] if len(row) > 1 else row[0]).upper() for row in features]
    gene_symbols = [g if g else f"GENE_{i}" for i, g in enumerate(gene_symbols)]
    x = mmread(matrix_path).tocsr().astype(float)
    lib = np.asarray(x.sum(axis=0)).ravel()
    detected = np.asarray((x > 0).sum(axis=0)).ravel()
    mito_idx = [i for i, g in enumerate(gene_symbols) if g.startswith("MT-")]
    mito = np.asarray(x[mito_idx, :].sum(axis=0)).ravel() if mito_idx else np.zeros(x.shape[1])
    pct_mito = np.divide(mito, lib, out=np.zeros_like(lib), where=lib > 0) * 100
    keep = (lib >= 500) & (detected >= 200) & (pct_mito <= 25)
    x = x[:, keep]
    kept_barcodes = [barcodes[i] for i, k in enumerate(keep) if k]
    lib = lib[keep]
    qc = pd.DataFrame(
        {
            "cell_id": [f"{sample['gsm']}:{b}" for b in kept_barcodes],
            "n_counts": lib,
            "n_genes": detected[keep],
            "pct_mito": pct_mito[keep],
            "pass_qc": True,
            "raw_barcode_count": len(barcodes),
        }
    )

    marker_scores = {}
    for label, genes in MARKERS.items():
        marker_scores[label] = mean_log_cpm_scores(x, gene_symbols, {g.upper() for g in genes}, lib)
    marker_df = pd.DataFrame(marker_scores)
    cell_type = marker_df.idxmax(axis=1)
    cell_type = cell_type.where(marker_df.max(axis=1) > 0, "unassigned")

    rows = []
    for axis, axis_programs in programs.items():
        for program_type, genes in axis_programs.items():
            vals = mean_log_cpm_scores(x, gene_symbols, genes, lib)
            rows.append(pd.Series(vals, name=f"{axis}_{program_type}"))
    score_df = pd.concat(rows, axis=1)
    score_df["cell_barcode"] = kept_barcodes
    score_df["cell_id"] = [f"{sample['gsm']}:{b}" for b in kept_barcodes]
    score_df["gsm"] = sample["gsm"]
    score_df["donor_id"] = sample["donor_id"]
    score_df["timepoint"] = sample["timepoint"]
    score_df["tissue_state"] = sample["tissue_state"]
    score_df["baseline_primary"] = sample["baseline_primary"]
    score_df["cell_type"] = cell_type.values
    score_df["marker_score_max"] = marker_df.max(axis=1).values
    score_df["n_counts"] = lib
    score_df["n_genes"] = detected[keep]
    score_df["pct_mito"] = pct_mito[keep]
    return qc, score_df


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
    n = len(diffs)
    if n == 0:
        return np.nan
    obs = abs(diffs.mean())
    vals = []
    for signs in itertools.product([-1, 1], repeat=n):
        vals.append(abs((diffs * np.array(signs)).mean()))
    return float((np.sum(np.array(vals) >= obs) + 1) / (len(vals) + 1))


def bootstrap_ci(diffs: np.ndarray, n_iter: int = 2000, seed: int = 20260811) -> tuple[float, float]:
    diffs = diffs[np.isfinite(diffs)]
    if len(diffs) == 0:
        return np.nan, np.nan
    rng = np.random.default_rng(seed)
    vals = [rng.choice(diffs, size=len(diffs), replace=True).mean() for _ in range(n_iter)]
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def summarize_scores(cells: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    score_cols = [c for c in cells.columns if re.match(r"F[1267]_(CORE|EXTENDED)$", c)]
    group_cols = ["donor_id", "gsm", "timepoint", "tissue_state", "baseline_primary", "cell_type"]
    donor_celltype = cells.groupby(group_cols)[score_cols].agg(["mean", "count"])
    donor_celltype.columns = [f"{a}_{b}" for a, b in donor_celltype.columns]
    donor_celltype = donor_celltype.reset_index()
    donor_celltype.to_csv(OUT / "GSE228421_donor_celltype_axis_scores.tsv", sep="\t", index=False)

    baseline = donor_celltype[donor_celltype["baseline_primary"].eq(True)]
    rows = []
    for axis in AXES:
        for program_type in PROGRAM_TYPES:
            col = f"{axis}_{program_type}_mean"
            for cell_type, sub in baseline.groupby("cell_type"):
                wide = sub.pivot_table(index="donor_id", columns="tissue_state", values=col, aggfunc="mean")
                if {"lesional", "nonlesional"} <= set(wide.columns):
                    diffs = (wide["lesional"] - wide["nonlesional"]).dropna().to_numpy()
                    ci_low, ci_high = bootstrap_ci(diffs)
                    rows.append(
                        {
                            "axis": axis,
                            "program_type": program_type,
                            "cell_type": cell_type,
                            "n_donors": len(diffs),
                            "mean_LS_minus_NL": float(np.mean(diffs)) if len(diffs) else np.nan,
                            "bootstrap_ci_low": ci_low,
                            "bootstrap_ci_high": ci_high,
                            "signflip_p": paired_signflip_p(diffs),
                        }
                    )
    paired = pd.DataFrame(rows)
    paired["fdr_by_program_type"] = paired.groupby("program_type")["signflip_p"].transform(bh_fdr)
    paired.to_csv(OUT / "GSE228421_baseline_LS_vs_NL_donor_statistics.tsv", sep="\t", index=False)

    loc_rows = []
    base_cells = cells[cells["baseline_primary"].eq(True)]
    for axis in AXES:
        for program_type in PROGRAM_TYPES:
            col = f"{axis}_{program_type}"
            means = base_cells.groupby(["donor_id", "cell_type"])[col].mean().reset_index()
            ct = means.groupby("cell_type")[col].agg(["mean", "std", "count"]).reset_index().sort_values("mean", ascending=False)
            if not ct.empty:
                top = ct.iloc[0]
                second = ct.iloc[1] if len(ct) > 1 else top
                loc_rows.append(
                    {
                        "axis": axis,
                        "program_type": program_type,
                        "dominant_cell_type": top["cell_type"],
                        "dominant_mean_score": top["mean"],
                        "secondary_cell_type": second["cell_type"],
                        "secondary_mean_score": second["mean"],
                        "specificity_delta_vs_second": top["mean"] - second["mean"],
                        "n_cell_types_observed": len(ct),
                    }
                )
    localization = pd.DataFrame(loc_rows)
    localization.to_csv(OUT / "GSE228421_cell_type_localization.tsv", sep="\t", index=False)

    treat_rows = []
    lesional = donor_celltype[donor_celltype["tissue_state"].eq("lesional")]
    for axis in AXES:
        for program_type in PROGRAM_TYPES:
            col = f"{axis}_{program_type}_mean"
            for cell_type, sub in lesional.groupby("cell_type"):
                wide = sub.pivot_table(index="donor_id", columns="timepoint", values=col, aggfunc="mean")
                for tp in ["day3", "day14"]:
                    if {"baseline", tp} <= set(wide.columns):
                        diffs = (wide[tp] - wide["baseline"]).dropna().to_numpy()
                        ci_low, ci_high = bootstrap_ci(diffs)
                        treat_rows.append(
                            {
                                "axis": axis,
                                "program_type": program_type,
                                "cell_type": cell_type,
                                "contrast": f"{tp}_minus_baseline_lesional",
                                "n_donors": len(diffs),
                                "mean_treatment_shift": float(np.mean(diffs)) if len(diffs) else np.nan,
                                "bootstrap_ci_low": ci_low,
                                "bootstrap_ci_high": ci_high,
                                "signflip_p": paired_signflip_p(diffs),
                            }
                        )
    treatment = pd.DataFrame(treat_rows)
    if not treatment.empty:
        treatment["fdr_by_program_type"] = treatment.groupby("program_type")["signflip_p"].transform(bh_fdr)
    treatment.to_csv(OUT / "GSE228421_treatment_timepoint_sensitivity.tsv", sep="\t", index=False)
    return donor_celltype, paired, localization, treatment


def dropout_robustness(cells: pd.DataFrame) -> pd.DataFrame:
    # This is a score-level robustness proxy: CORE and EXTENDED donor-celltype means should agree.
    rows = []
    for axis in AXES:
        core = cells.groupby(["donor_id", "timepoint", "tissue_state", "cell_type"])[f"{axis}_CORE"].mean()
        ext = cells.groupby(["donor_id", "timepoint", "tissue_state", "cell_type"])[f"{axis}_EXTENDED"].mean()
        common = core.dropna().index.intersection(ext.dropna().index)
        r = spearmanr(core.loc[common], ext.loc[common]).correlation if len(common) >= 5 else np.nan
        rows.append({"axis": axis, "core_extended_pseudobulk_spearman": r, "n_donor_celltype_units": len(common)})
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "GSE228421_program_dropout_robustness.tsv", sep="\t", index=False)
    return out


def final_axis_table(paired: pd.DataFrame, localization: pd.DataFrame, robustness: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for axis in AXES:
        loc_core = localization[(localization["axis"].eq(axis)) & (localization["program_type"].eq("CORE"))].iloc[0]
        stats = paired[(paired["axis"].eq(axis)) & (paired["program_type"].eq("CORE")) & (paired["n_donors"].ge(4))]
        if axis == "F7":
            immune = {"T_cell", "NK_cell", "B_cell", "myeloid_monocyte", "dendritic"}
            immune_stats = stats[stats["cell_type"].isin(immune)]
            if not immune_stats.empty:
                stats = immune_stats
        stats = stats.sort_values("mean_LS_minus_NL", ascending=False).head(2)
        s = stats.iloc[0] if not stats.empty else pd.Series(dtype=object)
        secondary = stats.iloc[1]["cell_type"] if stats.shape[0] > 1 else loc_core["secondary_cell_type"]
        robust = robustness.set_index("axis").loc[axis]
        confidence = "MODERATE" if pd.notna(s.get("fdr_by_program_type", np.nan)) and s.get("fdr_by_program_type", 1) <= 0.20 and robust["core_extended_pseudobulk_spearman"] >= 0.5 else "LOW"
        status = "localized_candidate" if confidence in ["MODERATE", "HIGH"] else "directional_not_fdr_significant"
        rows.append(
            {
                "axis": axis,
                "dominant_cell": s.get("cell_type", loc_core["dominant_cell_type"]),
                "secondary_cell": secondary,
                "LS_NL_context": "skin baseline paired LS-vs-NL" if axis != "F7" else "skin immune localization; systemic support remains from bulk blood",
                "donor_effect": s.get("mean_LS_minus_NL", np.nan),
                "bootstrap_ci_low": s.get("bootstrap_ci_low", np.nan),
                "bootstrap_ci_high": s.get("bootstrap_ci_high", np.nan),
                "fdr": s.get("fdr_by_program_type", np.nan),
                "core_extended_spearman": robust["core_extended_pseudobulk_spearman"],
                "replication": "yes" if axis in ["F1", "F2", "F6"] else "support",
                "final_name": axis,
                "confidence": confidence,
                "phase2b_status": status,
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "Table_phase2b_axis_cell_localization.tsv", sep="\t", index=False)
    return out


def plot_outputs(paired: pd.DataFrame, localization: pd.DataFrame, final: pd.DataFrame) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    core_loc = localization[localization["program_type"].eq("CORE")]
    pivot = core_loc.pivot_table(index="axis", columns="dominant_cell_type", values="dominant_mean_score", aggfunc="mean").fillna(0)
    plt.figure(figsize=(8, 3.8))
    plt.imshow(pivot.to_numpy(), aspect="auto", cmap="mako" if False else "viridis")
    plt.yticks(range(len(pivot.index)), pivot.index)
    plt.xticks(range(len(pivot.columns)), pivot.columns, rotation=45, ha="right")
    plt.colorbar(label="Mean CORE score")
    plt.title("Phase 2B cell-type localization")
    plt.tight_layout()
    plt.savefig(FIG / "Figure3A_GSE228421_axis_celltype_localization.png", dpi=300)
    plt.savefig(FIG / "Figure3A_GSE228421_axis_celltype_localization.svg")
    plt.close()

    core = paired[paired["program_type"].eq("CORE")].copy()
    top_cells = final.set_index("axis")["dominant_cell"].to_dict()
    core = core[core.apply(lambda r: r["cell_type"] == top_cells.get(r["axis"]), axis=1)]
    plt.figure(figsize=(6.5, 3.8))
    x = np.arange(len(core))
    plt.bar(x, core["mean_LS_minus_NL"], color="#4C78A8")
    plt.errorbar(x, core["mean_LS_minus_NL"], yerr=[core["mean_LS_minus_NL"] - core["bootstrap_ci_low"], core["bootstrap_ci_high"] - core["mean_LS_minus_NL"]], fmt="none", color="black", capsize=3)
    plt.xticks(x, core["axis"] + "\n" + core["cell_type"], rotation=0)
    plt.axhline(0, color="black", linewidth=0.8)
    plt.ylabel("Donor mean LS-NL")
    plt.title("Phase 2B dominant-cell paired effects")
    plt.tight_layout()
    plt.savefig(FIG / "Figure3B_GSE228421_donor_paired_effects.png", dpi=300)
    plt.savefig(FIG / "Figure3B_GSE228421_donor_paired_effects.svg")
    plt.close()


def write_report(meta: pd.DataFrame, qc: pd.DataFrame, paired: pd.DataFrame, localization: pd.DataFrame, treatment: pd.DataFrame, robustness: pd.DataFrame, final: pd.DataFrame) -> None:
    if "raw_barcode_count" in qc.columns and {"gsm", "raw_barcode_count"} <= set(qc.columns):
        n_cells_raw = int(qc.groupby("gsm")["raw_barcode_count"].first().sum())
    else:
        n_cells_raw = qc.shape[0]
    n_cells_kept = int(qc["pass_qc"].sum()) if "pass_qc" in qc.columns else qc.shape[0]
    go = "STRONG GO TO GENETICS" if (final["confidence"].isin(["MODERATE", "HIGH"]).sum() >= 3) else ("CONDITIONAL GO" if final["confidence"].isin(["MODERATE", "HIGH"]).sum() >= 2 else "NO-GO / SHRINK")
    lines = [
        "# PHASE 2B GSE228421 Single-Cell Localization",
        "",
        "## Executive conclusion",
        "",
        f"{go}. Frozen F1/F2/F6/F7 programs were scored in GSE228421 single-cell skin data using donor-level summaries. CORE programs are primary; EXTENDED programs are sensitivity.",
        "",
        "## Dataset and lock",
        "",
        f"- GSE228421 samples parsed: {meta.shape[0]}.",
        f"- Donors detected: {meta['donor_id'].nunique()}.",
        f"- Raw cells/barcodes: {n_cells_raw}; QC-passing cells: {n_cells_kept}.",
        "- Primary analysis: baseline lesional versus baseline nonlesional, paired by donor.",
        "- Treatment day 3/day 14 lesional samples are sensitivity only.",
        "- Inference unit: donor/patient, not cell.",
        "",
        "## Final localization table",
        "",
        final.to_markdown(index=False),
        "",
        "## Cell-type localization",
        "",
        localization.to_markdown(index=False),
        "",
        "## Baseline paired donor statistics",
        "",
        paired.sort_values(["axis", "program_type", "fdr_by_program_type"]).head(80).to_markdown(index=False),
        "",
        "## CORE versus EXTENDED robustness",
        "",
        robustness.to_markdown(index=False),
        "",
        "## Treatment sensitivity",
        "",
        treatment.sort_values(["axis", "program_type", "fdr_by_program_type"]).head(80).to_markdown(index=False) if not treatment.empty else "No treatment sensitivity rows generated.",
        "",
        "## Reviewer attack points",
        "",
        "- Donor count is 5, so p values are low-power and confidence intervals should drive interpretation.",
        "- Cell-type annotation is marker-based and coarse; Phase 2B conclusions should be treated as localization candidates until refined annotation or reference mapping.",
        "- F7 is a systemic/supportive axis; skin single-cell localization can identify immune-state plausibility but cannot replace blood/PBMC validation.",
        "- CORE programs are primary. EXTENDED concordance supports robustness but cannot rescue failed CORE localization.",
        "",
        "## GO / CONDITIONAL GO / NO-GO",
        "",
        go,
        "",
        "## Next recommendation",
        "",
        "If at least two axes show MODERATE/HIGH localization confidence, proceed to refined annotation and then spatial validation. Do not start GWAS/MR until Phase 2B localization and Phase 2C spatial/perturbation boundaries are accepted.",
    ]
    REPORT.write_text("\n".join(lines) + "\n")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    meta, series_lines = parse_series_matrix(GEO / "GSE228421_series_matrix.txt.gz")
    meta.to_csv(OUT / "GSE228421_sample_metadata.tsv", sep="\t", index=False)
    (OUT / "GSE228421_series_provenance.txt").write_text("\n".join(series_lines) + "\n")
    download_10x(meta)
    programs = load_programs()
    qc_frames = []
    score_frames = []
    for _, sample in meta.iterrows():
        qc, scores = process_sample(sample, programs)
        qc_frames.append(qc.assign(gsm=sample["gsm"], donor_id=sample["donor_id"], timepoint=sample["timepoint"], tissue_state=sample["tissue_state"]))
        score_frames.append(scores)
    qc_all = pd.concat(qc_frames, ignore_index=True)
    cells = pd.concat(score_frames, ignore_index=True)
    qc_all.to_csv(OUT / "GSE228421_cell_qc.tsv.gz", sep="\t", index=False, compression="gzip")
    cells.to_csv(OUT / "GSE228421_cell_axis_scores.tsv.gz", sep="\t", index=False, compression="gzip")
    donor_celltype, paired, localization, treatment = summarize_scores(cells)
    robustness = dropout_robustness(cells)
    final = final_axis_table(paired, localization, robustness)
    plot_outputs(paired, localization, final)
    write_report(meta, qc_all, paired, localization, treatment, robustness, final)


if __name__ == "__main__":
    main()
