# PHASE 2C GSE225475 Primary Spatial Localization

## 结论

GSE225475 primary spatial localization completed as supportive spatial co-localization. The dataset has 2 healthy and 4 psoriasis sections without LS/NL pairing, so it cannot provide donor-level paired inference. It is used to test whether frozen axis scores co-vary across Visium spots with predefined spatial marker programs.

## 数据概况

- Sections: 6
- Spots scored: 7570
- Groups: {'PsO': 4, 'Healthy': 2}

## Dominant Spatial Programs

| axis   | dominant_spatial_program    |   median_spot_spearman |     mean |   count |
|:-------|:----------------------------|-----------------------:|---------:|--------:|
| F1     | keratinocyte_stress_hypoxia |               0.502309 | 0.514692 |       6 |
| F2     | keratinocyte_stress_hypoxia |               0.506033 | 0.499581 |       6 |
| F6     | keratinocyte_stress_hypoxia |               0.54579  | 0.555454 |       6 |
| F7     | keratinocyte_basal          |               0.504906 | 0.544217 |       6 |

## Section-Level Psoriasis-vs-Healthy Axis Scores

| axis   | program_type   |   n_psoriasis_sections |   n_healthy_sections |   mean_psoriasis_minus_healthy |   mannwhitney_p |
|:-------|:---------------|-----------------------:|---------------------:|-------------------------------:|----------------:|
| F1     | CORE           |                      4 |                    2 |                      0.0211312 |        0.533333 |
| F1     | EXTENDED       |                      4 |                    2 |                      0.0288623 |        0.8      |
| F2     | CORE           |                      4 |                    2 |                      0.0347888 |        1        |
| F2     | EXTENDED       |                      4 |                    2 |                      0.0211175 |        1        |
| F6     | CORE           |                      4 |                    2 |                      0.0981898 |        0.133333 |
| F6     | EXTENDED       |                      4 |                    2 |                      0.077116  |        0.133333 |
| F7     | CORE           |                      4 |                    2 |                     -0.076875  |        0.8      |
| F7     | EXTENDED       |                      4 |                    2 |                     -0.014508  |        0.8      |

## Sample Scores

| sample_accession   | sample_name   | disease_group   | tissue_state          |   F1_CORE |   F1_EXTENDED |   F2_CORE |   F2_EXTENDED |   F6_CORE |   F6_EXTENDED |   F7_CORE |   F7_EXTENDED |
|:-------------------|:--------------|:----------------|:----------------------|----------:|--------------:|----------:|--------------:|----------:|--------------:|----------:|--------------:|
| GSM7049132         | NS1           | Healthy         | healthy               |  0.300545 |      0.237038 |  0.184317 |      0.214345 |  0.337806 |      0.284972 |  0.937696 |      0.540724 |
| GSM7049133         | NS2           | Healthy         | healthy               |  0.32225  |      0.249625 |  0.176674 |      0.204702 |  0.350914 |      0.304848 |  1.04012  |      0.598463 |
| GSM7049134         | PP1           | PsO             | psoriasis_unqualified |  0.348557 |      0.261734 |  0.19576  |      0.219254 |  0.42121  |      0.358127 |  1.1268   |      0.652263 |
| GSM7049135         | PP2           | PsO             | psoriasis_unqualified |  0.31006  |      0.238328 |  0.169384 |      0.192193 |  0.374696 |      0.328735 |  1.08644  |      0.617967 |
| GSM7049136         | PP3           | PsO             | psoriasis_unqualified |  0.311901 |      0.224936 |  0.152341 |      0.173368 |  0.372534 |      0.329397 |  0.969303 |      0.566295 |
| GSM7049137         | PP4           | PsO             | psoriasis_unqualified |  0.359598 |      0.363777 |  0.343652 |      0.337749 |  0.60176  |      0.471845 |  0.465589 |      0.383814 |

## Boundary

This dataset supports spatial localization only. Because donor IDs and LS/NL labels are not recoverable from GEO sample metadata, no patient-level paired spatial claim is made.
