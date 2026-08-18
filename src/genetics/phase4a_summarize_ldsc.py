#!/usr/bin/env python3
"""Summarize Phase 4A LDSC h2 and rg results."""

from __future__ import annotations

import csv
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MUNGE = ROOT / "results" / "phase4a" / "munge"
OUT = ROOT / "results" / "phase4a"
REPORT = ROOT / "reports" / "PHASE4A_LDSC_GENETIC_CORRELATION_REPORT.md"

TRAITS = {
    "psoriatic_arthritis_GCST90243956": ("Psoriatic arthritis", "musculoskeletal_autoimmune"),
    "crohn_disease_GCST004132": ("Crohn disease", "intestinal_autoimmune"),
    "ulcerative_colitis_GCST004133": ("Ulcerative colitis", "intestinal_autoimmune"),
    "coronary_artery_disease_CADMETA_eu": ("Coronary artery disease", "cardiometabolic_vascular"),
    "ischemic_stroke_GCST006910": ("Ischemic stroke", "cardiometabolic_vascular"),
    "chronic_kidney_disease_CKDGen_Wuttke2019": ("Chronic kidney disease", "renal"),
}

BLOCKED = [
    ("Type 2 diabetes", "cardiometabolic_metabolic", "DOWNLOAD_OR_ARCHIVE_FAIL", "Frozen primary DIAMANTE EUR zip request returned a non-extractable/incomplete archive; backup not substituted."),
    ("MASLD", "hepatometabolic", "PRIMARY_FILE_UNRESOLVED", "Frozen primary Ghodsian2021/GCST90091033 source remained contradictory or inaccessible; Namjou GCST008471 remains rejected as primary."),
    ("Major depressive disorder", "neuropsychiatric", "ACCESS_BLOCKED_403", "Frozen primary PGC MDD2 noUKBB/no23andMe Figshare/API access returned 403 or license gating."),
    ("Uveitis", "ocular_inflammatory", "ACCESS_BLOCKED_FORM_REQUIRED", "Frozen primary FinnGen/anterior uveitis source requires access form/email; no backup substituted."),
]


def parse_h2(path: Path) -> dict[str, str]:
    text = path.read_text()
    out: dict[str, str] = {}
    patterns = {
        "h2_obs": r"Total Observed scale h2: ([\-0-9.eE]+) \(([\-0-9.eE]+)\)",
        "mean_chi2": r"Mean Chi\^2: ([\-0-9.eE]+)",
        "lambda_gc": r"Lambda GC: ([\-0-9.eE]+)",
        "intercept": r"Intercept: ([\-0-9.eE]+) \(([\-0-9.eE]+)\)",
    }
    m = re.search(patterns["h2_obs"], text)
    if m:
        out["h2_obs"], out["h2_obs_se"] = m.group(1), m.group(2)
    for key in ["mean_chi2", "lambda_gc"]:
        m = re.search(patterns[key], text)
        if m:
            out[key] = m.group(1)
    intercepts = re.findall(patterns["intercept"], text)
    if intercepts:
        out["h2_intercept"], out["h2_intercept_se"] = intercepts[-1]
    return out


def parse_rg(path: Path) -> dict[str, str]:
    text = path.read_text()
    out: dict[str, str] = {}
    m = re.search(r"Genetic Correlation: ([\-0-9.eE]+) \(([\-0-9.eE]+)\)", text)
    if m:
        out["rg"], out["rg_se"] = m.group(1), m.group(2)
    m = re.search(r"Z-score: ([\-0-9.eE]+)", text)
    if m:
        out["z"] = m.group(1)
    m = re.search(r"\nP: ([\-0-9.eE]+)", text)
    if m:
        out["p"] = m.group(1)
    cov_block = text.split("Genetic Covariance", 1)[-1].split("Genetic Correlation", 1)[0]
    m = re.search(r"Intercept: ([\-0-9.eE]+) \(([\-0-9.eE]+)\)", cov_block)
    if m:
        out["cross_trait_intercept"], out["cross_trait_intercept_se"] = m.group(1), m.group(2)
    return out


def bh_fdr(pvals: list[float]) -> list[float]:
    n = len(pvals)
    order = sorted(range(n), key=lambda i: pvals[i])
    q = [math.nan] * n
    prev = 1.0
    for rank, i in reversed(list(enumerate(order, start=1))):
        val = min(prev, pvals[i] * n / rank)
        q[i] = val
        prev = val
    return q


def qc_status(h2: dict[str, str], rg: dict[str, str], trait: str) -> str:
    h2_val = float(h2.get("h2_obs", "nan"))
    h2_se = float(h2.get("h2_obs_se", "nan"))
    intercept = float(h2.get("h2_intercept", "nan"))
    cross = float(rg.get("cross_trait_intercept", "nan"))
    flags = []
    if h2_val <= 0 or h2_se <= 0 or h2_val / h2_se < 3:
        flags.append("LOW_POWER_H2")
    if intercept > 1.08:
        flags.append("ELEVATED_H2_INTERCEPT")
    if abs(cross) > 0.05:
        flags.append("CROSS_TRAIT_INTERCEPT_ELEVATED")
    if trait == "psoriatic_arthritis_GCST90243956":
        flags.append("NEAR_NEIGHBOR_PHENOTYPE")
    return "PASS" if not flags else ";".join(flags)


