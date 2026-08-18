# PHASE 2C GSE202011 External Spatial Robustness

## 结论

GSE202011 was analyzed as an external spatial robustness dataset using sample-level H5 files. It is not used as a single-cell atlas. Section/spot analyses are interpreted as spatial support, not patient-level replication.

## 数据概况

- Sections: 30
- Spots scored: 24227
- Disease groups: {'PsO': 12, 'PsA': 11, 'Healthy': 7}
- Tissue states: {'lesional': 14, 'nonlesional': 9, 'healthy': 7}

## Dominant Spatial Programs

| axis   | dominant_spatial_program    |   median_spot_spearman |     mean |   count |
|:-------|:----------------------------|-----------------------:|---------:|--------:|
| F1     | keratinocyte_stress_hypoxia |               0.489475 | 0.493232 |      30 |
| F2     | keratinocyte_stress_hypoxia |               0.490773 | 0.503634 |      30 |
| F6     | keratinocyte_stress_hypoxia |               0.496115 | 0.510263 |      30 |
| F7     | keratinocyte_stress_hypoxia |               0.484714 | 0.486853 |      30 |

## Lesional-vs-Nonlesional Section-Level Support

| axis   | program_type   | disease_group   |   n_lesional_sections |   n_nonlesional_sections |   mean_lesional_minus_nonlesional |   mannwhitney_p |   fdr_by_program_type |
|:-------|:---------------|:----------------|----------------------:|-------------------------:|----------------------------------:|----------------:|----------------------:|
| F1     | CORE           | PsO             |                     7 |                        5 |                         0.0579978 |      0.030303   |             0.0808081 |
| F1     | CORE           | PsA             |                     7 |                        4 |                         0.0153487 |      0.787879   |             0.787879  |
| F1     | EXTENDED       | PsO             |                     7 |                        5 |                         0.0544103 |      0.0176768  |             0.0606061 |
| F1     | EXTENDED       | PsA             |                     7 |                        4 |                         0.0199111 |      0.412121   |             0.549495  |
| F2     | CORE           | PsO             |                     7 |                        5 |                         0.0455163 |      0.0176768  |             0.0707071 |
| F2     | CORE           | PsA             |                     7 |                        4 |                         0.0177108 |      0.527273   |             0.602597  |
| F2     | EXTENDED       | PsO             |                     7 |                        5 |                         0.0407142 |      0.030303   |             0.0606061 |
| F2     | EXTENDED       | PsA             |                     7 |                        4 |                         0.0134188 |      0.648485   |             0.648485  |
| F6     | CORE           | PsO             |                     7 |                        5 |                         0.113119  |      0.00252525 |             0.020202  |
| F6     | CORE           | PsA             |                     7 |                        4 |                         0.0554921 |      0.315152   |             0.504242  |
| F6     | EXTENDED       | PsO             |                     7 |                        5 |                         0.0923697 |      0.00505051 |             0.040404  |
| F6     | EXTENDED       | PsA             |                     7 |                        4 |                         0.0427022 |      0.412121   |             0.549495  |
| F7     | CORE           | PsO             |                     7 |                        5 |                         0.243891  |      0.0732323  |             0.146465  |
| F7     | CORE           | PsA             |                     7 |                        4 |                         0.0898634 |      0.527273   |             0.602597  |
| F7     | EXTENDED       | PsO             |                     7 |                        5 |                         0.150678  |      0.030303   |             0.0606061 |
| F7     | EXTENDED       | PsA             |                     7 |                        4 |                         0.0604107 |      0.527273   |             0.602597  |

## Boundary

The local `GSE202011_RAW.tar.incomplete` file was not used. All expression scoring used sample-level GEO H5 files audited in Phase 2C.
