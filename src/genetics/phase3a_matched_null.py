#!/usr/bin/env python3
"""Generate and summarize matched random gene-set nulls for Phase 3A."""

from __future__ import annotations

import csv
import random
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "phase3a"
AXES = ["F1", "F2", "F6", "F7"]
N_NULL = 2000
SEED = 20260811


def read_gene_results() -> dict[str, dict[str, float | str]]:
    genes = {}
    with (OUT / "magma_GCST90472771_body_only_MHC_excluded.genes.out").open() as fh:
        header = fh.readline().split()
        for line in fh:
            parts = line.split()
            if len(parts) < len(header):
                continue
            row = dict(zip(header, parts))
            gid = row["GENE"]
            start = int(row["START"])
            stop = int(row["STOP"])
            nsnps = int(row["NSNPS"])
            genes[gid] = {
                "gene_id": gid,
                "chromosome": row["CHR"],
                "start": start,
                "end": stop,
                "length": max(1, stop - start + 1),
                "nsnps": nsnps,
                "z": float(row["ZSTAT"]),
                "p": float(row["P"]),
            }
    return genes


def quantile_bins(values: list[int], n: int = 5) -> list[int]:
    vals = sorted(values)
    if not vals:
        return []
    cuts = []
    for i in range(1, n):
        idx = int(round(i * (len(vals) - 1) / n))
        cuts.append(vals[idx])
    return cuts


def assign_bin(value: int, cuts: list[int]) -> int:
    for i, cut in enumerate(cuts):
        if value <= cut:
            return i
    return len(cuts)


def read_axis_sets() -> dict[str, set[str]]:
    axis_sets = {}
    for axis in AXES:
        path = OUT / f"gene_set_{axis}_CORE.MHC_excluded.geneset"
        parts = path.read_text().strip().split("\t")
        axis_sets[axis] = set(parts[1:])
    return axis_sets


def main() -> None:
    rng = random.Random(SEED)
    genes = read_gene_results()
    axis_sets = read_axis_sets()
    universe = set(genes)

    length_cuts = quantile_bins([int(g["length"]) for g in genes.values()])
    nsnp_cuts = quantile_bins([int(g["nsnps"]) for g in genes.values()])
    bins: dict[tuple[str, int, int], list[str]] = defaultdict(list)
    broad_bins: dict[tuple[int, int], list[str]] = defaultdict(list)
    for gid, rec in genes.items():
        lb = assign_bin(int(rec["length"]), length_cuts)
        sb = assign_bin(int(rec["nsnps"]), nsnp_cuts)
        bins[(str(rec["chromosome"]), lb, sb)].append(gid)
        broad_bins[(lb, sb)].append(gid)

    with (OUT / "matched_null_core_MHC_excluded.sets.annot").open("w") as annot, (OUT / "matched_null_generation_qc.tsv").open("w", newline="") as qcfh:
        qc = csv.writer(qcfh, delimiter="\t")
        qc.writerow(["axis", "null_set_id", "target_genes", "sampled_genes", "fallback_draws"])
        for axis in AXES:
            target = [g for g in axis_sets[axis] if g in universe]
            target_size = len(target)
            target_by_bin: dict[tuple[str, int, int], int] = defaultdict(int)
            for gid in target:
                rec = genes[gid]
                target_by_bin[(str(rec["chromosome"]), assign_bin(int(rec["length"]), length_cuts), assign_bin(int(rec["nsnps"]), nsnp_cuts))] += 1
            for i in range(N_NULL):
                sampled: set[str] = set()
                fallback = 0
                for key, count in target_by_bin.items():
                    chrom, lb, sb = key
                    candidates = [g for g in bins[key] if g not in axis_sets[axis] and g not in sampled]
                    if len(candidates) < count:
                        fallback += count - len(candidates)
                        candidates = [g for g in broad_bins[(lb, sb)] if g not in axis_sets[axis] and g not in sampled]
                    if len(candidates) < count:
                        candidates = [g for g in universe if g not in axis_sets[axis] and g not in sampled]
                    sampled.update(rng.sample(candidates, min(count, len(candidates))))
                while len(sampled) < target_size:
                    sampled.add(rng.choice(list(universe - axis_sets[axis] - sampled)))
                name = f"{axis}_NULL_{i:04d}"
                annot.write(name + "\t" + "\t".join(sorted(sampled)) + "\n")
                qc.writerow([axis, name, target_size, len(sampled), fallback])


if __name__ == "__main__":
    main()
