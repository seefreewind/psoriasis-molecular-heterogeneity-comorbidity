# Analysis lock

Created before inspecting any clustering output.

## Primary inclusion

- Psoriasis patients from E-MTAB-14509.
- Baseline / pretreatment samples only for Phase 1 discovery and replication.
- RNA-seq samples with resolvable patient identity.
- Samples whose tissue and discovery/replication status can be recovered from official metadata.

## Exclusions

- Week 1, week 4, week 12, post-treatment, and any future response labels.
- Samples with unresolved patient identity.
- Samples whose cohort assignment is ambiguous.
- Samples failing objective QC rules recorded in `DECISION_LOG.md`.

## Statistical unit

The patient is the only clustering, bootstrap, replication, and association unit. Multiple tissues and visits are views or repeated observations, not independent patients.

## Tissue strategy

Primary candidate views:

- Lesional Skin
- Nonlesional Skin
- Whole Blood

Two analysis tracks are locked before clustering:

- Analysis A: complete-case cross-tissue patients.
- Analysis B: partial-view sensitivity for patients with missing views.

The final primary strategy will be chosen from metadata completeness before clustering and logged in `DECISION_LOG.md`.

## Feature families

Primary endotype discovery must use biologically compressed features:

- pathway activities,
- regulon/signaling activities,
- cellular composition/state proxies.

Raw/highly variable genes may be a sensitivity analysis but cannot be the only primary input.

## Integration and clustering

- Preferred latent model: MOFA2 with tissues as views.
- If MOFA2 cannot be installed or the available replication tissues make frozen projection inappropriate, a transparent fallback latent representation may be used and logged.
- Clustering is fit only in the discovery cohort.
- Candidate k values: 2-6.
- Minimum target cluster size: 10 patients.
- Target cluster-wise bootstrap Jaccard: at least 0.75.
- Random seed: 20260810.

## Frozen replication

After discovery, freeze:

- feature definitions,
- transformations,
- scaling,
- latent representation or projection,
- cluster centroids,
- classifier/assignment rule.

Replication patients must be assigned to discovery-defined endotypes by frozen centroids, frozen classifier, or frozen projection. Reclustering replication patients is prohibited.

## GO criteria

Strong GO requires most of:

- at least two stable clusters, preferably at least three;
- major clusters with Jaccard at least 0.75;
- reasonable cluster sizes;
- executable replication assignment;
- clear discovery/replication biological signature concordance;
- endotypes not reducible to batch, BMI, PASI, age, sex, or HLA-C*06:02;
- at least two endotypes interpreted by at least two independent biological feature families;
- cross-tissue information contributes beyond a single tissue.

CONDITIONAL GO is allowed if the evidence supports molecular states or axes but not a strong discrete endotype claim.

NO-GO is required for unstable clusters, replication failure, cluster equals batch/severity/BMI, unresolvable discovery/replication identity, or severe tissue missingness that destroys the primary design.

## Phase 1B Molecular Axis Lock

This section is added after the Phase 1 discrete-clustering stability audit.

### Trigger for reframing

The Phase 1 fallback biological-feature analysis selected k = 2, but the minimum bootstrap Jaccard was 0.562, below the locked strong discrete-cluster target of 0.75. Discovery-to-replication signature concordance was high, while nearest-centroid assignment confidence was only moderate. This pattern supports testing reproducible continuous molecular structure rather than treating the k = 2 partition as a robust discrete endotype result.

This reframing is triggered by the prespecified stability failure and internal replication geometry. It is not triggered by downstream GWAS, MR, comorbidity, colocalization, drug, or external trait analyses, none of which have been run.

### Primary representation

- Discrete clusters are no longer required as the primary Phase 1B phenotype.
- Continuous latent molecular axes are now the primary representation.
- Previous k = 2 results remain reported and must not be deleted.
- Clustering is secondary and exploratory in Phase 1B.
- The preferred future genetics unit, if Phase 1B succeeds, is a frozen axis-associated gene/program set rather than post-hoc cluster DEGs.

### Phase 1B cohorts and views

- Discovery three-view analysis uses only baseline patients with lesional skin, non-lesional skin, and whole blood.
- Skin-paired analysis uses baseline lesional and non-lesional skin for compatibility with E-MTAB-14509 replication.
- Entire missing tissues must not be imputed.
- Replication skin projection must use frozen discovery definitions and must not refit factors or rediscover axes.
- Blood support within E-MTAB-14509 is discovery-only cross-tissue support, not independent cross-tissue replication.

