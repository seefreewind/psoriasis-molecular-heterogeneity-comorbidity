#!/usr/bin/env python3
"""Prepare outcome-by-tissue probe lists for restricted Phase 4C SMR."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path("/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity")
CANDIDATES = ROOT / "results/phase4c_preparation/phase4c_coloc_candidate_loci.tsv"
BESD_DIR = ROOT / "data/genetics/reference/gtex_v8_smr_besd/extracted"
OUTDIR = ROOT / "results/phase4c_smr/probe_lists"
MANIFEST = ROOT / "results/phase4c_smr/phase4c_smr1_probe_list_manifest.tsv"

OUTCOME_TISSUES = {
    "cad": [
        "Skin_Sun_Exposed_Lower_leg",
        "Skin_Not_Sun_Exposed_Suprapubic",
        "Whole_Blood",
        "Artery_Coronary",
        "Artery_Aorta",
        "Artery_Tibial",
    ],
    "psa": [
        "Skin_Sun_Exposed_Lower_leg",
        "Skin_Not_Sun_Exposed_Suprapubic",
        "Whole_Blood",
        "Spleen",
        "Cells_EBV-transformed_lymphocytes",
    ],
    "crohn": [
        "Skin_Sun_Exposed_Lower_leg",
        "Skin_Not_Sun_Exposed_Suprapubic",
        "Whole_Blood",
        "Colon_Sigmoid",
        "Colon_Transverse",
        "Spleen",
        "Cells_EBV-transformed_lymphocytes",
    ],
    "uc": [
        "Skin_Sun_Exposed_Lower_leg",
        "Skin_Not_Sun_Exposed_Suprapubic",
        "Whole_Blood",
        "Colon_Sigmoid",
        "Colon_Transverse",
        "Spleen",
        "Cells_EBV-transformed_lymphocytes",
    ],
}


def read_epi(tissue: str) -> pd.DataFrame:
    path = BESD_DIR / tissue / f"{tissue}.epi"
    cols = ["chr", "probe", "cm", "pos", "gene", "strand"]
    x = pd.read_csv(path, sep="\t", names=cols, usecols=range(6))
    x["chr"] = pd.to_numeric(x["chr"], errors="coerce").astype("Int64")
    x["pos"] = pd.to_numeric(x["pos"], errors="coerce")
    return x


def probe_hits(epi: pd.DataFrame, loci: pd.DataFrame) -> pd.DataFrame:
    pieces = []
    for row in loci.itertuples(index=False):
        hit = epi.loc[
            (epi["chr"] == int(row.chr))
            & (epi["pos"] >= int(row.start))
            & (epi["pos"] <= int(row.stop))
        ].copy()
        if hit.empty:
            continue
        hit.insert(0, "locus", row.locus)
        hit.insert(1, "locus_start", row.start)
        hit.insert(2, "locus_stop", row.stop)
        pieces.append(hit)
    if not pieces:
        return pd.DataFrame(
            columns=["locus", "locus_start", "locus_stop", "chr", "probe", "cm", "pos", "gene", "strand"]
        )
    return pd.concat(pieces, ignore_index=True).drop_duplicates(["probe"])


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    candidates = pd.read_csv(CANDIDATES, sep="\t")
    rows = []
    epi_cache: dict[str, pd.DataFrame] = {}

    for outcome, tissues in OUTCOME_TISSUES.items():
        loci = candidates.loc[
            candidates["outcome"] == outcome, ["locus", "chr", "start", "stop", "phase4br_tier"]
        ].drop_duplicates()
        for tissue in tissues:
            if tissue not in epi_cache:
                epi_cache[tissue] = read_epi(tissue)
            hits = probe_hits(epi_cache[tissue], loci)
            stem = f"{outcome}__{tissue}"
            tsv = OUTDIR / f"{stem}.probes.tsv"
            txt = OUTDIR / f"{stem}.probe_ids.txt"
            hits.to_csv(tsv, sep="\t", index=False)
            hits["probe"].to_csv(txt, index=False, header=False)
            rows.append(
                {
                    "outcome": outcome,
                    "tissue": tissue,
                    "n_candidate_loci": loci["locus"].nunique(),
                    "n_probes": len(hits),
                    "probe_tsv": str(tsv),
                    "probe_id_file": str(txt),
                    "besd_prefix": str(BESD_DIR / tissue / tissue),
                    "gwas_ma": str(ROOT / f"results/phase4c_smr/gwas_ma/{outcome}.phase4c_loci.ma"),
                }
            )

    pd.DataFrame(rows).to_csv(MANIFEST, sep="\t", index=False)
    print(f"Wrote {MANIFEST}")
    print(pd.DataFrame(rows).groupby("outcome")["n_probes"].sum().to_string())


if __name__ == "__main__":
    main()
