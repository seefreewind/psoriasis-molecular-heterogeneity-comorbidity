# Figure 2 Final Redesign Report

## Previous Weaknesses
- Panel b used an ambiguous `View R²` label even though displayed values exceeded the 0-1 range of raw R².
- Tissue/view colors overlapped visually with the program palette used for F1/F2/F6/F7.
- The evidence matrix used dense colored cells, making evidence strength harder to read.
- Replication values were displayed as heavy bars.
- Panel c could encourage effect-size ordering rather than the manuscript-wide F1/F2/F6 order.
- Panel d used oversized role boxes.
- The genetic-anchoring column partially duplicated the later Figure 4 hypothesis-test result.

## Changes Implemented
- Panel a was retained as the largest evidence summary but converted to a neutral symbol-coded matrix.
- The genetic-anchoring column was removed from Figure 2 so the genetics boundary remains a Figure 4 result.
- Panel b was converted from grouped tissue-colored bars to a neutral contribution heatmap.
- Panel b now uses the audited label `View contribution, R² (%)`.
- Panel c was converted to a lollipop plot in fixed F1/F2/F6 order.
- Panel d was compressed into a four-row role card with conservative wording.
- Program colors are reserved for F1/F2/F6/F7 row labels, chips and replication points.

## Panel-b Decision
Contribution heatmap was selected over grouped bars because the source statistic is a non-directional contribution measure and the heatmap makes dominant tissue/view structure visible while avoiding a tissue/program color conflict.

## Genetic-anchoring-column Decision
The genetic-anchoring column was removed from Figure 2. Figure 2 now focuses on molecular evidence, tissue contribution, independent paired-skin replication and conservative program interpretation; the axis-specific genetic anchoring test is left to Figure 4.

## Systemic-support Wording
- F1/F2/F6 are labeled as `supportive` in the systemic-support column because the frozen evidence matrix contains internal blood/cross-tissue support but these programs remain skin-primary.
- F7 is labeled as `systemic candidate` because it is blood-dominant and has the strongest systemic-supportive designation in the frozen evidence matrix.

## Publication-ready Legend
Figure 2. Reproducible molecular programs retained after the discrete representation did not meet the prespecified stability criterion. a, Evidence summary for the four retained programs. Symbols encode evidence strength or support category, while row labels use the manuscript-wide program colors. Genetic anchoring is not shown in this figure because it is evaluated separately in Figure 4. b, Relative contribution of lesional skin, non-lesional skin and blood views to each program, displayed directly from the source `*_view_r2` variables as view contribution, R² (%). c, Independent paired-skin replication in GSE244679, shown as absolute Spearman correlation between projected program loading and paired lesional-minus-adjacent skin contrast. Values were F1 |rho| = 0.688, F2 |rho| = 0.518 and F6 |rho| = 0.375. d, Conservative manuscript-level interpretation of the retained molecular programs. F1, F2 and F6 are skin-primary molecular programs with independent paired-skin support, whereas F7 remains a systemic-supportive candidate; these programs are not presented as genetically anchored endotypes.

## Final Main Claim
F1, F2 and F6 represent reproducible skin-primary molecular programs with independent paired-skin support, whereas F7 remains a systemic-supportive candidate.

## Final Quality Test
| Item | Answer |
|---|---|
| Can F1/F2/F6/F7 be understood without Table 2? | YES |
| Is the panel-b statistic labeled correctly? | YES |
| Are tissue and program color semantics distinct? | YES |
| Is the program order consistent throughout? | YES |
| Is independent replication visually obvious? | YES |
| Is F7 clearly differentiated from F1/F2/F6? | YES |
| Does F2 remain conservatively described? | YES |
| Does F6 remain conservatively described? | YES |
| Does Figure 2 avoid prematurely duplicating Figure 4? | YES |
| Is the figure readable at realistic manuscript scale? | YES |
| Does every displayed number trace to source data? | YES |
| Is the overall figure less dense than the current version? | YES |
