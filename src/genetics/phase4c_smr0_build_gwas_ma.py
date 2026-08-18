#!/usr/bin/env python3
"""Build SMR .ma files from Phase 4C GWAS locus extracts."""

from __future__ import annotations

import gzip
import subprocess
from pathlib import Path

import pandas as pd


ROOT = Path("/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity")
GWAS_DIR = ROOT / "results/phase4c_preparation/gwas_loci"
OUTDIR = ROOT / "results/phase4c_smr/gwas_ma"
LOGDIR = ROOT / "logs/phase4c_smr"
BFILE = ROOT / "data/genetics/reference/ld/g1000_eur/g1000_eur"
PLINK2 = Path("/Users/zy/.local/bin/plink2")

TRAIT_N = {
    "psoriasis": 36466 + 458078,
    "cad": 122733 + 424528,
    "psa": 5065 + 21286,
    "crohn": 12194 + 28072,
    "uc": 12366 + 33609,
}

TRAIT_FILES = {
    "psoriasis": GWAS_DIR / "psoriasis_phase4c_locus_raw.tsv.gz",
    "cad": GWAS_DIR / "cad_phase4c_locus_raw.tsv.gz",
    "psa": GWAS_DIR / "psa_phase4c_locus_raw.tsv.gz",
    "crohn": GWAS_DIR / "crohn_phase4c_locus_raw.tsv.gz",
    "uc": GWAS_DIR / "uc_phase4c_locus_raw.tsv.gz",
}


def read_gwas() -> pd.DataFrame:
    pieces = []
    for trait, path in TRAIT_FILES.items():
        df = pd.read_csv(path, sep="\t", compression="gzip", low_memory=False)
        df["trait"] = trait
        pieces.append(df)
    x = pd.concat(pieces, ignore_index=True)
    x["effect_allele"] = x["effect_allele"].astype(str).str.upper()
    x["other_allele"] = x["other_allele"].astype(str).str.upper()
    x["chr"] = pd.to_numeric(x["chr"], errors="coerce").astype("Int64")
    x["bp"] = pd.to_numeric(x["bp"], errors="coerce").astype("Int64")
    x["beta"] = pd.to_numeric(x["beta"], errors="coerce")
    x["se"] = pd.to_numeric(x["se"], errors="coerce")
    x["p"] = pd.to_numeric(x["p"], errors="coerce")
    x["eaf"] = pd.to_numeric(x["eaf"], errors="coerce")
    x["rsid"] = x["rsid"].replace({"nan": pd.NA, "NaN": pd.NA, "": pd.NA})
    return x


def key(chr_: object, bp: object, a1: str, a2: str) -> tuple[int, int, str, str] | None:
    if pd.isna(chr_) or pd.isna(bp) or not a1 or not a2 or a1 == "NAN" or a2 == "NAN":
        return None
    alleles = tuple(sorted([a1.upper(), a2.upper()]))
    return (int(chr_), int(bp), alleles[0], alleles[1])


def build_needed_keys(gwas: pd.DataFrame) -> set[tuple[int, int, str, str]]:
    out = set()
    for row in gwas.itertuples(index=False):
        k = key(row.chr, row.bp, row.effect_allele, row.other_allele)
        if k is not None:
            out.add(k)
    return out


def scan_bim_for_rsids(needed: set[tuple[int, int, str, str]]) -> pd.DataFrame:
    rows = []
    with open(f"{BFILE}.bim", "rt") as handle:
        for line in handle:
            chrom, rsid, _cm, bp, a1, a2 = line.rstrip("\n").split("\t")[:6]
            k = key(chrom, bp, a1, a2)
            if k in needed:
                rows.append(
                    {
                        "chr": int(chrom),
                        "bp": int(bp),
                        "allele_low": k[2],
                        "allele_high": k[3],
                        "mapped_rsid": rsid,
                        "bim_a1": a1.upper(),
                        "bim_a2": a2.upper(),
                    }
                )
    if not rows:
        return pd.DataFrame(
            columns=["chr", "bp", "allele_low", "allele_high", "mapped_rsid", "bim_a1", "bim_a2"]
        )
    return pd.DataFrame(rows).drop_duplicates(["chr", "bp", "allele_low", "allele_high"])


