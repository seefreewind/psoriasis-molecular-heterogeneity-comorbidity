# Figure 5 Final Redesign Report

## Previous Strengths
- Strong global-to-local narrative.
- Clear LDSC forest plot.
- Effective local-rho heatmap.

## Previous Weaknesses
- Panel-b circles were visually ambiguous.
- Nominal and FDR-supported local-count semantics were not sufficiently explicit.
- Panel-c blank cells could be confused with zero-valued rho.
- The locus selection/display rule was not sufficiently visible.
- Crohn/UC global negative estimates could invite an over-simple protective interpretation.

## Changes Implemented
- Added the title `Genome-wide and local shared genetic architecture of psoriasis comorbidity`.
- Standardized panel-a QC annotations into an aligned column with `QC pass`, `QC flag` and `near-neighbor / QC flag`.
- Removed ambiguous panel-b circles and added an aligned FDR-supported count column.
- Defined panel-b bars as nominal local-rg signal counts.
- Re-encoded panel-c non-displayed cells as uniform neutral grey.
- Displayed numeric local rho only for cells meeting the predefined robust display criterion.
- Added a short IBD heterogeneity annotation without labeling Crohn/UC as protective or inverse.

## Panel-b Definition
Panel b uses `results/phase4b_restricted_lava/phase4b_restricted_lava_summary.tsv`. Leftward bars show the number of nominal negative local-rg signals; rightward bars show the number of nominal positive local-rg signals. The aligned column reports `fdr05_all_tests`, the count of local-rg loci with all-tests FDR < 0.05.

## Panel-c Selection Rule
Panel c starts from the existing selected locus set used in the prior Figure 5 code: 347, 1215, 1841, 57, 887, 908, 1041, 1082, 2251, 1559, 2203 and 113. A locus-trait cell is displayed with color and numeric local rho only when it is present in this selected set, has all-tests FDR < 0.05 in the restricted LAVA result, and is Phase 4B-R Tier 1 or Tier 2 in the LD-reference validation table. Cells not meeting that rule are shown in uniform grey and should not be interpreted as rho = 0.

## PsA rg Greater Than 1 Interpretation
PsA is displayed as analyzed and is not clipped. The legend should state that PsA is a near-neighbor positive-control phenotype and that rg > 1 is interpreted in the context of elevated cross-trait intercept, potential sample overlap or near-identical liability, not as a literal biological correlation greater than 1.

## Publication-ready Legend
Figure 5. Genome-wide and local shared genetic architecture of psoriasis comorbidity. a, LDSC genome-wide genetic correlation between overall psoriasis susceptibility and six comorbidity outcomes. Points show rg estimates and horizontal intervals show 95% CI; aligned labels summarize QC interpretation. Psoriatic arthritis is shown as a near-neighbor positive-control phenotype, and its rg estimate greater than 1 should be interpreted in light of elevated cross-trait intercept and overlap or near-identical-liability concerns rather than as a literal correlation above 1. b, Directional balance of LAVA local-rg results for CAD, PsA, Crohn disease and UC. Bars show nominal negative and positive local-rg counts; the aligned column reports the number of all-tests FDR-supported local-rg loci. c, Local genetic correlation at selected robust loci. Heatmap color encodes local ρ on a diverging scale centered at zero, and numeric labels are shown only for locus-trait cells meeting the predefined robust display criterion. Grey cells indicate that the selected locus-trait pair did not meet the robust display criterion and do not represent ρ = 0. Crohn disease and UC are interpreted as showing directionally heterogeneous local sharing; their genome-wide negative estimates remain QC-sensitive.

## Final Main Claim
Overall psoriasis susceptibility shows disease-specific shared genetic architecture, with robust positive CAD sharing, strong PsA positive-control architecture and directionally heterogeneous local sharing with inflammatory bowel disease.

## Final Quality Test
| Item | Answer |
|---|---|
| Is the genome-wide result immediately readable? | YES |
| Is CAD visually recognizable as the cleanest non-neighbour signal? | YES |
| Is PsA clearly treated as a near-neighbour positive control? | YES |
| Is rg >1 handled transparently? | YES |
| Is panel b's statistical definition unambiguous? | YES |
| Are positive and negative local directions visually balanced? | YES |
| Is Crohn visibly negative-dominant but mixed? | YES |
| Is UC visibly heterogeneous? | YES |
| Is the local-rho heatmap selection rule reproducible? | YES |
| Can blank cells not be confused with rho=0? | YES |
| Are IBD results prevented from being interpreted as protective? | YES |
| Are all numeric values source-traceable? | YES |
| Is the figure readable at realistic manuscript scale? | YES |

Final status: FIGURE5_FINAL_READY
