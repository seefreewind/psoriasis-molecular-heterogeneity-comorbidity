#!/usr/bin/env python3
"""Map coordinate-style summary statistics markers to HapMap3 rsIDs for LDSC."""

from __future__ import annotations

import argparse
import csv
import gzip
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LDSC_REF = (
    ROOT
    / "data"
    / "genetics"
    / "reference"
    / "ldsc"
    / "eur_w_ld_chr_zenodo18749273"
    / "eur_w_ld_chr"
)
MARKER_RE = re.compile(r"^(?P<chrom>[0-9]+):(?P<bp>[0-9]+)_(?P<a>[ACGTacgt]+)_(?P<b>[ACGTacgt]+)$")


def read_hm3_alleles() -> dict[str, tuple[str, str]]:
    alleles: dict[str, tuple[str, str]] = {}
    with (LDSC_REF / "w_hm3.snplist").open(newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            alleles[row["SNP"]] = (row["A1"].upper(), row["A2"].upper())
    return alleles


def read_hm3_positions() -> dict[tuple[str, str], list[str]]:
    by_pos: dict[tuple[str, str], list[str]] = defaultdict(list)
    for chrom in range(1, 23):
        with gzip.open(LDSC_REF / f"{chrom}.l2.ldscore.gz", "rt", newline="") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                by_pos[(row["CHR"], row["BP"])].append(row["SNP"])
    return by_pos


def opener(path: Path, mode: str):
    return gzip.open(path, mode, newline="") if path.suffix == ".gz" else path.open(mode, newline="")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--qc", required=True)
    parser.add_argument("--marker-col", default="MarkerName")
    parser.add_argument("--a1-col", default="Allele1")
    parser.add_argument("--a2-col", default="Allele2")
    parser.add_argument("--keep-cols", nargs="+", required=True)
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)
    qc_path = Path(args.qc)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    qc_path.parent.mkdir(parents=True, exist_ok=True)

    hm3_alleles = read_hm3_alleles()
    hm3_by_pos = read_hm3_positions()
    counts: Counter = Counter()
    seen: set[str] = set()

    with opener(in_path, "rt") as infh, gzip.open(out_path, "wt", newline="") as outfh:
        reader = csv.DictReader(infh, delimiter="\t")
        fieldnames = ["SNP", "chromosome", "base_pair_location"] + args.keep_cols
        writer = csv.DictWriter(outfh, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in reader:
            counts["total_rows"] += 1
            marker = row[args.marker_col]
            match = MARKER_RE.match(marker)
            if match is None:
                counts["marker_parse_fail"] += 1
                continue
            chrom = match.group("chrom")
            bp = match.group("bp")
            a1 = row[args.a1_col].upper()
            a2 = row[args.a2_col].upper()
            if len(a1) != 1 or len(a2) != 1 or a1 not in "ACGT" or a2 not in "ACGT":
                counts["non_acgt_or_non_snp"] += 1
                continue
            snps = hm3_by_pos.get((chrom, bp))
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
            if {a1, a2} != set(hm3):
                counts["allele_pair_mismatch"] += 1
                continue
            if snp in seen:
                counts["duplicate_output_snp"] += 1
                continue
            seen.add(snp)
            counts["mapped_hm3_allele_matched"] += 1
            out_row = {"SNP": snp, "chromosome": chrom, "base_pair_location": bp}
            out_row.update({col: row[col] for col in args.keep_cols})
            writer.writerow(out_row)

    with qc_path.open("w", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerow(["metric", "value"])
        for key in sorted(counts):
            writer.writerow([key, counts[key]])
        total = counts["total_rows"]
        mapped = counts["mapped_hm3_allele_matched"]
        writer.writerow(["mapped_fraction_of_raw", f"{mapped / total:.6f}" if total else "NA"])
        writer.writerow(["output_sumstats", str(out_path)])
        writer.writerow(["ldsc_reference", str(LDSC_REF)])


if __name__ == "__main__":
    main()
