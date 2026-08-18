# PHASE2A AXIS MECHANISM PRIORITIZATION

# Executive conclusion

CONDITIONAL GO: Phase 2A retains F1, F2, and F6 as skin-primary axes and F7 as a supportive/systemic axis. This supports moving into donor-level single-cell localization, but F1/F2/F7 still require cell-state anchoring before strong mechanism naming.

# Current evidence boundary

The manuscript remains framed as skin-primary continuous molecular axes of psoriasis with selective systemic blood support. Phase 2A does not demonstrate genetics, MR, colocalization, druggability, or multisystem comorbidity mechanisms.

# Axis-by-axis assessment

| factor   | final_name                             | name_confidence   | dominant_tissue   | mechanistic_domain                                   |   seed_stability |   bootstrap_stability |   internal_skin_replication |   external_skin_replication |   blood_support |   PASI_dependence |   BMI_dependence | batch_dependence                             |   feature_family_count |   core_gene_count |   extended_gene_count | single_cell_ready   | genetics_ready   | final_tier   | final_role               |
|:---------|:---------------------------------------|:------------------|:------------------|:-----------------------------------------------------|-----------------:|----------------------:|----------------------------:|----------------------------:|----------------:|------------------:|-----------------:|:---------------------------------------------|-----------------------:|------------------:|----------------------:|:--------------------|:-----------------|:-------------|:-------------------------|
| F1       | F1                                     | LOW               | LS                | metabolic/hypoxia-stress-like lesional skin axis     |                1 |                     1 |                    0.45681  |                    0.688398 |        0.514258 |       3.96964e-05 |      0.0333218   | not_available_not_in_current_covariate_model |                      1 |               304 |                   809 | True                | True             | Tier A       | PRIMARY AXIS             |
| F2       | F2                                     | LOW               | NL                | stromal/repair-remodeling-like nonlesional skin axis |                1 |                     1 |                    0.527544 |                    0.518229 |        0.594313 |       0.00630593  |      0.0472485   | not_available_not_in_current_covariate_model |                      1 |               725 |                  1184 | True                | True             | Tier A       | PRIMARY AXIS             |
| F3       | T17/NF-kB inflammatory-like blood axis | MODERATE          | BLD               | T17/NF-kB inflammatory-like blood axis               |                1 |                     1 |                    0.220623 |                    0.356222 |        0.582392 |       0.0489639   |      0.0930385   | not_available_not_in_current_covariate_model |                      3 |                 0 |                     0 | False               | False            | Tier B       | SECONDARY AXIS           |
| F4       | F4                                     | LOW               | BLD               | DNA-damage/chromatin-like blood factor               |                1 |                     1 |                    0.145683 |                    0.152453 |        0.544689 |       0.00327249  |      0.00481692  | not_available_not_in_current_covariate_model |                      1 |                 0 |                     0 | False               | False            | Tier D       | UNINTERPRETABLE / RETIRE |
| F5       | F5                                     | LOW               | LS                | stromal/repair-remodeling-like lesional skin axis    |                1 |                     1 |                    0.29607  |                    0.35532  |        0.306056 |       0.0247495   |      0.000568129 | not_available_not_in_current_covariate_model |                      2 |                 0 |                     0 | False               | False            | Tier B       | SECONDARY AXIS           |
| F6       | metabolic/hypoxia-stress skin axis     | MODERATE          | LS                | metabolic/hypoxia-stress skin axis                   |                1 |                     1 |                    0.125892 |                    0.375292 |        0.505263 |       0.00245693  |      0.00300386  | not_available_not_in_current_covariate_model |                      3 |               134 |                   544 | True                | True             | Tier A       | PRIMARY AXIS             |
| F7       | F7                                     | LOW               | BLD               | IFN/antiviral-myeloid systemic blood candidate       |                1 |                     1 |                    0.135281 |                    0.203905 |        0.576815 |       0.00765737  |      0.000515541 | not_available_not_in_current_covariate_model |                      1 |               232 |                   507 | True                | True             | Tier C       | SUPPORTIVE/SYSTEMIC AXIS |
| F8       | F8                                     | LOW               | NL                | growth-factor/stromal-remodeling nonlesional axis    |                1 |                     1 |                    0.272942 |                    0.19673  |        0.628626 |       0.00558471  |      0.000718002 | not_available_not_in_current_covariate_model |                      1 |                 0 |                     0 | False               | False            | Tier B       | SECONDARY AXIS           |

