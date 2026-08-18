# Figure 3 Representative Sample Audit

Panel d uses a pre-specified representative rule: among psoriasis GSE225475 samples, calculate the mean absolute Spearman correlation of F1_CORE, F2_CORE and F6_CORE with `marker_keratinocyte_stress_hypoxia`; choose the sample closest to the median of that statistic, with sample name as the deterministic tie-breaker.

| sample_name   |   mean_abs_corr |   n_spots |   abs_distance_to_median |
|:--------------|----------------:|----------:|-------------------------:|
| PP1           |        0.501147 |      1352 |                0.0164076 |
| PP2           |        0.468332 |      1393 |                0.0164076 |
| PP3           |        0.648946 |      1463 |                0.164207  |
| PP4           |        0.427914 |      1118 |                0.0568258 |

Selected sample: `PP1`. Coordinate match rate: 100.0%.
