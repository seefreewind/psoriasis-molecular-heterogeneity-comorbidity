#!/usr/bin/env python3
"""Phase 4B-0 direction and QC adjudication for anomalous global rg results."""

from __future__ import annotations

import csv
import gzip
import math
from pathlib import Path
from typing import Iterable

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
MUNGE = ROOT / "results" / "phase4a" / "munge"
INPUTS = ROOT / "results" / "phase4a" / "munge_inputs"
OUT = ROOT / "results" / "phase4b0"
REPORT = ROOT / "reports" / "PHASE4B0_RG_SIGN_QC_ADJUDICATION.md"


TRAITS = {
    "psoriasis_GCST90472771": {
        "label": "Psoriasis",
        "input": INPUTS / "psoriasis_GCST90472771.hm3_rsids.tsv.gz",
        "a1": "effect_allele",
        "a2": "other_allele",
        "effect": "beta",
        "se": "standard_error",
    },
    "psoriatic_arthritis_GCST90243956": {
        "label": "Psoriatic arthritis",
        "input": ROOT / "data" / "genetics" / "phase4a_raw" / "psoriatic_arthritis_GCST90243956" / "GCST90243956.tsv",
        "snp": "rs_id",
        "a1": "effect_allele",
        "a2": "other_allele",
        "effect": "beta",
        "se": "standard_error",
    },
    "crohn_disease_GCST004132": {
        "label": "Crohn disease",
        "input": INPUTS / "crohn_disease_GCST004132.hm3_rsids.tsv.gz",
        "a1": "Allele1",
        "a2": "Allele2",
        "effect": "Effect",
        "se": "StdErr",
    },
    "ulcerative_colitis_GCST004133": {
        "label": "Ulcerative colitis",
        "input": INPUTS / "ulcerative_colitis_GCST004133.hm3_rsids.tsv.gz",
        "a1": "Allele1",
        "a2": "Allele2",
        "effect": "Effect",
        "se": "StdErr",
    },
    "coronary_artery_disease_CADMETA_eu": {
        "label": "Coronary artery disease",
        "input": INPUTS / "coronary_artery_disease_CADMETA_eu.ldsc_input.tsv.gz",
        "a1": "Allele1",
        "a2": "Allele2",
        "effect": "Effect",
        "se": "StdErr",
    },
}


def read_table(path: Path, usecols: list[str] | None = None, chunksize: int | None = None):
    compression = "gzip" if path.suffix == ".gz" else None
    return pd.read_csv(path, sep=r"\s+", compression=compression, usecols=usecols, chunksize=chunksize)


def read_munged(trait: str) -> pd.DataFrame:
    path = MUNGE / f"{trait}.sumstats.gz"
    df = read_table(path)
    df = df.dropna(subset=["Z"]).copy()
    df["A1"] = df["A1"].str.upper()
    df["A2"] = df["A2"].str.upper()
    return df


def iter_input_rows(cfg: dict, snps: set[str]) -> Iterable[pd.DataFrame]:
    path = cfg["input"]
    snp_col = cfg.get("snp", "SNP")
    usecols = [snp_col, cfg["a1"], cfg["a2"], cfg["effect"], cfg["se"]]
    reader = read_table(path, usecols=usecols, chunksize=500_000)
    for chunk in reader:
        chunk = chunk.rename(columns={snp_col: "SNP"})
        chunk = chunk[chunk["SNP"].isin(snps)]
        if not chunk.empty:
            yield chunk


def direction_audit(trait: str, cfg: dict) -> dict[str, object]:
    munged = read_munged(trait)
    snps = set(munged["SNP"])
    raw = pd.concat(iter_input_rows(cfg, snps), ignore_index=True)
    raw[cfg["a1"]] = raw[cfg["a1"]].str.upper()
    raw[cfg["a2"]] = raw[cfg["a2"]].str.upper()
    raw["raw_z"] = pd.to_numeric(raw[cfg["effect"]], errors="coerce") / pd.to_numeric(raw[cfg["se"]], errors="coerce")
    merged = raw.merge(munged[["SNP", "A1", "A2", "Z"]], on="SNP", how="inner")
    same = (merged["A1"] == merged[cfg["a1"]]) & (merged["A2"] == merged[cfg["a2"]])
    flipped = (merged["A1"] == merged[cfg["a2"]]) & (merged["A2"] == merged[cfg["a1"]])
    merged["expected_z"] = float("nan")
    merged.loc[same, "expected_z"] = merged.loc[same, "raw_z"]
    merged.loc[flipped, "expected_z"] = -merged.loc[flipped, "raw_z"]
    valid = merged.dropna(subset=["expected_z", "Z"])
    diff = (valid["Z"] - valid["expected_z"]).abs()
    sign_ok = (valid["Z"] * valid["expected_z"]) >= 0
    out_path = OUT / f"{trait}.direction_audit_sample.tsv.gz"
    keep = valid[["SNP", cfg["a1"], cfg["a2"], "A1", "A2", "raw_z", "expected_z", "Z"]].head(200_000)
    with gzip.open(out_path, "wt", newline="") as fh:
        keep.to_csv(fh, sep="\t", index=False)
    return {
        "trait": trait,
        "label": cfg["label"],
        "munged_nonmissing_snps": len(munged),
        "raw_joined_snps": len(merged),
        "same_allele_orientation": int(same.sum()),
        "flipped_allele_orientation": int(flipped.sum()),
        "allele_orientation_unresolved": int((~(same | flipped)).sum()),
        "direction_checked_snps": len(valid),
        "sign_concordance": float(sign_ok.mean()) if len(valid) else math.nan,
        "median_abs_z_difference": float(diff.median()) if len(valid) else math.nan,
        "p99_abs_z_difference": float(diff.quantile(0.99)) if len(valid) else math.nan,
        "sample_output": str(out_path),
    }


