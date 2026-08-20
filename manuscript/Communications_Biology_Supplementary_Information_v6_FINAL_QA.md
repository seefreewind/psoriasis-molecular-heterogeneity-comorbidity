# Communications Biology Supplementary Information

# Supplementary Methods

## 1. Overview

These Supplementary Methods provide detailed implementation of the transcriptomic, cellular, spatial, genetic and regulatory analyses supporting the study. The analyses were organized to distinguish psoriasis tissue-state programs from overall inherited comorbidity liability and from restricted regulatory-prioritization evidence at shared loci.

## 2. Cohort Definition And Dataset Roles

E-MTAB-14509 was used for bulk transcriptomic discovery and internal replication across lesional skin, non-lesional skin and whole blood. The discrete branch used 82 paired baseline skin patients. The continuous multi-view model used 76 complete baseline patients with lesional skin, non-lesional skin and whole-blood views. The internal skin replication set contained 57 paired skin patients. GSE244679 provided independent paired-skin support, GSE61281 provided external cross-platform whole-blood support, GSE228421 provided the primary single-cell contextualization, GSE173706 provided independent single-cell sensitivity, and GSE225475 and GSE202011 provided spatial transcriptomic contextualization. Genetic analyses used overall psoriasis susceptibility rather than axis-specific exposures.

## 3. Discrete Representation And Stability Testing

The prespecified primary discrete representation was k = 2. k = 3–6 solutions were evaluated as sensitivity and exploratory stability checks. The discrete branch used lesional–non-lesional normalized expression, the top 1,000 variable genes and principal-component summarization; it was separate from the three-view multi-view factor model. The first five principal components were used when available. k-means used random_state = 20260810 and n_init = 100 for the primary fit. Bootstrap stability used 100 resamples with k-means n_init = 20. Cluster stability was summarized by the minimum best-match bootstrap Jaccard index. A minimum Jaccard threshold of 0.75 was prespecified for manuscript-level categorical interpretation. The discrete and continuous analyses used related but non-identical transcriptomic representations. The clustering result therefore constrained the categorical endotype claim rather than constituting a formal head-to-head model-comparison test.

## 4. Continuous Multi-View Molecular Modeling

MOFA-style multi-view modeling used lesional skin, non-lesional skin and whole-blood feature matrices. Patients were restricted to complete baseline availability across all three views. Within each view, features with any missing value in the discovery matrix were removed, nonconstant features were retained using SD > 1 × 10⁻⁸, and the top 450 features per view were selected by discovery-set standard deviation. Selected features were z-scored using discovery means and standard deviations. The same discovery scalers were reused when projecting internal replication data. The model used eight factors and five random seeds: 20260810, 20260811, 20260812, 20260813 and 20260814. The reference seed was 20260810. MOFA options were center_groups = true, scale_views = false, use_float32 = true, spike-and-slab weights enabled, ARD weights enabled, 600 training iterations, startELBO = 1, freqELBO = 20 and convergence_mode = fast. The 450-feature and eight-factor settings were fixed before external replication, cellular/spatial contextualization and genetic testing and were not tuned against downstream outcomes.

## 5. Factor Alignment And Stability

Cross-seed factor alignment used absolute Pearson correlation of patient scores between each non-reference seed and the reference seed, followed by linear-sum assignment to maximize absolute score concordance. Factor signs were aligned to the reference by the signed Pearson correlation of patient scores. Loading stability was then compared after sign alignment. Robustness metrics were median absolute Pearson score correlation, median absolute Spearman loading correlation across views, median top-75 loading Jaccard overlap across views and mean view-level variance explained in the reference model. A factor was classified as robust when median score correlation was ≥ 0.75, median loading correlation was ≥ 0.55 and mean view R² was ≥ 0.01. Intermediate status required median score correlation ≥ 0.50, median loading correlation ≥ 0.35 and mean view R² ≥ 0.005.

## 6. Molecular Program Construction

Factor identity and gene-program membership were defined before single-cell, spatial and genetic analyses. Downstream evidence informed contextual interpretation but did not alter program composition. For each retained factor, source features were the top 30 loading-ranked features per factor across all views, as implemented in the source code. Genes were mapped from pathway, regulon, cell-state and leading-edge feature annotations. CORE genes required support from at least two source features and at least one evidence family. EXTENDED programs included all genes mapped from the factor-level source-feature set. If fewer than 15 CORE genes were obtained, a fallback would have assigned the top 30 genes by source-feature count and loading strength to CORE, but this fallback was not triggered for F1, F2, F6 or F7.

