# Supplementary Methods

## 1. Overview

These Supplementary Methods document the analytical procedures used to separate reproducible psoriasis tissue-state programs from overall inherited comorbidity liability. The document is a final reproducibility lock based on archived scripts and result tables. No new transcriptomic dataset, molecular axis, gene program, GWAS outcome, regulatory candidate, Mendelian-randomization workflow or network-based workflow was introduced in this pass.

The retained interpretation is deliberately conservative. F1 is treated as a skin-primary tissue-state program, F2 as a skin-primary program with possible field-state support, F6 as a skin-primary program with stress-like features and F7 as a systemic-supportive candidate. None of these programs is described as a validated endotype, a definitive cell-state label or a germline-defined subtype.

## 2. Cohort Definition, Tissue Structure And Dataset Roles

E-MTAB-14509 was used for bulk transcriptomic discovery and internal replication across lesional skin, non-lesional skin and whole blood. The discovery analysis used 82 paired baseline skin patients for the discrete-clustering test and 76 complete baseline patients with all three molecular views for multi-view factor modeling. GSE244679 provided independent paired-skin support. GSE61281 provided external cross-platform whole-blood support. GSE228421 was the primary single-cell contextualization dataset, and GSE173706 was used only as independent single-cell sensitivity support. GSE225475 and GSE202011 were used for spatial transcriptomic contextualization. GCST90472771 represented overall psoriasis susceptibility in genetic analyses, and GTEx v8 supplied tissue eQTL data for regulatory follow-up.

## 3. Discrete Representation And Stability Testing

Discrete clustering was evaluated before the continuous-axis analysis. Discovery lesional-minus-non-lesional normalized expression was restricted to the top 1,000 variable genes, standardized in the discovery set and summarized with principal components. k-means clustering was run for k = 2 to 6 using the first five principal components when available, with random_state = 20260810 and n_init = 100 for the primary fit. Bootstrap stability used 100 resamples; each bootstrap fit used k-means with n_init = 20 and random seeds drawn from the same reproducible random-number stream. Cluster stability was summarized as the minimum best-match bootstrap Jaccard index. A representation required minimum cluster size >= 10 and minimum bootstrap Jaccard >= 0.75 to support a categorical endotype claim. The tested k = 2 representation had a minimum bootstrap Jaccard of 0.562, below this threshold, so categorical endotype claims were not pursued.

## 4. Continuous Multi-View Molecular Axis Discovery

Continuous molecular programs were modeled with MOFA-style multi-view factor analysis across lesional skin, non-lesional skin and whole blood. The model used eight factors and five random seeds: 20260810, 20260811, 20260812, 20260813 and 20260814. Feature matrices were centered by group with scale_views = false and float32 storage. Model options used spike-slab weights and ARD weights. Training used 600 iterations, startELBO = 1, freqELBO = 20 and convergence_mode = fast. Factors were retained for interpretation only after seed stability, view contribution, internal replication, external support, biological interpretability and confounding checks were reviewed. Downstream genetic results were not used to select or rename molecular programs.

## 5. Molecular Program Construction

For each factor, feature families from pathway, regulon, cell-state and leading-edge gene summaries were ranked by absolute loading. The feature-to-gene procedure used the top 30 loading-ranked features per factor and view as the source universe for gene-program construction. CORE genes required support from at least two source features and at least one evidence family. EXTENDED programs included all mapped genes from the retained source features. A fallback top-up rule was available if fewer than 15 CORE genes were obtained, but it was not triggered for the retained programs. CORE/EXTENDED sizes were F1 304/809, F2 725/1184, F6 134/544 and F7 232/507.

## 6. Bulk Replication And Systemic Support