# Mechanistic interpretation

| factor   | candidate_domain                                     | name_confidence   | biological_interpretability   | rationale                                                                                                                |
|:---------|:-----------------------------------------------------|:------------------|:------------------------------|:-------------------------------------------------------------------------------------------------------------------------|
| F1       | metabolic/hypoxia-stress-like lesional skin axis     | LOW               | single_family_or_diffuse      | strongest GSE244679 paired-skin support; LS-dominant; descriptive mechanism only until cell localization                 |
| F2       | stromal/repair-remodeling-like nonlesional skin axis | LOW               | single_family_or_diffuse      | strong internal and GSE244679 NL skin support; nonlesional stromal/repair-like candidate                                 |
| F3       | T17/NF-kB inflammatory-like blood axis               | MODERATE          | multifamily                   | interpretable inflammatory blood factor but not selected primary because skin architecture is less central than F1/F2/F6 |
| F4       | DNA-damage/chromatin-like blood factor               | LOW               | single_family_or_diffuse      | robust but weaker replication and single-family/diffuse chromatin signal                                                 |
| F5       | stromal/repair-remodeling-like lesional skin axis    | LOW               | single_family_or_diffuse      | moderate paired-skin support but less complementary after selecting F2/F6                                                |
| F6       | metabolic/hypoxia-stress skin axis                   | MODERATE          | multifamily                   | LS-dominant hypoxia/stress axis with GSE244679 support and multifamily evidence                                          |
| F7       | IFN/antiviral-myeloid systemic blood candidate       | LOW               | single_family_or_diffuse      | blood-dominant systemic candidate with strongest GSE61281 support; not skin-primary                                      |
| F8       | growth-factor/stromal-remodeling nonlesional axis    | LOW               | single_family_or_diffuse      | NL-dominant but weaker external support and diffuse biology                                                              |

# Tissue architecture

| factor   |   variance_explained_LS |   variance_explained_NL |   variance_explained_blood | dominant_tissue   | cross_tissue_coherence   |
|:---------|------------------------:|------------------------:|---------------------------:|:------------------|:-------------------------|
| F1       |             37.9776     |              0.0113785  |                 0.787157   | LS                | skin_dominant            |
| F2       |              0.792247   |             35.355      |                 0.00184774 | NL                | skin_dominant            |
| F3       |              0.371206   |              1.072      |                19.8354     | BLD               | blood_dominant           |
| F4       |              0.0445008  |              0.704551   |                12.5861     | BLD               | blood_dominant           |
| F5       |             10.7937     |              0.00532269 |                 0.0109196  | LS                | skin_dominant            |
| F6       |              8.61971    |              1.97383    |                 0.00235438 | LS                | skin_dominant            |
| F7       |              0.00228286 |              0.00412464 |                 9.65739    | BLD               | blood_dominant           |
| F8       |              0.0108957  |              9.01272    |                 0.00315309 | NL                | skin_dominant            |

# External replication

