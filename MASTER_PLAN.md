# Master plan

## Scientific question

Does psoriasis contain reproducible cross-tissue molecular endotypes, and are these endotypes stable, interpretable, and not reducible to severity, BMI, batch, or leakage?

## Phase 0: project lock and data audit

1. Create the project skeleton and versioned analysis documents.
2. Retrieve E-MTAB-14509 metadata from official EMBL-EBI BioStudies/ArrayExpress resources.
3. Parse SDRF metadata into patient-level and sample-level audit tables.
4. Identify baseline, pretreatment, discovery, and replication samples.
5. Record missingness, tissue completeness, repeated measures, raw/processed data availability, and leakage risks.
6. Freeze Phase 1 analysis rules before inspecting clustering results.

## Phase 1: baseline-only endotype discovery and replication

1. Build discovery and replication baseline cohorts using patient as the statistical unit.
2. Run expression QC per tissue/cohort and log any exclusions.
3. Construct biologically compressed feature families:
   - pathway activity,
   - regulon/signaling activity,
   - cell-composition or cell-state proxies.
4. Integrate views using a multi-view latent representation, preferring MOFA2 when available.
5. Discover clusters only in discovery patients and evaluate k = 2-6.
6. Freeze all transforms, features, centroids, and classifiers.
7. Assign replication patients to discovery-defined endotypes without reclustering.
8. Run confounding audits, negative controls, and sensitivity analyses.
9. Produce Phase 1 figures/tables and a GO / CONDITIONAL GO / NO-GO report.

## Guardrails

- Baseline/pretreatment only for discovery.
- Patient is the statistical unit.
- No patient can cross discovery and replication.
- Replication never refits clustering.
- Raw genes cannot be the only primary feature space.
- Discrete endotypes will not be forced if the data support only continuous molecular axes.