GSE244679 was treated as independent paired-skin support and was not used to establish mechanism. Raw count files were assembled by sample, gene symbols were aggregated by summation and expression was transformed to log2 CPM. Sample titles defined lesional psoriatic skin and adjacent normal skin, and paired replicate identifiers defined 24 lesional/adjacent-normal pairs. For each pair, projected gene-set scores were summarized as lesional minus adjacent-normal differences. Discovery loadings were fixed before projection. Support was quantified as Spearman correlation between discovery factor loadings and external paired score differences over shared axis features. Absolute Spearman ρ was reported because factor sign is arbitrary in latent-factor models. The strongest retained paired-skin supports were F1 in lesional skin (|ρ| = 0.688), F2 in non-lesional skin (|ρ| = 0.518) and F6 in lesional skin (|ρ| = 0.375).

GSE61281 was treated as external cross-platform whole-blood support rather than design-matched replication. The dataset contains 52 Agilent GPL6480 two-colour whole-blood microarray samples: 20 cutaneous psoriasis without arthritis, 20 psoriatic arthritis and 12 unaffected controls. GEO series-matrix values were treated as normalized microarray measurements. Probes were mapped with GPL6480 gene symbols; when multiple symbols were reported, the first symbol was used, empty mappings were removed and probe-level values mapping to the same gene were averaged. Program scores used the same rank-percentile scoring framework as the paired-skin projection. Contrasts were cutaneous psoriasis without arthritis versus control, psoriatic arthritis versus control and psoriasis spectrum versus control. The main F7 support statistic came from psoriasis spectrum versus control in whole blood, with |ρ| = 0.455.

## 7. Clinical And Confounding Audit

Clinical-confounding analyses used factor scores as dependent variables and PASI, BMI, age, sex and HLA-C*06:02 carrier status as covariates. Analyses used complete baseline metadata from the discovery cohort. Factor scores and covariates were standardized before linear regression. For each covariate, a full model including all covariates was compared with a reduced model excluding the tested covariate to estimate partial R². Coefficients, standard errors, t-test P values and Benjamini-Hochberg FDR values were reported across tested factor-covariate pairs. Batch association was recorded as not available because a harmonized batch covariate was not present in the current covariate model. The maximum partial R² values for retained axes were F1 0.033, F2 0.047, F6 0.011, F7 0.008; these analyses audited interpretation and did not determine program membership.

## 8. Primary Single-Cell Contextualization

Retained CORE and EXTENDED gene programs were scored in GSE228421. Program scores were computed per cell and then summarized at donor-by-cell-type level. Lesional versus non-lesional analyses used donor-level statistics rather than treating cells as independent observations. CORE programs were primary, and EXTENDED programs were sensitivity checks. Cell-type localization, lesional/non-lesional direction, patient bootstrap confidence intervals, multi-cell-type FDR, dropout robustness and treatment/timepoint sensitivity were used to evaluate whether a program had coherent cellular context. These analyses localized programs but did not rename or redefine them.

## 9. Independent Single-Cell Sensitivity In GSE173706

GSE173706 was used as an independent single-cell sensitivity dataset because it remains part of the main manuscript and Figure 3. The GEO metadata described 33 skin samples from 23 donors, including 25 psoriasis samples and 8 healthy samples. Tissue states comprised 14 lesional, 11 non-lesional and 8 healthy samples. The source workflow used 10X Chromium libraries sequenced on NovaSeq 6000, Cell Ranger mkfastq/count/aggr v4.0.0 and hg38 alignment. Supplementary raw count CSV files were mapped to gene symbols by removing Ensembl version suffixes and using the archived Ensembl-to-symbol map; duplicate gene symbols were summed. Cells were retained with library size >= 500, detected genes >= 200 and mitochondrial percentage <= 25%. Program scores were mean log1p(CP10K) expression over genes present in each program, with scores treated as missing when fewer than two genes were available. Marker-panel scores assigned coarse and refined cell states. Paired psoriasis lesional versus non-lesional statistics used donor-level summaries, sign-flip testing and 2,000 bootstrap iterations with seed 20260811; FDR was controlled within program type. Healthy comparisons were donor-level Mann-Whitney tests when at least three donors were available in each group. This dataset was interpreted as sensitivity support only. Dominant paired sensitivity effects were F1 0.065, F2 0.037, F6 0.094 and F7 0.128; all retained low-confidence sensitivity labels.

