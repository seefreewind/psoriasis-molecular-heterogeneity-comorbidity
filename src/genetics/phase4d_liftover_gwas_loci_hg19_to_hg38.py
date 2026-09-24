#!/usr/bin/env python3
from pathlib import Path
import gzip

import pandas as pd
from pyliftover import LiftOver


ROOT = Path(__file__).resolve().parents[2]
CHAIN = ROOT / "data" / "genetics" / "reference" / "liftover" / "hg19ToHg38.over.chain.gz"
INDIR = ROOT / "results" / "phase4c_preparation" / "gwas_loci"
OUTDIR = ROOT / "results" / "phase4d_coloc" / "gwas_loci_hg38"
OUTDIR.mkdir(parents=True, exist_ok=True)


def liftover_file(trait: str, lo: LiftOver):
    inp = INDIR / f"{trait}_phase4c_locus_raw.tsv.gz"
    out = OUTDIR / f"{trait}_phase4c_locus_raw.hg38.tsv.gz"
    df = pd.read_csv(inp, sep="\t")
    hg38_chr = []
    hg38_bp = []
    status = []
    for chrom, bp in zip(df["chr"], df["bp"]):
        qchrom = f"chr{chrom}"
        # pyliftover uses zero-based coordinates; convert back to 1-based.
        hits = lo.convert_coordinate(qchrom, int(bp) - 1)
        if len(hits) == 1:
            hchrom, hpos0, strand, score = hits[0]
            hg38_chr.append(hchrom.replace("chr", ""))
            hg38_bp.append(int(hpos0) + 1)
            status.append("PASS")
        elif len(hits) == 0:
            hg38_chr.append("")
            hg38_bp.append("")
            status.append("NO_HIT")
        else:
            hg38_chr.append("")
            hg38_bp.append("")
            status.append("MULTI_HIT")
    df["hg38_chr"] = hg38_chr
    df["hg38_bp"] = hg38_bp
    df["liftover_status"] = status
    df.loc[df["liftover_status"].eq("PASS"), "hg38_chr"] = (
        df.loc[df["liftover_status"].eq("PASS"), "hg38_chr"].astype(str).str.replace(r"\.0$", "", regex=True)
    )
    df.loc[df["liftover_status"].eq("PASS"), "hg38_bp"] = (
        df.loc[df["liftover_status"].eq("PASS"), "hg38_bp"].astype(int).astype(str)
    )
    with gzip.open(out, "wt") as fh:
        df.to_csv(fh, sep="\t", index=False)
    qc = (
        df["liftover_status"]
        .value_counts(dropna=False)
        .rename_axis("liftover_status")
        .reset_index(name="n")
    )
    qc["trait"] = trait
    qc["input_rows"] = len(df)
    qc["output_file"] = str(out)
    return qc


def main():
    lo = LiftOver(str(CHAIN))
    traits = ["psoriasis", "crohn", "uc"]
    qcs = [liftover_file(t, lo) for t in traits]
    qc = pd.concat(qcs, ignore_index=True)
    qc.to_csv(OUTDIR / "phase4d_gwas_liftover_hg19_to_hg38_qc.tsv", sep="\t", index=False)
    print(qc.to_string(index=False))


if __name__ == "__main__":
    main()
