#!/usr/bin/env python3
"""Summarize Phase 4C SMR/HEIDI results."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd


ROOT = Path("/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity")
RUN_MANIFEST = Path(
    os.environ.get(
        "PHASE4C_SMR_RUN_MANIFEST",
        ROOT / "results/phase4c_smr/phase4c_smr1_run_manifest.tsv",
    )
)
CANDIDATES = ROOT / "results/phase4c_preparation/phase4c_coloc_candidate_loci.tsv"
OUTDIR = ROOT / "results/phase4c_smr"
ALL = Path(
    os.environ.get("PHASE4C_SMR_ALL_RESULTS", OUTDIR / "phase4c_smr1_all_results.tsv")
)
TOP = Path(
    os.environ.get("PHASE4C_SMR_TOP_RESULTS", OUTDIR / "phase4c_smr1_top_results.tsv")
)
SUMMARY = Path(
    os.environ.get("PHASE4C_SMR_SUMMARY", OUTDIR / "phase4c_smr1_summary.tsv")
)


def bh(p: pd.Series) -> pd.Series:
    p = pd.to_numeric(p, errors="coerce")
    out = pd.Series(index=p.index, dtype=float)
    valid = p.dropna()
    if valid.empty:
        return out
    order = valid.sort_values().index
    ranked = valid.loc[order]
    m = len(ranked)
    vals = ranked.to_numpy()
    q = vals * m / (pd.Series(range(1, m + 1), index=order).to_numpy())
    q = pd.Series(q, index=order).iloc[::-1].cummin().iloc[::-1].clip(upper=1)
    out.loc[q.index] = q
    return out


def load_results() -> pd.DataFrame:
    manifest = pd.read_csv(RUN_MANIFEST, sep="\t")
    pieces = []
    for row in manifest.itertuples(index=False):
        path = Path(row.smr_file)
        if row.status != "PASS" or not path.exists() or path.stat().st_size == 0:
            continue
        x = pd.read_csv(path, sep="\t")
        if x.empty:
            continue
        x.insert(0, "outcome", row.outcome)
        x.insert(1, "tissue", row.tissue)
        pieces.append(x)
    return pd.concat(pieces, ignore_index=True) if pieces else pd.DataFrame()


def add_locus(results: pd.DataFrame) -> pd.DataFrame:
    cand = pd.read_csv(CANDIDATES, sep="\t")
    rows = []
    for r in results.itertuples(index=False):
        hit = cand.loc[
            (cand["outcome"] == r.outcome)
            & (cand["chr"] == int(r.ProbeChr))
            & (cand["start"] <= int(r.Probe_bp))
            & (cand["stop"] >= int(r.Probe_bp))
        ]
        base = r._asdict()
        if hit.empty:
            base.update(
                {
                    "locus": pd.NA,
                    "phase4br_tier": pd.NA,
                    "local_direction_group": pd.NA,
                    "rho_ukb": pd.NA,
                    "p_ukb": pd.NA,
                }
            )
            rows.append(base)
        else:
            for h in hit.itertuples(index=False):
                b = dict(base)
                b.update(
                    {
                        "locus": h.locus,
                        "phase4br_tier": h.phase4br_tier,
                        "local_direction_group": h.local_direction_group,
                        "rho_ukb": h.rho_ukb,
                        "p_ukb": h.p_ukb,
                    }
                )
                rows.append(b)
    return pd.DataFrame(rows)


def main() -> None:
    results = load_results()
    if results.empty:
        raise SystemExit("No SMR results found")
    results = add_locus(results)
    results["p_SMR"] = pd.to_numeric(results["p_SMR"], errors="coerce")
    results["p_HEIDI"] = pd.to_numeric(results["p_HEIDI"], errors="coerce")
    results["smr_fdr_global"] = bh(results["p_SMR"])
    results["smr_fdr_within_outcome"] = results.groupby("outcome", group_keys=False)["p_SMR"].apply(bh)
    results["smr_fdr_within_outcome_tissue"] = results.groupby(
        ["outcome", "tissue"], group_keys=False
    )["p_SMR"].apply(bh)
    results["heidi_pass_0p01"] = results["p_HEIDI"].isna() | (results["p_HEIDI"] > 0.01)
    results["smr_primary_signal"] = (
        (results["smr_fdr_global"] < 0.05) & results["heidi_pass_0p01"]
    )

    sort_cols = ["smr_primary_signal", "smr_fdr_global", "p_SMR"]
    results.sort_values(sort_cols, ascending=[False, True, True]).to_csv(
        ALL, sep="\t", index=False
    )

    top = (
        results.sort_values(["outcome", "tissue", "p_SMR"])
        .groupby(["outcome", "tissue"], as_index=False)
        .head(10)
    )
    top.to_csv(TOP, sep="\t", index=False)

    summary = (
        results.groupby(["outcome", "tissue"], dropna=False)
        .agg(
            n_results=("probeID", "size"),
            n_global_fdr=("smr_fdr_global", lambda x: int((x < 0.05).sum())),
            n_global_fdr_heidi=("smr_primary_signal", "sum"),
            min_p_smr=("p_SMR", "min"),
            min_fdr_global=("smr_fdr_global", "min"),
        )
        .reset_index()
        .sort_values(["outcome", "min_p_smr"])
    )
    summary.to_csv(SUMMARY, sep="\t", index=False)
    print(summary.to_string(index=False))
    print(f"Wrote {ALL}")
    print(f"Wrote {TOP}")
    print(f"Wrote {SUMMARY}")


if __name__ == "__main__":
    main()
