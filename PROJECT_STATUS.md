# Project status

## Current phase

Phase 0 complete; Python fallback Phase 1 complete; Phase 1B molecular-axis rescue and selected external support processing complete; strict Phase 2A axis mechanism prioritization and freeze complete; Phase 2B/2B-R/2C transcriptomic localization complete; Phase 3A psoriasis genetic anchoring complete; Phase 4A overall psoriasis multisystem genetic architecture design locked.

## Completed

- Created the project directory structure.
- Downloaded the official E-MTAB-14509 BioStudies JSON record.
- Downloaded the official E-MTAB-14509 IDF and SDRF metadata.
- Created the initial analysis lock, decision log, master plan, and config scaffold.
- Downloaded normalized discovery skin, normalized discovery blood, and normalized replication skin matrices.
- Generated metadata audit tables and report.
- Ran leakage tests.
- Ran a baseline skin-paired expression-axis smoke test with frozen replication assignment.
- Downloaded all official raw and normalized count matrices listed in E-MTAB-14509.
- Generated Hallmark + curated pathway/regulon/cell-state fallback feature scores.
- Ran skin-paired baseline biological-feature fallback clustering, frozen replication assignment, confounding audit, negative controls, and sensitivity analyses.
- Generated Phase 1 figures in PNG/SVG/PDF.
- Installed a dedicated Phase 1B Python environment with `mofapy2`, `decoupler`, `gseapy`, `scanpy`, and supporting packages.
- Built Phase 1B Hallmark/Reactome/curated/cell-state/regulon/signaling feature matrices.
- Ran discovery-only three-view MOFA2 molecular-axis models across five seeds on 76 complete LS/NL/blood baseline patients.
- Projected frozen skin axes into E-MTAB-14509 replication skin samples.
- Audited external GEO datasets GSE121212, GSE244679, GSE54456, GSE147339, and GSE61281.
- Downloaded and checksummed processed files for GSE121212, GSE54456, and GSE147339.
- Completed GSE244679 paired-skin raw-count tar download, extracted 48 per-sample count files, and processed 24 paired lesional psoriatic versus adjacent normal skin samples.
- Downloaded GSE147339 and GSE61281 series matrices plus GPL6480 platform annotation for platform-aware external blood support.
- Ran feasible GSE121212 paired psoriasis skin support analysis.
- Ran GSE244679 paired-skin axis replication analysis.
- Ran GSE147339 whole-blood RNA-seq and GSE61281 GPL6480-mapped microarray blood support analyses.
- Accepted the skin-primary continuous-axis manuscript boundary with selective systemic support.
- Ran strict Phase 2A axis triage, mechanism-card construction, redundancy analysis, gene-program freeze, readiness audits, and Figure 2 drafts.
- Froze three primary skin axes for the next phase: F1, F2, and F6.
- Froze F7 as a supportive/systemic axis for the next phase.
- Downloaded and processed all 20 official GSE228421 10x supplementary samples.
- Scored frozen F1/F2/F6/F7 CORE and EXTENDED gene programs at cell level, then summarized them to donor x cell-type units.
- Ran baseline paired lesional versus non-lesional donor-level statistics, CORE/EXTENDED robustness, treatment timepoint sensitivity, and program-dropout robustness for Phase 2B.

## Key results