def main() -> None:
    rows = []
    pvals = []
    psoriasis_h2 = parse_h2(MUNGE / "psoriasis_GCST90472771.h2.log")
    for trait, (name, system) in TRAITS.items():
        h2 = parse_h2(MUNGE / f"{trait}.h2.log")
        rg = parse_rg(MUNGE / f"rg_psoriasis_vs_{trait}.log")
        p = float(rg["p"])
        pvals.append(p)
        row = {
            "Outcome": name,
            "system": system,
            "rg": rg["rg"],
            "SE": rg["rg_se"],
            "Z": rg["z"],
            "P": rg["p"],
            "FDR": "",
            "h2_psoriasis": psoriasis_h2.get("h2_obs", "NA"),
            "h2_psoriasis_SE": psoriasis_h2.get("h2_obs_se", "NA"),
            "h2_outcome": h2.get("h2_obs", "NA"),
            "h2_outcome_SE": h2.get("h2_obs_se", "NA"),
            "outcome_intercept": h2.get("h2_intercept", "NA"),
            "cross_trait_intercept": rg.get("cross_trait_intercept", "NA"),
            "QC_status": qc_status(h2, rg, trait),
        }
        rows.append(row)

    for row, fdr in zip(rows, bh_fdr(pvals)):
        row["FDR"] = f"{fdr:.6g}"

    table_path = OUT / "phase4a_ldsc_rg_results.tsv"
    with table_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    blocked_path = OUT / "phase4a_blocked_primary_outcomes.tsv"
    with blocked_path.open("w", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerow(["Outcome", "system", "status", "reason"])
        writer.writerows(BLOCKED)

    significant = [r for r in rows if float(r["FDR"]) < 0.05]
    significant_systems = sorted({r["system"] for r in significant})
    if len(significant_systems) >= 3:
        decision = "GO TO PHASE 4B"
    elif len(significant) >= 1:
        decision = "CONDITIONAL GO"
    else:
        decision = "SHRINK"

    md_rows = [
        "| Outcome | system | rg | SE | P | FDR | h2_outcome | cross-trait intercept | QC |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for r in rows:
        md_rows.append(
            f"| {r['Outcome']} | {r['system']} | {float(r['rg']):.4f} | {float(r['SE']):.4f} | "
            f"{float(r['P']):.3g} | {float(r['FDR']):.3g} | {float(r['h2_outcome']):.4f} | "
            f"{float(r['cross_trait_intercept']):.4f} | {r['QC_status']} |"
        )

    blocked_rows = [
        "| Outcome | status | reason |",
        "|---|---|---|",
    ]
    for outcome, _system, status, reason in BLOCKED:
        blocked_rows.append(f"| {outcome} | {status} | {reason} |")

    REPORT.write_text(
        "\n".join(
            [
                "# Phase 4A LDSC genome-wide genetic correlation report",
                "",
                "## Scope lock",
                "",
                "Exposure was frozen as overall psoriasis susceptibility GCST90472771. F1/F2/F6/F7 molecular axes were not used in genetic analyses. Phase 4A stopped at genome-wide LDSC rg; LAVA, coloc, MR, and axis-specific genetics were not run.",
                "",
                "## Download and munge status",
                "",
                "Six frozen primary outcomes were downloaded, harmonized to HapMap3/LDSC-compatible rsIDs, munged, and passed single-trait LDSC estimability. Four frozen primary outcomes were not replaced by backups because primary access or archive integrity failed.",
                "",
                "Blocked frozen primary outcomes:",
                "",
                *blocked_rows,
                "",
                "## LDSC rg results",
                "",
                *md_rows,
                "",
                "## GO decision",
                "",
                f"Decision: **{decision}**.",
                "",
                f"FDR-supported signals were observed in {len(significant)} traits across {len(significant_systems)} system domains: {', '.join(significant_systems) if significant_systems else 'none'}.",
                "",
                "Interpretation boundary: PsA is a near-neighbor phenotype and showed rg > 1 with elevated cross-trait intercept, so it supports strong shared autoimmune architecture but should not be treated as an independent multisystem signal without local/sensitivity analyses. CD and UC showed significant negative rg in this frozen run and need careful source/build/phenotype interpretation before biological storytelling. CAD showed a positive rg. Stroke and CKD were not significant and had low observed-scale h2, so they are low-power or null in Phase 4A.",
                "",
                "## Output files",
                "",
                f"- LDSC rg table: `{table_path}`",
                f"- Blocked primary outcome table: `{blocked_path}`",
                f"- Psoriasis HapMap3 mapping QC: `{OUT / 'munge_inputs' / 'psoriasis_GCST90472771.hm3_mapping_qc.tsv'}`",
                f"- LDSC logs: `{ROOT / 'logs' / 'phase4a' / 'ldsc'}`",
                "",
            ]
        )
    )


if __name__ == "__main__":
    main()
