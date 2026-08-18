# Figure 3 Spatial Metric Audit

## Source Tables
- `results/phase2c/GSE225475_spatial_axis_localization.tsv`
- `results/phase2c/GSE202011_spatial_axis_localization.tsv`
- Spot-level source tables: `results/phase2c/GSE225475_spot_axis_scores.tsv.gz` and `results/phase2c/GSE202011_spot_axis_scores.tsv.gz`

## Metric Definition
Panel c displays `median_spot_spearman`. The source correlation files define the underlying statistic as `spot_spearman`, calculated per spatial sample between a frozen CORE program score and a spatial marker program across spots within that sample. The panel-level value is the median across samples for the dominant spatial marker program reported in each dataset.

## Unit Of Analysis
The correlation is a within-sample spot-level concordance statistic summarized across spatial samples. It is used as spatial contextual evidence, not as donor-level causal or mechanistic localization evidence.

## Displayed Target
The x-axis is labeled `Median spot-level program-marker correlation (rho)`. GSE225475 uses 6 spatial samples and GSE202011 uses 30 spatial samples according to the source tables. F7 has a positive spot-level rho but is retained as systemic/supportive because the broader evidence does not establish a coherent skin-localized immune program.

## Panel D Coordinate Audit
GSE225475 has real Visium coordinates in `data/external/geo/GSE225475_visium/<sample>/spatial/tissue_positions_list.csv`. Coordinates were matched to panel-d spot scores through `spot_barcode`, not the sample-prefixed `spot_id`. The selected sample `PP1` had 100.0% matched in-tissue spots.
