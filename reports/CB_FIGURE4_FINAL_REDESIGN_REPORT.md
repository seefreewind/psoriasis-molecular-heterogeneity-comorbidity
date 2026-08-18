# Figure 4 Final Redesign Report

## Previous Weaknesses
- The previous framing could read as negative or failure-oriented rather than as an evidence-boundary result.
- Panel a used workflow-like language and the word `Frozen`.
- Panel b placed FDR labels close to the intervals instead of using a clean aligned column.
- Panel c used `Observed statistic vs null mean +/- SD`, which described the encoding rather than the x-axis statistic.
- Panel d used parallel boxes and did not clearly show the decision transition.
- The phrase `genetic exposure layer` could imply MR-style causal exposure terminology.

## Changes Implemented
- The figure title is now `Genetic evidence separates molecular programs from overall psoriasis liability`.
- Panel a now presents a compact prespecified genetic hypothesis.
- Panel b identifies the primary analysis as CORE, MHC-excluded competitive MAGMA gene-set testing and uses an aligned FDR q column.
- Panel c uses `MAGMA gene-set beta` as the x-axis and aligns empirical P values in a dedicated `P_emp` column.
- Panel d was redesigned as a decision fork from prespecified molecular programs through genetic anchoring test to two retained evidence layers.
- Program colors are used only for F1/F2/F6/F7; the inherited-liability pathway uses neutral blue-grey.

## Primary Test Specification
Panel b represents the prespecified primary CORE gene-set analysis using MHC-excluded competitive MAGMA gene-set beta estimates from `results/phase3a/magma_core_MHC_excluded.tsv`. Error bars show beta +/- 1.96 SE, and FDR q values are taken directly from the same source table.

## Matched-null Specification
Panel c represents observed CORE MHC-excluded MAGMA gene-set beta relative to matched random gene-set null summaries from `results/phase3a/matched_null_results.tsv`. Grey intervals show matched-null mean +/- SD, and `P_emp` values are empirical P values from 2,000 matched random sets.

## Panel-d Interpretation
The decision fork shows that the negative genetic result constrained interpretation rather than invalidating the transcriptomic programs. F1/F2/F6/F7 remain molecular tissue-state programs, while downstream comorbidity genetics uses overall psoriasis susceptibility as the inherited-liability layer.

## Publication-ready Legend
Figure 4. Genetic evidence separates molecular programs from overall psoriasis liability. a, F1/F2/F6/F7 molecular programs were defined before genetic analysis and tested for psoriasis genetic enrichment. b, Primary prespecified axis-specific CORE gene-set results from the MHC-excluded competitive MAGMA analysis, showing beta estimates with 95% CI and FDR correction. c, Observed axis statistic relative to matched random gene-set null distributions. Colored points indicate observed MAGMA gene-set beta values, grey intervals indicate matched-null mean +/- SD, and aligned values show empirical P from 2,000 matched random sets. d, No program met the robust prespecified genetic-anchoring criteria. This result constrained their interpretation as tissue-state programs rather than inherited psoriasis subtypes; downstream multisystem genetic analyses therefore used overall psoriasis susceptibility.

## Final Main Claim
Prespecified molecular programs did not meet robust axis-specific genetic anchoring criteria and were therefore retained as tissue-state programs, while overall psoriasis inherited liability formed the basis for downstream multisystem genetic analyses.

## Final Quality Test
| Item | Answer |
|---|---|
| Does the reader understand what genetic hypothesis was tested? | YES |
| Is the primary genetic result identifiable? | YES |
| Is the matched-null analysis visibly a robustness test? | YES |
| Are all four programs treated consistently? | YES |
| Is F2 not post-hoc promoted? | YES |
| Does panel d explain why the project proceeds despite the negative axis result? | YES |
| Are molecular programs visibly retained as biologically meaningful tissue states? | YES |
| Is overall psoriasis liability clearly distinguished from molecular programs? | YES |
| Does the figure avoid implying MR causality? | YES |
| Does it avoid implying complete independence between transcriptomic and genetic biology? | YES |
| Are all values source-traceable? | YES |
| Can the full logic be understood in <10 seconds? | YES |

Final status: FIGURE4_FINAL_READY
