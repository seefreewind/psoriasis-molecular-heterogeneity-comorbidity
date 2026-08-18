# PHASE 4D CAD Tier A Restricted Colocalization Report

Date: 2026-08-16  
Outcome: coronary artery disease (CAD)  
Input set: Phase 4C CAD Tier A recurrent SMR2 candidates  
Status: `CAD_COLOC_NO_STRONG_PP4_SIGNAL`

## 1. Analysis summary

We ran restricted coloc for CAD Tier A candidate gene-tissue pairs using eQTL Catalogue imported GTEx v8 remote tabix files. This analysis used rsID matching, allele harmonization to the eQTL ALT allele, CAD binary-trait metadata from Phase 4B LAVA (`122,733` cases and `424,528` controls), and `coloc.abf`.

Input table:

`results/phase4d_coloc/phase4d_coloc_input_feasibility_by_candidate_tissue.tsv`

Output table:

`results/phase4d_coloc/phase4d_restricted_coloc_cad_tierA_results.tsv`

Runner:

`src/genetics/phase4d_run_restricted_coloc_tierA.R`

## 2. Main result

All 19 CAD Tier A gene-tissue pairs passed input extraction and variant matching. No pair reached the planned strong colocalization threshold `PP4 >= 0.8`.

The strongest signals were skin-supported candidates at CAD locus 113:

| Gene | Tissue | Locus | Matched SNPs | PP3 | PP4 | Interpretation |
|---|---|---:|---:|---:|---:|---|
| `UBQLN4` | Skin sun-exposed lower leg | 113 | 2536 | 0.029 | 0.754 | suggestive |
| `UBQLN4` | Skin not sun-exposed suprapubic | 113 | 2527 | 0.030 | 0.746 | suggestive |
| `MEX3A` | Skin sun-exposed lower leg | 113 | 2495 | 0.048 | 0.597 | suggestive |
| `MEX3A` | Skin not sun-exposed suprapubic | 113 | 2486 | 0.048 | 0.595 | suggestive |

These results are suggestive but below the planned threshold. They can be retained as sensitivity-level coloc candidates, not as main coloc-supported findings.

## 3. Distinct-signal pattern

Most other CAD Tier A candidates showed `PP3 > PP4`, indicating evidence more consistent with distinct GWAS and eQTL signals than with a shared causal variant under the coloc model.

Examples:

| Gene | Tissue | Locus | PP3 | PP4 |
|---|---|---:|---:|---:|
| `TMEM116` | Artery aorta | 1841 | ~1.000 | 9.61e-09 |
| `TMEM116` | Artery coronary | 1841 | ~1.000 | 2.59e-06 |
| `TMEM116` | Whole blood | 1841 | ~1.000 | 5.89e-12 |
| `MAPKAPK5` | Skin sun-exposed lower leg | 1841 | ~1.000 | 1.23e-12 |
| `SMARCA4` | Skin sun-exposed lower leg | 2318 | ~1.000 | 6.17e-20 |
| `SMARCA4` | Skin not sun-exposed suprapubic | 2318 | ~1.000 | 3.50e-10 |

This is an important boundary for the manuscript. Several CAD genes have strong SMR/HEIDI support, but formal coloc does not support a shared causal variant for most CAD Tier A gene-tissue pairs tested here.

## 4. Interpretation

The CAD story should now be calibrated as:

> CAD remains the cleanest systemic shared-architecture track in Phase 4A/4B and has a robust SMR/HEIDI-prioritized regulatory-gene layer in Phase 4C, but restricted coloc does not yet provide strong PP4-supported gene-tissue pairs among CAD Tier A candidates.

Do not write:

> CAD Tier A genes are colocalized causal regulatory genes.

Allowed wording:

> CAD Tier A candidates were prioritized by SMR/HEIDI; restricted coloc showed suggestive support for `UBQLN4` and `MEX3A` in skin, while most other CAD candidates showed distinct-signal patterns.

## 5. Manuscript consequence

Phase 4C remains valid as an SMR/HEIDI candidate-gene prioritization layer. Phase 4D should be presented as a stricter follow-up that narrowed the claim:

1. no CAD Tier A candidate reached `PP4 >= 0.8`;
2. `UBQLN4` and `MEX3A` can be discussed as suggestive skin-supported CAD-local candidates;
3. `SMARCA4`, `TMEM116`, `MAPKAPK5` and `ADAM1B` should not be promoted as coloc-supported despite SMR recurrence;
4. the paper gains rigor by showing that SMR/HEIDI and coloc do not always agree.

## 6. Next step

Proceed to PsA Tier A restricted coloc as positive-control analysis.

Decision rule:

- If PsA Tier A produces strong `PP4 >= 0.8` signals, the coloc pipeline is behaving as expected and CAD's weaker PP4 can be interpreted as a real biological/statistical boundary.
- If PsA also produces no PP4-supported signals, reassess the coloc model, priors, coordinate/build matching, and eQTL source before running IBD.

MR remains prohibited.