## 10. Spatial Transcriptomic Contextualization

Spatial transcriptomic analyses in GSE225475 and GSE202011 were used for contextualization rather than patient-level replication or evidence of a shared causal spatial unit. For each spatial sample, prespecified CORE program scores were correlated across spots with curated spatial marker programs using Spearman correlation. The reported spatial ρ is the median within-sample spot-level program-marker correlation across samples for the dominant marker program in each dataset. Sections or spots were not treated as independent patients. Dominant-marker consistency is summarized below and in the spatial audit:

- F1: keratinocyte_stress_hypoxia in GSE225475 (median ρ = 0.502) and keratinocyte_stress_hypoxia in GSE202011 (median ρ = 0.489); interpretation: cross-dataset spatial concordance.
- F2: keratinocyte_stress_hypoxia in GSE225475 (median ρ = 0.506) and keratinocyte_stress_hypoxia in GSE202011 (median ρ = 0.491); interpretation: cross-dataset spatial concordance.
- F6: keratinocyte_stress_hypoxia in GSE225475 (median ρ = 0.546) and keratinocyte_stress_hypoxia in GSE202011 (median ρ = 0.496); interpretation: cross-dataset spatial concordance.
- F7: keratinocyte_basal in GSE225475 (median ρ = 0.505) and keratinocyte_stress_hypoxia in GSE202011 (median ρ = 0.485); interpretation: dataset-specific spatial contextualization.

## 11. Axis Genetic Anchoring

Axis-specific genetic anchoring used GCST90472771 psoriasis GWAS summary statistics and retained CORE gene programs. The primary MAGMA analysis used MHC-excluded gene sets to avoid dominance by the extended HLA region. Four primary CORE MHC-excluded tests were corrected with Benjamini-Hochberg FDR. Matched-null sensitivity generated 2,000 random gene sets per axis using seed 20260811. Null sets were matched to axis gene sets on chromosome, gene-length quintile and NSNP quintile where possible, with broad-bin and genome-wide fallback only when exact bins were insufficient. Empirical P values used P_emp = (1 + number of null beta values >= observed beta) / (N + 1). Primary MAGMA FDR values were F1 0.8101, F2 0.3717, F6 0.4012 and F7 0.4012. No retained axis showed robust genetic anchoring.

## 12. GWAS Provenance And Harmonization

The genetic comorbidity analysis used overall psoriasis susceptibility as the exposure layer, represented by GCST90472771. Outcomes with completed LDSC analyses were psoriatic arthritis, Crohn disease, ulcerative colitis, coronary artery disease, ischemic stroke and chronic kidney disease. Prespecified outcomes whose primary sources remained unresolved or unavailable at the computation lock were not treated as null. Summary statistics were harmonized to LDSC-compatible rsID, allele, signed-statistic and HapMap3 reference formats when raw data were available. Dataset provenance, primary/backup source status and QC status are reported in Supplementary Table S4.

## 13. LDSC Genome-Wide Genetic Correlation

LDSC estimated genome-wide genetic correlation (r_g) between overall psoriasis susceptibility and each QC-passing outcome. Analyses recorded r_g, SE, Z, P, FDR, trait heritability, outcome intercept and cross-trait intercept. FDR was controlled across the analyzed psoriasis-comorbidity pairs. Psoriatic arthritis was interpreted as a near-neighbor positive control with elevated cross-trait intercept. Crohn disease and ulcerative colitis were interpreted with QC caution because the negative global r_g estimates and intercept patterns required direction and reference audits. Coronary artery disease provided the clearest non-neighbor systemic genome-wide signal (r_g = 0.173, FDR = 7.49e-10).

