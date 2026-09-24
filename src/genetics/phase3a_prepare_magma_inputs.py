#!/usr/bin/env python3
"""Prepare fixed Phase 3A gene mapping and MAGMA input files."""

from __future__ import annotations

import csv
import gzip
import hashlib
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PHASE2A = ROOT / "results" / "phase2a" / "axis_gene_programs"
OUT = ROOT / "results" / "phase3a"
GWAS = ROOT / "data" / "genetics" / "psoriasis_GCST90472771" / "GCST90472771.tsv.gz"
GENE_LOC = ROOT / "data" / "genetics" / "reference" / "magma" / "NCBI37.3" / "NCBI37.3.gene.loc"
BIM = ROOT / "data" / "genetics" / "reference" / "magma" / "g1000_eur" / "g1000_eur.bim"

AXES = ["F1", "F2", "F6", "F7"]
MHC_CHR = "6"
MHC_START = 25_000_000
MHC_END = 34_000_000


def hash_core(axis: str) -> str:
    h = hashlib.sha256()
    with (PHASE2A / f"{axis}_gene_program.tsv").open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_gene_loc() -> dict[str, dict[str, str]]:
    by_symbol: dict[str, dict[str, str]] = {}
    with GENE_LOC.open() as fh:
        for line in fh:
            entrez, chrom, start, end, strand, symbol = line.rstrip("\n").split("\t")
            by_symbol.setdefault(symbol.upper(), {
                "gene_id": entrez,
                "chromosome": chrom,
                "start": start,
                "end": end,
                "symbol": symbol,
            })
    return by_symbol


def read_program(axis: str) -> list[dict[str, str]]:
    path = PHASE2A / f"{axis}_gene_program.tsv"
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def is_mhc(chrom: str, start: str, end: str) -> bool:
    if chrom != MHC_CHR:
        return False
    return int(start) <= MHC_END and int(end) >= MHC_START


def write_gene_sets_and_mapping() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    gene_loc = read_gene_loc()
    mapping_rows = []
    coverage_rows = []
    mhc_rows = []
    overlap_core: dict[str, set[str]] = {}

    for axis in AXES:
        rows = read_program(axis)
        for program_type in ["CORE", "EXTENDED"]:
            genes = []
            for row in rows:
                if row["leading_edge_status"] == "CORE" or program_type == "EXTENDED":
                    genes.append(row["gene_symbol"])
            unique_genes = sorted(dict.fromkeys(genes))
            overlap_core.setdefault(axis, set())
            if program_type == "CORE":
                overlap_core[axis] = set(unique_genes)
            mapped = 0
            mhc = 0
            primary = 0
            geneset_genes = []
            for gene in unique_genes:
                rec = gene_loc.get(gene.upper())
                if rec is None:
                    status = "unmapped_to_NCBI37.3_gene_loc"
                    chrom = start = end = gene_id = "NA"
                    mhc_status = "not_mapped"
                    included = "False"
                    reason = status
                else:
                    mapped += 1
                    gene_id = rec["gene_id"]
                    chrom, start, end = rec["chromosome"], rec["start"], rec["end"]
                    mhc_flag = is_mhc(chrom, start, end)
                    mhc_status = "MHC" if mhc_flag else "non_MHC"
                    if mhc_flag:
                        mhc += 1
                    included = "False" if mhc_flag else "True"
                    reason = "MHC_excluded_primary" if mhc_flag else "included_primary"
                    if not mhc_flag:
                        primary += 1
                    geneset_genes.append(gene_id)
                mapping_rows.append({
                    "axis": axis,
                    "program_type": program_type,
                    "gene_symbol": gene,
                    "gene_id": gene_id,
                    "annotation_status": status if rec is None else "mapped",
                    "chromosome": chrom,
                    "start": start,
                    "end": end,
                    "MHC_status": mhc_status,
                    "included_primary": included,
                    "exclusion_reason": reason,
                })
                if rec is not None and mhc_status == "MHC":
                    mhc_rows.append({
                        "axis": axis,
                        "program_type": program_type,
                        "gene_symbol": gene,
                        "gene_id": gene_id,
                        "chromosome": chrom,
                        "start": start,
                        "end": end,
                        "MHC_definition": f"chr6:{MHC_START}-{MHC_END}_GRCh37",
                    })
            coverage_rows.append({
                "axis": axis,
                "program_type": program_type,
                "frozen_gene_count": len(unique_genes),
                "mapped_genes": mapped,
                "unmapped_genes": len(unique_genes) - mapped,
                "MHC_genes": mhc,
                "primary_analysis_genes": primary,
                "percentage_retained_primary": round(primary / len(unique_genes) * 100, 3) if unique_genes else 0,
                "gene_program_sha256": hash_core(axis),
            })
            prefix = OUT / f"gene_set_{axis}_{program_type}"
            with (prefix.with_suffix(".all_mapped.geneset")).open("w") as fh:
                fh.write(f"{axis}_{program_type}\t" + "\t".join(sorted(set(geneset_genes))) + "\n")
            primary_ids = [r["gene_id"] for r in mapping_rows if r["axis"] == axis and r["program_type"] == program_type and r["included_primary"] == "True"]
            with (prefix.with_suffix(".MHC_excluded.geneset")).open("w") as fh:
                fh.write(f"{axis}_{program_type}_MHC_EXCLUDED\t" + "\t".join(sorted(set(primary_ids))) + "\n")

    with (OUT / "axis_gene_annotation_mapping.tsv").open("w", newline="") as fh:
        fieldnames = ["axis", "program_type", "gene_symbol", "gene_id", "annotation_status", "chromosome", "start", "end", "MHC_status", "included_primary", "exclusion_reason"]
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(mapping_rows)

    with (OUT / "axis_gene_mapping_coverage.tsv").open("w", newline="") as fh:
        fieldnames = ["axis", "program_type", "frozen_gene_count", "mapped_genes", "unmapped_genes", "MHC_genes", "primary_analysis_genes", "percentage_retained_primary", "gene_program_sha256"]
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(coverage_rows)

    with (OUT / "MHC_gene_membership.tsv").open("w", newline="") as fh:
        fieldnames = ["axis", "program_type", "gene_symbol", "gene_id", "chromosome", "start", "end", "MHC_definition"]
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(mhc_rows)

    overlap_rows = []
    for i, a in enumerate(AXES):
        for b in AXES[i + 1:]:
            shared = overlap_core[a] & overlap_core[b]
            union = overlap_core[a] | overlap_core[b]
            smaller = min(len(overlap_core[a]), len(overlap_core[b]))
            overlap_rows.append({
                "factor_a": a,
                "factor_b": b,
                "jaccard": len(shared) / len(union) if union else 0,
                "overlap_coefficient": len(shared) / smaller if smaller else 0,
                "shared_gene_count": len(shared),
                "unique_a_count": len(overlap_core[a] - overlap_core[b]),
                "unique_b_count": len(overlap_core[b] - overlap_core[a]),
            })
    with (OUT / "axis_gene_overlap_genetics.tsv").open("w", newline="") as fh:
        fieldnames = ["factor_a", "factor_b", "jaccard", "overlap_coefficient", "shared_gene_count", "unique_a_count", "unique_b_count"]
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(overlap_rows)