### Feature families

Phase 1B feature reconstruction must use frozen, predefined, interpretable feature families:

- pathway activity using Hallmark, Reactome where available, and curated psoriasis/inflammation modules;
- regulon/signaling activity using decoupler or equivalent mature Python implementations where available;
- cell-state signatures using predefined keratinocyte, T17, CD8/TRM, myeloid, neutrophil, fibroblast, endothelial, B-cell, and NK-cell programs.

Feature definitions must not be optimized using external replication, clinical significance, GWAS, comorbidity, or downstream outcomes.

### Axis model selection

- Fit latent-axis models in discovery only.
- Candidate factor range: 5-10 initial factors where the method supports it.
- Use multiple random seeds.
- Select retained axes by variance explained, convergence, seed/bootstrap stability, loading reproducibility, top-feature overlap, factor score reproducibility, and biological interpretability.
- Do not select factors based on downstream clinical, genetic, comorbidity, or external-trait significance.

### Axis interpretation

- Name factors F1, F2, F3, etc. initially.
- Assign biological labels only if supported by at least two independent feature families.
- Classify each factor as robust, intermediate, or unstable.
- A factor dominated by one obvious clinical or technical covariate must not be interpreted as a mechanistic axis.

### Phase 1B GO criteria

STRONG GO requires at least two molecular axes satisfying most of:

- stable across seeds/bootstrap;
- biologically interpretable using at least two evidence families;
- reproducible in E-MTAB-14509 replication skin;
- supported in at least one independent external skin cohort;
- not dominated by batch, PASI, BMI, age, sex, or HLA-C*06:02;
- coherent discovery-only blood/systemic support for one or more axes.

CONDITIONAL GO is appropriate if only one robust axis exists, replication is moderate, or external support is incomplete.

NO-GO is required if latent factors are unstable, external replication fails, or factors are primarily technical/severity effects.

## Phase 2A Axis Mechanism Prioritization Lock

This section is added after accepting the skin-primary continuous molecular-axis manuscript boundary and before inspecting any downstream GWAS, MR, colocalization, comorbidity, drug, or therapeutic-target results.

### Objective

Phase 2A converts the existing robust continuous molecular factors F1-F8 into biologically interpretable, audit-ready mechanistic axes. It prioritizes 3-4 primary or supportive axes, freezes their definitions, and determines which axes are eligible for downstream single-cell, spatial, and genetic analyses.

Phase 2A is an interpretation, prioritization, and evidence-audit phase. It must not rediscover molecular axes, refit Phase 1B factors, or modify Phase 1/Phase 1B results to obtain a cleaner story.

### Allowed prioritization evidence

Axis priority must be based only on evidence available before downstream genetics and comorbidity analyses:

- latent-factor robustness;
- biological interpretability;
- internal E-MTAB-14509 skin replication;
- independent external skin replication;
- confounding independence;
- coherent tissue contribution;
- blood/systemic support where available;
- suitability for downstream genetic annotation.

### Explicit prohibitions

Phase 2A must not:

- prioritize an axis because it later produces a significant GWAS result;
- prioritize an axis because it gives a desirable comorbidity association;
- rename an axis after seeing MR, colocalization, or comorbidity results;
- select genes based on future p-values;
- drop a robust axis solely because its biological story is inconvenient;
- use future single-cell, spatial, GWAS, MR, LDSC, LAVA, colocalization, drug, or comorbidity evidence to define Phase 2A axis membership.

### Naming rules

An axis can receive a biological name only when at least two independent biological evidence families converge, preferably pathway plus regulon plus cell-state evidence. A statistically robust MOFA factor is not automatically a biological mechanism.

If evidence remains single-family, diffuse, or tissue-ambiguous, retain the F-number and use a descriptive card rather than a formal mechanism name.

### Gene-program freeze

CORE and EXTENDED gene programs for retained primary or supportive/systemic axes must be frozen before downstream single-cell, spatial, or genetics analysis. Gene membership must come from loading-supported source features and recorded gene-set provenance, not from future genetic, comorbidity, or clinical-significance results.

### Future statistical unit

For single-cell and spatial validation, the unit of inference must be patient/donor, not individual cells or spots. Cell-level or spot-level scores may be summarized within donor, cell type, and tissue niche, but inferential testing must use donor-level summaries.

## Phase 2B Single-Cell Localization Lock

This section is added before analyzing GSE228421 single-cell expression data.

### Objective

