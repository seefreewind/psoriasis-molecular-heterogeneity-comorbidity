#!/usr/bin/env python3

from pathlib import Path

import pandas as pd


ROOT = Path.cwd()
INFILE = ROOT / "results/phase4b_restricted_lava/phase4b_restricted_lava_bivariate.tsv"
OUTDIR = ROOT / "results/phase4br_ld_reference_validation"
OUTDIR.mkdir(parents=True, exist_ok=True)

b = pd.read_csv(INFILE, sep="\t")
b["locus"] = b["locus"].astype(str)
b["fdr_all_tests"] = b["fdr_all_tests"].astype(float)
b["fdr_within_outcome"] = b["fdr_within_outcome"].astype(float)

parts = []

cad = b[
    (b["outcome"] == "cad")
    & (b["rho"] > 0)
    & (b["fdr_all_tests"] < 0.05)
].copy()
cad["validation_priority"] = "CAD_globalFDR_positive"
parts.append(cad)

psa = b[(b["outcome"] == "psa") & (b["rho"] > 0)].sort_values("p").head(10).copy()
psa["validation_priority"] = "PsA_top10_positive_control"
parts.append(psa)

ibd = b[
    (b["outcome"].isin(["crohn", "uc"]))
    & (b["fdr_within_outcome"] < 0.05)
].copy()
common = set(ibd[ibd["outcome"] == "crohn"]["locus"]).intersection(
    set(ibd[ibd["outcome"] == "uc"]["locus"])
)
ibd_common = ibd[ibd["locus"].isin(common)].copy()
ibd_common["validation_priority"] = "IBD_common_FDR"
parts.append(ibd_common)

for outcome in ["crohn", "uc"]:
    x = ibd[ibd["outcome"] == outcome]
    neg = x[~x["locus"].isin(common) & (x["rho"] < 0)].sort_values("p").head(3).copy()
    neg["validation_priority"] = "IBD_negative_FDR"
    pos = x[~x["locus"].isin(common) & (x["rho"] > 0)].sort_values("p").head(3).copy()
    pos["validation_priority"] = "IBD_positive_FDR"
    parts.extend([neg, pos])

out = pd.concat(parts, ignore_index=True)
out = out.drop_duplicates(["outcome", "locus"]).copy()
out["ld_ref_primary"] = "1000G_EUR_PLINK"
out["ld_ref_retest"] = "LAVA_UKB_v1.1_binary"
out["phase4c_eligible_before_retest"] = True
out = out.sort_values(["outcome", "validation_priority", "p"])

cols = [
    "outcome",
    "pair_scope",
    "validation_priority",
    "locus",
    "chr",
    "start",
    "stop",
    "rho",
    "se_approx",
    "z_approx",
    "p",
    "fdr_within_outcome",
    "fdr_all_tests",
    "direction",
    "h2_psoriasis",
    "h2_outcome",
    "univ_p_psoriasis",
    "univ_p_outcome",
    "ld_ref_primary",
    "ld_ref_retest",
    "phase4c_eligible_before_retest",
]
out[cols].to_csv(OUTDIR / "phase4br_priority_loci.tsv", sep="\t", index=False)

chroms = sorted(out["chr"].astype(int).unique())
group_map = {
    "chr1-2": [1, 2],
    "chr3-4": [3, 4],
    "chr5-6": [5, 6],
    "chr7-9": [7, 8, 9],
    "chr10-12": [10, 11, 12],
    "chr13-16": [13, 14, 15, 16],
    "chr17-23": [17, 18, 19, 20, 21, 22, 23],
}
rows = []
for group, gs in group_map.items():
    needed = sorted(set(chroms).intersection(gs))
    if needed:
        rows.append({"ukb_archive_group": group, "needed_chromosomes": ",".join(map(str, needed))})
pd.DataFrame(rows).to_csv(OUTDIR / "phase4br_required_ukb_ld_archives.tsv", sep="\t", index=False)

print(out[["outcome", "locus", "chr", "rho", "p", "fdr_all_tests", "validation_priority"]].to_string(index=False))
print(f"priority disease-locus rows: {len(out)}")
print(f"unique loci: {out['locus'].nunique()}")
print(f"required chromosomes: {','.join(map(str, chroms))}")
