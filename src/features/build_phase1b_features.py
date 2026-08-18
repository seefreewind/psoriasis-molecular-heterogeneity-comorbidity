#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import json

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data/raw"
META = ROOT / "data/metadata/EMTAB14509_sample_metadata.tsv"
MAP = ROOT / "results/phase1/ensembl_gene_symbol_map.tsv"
HALLMARK = ROOT / "data/metadata/h.all.v2025.1.Hs.symbols.gmt"
REACTOME = ROOT / "data/metadata/phase1b/reactome_gmt/ReactomePathways.gmt"
CURATED = ROOT / "src/features/curated_gene_sets.tsv"
OUT = ROOT / "results/phase1b"
PROV = ROOT / "data/metadata/phase1b"


def read_matrix(name: str) -> pd.DataFrame:
    return pd.read_csv(RAW / name, sep="\t", index_col=0)


def patient_matrix(mat: pd.DataFrame, meta: pd.DataFrame, cohort: str, tissue: str) -> pd.DataFrame:
    rows = meta[(meta["cohort"].eq(cohort)) & (meta["timepoint"].eq(0)) & (meta["tissue"].eq(tissue))]
    samples = [s for s in rows["sample_id"] if s in mat.columns]
    patient = rows.set_index("sample_id").loc[samples, "patient_id"].astype(str)
    x = mat[samples].T
    x.index = patient.values
    return x.groupby(level=0).mean()


def to_symbol(x: pd.DataFrame) -> pd.DataFrame:
    mapping = pd.read_csv(MAP, sep="\t").set_index("ensembl_gene")["gene_symbol"]
    y = x.copy()
    y.columns = [str(c).split(".")[0] for c in y.columns]
    common = [c for c in y.columns if c in mapping.index]
    y = y[common]
    y.columns = mapping.loc[common].values
    return y.T.groupby(level=0).mean().T


def read_gmt(path: Path, prefix: str, min_size=10, max_size=300) -> dict[str, list[str]]:
    sets = {}
    with path.open() as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            name = f"{prefix}::{parts[0]}"
            genes = sorted(set(parts[2:]))
            if min_size <= len(genes) <= max_size:
                sets[name] = genes
    return sets


def curated_sets() -> dict[str, list[str]]:
    df = pd.read_csv(CURATED, sep="\t")
    out = defaultdict(set)
    for row in df.itertuples(index=False):
        out[f"{row.feature_family}::{row.feature_name}"].add(row.gene_symbol)
    return {k: sorted(v) for k, v in out.items() if len(v) >= 2}


def cell_sets() -> dict[str, list[str]]:
    return {
        "cell_state::keratinocyte_proliferation": ["KRT6A", "KRT16", "KRT17", "MKI67", "TOP2A"],
        "cell_state::keratinocyte_differentiation": ["KRT1", "KRT10", "FLG", "LOR", "IVL"],
        "cell_state::T17_Th17": ["RORC", "IL23R", "CCR6", "IL17A", "IL17F", "KLRB1"],
        "cell_state::CD8_TRM": ["CD8A", "CD8B", "GZMB", "NKG7", "ITGAE", "CXCR6"],
        "cell_state::dendritic_cells": ["ITGAX", "CD1C", "CLEC10A", "FCER1A", "LILRA4"],
        "cell_state::monocyte_macrophage": ["CD14", "LYZ", "CSF1R", "FCGR3A", "C1QA", "C1QB"],
        "cell_state::neutrophil": ["S100A8", "S100A9", "FCGR3B", "CXCR2", "MPO"],
        "cell_state::fibroblast": ["COL1A1", "COL1A2", "DCN", "LUM", "COL3A1"],
        "cell_state::endothelial": ["PECAM1", "VWF", "KDR", "ENG", "CDH5"],
        "cell_state::B_cell": ["MS4A1", "CD79A", "CD79B", "BANK1", "CD19"],
        "cell_state::NK_cell": ["NKG7", "GNLY", "KLRD1", "PRF1", "KLRF1"],
    }


def zscore(x: pd.DataFrame) -> pd.DataFrame:
    y = x.apply(pd.to_numeric, errors="coerce")
    return ((y - y.mean(axis=0)) / y.std(axis=0).replace(0, np.nan)).fillna(0).astype(float)


def score_gene_sets(x: pd.DataFrame, gene_sets: dict[str, list[str]]) -> tuple[pd.DataFrame, pd.DataFrame]:
    # ssGSEA-like rank enrichment using mean normalized ranks for each frozen gene set.
    # gseapy is installed and version-locked for mature ssGSEA support; this vectorized
    # implementation keeps Phase 1B tractable for repeated tissue views.
    ranks = x.rank(axis=1, method="average", pct=True)
    scores = {}
    defs = []
    available = set(ranks.columns)
    for name, genes in gene_sets.items():
        present = sorted(available & set(genes))
        if len(present) < 2:
            continue
        vals = ranks[present].mean(axis=1)
        scores[name] = (vals - vals.mean()) / (vals.std() if vals.std() else 1)
        fam, feat = name.split("::", 1)
        defs.append({
            "feature_id": name,
            "feature_family": fam,
            "feature_name": feat,
            "n_genes_defined": len(genes),
            "n_genes_present": len(present),
            "genes_present": ";".join(present),
        })
    return pd.DataFrame(scores, index=x.index), pd.DataFrame(defs)


