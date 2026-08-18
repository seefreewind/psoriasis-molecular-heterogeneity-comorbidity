# PHASE 4A — Overall Psoriasis Multisystem Genetic Architecture Plan

Date: 2026-08-12

## One-line decision

Phase 4A will test overall psoriasis genetic liability against prespecified multisystem comorbidities. It will not test F1/F2/F6/F7 as genetic exposures.

## Why this phase exists

Phase 3A produced a clear `NO-GO_FOR_GENETICALLY_ANCHORED_AXES`. The frozen transcriptomic axes remain useful as replicated skin-primary molecular programs, but they cannot be described as inherited psoriasis susceptibility components.

The genetic layer is therefore redesigned around a cleaner question:

> Does overall psoriasis genetic liability share genome-wide or local genetic architecture with major clinical comorbidities?

This separates two valid findings:

- transcriptomic layer: replicated tissue molecular heterogeneity;
- genetic layer: shared multisystem inherited liability.

## Frozen exposure

Primary exposure:

- overall psoriasis susceptibility GWAS;
- primary source: GCST90472771;
- current local status: official GWAS Catalog/EMBL-EBI source audited and downloaded in Phase 3A.

No axis score, axis gene set, CORE program, EXTENDED program, or transcriptomic loading may be used as the Phase 4A exposure.

## Frozen outcomes

The Phase 4A primary outcome panel contains 10 diseases:

| Outcome | System domain | Primary role |
|---|---|---|
| Psoriatic arthritis | autoimmune / musculoskeletal | expected positive control-like comorbidity |
| Crohn disease | autoimmune / intestinal inflammation | inflammatory comorbidity |
| Ulcerative colitis | autoimmune / intestinal inflammation | inflammatory comorbidity |
| Coronary artery disease | cardiometabolic / vascular | multisystem cardiometabolic comorbidity |
| Ischemic stroke | vascular / neurologic | vascular comorbidity |
| Type 2 diabetes | cardiometabolic | metabolic comorbidity |
| MASLD | hepatometabolic | metabolic liver comorbidity |
| Major depression | neuropsychiatric / immune-neuroendocrine | neuroimmune comorbidity |
| Uveitis | ocular / immune | immune extra-cutaneous comorbidity |
| Chronic kidney disease | renal / vascular-metabolic | renal comorbidity |

No additional diseases should be added before the frozen 10-outcome panel is audited and tested.

## Phase 4A module order

### Module 1: Outcome GWAS audit

For each outcome, record:

- source repository and accession or URL;
- publication or consortium;
- ancestry;
- sample size and case/control count if binary;
- genome build;
- variant identifier fields;
- effect allele and non-effect allele fields;
- beta/log odds ratio or odds ratio;
- standard error;
- P value;
- effective sample size availability;
- sample-overlap risk with psoriasis GWAS;
- download feasibility.

Datasets that lack essential LDSC fields move to replacement-audit status before analysis.

### Module 2: Harmonization and munging

Use the same reference and allele-harmonization principles across psoriasis and outcome GWAS files.

Required checks:

- genome build compatibility;
- SNP ID or chr:position mapping;
- allele validity;
- duplicate variant handling;
- strand-ambiguous SNP filtering policy;
- INFO/MAF filters when available;
- sample size or effective sample size handling;
- liability-scale settings for binary traits where needed.

### Module 3: LDSC genome-wide genetic correlation

Primary output table:

| Disease | rg | SE | P | FDR | Interpretation |
|---|---:|---:|---:|---:|---|

FDR is calculated across the 10 prespecified outcomes.

Interpretation tiers:

- Tier A: FDR-significant rg with coherent direction and acceptable LDSC QC;
- Tier B: nominal rg with plausible biology and acceptable QC;
- Tier C: weak or unstable rg;
- Tier D: not analyzable or QC failure.

### Module 4: Phase 4B candidate selection

Only Tier A and selected Tier B disease pairs proceed to LAVA local genetic correlation.

Proceeding to LAVA requires:

- harmonized summary statistics for both traits;
- compatible ancestry and LD reference;
- sufficient genome-wide signal or local h2 support;
- no unresolved major sample-overlap issue.

### Module 5: Later shared-locus and causal-direction layers

Shared loci, colocalization, TWAS sensitivity, and bidirectional MR are not Phase 4A primary analyses.

They are deferred as:

- Phase 4B: LAVA local genetic correlation;
- Phase 4C: shared loci and colocalization;
- Phase 4D: bidirectional MR as directional support;
- Phase 4E: exploratory transcriptomic contextualization.

## Transcriptomic contextualization rule

F1/F2/F6/F7 may be reintroduced only after shared loci are discovered independently.

Allowed:

- overlap between shared-locus genes and frozen axis programs;
- ORA against frozen CORE/EXTENDED programs;
- rank enrichment using frozen axis gene rankings.

Required wording:

> transcriptomic contextualization of shared genetic loci

Prohibited wording:

> axis-specific genetic causation

## Stop and shrink rules

If at least 2-3 distinct system domains show supported genome-wide or local sharing, continue toward a multisystem comorbidity genetic architecture manuscript.

If support is concentrated in psoriatic arthritis and inflammatory bowel disease, shrink to autoimmune comorbidity genetic architecture.

If most outcomes fail LDSC QC or show no interpretable sharing, report Phase 4A as a negative genetic-comorbidity architecture screen and keep the manuscript centered on replicated tissue molecular heterogeneity.

## Prohibited analyses in this phase

- Axis-specific LDSC, LAVA, MR, coloc, or TWAS.
- Alternative GWAS hunting to rescue F1/F2/F6/F7.
- EXTENDED gene-set rescue.
- PPI, hub-gene, LASSO, or drug prediction.
- Large disease scans before the frozen 10-outcome panel is complete.
- Renaming transcriptomic axes using genetic results.

## Expected outputs

- `results/phase4a/frozen_comorbidity_outcomes.tsv`
- `reports/PHASE4A_GWAS_OUTCOME_DATA_AUDIT.md`
- harmonized outcome GWAS manifest
- LDSC munged summary statistics
- `results/phase4a/ldsc_genetic_correlation_results.tsv`
- Phase 4A GO/SHRINK report

## Manuscript positioning

Current best title direction:

> Molecular heterogeneity and shared multisystem genetic architecture of psoriasis

Alternative title direction:

> Replicated molecular axes of psoriasis are distinct from its shared genetic architecture of multisystem comorbidity

