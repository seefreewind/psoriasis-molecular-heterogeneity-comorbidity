#!/usr/bin/env python3

from pathlib import Path

import pandas as pd


ROOT = Path.cwd()
BASE = ROOT / "results/phase4br_ld_reference_validation"
UKB_DIR = BASE / "ukb_lava" / "loci"
OUT = BASE / "phase4br_ld_reference_comparison.tsv"
SUMMARY = BASE / "phase4br_tier_summary.tsv"

priority = pd.read_csv(BASE / "phase4br_priority_loci.tsv", sep="\t")
priority["locus"] = priority["locus"].astype(str)

frames = []
for path in sorted(UKB_DIR.glob("*_bivar.tsv")) if UKB_DIR.exists() else []:
    df = pd.read_csv(path, sep="\t")
    frames.append(df)
ukb = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
if not ukb.empty:
    ukb["locus"] = ukb["locus"].astype(str)
    ukb = ukb.drop_duplicates(["outcome", "locus"], keep="first")
    ukb = ukb.rename(
        columns={
            "rho": "rho_ukb",
            "p": "p_ukb",
            "h2_psoriasis": "h2_psoriasis_ukb",
            "h2_outcome": "h2_outcome_ukb",
            "univ_p_psoriasis": "univ_p_psoriasis_ukb",
            "univ_p_outcome": "univ_p_outcome_ukb",
            "se_approx": "se_approx_ukb",
            "z_approx": "z_approx_ukb",
        }
    )
else:
    ukb = pd.DataFrame(columns=["outcome", "locus"])

status_frames = []
for path in sorted(UKB_DIR.glob("*_status.tsv")) if UKB_DIR.exists() else []:
    status_frames.append(pd.read_csv(path, sep="\t"))
status = pd.concat(status_frames, ignore_index=True) if status_frames else pd.DataFrame()
if not status.empty:
    status["locus"] = status["locus"].astype(str)
    status = status.drop_duplicates(["outcome", "locus"], keep="last")
else:
    status = pd.DataFrame(columns=["outcome", "locus", "status"])

base_cols = [
    "outcome",
    "pair_scope",
    "validation_priority",
    "locus",
    "chr",
    "start",
    "stop",
    "rho",
    "p",
    "fdr_within_outcome",
    "fdr_all_tests",
    "direction",
    "h2_psoriasis",
    "h2_outcome",
    "univ_p_psoriasis",
    "univ_p_outcome",
]
merged = priority[base_cols].rename(
    columns={
        "rho": "rho_1000g",
        "p": "p_1000g",
        "h2_psoriasis": "h2_psoriasis_1000g",
        "h2_outcome": "h2_outcome_1000g",
        "univ_p_psoriasis": "univ_p_psoriasis_1000g",
        "univ_p_outcome": "univ_p_outcome_1000g",
    }
)
if not ukb.empty:
    keep = [
        c
        for c in [
            "outcome",
            "locus",
            "rho_ukb",
            "se_approx_ukb",
            "z_approx_ukb",
            "p_ukb",
            "h2_psoriasis_ukb",
            "h2_outcome_ukb",
            "univ_p_psoriasis_ukb",
            "univ_p_outcome_ukb",
        ]
        if c in ukb.columns
    ]
    merged = merged.merge(ukb[keep], on=["outcome", "locus"], how="left")
merged = merged.merge(status[["outcome", "locus", "status"]], on=["outcome", "locus"], how="left")

merged["ukb_status"] = merged["status"].fillna("NOT_RUN")
merged["direction_ukb"] = merged["rho_ukb"].map(lambda x: "positive" if pd.notna(x) and x > 0 else ("negative" if pd.notna(x) else pd.NA))
merged["direction_concordant"] = (
    (merged["rho_1000g"] > 0) & (merged["rho_ukb"] > 0)
) | ((merged["rho_1000g"] < 0) & (merged["rho_ukb"] < 0))
merged["ukb_local_h2_reliable"] = (
    (merged["univ_p_psoriasis_ukb"].astype(float) < 0.05)
    & (merged["univ_p_outcome_ukb"].astype(float) < 0.05)
)
merged["ukb_fdr_within_outcome"] = pd.NA
for outcome, idx in merged[pd.notna(merged["p_ukb"])].groupby("outcome").groups.items():
    p = merged.loc[idx, "p_ukb"].astype(float)
    order = p.sort_values().index
    m = len(order)
    q = pd.Series(index=order, dtype=float)
    prev = 1.0
    for rank, ix in reversed(list(enumerate(order, start=1))):
        val = min(prev, float(p.loc[ix]) * m / rank)
        q.loc[ix] = val
        prev = val
    merged.loc[order, "ukb_fdr_within_outcome"] = q.loc[order]


def tier(row):
    if row["ukb_status"] != "OK" or pd.isna(row.get("rho_ukb")):
        return "Tier 3"
    if not row["direction_concordant"] or not row["ukb_local_h2_reliable"]:
        return "Tier 3"
    if pd.notna(row["ukb_fdr_within_outcome"]) and float(row["ukb_fdr_within_outcome"]) < 0.05:
        return "Tier 1"
    if pd.notna(row["p_ukb"]) and float(row["p_ukb"]) < 0.05:
        return "Tier 2"
    return "Tier 2"


merged["phase4br_tier"] = merged.apply(tier, axis=1)
merged["phase4c_coloc_eligible"] = merged["phase4br_tier"].isin(["Tier 1", "Tier 2"])
merged.to_csv(OUT, sep="\t", index=False)

summary = (
    merged.groupby(["outcome", "phase4br_tier"])
    .size()
    .reset_index(name="n_loci")
    .sort_values(["outcome", "phase4br_tier"])
)
summary.to_csv(SUMMARY, sep="\t", index=False)

print(summary.to_string(index=False))