def decoupler_scores(x: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    import decoupler as dc
    scores = []
    defs = []
    z = zscore(x)
    try:
        progeny = dc.get_progeny(organism="human", top=100)
        progeny = progeny.assign(
            source=progeny["source"].astype(str),
            target=progeny["target"].astype(str),
            weight=progeny["weight"].astype(float),
        )
        _, acts, _, _ = dc.run_wmean(z, progeny, source="source", target="target", weight="weight", min_n=5, times=100)
        acts = acts.add_prefix("signaling_PROGENy::")
        scores.append(acts)
        for src, n in progeny.groupby("source")["target"].nunique().items():
            defs.append({"feature_id": f"signaling_PROGENy::{src}", "feature_family": "signaling_PROGENy", "feature_name": src, "n_genes_defined": int(n), "n_genes_present": int(n), "genes_present": ""})
    except Exception as e:
        (OUT / "decoupler_progeny_error.txt").write_text(repr(e))
    try:
        dorothea = dc.get_dorothea(organism="human", levels=["A", "B", "C"])
        keep = {"STAT1", "STAT3", "RELA", "NFKB1", "IRF1", "IRF3", "IRF7", "JUN", "FOS", "CEBPA", "CEBPB", "SMAD3", "HIF1A", "AHR"}
        dorothea = dorothea[dorothea["source"].isin(keep)]
        dorothea = dorothea.assign(
            source=dorothea["source"].astype(str),
            target=dorothea["target"].astype(str),
            weight=dorothea["weight"].astype(float),
        )
        acts, _ = dc.run_ulm(z, dorothea, source="source", target="target", weight="weight", min_n=5)
        acts = acts.add_prefix("regulon_DoRothEA::")
        scores.append(acts)
        for src, n in dorothea.groupby("source")["target"].nunique().items():
            defs.append({"feature_id": f"regulon_DoRothEA::{src}", "feature_family": "regulon_DoRothEA", "feature_name": src, "n_genes_defined": int(n), "n_genes_present": int(n), "genes_present": ""})
    except Exception as e:
        (OUT / "decoupler_dorothea_error.txt").write_text(repr(e))
    if scores:
        return pd.concat(scores, axis=1), pd.DataFrame(defs)
    return pd.DataFrame(index=x.index), pd.DataFrame(defs)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    PROV.mkdir(parents=True, exist_ok=True)
    meta = pd.read_csv(META, sep="\t")
    meta["patient_id"] = meta["patient_id"].astype(str)

    gene_sets = {}
    gene_sets.update(read_gmt(HALLMARK, "Hallmark"))
    gene_sets.update(read_gmt(REACTOME, "Reactome"))
    gene_sets.update(curated_sets())
    gene_sets.update(cell_sets())
    with (PROV / "phase1b_gene_sets.json").open("w") as f:
        json.dump(gene_sets, f, indent=2, sort_keys=True)

    specs = [
        ("discovery", "Lesional Skin", "Skin_norm_counts_d.txt", "LS"),
        ("discovery", "Nonlesional Skin", "Skin_norm_counts_d.txt", "NL"),
        ("discovery", "Whole Blood", "Blood_norm_counts_d.txt", "BLD"),
        ("replication", "Lesional Skin", "Skin_norm_counts_r.txt", "LS"),
        ("replication", "Nonlesional Skin", "Skin_norm_counts_r.txt", "NL"),
    ]
    all_defs = []
    view_scores = []
    for cohort, tissue, file_name, code in specs:
        sym = to_symbol(patient_matrix(read_matrix(file_name), meta, cohort, tissue))
        gs, defs1 = score_gene_sets(sym, gene_sets)
        dc_scores, defs2 = decoupler_scores(sym)
        scores = pd.concat([gs, dc_scores], axis=1)
        scores.columns = [f"{code}__{c}" for c in scores.columns]
        scores.insert(0, "patient_id", scores.index)
        scores.insert(1, "cohort", cohort)
        scores.insert(2, "view", code)
        scores.to_csv(OUT / f"phase1b_feature_scores_{cohort}_{code}.tsv", sep="\t", index=False)
        defs = pd.concat([defs1, defs2], ignore_index=True)
        defs["view"] = code
        defs["cohort"] = cohort
        all_defs.append(defs)
        view_scores.append((cohort, code, scores.drop(columns=["cohort", "view"]).set_index("patient_id")))

    pd.concat(all_defs, ignore_index=True).drop_duplicates(["feature_id", "view"]).to_csv(
        OUT / "phase1b_feature_definitions.tsv", sep="\t", index=False
    )
    for cohort in ["discovery", "replication"]:
        parts = [x for c, _, x in view_scores if c == cohort]
        wide = pd.concat(parts, axis=1, join="outer")
        wide.insert(0, "patient_id", wide.index)
        wide.insert(1, "cohort", cohort)
        wide.to_csv(OUT / f"phase1b_feature_matrix_{cohort}.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()
