# Phase 4D Restricted Tier A Colocalization Final Report

Date: 2026-08-16

## Executive decision

Phase 4D restricted coloc is complete.

Current status:

```text
PHASE4D_COMPLETE_RESTRICTED_COLOC
MR_REMAINS_PROHIBITED
AXIS_SPECIFIC_GENETICS_REMAINS_NO_GO
```

The restricted Tier A coloc analysis supports three conclusions.

First, the positive-control PsA analysis recovered strong colocalization signals, showing that the eQTL-coloc pipeline is technically capable of detecting shared causal-signal evidence when it exists.

Second, CAD remains the cleanest non-neighbor systemic genetic-correlation signal from Phase 4A/4B, but the restricted Tier A eQTL-coloc layer did not identify a strong CAD gene-tissue pair. CAD should therefore be described as LAVA/SMR-prioritized shared genetic architecture, not as coloc-confirmed eQTL mediation.

Third, UC produced a strong colon-specific coloc-supported signal at RP11-973H7.1 in locus 2251, but this result used an eQTL MAF proxy because the available UC GWAS locus file lacked GWAS EAF. It can be retained as a high-value IBD coloc candidate with a sensitivity label, not as an unrestricted definitive coloc result.

## Inputs

### GWAS traits

The restricted coloc analysis used the frozen Phase 4 genetic scope:

| Trait | Role | Binary trait metadata source |
|---|---|---|
| Psoriasis | exposure / anchor trait | LAVA input metadata |
| CAD | primary systemic target | LAVA input metadata |
| PsA | positive-control / near-neighbor sensitivity | LAVA input metadata |
| Crohn disease | IBD direction-heterogeneity target | LAVA input metadata |
| Ulcerative colitis | IBD direction-heterogeneity target | LAVA input metadata |

Binary trait parameters recovered from the LAVA input metadata were used for coloc `type="cc"`:

| Trait | Cases | Controls | Total N | Case fraction |
|---|---:|---:|---:|---:|
| psoriasis | 36,466 | 458,078 | 494,544 | 0.073737 |
| CAD | 122,733 | 424,528 | 547,261 | 0.224268 |
| PsA | 5,065 | 21,286 | 26,351 | 0.192213 |
| Crohn disease | 12,194 | 28,072 | 40,266 | 0.302836 |
| ulcerative colitis | 12,366 | 33,609 | 45,975 | 0.268972 |

### eQTL data

GTEx v8 eQTLs were accessed through eQTL Catalogue imported GTEx v8 remote tabix files. Local GTEx v8 SMR BESD files were retained for SMR/HEIDI, but they were not used as direct coloc input because BESD is not a coloc-ready per-variant summary-statistic format.

The restricted coloc workflow used the frozen Phase 4C Tier A gene-tissue candidates derived from recurrent LAVA/SMR evidence. No transcriptomic axes were used as genetic exposures.

## Harmonization and matching

The analysis used the following matching rules:

| Outcome | Matching strategy | Notes |
|---|---|---|
| CAD | rsID matching | GWAS locus file retained rsID-level variants |
| PsA | rsID matching | GWAS locus file retained rsID-level variants |
| Crohn disease | hg19 to hg38 liftover, then coordinate matching | GWAS rsIDs were unavailable for coloc matching |
| Ulcerative colitis | hg19 to hg38 liftover, then coordinate matching | GWAS rsIDs were unavailable for coloc matching |

For Crohn disease and ulcerative colitis, GWAS EAF was unavailable in the coloc locus files. These IBD analyses therefore used GTEx eQTL MAF as a proxy for coloc variance specification and are flagged as:

```text
maf_source = eqtl_maf_proxy
```

This is acceptable for restricted sensitivity triage, but any IBD coloc result should remain labeled until an EAF-containing GWAS file or equivalent allele-frequency annotation is obtained.

## QC and implementation

Scripts:

| Script | Purpose |
|---|---|
| `src/genetics/phase4d_coloc_input_feasibility_audit.py` | audited GTEx/eQTL source feasibility |
| `src/genetics/phase4d_coloc_smoke_test.R` | confirmed the coloc data path and gene-specific filtering |
| `src/genetics/phase4d_liftover_gwas_loci_hg19_to_hg38.py` | lifted psoriasis, Crohn, and UC locus files from hg19 to hg38 |
| `src/genetics/phase4d_run_restricted_coloc_tierA.R` | ran restricted Tier A coloc for CAD, PsA, Crohn, and UC |

Key output tables:

