#!/usr/bin/env python3
from pathlib import Path
import tarfile

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
OUTDIR = ROOT / "results" / "phase4d_coloc"
OUTDIR.mkdir(parents=True, exist_ok=True)

FROZEN = ROOT / "results" / "phase4c_smr" / "phase4c_frozen_shared_locus_eqtl_gene_table.tsv"
CANDIDATE_LOCI = ROOT / "results" / "phase4c_preparation" / "phase4c_coloc_candidate_loci.tsv"
EQTL_AUDIT = ROOT / "results" / "phase4c_preparation" / "phase4c_eqtl_source_audit.tsv"
BESD_AUDIT = ROOT / "results" / "phase4c_preparation" / "phase4c_gtex_v8_smr_besd_audit.tsv"
GTEX_SIG_TAR = ROOT / "data" / "genetics" / "reference" / "gtex_v8_eqtl_significant" / "raw" / "GTEx_Analysis_v8_eQTL.tar"
GWAS_LOCI = ROOT / "results" / "phase4c_preparation" / "gwas_loci"
EQTL_CATALOGUE_IMPORTED = OUTDIR / "tabix_ftp_paths_imported.tsv"


def split_semicolon(value):
    if pd.isna(value) or not str(value).strip():
        return []
    return [x.strip() for x in str(value).split(";") if x.strip()]


def tar_members(path):
    if not path.exists():
        return []
    try:
        with tarfile.open(path, "r") as tf:
            return tf.getnames()
    except tarfile.TarError:
        return []


def main():
    frozen = pd.read_csv(FROZEN, sep="\t")
    loci = pd.read_csv(CANDIDATE_LOCI, sep="\t")
    eqtl_audit = pd.read_csv(EQTL_AUDIT, sep="\t")
    besd_audit = pd.read_csv(BESD_AUDIT, sep="\t")
    if EQTL_CATALOGUE_IMPORTED.exists():
        imported = pd.read_csv(EQTL_CATALOGUE_IMPORTED, sep="\t")
        imported_paths = dict(zip(imported["qtl_group"], imported["ftp_path"]))
    else:
        imported_paths = {}

    rows = []
    for _, row in frozen.iterrows():
        for tissue in split_semicolon(row["tissues"]):
            besd = besd_audit.loc[besd_audit["tissue"].eq(tissue)]
            if besd.empty:
                besd_status = "NOT_FOUND"
                smr_usable = False
            else:
                besd_status = str(besd.iloc[0]["zip_status"])
                smr_usable = bool(besd.iloc[0]["smr_usable"])
            eqtl_catalogue_path = imported_paths.get(tissue, "")
            eqtl_catalogue_available = bool(eqtl_catalogue_path)
            input_status = (
                "FEASIBLE_VIA_EQTL_CATALOGUE_REMOTE_TABIX"
                if eqtl_catalogue_available
                else "BLOCKED_BY_EQTL_INPUT"
            )
            blocking_reason = (
                "Local GTEx Portal all-associations files are unavailable, but eQTL Catalogue "
                "imported GTEx v8 tabix files provide complete regional per-variant eQTL "
                "statistics suitable for coloc extraction. Proceed with remote-tabix smoke test "
                "and then restricted coloc."
                if eqtl_catalogue_available
                else (
                    "No local complete per-variant eQTL association matrix with beta/slope, SE, "
                    "allele frequency, variant ID, and sample size for every SNP in the locus. "
                    "SMR BESD is usable for SMR/HEIDI but not directly accepted as coloc input; "
                    "significant-only eQTL files are insufficient because coloc needs null and "
                    "non-significant variants."
                )
            )
            rows.append(
                {
                    "outcome": row["outcome"],
                    "phase4c_role": row["phase4c_role"],
                    "locus": row["locus"],
                    "chr": row["chr"],
                    "start": row["start"],
                    "stop": row["stop"],
                    "phase4br_tier": row["phase4br_tier"],
                    "local_direction_group": row["local_direction_group"],
                    "gene": row["gene"],
                    "probeID": row["probeID"],
                    "tissue": tissue,
                    "phase4c_eqtl_gene_tier": row["phase4c_eqtl_gene_tier"],
                    "besd_status": besd_status,
                    "smr_usable": smr_usable,
                    "gwas_locus_sumstats_ready": True,
                    "significant_eqtl_only_ready": False,
                    "full_eqtl_allpairs_ready": False,
                    "eqtl_catalogue_imported_gtex_path": eqtl_catalogue_path,
                    "eqtl_catalogue_remote_tabix_available": eqtl_catalogue_available,
                    "formal_coloc_input_status": input_status,
                    "coloc_ready": False,
                    "blocking_reason": blocking_reason,
                }
            )

    long = pd.DataFrame(rows)
    long.to_csv(OUTDIR / "phase4d_coloc_input_feasibility_by_candidate_tissue.tsv", sep="\t", index=False)

    summary = (
        long.groupby(["outcome", "phase4c_role", "phase4c_eqtl_gene_tier"], dropna=False)
        .agg(
            n_gene_tissue_rows=("gene", "size"),
            n_genes=("gene", "nunique"),
            n_loci=("locus", "nunique"),
            n_tissues=("tissue", "nunique"),
            n_smr_usable_rows=("smr_usable", "sum"),
            n_eqtl_catalogue_remote_tabix_rows=("eqtl_catalogue_remote_tabix_available", "sum"),
            n_coloc_ready_rows=("coloc_ready", "sum"),
        )
        .reset_index()
    )
    summary["coloc_feasibility_status"] = summary.apply(
        lambda r: "FEASIBLE_VIA_EQTL_CATALOGUE_REMOTE_TABIX"
        if r["n_eqtl_catalogue_remote_tabix_rows"] == r["n_gene_tissue_rows"]
        else "PARTIAL_OR_BLOCKED_EQTL_INPUT",
        axis=1,
    )
    summary.to_csv(OUTDIR / "phase4d_coloc_input_feasibility_summary.tsv", sep="\t", index=False)

    members = tar_members(GTEX_SIG_TAR)
    tar_status = pd.DataFrame(
        [
            {
                "resource": "GTEx_Analysis_v8_eQTL.tar",
                "path": str(GTEX_SIG_TAR),
                "exists": GTEX_SIG_TAR.exists(),
                "size_bytes": GTEX_SIG_TAR.stat().st_size if GTEX_SIG_TAR.exists() else 0,
                "tar_member_count": len(members),
                "contains_only_adipose_subcutaneous_members": all(
                    m.startswith("GTEx_Analysis_v8_eQTL/Adipose_Subcutaneous") for m in members
                )
                if members
                else False,
                "interpretation": (
                    "Partial/incomplete for Phase 4D. Current tar contains only "
                    "Adipose_Subcutaneous eGenes and significant variant-gene pairs; it does not "
                    "cover priority tissues and does not contain complete all-variant association files."
                ),
            }
        ]
    )
    tar_status.to_csv(OUTDIR / "phase4d_gtex_significant_tar_status.tsv", sep="\t", index=False)

    eqtl_audit.to_csv(OUTDIR / "phase4d_prior_eqtl_source_audit_snapshot.tsv", sep="\t", index=False)
    loci.to_csv(OUTDIR / "phase4d_coloc_candidate_loci_snapshot.tsv", sep="\t", index=False)

    print("Wrote:")
    for path in sorted(OUTDIR.glob("phase4d_*")):
        print(path)


if __name__ == "__main__":
    main()
