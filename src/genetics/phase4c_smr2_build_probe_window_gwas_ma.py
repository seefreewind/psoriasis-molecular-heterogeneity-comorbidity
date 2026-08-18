#!/usr/bin/env python3
"""Build probe +/-2 Mb GWAS .ma files for stricter Phase 4C SMR sensitivity."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pandas as pd


ROOT = Path("/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity")
PROBE_MANIFEST = ROOT / "results/phase4c_smr/phase4c_smr1_probe_list_manifest.tsv"
OUTDIR = ROOT / "results/phase4c_smr/gwas_ma_probe2mb"
MANIFEST = OUTDIR / "phase4c_smr2_probe2mb_gwas_ma_manifest.tsv"
INTERVALS_OUT = OUTDIR / "phase4c_smr2_probe2mb_intervals.tsv"
BFILE = ROOT / "data/genetics/reference/ld/g1000_eur/g1000_eur"
PLINK2 = Path("/Users/zy/.local/bin/plink2")
WINDOW = 2_000_000

TRAIT_N = {
    "psoriasis": 36466 + 458078,
    "cad": 122733 + 424528,
    "psa": 5065 + 21286,
    "crohn": 12194 + 28072,
    "uc": 12366 + 33609,
}

TRAIT_FILES = {
    "psoriasis": ROOT / "data/genetics/psoriasis_GCST90472771/GCST90472771.tsv.gz",
    "cad": ROOT / "data/genetics/phase4a_raw/coronary_artery_disease_CADMETA_eu/CAD_META.gz",
    "psa": ROOT / "data/genetics/phase4a_raw/psoriatic_arthritis_GCST90243956/GCST90243956.tsv",
    "crohn": ROOT / "data/genetics/phase4a_raw/crohn_disease_GCST004132/cd_build37_40266_20161107.txt.gz",
    "uc": ROOT / "data/genetics/phase4a_raw/ulcerative_colitis_GCST004133/uc_build37_45975_20161107.txt.gz",
}


def standardize_psoriasis(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "chr": pd.to_numeric(df["chromosome"], errors="coerce"),
            "bp": pd.to_numeric(df["base_pair_location"], errors="coerce"),
            "effect_allele": df["effect_allele"].astype(str).str.upper(),
            "other_allele": df["other_allele"].astype(str).str.upper(),
            "beta": pd.to_numeric(df["beta"], errors="coerce"),
            "se": pd.to_numeric(df["standard_error"], errors="coerce"),
            "p": pd.to_numeric(df["p_value"], errors="coerce"),
            "eaf": pd.NA,
            "rsid": pd.NA,
        }
    )


def standardize_cad(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "chr": pd.to_numeric(df["CHR"], errors="coerce"),
            "bp": pd.to_numeric(df["BP"], errors="coerce"),
            "effect_allele": df["Allele1"].astype(str).str.upper(),
            "other_allele": df["Allele2"].astype(str).str.upper(),
            "beta": pd.to_numeric(df["Effect"], errors="coerce"),
            "se": pd.to_numeric(df["StdErr"], errors="coerce"),
            "p": pd.to_numeric(df["P-value"], errors="coerce"),
            "eaf": pd.to_numeric(df["Freq1"], errors="coerce"),
            "rsid": df["oldID"].astype(str),
        }
    )


def parse_marker(marker: pd.Series) -> pd.DataFrame:
    parts = marker.astype(str).str.split(":", n=1, expand=True)
    return pd.DataFrame(
        {
            "chr": pd.to_numeric(parts[0], errors="coerce"),
            "bp": pd.to_numeric(parts[1].str.split("_", n=1, expand=True)[0], errors="coerce"),
        }
    )


def standardize_ibd(df: pd.DataFrame) -> pd.DataFrame:
    pos = parse_marker(df["MarkerName"])
    return pd.DataFrame(
        {
            "chr": pos["chr"],
            "bp": pos["bp"],
            "effect_allele": df["Allele1"].astype(str).str.upper(),
            "other_allele": df["Allele2"].astype(str).str.upper(),
            "beta": pd.to_numeric(df["Effect"], errors="coerce"),
            "se": pd.to_numeric(df["StdErr"], errors="coerce"),
            "p": pd.to_numeric(df["P.value"], errors="coerce"),
            "eaf": pd.NA,
            "rsid": pd.NA,
        }
    )


def standardize_psa(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "chr": pd.to_numeric(df["chromosome"], errors="coerce"),
            "bp": pd.to_numeric(df["base_pair_location"], errors="coerce"),
            "effect_allele": df["effect_allele"].astype(str).str.upper(),
            "other_allele": df["other_allele"].astype(str).str.upper(),
            "beta": pd.to_numeric(df["beta"], errors="coerce"),
            "se": pd.to_numeric(df["standard_error"], errors="coerce"),
            "p": pd.to_numeric(df["p_value"], errors="coerce"),
            "eaf": pd.to_numeric(df["effect_allele_frequency"], errors="coerce"),
            "rsid": df["rs_id"].astype(str),
        }
    )


STANDARDIZERS = {
    "psoriasis": standardize_psoriasis,
    "cad": standardize_cad,
    "psa": standardize_psa,
    "crohn": standardize_ibd,
    "uc": standardize_ibd,
}


def merge_intervals(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for chrom, sub in df.sort_values(["chr", "start"]).groupby("chr"):
        cur_start = None
        cur_stop = None
        n_probes = 0
        for row in sub.itertuples(index=False):
            if cur_start is None:
                cur_start, cur_stop, n_probes = int(row.start), int(row.stop), int(row.n_probes)
            elif int(row.start) <= cur_stop + 1:
                cur_stop = max(cur_stop, int(row.stop))
                n_probes += int(row.n_probes)
            else:
                rows.append({"chr": int(chrom), "start": cur_start, "stop": cur_stop, "n_probes": n_probes})
                cur_start, cur_stop, n_probes = int(row.start), int(row.stop), int(row.n_probes)
        if cur_start is not None:
            rows.append({"chr": int(chrom), "start": cur_start, "stop": cur_stop, "n_probes": n_probes})
    return pd.DataFrame(rows)


def build_intervals() -> pd.DataFrame:
    manifest = pd.read_csv(PROBE_MANIFEST, sep="\t")
    rows = []
    for outcome, sub in manifest.groupby("outcome"):
        probes = []
        for path in sub["probe_tsv"].drop_duplicates():
            x = pd.read_csv(path, sep="\t")
            probes.append(x[["chr", "probe", "pos"]])
        p = pd.concat(probes, ignore_index=True).drop_duplicates(["probe", "chr", "pos"])
        p = p.dropna(subset=["chr", "pos"])
        p["chr"] = p["chr"].astype(int)
        p["start"] = (p["pos"].astype(int) - WINDOW).clip(lower=1)
        p["stop"] = p["pos"].astype(int) + WINDOW
        raw = (
            p.groupby(["chr", "start", "stop"], as_index=False)
            .agg(n_probes=("probe", "nunique"))
            .sort_values(["chr", "start"])
        )
        merged = merge_intervals(raw)
        merged.insert(0, "trait", outcome)
        rows.append(merged)
    all_intervals = pd.concat(rows, ignore_index=True)

    # Psoriasis is included for future shared-gene cross-checks, using the union of all outcome windows.
    psoriasis = (
        all_intervals[["chr", "start", "stop", "n_probes"]]
        .groupby(["chr", "start", "stop"], as_index=False)
        .agg(n_probes=("n_probes", "sum"))
    )
    psoriasis = merge_intervals(psoriasis)
    psoriasis.insert(0, "trait", "psoriasis")
    all_intervals = pd.concat([all_intervals, psoriasis], ignore_index=True)
    all_intervals.to_csv(INTERVALS_OUT, sep="\t", index=False)
    return all_intervals


def assign_intervals(std: pd.DataFrame, intervals: pd.DataFrame) -> pd.DataFrame:
    std = std.dropna(subset=["chr", "bp"]).copy()
    if std.empty:
        return std
    std["chr"] = std["chr"].astype(int)
    std["bp"] = std["bp"].astype(int)
    pieces = []
    for chrom, ints in intervals.groupby("chr"):
        chrom_rows = std.loc[std["chr"] == int(chrom)]
        if chrom_rows.empty:
            continue
        mask = pd.Series(False, index=chrom_rows.index)
        for row in ints.itertuples(index=False):
            mask |= (chrom_rows["bp"] >= int(row.start)) & (chrom_rows["bp"] <= int(row.stop))
        if mask.any():
            pieces.append(chrom_rows.loc[mask])
    return pd.concat(pieces, ignore_index=True) if pieces else pd.DataFrame()


def read_chunks(path: Path, chunksize: int = 500_000):
    compression = "gzip" if path.suffix == ".gz" else None
    return pd.read_csv(path, sep="\t", compression=compression, chunksize=chunksize, low_memory=False)


def key(chr_: object, bp: object, a1: str, a2: str):
    if pd.isna(chr_) or pd.isna(bp) or not a1 or not a2:
        return None
    alleles = sorted([str(a1).upper(), str(a2).upper()])
    if "NAN" in alleles:
        return None
    return int(chr_), int(bp), alleles[0], alleles[1]


def add_mapping_cols(df: pd.DataFrame) -> pd.DataFrame:
    alleles = df.apply(
        lambda r: sorted([str(r["effect_allele"]).upper(), str(r["other_allele"]).upper()]),
        axis=1,
        result_type="expand",
    )
    df = df.copy()
    df["allele_low"] = alleles[0]
    df["allele_high"] = alleles[1]
    return df


def scan_bim(needed: set[tuple[int, int, str, str]]) -> pd.DataFrame:
    rows = []
    with open(f"{BFILE}.bim", "rt") as handle:
        for line in handle:
            chrom, rsid, _cm, bp, a1, a2 = line.rstrip("\n").split("\t")[:6]
            k = key(chrom, bp, a1, a2)
            if k in needed:
                rows.append({"chr": k[0], "bp": k[1], "allele_low": k[2], "allele_high": k[3], "mapped_rsid": rsid})
    return pd.DataFrame(rows).drop_duplicates(["chr", "bp", "allele_low", "allele_high"])


def run_plink_freq(rsids: pd.Series) -> pd.DataFrame:
    snp_file = OUTDIR / "phase4c_smr2_probe2mb_all_rsids.txt"
    rsids.dropna().drop_duplicates().sort_values().to_csv(snp_file, index=False, header=False)
    out_prefix = OUTDIR / "phase4c_smr2_probe2mb_g1000_eur"
    subprocess.run(
        [
            str(PLINK2),
            "--bfile",
            str(BFILE),
            "--extract",
            str(snp_file),
            "--freq",
            "--out",
            str(out_prefix),
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    x = pd.read_csv(f"{out_prefix}.afreq", sep=r"\s+", engine="python")
    x = x.rename(columns={"ID": "SNP", "REF": "ref", "ALT": "alt", "ALT_FREQS": "alt_freq"})
    x["ref"] = x["ref"].astype(str).str.upper()
    x["alt"] = x["alt"].astype(str).str.upper()
    x["alt_freq"] = pd.to_numeric(x["alt_freq"], errors="coerce")
    return x[["SNP", "ref", "alt", "alt_freq"]]


def freq_for_a1(row: pd.Series):
    if pd.notna(row.get("eaf")):
        return float(row["eaf"])
    if pd.isna(row.get("alt_freq")):
        return None
    a1 = str(row["A1"]).upper()
    if a1 == str(row.get("alt")).upper():
        return float(row["alt_freq"])
    if a1 == str(row.get("ref")).upper():
        return float(1 - row["alt_freq"])
    return None


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    intervals = build_intervals()
    extracted = []
    manifest_rows = []

    for trait, path in TRAIT_FILES.items():
        trait_intervals = intervals.loc[intervals["trait"] == trait, ["chr", "start", "stop"]]
        pieces = []
        for chunk in read_chunks(path):
            std = STANDARDIZERS[trait](chunk)
            hit = assign_intervals(std, trait_intervals)
            if not hit.empty:
                pieces.append(hit)
        gwas = pd.concat(pieces, ignore_index=True) if pieces else pd.DataFrame()
        gwas["trait"] = trait
        extracted.append(gwas)
        manifest_rows.append({"trait": trait, "probe2mb_raw_rows": len(gwas), "n_intervals": len(trait_intervals)})

    all_gwas = pd.concat(extracted, ignore_index=True)
    all_gwas["rsid"] = all_gwas["rsid"].replace({"nan": pd.NA, "NaN": pd.NA, "": pd.NA})
    needed = set()
    for row in all_gwas.itertuples(index=False):
        k = key(row.chr, row.bp, row.effect_allele, row.other_allele)
        if k is not None:
            needed.add(k)
    bim_map = scan_bim(needed)
    bim_map.to_csv(OUTDIR / "phase4c_smr2_probe2mb_bim_rsid_map.tsv", sep="\t", index=False)

    x = add_mapping_cols(all_gwas)
    x = x.merge(bim_map, on=["chr", "bp", "allele_low", "allele_high"], how="left")
    x["SNP"] = x["rsid"].where(x["rsid"].notna(), x["mapped_rsid"])
    freq = run_plink_freq(x["SNP"])
    x = x.merge(freq, on="SNP", how="left")
    x["A1"] = x["effect_allele"]
    x["A2"] = x["other_allele"]
    x["b"] = x["beta"]
    x["N"] = x["trait"].map(TRAIT_N)
    x["freq"] = x.apply(freq_for_a1, axis=1)

    final_rows = []
    for trait, sub in x.groupby("trait"):
        ma = sub.dropna(subset=["SNP", "A1", "A2", "b", "se", "p", "N"]).drop_duplicates("SNP").copy()
        ma["freq"] = ma["freq"].where(ma["freq"].notna(), "NA")
        outfile = OUTDIR / f"{trait}.phase4c_probe2mb.ma"
        ma[["SNP", "A1", "A2", "freq", "b", "se", "p", "N"]].to_csv(outfile, sep="\t", index=False)
        raw_rows = next(r["probe2mb_raw_rows"] for r in manifest_rows if r["trait"] == trait)
        n_intervals = next(r["n_intervals"] for r in manifest_rows if r["trait"] == trait)
        final_rows.append(
            {
                "trait": trait,
                "n_intervals": n_intervals,
                "probe2mb_raw_rows": raw_rows,
                "ma_rows": len(ma),
                "rows_with_rsid": int(sub["SNP"].notna().sum()),
                "rows_with_freq": int(pd.to_numeric(sub["freq"], errors="coerce").notna().sum()),
                "missing_rsid_rows": int(sub["SNP"].isna().sum()),
                "output_file": str(outfile),
            }
        )
    pd.DataFrame(final_rows).sort_values("trait").to_csv(MANIFEST, sep="\t", index=False)
    print(pd.DataFrame(final_rows).sort_values("trait").to_string(index=False))


if __name__ == "__main__":
    main()