| factor   |   internal_skin_replication |   external_GSE121212_support |   external_GSE244679_support | external_GSE54456_support_if_available   |
|:---------|----------------------------:|-----------------------------:|-----------------------------:|:-----------------------------------------|
| F1       |                    0.45681  |                    0.0475572 |                     0.688398 | not_analyzed                             |
| F2       |                    0.527544 |                    0.066494  |                     0.518229 | not_analyzed                             |
| F3       |                    0.220623 |                    0.0303549 |                     0.356222 | not_analyzed                             |
| F4       |                    0.145683 |                    0.111063  |                     0.152453 | not_analyzed                             |
| F5       |                    0.29607  |                    0.0385842 |                     0.35532  | not_analyzed                             |
| F6       |                    0.125892 |                    0.0323833 |                     0.375292 | not_analyzed                             |
| F7       |                    0.135281 |                    0.0167272 |                     0.203905 | not_analyzed                             |
| F8       |                    0.272942 |                    0.0646705 |                     0.19673  | not_analyzed                             |

# Blood/systemic support

| factor   |   internal_blood_support |   GSE147339_blood_support |   GSE61281_blood_support |   blood_support_abs_max |
|:---------|-------------------------:|--------------------------:|-------------------------:|------------------------:|
| F1       |                 0.514258 |               -0.048473   |               -0.209164  |                0.514258 |
| F2       |                 0.594313 |                0.00132328 |               -0.258128  |                0.594313 |
| F3       |                 0.582392 |               -0.0517104  |                0.262383  |                0.582392 |
| F4       |                 0.544689 |               -0.173351   |                0.0603955 |                0.544689 |
| F5       |                 0.306056 |               -0.150453   |               -0.0649766 |                0.306056 |
| F6       |                 0.505263 |                0.081723   |               -0.0797162 |                0.505263 |
| F7       |                 0.576815 |                0.0767031  |               -0.454939  |                0.576815 |
| F8       |                 0.628626 |                0.037414   |               -0.184483  |                0.628626 |

# Confounding

| factor   |   PASI_association |   BMI_association |   age_association |   sex_association |   HLA_association | batch_association                            |   max_confounder_partial_r2 |
|:---------|-------------------:|------------------:|------------------:|------------------:|------------------:|:---------------------------------------------|----------------------------:|
| F1       |        3.96964e-05 |       0.0333218   |       0.0139943   |       0.0288303   |       0.00985675  | not_available_not_in_current_covariate_model |                  0.0333218  |
| F2       |        0.00630593  |       0.0472485   |       0.0102412   |       0.00280476  |       0.00487797  | not_available_not_in_current_covariate_model |                  0.0472485  |
| F3       |        0.0489639   |       0.0930385   |       0.000689996 |       0.000477142 |       0.00307582  | not_available_not_in_current_covariate_model |                  0.0930385  |
| F4       |        0.00327249  |       0.00481692  |       0.0667753   |       0.000104002 |       0.0396447   | not_available_not_in_current_covariate_model |                  0.0667753  |
| F5       |        0.0247495   |       0.000568129 |       0.0010904   |       0.00267782  |       0.00351407  | not_available_not_in_current_covariate_model |                  0.0247495  |
| F6       |        0.00245693  |       0.00300386  |       5.26097e-05 |       0.010528    |       0.010758    | not_available_not_in_current_covariate_model |                  0.010758   |
| F7       |        0.00765737  |       0.000515541 |       0.00657253  |       9.48069e-05 |       0.0068486   | not_available_not_in_current_covariate_model |                  0.00765737 |
| F8       |        0.00558471  |       0.000718002 |       0.0149667   |       0.00530658  |       0.000868877 | not_available_not_in_current_covariate_model |                  0.0149667  |

# Redundancy

No retained MOFA factors are automatically merged. Pairwise redundancy is reported to classify broad domains while preserving original F identifiers.