Phase 2B tests whether frozen Phase 2A CORE and EXTENDED gene programs for F1, F2, F6, and F7 localize to specific donor-level cell types or cell states in psoriasis skin single-cell RNA-seq.

Phase 2B is a biological localization phase. It must not redefine Phase 1B factors, alter Phase 2A gene programs, or choose CORE versus EXTENDED based on which result is more favorable.

### Primary and sensitivity programs

- CORE programs are primary.
- EXTENDED programs are sensitivity analyses.
- Direction, interpretation, and entry into later genetics must be based on CORE first.
- EXTENDED can support robustness but cannot rescue a failed CORE result by itself.

### Statistical unit

The unit of inference is donor/patient.

Allowed:

- per-cell scoring as an intermediate calculation;
- cell-type annotation or marker-based coarse labels;
- donor x sample x cell-type summaries;
- donor-level paired lesional versus nonlesional tests;
- donor bootstrap confidence intervals.

Prohibited:

- treating cells as independent biological replicates;
- reporting cell-level p values as the primary evidence;
- interpreting treatment samples as baseline validation;
- changing gene-program membership after viewing GSE228421 results.

### Primary analysis set

Baseline/pre-treatment day 0 samples are the primary analysis:

- baseline lesional skin;
- baseline nonlesional skin;
- paired by donor where available.

Treatment day 3 and day 14 lesional samples are sensitivity/perturbation evidence only.

### Phase 2B GO criteria

STRONG GO TO GENETICS requires at least three retained axes with:

- donor-level cell-type localization;
- at least one clear dominant cell type or state;
- CORE and EXTENDED results directionally consistent;
- biologically plausible lesional/nonlesional pattern;
- external bulk replication already available;
- no evidence that the signal is only a PASI/BMI/technical surrogate;
- mechanism naming confidence upgraded to MODERATE or HIGH.

CONDITIONAL GO is appropriate if only two axes achieve clear donor-level localization, or if F7 remains supportive/systemic but useful.

NO-GO / SHRINK is required if F1, F2, and F6 are diffuse across cell types without specificity. In that case, frame them as bulk tissue molecular programs rather than cell-state mechanisms.

### Prohibited downstream analyses

Do not run GWAS, MR, LDSC, LAVA, colocalization, drug prediction, PPI, hub-gene, or LASSO analyses during Phase 2B.

## Phase 2B-R + Phase 2C Stop-Rule Lock

This section is added after completing the first GSE228421 Phase 2B analysis.

### Rationale

GSE228421 produced directional keratinocyte clues for F1, F2, and F6 and a skin immune clue for F7, but all axes remained LOW confidence under donor-level FDR criteria. This pattern justifies one limited refinement and one independent validation block, but not unlimited transcriptomic rescue.

### Phase 2B-R scope

Phase 2B-R is a one-pass high-resolution refinement of GSE228421 only.

Allowed refinements:

- keratinocyte states: basal, spinous/suprabasal, proliferative, inflammatory, IFN-response, stress/hypoxia;
- fibroblast states: inflammatory versus homeostatic/stromal;
- myeloid states: monocyte/macrophage/DC;
- T/NK states: coarse immune states sufficient to evaluate F7.

Prohibited:

- refitting Phase 1B axes;
- modifying frozen F1/F2/F6/F7 CORE or EXTENDED gene programs;
- creating new clusters merely to obtain a more favorable mechanism;
- choosing CORE versus EXTENDED after seeing which looks stronger.

### Phase 2C scope

Phase 2C is the independent validation block.

GSE202011 is locked as an independent spatial transcriptomics resource based on local GEO audit and official GEO metadata. It must not be mislabeled as the 67,378-cell scRNA atlas unless the matching scRNA object/accession is independently identified and audited.

Before using an independent scRNA atlas, the exact accession or processed object must be recorded, and donor/sample-level metadata must be audited.

### Stop rule

After Phase 2B-R and Phase 2C:

- stop adding new transcriptomic datasets for rescue;
- freeze mechanism confidence v2;
- either upgrade selected axes to mechanistic axes or permanently shrink them to bulk tissue molecular axes with directional cellular clues.

### Genetics entry rule

Phase 3 genetics can begin only after mechanism freeze v2. It does not require every axis to become a high-confidence cell-state mechanism, but it does require that all axis gene programs remain frozen before genetics. GWAS, MR, LDSC, LAVA, and colocalization results must not be used to rename axes or revise gene-program membership.

### Continuing prohibitions

