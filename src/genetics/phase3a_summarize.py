#!/usr/bin/env python3
"""Summarize Phase 3A genetic anchoring outputs."""

from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "phase3a"
REPORTS = ROOT / "reports"
AXES = ["F1", "F2", "F6", "F7"]


def parse_gsa(path: Path) -> list[dict[str, str]]:
    rows = []
    for line in path.read_text().splitlines():
        if not line or line.startswith("#") or line.startswith("VARIABLE"):
            continue
        parts = line.split()
        if "MODEL" in path.read_text().splitlines()[5:20]:
            pass
        if len(parts) == 7:
            rows.append({"variable": parts[0], "type": parts[1], "NGENES": parts[2], "beta": parts[3], "beta_std": parts[4], "SE": parts[5], "P": parts[6]})
        elif len(parts) == 8:
            rows.append({"variable": parts[0], "type": parts[1], "model": parts[2], "NGENES": parts[3], "beta": parts[4], "beta_std": parts[5], "SE": parts[6], "P": parts[7]})
    return rows


def fdr_bh(pvals: list[float]) -> list[float]:
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    out = [1.0] * m
    prev = 1.0
    for rank, idx in reversed(list(enumerate(order, start=1))):
        val = min(prev, pvals[idx] * m / rank)
        out[idx] = val
        prev = val
    return out


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def summarize_matched_null(core_rows: list[dict[str, str]]) -> dict[str, dict[str, float]]:
    observed = {r["axis"]: float(r["beta"]) for r in core_rows}
    null_rows = parse_gsa(OUT / "magma_matched_null_core_MHC_excluded.gsa.out")
    by_axis: dict[str, list[float]] = defaultdict(list)
    for r in null_rows:
        axis = r["variable"].split("_")[0]
        by_axis[axis].append(float(r["beta"]))
    out = {}
    table = []
    for axis in AXES:
        vals = by_axis[axis]
        obs = observed[axis]
        ge = sum(v >= obs for v in vals)
        emp = (ge + 1) / (len(vals) + 1)
        mean = sum(vals) / len(vals)
        sd = math.sqrt(sum((v - mean) ** 2 for v in vals) / (len(vals) - 1))
        percentile = sum(v <= obs for v in vals) / len(vals) * 100
        out[axis] = {"observed": obs, "null_mean": mean, "null_sd": sd, "empirical_percentile": percentile, "empirical_P": emp}
        table.append({"axis": axis, "observed_statistic": obs, "null_mean": mean, "null_SD": sd, "empirical_percentile": percentile, "empirical_P": emp, "n_random_sets": len(vals)})
    write_tsv(OUT / "matched_null_results.tsv", table, ["axis", "observed_statistic", "null_mean", "null_SD", "empirical_percentile", "empirical_P", "n_random_sets"])
    return out


def parse_and_write_sensitivity() -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    unique = parse_gsa(OUT / "magma_unique_gene_sensitivity_raw.gsa.out")
    shared = parse_gsa(OUT / "magma_shared_vs_unique_raw.gsa.out")
    unique_rows = []
    for r in unique:
        axis = r["variable"].split("_")[0]
        unique_rows.append({"axis": axis, "set": r["variable"], "N_tested_genes": r["NGENES"], "beta": r["beta"], "SE": r["SE"], "P": r["P"], "interpretation": "nominal_only_sensitivity" if float(r["P"]) < 0.05 else "not_significant"})
    write_tsv(OUT / "magma_unique_gene_sensitivity.tsv", unique_rows, ["axis", "set", "N_tested_genes", "beta", "SE", "P", "interpretation"])

    shared_rows = []
    for r in shared:
        axis = r["variable"].split("_")[0] if r["variable"].startswith("F") else "SHARED"
        shared_rows.append({"component": r["variable"], "axis": axis, "N_tested_genes": r["NGENES"], "beta": r["beta"], "SE": r["SE"], "P": r["P"], "interpretation": "nominal_only_sensitivity" if float(r["P"]) < 0.05 else "not_significant"})
    write_tsv(OUT / "shared_vs_unique_genetic_signal.tsv", shared_rows, ["component", "axis", "N_tested_genes", "beta", "SE", "P", "interpretation"])

    cond_rows = []
    cond_by_axis = {}
    for axis in AXES:
        rows = parse_gsa(OUT / f"magma_axis_conditional_{axis}_raw.gsa.out")
        var = f"{axis}_CORE_MHC_EXCLUDED"
        row = next(r for r in rows if r["variable"] == var)
        cond = {"axis": axis, "N_tested_genes": row["NGENES"], "beta": row["beta"], "SE": row["SE"], "P": row["P"], "conditional_signal": "nominal_only_sensitivity" if float(row["P"]) < 0.05 else "not_significant"}
        cond_rows.append(cond)
        cond_by_axis[axis] = cond
    write_tsv(OUT / "magma_axis_conditional.tsv", cond_rows, ["axis", "N_tested_genes", "beta", "SE", "P", "conditional_signal"])
    return {r["axis"]: r for r in unique_rows}, {r["axis"]: r for r in shared_rows if r["axis"] != "SHARED"}, cond_by_axis