- Official SDRF resolves 146 patients overall: 89 discovery and 57 replication.
- Baseline resolves 145 patients: 88 discovery and 57 replication.
- Discovery baseline has 82 lesional skin, 82 non-lesional skin, and 82 whole-blood samples; 76 patients have all three baseline tissues.
- Replication baseline has 57 lesional and 57 non-lesional skin samples, but no whole-blood samples.
- Smoke-test k=2 expression-axis split had high direction concordance in replication but bootstrap Jaccard below the locked 0.75 threshold.
- Fallback biological-feature primary analysis selected k=2.
- k=2 cluster sizes were 51 and 31 discovery patients.
- Minimum selected-cluster bootstrap Jaccard was 0.562, below the locked 0.75 target.
- Discovery-replication signature concordance was high (Spearman 0.911), but assignment confidence was moderate (mean 0.509).
- Phase 1B MOFA2 modeled 76 discovery patients with complete lesional skin, non-lesional skin, and blood views.
- Eight reference factors were stable across five MOFA2 seeds under the current deterministic feature filter.
- Internal E-MTAB-14509 skin projection showed several moderate loading-vs-replication score correlations, supporting axis-based rescue but not discrete cluster rescue.
- Discovery blood support remains discovery-only because E-MTAB-14509 replication lacks blood RNA-seq.
- GSE121212 external paired psoriasis skin support was feasible in 27 paired patients, but correlations were weak.
- GSE244679 external paired-skin analysis adds independent support for several axes: F1-LS, F2-NL, F6-LS, F3-NL, and F5-LS showed the strongest loading-vs-lesional-minus-adjacent correlations by absolute magnitude.
- GSE147339 external blood support is weak across axes.
- GSE61281 external blood support is platform-dependent but informative after GPL6480 probe mapping, with the strongest signal for F7 across PsC-control, PsA-control, and combined psoriasis-spectrum-control contrasts.
- Strict Phase 2A prioritization selected F1, F2, and F6 as primary skin axes and F7 as a supportive/systemic axis.
- F3, F5, and F8 remain secondary axes; F4 is retired from the main story as uninterpretable/supplementary.
- Formal mechanism names remain provisional. F6 and F3 have moderate naming confidence based on multifamily evidence; F1, F2, and F7 keep F-number labels plus descriptive domains until donor-level single-cell localization.
- Phase 2B GSE228421 found directional keratinocyte LS-vs-NL signals for F1, F2, and F6 and a skin immune NK/B-cell directional signal for F7, but all four axes remain LOW confidence because donor-level FDR thresholds were not met with 5 donors.
- Strict Phase 2B conclusion is NO-GO / SHRINK for mechanism naming and genetics escalation from GSE228421 alone. The axes should be framed as bulk tissue molecular programs with directional cell-type clues unless refined annotation/spatial validation strengthens them.
- The next route is locked as Phase 2B-R + Phase 2C with stop rules: one-pass GSE228421 high-resolution refinement, GSE202011 independent spatial validation, independent scRNA validation only after exact data-source audit, then stop adding transcriptomic datasets.
- Local and official GEO audit show that GSE202011 is a spatial transcriptomics dataset with 30 samples and supplementary H5/images, not automatically the independent 67,378-cell scRNA atlas.

## QC findings

- No patient crosses discovery and replication.
- No duplicated SDRF sample IDs.
- No post-treatment samples enter the baseline cohort.
- Replication lacks blood; this is a major design limitation for cross-tissue replication.
- Raw and normalized matrices are fully downloaded and checksummed.
- Replication lacks blood; this remains the dominant design limitation for cross-tissue replication.

## Decisions made

- E-MTAB-14509 is the primary dataset.
- Baseline-only discovery and frozen replication are locked.
- E-MTAB-14509-only replication should be framed as skin-paired replication, not full three-tissue replication.
- The expression-axis smoke test is not accepted as the primary mechanistic endotype result.
- The Python fallback biological-feature result supports only CONDITIONAL GO, not Strong GO, because stability is below the locked threshold.
- Sensitivity analyses are lightweight fixed-k checks; the primary stability result uses 300 bootstrap iterations.

## Open risks

- Preferred R implementation is no longer required for Phase 1B because the Python MOFA2 stack is installed and working; earlier R limitations remain recorded in `environment/INSTALL_LOG.md`.
- Baseline discovery sample count is lower than the publication-level discovery patient count and needs patient-level explanation.
- Cross-tissue replication remains limited because E-MTAB-14509 replication lacks blood.
- External blood results should be treated as support, not design-matched replication, because GSE147339 is small and GSE61281 is a different two-color microarray PsA/PsC/control design.
- Factor signs remain arbitrary until axes are anchored to named biological or clinical phenotypes; external correlation signs should be interpreted as orientation.
- GSE228421 uses raw 10x matrices with very large barcode spaces; Phase 2B reports raw barcode counts separately from QC-passing cells and keeps donor-level inference as the only statistical unit.
- Current Phase 2B cell-type labels are marker-based coarse annotations, not reference-mapped high-resolution cell states.
- GSE202011 should not be mislabeled as single-cell validation. It is currently locked as spatial validation unless a separate matching scRNA object/accession is identified and audited.

