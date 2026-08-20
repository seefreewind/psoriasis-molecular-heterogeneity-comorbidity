# GSE173706 method coverage audit

Main-manuscript use detected: YES

GSE173706 remains cited as an independent single-cell sensitivity dataset in the current main manuscript and Figure 3. Supplementary Methods v5 therefore includes a dedicated subsection.

Coverage summary:

| Item | Status |
|---|---|
| Accession | GSE173706 |
| Samples | 33 samples |
| Donors | 23 donors |
| Disease groups | {'PsO': 25, 'Healthy': 8} |
| Tissue states | {'lesional': 14, 'nonlesional': 11, 'healthy': 8} |
| Sequencing/preprocessing source | 10X Chromium; NovaSeq 6000; Cell Ranger mkfastq/count/aggr v4.0.0 against hg38, from GEO metadata |
| Program scoring | mean log1p(CP10K) CORE/EXTENDED gene-program expression |
| Annotation | marker-panel coarse cell-type and refined state assignment from archived script |
| Statistical unit | donor/sample summarized signal, not cells as independent observations |
| Outcome used as sensitivity evidence | direction and localization consistency with primary single-cell contextualization |

Dominant sensitivity rows:

| axis   | dominant_refined_state_paired   | parent_cell_type   | score_localization    |   n_paired_donors |   paired_LS_minus_NL |   paired_ci_low |   paired_ci_high |   paired_fdr | lesional_vs_healthy_top_state   |   lesional_vs_healthy_effect |   core_extended_spearman | independent_scrna_confidence   |
|:-------|:--------------------------------|:-------------------|:----------------------|------------------:|---------------------:|----------------:|-----------------:|-------------:|:--------------------------------|-----------------------------:|-------------------------:|:-------------------------------|
| F1     | keratinocyte_inflammatory_T17   | keratinocyte       | melanocyte_unresolved |                10 |            0.0647195 |       0.0213119 |        0.10989   |     0.278363 | keratinocyte_inflammatory_T17   |                    0.0839643 |                 0.953799 | LOW                            |
| F2     | keratinocyte_stress_hypoxia     | keratinocyte       | melanocyte_unresolved |                 8 |            0.0372059 |       0.0100311 |        0.0658886 |     0.312439 | keratinocyte_inflammatory_T17   |                    0.050746  |                 0.982464 | LOW                            |
| F6     | keratinocyte_stress_hypoxia     | keratinocyte       | melanocyte_unresolved |                 8 |            0.0935218 |       0.0173958 |        0.169671  |     0.312439 | keratinocyte_inflammatory_T17   |                    0.111487  |                 0.9634   | LOW                            |
| F7     | B_cell_unresolved               | B_cell             | keratinocyte_basal    |                 9 |            0.128239  |      -0.0114021 |        0.328622  |     0.622222 | dendritic_LAMP3_CCR7            |                    0.470784  |                 0.943936 | LOW                            |
