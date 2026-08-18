# PHASE 4A — Audit and Harmonization Lock

Date: 2026-08-12

## Phase 4A scope

Phase 4A now starts formally, but the first step is source audit and harmonization planning. No LDSC genetic-correlation results have been generated in this step.

The frozen analysis is:

```text
overall psoriasis susceptibility
        x
10 prespecified comorbidities
        ->
LDSC genome-wide genetic correlation only
```

F1/F2/F6/F7 are not exposures and are not used for disease selection, GWAS selection, or post-hoc interpretation in Phase 4A.

## Frozen outcomes and source status

The machine-readable audit matrix is:

- `results/phase4a/phase4a_gwas_audit_matrix.tsv`
- `results/phase4a/download_preflight_headers.tsv`

Current source status:

| Outcome | Phase 4A status | Main source decision |
|---|---|---|
| Psoriatic arthritis | primary locked | GCST90243956, Soomro 2022 PsA vs controls |
| Crohn disease | primary locked pending exact file ID | de Lange 2017 / IIBDGC European Crohn subtype |
| Ulcerative colitis | primary locked pending exact file ID | de Lange 2017 / IIBDGC European UC subtype |
| Coronary artery disease | primary locked with overlap flag | GWAS_CADMETA_eu, CARDIoGRAMplusC4D + UK Biobank European meta-analysis |
| Ischemic stroke | primary locked | MEGASTROKE European ischemic stroke |
| Type 2 diabetes | primary locked | Mahajan 2022 DIAMANTE European unadjusted T2D |
| MASLD | conditional primary pending | Ghodsian 2021 EHR-documented NAFLD preferred; Namjou GCST008471 rejected as primary because it is small/activity-score based |
| Major depression | primary locked | PGC MDD2 without UK Biobank and 23andMe |
| Uveitis | conditional primary pending | European anterior uveitis source needed; BBJ is ancestry-mismatched backup only |
| Chronic kidney disease | primary locked pending exact file ID | CKDGen 2019 binary CKD preferred |

## Download preflight

Initial public-file preflight completed for selected GWAS Catalog/FTP files:

- GCST90243956 PsA primary: FTP directory and header are reachable; metadata reports GRCh37, 1-based coordinates, HRC r1.1 imputation, GWAS-SSF v1.0, European ancestry, 5,065 cases and 21,286 controls.
- GCST90243957 PsA backup: FTP directory is reachable, but the phenotype is PsA versus cutaneous psoriasis and is not suitable as the primary disease-versus-control genetic-correlation outcome.
- GCST006910 ischemic stroke: FTP directory and European MEGASTROKE header are reachable; sample N must be supplied from metadata during munging.
- GCST008471 Namjou NAFLD NAS score: FTP directory and header are reachable, but it is a case-only quantitative NAS pathology score with N=235, so it is rejected as MASLD/NAFLD primary input.

## Primary/backup rules

- The primary outcome GWAS is chosen before LDSC and cannot be changed based on rg significance.
- Backup GWAS can replace primary only for documented access failure, missing essential columns, severe QC failure, ancestry mismatch, or unusable phenotype definition.
- Backup selection must be recorded in `DECISION_LOG.md` before rg results are inspected.
- UK Biobank-heavy sources are allowed only with explicit overlap-risk annotation and LDSC cross-trait intercept reporting.

## Harmonization target

All summary statistics must be transformed into LDSC-compatible munged files using a single reference system.

Target system:

- rsID-centered variant identity where available;
- HapMap3 SNP set for LDSC regression;
- European LD-score reference for primary analyses;
- aligned effect allele and non-effect allele;
- signed effect size as beta/log OR where available;
- P value and sample size/effective sample size;
- binary-trait case/control counts recorded separately.

Genome build handling:

- Do not assume build from publication prose.
- Inspect header, README, and variant coordinate pattern before munging.
- If only rsID is used, build is less critical for LDSC but still recorded for later LAVA/coloc.
- If chr:position is used, build must be resolved before mapping.

## Munge QC required for every GWAS

Before LDSC rg, create one QC row per GWAS with:

- raw file path and checksum;
- source URL/accession;
- raw row count;
- variants with rsID;
- variants retained after HapMap3 merge;
- variants retained after allele filtering;
- variants retained after INFO/MAF filtering if available;
- mean chi-square;
- lambda GC;
- maximum chi-square;
- estimated h2 intercept fields from LDSC if available;
- notes on strand ambiguity, duplicate SNPs, missing N, missing allele, or extreme P values.

Any GWAS with abnormal SNP retention, missing essential columns, impossible allele coding, or implausible mean chi-square must be fixed before genetic correlation.

## LDSC Phase 4A output

The only Phase 4A result matrix is:

```text
Psoriasis x {PsA, CD, UC, CAD, ischemic stroke, T2D, MASLD, MDD, uveitis, CKD}
```

Required columns:

- outcome;
- primary GWAS source;
- rg;
- SE;
- Z;
- P;
- FDR across 10 outcomes;
- LDSC h2 z-score for psoriasis;
- LDSC h2 z-score for outcome;
- LDSC intercepts;
- cross-trait intercept;
- SNP count used by LDSC;
- interpretation tier.

## GO/CONDITIONAL/SHRINK rule

The Phase 4A decision is frozen before LDSC execution:

- GO: at least 3-4 different system domains show FDR-significant rg, coherent direction, and acceptable LDSC QC.
- CONDITIONAL GO: only 1-2 strong signals are detected, but they span more than one system domain or include a central comorbidity with clean QC.
- SHRINK: there is little robust rg evidence, major QC failure across outcomes, or signal is confined to one classic autoimmune outcome/domain.

## Prohibited during Phase 4A

- Axis-specific LDSC, LAVA, MR, coloc, or TWAS.
- LAVA before Phase 4A LDSC decision.
- Shared loci, coloc, or MR before Phase 4A LDSC decision.
- Replacing outcomes based on nonsignificant LDSC results.
- Adding diseases to create a positive multisystem story.
- Using F1/F2/F6/F7 to select or rename genetic results.
