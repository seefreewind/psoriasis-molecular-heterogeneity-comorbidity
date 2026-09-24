#!/usr/bin/env python3
"""External skin replication and blood support for Phase 1B axes."""

from __future__ import annotations

import gzip
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parents[2]
PHASE1B = ROOT / "results" / "phase1b"
EXT = ROOT / "data" / "external" / "geo"
GSE244679_DIR = EXT / "GSE244679_RAW"


def parse_series_matrix_metadata(path: Path) -> pd.DataFrame:
    rows = {}
    with gzip.open(path, "rt", errors="replace") as fh:
        for line in fh:
            if line.startswith("!series_matrix_table_begin"):
                break
            if not line.startswith("!Sample_"):
                continue
            parts = [p.strip().strip('"') for p in line.rstrip("\n").split("\t")]
            key = parts[0].replace("!Sample_", "")
            vals = parts[1:]
            if key in rows:
                key = f"{key}_{sum(k.startswith(key) for k in rows) + 1}"
            rows[key] = vals
    if "geo_accession" not in rows:
        return pd.DataFrame()
    meta = pd.DataFrame(rows)
    return meta.rename(columns={"geo_accession": "gsm"})


def read_series_matrix_expression(path: Path) -> pd.DataFrame:
    lines = []
    in_table = False
    with gzip.open(path, "rt", errors="replace") as fh:
        for line in fh:
            if line.startswith("!series_matrix_table_begin"):
                in_table = True
                continue
            if line.startswith("!series_matrix_table_end"):
                break
            if in_table:
                lines.append(line)
    if not lines:
        return pd.DataFrame()
    from io import StringIO

    mat = pd.read_csv(StringIO("".join(lines)), sep="\t", index_col=0)
    mat.index = mat.index.astype(str).str.strip('"')
    mat.columns = [c.strip('"') for c in mat.columns]
    return mat.apply(pd.to_numeric, errors="coerce")


def read_geo_platform_table(path: Path) -> pd.DataFrame:
    lines = []
    in_table = False
    with gzip.open(path, "rt", errors="replace") as fh:
        for line in fh:
            if line.startswith("!platform_table_begin"):
                in_table = True
                continue
            if line.startswith("!platform_table_end"):
                break
            if in_table:
                lines.append(line)
    if not lines:
        return pd.DataFrame()
    from io import StringIO

    return pd.read_csv(StringIO("".join(lines)), sep="\t", dtype=str)


def score_gene_sets(x: pd.DataFrame, gene_sets: dict[str, list[str]]) -> pd.DataFrame:
    x = x.T.groupby(level=0).mean().T
    ranks = x.rank(axis=1, method="average", pct=True)
    available = set(ranks.columns)
    scores = {}
    for name, genes in gene_sets.items():
        present = sorted(available & set(genes))
        if len(present) < 2:
            continue
        vals = ranks[present].mean(axis=1)
        sd = vals.std(ddof=0)
        scores[name] = (vals - vals.mean()) / (sd if sd else 1)
    return pd.DataFrame(scores, index=x.index)


def safe_spearman(a: pd.Series, b: pd.Series) -> float:
    common = a.dropna().index.intersection(b.dropna().index)
    if len(common) < 10:
        return np.nan
    if a.loc[common].std(ddof=0) == 0 or b.loc[common].std(ddof=0) == 0:
        return np.nan
    return float(spearmanr(a.loc[common], b.loc[common]).correlation)


def load_gene_sets() -> dict[str, list[str]]:
    return json.loads((ROOT / "data" / "metadata" / "phase1b" / "phase1b_gene_sets.json").read_text())


def load_loadings() -> pd.DataFrame:
    return pd.read_csv(PHASE1B / "factor_loadings.tsv", sep="\t")


