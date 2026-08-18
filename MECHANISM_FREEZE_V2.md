# MECHANISM FREEZE V2

Final Phase 2B-R/2C status: **SHRINK_TO_BULK_MOLECULAR_PROGRAMS_WITH_DIRECTIONAL_CELLULAR_SPATIAL_SUPPORT**.

Phase 2B-R and Phase 2C completed the final transcriptomics rescue attempt. No additional bulk RNA-seq, scRNA-seq, or spatial transcriptomics datasets should be introduced solely to rescue weak mechanism naming.

## Frozen Interpretation

- F1, F2, and F6 remain frozen skin-primary bulk molecular axes with directional keratinocyte/spatial support.
- Across GSE228421 refinement and GSE173706 independent scRNA, F1/F2/F6 repeatedly point toward keratinocyte stress/inflammatory states, but donor-level FDR criteria remain unmet.
- Across GSE225475 and GSE202011, F1/F2/F6 consistently co-localize most strongly with keratinocyte stress/hypoxia spatial programs.
- F7 remains a systemic/supportive axis. Current skin scRNA/spatial evidence does not justify naming it as a skin-localized immune spatial mechanism.

## Genetics Entry Decision

Do not enter Phase 3 under a claim of validated cell-state mechanisms. Phase 3 may proceed only as axis-gene-program genetics for frozen bulk molecular programs, with cellular/spatial findings described as directional support. GWAS, MR, LDSC, LAVA, and colocalization must not be used to rename axes or revise gene membership.

## Triangulation Table

| axis   | phase2br_gse228421_state      | phase2br_confidence   | gse173706_independent_scrna_state   | gse173706_confidence   | gse225475_primary_spatial_program   |   gse225475_median_spot_spearman | gse202011_external_spatial_program   |   gse202011_median_spot_spearman | single_cell_convergence   | spatial_convergence   | final_name_v2                                               | mechanism_confidence_v2   | freeze_decision                                                   |
|:-------|:------------------------------|:----------------------|:------------------------------------|:-----------------------|:------------------------------------|---------------------------------:|:-------------------------------------|---------------------------------:|:--------------------------|:----------------------|:------------------------------------------------------------|:--------------------------|:------------------------------------------------------------------|
| F1     | keratinocyte_inflammatory_T17 | LOW                   | keratinocyte_inflammatory_T17       | LOW                    | keratinocyte_stress_hypoxia         |                         0.502309 | keratinocyte_stress_hypoxia          |                         0.489475 | yes_directional           | yes_spatial_program   | keratinocyte stress/inflammatory spatial program            | DIRECTIONAL_SUPPORT_ONLY  | retain_as_bulk_axis_with_directional_keratinocyte_spatial_support |
| F2     | keratinocyte_stress_hypoxia   | LOW                   | keratinocyte_stress_hypoxia         | LOW                    | keratinocyte_stress_hypoxia         |                         0.506033 | keratinocyte_stress_hypoxia          |                         0.490773 | yes_directional           | yes_spatial_program   | keratinocyte stress/inflammatory spatial program            | DIRECTIONAL_SUPPORT_ONLY  | retain_as_bulk_axis_with_directional_keratinocyte_spatial_support |
| F6     | keratinocyte_inflammatory_T17 | LOW                   | keratinocyte_stress_hypoxia         | LOW                    | keratinocyte_stress_hypoxia         |                         0.54579  | keratinocyte_stress_hypoxia          |                         0.496115 | yes_directional           | yes_spatial_program   | keratinocyte stress/inflammatory spatial program            | DIRECTIONAL_SUPPORT_ONLY  | retain_as_bulk_axis_with_directional_keratinocyte_spatial_support |
| F7     | B_cell_unresolved             | LOW                   | B_cell_unresolved                   | LOW                    | keratinocyte_basal                  |                         0.504906 | keratinocyte_stress_hypoxia          |                         0.484714 | yes_directional           | partial               | systemic/supportive immune axis; not skin-spatial-localized | LOW                       | retain_as_supportive_systemic_axis_only                           |
