# Spatial ρ Definition Audit

| dataset | program | unit | x_variable | y_variable | correlation_type | aggregation | reported_value | source_file |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE225475 | F1 | spatial sample/spot | prespecified CORE F1 spot score | keratinocyte_stress_hypoxia marker program | Spearman | median across 6 samples | 0.502 | results/phase2c/GSE225475_spatial_axis_localization.tsv |
| GSE225475 | F2 | spatial sample/spot | prespecified CORE F2 spot score | keratinocyte_stress_hypoxia marker program | Spearman | median across 6 samples | 0.506 | results/phase2c/GSE225475_spatial_axis_localization.tsv |
| GSE225475 | F6 | spatial sample/spot | prespecified CORE F6 spot score | keratinocyte_stress_hypoxia marker program | Spearman | median across 6 samples | 0.546 | results/phase2c/GSE225475_spatial_axis_localization.tsv |
| GSE225475 | F7 | spatial sample/spot | prespecified CORE F7 spot score | keratinocyte_basal marker program | Spearman | median across 6 samples | 0.505 | results/phase2c/GSE225475_spatial_axis_localization.tsv |
| GSE202011 | F1 | spatial sample/spot | prespecified CORE F1 spot score | keratinocyte_stress_hypoxia marker program | Spearman | median across 30 samples | 0.489 | results/phase2c/GSE202011_spatial_axis_localization.tsv |
| GSE202011 | F2 | spatial sample/spot | prespecified CORE F2 spot score | keratinocyte_stress_hypoxia marker program | Spearman | median across 30 samples | 0.491 | results/phase2c/GSE202011_spatial_axis_localization.tsv |
| GSE202011 | F6 | spatial sample/spot | prespecified CORE F6 spot score | keratinocyte_stress_hypoxia marker program | Spearman | median across 30 samples | 0.496 | results/phase2c/GSE202011_spatial_axis_localization.tsv |
| GSE202011 | F7 | spatial sample/spot | prespecified CORE F7 spot score | keratinocyte_stress_hypoxia marker program | Spearman | median across 30 samples | 0.485 | results/phase2c/GSE202011_spatial_axis_localization.tsv |

Conclusion: v9 defines spatial ρ consistently in Results, Methods, Table 2 and Figure 3 legend. F7 positive ρ is treated as spatial-context concordance, not coherent skin-localized immune identity.