def build_gse244679_matrix() -> tuple[pd.DataFrame, pd.DataFrame]:
    meta = parse_series_matrix_metadata(EXT / "GSE244679_series_matrix.txt.gz")
    if meta.empty:
        raise RuntimeError("Could not parse GSE244679 sample metadata.")
    meta["condition"] = np.where(
        meta["title"].str.contains("Psoriatic", case=False, na=False),
        "lesional_psoriatic",
        "adjacent_normal",
    )
    meta["pair_id"] = meta["title"].str.extract(r"Rep(\d+)", expand=False)
    files = sorted(GSE244679_DIR.glob("GSM*_raw_read_counts_genes.txt.gz"))
    columns = []
    matrices = []
    for path in files:
        gsm = path.name.split("_", 1)[0]
        if gsm not in set(meta["gsm"]):
            continue
        with gzip.open(path, "rt", errors="replace") as fh:
            df = pd.read_csv(fh, sep=r"\s+", engine="python")
        count_col = [c for c in df.columns if c not in {"gene_id", "gene_name", "gene_type"}][-1]
        s = pd.to_numeric(df[count_col], errors="coerce")
        tmp = pd.DataFrame({"gene": df["gene_name"].astype(str), gsm: s})
        tmp = tmp.groupby("gene")[gsm].sum()
        matrices.append(tmp)
        columns.append(gsm)
    counts = pd.concat(matrices, axis=1).fillna(0)
    lib = counts.sum(axis=0)
    logcpm = np.log2((counts / lib) * 1_000_000 + 1).T
    logcpm.index.name = "sample"
    logcpm.to_csv(PHASE1B / "external_GSE244679_logCPM.tsv", sep="\t")
    meta.to_csv(PHASE1B / "external_GSE244679_sample_metadata.tsv", sep="\t", index=False)
    return logcpm, meta


def gse244679_skin_replication(loadings: pd.DataFrame, gene_sets: dict[str, list[str]]) -> pd.DataFrame:
    expr, meta = build_gse244679_matrix()
    scores = score_gene_sets(expr, gene_sets)
    meta = meta.set_index("gsm").loc[scores.index]
    lesional = scores.loc[meta["condition"].eq("lesional_psoriatic")]
    adjacent = scores.loc[meta["condition"].eq("adjacent_normal")]
    # Pair-aware mean difference by Rep number.
    paired_diffs = []
    for pair_id in sorted(set(meta["pair_id"].dropna())):
        sample_ids = meta.index[meta["pair_id"].eq(pair_id)]
        ls = sample_ids[meta.loc[sample_ids, "condition"].eq("lesional_psoriatic")]
        nl = sample_ids[meta.loc[sample_ids, "condition"].eq("adjacent_normal")]
        if len(ls) == 1 and len(nl) == 1:
            paired_diffs.append(scores.loc[ls[0]] - scores.loc[nl[0]])
    delta = pd.concat(paired_diffs, axis=1).mean(axis=1)
    rows = []
    for factor in sorted(loadings["factor"].unique(), key=lambda x: int(x[1:])):
        for view in ["LS", "NL"]:
            w = loadings[(loadings["factor"] == factor) & (loadings["view"] == view)].set_index("feature")["loading"]
            common = w.index.intersection(delta.index)
            rows.append(
                {
                    "dataset": "GSE244679",
                    "axis": factor,
                    "view": view,
                    "n_pairs": len(paired_diffs),
                    "n_common_axis_features": len(common),
                    "loading_vs_paired_lesional_minus_adjacent_spearman": safe_spearman(w.loc[common], delta.loc[common]),
                    "external_effect_definition": "mean paired score difference: lesional psoriatic skin minus adjacent normal skin",
                }
            )
    out = pd.DataFrame(rows)
    out.to_csv(PHASE1B / "external_GSE244679_skin_axis_replication.tsv", sep="\t", index=False)
    return out


