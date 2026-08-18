#!/usr/bin/env python3
"""Prepare LDSC-ready psoriasis summary statistics with HapMap3 rsIDs.

GCST90472771 is distributed with chromosome and base-pair coordinates but no
rsID column. LDSC munge and rg should use rsIDs that are compatible with the
LD-score reference, so this script maps the psoriasis GWAS to HapMap3 SNPs by
GRCh37 chromosome/base-pair position and checks that the reported allele pair
matches the HapMap3 allele pair.
"""

from __future__ import annotations

import csv
import gzip
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GWAS = ROOT / "data" / "genetics" / "psoriasis_GCST90472771" / "GCST90472771.tsv.gz"
LDSC_REF = (
    ROOT
    / "data"
    / "genetics"
    / "reference"
    / "ldsc"
    / "eur_w_ld_chr_zenodo18749273"
    / "eur_w_ld_chr"
)
OUTDIR = ROOT / "results" / "phase4a" / "munge_inputs"
OUT_SUMSTATS = OUTDIR / "psoriasis_GCST90472771.hm3_rsids.tsv.gz"
OUT_QC = OUTDIR / "psoriasis_GCST90472771.hm3_mapping_qc.tsv"


def read_hm3_alleles() -> dict[str, tuple[str, str]]:
    alleles: dict[str, tuple[str, str]] = {}
    with (LDSC_REF / "w_hm3.snplist").open(newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        for row in reader:
            alleles[row["SNP"]] = (row["A1"].upper(), row["A2"].upper())
    return alleles


def read_hm3_positions() -> tuple[dict[tuple[str, str], list[str]], Counter]:
    by_pos: dict[tuple[str, str], list[str]] = defaultdict(list)
    counts: Counter = Counter()
    for chrom in range(1, 23):
        path = LDSC_REF / f"{chrom}.l2.ldscore.gz"
        with gzip.open(path, "rt", newline="") as fh:
            reader = csv.DictReader(fh, delimiter="\t")
            for row in reader:
                by_pos[(row["CHR"], row["BP"])].append(row["SNP"])
                counts["hm3_ldscore_rows"] += 1
    counts["hm3_unique_positions"] = sum(1 for snps in by_pos.values() if len(snps) == 1)
    counts["hm3_duplicate_positions"] = sum(1 for snps in by_pos.values() if len(snps) > 1)
    return by_pos, counts


def is_acgt(a1: str, a2: str) -> bool:
    return len(a1) == 1 and len(a2) == 1 and a1 in "ACGT" and a2 in "ACGT"


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    hm3_alleles = read_hm3_alleles()
    hm3_by_pos, counts = read_hm3_positions()
    seen: set[str] = set()

    with gzip.open(GWAS, "rt", newline="") as infh, gzip.open(OUT_SUMSTATS, "wt", newline="") as outfh:
        reader = csv.DictReader(infh, delimiter="\t")
        fieldnames = [
            "SNP",
            "chromosome",
            "base_pair_location",
            "effect_allele",
            "other_allele",
            "beta",
            "standard_error",
            "p_value",
            "cum_eff_sample_size",
        ]
        writer = csv.DictWriter(outfh, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in reader:
            counts["total_gwas_rows"] += 1
            ea = row["effect_allele"].upper()
            oa = row["other_allele"].upper()
            if not is_acgt(ea, oa):
                counts["non_acgt_or_non_snp"] += 1
                continue

            snps = hm3_by_pos.get((row["chromosome"], row["base_pair_location"]))
            if not snps:
                counts["no_hm3_position_match"] += 1
                continue
            if len(snps) > 1:
                counts["ambiguous_hm3_position"] += 1
                continue

            snp = snps[0]
            hm3 = hm3_alleles.get(snp)
            if hm3 is None:
                counts["hm3_position_missing_snplist_alleles"] += 1
                continue
            if {ea, oa} != set(hm3):
                counts["allele_pair_mismatch"] += 1
                continue
            if snp in seen:
                counts["duplicate_output_snp"] += 1
                continue

            seen.add(snp)
            counts["mapped_hm3_allele_matched"] += 1
            writer.writerow(
                {
                    "SNP": snp,
                    "chromosome": row["chromosome"],
                    "base_pair_location": row["base_pair_location"],
                    "effect_allele": ea,
                    "other_allele": oa,
                    "beta": row["beta"],
                    "standard_error": row["standard_error"],
                    "p_value": row["p_value"],
                    "cum_eff_sample_size": row["cum_eff_sample_size"],
                }
            )

    with OUT_QC.open("w", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerow(["metric", "value"])
        for key in sorted(counts):
            writer.writerow([key, counts[key]])
        total = counts["total_gwas_rows"]
        mapped = counts["mapped_hm3_allele_matched"]
        writer.writerow(["mapped_fraction_of_raw", f"{mapped / total:.6f}" if total else "NA"])
        writer.writerow(["output_sumstats", str(OUT_SUMSTATS)])
        writer.writerow(["ldsc_reference", str(LDSC_REF)])


if __name__ == "__main__":
    main()
