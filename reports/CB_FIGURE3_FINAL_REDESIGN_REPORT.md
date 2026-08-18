# Figure 3 Final Redesign Report

## Previous Weaknesses
- Panel a was titled as localization even though it displayed donor-level LS-NL directional effects by cell type.
- Panel a annotated every heatmap cell, causing near-zero values to dominate the visual field.
- Panel c used a heatmap for tightly clustered rho values and did not define the statistic precisely.
- Panel d used an ordered spot-level gradient despite recoverable Visium coordinates.

## Source-data Audit
- Single-cell panel source: `results/phase2b/GSE228421_baseline_LS_vs_NL_donor_statistics.tsv`.
- Donor-level summary source: `results/phase2b/Table_phase2b_axis_cell_localization.tsv`.
- Spatial concordance sources: `results/phase2c/GSE225475_spatial_axis_localization.tsv` and `results/phase2c/GSE202011_spatial_axis_localization.tsv`.
- Panel-d spot scores came from `results/phase2c/GSE225475_spot_axis_scores.tsv.gz`; coordinates came from `data/external/geo/GSE225475_visium/PP1/spatial/tissue_positions_list.csv`.

## Panel a Changes
- The title was changed to `Cell-type-specific lesional-non-lesional program shifts`.
- The color scale is diverging and centered at zero.
- Numeric labels are display-only and shown only for absolute effects >= 0.03.
- A row outline marks the strongest absolute directional shift per program without using significance stars.

## Panel b Interval Audit
The source table contains `bootstrap_ci_low` and `bootstrap_ci_high`; panel b reports donor-level LS-NL effects with 95% bootstrap CI. The x-axis is shared across F1/F2/F6/F7 and preserves the wider F7 interval.

## Panel c Rho-definition Audit
Panel c displays median spot-level program-marker Spearman rho. These are spatial-context concordance summaries across samples and are not interpreted as cell-state mechanisms or causal localization. F7 remains systemic/supportive despite positive spatial rho.

## Panel d Representative-sample Rule
The representative GSE225475 psoriasis sample is selected as the sample closest to the median mean absolute correlation between F1/F2/F6 CORE scores and the keratinocyte-stress marker. The selected sample is `PP1`. Real spot coordinates matched 100.0% of displayed spots through `spot_barcode`.

## Panels Moved To Supplementary
The previous ordered spot-level heatmap is no longer used in the main figure. It can be retained as a supplementary contextual gradient if needed.

## Claim-boundary Audit
The figure supports directional cellular and spatial contextualization of retained molecular programs. It does not claim definitive cell-state mechanisms, genetic endotypes, cell-level independent inference or causality.

## Remaining Limitations
Panel d uses spatial geometry without histology image overlay. Separate display scales are used for the reference marker and F1/F2/F6 because these raw program scores are not assumed to be directly comparable across variables.

## Final Quality Test
| Item | Answer |
|---|---|
| Does Figure 3 visibly contain both cellular and spatial evidence? | YES |
| Is panel a described as an effect rather than localization? | YES |
| Is donor-level inference obvious? | YES |
| Is F7 uncertainty preserved? | YES |
| Is the meaning of spatial rho unambiguous? | YES |
| Can the reader understand why positive F7 rho does not equal a coherent skin-spatial immune axis? | YES |
| Does panel d show actual tissue coordinates if those data already exist? | YES |
| Was the representative sample selected without cherry-picking? | YES |
| Are F1/F2/F6 presented as contextual tissue programs rather than definitive mechanisms? | YES |
| Is F7 still described as systemic/supportive? | YES |
| Are all numeric values traceable? | YES |
| Is the figure readable at normal manuscript size? | YES |

Final status: FIGURE3_FINAL_READY
