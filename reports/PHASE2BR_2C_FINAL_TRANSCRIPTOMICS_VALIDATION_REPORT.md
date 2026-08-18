# PHASE 2B-R + PHASE 2C Final Transcriptomics Validation Report

## Executive Conclusion

**SHRINK_TO_BULK_MOLECULAR_PROGRAMS_WITH_DIRECTIONAL_CELLULAR_SPATIAL_SUPPORT.** The final transcriptomics validation block strengthens the directional keratinocyte/spatial interpretation for F1/F2/F6 but does not meet the locked threshold for formal mechanism naming. F7 remains systemic/supportive rather than skin-spatial localized.

## What Was Completed

- Accession audit and DATA_MANIFEST correction for GSE228421, GSE173706, GSE225475, and GSE202011.
- Phase 2B-R one-pass GSE228421 marker/reference refinement.
- Phase 2C independent scRNA validation using GSE173706.
- Phase 2C primary spatial localization using GSE225475.
- Phase 2C external spatial robustness using GSE202011 sample-level H5 files.
- Mechanism triangulation and mechanism freeze v2.

## Answers To The Locked Questions

1. F1 is not formally validated as a named mechanism; it has directional keratinocyte inflammatory/stress support.
2. F2 is not formally validated as fibroblast/stromal; it trends toward keratinocyte stress/hypoxia rather than a clean stromal-repair axis.
3. F6 has the most coherent keratinocyte stress/hypoxia spatial support but remains below donor-level single-cell confidence thresholds.
4. F7 is not confirmed as a skin-localized myeloid/IFN axis; retain it as systemic/supportive only.
5. CORE remains primary; EXTENDED is sensitivity only.
6. Donor/section-level inference was preserved; cells/spots were not treated as independent patients.
7. GSE173706 supports directional independent scRNA validation but not formal MODERATE/HIGH mechanism confidence.
8. GSE225475 supports keratinocyte stress/hypoxia spatial localization for F1/F2/F6.
9. GSE202011 independently supports the same keratinocyte stress/hypoxia spatial program.
10. GSE202011 was not used as a single-cell atlas.
11. No GWAS, MR, LDSC, LAVA, colocalization, drug prediction, PPI, hub-gene, or LASSO analyses were run.
12. No frozen gene programs were modified.
13. No additional transcriptomics rescue datasets should be added after this block.
14. Mechanism confidence v2 remains below formal naming threshold for all axes.
15. F1/F2/F6 can be carried forward as frozen bulk molecular axes with directional cellular/spatial support.
16. F7 can be carried forward only as a supportive/systemic candidate.
17. Phase 3 can start only if claim language is shrunk to gene-program genetics rather than validated cell-state mechanisms.

## Triangulation

| axis   | phase2br_gse228421_state      | phase2br_confidence   | gse173706_independent_scrna_state   | gse173706_confidence   | gse225475_primary_spatial_program   |   gse225475_median_spot_spearman | gse202011_external_spatial_program   |   gse202011_median_spot_spearman | single_cell_convergence   | spatial_convergence   | final_name_v2                                               | mechanism_confidence_v2   | freeze_decision                                                   |
|:-------|:------------------------------|:----------------------|:------------------------------------|:-----------------------|:------------------------------------|---------------------------------:|:-------------------------------------|---------------------------------:|:--------------------------|:----------------------|:------------------------------------------------------------|:--------------------------|:------------------------------------------------------------------|
| F1     | keratinocyte_inflammatory_T17 | LOW                   | keratinocyte_inflammatory_T17       | LOW                    | keratinocyte_stress_hypoxia         |                         0.502309 | keratinocyte_stress_hypoxia          |                         0.489475 | yes_directional           | yes_spatial_program   | keratinocyte stress/inflammatory spatial program            | DIRECTIONAL_SUPPORT_ONLY  | retain_as_bulk_axis_with_directional_keratinocyte_spatial_support |
| F2     | keratinocyte_stress_hypoxia   | LOW                   | keratinocyte_stress_hypoxia         | LOW                    | keratinocyte_stress_hypoxia         |                         0.506033 | keratinocyte_stress_hypoxia          |                         0.490773 | yes_directional           | yes_spatial_program   | keratinocyte stress/inflammatory spatial program            | DIRECTIONAL_SUPPORT_ONLY  | retain_as_bulk_axis_with_directional_keratinocyte_spatial_support |
| F6     | keratinocyte_inflammatory_T17 | LOW                   | keratinocyte_stress_hypoxia         | LOW                    | keratinocyte_stress_hypoxia         |                         0.54579  | keratinocyte_stress_hypoxia          |                         0.496115 | yes_directional           | yes_spatial_program   | keratinocyte stress/inflammatory spatial program            | DIRECTIONAL_SUPPORT_ONLY  | retain_as_bulk_axis_with_directional_keratinocyte_spatial_support |
| F7     | B_cell_unresolved             | LOW                   | B_cell_unresolved                   | LOW                    | keratinocyte_basal                  |                         0.504906 | keratinocyte_stress_hypoxia          |                         0.484714 | yes_directional           | partial               | systemic/supportive immune axis; not skin-spatial-localized | LOW                       | retain_as_supportive_systemic_axis_only                           |

## Final Status

SHRINK_TO_BULK_MOLECULAR_PROGRAMS_WITH_DIRECTIONAL_CELLULAR_SPATIAL_SUPPORT