| factor_a   | factor_b   |   patient_score_spearman |   loading_similarity_spearman |   top_pathway_feature_jaccard |   top_feature_overlap_coefficient |   regulon_overlap_count |   cell_state_overlap_count | redundancy_class         |
|:-----------|:-----------|-------------------------:|------------------------------:|------------------------------:|----------------------------------:|------------------------:|---------------------------:|:-------------------------|
| F4         | F7         |              0.123254    |                    0.0677752  |                    0.348315   |                         0.516667  |                      13 |                         11 | same_broad_domain_review |
| F1         | F6         |              0.0290362   |                    0.112356   |                    0.121495   |                         0.216667  |                      13 |                         11 | distinct_or_low_overlap  |
| F3         | F4         |             -0.0259467   |                    0.087819   |                    0.0909091  |                         0.166667  |                      13 |                         11 | distinct_or_low_overlap  |
| F1         | F2         |              0.210417    |                    0.0683291  |                    0.0526316  |                         0.1       |                      13 |                         11 | distinct_or_low_overlap  |
| F1         | F8         |              0.135803    |                    0.0349101  |                    0.0526316  |                         0.1       |                      13 |                         11 | distinct_or_low_overlap  |
| F2         | F5         |             -0.0102802   |                   -0.0464945  |                    0.0344828  |                         0.0666667 |                      13 |                         11 | distinct_or_low_overlap  |
| F7         | F8         |             -0.0412303   |                    0.00349628 |                    0.0344828  |                         0.0666667 |                      13 |                         11 | distinct_or_low_overlap  |
| F2         | F6         |              0.0897608   |                    0.0306988  |                    0.025641   |                         0.05      |                      13 |                         11 | distinct_or_low_overlap  |
| F3         | F6         |              0.0561586   |                    0.0784137  |                    0.025641   |                         0.05      |                      13 |                         11 | distinct_or_low_overlap  |
| F6         | F8         |             -0.0114559   |                    0.0082538  |                    0.0169492  |                         0.0333333 |                      13 |                         11 | distinct_or_low_overlap  |
| F6         | F7         |             -0.000437457 |                    0.0389958  |                    0.0169492  |                         0.0333333 |                      13 |                         11 | distinct_or_low_overlap  |
| F2         | F3         |             -0.0384962   |                   -0.0164542  |                    0.00840336 |                         0.0166667 |                      13 |                         11 | distinct_or_low_overlap  |

# Primary-axis selection

Primary axes: F1, F2, F6. Supportive/systemic axis: F7. Secondary axes: F3, F5, F8. Retire from main story: F4.

| factor   | final_name                         | name_confidence   | dominant_tissue   | mechanistic_domain                                   |   seed_stability |   bootstrap_stability |   internal_skin_replication |   external_skin_replication |   blood_support |   PASI_dependence |   BMI_dependence | batch_dependence                             |   feature_family_count |   core_gene_count |   extended_gene_count | single_cell_ready   | genetics_ready   | final_tier   | final_role               |
|:---------|:-----------------------------------|:------------------|:------------------|:-----------------------------------------------------|-----------------:|----------------------:|----------------------------:|----------------------------:|----------------:|------------------:|-----------------:|:---------------------------------------------|-----------------------:|------------------:|----------------------:|:--------------------|:-----------------|:-------------|:-------------------------|
| F1       | F1                                 | LOW               | LS                | metabolic/hypoxia-stress-like lesional skin axis     |                1 |                     1 |                    0.45681  |                    0.688398 |        0.514258 |       3.96964e-05 |      0.0333218   | not_available_not_in_current_covariate_model |                      1 |               304 |                   809 | True                | True             | Tier A       | PRIMARY AXIS             |
| F2       | F2                                 | LOW               | NL                | stromal/repair-remodeling-like nonlesional skin axis |                1 |                     1 |                    0.527544 |                    0.518229 |        0.594313 |       0.00630593  |      0.0472485   | not_available_not_in_current_covariate_model |                      1 |               725 |                  1184 | True                | True             | Tier A       | PRIMARY AXIS             |
| F6       | metabolic/hypoxia-stress skin axis | MODERATE          | LS                | metabolic/hypoxia-stress skin axis                   |                1 |                     1 |                    0.125892 |                    0.375292 |        0.505263 |       0.00245693  |      0.00300386  | not_available_not_in_current_covariate_model |                      3 |               134 |                   544 | True                | True             | Tier A       | PRIMARY AXIS             |
| F7       | F7                                 | LOW               | BLD               | IFN/antiviral-myeloid systemic blood candidate       |                1 |                     1 |                    0.135281 |                    0.203905 |        0.576815 |       0.00765737  |      0.000515541 | not_available_not_in_current_covariate_model |                      1 |               232 |                   507 | True                | True             | Tier C       | SUPPORTIVE/SYSTEMIC AXIS |

