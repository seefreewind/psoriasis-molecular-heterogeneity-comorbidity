#!/usr/bin/env python3
"""Prepare restricted Phase 4B LAVA input files."""

from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "phase4b_lava"
MUNGE = ROOT / "results" / "phase4a" / "munge"

PHENOS = [
    ("psoriasis", "36466", "458078", "psoriasis_GCST90472771.sumstats.gz"),
    ("psa", "5065", "21286", "psoriatic_arthritis_GCST90243956.sumstats.gz"),
    ("crohn", "12194", "28072", "crohn_disease_GCST004132.sumstats.gz"),
    ("uc", "12366", "33609", "ulcerative_colitis_GCST004133.sumstats.gz"),
    ("cad", "122733", "424528", "coronary_artery_disease_CADMETA_eu.sumstats.gz"),
]

# LDSC cross-trait intercept approximation from Phase 4A logs.
OVERLAP = {
    ("psoriasis", "psa"): 0.3142,
    ("psoriasis", "crohn"): -0.0636,
    ("psoriasis", "uc"): -0.0625,
    ("psoriasis", "cad"): 0.0189,
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sumstats_dir = OUT / "sumstats"
    sumstats_dir.mkdir(exist_ok=True)
    for _phen, _cases, _controls, filename in PHENOS:
        src = MUNGE / filename
        dst = sumstats_dir / filename
        if not dst.exists() or dst.stat().st_size != src.stat().st_size:
            shutil.copy2(src, dst)

    info_path = OUT / "input.info.tsv"
    with info_path.open("w", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerow(["phenotype", "cases", "controls", "filename"])
        for row in PHENOS:
            writer.writerow(row)

    names = [p[0] for p in PHENOS]
    overlap_path = OUT / "sample.overlap.tsv"
    with overlap_path.open("w", newline="") as fh:
        writer = csv.writer(fh, delimiter=" ")
        writer.writerow([""] + names)
        for a in names:
            row = [a]
            for b in names:
                if a == b:
                    row.append("1")
                else:
                    row.append(str(OVERLAP.get((a, b), OVERLAP.get((b, a), 0))))
            writer.writerow(row)

    locus_src = ROOT / "tools" / "phase4b_lava" / "LAVA-main" / "support_data" / "blocks_s2500_m25_f1_w200.GRCh37_hg19.locfile"
    locus_dst = OUT / "blocks_s2500_m25_f1_w200.GRCh37_hg19.locfile"
    if not locus_dst.exists() or locus_dst.stat().st_size != locus_src.stat().st_size:
        shutil.copy2(locus_src, locus_dst)

    manifest = OUT / "phase4b_lava_input_manifest.tsv"
    with manifest.open("w", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerow(["key", "value"])
        writer.writerow(["input_info", str(info_path)])
        writer.writerow(["sample_overlap", str(overlap_path)])
        writer.writerow(["sumstats_dir", str(sumstats_dir)])
        writer.writerow(["locus_file", str(locus_dst)])
        writer.writerow(["plink_reference_prefix", str(ROOT / "data" / "genetics" / "reference" / "magma" / "g1000_eur" / "g1000_eur")])
        writer.writerow(["reference_limitation", "1000G_EUR_PLINK_used; LAVA_0.1.5_recommends_UKB_binary_reference_for_final_EUR_analysis"])


if __name__ == "__main__":
    main()
