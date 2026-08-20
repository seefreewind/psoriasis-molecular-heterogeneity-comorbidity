# CORE/EXTENDED source-feature rule audit

Authoritative script: `src/integration/phase2a_strict_axis_freeze.py`.

The function `top_features(loadings, factor, n=30)` first subsets by factor, computes absolute loading across all rows retained for that factor, sorts the combined loading table and selects the first 30 rows. It does not group by view before selection. The correct publication wording is therefore **top 30 features per factor across all views**, not top 30 per factor per view.

| Axis   | Actual_source_feature_rule                  |   Number_source_features | Views_represented   | Feature_families_represented                        | Effect_on_program_construction                                                                                                   |
|:-------|:--------------------------------------------|-------------------------:|:--------------------|:----------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------|
| F1     | top 30 features per factor across all views |                       30 | LS                  | Reactome                                            | Genes were mapped from this factor-level top-feature set; CORE/EXTENDED membership was not selected separately within each view. |
| F2     | top 30 features per factor across all views |                       30 | NL                  | Reactome                                            | Genes were mapped from this factor-level top-feature set; CORE/EXTENDED membership was not selected separately within each view. |
| F6     | top 30 features per factor across all views |                       30 | LS                  | Hallmark;Reactome;regulon_DoRothEA                  | Genes were mapped from this factor-level top-feature set; CORE/EXTENDED membership was not selected separately within each view. |
| F7     | top 30 features per factor across all views |                       30 | BLD                 | Reactome;pathway;regulon_DoRothEA;signaling_PROGENy | Genes were mapped from this factor-level top-feature set; CORE/EXTENDED membership was not selected separately within each view. |