## 7. Bulk Replication And Systemic Support

GSE244679 was used as independent paired-skin support. Raw counts were aggregated by gene symbol and transformed to log2 CPM. Gene-set scores were computed as follows: within each sample, genes were ranked by expression percentile; for each gene-set feature, the score was the mean percentile rank of present genes; feature scores were z-scored across samples. The external contrast for each feature was lesional psoriatic skin minus adjacent-normal skin within each pair, averaged over 24 valid pairs. The reported statistic was the Spearman correlation across common axis features between the fixed discovery factor loading vector for a factor/view and the GSE244679 mean paired feature-level contrast vector. Absolute |ρ| was reported because latent-factor sign is arbitrary.

GSE61281 was used as external cross-platform whole-blood support rather than design-matched replication. The dataset contained Agilent GPL6480 whole-blood microarray samples from cutaneous psoriasis without arthritis, psoriatic arthritis and unaffected controls. GEO series-matrix values were treated as normalized microarray expression. Probes were mapped through GPL6480 gene symbols; if multiple symbols were listed, the first was used, empty mappings were removed and multiple probes mapping to the same gene were averaged. The same within-sample percentile-rank gene-set scoring was applied. Contrasts were case-group mean score minus control mean score, including the psoriasis-spectrum contrast that combined cutaneous psoriasis and psoriatic arthritis.

## 8. Clinical/Confounding Audit

Clinical/confounding analyses used factor scores as dependent variables and PASI, BMI, age, sex and HLA-C*06:02 carrier status as covariates in complete baseline discovery metadata. Factor scores and covariates were standardized before linear regression. For each covariate, partial R² compared a full model containing all covariates with a reduced model excluding the tested covariate. Coefficients, standard errors, t-test P values and Benjamini-Hochberg FDR values were reported. Batch association was recorded as unavailable because no harmonized batch covariate was present in the current covariate model.

## 9. Primary Single-Cell Contextualization

GSE228421 10x single-cell matrices were read from barcodes, features and matrix-market UMI-count files. Gene symbols were taken from the feature table and converted to uppercase. Library size, detected-gene count and mitochondrial percentage were computed per cell; mitochondrial genes were identified by the MT- prefix. Cells were retained with total counts ≥ 500, detected genes ≥ 200 and mitochondrial percentage ≤ 25%. CORE programs were primary and EXTENDED programs were sensitivity analyses. Program scores were mean log1p(CP10K) expression over overlapping program genes and were treated as missing when fewer than three genes overlapped. Marker-panel scores assigned cell types by maximum marker score; cells with maximum marker score ≤ 0 were assigned as unassigned. Scores were aggregated by donor, sample, timepoint, tissue state and cell type. The primary comparison was baseline lesional versus non-lesional skin at donor level. Paired donor differences were tested using sign-flip tests, 95% bootstrap confidence intervals used 2,000 bootstrap iterations with seed 20260811, and FDR was controlled within CORE or EXTENDED program type. Treatment/timepoint analyses were sensitivity analyses and did not redefine program identity.

## 10. Independent Single-Cell Sensitivity

GSE173706 was used only as an independent single-cell sensitivity dataset. The metadata contained 33 skin samples from 23 donors, including psoriasis lesional, psoriasis non-lesional and healthy skin samples. Raw count CSV files were mapped to gene symbols by removing Ensembl version suffixes and using the archived Ensembl-to-symbol map; duplicate symbols were summed. Cells were retained with total counts ≥ 500, detected genes ≥ 200 and mitochondrial percentage ≤ 25%. Program scores used mean log1p(CP10K) expression over available program genes and were summarized at donor/sample and cell-state level. Paired lesional–non-lesional statistics used donor-level summaries, sign-flip testing, 2,000 bootstrap iterations with seed 20260811 and FDR within program type. Healthy comparisons used donor-level Mann-Whitney tests when at least three donors were available per group. The dataset served as sensitivity support and did not supersede GSE228421.

## 11. Spatial Transcriptomic Contextualization

Spatial transcriptomic analyses used prespecified CORE program scores and all prespecified marker programs. For each spatial sample, within-sample spot-level Spearman correlation was calculated between each CORE program score and each spatial marker-program score. The dominant marker for each program and dataset was selected by the highest signed median correlation across samples, not by the highest absolute correlation. The median correlation summarized spot-level association within a dataset. Spots and sections were not treated as patient-level replicates.