| File | Description |
|---|---|
| `results/phase4d_coloc/phase4d_restricted_coloc_cad_tierA_results.tsv` | CAD restricted Tier A coloc |
| `results/phase4d_coloc/phase4d_restricted_coloc_psa_tierA_results.tsv` | PsA restricted Tier A coloc |
| `results/phase4d_coloc/phase4d_restricted_coloc_crohn_tierA_results.tsv` | Crohn restricted Tier A coloc |
| `results/phase4d_coloc/phase4d_restricted_coloc_uc_tierA_results.tsv` | UC restricted Tier A coloc |
| `results/phase4d_coloc/phase4d_restricted_coloc_tierA_all_results.tsv` | combined coloc result table |
| `results/phase4d_coloc/phase4d_restricted_coloc_tierA_summary.tsv` | outcome-level interpretation summary |

Coloc interpretation thresholds were frozen as:

| Tier | Rule | Interpretation |
|---|---|---|
| coloc-supported | PP4 >= 0.80 | evidence for a shared causal signal |
| suggestive | 0.50 <= PP4 < 0.80 | candidate shared signal requiring stronger support |
| distinct-signal | PP3 > PP4 | likely distinct causal signals within the same locus |

## Outcome-level summary

| Outcome | Interpretation tier | Number of gene-tissue pairs |
|---|---|---:|
| CAD | distinct_signal_PP3_gt_PP4 | 15 |
| CAD | suggestive_PP4_0p5_to_0p8 | 4 |
| Crohn disease | distinct_signal_PP3_gt_PP4 | 22 |
| Crohn disease | suggestive_PP4_0p5_to_0p8 | 2 |
| PsA | coloc_supported_PP4_ge_0p8 | 3 |
| PsA | distinct_signal_PP3_gt_PP4 | 32 |
| PsA | suggestive_PP4_0p5_to_0p8 | 4 |
| Ulcerative colitis | coloc_supported_PP4_ge_0p8 | 2 |
| Ulcerative colitis | distinct_signal_PP3_gt_PP4 | 24 |

Outcome-level PP4 distribution:

| Outcome | Tested pairs | Max PP4 | Median PP4 |
|---|---:|---:|---:|
| CAD | 19 | 0.754341 | 0.00000259 |
| Crohn disease | 24 | 0.638935 | 0.001099 |
| PsA | 39 | 0.970896 | 0.00000226 |
| Ulcerative colitis | 26 | 0.959990 | 0.000227 |

## Strong coloc-supported findings

### PsA positive-control signals

| Outcome | Locus | Gene | Tissue | Matched variants | PP3 | PP4 |
|---|---:|---|---|---:|---:|---:|
| PsA | 887 | SLC22A5 | Spleen | 2,092 | 0.029104 | 0.970896 |
| PsA | 1793 | RP11-977G19.11 | EBV-transformed lymphocytes | 2,036 | 0.054524 | 0.945450 |
| PsA | 887 | SLC22A5 | EBV-transformed lymphocytes | 2,079 | 0.064967 | 0.934371 |

Interpretation:

The PsA positive-control analysis recovered strong PP4-supported immune/eQTL signals. This supports the technical validity of the restricted coloc workflow and confirms that the absence of strong CAD PP4 is unlikely to be caused by a globally failed pipeline.

### Ulcerative colitis colon-specific signal

| Outcome | Locus | Gene | Tissue | Matched variants | PP3 | PP4 | MAF source |
|---|---:|---|---|---:|---:|---:|---|
| UC | 2251 | RP11-973H7.1 | Colon Transverse | 2,649 | 0.037769 | 0.959990 | eQTL MAF proxy |
| UC | 2251 | RP11-973H7.1 | Colon Sigmoid | 2,649 | 0.037938 | 0.959811 | eQTL MAF proxy |

Interpretation:

RP11-973H7.1 at locus 2251 is the strongest IBD coloc-supported result and is tissue-concordant with ulcerative colitis biology. Because this analysis used eQTL MAF as a proxy for GWAS EAF, it should enter the manuscript as a sensitivity-labeled coloc-supported candidate. It should be prioritized for EAF-complete reanalysis before any causal or mediation claim.

## Suggestive findings

### CAD

| Outcome | Locus | Gene | Tissue | Matched variants | PP3 | PP4 |
|---|---:|---|---|---:|---:|---:|
| CAD | 113 | UBQLN4 | Skin Sun Exposed Lower leg | 2,536 | 0.029294 | 0.754341 |
| CAD | 113 | UBQLN4 | Skin Not Sun Exposed Suprapubic | 2,527 | 0.030330 | 0.745851 |
| CAD | 113 | MEX3A | Skin Sun Exposed Lower leg | 2,495 | 0.048183 | 0.596904 |
| CAD | 113 | MEX3A | Skin Not Sun Exposed Suprapubic | 2,486 | 0.048396 | 0.595072 |

Interpretation:

CAD produced skin-enriched suggestive coloc signals at locus 113, led by UBQLN4 and MEX3A. These do not pass the PP4 >= 0.80 coloc-supported threshold. CAD should remain the main systemic genetic-architecture result because Phase 4A/4B gave clean cross-system evidence, but the eQTL-coloc layer should be described as suggestive only.

