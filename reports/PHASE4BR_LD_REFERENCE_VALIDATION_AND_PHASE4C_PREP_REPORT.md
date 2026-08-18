# Phase 4B-R LD-reference validation and Phase 4C coloc preparation

Date: 2026-08-14

## Executive decision

Phase 4B-R is complete. The restricted LAVA loci were re-tested with the LAVA UK Biobank v1.1 binary LD reference, and only LD-reference-stable loci are allowed to enter Phase 4C colocalization.

The project should proceed to Phase 4C with the following boundary:

- CAD remains the primary systemic comorbidity signal.
- PsA is retained as a positive-control / near-neighbor phenotype.
- Crohn disease and ulcerative colitis are retained as IBD direction-heterogeneity phenotypes.
- Only Tier 1 and Tier 2 loci enter coloc.
- Tier 3 loci are excluded from coloc.
- No MR, LAVA expansion, or axis-specific genetics is allowed at this step.

## Why this step was inserted

The restricted Phase 4B LAVA run used a 1000G EUR PLINK LD reference and produced interpretable local genetic correlation signals. Because LAVA 0.1.5 recommends the UK Biobank binary LD reference for European-ancestry analyses, high-value loci were re-tested before coloc. This was necessary because the initial LAVA run contained local warning patterns, including negative variance estimates and low-coverage or unstable loci.

The local LAVA reference note used for this decision is:

`tools/phase4b_lava/LAVA-main/REFERENCE.md`

It states that the UK Biobank reference is recommended for European-ancestry analyses and is computed from 100,000 unrelated European-ancestry UK Biobank individuals.

## Inputs

Primary 1000G restricted LAVA output:

- `results/phase4b_restricted_lava/phase4b_restricted_lava_bivariate.tsv`
- `results/phase4b_restricted_lava/phase4b_restricted_lava_top_loci.tsv`

Phase 4B-R priority locus list:

- `results/phase4br_ld_reference_validation/phase4br_priority_loci.tsv`

UKB LD reference:

- Raw archives: `data/genetics/reference/lava_ukb_v1.1/raw/`
- Extracted reference: `data/genetics/reference/lava_ukb_v1.1/extracted/`
- Extracted `.bcor` files: 23
- Extracted `.info` files: 23

Logs:

- `logs/phase4br_ld_reference/aria2_download.log`
- `logs/phase4br_ld_reference/ukb_lava_v1.1_extracted_files.txt`
- `logs/phase4br_ld_reference/phase4br_ukb_chr1_2_smoke.log`
- `logs/phase4br_ld_reference/phase4br_ukb_chr4_validation.log`
- `logs/phase4br_ld_reference/phase4br_ukb_chr5_6_validation.log`
- `logs/phase4br_ld_reference/phase4br_ukb_chr7_9_validation.log`
- `logs/phase4br_ld_reference/phase4br_ukb_chr10_12_validation.log`
- `logs/phase4br_ld_reference/phase4br_ukb_chr13_16_validation.log`
- `logs/phase4br_ld_reference/phase4br_ukb_chr17_23_validation.log`

## Priority locus selection

Only high-value loci were re-tested, rather than re-running all 2495 LAVA loci.

The re-test set contained 53 disease-locus rows across 38 unique loci. The required chromosomes were:

`1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 13, 15, 17, 18, 19, 20, 21, 22`

Selection rules:

- CAD: all positive local loci with global all-test FDR support from the restricted LAVA run.
- PsA: the strongest positive loci, used as positive-control local architecture.
- Crohn/UC: shared IBD loci and selected positive/negative loci to test whether direction heterogeneity survives LD-reference re-testing.

## Tier definitions

Tier 1:

- Direction concordant between 1000G and UKB.
- Both traits have reliable local h2 under UKB.
- UKB local signal remains FDR-supported within outcome.

Tier 2:

- Direction concordant between 1000G and UKB.
- Both traits have reliable local h2 under UKB.
- Statistical support weakens under UKB but the direction and local h2 remain interpretable.

Tier 3:

- Direction flip, missing result, negative local variance, unreliable local h2, or required phenotype unavailable after local variance filtering.

Only Tier 1 and Tier 2 are eligible for Phase 4C coloc.

## Final tier summary

| Outcome | Tier 1 | Tier 2 | Tier 3 | Phase 4C eligible |
|---|---:|---:|---:|---:|
| CAD | 5 | 7 | 5 | 12 |
| Crohn disease | 11 | 1 | 1 | 12 |
| PsA | 10 | 0 | 0 | 10 |
| Ulcerative colitis | 9 | 1 | 3 | 10 |
| Total | 35 | 9 | 9 | 44 |

Machine-readable tier outputs:

- `results/phase4br_ld_reference_validation/phase4br_ld_reference_comparison.tsv`
- `results/phase4br_ld_reference_validation/phase4br_tier_summary.tsv`