## Files generated

- `data/metadata/E-MTAB-14509.biostudies.json`
- `data/metadata/E-MTAB-14509.idf.txt`
- `data/metadata/E-MTAB-14509.sdrf.txt`
- `ANALYSIS_LOCK.md`
- `MASTER_PLAN.md`
- `DECISION_LOG.md`
- `PROJECT_STATUS.md`
- `reports/EMTAB14509_metadata_audit.md`
- `reports/PHASE1_ENDOTYPE_GO_NOGO_REPORT.md`
- `results/qc/sample_flow.tsv`
- `results/qc/patient_tissue_matrix.tsv`
- `results/qc/missingness.tsv`
- `results/qc/leakage_checks.tsv`
- `results/phase1/smoke_test_frozen_assignments.tsv`
- `results/phase1/phase1_smoke_summary.tsv`
- `results/phase1/baseline_biological_feature_matrix_discovery.tsv`
- `results/phase1/baseline_biological_feature_matrix_replication.tsv`
- `results/phase1/frozen_endotype_assignments.tsv`
- `results/tables/Table_S3_feature_definitions.tsv`
- `results/tables/Table_S4_cluster_stability.tsv`
- `results/tables/Table_S5_endotype_signatures.tsv`
- `results/tables/Table_S6_clinical_confounding_associations.tsv`
- `results/tables/Table_S7_replication_metrics.tsv`
- `results/tables/Table_S8_sensitivity_analyses.tsv`
- `results/figures/*.png`
- `results/figures/*.svg`
- `results/figures/*.pdf`
- `reports/PHASE1B_MOLECULAR_AXIS_REPORT.md`
- `results/phase1b/phase1b_feature_matrix_discovery.tsv`
- `results/phase1b/phase1b_feature_matrix_replication.tsv`
- `results/phase1b/mofa_seed_20260810.hdf5`
- `results/phase1b/mofa_seed_20260811.hdf5`
- `results/phase1b/mofa_seed_20260812.hdf5`
- `results/phase1b/mofa_seed_20260813.hdf5`
- `results/phase1b/mofa_seed_20260814.hdf5`
- `results/phase1b/molecular_axis_scores_discovery.tsv`
- `results/phase1b/factor_loadings.tsv`
- `results/phase1b/factor_stability.tsv`
- `results/phase1b/factor_biology.tsv`
- `results/phase1b/replication_ETAB14509.tsv`
- `results/phase1b/cross_tissue_discovery_support.tsv`
- `results/phase1b/axes_vs_clusters.tsv`
- `results/phase1b/external_dataset_audit.tsv`
- `results/phase1b/external_axis_support.tsv`
- `results/phase1b/external_GSE244679_logCPM.tsv`
- `results/phase1b/external_GSE244679_sample_metadata.tsv`
- `results/phase1b/external_GSE244679_skin_axis_replication.tsv`
- `results/phase1b/external_GSE147339_blood_axis_support.tsv`
- `results/phase1b/external_GSE61281_gene_expression.tsv`
- `results/phase1b/external_GSE61281_sample_metadata.tsv`
- `results/phase1b/external_GSE61281_matrix_audit.tsv`
- `results/phase1b/external_GSE61281_blood_axis_support.tsv`
- `results/phase1b/external_axis_replication_and_blood_support.tsv`
- `reports/PHASE2A_AXIS_MECHANISM_PRIORITIZATION.md`
- `reports/mechanism_cards/F1.md` through `reports/mechanism_cards/F8.md`
- `results/phase2a/axis_evidence_matrix.tsv`
- `results/phase2a/axis_priority_matrix.tsv`
- `results/phase2a/axis_mechanism_cards.tsv`
- `results/phase2a/factor_redundancy.tsv`
- `results/phase2a/axis_gene_programs/F1_gene_program.tsv`
- `results/phase2a/axis_gene_programs/F2_gene_program.tsv`
- `results/phase2a/axis_gene_programs/F6_gene_program.tsv`
- `results/phase2a/axis_gene_programs/F7_gene_program.tsv`
- `results/phase2a/axis_gene_program_overlap.tsv`
- `results/phase2a/single_cell_readiness.tsv`
- `results/phase2a/candidate_single_cell_dataset_audit.tsv`
- `results/phase2a/candidate_spatial_dataset_audit.tsv`
- `results/phase2a/Table_axis_prioritization_master.tsv`
- `reports/PHASE2B_GSE228421_SINGLE_CELL_LOCALIZATION.md`
- `results/phase2b/Table_phase2b_axis_cell_localization.tsv`
- `results/phase2b/GSE228421_baseline_LS_vs_NL_donor_statistics.tsv`
- `results/phase2b/GSE228421_cell_type_localization.tsv`
- `results/phase2b/GSE228421_donor_celltype_axis_scores.tsv`
- `results/phase2b/GSE228421_treatment_timepoint_sensitivity.tsv`
- `results/phase2b/GSE228421_program_dropout_robustness.tsv`
- `results/figures/phase2b/Figure3A_GSE228421_axis_celltype_localization.png`
- `results/figures/phase2b/Figure3B_GSE228421_donor_paired_effects.png`
- `reports/PHASE2BR_2C_STOP_RULE_ROADMAP.md`
- `results/phase2br_2c/GSE202011_spatial_sample_audit.tsv`
- `results/phase2br_2c/GSE202011_spatial_sample_summary.tsv`
- `reports/PHASE3A_GWAS_DATA_AUDIT.md`
- `reports/PHASE3A_GWAS_QC.md`
- `reports/PHASE3A_PSORIASIS_GENETIC_ANCHORING.md`
- `GENETIC_FREEZE_V1.md`
- `当前情况_Phase3A遗传锚定后_2026-08-11.md`
- `reports/PHASE4A_OVERALL_PSORIASIS_MULTISYSTEM_GENETIC_ARCHITECTURE_PLAN.md`
- `reports/PHASE4A_GWAS_OUTCOME_DATA_AUDIT.md`
- `reports/PHASE4A_AUDIT_AND_HARMONIZATION_LOCK.md`
- `configs/phase4a_harmonization_spec.tsv`
- `results/phase4a/frozen_comorbidity_outcomes.tsv`
- `results/phase4a/candidate_outcome_gwas_sources.tsv`
- `results/phase4a/phase4a_gwas_audit_matrix.tsv`
- `results/phase4a/download_preflight_headers.tsv`
- `当前情况_Phase4A路线切换_2026-08-12.md`
- `results/phase3a/Table_axis_genetic_anchoring.tsv`
- `results/phase3a/Table1_axis_genetic_anchoring.tsv`
- `results/phase3a/magma_core_MHC_excluded.tsv`
- `results/phase3a/matched_null_results.tsv`
- `results/phase3a/magma_axis_conditional.tsv`
- `results/phase3a/phase3b_candidate_genes.tsv`
- `results/figures/phase3a/Figure6*.png`

## Next actions

- Do not proceed to axis-specific Phase 3B colocalization, MR, or Phase 4 multisystem comorbidity genetics based on F1/F2/F6/F7 as genetically anchored axes.
- Proceed with Phase 4A as overall psoriasis genetic liability versus 10 frozen comorbidities.
- Audit public outcome GWAS sources before LDSC/LAVA.
- Run LDSC genome-wide genetic correlation first; reserve LAVA, shared loci, colocalization, and MR for supported disease pairs.
- Use transcriptomic axes only as later exploratory contextualization of independently identified shared genetic loci.

## GO/NO-GO status

NO-GO FOR GENETICALLY ANCHORED AXES: Phase 3A did not detect robust psoriasis susceptibility enrichment for frozen F1/F2/F6/F7 CORE programs after MHC exclusion, matched-null testing, shared/unique analysis, and conditional MAGMA. This blocks claims that the retained molecular axes represent distinct inherited psoriasis susceptibility components.

GO FOR PHASE 4A REDESIGN: The project continues as a two-layer model: replicated psoriasis tissue molecular heterogeneity plus independently tested overall psoriasis multisystem shared genetic architecture.
