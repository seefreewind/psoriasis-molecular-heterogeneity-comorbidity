#!/usr/bin/env python3
"""Feasible external support analyses for Phase 1B molecular axes."""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parents[2]
PHASE1B = ROOT / "results" / "phase1b"
EXT = ROOT / "data" / "external" / "geo"


def score_gene_sets(x: pd.DataFrame, gene_sets: dict[str, list[str]]) -> pd.DataFrame:
    ranks = x.rank(axis=1, method="average", pct=True)
    scores = {}
    available = set(ranks.columns)
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


def load_gse121212_pso() -> dict[str, pd.DataFrame]:
    path = EXT / "GSE121212_readcount.txt.gz"
    with gzip.open(path, "rt", errors="replace") as fh:
        counts = pd.read_csv(fh, sep="\t", index_col=0)
    counts.index = counts.index.astype(str)
    pso_cols = [c for c in counts.columns if c.startswith("PSO_")]
    counts = counts[pso_cols]
    log = np.log2(counts.T + 1)
    paired = {}
    for sample in log.index:
        patient = "_".join(sample.split("_")[:2])
        if sample.endswith("_lesional"):
            paired.setdefault(patient, {})["LS"] = sample
        elif sample.endswith("_non-lesional"):
            paired.setdefault(patient, {})["NL"] = sample
    complete = {p: v for p, v in paired.items() if {"LS", "NL"} <= set(v)}
    return {
        "LS": log.loc[[v["LS"] for v in complete.values()]].set_axis(list(complete), axis=0),
        "NL": log.loc[[v["NL"] for v in complete.values()]].set_axis(list(complete), axis=0),
    }


def external_gse121212_skin_support() -> pd.DataFrame:
    gene_sets = json.loads((ROOT / "data" / "metadata" / "phase1b" / "phase1b_gene_sets.json").read_text())
    loadings = pd.read_csv(PHASE1B / "factor_loadings.tsv", sep="\t")
    views = load_gse121212_pso()
    scored = {view: score_gene_sets(mat, gene_sets) for view, mat in views.items()}
    rows = []
    for factor in sorted(loadings["factor"].unique(), key=lambda x: int(x[1:])):
        for view in ["LS", "NL"]:
            w = loadings[(loadings["factor"] == factor) & (loadings["view"] == view)].set_index("feature")["loading"]
            common = w.index.intersection(scored[view].columns)
            effect = scored[view][common].mean(axis=0)
            rows.append(
                {
                    "dataset": "GSE121212",
                    "axis": factor,
                    "view": view,
                    "n_paired_psoriasis_patients": len(scored[view]),
                    "n_common_axis_features": len(common),
                    "loading_vs_external_mean_score_spearman": safe_spearman(w.loc[common], effect.loc[common]),
                    "interpretation": "paired_psoriasis_skin_external_support_not_full_blood_replication",
                }
            )
    out = pd.DataFrame(rows)
    out.to_csv(PHASE1B / "external_axis_support.tsv", sep="\t", index=False)
    return out


def main() -> None:
    external_gse121212_skin_support()


if __name__ == "__main__":
    main()