## 14. LAVA Local Genetic Correlation And LD-Reference Review

Restricted LAVA localized genome-wide sharing for coronary artery disease, psoriatic arthritis, Crohn disease and ulcerative colitis. The main restricted run used the 1000 Genomes European reference and the GRCh37/hg19 LAVA block definition blocks_s2500_m25_f1_w200. The sample-overlap matrix used LDSC cross-trait-intercept-informed parameters for psoriasis-outcome pairs: psoriasis-PsA 0.3142, psoriasis-Crohn disease -0.0636, psoriasis-ulcerative colitis -0.0625 and psoriasis-CAD 0.0189. These values are signed intercept/covariance parameters for LAVA input, not literal sample-overlap counts.

Figure 5 counts labeled FDR-supported local r_g loci refer to all-tests BH-FDR < 0.05 from the 1000 Genomes restricted LAVA run. Outcome-level local summaries also retained within-outcome FDR. High-priority loci were then reviewed with the UK Biobank European binary LD reference. Tier 3 was assigned if the UKB run failed, local heritability was unreliable in either trait or the local ρ direction changed. Tier 1 required concordant local ρ direction, reliable local heritability in both traits and UKB within-outcome FDR < 0.05. Tier 2 required concordant direction and reliable local heritability with weaker statistical support. Only Tier 1 and Tier 2 loci were eligible for regulatory follow-up. Reviewed tier counts were [{'outcome': 'cad', 'phase4br_tier': 'Tier 1', 'n_loci': 5}, {'outcome': 'cad', 'phase4br_tier': 'Tier 2', 'n_loci': 7}, {'outcome': 'cad', 'phase4br_tier': 'Tier 3', 'n_loci': 5}, {'outcome': 'crohn', 'phase4br_tier': 'Tier 1', 'n_loci': 11}, {'outcome': 'crohn', 'phase4br_tier': 'Tier 2', 'n_loci': 1}, {'outcome': 'crohn', 'phase4br_tier': 'Tier 3', 'n_loci': 1}, {'outcome': 'psa', 'phase4br_tier': 'Tier 1', 'n_loci': 10}, {'outcome': 'uc', 'phase4br_tier': 'Tier 1', 'n_loci': 9}, {'outcome': 'uc', 'phase4br_tier': 'Tier 2', 'n_loci': 1}, {'outcome': 'uc', 'phase4br_tier': 'Tier 3', 'n_loci': 3}].

## 15. Shared-Locus And GTEx eQTL Prioritization

Regulatory follow-up was restricted to Tier 1/2 local loci and prespecified tissues. Coronary artery disease used skin, blood and arterial tissues; psoriatic arthritis used skin and immune-relevant tissues; Crohn disease and ulcerative colitis used skin, blood, intestinal and immune-relevant tissues. Candidate genes were not introduced from network expansion. They arose from locus boundaries, eQTL availability and the restricted follow-up workflow.

## 16. SMR And HEIDI

SMR/HEIDI used GTEx v8 cis-eQTL data to prioritize outcome-gene pairs within eligible local-r_g loci. The primary probe set included GTEx probes located within eligible LAVA locus boundaries. A separate sensitivity analysis used ±2 Mb probe-centered windows and merged overlapping intervals before extracting GWAS summary statistics. Restricted SMR used a 1000 Genomes European LD reference, --peqtl-smr 5e-8, --heidi-min-m 3 and four threads. SMR FDR was calculated globally across restricted rows, with within-outcome and within-outcome-tissue FDR retained for description. HEIDI pass was defined as p_HEIDI > 0.01 when evaluable; p_HEIDI <= 0.01 was treated as heterogeneity evidence under the HEIDI test; missing HEIDI values were not evaluable. Archived HEIDI category totals were {'fail': 149, 'not_evaluable': 4, 'pass': 956}.

## 17. Restricted Colocalization