## Main biological and statistical interpretation

### CAD

CAD remains the cleanest non-neighbor systemic signal. All coloc-eligible CAD loci retain positive local rg under the UKB reference.

Tier 1 CAD loci:

| Locus | Chr | rho_UKB | P_UKB |
|---:|---:|---:|---:|
| 347 | 2 | 0.979 | 1.67e-07 |
| 1841 | 12 | 0.517 | 3.57e-04 |
| 113 | 1 | 0.705 | 4.68e-03 |
| 267 | 2 | 0.560 | 1.55e-02 |
| 2318 | 19 | 0.185 | 1.83e-02 |

Important exclusion:

- CAD locus 1215 was one of the strongest 1000G signals but failed under UKB because local h2 was not reliable in both traits. It should not enter coloc.

Interpretation: the psoriasis-CAD signal is not a single-locus artifact, but the final coloc story must rely on UKB-stable Tier 1/2 loci.

### PsA

PsA behaved as the expected near-neighbor positive control. All 10 selected PsA loci are Tier 1 and positive under UKB.

Interpretation: this supports the LAVA pipeline's ability to recover strong immune-neighbor sharing. PsA should be used for sanity checking and method validation, not as the main multisystem comorbidity claim.

### Crohn disease

Crohn disease retains direction heterogeneity under UKB:

- Tier 1 negative local rg loci: 7
- Tier 1 positive local rg loci: 4
- Tier 2 negative local rg loci: 1

The strongest shared IBD locus remains negative:

| Locus | Chr | rho_UKB | P_UKB |
|---:|---:|---:|---:|
| 57 | 1 | -0.564 | 2.06e-20 |

Important exclusion:

- Crohn locus 26 was positive in the 1000G run but failed UKB local h2 reliability, so it should not enter coloc.

Interpretation: the Crohn result should not be summarized as a simple genome-wide negative relationship. The stronger claim is local direction heterogeneity.

### Ulcerative colitis

UC also retains direction heterogeneity:

- Tier 1 negative local rg loci: 7
- Tier 1 positive local rg loci: 2
- Tier 2 positive local rg loci: 1

The shared IBD locus 57 is robustly negative:

| Locus | Chr | rho_UKB | P_UKB |
|---:|---:|---:|---:|
| 57 | 1 | -0.722 | 5.27e-20 |

Important exclusions:

- UC loci 26, 638, and 768 are Tier 3 because UKB local h2 or phenotype availability failed.

Interpretation: the IBD finding is better framed as mixed local architecture, with coloc performed separately for positive-local and negative-local loci.

## Phase 4C coloc candidate set

The coloc-ready candidate table has been frozen:

- `results/phase4c_preparation/phase4c_coloc_candidate_loci.tsv`
- `results/phase4c_preparation/phase4c_coloc_candidate_summary.tsv`

Candidate counts:

| Outcome | Direction group | Tier | Coloc role | N loci |
|---|---|---|---|---:|
| CAD | positive | Tier 1 | primary_coloc | 5 |
| CAD | positive | Tier 2 | sensitivity_coloc | 7 |
| Crohn disease | negative | Tier 1 | primary_coloc | 7 |
| Crohn disease | positive | Tier 1 | primary_coloc | 4 |
| Crohn disease | negative | Tier 2 | sensitivity_coloc | 1 |
| PsA | positive | Tier 1 | primary_coloc | 10 |
| Ulcerative colitis | negative | Tier 1 | primary_coloc | 7 |
| Ulcerative colitis | positive | Tier 1 | primary_coloc | 2 |
| Ulcerative colitis | positive | Tier 2 | sensitivity_coloc | 1 |

## Phase 4C execution boundary

Proceed to shared-locus and eQTL colocalization with this scope:

CAD:

- Primary systemic target.
- Use skin, blood, and vascular/arterial eQTL resources.
- Prioritize Tier 1 loci for main tables; keep Tier 2 for sensitivity tables.

PsA:

- Positive-control / near-neighbor phenotype.
- Use skin and blood/immune eQTL resources.
- Use results to confirm pipeline behavior, not as the central multisystem claim.

Crohn disease and UC:

- Analyze positive-local and negative-local loci separately.
- Use skin, blood, intestinal, and immune eQTL resources.
- Interpret as local direction heterogeneity, not as a uniform protective or risk-sharing architecture.

Do not perform:

- MR
- axis-specific LDSC/LAVA/MR/coloc
- drug prediction
- PPI or hub-gene expansion
- genome-wide LAVA expansion beyond the current restricted, frozen scope

## GO decision

Phase 4B-R gives a GO to Phase 4C, with a restricted coloc scope.

The immediate next task is:

`PHASE 4C — SHARED-LOCUS AND eQTL COLOCALIZATION FOR UKB-STABLE TIER 1/2 LAVA LOCI`

