#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data/raw"
META = ROOT / "data/metadata/EMTAB14509_sample_metadata.tsv"
GTF = ROOT / "data/metadata/Homo_sapiens.GRCh38.113.gtf.gz"
HALLMARK = ROOT / "data/metadata/h.all.v2025.1.Hs.symbols.gmt"
CURATED = ROOT / "src/features/curated_gene_sets.tsv"
OUT = ROOT / "results/phase1"
TABLES = ROOT / "results/tables"


def parse_gtf_symbols() -> pd.DataFrame:
    import gzip

    rows = []
    gene_id_re = re.compile(r'gene_id "([^"]+)"')
    gene_name_re = re.compile(r'gene_name "([^"]+)"')
    biotype_re = re.compile(r'gene_biotype "([^"]+)"')
    with gzip.open(GTF, "rt") as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 9 or parts[2] != "gene":
                continue
            attr = parts[8]
            gid = gene_id_re.search(attr)
            gname = gene_name_re.search(attr)
            biotype = biotype_re.search(attr)
            if gid and gname:
                rows.append(
                    {
                        "ensembl_gene": gid.group(1).split(".")[0],
                        "gene_symbol": gname.group(1),
                        "gene_biotype": biotype.group(1) if biotype else "",
                    }
                )
    return pd.DataFrame(rows).drop_duplicates("ensembl_gene")


def read_matrix(name: str) -> pd.DataFrame:
    return pd.read_csv(RAW / name, sep="\t", index_col=0)


def baseline_patient_matrix(mat: pd.DataFrame, meta: pd.DataFrame, cohort: str, tissue: str) -> pd.DataFrame:
    rows = meta[(meta["cohort"].eq(cohort)) & (meta["timepoint"].eq(0)) & (meta["tissue"].eq(tissue))]
    samples = [s for s in rows["sample_id"] if s in mat.columns]
    if not samples:
        return pd.DataFrame()
    patient = rows.set_index("sample_id").loc[samples, "patient_id"].astype(str)
    x = mat[samples].T
    x.index = patient.values
    return x.groupby(level=0).mean()


def read_gmt(path: Path) -> dict[str, set[str]]:
    gene_sets = {}
    with path.open() as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 3:
                gene_sets[f"Hallmark::{parts[0]}"] = set(parts[2:])
    return gene_sets


def read_curated(path: Path) -> dict[str, set[str]]:
    df = pd.read_csv(path, sep="\t")
    gene_sets = defaultdict(set)
    for row in df.itertuples(index=False):
        gene_sets[f"{row.feature_family}::{row.feature_name}"].add(row.gene_symbol)
    return dict(gene_sets)


def symbol_matrix(x: pd.DataFrame, mapping: pd.DataFrame) -> pd.DataFrame:
    map_series = mapping.set_index("ensembl_gene")["gene_symbol"]
    y = x.copy()
    y.columns = [str(c).split(".")[0] for c in y.columns]
    common = [c for c in y.columns if c in map_series.index]
    y = y[common]
    y.columns = map_series.loc[common].values
    y = y.T.groupby(level=0).mean().T
    return y


def zscore_rows(x: pd.DataFrame) -> pd.DataFrame:
    sd = x.std(axis=0).replace(0, np.nan)
    return ((x - x.mean(axis=0)) / sd).fillna(0)


def score_sets(x_symbol: pd.DataFrame, gene_sets: dict[str, set[str]]) -> tuple[pd.DataFrame, pd.DataFrame]:
    z = zscore_rows(x_symbol)
    scores = {}
    defs = []
    available = set(z.columns)
    for name, genes in gene_sets.items():
        present = sorted(available & set(genes))
        if len(present) < 2:
            continue
        scores[name] = z[present].mean(axis=1)
        family, feature = name.split("::", 1)
        defs.append(
            {
                "feature_id": name,
                "feature_family": family,
                "feature_name": feature,
                "n_genes_defined": len(genes),
                "n_genes_present": len(present),
                "genes_present": ";".join(present),
            }
        )
    return pd.DataFrame(scores, index=z.index), pd.DataFrame(defs)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    meta = pd.read_csv(META, sep="\t")
    meta["patient_id"] = meta["patient_id"].astype(str)
    mapping = parse_gtf_symbols()
    mapping.to_csv(OUT / "ensembl_gene_symbol_map.tsv", sep="\t", index=False)

    gene_sets = {}
    gene_sets.update(read_gmt(HALLMARK))
    gene_sets.update(read_curated(CURATED))

    specs = [
        ("discovery", "Lesional Skin", "Skin_norm_counts_d.txt", "LS"),
        ("discovery", "Nonlesional Skin", "Skin_norm_counts_d.txt", "NL"),
        ("discovery", "Whole Blood", "Blood_norm_counts_d.txt", "BLD"),
        ("replication", "Lesional Skin", "Skin_norm_counts_r.txt", "LS"),
        ("replication", "Nonlesional Skin", "Skin_norm_counts_r.txt", "NL"),
    ]
    all_defs = []
    matrices = []
    for cohort, tissue, file_name, tissue_code in specs:
        mat = read_matrix(file_name)
        x = baseline_patient_matrix(mat, meta, cohort, tissue)
        if x.empty:
            continue
        xs = symbol_matrix(x, mapping)
        scores, defs = score_sets(xs, gene_sets)
        scores.columns = [f"{tissue_code}__{c}" for c in scores.columns]
        scores.insert(0, "patient_id", scores.index)
        scores.insert(1, "cohort", cohort)
        scores.insert(2, "tissue", tissue)
        scores.to_csv(OUT / f"feature_scores_{cohort}_{tissue_code}.tsv", sep="\t", index=False)
        defs["tissue_code"] = tissue_code
        defs["cohort"] = cohort
        all_defs.append(defs)
        wide = scores.drop(columns=["cohort", "tissue"]).set_index("patient_id")
        matrices.append((cohort, tissue_code, wide))

    pd.concat(all_defs, ignore_index=True).drop_duplicates(
        ["feature_id", "tissue_code"]
    ).to_csv(TABLES / "Table_S3_feature_definitions.tsv", sep="\t", index=False)

    for cohort in ["discovery", "replication"]:
        parts = [wide for c, _, wide in matrices if c == cohort]
        if not parts:
            continue
        joined = pd.concat(parts, axis=1, join="outer")
        joined.insert(0, "patient_id", joined.index)
        joined.insert(1, "cohort", cohort)
        joined.to_csv(OUT / f"baseline_biological_feature_matrix_{cohort}.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()

