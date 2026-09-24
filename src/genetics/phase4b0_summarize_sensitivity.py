#!/usr/bin/env python3
"""Append Phase 4B-0 LDSC sensitivity results to the adjudication report."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results" / "phase4b0"
REPORT = ROOT / "reports" / "PHASE4B0_RG_SIGN_QC_ADJUDICATION.md"


def parse_rg(path: Path) -> dict[str, str]:
    text = path.read_text()
    out = {"log": str(path)}
    for key, pattern in {
        "rg": r"Genetic Correlation: ([\-0-9.eE]+) \(([\-0-9.eE]+)\)",
        "z": r"Z-score: ([\-0-9.eE]+)",
        "p": r"\nP: ([\-0-9.eE]+)",
    }.items():
        m = re.search(pattern, text)
        if m:
            if key == "rg":
                out["rg"], out["se"] = m.group(1), m.group(2)
            else:
                out[key] = m.group(1)
    cov_block = text.split("Genetic Covariance", 1)[-1].split("Genetic Correlation", 1)[0]
    m = re.search(r"Intercept: ([\-0-9.eE]+) \(([\-0-9.eE]+)\)", cov_block)
    if m:
        out["cross_trait_intercept"], out["cross_trait_intercept_se"] = m.group(1), m.group(2)
    return out


def main() -> None:
    rows = []
    for trait, label in [
        ("psoriatic_arthritis_GCST90243956", "Psoriatic arthritis"),
        ("crohn_disease_GCST004132", "Crohn disease"),
        ("ulcerative_colitis_GCST004133", "Ulcerative colitis"),
        ("coronary_artery_disease_CADMETA_eu", "Coronary artery disease"),
    ]:
        rec = parse_rg(BASE / "ldsc" / f"rg_no_mhc_psoriasis_vs_{trait}.log")
        rec.update({"trait": label, "sensitivity": "explicit_no_MHC"})
        rows.append(rec)
    for trait, label in [
        ("crohn_disease_GCST004132", "Crohn disease"),
        ("ulcerative_colitis_GCST004133", "Ulcerative colitis"),
    ]:
        rec = parse_rg(BASE / "ldsc" / f"rg_signflip_psoriasis_vs_{trait}.log")
        rec.update({"trait": label, "sensitivity": "outcome_Z_sign_flipped"})
        rows.append(rec)

    path = BASE / "phase4b0_ldsc_sensitivity_rg.tsv"
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["trait", "sensitivity", "rg", "se", "z", "p", "cross_trait_intercept", "cross_trait_intercept_se", "log"],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    lines = REPORT.read_text().rstrip().splitlines()
    lines.extend(
        [
            "",
            "## LDSC sensitivity adjudication",
            "",
            "| trait | sensitivity | rg | SE | P | cross-trait intercept |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for r in rows:
        lines.append(
            f"| {r['trait']} | {r['sensitivity']} | {float(r['rg']):.4f} | {float(r['se']):.4f} | "
            f"{float(r['p']):.3g} | {float(r['cross_trait_intercept']):.4f} |"
        )
    lines.extend(
        [
            "",
            "## Final Phase 4B-0 adjudication",
            "",
            "**PsA:** processing direction is PASS, but rg > 1 and cross-trait intercept remains high after explicit no-MHC sensitivity. Adjudication: keep as positive-control / near-neighbor sensitivity only; do not use as an independent multisystem comorbidity signal.",
            "",
            "**CD/UC:** processing direction is PASS and explicit no-MHC sensitivity does not change the negative rg. Forced sign flipping mirrors rg to the same positive magnitude, confirming that LDSC is responding coherently to the signed input. Adjudication: no simple munge or allele-flip bug detected; retain CD/UC as QC-flagged targets. Their global negative rg should be interpreted only after restricted local rg checks for directional heterogeneity.",
            "",
            "**CAD:** processing direction is PASS and no-MHC sensitivity is unchanged. Adjudication: clean primary systemic target for restricted LAVA.",
            "",
            "**Phase 4B restricted LAVA scope:** CAD primary; PsA positive-control / near-neighbor sensitivity; CD and UC QC-flagged local-heterogeneity targets. Stroke and CKD remain null/low-power references and are not included in restricted LAVA main analysis.",
            "",
            f"- LDSC sensitivity table: `{path}`",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
