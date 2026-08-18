# Phase 1 endotype GO/NO-GO report

# Executive conclusion

**CONDITIONAL GO**

This report reflects the completed Python fallback biological-feature analysis. It uses locked baseline-only, patient-level, skin-paired discovery and frozen replication assignment. It does not claim fully replicated cross-tissue endotypes because E-MTAB-14509 replication lacks blood.

# Dataset integrity

Official SDRF metadata resolve patient IDs, baseline timepoint, tissue, and discovery/replication status. Leakage tests pass.

# Cohort composition

- Discovery skin-paired baseline patients used in primary analysis: 82
- Replication skin-paired baseline patients assigned by frozen centroids: 57
- Primary skin-paired biological features: 170

# Leakage audit

Discovery used baseline samples only. Replication was assigned with frozen scaler, PCA projection, and nearest centroids; no replication reclustering was performed.

# QC

Expression QC outputs are available in `results/qc/`. Official raw and normalized count matrices listed in the BioStudies file audit are now fully downloaded and checksummed. Normalized matrices were used for this fallback feature analysis.

# Cross-tissue structure

Discovery has a three-view subset, but replication does not contain blood. The primary replicated analysis is therefore skin-paired only. Blood can be analyzed as discovery-only support, not as replicated cross-tissue evidence.

# Endotype discovery

Candidate k=2-6 was evaluated in discovery biological features. Selected k=2.

# Stability

Minimum selected-cluster bootstrap Jaccard: 0.562. Locked strong-GO target is 0.75.

# Biological interpretation

Feature signatures are in `results/tables/Table_S5_endotype_signatures.tsv`. Endotype names remain E1/E2/... until interpretation is supported by at least two independent feature families.

# Confounding audit

Clinical/confounder association tests are in `results/tables/Table_S6_clinical_confounding_associations.tsv`.

# Replication

Frozen nearest-centroid replication assignment was executed. Minimum signature concordance across endotypes: 0.911. Mean centroid-assignment confidence: 0.509.

# Sensitivity analyses

Sensitivity results are in `results/tables/Table_S8_sensitivity_analyses.tsv`.

# Negative controls

Feature-value permutation controls are in `results/tables/negative_controls.tsv`.

# Key limitations

- Replication lacks blood, preventing a strong replicated cross-tissue claim.
- This is a Python fallback using Hallmark and curated score averages, not the preferred GSVA/MOFA2 implementation.
- Sensitivity analyses use fixed-k lightweight checks as a computational-cost adjustment; the primary k=2-6 stability analysis used 300 bootstrap iterations.
- The preferred R/MOFA2/GSVA workflow could not be run in the current local environment after user-level BiocManager and micromamba/bioconda attempts.
- If cluster stability remains below 0.75, discrete endotypes should be treated as provisional molecular states or axes.

# Reviewer attack points

- Cross-tissue replication is unavailable within E-MTAB-14509.
- Discovery/replication differences can still reflect cohort/protocol effects.
- Fallback curated marker scores are less mature than GSVA/decoupleR/MOFA2.

# Recommendation

Do not proceed to single-cell/spatial, GWAS anchoring, multisystem comorbidity GWAS, LDSC/LAVA, cis-eQTL/pQTL MR, or colocalization under the original discrete cross-tissue endotype claim. Current recommended framing is skin-paired baseline molecular states or molecular axes with discovery-only blood support. A human decision is needed before either accepting this reframing or moving the preferred R/MOFA2 workflow to a compatible compute environment.