def add_mapping_keys(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    alleles = df.apply(
        lambda r: sorted([str(r["effect_allele"]).upper(), str(r["other_allele"]).upper()]),
        axis=1,
        result_type="expand",
    )
    df["allele_low"] = alleles[0]
    df["allele_high"] = alleles[1]
    return df


def run_plink_freq(rsids: pd.Series) -> pd.DataFrame:
    snp_file = OUTDIR / "phase4c_smr0_all_rsids.txt"
    rsids.dropna().drop_duplicates().sort_values().to_csv(snp_file, index=False, header=False)
    out_prefix = OUTDIR / "phase4c_smr0_g1000_eur"
    cmd = [
        str(PLINK2),
        "--bfile",
        str(BFILE),
        "--extract",
        str(snp_file),
        "--freq",
        "--out",
        str(out_prefix),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    afreq = pd.read_csv(f"{out_prefix}.afreq", sep=r"\s+", engine="python")
    afreq = afreq.rename(
        columns={
            "#CHROM": "chr_freq",
            "ID": "SNP",
            "REF": "ref",
            "ALT": "alt",
            "ALT_FREQS": "alt_freq",
        }
    )
    afreq["alt_freq"] = pd.to_numeric(afreq["alt_freq"], errors="coerce")
    afreq["ref"] = afreq["ref"].astype(str).str.upper()
    afreq["alt"] = afreq["alt"].astype(str).str.upper()
    return afreq[["SNP", "ref", "alt", "alt_freq"]]


def allele_frequency_for_a1(row: pd.Series) -> float | None:
    a1 = str(row["A1"]).upper()
    if pd.notna(row.get("eaf")):
        return float(row["eaf"])
    if pd.isna(row.get("alt_freq")):
        return None
    if a1 == str(row.get("alt")).upper():
        return float(row["alt_freq"])
    if a1 == str(row.get("ref")).upper():
        return float(1.0 - row["alt_freq"])
    return None


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    LOGDIR.mkdir(parents=True, exist_ok=True)
    gwas = read_gwas()
    needed = build_needed_keys(gwas)
    bim_map = scan_bim_for_rsids(needed)
    bim_map.to_csv(OUTDIR / "phase4c_smr0_bim_rsid_map.tsv", sep="\t", index=False)

    x = add_mapping_keys(gwas)
    x = x.merge(bim_map, on=["chr", "bp", "allele_low", "allele_high"], how="left")
    x["SNP"] = x["rsid"].where(x["rsid"].notna(), x["mapped_rsid"])
    x["A1"] = x["effect_allele"]
    x["A2"] = x["other_allele"]
    x["b"] = x["beta"]
    x["N"] = x["trait"].map(TRAIT_N)

    freq = run_plink_freq(x["SNP"])
    x = x.merge(freq, on="SNP", how="left")
    x["freq"] = x.apply(allele_frequency_for_a1, axis=1)

    manifest_rows = []
    for trait, sub in x.groupby("trait"):
        before = len(sub)
        ma = sub.dropna(subset=["SNP", "A1", "A2", "b", "se", "p", "N"]).copy()
        ma = ma.drop_duplicates("SNP")
        ma["freq"] = ma["freq"].where(ma["freq"].notna(), "NA")
        outfile = OUTDIR / f"{trait}.phase4c_loci.ma"
        ma[["SNP", "A1", "A2", "freq", "b", "se", "p", "N"]].to_csv(
            outfile, sep="\t", index=False
        )
        manifest_rows.append(
            {
                "trait": trait,
                "input_rows": before,
                "ma_rows": len(ma),
                "rows_with_rsid": int(sub["SNP"].notna().sum()),
                "rows_with_freq": int(pd.to_numeric(sub["freq"], errors="coerce").notna().sum()),
                "missing_rsid_rows": int(sub["SNP"].isna().sum()),
                "output_file": str(outfile),
            }
        )

    pd.DataFrame(manifest_rows).sort_values("trait").to_csv(
        OUTDIR / "phase4c_smr0_gwas_ma_manifest.tsv", sep="\t", index=False
    )
    print(pd.DataFrame(manifest_rows).sort_values("trait").to_string(index=False))


if __name__ == "__main__":
    main()