### Crohn disease

| Outcome | Locus | Gene | Tissue | Matched variants | PP3 | PP4 | MAF source |
|---|---:|---|---|---:|---:|---:|---|
| Crohn disease | 887 | SLC22A5 | Colon Sigmoid | 3,638 | 0.357880 | 0.638935 | eQTL MAF proxy |
| Crohn disease | 10 | PARK7 | Whole Blood | 2,222 | 0.434408 | 0.564517 | eQTL MAF proxy |

Interpretation:

Crohn disease produced only suggestive PP4 signals. Because all Crohn coloc runs depended on eQTL MAF proxy and no pair reached PP4 >= 0.80, Crohn should not be treated as coloc-confirmed. It remains part of the IBD local-direction heterogeneity story from LAVA/SMR, with coloc candidates requiring EAF-complete reanalysis.

## Distinct-signal findings

Most tested Tier A gene-tissue pairs were PP3-dominant, especially for CAD, Crohn disease, and several UC/PsA candidates. This pattern means that LAVA or SMR-prioritized shared loci often do not collapse into a single shared eQTL-mediated causal signal under coloc. This distinction is important for the manuscript:

```text
shared locus / local rg / SMR signal
does not automatically equal
same causal variant / eQTL-mediated colocalization
```

This result strengthens the evidentiary hierarchy. LAVA identifies local shared architecture, SMR/HEIDI prioritizes expression-linked genes, and coloc is reserved for the narrower claim that two association patterns are consistent with one shared causal signal.

## Manuscript interpretation

### CAD

CAD remains the primary systemic comorbidity genetics target because it showed the cleanest non-neighbor Phase 4A/4B signal. The current coloc layer does not support a strong CAD eQTL-mediated shared causal signal among restricted Tier A candidates.

Recommended manuscript wording:

> For CAD, restricted eQTL colocalization did not identify PP4-supported gene-tissue pairs among Tier A candidates. UBQLN4 and MEX3A at locus 113 showed suggestive skin eQTL colocalization, but the CAD signal should be interpreted primarily as shared genetic architecture supported by genome-wide and local genetic-correlation analyses, with SMR/HEIDI-prioritized expression candidates requiring further validation.

### PsA

PsA should remain a positive control rather than a central multisystem comorbidity claim. Its strong SLC22A5 and RP11-977G19.11 coloc signals show that the pipeline can recover strong shared causal-signal evidence for a near-neighbor psoriatic disease phenotype.

Recommended manuscript wording:

> The PsA positive-control analysis recovered strong PP4-supported eQTL colocalization for SLC22A5 and RP11-977G19.11 in immune-relevant tissues, supporting the validity of the restricted coloc workflow.

### IBD

IBD should be framed as local-direction heterogeneous rather than simply positive or negative global genetic correlation. UC has one high-value colon-specific coloc-supported candidate, while Crohn disease remains suggestive only.

Recommended manuscript wording:

> In IBD, restricted coloc highlighted tissue-specific heterogeneity. UC showed strong colon-specific colocalization for RP11-973H7.1 at locus 2251 under an eQTL MAF-proxy sensitivity framework, whereas Crohn disease showed only suggestive signals. These findings support a local-architecture view of psoriasis-IBD sharing and argue against reducing the relationship to a single genome-wide direction.

## Limitations and required labels

1. The coloc analysis was restricted to Tier A candidates and should not be interpreted as an exhaustive genome-wide coloc screen.
2. GTEx v8 eQTLs were accessed through eQTL Catalogue imported remote tabix files; this is appropriate for summary-statistic coloc, but source and tissue mapping should be documented in Methods.
3. Crohn disease and UC analyses used eQTL MAF as a proxy because GWAS EAF was unavailable in the current locus files.
4. PP4-supported UC results require EAF-complete sensitivity analysis before any causal-mediation claim.
5. CAD has no strong PP4-supported Tier A coloc result; the CAD story should not be rewritten as coloc-confirmed expression mediation.
6. F1/F2/F6/F7 molecular axes remain excluded from genetics main analyses and should only appear later as transcriptomic contextualization.

## Next action

The next recommended step is manuscript integration, not MR.

Immediate next file to prepare:

```text
PHASE4D_MANUSCRIPT_RESULTS_AND_DISCUSSION_UPDATE.md
```

That update should add:

1. A coloc Methods paragraph.
2. A coloc Results subsection.
3. A restrained Discussion paragraph on the evidence hierarchy.
4. Supplementary table captions for the combined coloc results.
5. A fixed GO/NO-GO statement for MR.

MR should remain blocked until the project explicitly decides whether any mediation analysis will be limited to PP4-supported loci only and whether IBD GWAS EAF-complete files can be obtained.