# Frozen gene programs

| factor   |   core_gene_count |   extended_gene_count |
|:---------|------------------:|----------------------:|
| F1       |               304 |                   809 |
| F2       |               725 |                  1184 |
| F6       |               134 |                   544 |
| F7       |               232 |                   507 |

# Single-cell readiness

| factor   |   core_gene_count |   extended_gene_count | core_program_large_enough   | housekeeping_dominance_risk   | likely_scoreable_in_scRNAseq   | expected_cell_type_or_state                                                 | biologically_falsifiable   | single_cell_ready   | phase2b_entry   |
|:---------|------------------:|----------------------:|:----------------------------|:------------------------------|:-------------------------------|:----------------------------------------------------------------------------|:---------------------------|:--------------------|:----------------|
| F1       |               304 |                   809 | True                        | review                        | True                           | keratinocyte/stress or epidermal metabolic state to be tested               | True                       | True                | yes             |
| F2       |               725 |                  1184 | True                        | low_to_moderate               | True                           | fibroblast/endothelial/repair or nonlesional stromal state to be tested     | True                       | True                | yes             |
| F6       |               134 |                   544 | True                        | review                        | True                           | keratinocyte hypoxia/stress or epithelial response state to be tested       | True                       | True                | yes             |
| F7       |               232 |                   507 | True                        | low_to_moderate               | True                           | myeloid/monocyte/neutrophil/IFN-response systemic immune state to be tested | True                       | True                | yes             |

# Spatial readiness

| accession   | data_type   | local_series_matrix                                                                                                   |   n_geo_samples |   estimated_donor_or_patient_count_from_metadata | reported_cell_or_spot_count_from_series_matrix   | sample_title_examples                                                                                                                                                                                                                           | lesional_nonlesional_control_metadata_detected   | treatment_timepoint_metadata_detected   | donor_metadata_detected   | raw_processed_availability                            | suitability_for_patient_level_pseudobulk   | suitability_for_frozen_axis_scoring     | pseudoreplication_risk           |
|:------------|:------------|:----------------------------------------------------------------------------------------------------------------------|----------------:|-------------------------------------------------:|:-------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------|:----------------------------------------|:--------------------------|:------------------------------------------------------|:-------------------------------------------|:----------------------------------------|:---------------------------------|
| GSE202011   | spatial     | /Users/zy/Documents/ChatGPT/银屑病机制论文设计/psoriasis_endotype_comorbidity/data/external/geo/GSE202011_series_matrix.txt.gz |              30 |                                                9 | not_reported_in_series_matrix                    | PSO Lesional Skin Patient 1; PSO Non-Lesional Skin Patient 1; PSO Lesional Skin Patient 2 R1; PSO Lesional Skin Patient 2 R2; PSO Non-Lesional Skin Patient 2; PSA Lesional Patient 2 R1; PSA Lesional Patient 2 R2; PSA Non-Lesional Patient 2 | True                                             | False                                   | True                      | series_matrix_metadata_only_audited_no_large_download | candidate_needs_full_metadata_review       | candidate_if_spot_gene_matrix_available | must_use_donor_as_inference_unit |

# Genetics readiness

