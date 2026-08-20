# Methods Reproducibility Gap Audit

| Analysis block | Essential element | Location | Severity |
| --- | --- | --- | --- |
| Discrete clustering | k tested, bootstrap unit, Jaccard value, 0.75 threshold | MAIN_METHODS; Results; Figure 1 legend | PASS |
| Discrete clustering | exact clustering algorithm and bootstrap repetition count | SUPPLEMENTARY_METHODS/analysis scripts | MAJOR if not expanded in SI |
| Continuous modeling | mofapy2 implementation, views, 76 complete cases, five seeds | MAIN_METHODS; source scripts | PASS |
| Continuous modeling | feature preprocessing, normalization, number of factors, stability definition | SUPPLEMENTARY_METHODS/source scripts | MAJOR if SI not expanded |
| CORE/EXTENDED programs | assignment procedure, thresholds and program sizes | SUPPLEMENTARY_METHODS/source scripts | MAJOR |
| Single-cell | donor aggregation and no cell-level n inflation | MAIN_METHODS | PASS |
| Single-cell | QC, annotation, scoring, bootstrap/FDR details | SUPPLEMENTARY_METHODS/source scripts | MAJOR |
| Spatial | ρ definition, unit and aggregation | MAIN_METHODS; Results; Figure 3 legend | PASS |
| Spatial | preprocessing and representative-section rule | SUPPLEMENTARY_METHODS/source scripts | MAJOR |
| MAGMA | CORE primary, EXTENDED sensitivity, MHC-excluded primary, FDR, matched-null | MAIN_METHODS | PASS |
| MAGMA | gene annotation build, matched-null construction details and empirical P definition | SUPPLEMENTARY_METHODS/source scripts | MAJOR |
| LDSC | harmonization, h², intercept, FDR and QC flags | MAIN_METHODS | PASS |
| LDSC | exact LD-score reference and filtering thresholds | SUPPLEMENTARY_METHODS/source scripts | MAJOR |
| LAVA | local h² screening, restricted targets, FDR, LD-reference validation | MAIN_METHODS | PASS |
| LAVA | exact block/reference configuration | SUPPLEMENTARY_METHODS/source scripts | MAJOR |
| SMR/HEIDI | GTEx source, primary and second probe-window sensitivity | MAIN_METHODS | PASS |
| SMR/HEIDI | cis window, instrument rule, HEIDI threshold, SMR significance | SUPPLEMENTARY_METHODS/source scripts | MAJOR |
| coloc | restricted candidate set, PP4/PP3 interpretation, MAF proxy flag | MAIN_METHODS | PASS |
| coloc | priors, window and allele harmonization details | SUPPLEMENTARY_METHODS/source scripts | MAJOR |

Conclusion: no main-text blocking gap remains after v9. Several reproducibility details should be expanded in Supplementary Methods before final upload.
