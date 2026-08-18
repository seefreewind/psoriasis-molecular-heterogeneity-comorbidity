# PHASE 4D PsA Tier A Positive-Control Colocalization Report

Date: 2026-08-16  
Outcome: psoriatic arthritis (PsA)  
Input set: Phase 4C PsA Tier A recurrent SMR2 candidates  
Status: `POSITIVE_CONTROL_PASS`

## 1. Purpose

PsA was run after CAD as a positive-control / near-neighbor phenotype. The goal was to test whether the Phase 4D coloc pipeline can recover strong shared GWAS-eQTL signals in a phenotype genetically close to psoriasis. This was not intended as the primary multisystem comorbidity claim.

Input:

`results/phase4d_coloc/phase4d_coloc_input_feasibility_by_candidate_tissue.tsv`

Output:

`results/phase4d_coloc/phase4d_restricted_coloc_psa_tierA_results.tsv`

Runner:

`src/genetics/phase4d_run_restricted_coloc_tierA.R`

## 2. Main result

All 39 PsA Tier A gene-tissue pairs completed. Three pairs reached the strong coloc threshold `PP4 >= 0.8`.

| Gene | Tissue | Locus | Matched SNPs | PP3 | PP4 | Interpretation |
|---|---|---:|---:|---:|---:|---|
| `SLC22A5` | Spleen | 887 | 2092 | 0.029 | 0.971 | coloc-supported |
| `RP11-977G19.11` | EBV-transformed lymphocytes | 1793 | 2036 | 0.055 | 0.945 | coloc-supported |
| `SLC22A5` | EBV-transformed lymphocytes | 887 | 2079 | 0.065 | 0.934 | coloc-supported |

Four additional pairs were suggestive but below the `PP4 >= 0.8` threshold:

| Gene | Tissue | Locus | PP4 |
|---|---|---:|---:|
| `RP11-977G19.11` | Skin not sun-exposed suprapubic | 1793 | 0.783 |
| `RP11-977G19.11` | Whole blood | 1793 | 0.773 |
| `SLC22A5` | Skin sun-exposed lower leg | 887 | 0.762 |
| `RP11-977G19.11` | Skin sun-exposed lower leg | 1793 | 0.749 |

## 3. Interpretation

This positive-control result supports the technical validity of the Phase 4D coloc route:

1. eQTL Catalogue imported GTEx v8 remote tabix files are usable for formal restricted coloc.
2. rsID-based matching with allele harmonization gives adequate SNP overlap.
3. The pipeline can recover strong PP4 signals when they are present.

The contrast with CAD is informative. CAD Tier A candidates were strongly prioritized by SMR/HEIDI, but none reached PP4 >= 0.8 in restricted coloc. PsA did produce strong PP4 signals, so the CAD result should not be dismissed as a global pipeline failure.

## 4. Manuscript consequence

PsA should remain a positive-control / near-neighbor track:

Allowed wording:

> The positive-control PsA analysis recovered strong coloc-supported signals for `SLC22A5` in immune tissues and `RP11-977G19.11` in EBV-transformed lymphocytes, supporting the ability of the restricted coloc pipeline to resolve shared regulatory signals in a psoriasis-neighbor phenotype.

Avoid:

> PsA proves broad multisystem comorbidity genetics.

For CAD:

> The absence of strong PP4 among CAD Tier A candidates appears to be a stricter locus-level boundary rather than a failure of the coloc pipeline, because the same workflow recovered strong PsA positive-control signals.

## 5. Next step

Proceed to IBD Tier A restricted coloc, stratified by local-rg direction.

Priority:

1. Crohn disease Tier A.
2. UC Tier A.
3. Summarize positive-local and negative-local direction groups separately.

Do not run MR.
