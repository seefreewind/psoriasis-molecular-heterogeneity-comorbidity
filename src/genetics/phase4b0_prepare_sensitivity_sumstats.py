#!/usr/bin/env python3
"""Prepare sensitivity LDSC sumstats for Phase 4B-0 adjudication."""

from __future__ import annotations

import csv
import gzip
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
LDSC_REF = ROOT / "data" / "genetics" / "reference" / "ldsc" / "eur_w_ld_chr_zenodo18749273" / "eur_w_ld_chr"
MUNGE = ROOT / "results" / "phase4a" / "munge"
OUT = ROOT / "results" / "phase4b0" / "sensitivity_sumstats"
MHC_START = 25_000_000
MHC_END = 34_000_000

TRAITS = [
    "psoriasis_GCST90472771",
    "psoriatic_arthritis_GCST90243956",
    "crohn_disease_GCST004132",
    "ulcerative_colitis_GCST004133",
    "coronary_artery_disease_CADMETA_eu",
]


def read_snp_positions() -> pd.DataFrame:
    frames = []
    for chrom in range(1, 23):
        path = LDSC_REF / f"{chrom}.l2.ldscore.gz"
        df = pd.read_csv(path, sep=r"\s+", compression="gzip", usecols=["CHR", "SNP", "BP"])
        frames.append(df)
    old_chr6 = LDSC_REF / "6_old.l2.ldscore.gz"
    if old_chr6.exists():
        frames.append(pd.read_csv(old_chr6, sep=r"\s+", compression="gzip", usecols=["CHR", "SNP", "BP"]))
    return pd.concat(frames, ignore_index=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    positions = read_snp_positions()
    mhc_snps = set(positions.loc[(positions["CHR"] == 6) & (positions["BP"].between(MHC_START, MHC_END)), "SNP"])
    qc_rows = []
    for trait in TRAITS:
        src = MUNGE / f"{trait}.sumstats.gz"
        df = pd.read_csv(src, sep=r"\s+", compression="gzip")
        before = len(df)
        before_nonmissing = df["Z"].notna().sum()
        no_mhc = df[~df["SNP"].isin(mhc_snps)].copy()
        out = OUT / f"{trait}.no_mhc.sumstats.gz"
        with gzip.open(out, "wt", newline="") as fh:
            no_mhc.to_csv(fh, sep="\t", index=False, na_rep="")
        qc_rows.append({
            "trait": trait,
            "operation": "exclude_MHC_chr6_25_34Mb_GRCh37",
            "rows_before": before,
            "nonmissing_before": int(before_nonmissing),
            "rows_after": len(no_mhc),
            "nonmissing_after": int(no_mhc["Z"].notna().sum()),
            "output": str(out),
        })
        if trait in {"crohn_disease_GCST004132", "ulcerative_colitis_GCST004133"}:
            flipped = df.copy()
            flipped.loc[flipped["Z"].notna(), "Z"] = -flipped.loc[flipped["Z"].notna(), "Z"]
            out_flip = OUT / f"{trait}.sign_flipped.sumstats.gz"
            with gzip.open(out_flip, "wt", newline="") as fh:
                flipped.to_csv(fh, sep="\t", index=False, na_rep="")
            qc_rows.append({
                "trait": trait,
                "operation": "sign_flip_all_nonmissing_Z",
                "rows_before": before,
                "nonmissing_before": int(before_nonmissing),
                "rows_after": len(flipped),
                "nonmissing_after": int(flipped["Z"].notna().sum()),
                "output": str(out_flip),
            })

    with (OUT.parent / "phase4b0_sensitivity_sumstats_qc.tsv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(qc_rows[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(qc_rows)


if __name__ == "__main__":
    main()
