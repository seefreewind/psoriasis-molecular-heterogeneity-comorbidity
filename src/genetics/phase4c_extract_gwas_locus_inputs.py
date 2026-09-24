#!/usr/bin/env python3
"""Extract raw GWAS locus-level inputs for Phase 4C coloc."""

from __future__ import annotations

import gzip
from pathlib import Path
from typing import Callable

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
CANDIDATES = ROOT / "results/phase4c_preparation/phase4c_coloc_candidate_loci.tsv"
OUTDIR = ROOT / "results/phase4c_preparation/gwas_loci"
MANIFEST = ROOT / "results/phase4c_preparation/phase4c_gwas_locus_input_manifest.tsv"
LEADS = ROOT / "results/phase4c_preparation/phase4c_gwas_locus_lead_variants.tsv"


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
            "marker": pd.NA,
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
            "marker": df["MarkerName"].astype(str),
        }
    )


def parse_marker_chr_bp(marker: pd.Series) -> pd.DataFrame:
    parts = marker.astype(str).str.split(":", n=1, expand=True)
    chr_col = pd.to_numeric(parts[0], errors="coerce")
    bp_col = pd.to_numeric(parts[1].str.split("_", n=1, expand=True)[0], errors="coerce")
    return pd.DataFrame({"chr": chr_col, "bp": bp_col})


def standardize_ibd(df: pd.DataFrame) -> pd.DataFrame:
    pos = parse_marker_chr_bp(df["MarkerName"])
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
            "marker": df["MarkerName"].astype(str),
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
            "marker": df["variant_id"].astype(str),
        }
    )


STANDARDIZERS: dict[str, Callable[[pd.DataFrame], pd.DataFrame]] = {
    "psoriasis": standardize_psoriasis,
    "cad": standardize_cad,
    "psa": standardize_psa,
    "crohn": standardize_ibd,
    "uc": standardize_ibd,
}


def open_output(path: Path):
    return gzip.open(path, "wt")


def intervals_for_trait(candidates: pd.DataFrame, trait: str) -> pd.DataFrame:
    if trait == "psoriasis":
        intervals = candidates[["locus", "chr", "start", "stop"]].drop_duplicates()
    else:
        intervals = candidates.loc[
            candidates["outcome"] == trait, ["locus", "chr", "start", "stop"]
        ].drop_duplicates()
    return intervals.sort_values(["chr", "start", "stop", "locus"]).reset_index(drop=True)


def assign_loci(std: pd.DataFrame, intervals: pd.DataFrame) -> pd.DataFrame:
    pieces = []
    std = std.dropna(subset=["chr", "bp"]).copy()
    std["chr"] = std["chr"].astype(int)
    std["bp"] = std["bp"].astype(int)
    for chrom, loci in intervals.groupby("chr"):
        chrom_rows = std.loc[std["chr"] == int(chrom)]
        if chrom_rows.empty:
            continue
        for row in loci.itertuples(index=False):
            hit = chrom_rows.loc[(chrom_rows["bp"] >= row.start) & (chrom_rows["bp"] <= row.stop)].copy()
            if hit.empty:
                continue
            hit.insert(0, "locus", row.locus)
            hit.insert(1, "locus_start", row.start)
            hit.insert(2, "locus_stop", row.stop)
            pieces.append(hit)
    if not pieces:
        return pd.DataFrame()
    out = pd.concat(pieces, ignore_index=True)
    out["variant_key"] = (
        out["chr"].astype(str)
        + ":"
        + out["bp"].astype(str)
        + ":"
        + out["effect_allele"].astype(str)
        + ":"
        + out["other_allele"].astype(str)
    )
    out["z"] = out["beta"] / out["se"]
    return out


def read_chunks(path: Path, chunksize: int = 500_000):
    compression = "gzip" if path.suffix == ".gz" else None
    return pd.read_csv(path, sep="\t", compression=compression, chunksize=chunksize, low_memory=False)


def extract_trait(trait: str, candidates: pd.DataFrame) -> tuple[Path, pd.DataFrame]:
    intervals = intervals_for_trait(candidates, trait)
    outfile = OUTDIR / f"{trait}_phase4c_locus_raw.tsv.gz"
    first = True
    n_rows = 0
    lead_rows = []

    with open_output(outfile) as handle:
        for chunk in read_chunks(TRAIT_FILES[trait]):
            std = STANDARDIZERS[trait](chunk)
            assigned = assign_loci(std, intervals)
            if assigned.empty:
                continue
            assigned.insert(0, "trait", trait)
            assigned.to_csv(handle, sep="\t", index=False, header=first)
            first = False
            n_rows += len(assigned)

            tmp = assigned.dropna(subset=["p"]).copy()
            if not tmp.empty:
                idx = tmp.groupby("locus")["p"].idxmin()
                lead_rows.append(tmp.loc[idx])

    if lead_rows:
        leads = pd.concat(lead_rows, ignore_index=True)
        leads = leads.sort_values(["locus", "p"]).groupby("locus", as_index=False).first()
    else:
        leads = pd.DataFrame()

    manifest = pd.DataFrame(
        [
            {
                "trait": trait,
                "source_file": str(TRAIT_FILES[trait]),
                "output_file": str(outfile),
                "n_candidate_loci": intervals["locus"].nunique(),
                "n_extracted_rows": n_rows,
                "n_loci_with_any_variant": leads["locus"].nunique() if not leads.empty else 0,
            }
        ]
    )
    return outfile, manifest.join(pd.DataFrame())


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    candidates = pd.read_csv(CANDIDATES, sep="\t")

    manifests = []
    all_leads = []
    for trait in ["psoriasis", "cad", "psa", "crohn", "uc"]:
        _, manifest = extract_trait(trait, candidates)
        manifests.append(manifest)

        locus_file = OUTDIR / f"{trait}_phase4c_locus_raw.tsv.gz"
        if locus_file.exists() and locus_file.stat().st_size > 40:
            extracted = pd.read_csv(locus_file, sep="\t", compression="gzip")
            extracted = extracted.dropna(subset=["p"]).copy()
            if not extracted.empty:
                idx = extracted.groupby("locus")["p"].idxmin()
                leads = extracted.loc[idx].copy()
                all_leads.append(
                    leads[
                        [
                            "trait",
                            "locus",
                            "chr",
                            "bp",
                            "effect_allele",
                            "other_allele",
                            "beta",
                            "se",
                            "p",
                            "eaf",
                            "rsid",
                            "marker",
                            "variant_key",
                        ]
                    ]
                )

    pd.concat(manifests, ignore_index=True).to_csv(MANIFEST, sep="\t", index=False)
    if all_leads:
        pd.concat(all_leads, ignore_index=True).sort_values(["trait", "locus"]).to_csv(
            LEADS, sep="\t", index=False
        )
    print(f"Wrote {MANIFEST}")
    print(f"Wrote {LEADS}")


if __name__ == "__main__":
    main()