def gse147339_blood_support(loadings: pd.DataFrame, gene_sets: dict[str, list[str]]) -> pd.DataFrame:
    meta = parse_series_matrix_metadata(EXT / "GSE147339_series_matrix.txt.gz")
    expr = pd.read_csv(EXT / "GSE147339_counts.fpkm.csv.gz", index_col=0)
    expr.index = expr.index.astype(str).str.replace("\ufeff", "", regex=False)
    expr = np.log2(expr.T + 1)
    meta["sample_label"] = meta["title"].str.extract(r"^([^:]+):", expand=False)
    meta["condition"] = np.where(meta["title"].str.contains("Psoriasis", case=False, na=False), "psoriasis", "control")
    label_to_gsm = dict(zip(meta["sample_label"], meta["gsm"]))
    def normalize_label(label: str) -> str:
        m = re.search(r"Tube_(\d+)-1", str(label))
        return m.group(1) if m else str(label)

    expr.index = [label_to_gsm.get(normalize_label(i), str(i)) for i in expr.index]
    meta = meta.set_index("gsm").loc[expr.index]
    scores = score_gene_sets(expr, gene_sets)
    delta = scores.loc[meta["condition"].eq("psoriasis")].mean(axis=0) - scores.loc[meta["condition"].eq("control")].mean(axis=0)
    rows = []
    for factor in sorted(loadings["factor"].unique(), key=lambda x: int(x[1:])):
        w = loadings[(loadings["factor"] == factor) & (loadings["view"] == "BLD")].set_index("feature")["loading"]
        common = w.index.intersection(delta.index)
        rows.append(
            {
                "dataset": "GSE147339",
                "axis": factor,
                "view": "BLD",
                "n_psoriasis": int(meta["condition"].eq("psoriasis").sum()),
                "n_control": int(meta["condition"].eq("control").sum()),
                "n_common_axis_features": len(common),
                "loading_vs_psoriasis_minus_control_spearman": safe_spearman(w.loc[common], delta.loc[common]),
                "external_effect_definition": "mean score difference: psoriasis whole blood minus control whole blood",
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(PHASE1B / "external_GSE147339_blood_axis_support.tsv", sep="\t", index=False)
    return out


def parse_gse61281_conditions(meta: pd.DataFrame) -> pd.DataFrame:
    meta = meta.copy()
    title = meta["title"].fillna("")
    meta["condition"] = np.select(
        [
            title.str.contains("Cutaneous psoriasis without arthritis|PsC", case=False, regex=True),
            title.str.contains("Psoriatic arthritis|PsA", case=False, regex=True),
            title.str.contains("Control", case=False, regex=False),
        ],
        ["cutaneous_psoriasis_without_arthritis", "psoriatic_arthritis", "control"],
        default="unknown",
    )
    return meta


def build_gse61281_gene_matrix() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    path = EXT / "GSE61281_series_matrix.txt.gz"
    annot_path = EXT / "GPL6480.annot.gz"
    if not path.exists() or not annot_path.exists():
        missing = [str(p) for p in [path, annot_path] if not p.exists()]
        raise RuntimeError(f"GSE61281 requires local series matrix and GPL6480 annotation; missing: {missing}")
    meta = parse_series_matrix_metadata(path)
    meta = parse_gse61281_conditions(meta)
    mat = read_series_matrix_expression(path)
    platform = read_geo_platform_table(annot_path)
    if meta.empty or mat.empty or platform.empty:
        raise RuntimeError("GSE61281 metadata, expression matrix, or GPL6480 platform annotation is empty.")
    probe_to_symbol = platform[["ID", "Gene symbol"]].copy()
    probe_to_symbol["gene"] = (
        probe_to_symbol["Gene symbol"]
        .fillna("")
        .astype(str)
        .str.split(r"\s*///\s*", regex=True)
        .str[0]
        .str.strip()
    )
    probe_to_symbol = probe_to_symbol[probe_to_symbol["gene"].ne("")]
    probe_to_symbol = probe_to_symbol.drop_duplicates("ID").set_index("ID")["gene"]
    common = mat.index.intersection(probe_to_symbol.index)
    mapped = mat.loc[common].copy()
    mapped["gene"] = probe_to_symbol.loc[common].values
    gene_expr = mapped.groupby("gene").mean(numeric_only=True).T
    gene_expr.index.name = "sample"
    meta = meta.set_index("gsm").loc[gene_expr.index].rename_axis("gsm").reset_index()
    gene_expr.to_csv(PHASE1B / "external_GSE61281_gene_expression.tsv", sep="\t")
    meta.to_csv(PHASE1B / "external_GSE61281_sample_metadata.tsv", sep="\t", index=False)
    row = {
        "dataset": "GSE61281",
        "status": "platform_mapped_gene_matrix_ready",
        "platform": "GPL6480",
        "n_samples_metadata": len(meta),
        "n_expression_rows": mat.shape[0],
        "n_expression_columns": mat.shape[1],
        "n_probe_ids_with_gene_symbol": int(len(probe_to_symbol)),
        "n_mapped_expression_probes": int(len(common)),
        "n_gene_symbols_after_probe_aggregation": int(gene_expr.shape[1]),
        "n_psc": int(meta["condition"].eq("cutaneous_psoriasis_without_arthritis").sum()),
        "n_psa": int(meta["condition"].eq("psoriatic_arthritis").sum()),
        "n_control": int(meta["condition"].eq("control").sum()),
        "expression_handling": "GEO series-matrix values used as normalized microarray expression; probes averaged by GPL6480 Gene symbol",
    }
    out = pd.DataFrame([row])
    out.to_csv(PHASE1B / "external_GSE61281_matrix_audit.tsv", sep="\t", index=False)
    return gene_expr, meta, out


def gse61281_blood_support(loadings: pd.DataFrame, gene_sets: dict[str, list[str]]) -> pd.DataFrame:
    expr, meta, _ = build_gse61281_gene_matrix()
    meta = meta.set_index("gsm").loc[expr.index]
    scores = score_gene_sets(expr, gene_sets)
    contrasts = [
        (
            "cutaneous_psoriasis_without_arthritis_minus_control",
            meta["condition"].eq("cutaneous_psoriasis_without_arthritis"),
            meta["condition"].eq("control"),
        ),
        (
            "psoriatic_arthritis_minus_control",
            meta["condition"].eq("psoriatic_arthritis"),
            meta["condition"].eq("control"),
        ),
        (
            "psoriasis_spectrum_minus_control",
            meta["condition"].isin(["cutaneous_psoriasis_without_arthritis", "psoriatic_arthritis"]),
            meta["condition"].eq("control"),
        ),
    ]
    rows = []
    for contrast, case_mask, control_mask in contrasts:
        delta = scores.loc[case_mask].mean(axis=0) - scores.loc[control_mask].mean(axis=0)
        for factor in sorted(loadings["factor"].unique(), key=lambda x: int(x[1:])):
            w = loadings[(loadings["factor"] == factor) & (loadings["view"] == "BLD")].set_index("feature")["loading"]
            common = w.index.intersection(delta.index)
            rows.append(
                {
                    "dataset": "GSE61281",
                    "axis": factor,
                    "view": "BLD",
                    "contrast": contrast,
                    "n_case": int(case_mask.sum()),
                    "n_control": int(control_mask.sum()),
                    "n_common_axis_features": len(common),
                    "loading_vs_case_minus_control_spearman": safe_spearman(w.loc[common], delta.loc[common]),
                    "external_effect_definition": f"mean score difference: {contrast.replace('_', ' ')} in whole blood",
                }
            )
    out = pd.DataFrame(rows)
    out.to_csv(PHASE1B / "external_GSE61281_blood_axis_support.tsv", sep="\t", index=False)
    return out


def main() -> None:
    gene_sets = load_gene_sets()
    loadings = load_loadings()
    skin = gse244679_skin_replication(loadings, gene_sets)
    blood147339 = gse147339_blood_support(loadings, gene_sets)
    blood61281 = gse61281_blood_support(loadings, gene_sets)
    pd.concat(
        [
            skin.assign(result_type="skin_replication"),
            blood147339.assign(result_type="blood_support"),
            blood61281.assign(result_type="blood_support"),
        ],
        ignore_index=True,
        sort=False,
    ).to_csv(PHASE1B / "external_axis_replication_and_blood_support.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()