def z_correlation(psoriasis: pd.DataFrame, trait: str) -> dict[str, object]:
    other = read_munged(trait)
    merged = psoriasis[["SNP", "Z"]].rename(columns={"Z": "Z_psoriasis"}).merge(
        other[["SNP", "Z"]].rename(columns={"Z": "Z_outcome"}), on="SNP", how="inner"
    )
    return {
        "trait": trait,
        "shared_nonmissing_snps": len(merged),
        "pearson_z_correlation": merged["Z_psoriasis"].corr(merged["Z_outcome"], method="pearson"),
        "spearman_z_correlation": merged["Z_psoriasis"].corr(merged["Z_outcome"], method="spearman"),
        "mean_z_product": float((merged["Z_psoriasis"] * merged["Z_outcome"]).mean()),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    direction_rows = []
    for trait, cfg in TRAITS.items():
        direction_rows.append(direction_audit(trait, cfg))

    direction_path = OUT / "phase4b0_direction_audit.tsv"
    with direction_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(direction_rows[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(direction_rows)

    psoriasis = read_munged("psoriasis_GCST90472771")
    z_rows = [z_correlation(psoriasis, t) for t in TRAITS if t != "psoriasis_GCST90472771"]
    z_path = OUT / "phase4b0_pairwise_z_correlation.tsv"
    with z_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(z_rows[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(z_rows)

    mapping_files = sorted(INPUTS.glob("*.hm3_mapping_qc.tsv"))
    mapping_lines = []
    for path in mapping_files:
        mapping_lines.append(f"### {path.name}")
        mapping_lines.extend(path.read_text().strip().splitlines())
        mapping_lines.append("")

    md = [
        "# Phase 4B-0 rg sign/QC adjudication",
        "",
        "## Purpose",
        "",
        "This audit adjudicates anomalous Phase 4A global rg results before restricted LAVA. It checks whether LDSC munge preserved signed effect directions after allele alignment and documents coordinate-to-rsID mapping quality for psoriasis, CD, and UC.",
        "",
        "## Direction audit",
        "",
        "| trait | checked SNPs | same orientation | flipped orientation | unresolved | sign concordance | median |Z diff| | p99 |Z diff| |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in direction_rows:
        md.append(
            f"| {r['label']} | {r['direction_checked_snps']} | {r['same_allele_orientation']} | "
            f"{r['flipped_allele_orientation']} | {r['allele_orientation_unresolved']} | "
            f"{r['sign_concordance']:.6f} | {r['median_abs_z_difference']:.6g} | {r['p99_abs_z_difference']:.6g} |"
        )
    md.extend(
        [
            "",
            "## Pairwise munged Z correlations with psoriasis",
            "",
            "| trait | shared SNPs | Pearson r | Spearman r | mean z product |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for r in z_rows:
        label = TRAITS[r["trait"]]["label"]
        md.append(
            f"| {label} | {r['shared_nonmissing_snps']} | {r['pearson_z_correlation']:.6f} | "
            f"{r['spearman_z_correlation']:.6f} | {r['mean_z_product']:.6f} |"
        )
    md.extend(
        [
            "",
            "## Coordinate mapping QC",
            "",
            "```text",
            *mapping_lines,
            "```",
            "",
            "## Interim adjudication",
            "",
            "Munge-direction audit is considered PASS when sign concordance is ~1.0, unresolved allele orientation is 0, and absolute Z differences are negligible after expected allele flips. If CD/UC remain negative under this audit, the negative rg should not be attributed to a simple A1/A2 flip in the LDSC input. The next adjudication layer is sensitivity LDSC after MHC exclusion and explicit CD/UC sign-flip stress tests.",
            "",
            f"- Direction audit table: `{direction_path}`",
            f"- Pairwise Z table: `{z_path}`",
        ]
    )
    REPORT.write_text("\n".join(md))


if __name__ == "__main__":
    main()