Until mechanism freeze v2 is accepted, do not run GWAS, MR, LDSC, LAVA, colocalization, drug prediction, PPI, hub-gene, or LASSO analyses.

# Phase 2B-R / 2C Final Transcriptomics Validation Lock

This section is added before executing Phase 2B-R refinement and Phase 2C independent single-cell/spatial validation.

This is the final transcriptomics rescue attempt. After Phase 2B-R and Phase 2C are completed, no additional bulk RNA-seq, single-cell RNA-seq, or spatial transcriptomics datasets may be introduced solely to rescue weak mechanism naming, strengthen an axis story, or avoid shrinking the manuscript claim.

## Accession boundaries

- GSE228421 is locked as the psoriasis scRNA-seq dataset already used in Phase 2B and may be used for one-pass Phase 2B-R internal/mechanistic refinement only.
- GSE173706 is locked as a candidate independent psoriasis scRNA-seq atlas for Phase 2C, pending download and transparent annotation strategy.
- GSE225475 is locked as a candidate primary spatial transcriptomics localization dataset associated with the independent single-cell/spatial psoriasis study; it is not a single-cell dataset.
- GSE202011 is locked as an independent psoriasis/PsA spatial transcriptomics dataset for external spatial robustness; it must not be described as a single-cell atlas.

## Dataset-use rule

Every Phase 2B-R/2C dataset must pass the accession audit recorded in `reports/PHASE2C_DATASET_ACCESSION_AUDIT.md` before expression analysis. If downloaded files, donor IDs, disease labels, LS/NL labels, matrix format, annotations, or spatial images conflict with the audit, that dataset must be stopped until the inconsistency is resolved and logged.

## Frozen analysis units

- Frozen axes remain F1, F2, F6, and F7.
- Frozen CORE gene programs are primary.
- EXTENDED gene programs are sensitivity analyses.
- Donor/patient remains the inference unit for single-cell analysis.
- Spatial spots/sections are not independent patients and must be summarized at section/sample/donor level where inferential language is used.

## Final decision rule

At the end of Phase 2B-R/2C, the project must issue one mechanism-freeze v2 decision:

- proceed to genetics with 3-4 axes;
- proceed to genetics with 2 axes plus F7 supportive/systemic;
- shrink to bulk molecular programs with directional cellular/spatial support.

Until that decision is written, GWAS, MR, LDSC, LAVA, colocalization, drug prediction, PPI, hub-gene, and LASSO analyses remain prohibited.

# Phase 3A Genetic Anchoring Lock

This section is added after `MECHANISM_FREEZE_V2.md` and before examining psoriasis GWAS enrichment results.

Phase 3A tests whether the previously frozen F1/F2/F6/F7 molecular-axis gene programs capture inherited psoriasis susceptibility. It is a genetic anchoring phase for frozen bulk molecular programs, not a mechanism-renaming, multisystem comorbidity, MR, colocalization, drug-target, or causal mediator phase.

## Primary programs

- CORE programs are primary.
- EXTENDED programs are sensitivity only.

## Primary phenotype

- Psoriasis susceptibility GWAS.

## Primary genetic analysis

- MAGMA competitive gene-set analysis.

## Secondary genetic analysis

- Stratified LDSC / partitioned heritability only if technically appropriate after summary-statistics and reference-data audit.

## MHC handling

- Primary analysis: MHC excluded.
- Sensitivity analysis: MHC included.

## Axis definitions

- F1, F2, F6, and F7 identities are immutable.
- CORE and EXTENDED gene membership must be read from `results/phase2a/axis_gene_programs/` and must not be inferred from prose summaries.

## Multiple testing

- Primary family: 4 CORE molecular axes.
- Apply FDR across the 4 primary axis tests.
- Sensitivity analyses must be labeled separately and use separately reported multiplicity handling.

## Prohibited adaptations

Do not:

- add GWAS-significant genes to axis programs;
- remove GWAS-negative genes;
- select EXTENDED over CORE because results are stronger;
- rename an axis after genetic results;
- remove an axis because it is not enriched;
- redefine CORE membership using MAGMA statistics;
- merge axes based on genetic enrichment;
- choose MHC boundaries after seeing results.

## Phase 3A Final Genetic Freeze

Phase 3A completed with `NO-GO_FOR_GENETICALLY_ANCHORED_AXES`.