## 12. Axis-Specific Genetic Anchoring

Axis-specific genetic anchoring used GCST90472771 psoriasis GWAS summary statistics and retained CORE gene programs as the primary gene-set input. Gene mapping used the MAGMA NCBI37.3 gene-location file and the 1000 Genomes European reference. The primary analysis excluded the MHC region, defined as GRCh37 chr6:25,000,000–34,000,000. EXTENDED and MHC-included analyses were sensitivity analyses. MAGMA version information and software versions are listed in Supplementary Table S7. Four primary CORE/MHC-excluded tests were adjusted with Benjamini-Hochberg FDR. Matched-null sensitivity generated 2,000 random gene sets per axis with seed 20260811, matched first on chromosome, gene-length quintile and NSNP quintile; if insufficient, matching used length/NSNP quintiles across chromosomes, then genome-wide fallback excluding axis genes and already sampled genes. Empirical P values used P_emp = [1 + Σ I(beta_null ≥ beta_observed)] / (N_null + 1).

## 13. GWAS Provenance And Harmonization

GWAS analyses used overall psoriasis susceptibility as the inherited-liability exposure. Outcomes with source-resolved analyzable summary statistics were harmonized to LDSC-compatible rsID, allele, signed-statistic and HapMap3 formats. Prespecified outcomes whose primary sources were not resolved at the analysis cutoff were not interpreted as null. Provenance, ancestry/build notes and harmonization status are listed in Supplementary Table S4.

## 14. LDSC Genome-Wide Genetic Correlation

LDSC estimated genome-wide genetic correlation (r_g) between overall psoriasis susceptibility and each source-resolved outcome with analyzable summary statistics. The output recorded r_g, SE, Z, P, FDR, trait heritability, outcome intercept and cross-trait intercept. FDR was controlled across analyzed psoriasis–outcome pairs. Psoriatic arthritis was treated as a near-neighbor positive-control phenotype. Crohn disease and ulcerative colitis retained QC flags and were interpreted with sign/QC caution.

## 15. LAVA Local Genetic Correlation

Restricted LAVA tested local genetic correlation for coronary artery disease, psoriatic arthritis, Crohn disease and ulcerative colitis. The main restricted run used the 1000 Genomes European reference and the standard GRCh37/hg19 LAVA genomic partition file. The LDSC cross-trait intercept estimate was entered directly as the psoriasis–outcome off-diagonal value in the LAVA sample-overlap matrix. Negative Crohn disease and ulcerative colitis entries were signed intercept-derived parameters, not negative sample counts. Figure 5 FDR-supported local-r_g counts used all-tests Benjamini-Hochberg FDR < 0.05 from the 1000 Genomes restricted run. Within-outcome FDR was retained separately. UK Biobank European binary LD-reference review classified candidate loci. Local h² reliability required P_local_h² < 0.05 for psoriasis and P_local_h² < 0.05 for the outcome. Tier 1 required concordant local ρ direction across references, reliable local h² in both traits and UKB within-outcome FDR < 0.05. Tier 2 required concordant local ρ direction and reliable local h² in both traits but did not retain UKB within-outcome FDR < 0.05. Tier 3 denoted failed UKB review, unreliable local h² or direction reversal.

## 16. Shared-Locus/eQTL Prioritization

Shared-locus regulatory follow-up was restricted to Tier 1/2 local-r_g loci and prespecified GTEx v8 tissues. Coronary artery disease used skin, whole blood and arterial tissues; psoriatic arthritis used skin and immune-relevant tissues; Crohn disease and ulcerative colitis used skin, whole blood, intestinal and immune-relevant tissues. Candidate genes were derived from eligible local loci and eQTL availability, not from network expansion.

## 17. SMR/HEIDI

SMR/HEIDI used GTEx v8 cis-eQTL data within eligible local-r_g loci. The primary probe set included GTEx probes located within eligible LAVA locus boundaries. A sensitivity resource used ±2 Mb probe-centered windows and merged overlapping intervals before extracting GWAS summary statistics. The eQTL association threshold was P_eQTL < 5 × 10⁻⁸. HEIDI pass was defined as P_HEIDI > 0.01, HEIDI heterogeneity evidence as P_HEIDI ≤ 0.01 and missing HEIDI as not evaluable. Global SMR FDR was the primary multiplicity correction; within-outcome and within-outcome–tissue FDR fields were retained for description.

## 18. Colocalization