def prepare_magma_pvals() -> None:
    # Restrict reference map to positions present in GWAS to keep memory bounded.
    gwas_positions: set[tuple[str, str]] = set()
    with gzip.open(GWAS, "rt", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        for row in reader:
            gwas_positions.add((row["chromosome"], row["base_pair_location"]))

    ref_by_pos: dict[tuple[str, str], list[tuple[str, str, str]]] = defaultdict(list)
    with BIM.open() as fh:
        for line in fh:
            chrom, snp, _cm, pos, a1, a2 = line.rstrip("\n").split()
            key = (chrom, pos)
            if key in gwas_positions:
                ref_by_pos[key].append((snp, a1.upper(), a2.upper()))

    total = mapped = allele_mismatch = no_ref_position = duplicate_ref_match = non_snp = 0
    seen_snps: set[str] = set()
    out_pval = OUT / "GCST90472771.magma_pvals.tsv"
    with gzip.open(GWAS, "rt", newline="") as fh, out_pval.open("w", newline="") as outfh:
        reader = csv.DictReader(fh, delimiter="\t")
        writer = csv.writer(outfh, delimiter="\t")
        writer.writerow(["SNP", "P", "N"])
        for row in reader:
            total += 1
            ea = row["effect_allele"].upper()
            oa = row["other_allele"].upper()
            if len(ea) != 1 or len(oa) != 1 or ea not in "ACGT" or oa not in "ACGT":
                non_snp += 1
                continue
            refs = ref_by_pos.get((row["chromosome"], row["base_pair_location"]))
            if not refs:
                no_ref_position += 1
                continue
            matches = [snp for snp, a1, a2 in refs if {ea, oa} == {a1, a2}]
            if not matches:
                allele_mismatch += 1
                continue
            snp = matches[0]
            if snp in seen_snps:
                duplicate_ref_match += 1
                continue
            seen_snps.add(snp)
            mapped += 1
            writer.writerow([snp, row["p_value"], row["cum_eff_sample_size"]])

    with (OUT / "magma_snp_mapping_qc.tsv").open("w", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerow(["metric", "value"])
        for key, value in [
            ("total_gwas_variants", total),
            ("mapped_to_g1000_eur_rsids", mapped),
            ("non_snp_or_non_acgt_skipped", non_snp),
            ("no_reference_position", no_ref_position),
            ("allele_mismatch", allele_mismatch),
            ("duplicate_reference_snp_match_skipped", duplicate_ref_match),
            ("mapping_rate_percent", round(mapped / total * 100, 3)),
        ]:
            writer.writerow([key, value])


def main() -> None:
    write_gene_sets_and_mapping()
    prepare_magma_pvals()


if __name__ == "__main__":
    main()
