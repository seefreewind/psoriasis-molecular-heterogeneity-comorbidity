#!/usr/bin/env python3
"""Prepare Phase 4C coloc candidate loci from Phase 4B-R LD-reference tiers."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
INFILE = ROOT / "results/phase4br_ld_reference_validation/phase4br_ld_reference_comparison.tsv"
OUTDIR = ROOT / "results/phase4c_preparation"
OUTFILE = OUTDIR / "phase4c_coloc_candidate_loci.tsv"
SUMMARY = OUTDIR / "phase4c_coloc_candidate_summary.tsv"


TISSUE_PRIORITY = {
    "cad": "skin;blood;vascular_arterial",
    "psa": "skin;blood_immune",
    "crohn": "skin;blood;intestinal;immune",
    "uc": "skin;blood;intestinal;immune",
}

PAIR_ROLE = {
    "cad": "primary_systemic_cardiovascular",
    "psa": "positive_control_near_neighbor",
    "crohn": "ibd_direction_heterogeneity",
    "uc": "ibd_direction_heterogeneity",
}


def classify_local_direction(row: pd.Series) -> str:
    rho = row["rho_ukb"]
    if pd.isna(rho):
        rho = row["rho_1000g"]
    if rho > 0:
        return "positive_local_rg"
    if rho < 0:
        return "negative_local_rg"
    return "zero_or_unresolved"


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    comparison = pd.read_csv(INFILE, sep="\t")

    candidates = comparison.loc[comparison["phase4c_coloc_eligible"].astype(bool)].copy()
    candidates["phase4c_role"] = candidates["outcome"].map(PAIR_ROLE)
    candidates["eqtl_tissue_priority"] = candidates["outcome"].map(TISSUE_PRIORITY)
    candidates["local_direction_group"] = candidates.apply(classify_local_direction, axis=1)
    candidates["coloc_priority"] = candidates["phase4br_tier"].map(
        {"Tier 1": "primary_coloc", "Tier 2": "sensitivity_coloc"}
    )

    keep = [
        "outcome",
        "phase4c_role",
        "locus",
        "chr",
        "start",
        "stop",
        "phase4br_tier",
        "coloc_priority",
        "local_direction_group",
        "rho_1000g",
        "p_1000g",
        "rho_ukb",
        "p_ukb",
        "ukb_fdr_within_outcome",
        "h2_psoriasis_ukb",
        "h2_outcome_ukb",
        "eqtl_tissue_priority",
        "validation_priority",
    ]
    candidates[keep].sort_values(
        ["outcome", "phase4br_tier", "local_direction_group", "p_ukb", "locus"]
    ).to_csv(OUTFILE, sep="\t", index=False)

    summary = (
        candidates.groupby(
            ["outcome", "phase4br_tier", "local_direction_group", "coloc_priority"],
            dropna=False,
        )
        .size()
        .reset_index(name="n_loci")
        .sort_values(["outcome", "phase4br_tier", "local_direction_group"])
    )
    summary.to_csv(SUMMARY, sep="\t", index=False)

    print(f"Wrote {OUTFILE} ({len(candidates)} loci)")
    print(f"Wrote {SUMMARY}")


if __name__ == "__main__":
    main()