Restricted colocalization evaluated whether GWAS and GTEx eQTL association patterns were compatible with a shared association signal under the specified coloc model; it did not prove causality. Locus windows followed eligible LAVA boundaries. eQTL rows were restricted to SNPs with non-missing beta, SE and MAF. GWAS rows required non-missing beta and SE. Matching used rsID when available for at least 50 GWAS variants; otherwise hg38 coordinate keys were used. Alleles were aligned to the eQTL alternate allele: GWAS beta was retained when the GWAS effect allele matched the eQTL alternate allele and sign-flipped when the GWAS effect allele matched the eQTL reference allele. When GWAS effect-allele frequency was available, it was aligned to the eQTL alternate allele and converted to GWAS MAF; otherwise eQTL MAF was used as a proxy and flagged. GWAS and eQTL MAF values were required to be > 0 and < 0.5. Candidate pairs with fewer than 50 matched variants after alignment were considered insufficiently overlapping and were not interpreted. Priors were p1 = 1 × 10⁻⁴, p2 = 1 × 10⁻⁴ and p12 = 1 × 10⁻⁵. The eQTL allele-number field reports allele observations; median allele number divided by two was used to approximate tissue-specific diploid sample count, which is summarized in Supplementary Table S6. PP4 ≥ 0.80 was considered supported, 0.50 ≤ PP4 < 0.80 suggestive and PP3 > PP4 favored distinct rather than shared association signals under the specified model.

## 19. Multiple-Testing Policy

The analysis-specific multiple-testing families, corrections and thresholds are summarized in Supplementary Table S9.

## 20. Evidence Boundaries And Reproducibility

The study separates reproducible tissue-state programs from germline liability and regulatory follow-up. Transcriptomic programs were used for contextual interpretation after their membership was fixed. Genetic analyses used overall psoriasis susceptibility and did not reinterpret F1/F2/F6/F7 as genetically anchored axes. Software and package versions are listed in Supplementary Table S7. Code-to-output traceability is listed in Supplementary Table S8.

# Supplementary Results

Clinical covariate associations were small for the retained programs, with maximum partial R² values summarized in the table below.

| Program   |   Maximum partial R² |
|:----------|---------------------:|
| F1        |           0.0333218  |
| F2        |           0.0472485  |
| F6        |           0.010758   |
| F7        |           0.00765737 |

GSE173706 provided sensitivity evidence only. Directional paired effects and FDR values are summarized below and in Supplementary Data 3.

| Program   | Dominant sensitivity state    | Parent cell type   |   Paired lesional–non-lesional effect |      FDR | Sensitivity confidence   |
|:----------|:------------------------------|:-------------------|--------------------------------------:|---------:|:-------------------------|
| F1        | keratinocyte_inflammatory_T17 | keratinocyte       |                             0.0647195 | 0.278363 | LOW                      |
| F2        | keratinocyte_stress_hypoxia   | keratinocyte       |                             0.0372059 | 0.312439 | LOW                      |
| F6        | keratinocyte_stress_hypoxia   | keratinocyte       |                             0.0935218 | 0.312439 | LOW                      |
| F7        | B_cell_unresolved             | B_cell             |                             0.128239  | 0.622222 | LOW                      |

Spatial dominant-marker results are summarized below. F1, F2 and F6 showed cross-dataset spatial concordance. F7 showed dataset-specific spatial contextualization and was not interpreted as replicated skin-spatial immune context.

| Program   | GSE225475 dominant marker   |   GSE225475 median ρ | GSE202011 dominant marker   |   GSE202011 median ρ | Same marker?   | Allowed interpretation                     |
|:----------|:----------------------------|---------------------:|:----------------------------|---------------------:|:---------------|:-------------------------------------------|
| F1        | keratinocyte_stress_hypoxia |             0.502309 | keratinocyte_stress_hypoxia |             0.489475 | YES            | cross-dataset spatial concordance          |
| F2        | keratinocyte_stress_hypoxia |             0.506033 | keratinocyte_stress_hypoxia |             0.490773 | YES            | cross-dataset spatial concordance          |
| F6        | keratinocyte_stress_hypoxia |             0.54579  | keratinocyte_stress_hypoxia |             0.496115 | YES            | cross-dataset spatial concordance          |
| F7        | keratinocyte_basal          |             0.504906 | keratinocyte_stress_hypoxia |             0.484714 | NO             | dataset-specific spatial contextualization |

Axis-specific MAGMA and matched-null results are summarized below and in Supplementary Data 5.