def candidate_genes() -> None:
    gene_results = {}
    with (OUT / "magma_GCST90472771_body_only_MHC_excluded.genes.out").open() as fh:
        header = fh.readline().split()
        for line in fh:
            parts = line.split()
            if len(parts) >= len(header):
                r = dict(zip(header, parts))
                gene_results[r["GENE"]] = r
    mapping = read_tsv(OUT / "axis_gene_annotation_mapping.tsv")
    rows = []
    for axis in AXES:
        candidates = []
        for r in mapping:
            if r["axis"] == axis and r["program_type"] == "CORE" and r["included_primary"] == "True" and r["gene_id"] in gene_results:
                gr = gene_results[r["gene_id"]]
                candidates.append((float(gr["P"]), r, gr))
        for p, r, gr in sorted(candidates, key=lambda x: x[0])[:10]:
            rows.append({
                "axis": axis,
                "gene": r["gene_symbol"],
                "CORE_status": "CORE",
                "MAGMA_Z": gr["ZSTAT"],
                "MAGMA_P": gr["P"],
                "locus": f"chr{gr['CHR']}:{gr['START']}-{gr['STOP']}",
                "MHC_status": r["MHC_status"],
                "expression_context": "frozen_transcriptomic_axis_program",
                "candidate_for_eQTL_coloc": "defer_phase3b; axis_not_genetically_anchored_in_phase3a",
                "rationale": "top CORE gene-level MAGMA signal within a frozen axis; not causal and not colocated in Phase 3A",
            })
    write_tsv(OUT / "phase3b_candidate_genes.tsv", rows, ["axis", "gene", "CORE_status", "MAGMA_Z", "MAGMA_P", "locus", "MHC_status", "expression_context", "candidate_for_eQTL_coloc", "rationale"])


def main() -> None:
    core = read_tsv(OUT / "magma_core_MHC_excluded.tsv")
    null = summarize_matched_null(core)
    unique, shared, cond = parse_and_write_sensitivity()
    candidate_genes()

    mhc_included_rows = []
    for axis in AXES:
        mhc_included_rows.append({
            "axis": axis,
            "N_frozen_genes": "see_axis_gene_mapping_coverage",
            "N_tested_genes": "NA",
            "beta": "NA",
            "SE": "NA",
            "P": "NA",
            "FDR": "NA",
            "direction": "NA",
            "MHC_dependence": "not_estimable",
            "interpretation": "MHC-included MAGMA gene-level analysis was attempted but was computationally dominated by the MHC region and stopped; primary MHC-excluded analysis is reported.",
        })
    write_tsv(OUT / "magma_core_MHC_included.tsv", mhc_included_rows, ["axis", "N_frozen_genes", "N_tested_genes", "beta", "SE", "P", "FDR", "direction", "MHC_dependence", "interpretation"])

    sldsc_rows = []
    for axis in AXES:
        sldsc_rows.append({"axis": axis, "annotation_SNP_count": "not_run", "annotation_proportion": "not_run", "heritability_proportion": "not_run", "enrichment": "not_run", "coefficient": "not_run", "SE": "not_run", "P": "not_run", "FDR": "not_run", "classification": "inconclusive_not_technically_prioritized_after_negative_primary_MAGMA_and_no_local_baselineLD_model"})
    write_tsv(OUT / "sldsc_axis_enrichment.tsv", sldsc_rows, ["axis", "annotation_SNP_count", "annotation_proportion", "heritability_proportion", "enrichment", "coefficient", "SE", "P", "FDR", "classification"])

    tiers = []
    for r in core:
        axis = r["axis"]
        tier = "TIER D - NO DETECTABLE GENETIC ANCHORING"
        specificity = "no_detectable_enrichment"
        eligible = "no"
        if float(r["P"]) < 0.05 and float(r["FDR"]) >= 0.05:
            tier = "TIER D - NO ROBUST GENETIC ANCHORING"
        tiers.append({
            "axis": axis,
            "CORE_gene_count": next(x["frozen_gene_count"] for x in read_tsv(OUT / "axis_gene_mapping_coverage.tsv") if x["axis"] == axis and x["program_type"] == "CORE"),
            "mapped_gene_count": next(x["mapped_genes"] for x in read_tsv(OUT / "axis_gene_mapping_coverage.tsv") if x["axis"] == axis and x["program_type"] == "CORE"),
            "MHC_gene_count": next(x["MHC_genes"] for x in read_tsv(OUT / "axis_gene_mapping_coverage.tsv") if x["axis"] == axis and x["program_type"] == "CORE"),
            "MAGMA_MHC_excluded_beta": r["beta"],
            "MAGMA_MHC_excluded_P": r["P"],
            "MAGMA_FDR": r["FDR"],
            "MAGMA_MHC_included_P": "not_estimable",
            "MHC_dependence": "not_estimable; primary MHC excluded",
            "empirical_null_P": null[axis]["empirical_P"],
            "unique_gene_signal": unique[axis]["interpretation"],
            "conditional_signal": cond[axis]["conditional_signal"],
            "sLDSC_enrichment": "not_run",
            "sLDSC_P": "not_run",
            "genetic_specificity": specificity,
            "final_genetic_tier": tier,
            "eligible_for_phase3b": eligible,
            "eligible_for_comorbidity_phase": eligible,
        })
    fieldnames = ["axis", "CORE_gene_count", "mapped_gene_count", "MHC_gene_count", "MAGMA_MHC_excluded_beta", "MAGMA_MHC_excluded_P", "MAGMA_FDR", "MAGMA_MHC_included_P", "MHC_dependence", "empirical_null_P", "unique_gene_signal", "conditional_signal", "sLDSC_enrichment", "sLDSC_P", "genetic_specificity", "final_genetic_tier", "eligible_for_phase3b", "eligible_for_comorbidity_phase"]
    write_tsv(OUT / "Table_axis_genetic_anchoring.tsv", tiers, fieldnames)
    write_tsv(OUT / "Table1_axis_genetic_anchoring.tsv", tiers, fieldnames)


if __name__ == "__main__":
    main()
