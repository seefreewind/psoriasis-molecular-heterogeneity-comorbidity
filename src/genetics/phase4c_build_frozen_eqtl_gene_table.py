#!/usr/bin/env python3
"""Build frozen Phase 4C shared-locus eQTL gene table from SMR2 results."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path("/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity")
CANDIDATES = ROOT / "results/phase4c_preparation/phase4c_coloc_candidate_loci.tsv"
SMR2 = ROOT / "results/phase4c_smr/phase4c_smr2_probe2mb_all_results.tsv"
OUTDIR = ROOT / "results/phase4c_smr"
FROZEN = OUTDIR / "phase4c_frozen_shared_locus_eqtl_gene_table.tsv"
SUMMARY = OUTDIR / "phase4c_frozen_shared_locus_eqtl_gene_summary.tsv"


TISSUE_CLASS = {
    "Skin_Sun_Exposed_Lower_leg": "skin",
    "Skin_Not_Sun_Exposed_Suprapubic": "skin",
    "Whole_Blood": "blood_immune",
    "Spleen": "blood_immune",
    "Cells_EBV-transformed_lymphocytes": "blood_immune",
    "Artery_Coronary": "vascular_arterial",
    "Artery_Aorta": "vascular_arterial",
    "Artery_Tibial": "vascular_arterial",
    "Colon_Sigmoid": "intestinal",
    "Colon_Transverse": "intestinal",
}


def unique_join(values: pd.Series) -> str:
    vals = [str(v) for v in values.dropna().unique()]
    return ";".join(sorted(vals))


def sign_label(values: pd.Series) -> str:
    vals = pd.to_numeric(values, errors="coerce").dropna()
    if vals.empty:
        return "unknown"
    signs = set(vals.map(lambda x: "positive" if x > 0 else "negative" if x < 0 else "zero"))
    signs.discard("zero")
    if len(signs) == 1:
        return next(iter(signs))
    return "mixed"


def evidence_tier(row: pd.Series) -> str:
    if row["phase4br_tier"] == "Tier 1" and row["n_tissues"] >= 2:
        return "A_local_Tier1_recurrent_SMR2"
    if row["phase4br_tier"] == "Tier 1" and row["n_tissues"] == 1:
        return "B_local_Tier1_single_tissue_SMR2"
    if row["phase4br_tier"] == "Tier 2" and row["n_tissues"] >= 2:
        return "B_local_Tier2_recurrent_SMR2"
    return "C_local_Tier2_single_tissue_SMR2"


def role_label(outcome: str) -> str:
    return {
        "cad": "primary_systemic_cardiovascular",
        "psa": "positive_control_near_neighbor",
        "crohn": "ibd_direction_heterogeneity",
        "uc": "ibd_direction_heterogeneity",
    }.get(outcome, "secondary")


def main() -> None:
    cand = pd.read_csv(CANDIDATES, sep="\t")
    smr = pd.read_csv(SMR2, sep="\t")
    smr = smr[smr["smr_primary_signal"].astype(bool)].copy()
    smr["tissue_class"] = smr["tissue"].map(TISSUE_CLASS).fillna("other")

    group_cols = ["outcome", "locus", "Gene", "probeID"]
    rows = []
    for key, g in smr.groupby(group_cols, dropna=False):
        best = g.sort_values(["p_SMR", "smr_fdr_global"]).iloc[0]
        locus = cand[(cand["outcome"] == key[0]) & (cand["locus"] == int(key[1]))]
        if locus.empty:
            continue
        loc = locus.iloc[0]
        row = {
            "outcome": key[0],
            "phase4c_role": role_label(key[0]),
            "locus": int(key[1]),
            "chr": int(loc["chr"]),
            "start": int(loc["start"]),
            "stop": int(loc["stop"]),
            "phase4br_tier": loc["phase4br_tier"],
            "local_direction_group": loc["local_direction_group"],
            "rho_ukb": loc["rho_ukb"],
            "p_ukb": loc["p_ukb"],
            "ukb_fdr_within_outcome": loc["ukb_fdr_within_outcome"],
            "eqtl_tissue_priority": loc["eqtl_tissue_priority"],
            "gene": key[2],
            "probeID": key[3],
            "probe_chr": int(best["ProbeChr"]),
            "probe_bp": int(best["Probe_bp"]),
            "n_tissues": g["tissue"].nunique(),
            "tissues": unique_join(g["tissue"]),
            "tissue_classes": unique_join(g["tissue_class"]),
            "top_tissue": best["tissue"],
            "top_tissue_class": best["tissue_class"],
            "top_snp": best["topSNP"],
            "top_snp_chr": best["topSNP_chr"],
            "top_snp_bp": best["topSNP_bp"],
            "min_p_smr": g["p_SMR"].min(),
            "min_smr_fdr_global": g["smr_fdr_global"].min(),
            "min_p_heidi": g["p_HEIDI"].min(skipna=True),
            "n_heidi_tested": g["p_HEIDI"].notna().sum(),
            "all_rows_heidi_pass_0p01": bool(g["heidi_pass_0p01"].all()),
            "b_smr_direction": sign_label(g["b_SMR"]),
            "b_smr_top": best["b_SMR"],
            "se_smr_top": best["se_SMR"],
            "p_smr_top": best["p_SMR"],
            "p_heidi_top": best["p_HEIDI"],
            "nsnp_heidi_top": best["nsnp_HEIDI"],
        }
        rows.append(row)

    out = pd.DataFrame(rows)
    out["phase4c_eqtl_gene_tier"] = out.apply(evidence_tier, axis=1)
    out = out.sort_values(
        [
            "outcome",
            "phase4c_eqtl_gene_tier",
            "phase4br_tier",
            "locus",
            "min_p_smr",
            "gene",
        ]
    )
    out.to_csv(FROZEN, sep="\t", index=False)

    summary = (
        out.groupby(["outcome", "phase4c_role", "phase4br_tier", "local_direction_group"], dropna=False)
        .agg(
            n_loci=("locus", "nunique"),
            n_genes=("gene", "nunique"),
            n_recurrent_genes=("n_tissues", lambda x: int((x >= 2).sum())),
            min_p_smr=("min_p_smr", "min"),
            min_fdr_smr=("min_smr_fdr_global", "min"),
        )
        .reset_index()
        .sort_values(["outcome", "phase4br_tier", "local_direction_group"])
    )
    summary.to_csv(SUMMARY, sep="\t", index=False)

    print(f"Wrote {FROZEN}")
    print(f"Wrote {SUMMARY}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