| Program   |   MAGMA FDR |   Matched-null empirical P | Genetic interpretation                   |
|:----------|------------:|---------------------------:|:-----------------------------------------|
| F1        |    0.81005  |                  0.822089  | TIER D - NO DETECTABLE GENETIC ANCHORING |
| F2        |    0.371692 |                  0.0914543 | TIER D - NO DETECTABLE GENETIC ANCHORING |
| F6        |    0.401227 |                  0.356322  | TIER D - NO DETECTABLE GENETIC ANCHORING |
| F7        |    0.401227 |                  0.201399  | TIER D - NO DETECTABLE GENETIC ANCHORING |

LD-reference review of prioritized LAVA loci is summarized below and in Supplementary Data 6.

| Outcome   | LD-reference review tier   |   Number of loci |
|:----------|:---------------------------|-----------------:|
| cad       | Tier 1                     |                5 |
| cad       | Tier 2                     |                7 |
| cad       | Tier 3                     |                5 |
| crohn     | Tier 1                     |               11 |
| crohn     | Tier 2                     |                1 |
| crohn     | Tier 3                     |                1 |
| psa       | Tier 1                     |               10 |
| uc        | Tier 1                     |                9 |
| uc        | Tier 2                     |                1 |
| uc        | Tier 3                     |                3 |

HEIDI categories from the restricted SMR run are summarized below and in Supplementary Data 7.

| Outcome   | HEIDI category         |   Number of tests |
|:----------|:-----------------------|------------------:|
| cad       | heterogeneity evidence |                33 |
| cad       | not evaluable          |                 3 |
| cad       | pass                   |               385 |
| crohn     | heterogeneity evidence |                47 |
| crohn     | pass                   |               162 |
| psa       | heterogeneity evidence |                37 |
| psa       | not evaluable          |                 1 |
| psa       | pass                   |               274 |
| uc        | heterogeneity evidence |                32 |
| uc        | pass                   |               135 |

Restricted colocalization supported/suggestive counts are summarized below and in Supplementary Data 8.

| Outcome   | Interpretation tier        |   Number of tests |
|:----------|:---------------------------|------------------:|
| psa       | coloc_supported_PP4_ge_0p8 |                 3 |
| uc        | coloc_supported_PP4_ge_0p8 |                 2 |
| cad       | suggestive_PP4_0p5_to_0p8  |                 4 |
| crohn     | suggestive_PP4_0p5_to_0p8  |                 2 |
| psa       | suggestive_PP4_0p5_to_0p8  |                 4 |

# Supplementary Figure Legends

**Supplementary Figure S1. Discrete representation and multi-view factor stability.** The figure summarizes source result tables and is accompanied by panel source data.
**Supplementary Figure S2. Independent paired-skin replication and whole-blood support.** The figure summarizes source result tables and is accompanied by panel source data.
**Supplementary Figure S3. Single-cell and spatial contextualization sensitivity.** The figure summarizes source result tables and is accompanied by panel source data.
**Supplementary Figure S4. Axis-specific genetic anchoring sensitivity.** The figure summarizes source result tables and is accompanied by panel source data.
**Supplementary Figure S5. Genome-wide and local genetic-correlation quality control.** The figure summarizes source result tables and is accompanied by panel source data.
**Supplementary Figure S6. SMR/HEIDI and restricted colocalization sensitivity.** The figure summarizes source result tables and is accompanied by panel source data.

# Supplementary Tables

Supplementary Table S1. Analytical hierarchy and interpretation boundaries.

Supplementary Table S2. Molecular program construction audit.

Supplementary Table S3. Single-cell and spatial marker panels.

Supplementary Table S4. GWAS provenance and harmonization.

Supplementary Table S5. LDSC QC metrics.

Supplementary Table S6. GTEx tissue inputs for colocalization.

Supplementary Table S7. Software and package versions.

Supplementary Table S8. Analysis-to-code reproducibility index.

Supplementary Table S9. Multiple-testing policy.

# Supplementary Data

Supplementary Data 1. Full F1–F8 molecular evidence matrix.

Supplementary Data 2. CORE and EXTENDED gene programs.

Supplementary Data 3. Full single-cell donor/cell-type results.

Supplementary Data 4. Complete spatial marker-program correlation matrix.

Supplementary Data 5. MAGMA and matched-null results.

Supplementary Data 6. LDSC and LAVA results.

Supplementary Data 7. Full SMR/HEIDI outcome–gene results.

Supplementary Data 8. Full colocalization outcome–gene–tissue results.