Restricted colocalization evaluated whether GWAS and GTEx eQTL association patterns were compatible with a shared causal signal under the specified coloc model. It did not prove causality. Locus windows followed eligible LAVA locus boundaries. When lifted GWAS hg38 coordinates were available, eQTL query regions used the minimum and maximum hg38 positions of variants that passed liftover; otherwise original locus boundaries were used. Matching used rsID when at least 50 GWAS variants carried rsID information and hg38 coordinate keys otherwise. Default coloc priors were p1 = 1 × 10^-4, p2 = 1 × 10^-4 and p12 = 1 × 10^-5. GTEx allele-number values were used to estimate effective sample size as median(an)/2 across matched variants, because diploid samples contribute two alleles and variant-level missingness can vary. PP4 >= 0.80 was considered supported, 0.50 <= PP4 < 0.80 suggestive and PP3 > PP4 was interpreted as favoring distinct rather than shared association signals under the specified model. The final restricted set contained 5 supported and 10 suggestive outcome-gene-tissue tests.

## 18. Multiple-Testing And Threshold Conventions

Single-cell contrasts controlled Benjamini-Hochberg FDR within CORE or EXTENDED program type. MAGMA primary inference controlled FDR across four primary CORE MHC-excluded tests and used matched-null empirical P values as sensitivity evidence. LDSC controlled FDR across analyzed psoriasis-comorbidity pairs. LAVA reported both within-outcome and all-tests FDR; Figure 5 all-tests counts used fdr_all_tests < 0.05, whereas UKB-reference Tier 1 used UKB within-outcome FDR < 0.05 after candidate-locus review. SMR used global FDR as the primary multiplicity correction, with within-outcome fields retained for transparency. Coloc used posterior-probability thresholds rather than FDR.

## 19. Evidence Boundaries

The analysis distinguishes three layers: reproducible tissue-state programs, overall inherited psoriasis susceptibility and restricted regulatory candidates at shared loci. A transcriptomic program can be reproducible without being genetically anchored as a psoriasis susceptibility gene set. A genome-wide or local genetic correlation indicates shared inherited architecture but does not identify a shared cis-regulatory mediator. SMR and coloc prioritize candidate regulatory links under model assumptions; they do not establish clinical mechanism or therapeutic readiness.

## 20. Reproducibility Materials

Supplementary Tables S1-S8 provide the analysis hierarchy, molecular-program construction audit, marker panels, GWAS provenance, LDSC QC, GTEx tissue inputs, software versions and code-output index. Supplementary Data 1-8 provide full molecular evidence, CORE/EXTENDED gene programs, single-cell outputs, spatial correlations, MAGMA/matched-null results, LDSC/LAVA results, SMR/HEIDI results and restricted colocalization outputs. Supplementary Figures S1-S6 provide QC and sensitivity visual summaries from archived result tables.

## 21. Supplementary Tables/Data Index

Supplementary Table S1: Analytical hierarchy and interpretation boundaries.

Supplementary Table S2: Molecular program construction audit.

Supplementary Table S3: Single-cell and spatial marker panels.

Supplementary Table S4: GWAS provenance and harmonization.

Supplementary Table S5: LDSC QC metrics.

Supplementary Table S6: GTEx tissue inputs for colocalization.

Supplementary Table S7: Software and package versions.

Supplementary Table S8: Analysis-to-code reproducibility index.

Supplementary Data 1: Full F1-F8 molecular evidence matrix.

Supplementary Data 2: CORE and EXTENDED gene programs.

Supplementary Data 3: Full single-cell donor/cell-type results.

Supplementary Data 4: Complete spatial marker-program correlation matrix.

Supplementary Data 5: MAGMA and matched-null results.

Supplementary Data 6: LDSC and LAVA results.

Supplementary Data 7: Full SMR/HEIDI outcome-gene results.

Supplementary Data 8: Full colocalization outcome-gene-tissue results.
