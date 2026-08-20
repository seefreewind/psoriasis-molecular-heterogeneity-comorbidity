# Spatial Dominant-Marker Rule Audit

Dominant spatial marker programs were selected independently within each spatial dataset. For each axis, only CORE gene-program scores were used for this label selection. Spot-level Spearman correlations were computed between the axis score and each predefined marker program within each section, requiring at least 10 spots with non-missing scores. For each axis and marker program, the signed median Spearman correlation across sections was calculated. The dominant marker program was the marker with the highest signed median correlation, not the highest absolute correlation.

This rule was implemented before spatial interpretation and did not use genetic, SMR, coloc, or manuscript-level outcome labels. Section and spot results were interpreted as spatial support, not as patient-level replication.