- F1, F2, F6, and F7 remain frozen molecular-axis programs, but none may be called genetically anchored.
- Phase 3B eQTL colocalization, MR, TWAS-based mechanistic interpretation, pQTL analysis, drug-target analysis, and axis-specific multisystem comorbidity genetics remain prohibited under the axis-specific genetic-anchoring route.
- Any later genetics phase must be redesigned as overall psoriasis/shared-genetic architecture unless the user explicitly starts a new locked analysis plan.

# Phase 4A Overall Psoriasis Multisystem Genetic Architecture Lock

This section is added after accepting the Phase 3A `NO-GO_FOR_GENETICALLY_ANCHORED_AXES` result.

## Rationale

Phase 3A showed that frozen transcriptomic F1/F2/F6/F7 CORE programs do not capture robust, axis-specific inherited psoriasis susceptibility. The genetics story is therefore redesigned around overall psoriasis liability and multisystem shared genetic architecture. Transcriptomic axes remain a separate tissue-molecular layer and may only be used later to contextualize shared loci.

## Primary exposure

- Overall psoriasis susceptibility genetic liability.
- Primary psoriasis GWAS: GCST90472771, already audited and downloaded from official EMBL-EBI/GWAS Catalog sources.

## Frozen primary comorbidity outcomes

Phase 4A is limited to these 10 prespecified clinical comorbidities:

- psoriatic arthritis;
- Crohn disease;
- ulcerative colitis;
- coronary artery disease;
- ischemic stroke;
- type 2 diabetes;
- metabolic dysfunction-associated steatotic liver disease;
- major depression;
- uveitis;
- chronic kidney disease.

Outcome datasets must be audited for ancestry, genome build, sample size, case definition, summary-statistic availability, variant identifiers, effect allele fields, standard error or odds-ratio fields, and sample-overlap risk before analysis.

## Primary analysis

Genome-wide genetic correlation using LDSC is the first Phase 4A analysis layer.

Phase 4A itself stops at LDSC genome-wide genetic correlation. LAVA, shared loci, colocalization, TWAS sensitivity, bidirectional MR, and transcriptomic contextualization require a separate downstream phase decision after the LDSC result table and QC report are written.

Required output:

- disease/outcome;
- data source and accession or URL;
- sample size and ancestry if available;
- LDSC rg;
- standard error;
- P value;
- FDR across the 10 primary outcomes;
- interpretation tier.

## Secondary analysis

LAVA local genetic correlation is not part of Phase 4A primary execution. It is allowed only in Phase 4B after both psoriasis and outcome GWAS summary statistics pass harmonization and reference-data QC and the Phase 4A GO/SHRINK decision is logged.

LAVA is used to identify local shared genetic architecture. It must not be interpreted as evidence that F1/F2/F6/F7 are genetically causal axes.

## Downstream analyses

Shared loci, fine-mapping review, eQTL colocalization, TWAS sensitivity, and bidirectional MR are deferred to later Phase 4B-4D modules and may be run only for disease pairs with Phase 4A/4B support.

MR is directional support only. It must not be the central evidence layer and must not be used to claim clinical causality without colocalization and sensitivity support.

## Transcriptomic overlay

After shared loci are identified independently, frozen transcriptomic programs may be used only for secondary contextualization:

- overlap with shared-locus genes;
- over-representation analysis;
- rank enrichment.

This overlay must be described as `transcriptomic contextualization of shared genetic loci`, not as axis-specific genetic causation.

## Prohibited adaptations

Do not:

- rerun alternative psoriasis GWAS datasets to rescue F1/F2/F6/F7 axis genetics;
- use EXTENDED gene sets to rescue failed CORE results;
- interpret F2 nominal sensitivity as a genetics anchor;
- run axis-specific MR, LAVA, colocalization, or comorbidity genetics;
- scan large disease panels before completing the frozen 10-outcome Phase 4A analysis;
- perform drug prediction, PPI, hub-gene, or LASSO analyses;
- rename F1/F2/F6/F7 as inherited genetic subtypes.

## Phase 4 GO criteria

Phase 4A GO/SHRINK criteria are frozen before LDSC execution:

- GO: at least 3-4 different system domains show FDR-significant LDSC genetic correlation with coherent direction and acceptable LDSC QC.
- CONDITIONAL GO: only 1-2 strong signals are detected, but they span more than one system domain or include a biologically central comorbidity with clean QC.
- SHRINK: there is little robust rg evidence, major QC failure across outcomes, or signal is confined to one classic autoimmune outcome/domain.

If strong sharing is limited to psoriatic arthritis and inflammatory bowel disease, shrink the genetics story to autoimmune comorbidity genetic architecture rather than forcing a broad multisystem claim.
