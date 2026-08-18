# PHASE 4A — Outcome GWAS Data Audit

Date searched: 2026-08-12

## Audit conclusion

Phase 4A can proceed to a formal GWAS-source audit. The strongest immediate candidates are available through consortium or official data portals for psoriatic arthritis, inflammatory bowel disease, coronary artery disease, ischemic stroke, type 2 diabetes, major depression, and chronic kidney disease.

Two outcomes need stricter resolution before analysis:

- MASLD: public resources are often labeled NAFLD, hepatic steatosis, or imaging/diagnostic-code NAFLD rather than current MASLD; phenotype harmonization must be explicit.
- Uveitis: the largest anterior uveitis resources may require FinnGen-style access steps, while freely downloadable BBJ uveitis is East Asian and not ancestry-matched to the European psoriasis GWAS.

## Frozen exposure

| Trait | Source | Local status |
|---|---|---|
| Psoriasis | GCST90472771 | Audited and downloaded in Phase 3A |

## Candidate outcome sources

| Outcome | Preferred source candidate | Evidence from source audit | Current status | Main risk |
|---|---|---|---|---|
| Psoriatic arthritis | Soomro2022_Psoriatic_Arthritis_EU via Knowledge Portal / GWAS Catalog | European ancestry GWAS with 5,065 PsA cases and 21,286 controls; summary statistics available from GWAS Catalog | High-priority primary candidate | Possible sample overlap with psoriasis GWAS cohorts must be checked |
| Crohn disease | GWAS_IBDGenetics_eu via IIBDGC / Knowledge Portal | European-descent meta-analysis includes Crohn disease, ulcerative colitis, and IBD phenotypes | High-priority primary candidate | Older but well-established IBD genetics resource; exact files and columns must be inspected |
| Ulcerative colitis | GWAS_IBDGenetics_eu via IIBDGC / Knowledge Portal | Same European IBD source includes UC phenotype | High-priority primary candidate | Same as Crohn disease |
| Coronary artery disease | CARDIoGRAMplusC4D / Common Metabolic Diseases Knowledge Portal / GWAS Catalog | CARDIoGRAMplusC4D provides CAD/MI meta-analysis summary data through official portals | High-priority primary candidate | Choose European or predominantly European release; avoid mixed-ancestry mismatch if a European release is available |
| Ischemic stroke | MEGASTROKE / International Stroke Genetics Consortium | MEGASTROKE releases stroke and subtype GWAS summary statistics with P values, betas, and SEs | High-priority primary candidate | Use European ancestry and all ischemic stroke phenotype if available |
| Type 2 diabetes | DIAGRAM / DIAMANTE / T2DGGI European release | DIAGRAM/T2DGGI provides association summary statistics through the consortium downloads page; European ancestry Mahajan et al. 2022 release is listed | High-priority primary candidate | Download requires terms acknowledgement; BMI-adjusted files must not be used as primary |
| MASLD | Ghodsian 2021 EHR-documented NAFLD or another auditable European NAFLD/MASLD source | Ghodsian 2021 is preferred for audit because it is an EHR-documented NAFLD meta-analysis; Namjou GCST008471 is now rejected as primary because preflight shows a case-only NAS pathology-score file with N=235 | Conditional candidate | Phenotype label and power: NAFLD is not identical to current MASLD, and small activity-score files cannot serve as primary disease GWAS |
| Major depression | PGC MDD2 without UK Biobank via Figshare | PGC MDD summary statistics excluding 23andMe and UK Biobank are available under CC0 | High-priority primary candidate | MDD ascertainment heterogeneity; ensure no UKB overlap if using no-UKBB file |
| Uveitis | FinnGen anterior uveitis or GWAS Catalog if summary stats are available; BBJ uveitis as non-European fallback only | FinnGen access page documents DF13 public download process; BBJ provides uveitis summary statistics but East Asian ancestry | Conditional candidate | European ancestry source may require access form; BBJ is ancestry-mismatched for primary LDSC with European psoriasis |
| Chronic kidney disease | CKDGen CKD / kidney-function GWAS | CKDGen provides GWAS summary statistics for kidney function and CKD datasets | High-priority primary candidate | Select CKD binary trait rather than eGFR-only if the outcome is CKD |

## Source notes

- LDSC is the locked first layer because it estimates genome-wide heritability and genetic correlation from GWAS summary statistics.
- LAVA is reserved for local genetic correlation after dataset harmonization and LDSC results.
- Outcome sources must be ancestry-compatible with GCST90472771 wherever possible.
- If a disease has only mixed-ancestry or non-European summary statistics, the disease should be marked sensitivity or replaced by a better European source before primary LDSC.

## Immediate next checks

1. Build a machine-readable source manifest with URL, accession, sample size, ancestry, phenotype, and access status.
2. For each source, test whether files can be downloaded non-interactively.
3. Inspect headers before choosing munge rules.
4. Install LDSC in a project or user-level environment if not already available.
5. Download LDSC HapMap3 SNP list and European LD-score reference only from official LDSC/Broad resources.

## Local LDSC tool status

LDSC is not currently available on the shell `PATH`.

Installation attempts on 2026-08-12:

- GitHub clone of Python 3 LDSC-compatible repository to `~/.codex/tools/ldsc-py3`: blocked by repeated network disconnects.
- GitHub zip download of the same repository: partial download only; archive integrity check failed.
- Bioconda `ldsc` through micromamba into `environment/ldsc_env`: failed because the available package requires Python 2 and old pandas/nose dependencies that are not solvable on the current osx-arm64 environment.

Current tool decision:

- Phase 4A design and data-source audit can continue locally.
- LDSC execution requires either a successful Python 3 LDSC install, a Linux/x86_64 conda/container runtime, or another verified LDSC-compatible environment.
- Do not replace LDSC with ad hoc genetic-correlation code.

## Preflight updates

The stricter Phase 4A audit now has two additional machine-readable files:

- `results/phase4a/phase4a_gwas_audit_matrix.tsv`
- `results/phase4a/download_preflight_headers.tsv`

Preflight findings:

- GCST90243956 PsA primary has reachable GWAS Catalog FTP files and a usable GWAS-SSF header.
- GCST006910 ischemic stroke has a reachable European MEGASTROKE file with marker, allele, beta, SE, and P columns.
- GCST008471 is not a MASLD primary candidate because the reachable file inspected here is `NamjouB_31311600_NAS_score.txt`, a case-only quantitative NAS score analysis with N=235.

## Sources checked

- GWAS Catalog GCST90472771 psoriasis page.
- LDSC official GitHub repository.
- LAVA official GitHub repository.
- Knowledge Portal page for Soomro2022 psoriatic arthritis.
- Knowledge Portal page for IBD Genetics European GWAS.
- CARDIoGRAMplusC4D data-download page.
- MEGASTROKE / International Stroke Genetics Consortium data pages.
- DIAGRAM/T2DGGI consortium downloads page.
- PGC MDD2 without UK Biobank Figshare page.
- CKDGen Consortium data pages.
- FinnGen access-results page.
- Knowledge Portal and GWAS Catalog pages for NAFLD/MASLD candidates.
- PheWeb.jp BBJ downloads page for uveitis fallback.