| factor   |   core_gene_count | genetics_ready   | final_role               |
|:---------|------------------:|:-----------------|:-------------------------|
| F1       |               304 | True             | PRIMARY AXIS             |
| F2       |               725 | True             | PRIMARY AXIS             |
| F3       |                 0 | False            | SECONDARY AXIS           |
| F4       |                 0 | False            | UNINTERPRETABLE / RETIRE |
| F5       |                 0 | False            | SECONDARY AXIS           |
| F6       |               134 | True             | PRIMARY AXIS             |
| F7       |               232 | True             | SUPPORTIVE/SYSTEMIC AXIS |
| F8       |                 0 | False            | SECONDARY AXIS           |

# Reviewer attack points

- Several axes are Reactome-heavy and should not be overnamed before single-cell localization.
- GSE61281 is cross-platform microarray support, not design-matched blood replication.
- Batch association is not available in the current covariate model.
- F1 and F2 have strong skin replication but low formal naming confidence until cell-state evidence is added.
- Gene programs are frozen from loading-supported feature provenance, but CORE/EXTENDED thresholds require sensitivity checks in Phase 2B/3.

# Phase 2B recommendation

Proceed to donor-level single-cell localization for F1, F2, F6, and F7. Use per-cell scoring only as an intermediate step; inference must be donor-level pseudobulk or donor-level cell-type summaries.

# GO / CONDITIONAL GO / NO-GO

CONDITIONAL GO

# Final decision answers

1. Primary: F1, F2, F6.
2. Secondary: F3, F5, F8.
3. Systemic/supportive only: F7.
4. Retired from main story: F4.
5. Biological names: only F3 and F6 have MODERATE confidence; F1/F2/F7 retain F-number plus descriptive domain until Phase 2B.
6. Convincingly skin-primary: F1, F2, F6.
7. Meaningful systemic/blood support: F7, with weaker support for F3/F2.
8. No retained primary axis is dominated by PASI/BMI/HLA/age/sex under current partial R2; batch unavailable.
9. No axes are automatically merged; redundancy is tracked as broad-domain overlap.
10. Frozen CORE programs are in `results/phase2a/axis_gene_programs/`.
11. Enter single-cell validation: F1, F2, F6, F7.
12. Eventually enter GWAS anchoring: F1, F2, F6, F7 after Phase 2B localization and gene-program overlap checks.
13. Future target framing remains plausible but unproven: genetically anchored molecular axes of psoriasis may reveal distinct multisystem comorbidity architectures. This has not yet been demonstrated.

# Candidate single-cell dataset audit

| accession   | data_type   | local_series_matrix                                                                                                   |   n_geo_samples |   estimated_donor_or_patient_count_from_metadata | reported_cell_or_spot_count_from_series_matrix   | sample_title_examples                                                                                                                  | lesional_nonlesional_control_metadata_detected   | treatment_timepoint_metadata_detected   | donor_metadata_detected   | raw_processed_availability                            | suitability_for_patient_level_pseudobulk   | suitability_for_frozen_axis_scoring           | pseudoreplication_risk           |
|:------------|:------------|:----------------------------------------------------------------------------------------------------------------------|----------------:|-------------------------------------------------:|:-------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------|:----------------------------------------|:--------------------------|:------------------------------------------------------|:-------------------------------------------|:----------------------------------------------|:---------------------------------|
| GSE228421   | single-cell | /Users/zy/Documents/ChatGPT/银屑病机制论文设计/psoriasis_endotype_comorbidity/data/external/geo/GSE228421_series_matrix.txt.gz |              20 |                                                5 | not_reported_in_series_matrix                    | P1-V1 Lesional; P1-V1 Non Lesional; P1-V2 Lesional; P1-V3 Lesional; P2-V1 Lesional; P2-V1 Non Lesional; P2-V2 Lesional; P2-V3 Lesional | True                                             | True                                    | True                      | series_matrix_metadata_only_audited_no_large_download | candidate_needs_full_metadata_review       | candidate_if_gene_expression_matrix_available | must_use_donor_as_inference_unit |
