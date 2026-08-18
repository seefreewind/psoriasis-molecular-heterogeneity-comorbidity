# PHASE 1B Molecular Axis Report

## Executive decision

Phase 1B decision: **CONDITIONAL GO**.

Discrete k=2 endotypes remain documented as a secondary summary because their bootstrap stability did not meet the prespecified threshold. Continuous discovery-only molecular axes are treated as the primary molecular phenotype for downstream design decisions.

## Inputs and lock

- Discovery patients modeled: 76
- Views: lesional skin, nonlesional skin, blood.
- Feature filter: top 450 complete, nonconstant discovery features per view by within-view standard deviation.
- MOFA seeds: 20260810, 20260811, 20260812, 20260813, 20260814; initial factors: 8.

## Factor stability

| factor   |   median_score_abs_pearson_vs_seed1 |   median_loading_abs_spearman_vs_seed1 |   median_top75_jaccard_vs_seed1 |   mean_view_r2_reference | stability_status   |
|:---------|------------------------------------:|---------------------------------------:|--------------------------------:|-------------------------:|:-------------------|
| F1       |                                   1 |                                      1 |                               1 |                 12.9254  | robust             |
| F2       |                                   1 |                                      1 |                               1 |                 12.0497  | robust             |
| F3       |                                   1 |                                      1 |                               1 |                  7.09285 | robust             |
| F4       |                                   1 |                                      1 |                               1 |                  4.44506 | robust             |
| F5       |                                   1 |                                      1 |                               1 |                  3.60332 | robust             |
| F6       |                                   1 |                                      1 |                               1 |                  3.53196 | robust             |
| F7       |                                   1 |                                      1 |                               1 |                  3.22127 | robust             |
| F8       |                                   1 |                                      1 |                               1 |                  3.00892 | robust             |

## Biological annotation

| factor   | stability_status   | dominant_view   |      BLD_r2 |       LS_r2 |       NL_r2 | biology_label_status                      | top_positive_features                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | top_negative_features                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|:---------|:-------------------|:----------------|------------:|------------:|------------:|:------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| F1       | robust             | LS              |  0.787157   | 37.9776     |  0.0113785  | descriptive_only_single_family_or_diffuse | LS::Reactome::EGR2 and SOX10-mediated initiation of Schwann cell myelination; LS::Reactome::RHOU GTPase cycle; LS::Reactome::TGFBR3 expression; LS::Reactome::PKA-mediated phosphorylation of CREB; LS::Reactome::Insulin receptor signalling cascade; LS::Reactome::DAG and IP3 signaling; LS::Reactome::Expression of BMAL (ARNTL), CLOCK, and NPAS2; LS::Reactome::Myogenesis; LS::Reactome::Transcriptional Regulation by NPAS4; LS::Reactome::Signaling by TGFB family members                                                                                                                         | LS::Reactome::Mitochondrial translation; LS::Reactome::Mitochondrial translation initiation; LS::Reactome::Mitochondrial ribosome-associated quality control; LS::Reactome::Mitochondrial translation elongation; LS::Reactome::Autodegradation of Cdh1 by Cdh1:APC/C; LS::Reactome::Mitochondrial protein import; LS::Reactome::Negative regulation of NOTCH4 signaling; LS::Reactome::Vif-mediated degradation of APOBEC3G; LS::Reactome::Autodegradation of the E3 ubiquitin ligase COP1; LS::Reactome::Proteasome assembly                                                                                                                                                                   |
| F2       | robust             | NL              |  0.00184774 |  0.792247   | 35.355      | descriptive_only_single_family_or_diffuse | NL::Reactome::Constitutive Signaling by Aberrant PI3K in Cancer; NL::Reactome::RAC1 GTPase cycle; NL::Reactome::VEGFA-VEGFR2 Pathway; NL::Reactome::RHOA GTPase cycle; NL::Reactome::PI3K/AKT Signaling in Cancer; NL::Reactome::Regulation of CDH11 Expression and Function; NL::Reactome::PI5P, PP2A and IER3 Regulate PI3K/AKT Signaling; NL::Reactome::RAC3 GTPase cycle; NL::Reactome::Negative regulation of the PI3K/AKT network; NL::Reactome::MAPK1/MAPK3 signaling                                                                                                                                | NL::Reactome::tRNA modification in the nucleus and cytosol; NL::Reactome::tRNA processing; NL::Reactome::tRNA modification in the mitochondrion; NL::Reactome::Nucleotide Excision Repair; NL::Reactome::Transcription-Coupled Nucleotide Excision Repair (TC-NER); NL::Reactome::Dual incision in TC-NER; NL::Reactome::Gap-filling DNA repair synthesis and ligation in TC-NER; NL::Reactome::p53-Dependent G1/S DNA damage checkpoint; NL::Reactome::p53-Dependent G1 DNA Damage Response; NL::Reactome::rRNA processing in the nucleus and cytosol                                                                                                                                           |
| F3       | robust             | BLD             | 19.8354     |  0.371206   |  1.072      | labelable_multifamily                     | BLD::Reactome::rRNA modification in the nucleus and cytosol; BLD::Hallmark::HALLMARK_MYC_TARGETS_V2; BLD::Reactome::DNA Damage Recognition in GG-NER; BLD::Reactome::Folding of actin by CCT/TriC; BLD::Reactome::Global Genome Nucleotide Excision Repair (GG-NER); BLD::cell_state::T_cells; BLD::Reactome::Mitochondrial protein degradation; BLD::Reactome::Mitochondrial mRNA modification; BLD::Reactome::tRNA modification in the nucleus and cytosol; BLD::Reactome::rRNA processing in the mitochondrion                                                                                           | BLD::Hallmark::HALLMARK_INFLAMMATORY_RESPONSE; BLD::Reactome::Maternal to zygotic transition (MZT); BLD::Hallmark::HALLMARK_IL6_JAK_STAT3_SIGNALING; BLD::Reactome::Toll Like Receptor 9 (TLR9) Cascade; BLD::Reactome::Toll Like Receptor 7/8 (TLR7/8) Cascade; BLD::regulon_DoRothEA::NFKB1; BLD::Reactome::Toll-like Receptor Cascades; BLD::Reactome::MyD88 dependent cascade initiated on endosome; BLD::Reactome::Toll Like Receptor 4 (TLR4) Cascade; BLD::Hallmark::HALLMARK_TNFA_SIGNALING_VIA_NFKB                                                                                                                                                                                     |
| F4       | robust             | BLD             | 12.5861     |  0.0445008  |  0.704551   | descriptive_only_single_family_or_diffuse | BLD::Reactome::Transcriptional regulation by small RNAs; BLD::Reactome::Inhibition of DNA recombination at telomere; BLD::Reactome::NoRC negatively regulates rRNA expression; BLD::Reactome::Recognition and association of DNA glycosylase with site containing an affected pyrimidine; BLD::Reactome::Depyrimidination; BLD::Reactome::Cleavage of the damaged pyrimidine; BLD::Reactome::CHD6, CHD7, CHD8, CHD9 subfamily; BLD::Reactome::DNA methylation; BLD::Reactome::ERCC6 (CSB) and EHMT2 (G9a) positively regulate rRNA expression; BLD::Reactome::Gene Silencing by RNA                         | BLD::Reactome::RND2 GTPase cycle; BLD::Reactome::Signaling by phosphorylated juxtamembrane, extracellular and kinase domain KIT mutants; BLD::Reactome::Signaling by KIT in disease; BLD::Reactome::Regulation of KIT signaling; BLD::Reactome::Synthesis of PIPs at the early endosome membrane; BLD::Reactome::Interleukin-2 signaling; BLD::Reactome::Gastrin-CREB signalling pathway via PKC and MAPK; BLD::Reactome::ERK/MAPK targets; BLD::Reactome::Downstream signaling of activated FGFR2; BLD::Reactome::Regulation of glycolysis by fructose 2,6-bisphosphate metabolism                                                                                                              |
| F5       | robust             | LS              |  0.0109196  | 10.7937     |  0.00532269 | descriptive_only_single_family_or_diffuse | LS::Hallmark::HALLMARK_MYOGENESIS; LS::Reactome::Defective B3GAT3 causes JDSSDHD; LS::Reactome::Defective B4GALT7 causes EDS, progeroid type; LS::Reactome::Diseases associated with glycosaminoglycan metabolism; LS::Reactome::Defective B3GALT6 causes EDSP2 and SEMDJL1; LS::Reactome::Regulation of clotting cascade; LS::Reactome::Glycosaminoglycan-protein linkage region biosynthesis; LS::Reactome::Coagulation pathway; LS::Reactome::Initiation of coagulation cascade; LS::Reactome::Early SARS-CoV-2 Infection Events                                                                         | LS::Reactome::Regulation of TP53 Activity; LS::Reactome::Regulation of TP53 Activity through Phosphorylation; LS::Reactome::Protein ubiquitination; LS::Reactome::RAB geranylgeranylation; LS::Reactome::Mitotic Telophase/Cytokinesis; LS::Reactome::Condensation of Prometaphase Chromosomes; LS::Hallmark::HALLMARK_MITOTIC_SPINDLE; LS::Reactome::ATF6 (ATF6-alpha) activates chaperones; LS::Reactome::trans-Golgi Network Vesicle Budding; LS::Reactome::SUMOylation                                                                                                                                                                                                                       |
| F6       | robust             | LS              |  0.00235438 |  8.61971    |  1.97383    | labelable_multifamily                     | LS::Reactome::Cellular response to hypoxia; LS::Reactome::Regulation of CDH1 Function; LS::Reactome::AMPK-induced ERAD and lysosome mediated degradation of PD-L1(CD274); LS::Reactome::Degradation of CDH1; LS::Reactome::GLI3 is processed to GLI3R by the proteasome; LS::Reactome::Oxygen-dependent proline hydroxylation of Hypoxia-inducible Factor Alpha; LS::Reactome::Asymmetric localization of PCP proteins; LS::Hallmark::HALLMARK_MYC_TARGETS_V1; LS::Reactome::Regulation of mRNA stability by proteins that bind AU-rich elements; LS::Reactome::Regulation of RUNX3 expression and activity | LS::signaling_PROGENy::p53; LS::regulon_DoRothEA::IRF3; LS::Hallmark::HALLMARK_KRAS_SIGNALING_DN; LS::Reactome::Class C/3 (Metabotropic glutamate/pheromone receptors); LS::Reactome::Stimuli-sensing channels; LS::Reactome::TNFR1-induced proapoptotic signaling; LS::Reactome::Interleukin-37 signaling; LS::Reactome::TNFR1-induced NF-kappa-B signaling pathway; LS::Reactome::Beta-oxidation of very long chain fatty acids; LS::signaling_PROGENy::Trail                                                                                                                                                                                                                                  |
| F7       | robust             | BLD             |  9.65739    |  0.00228286 |  0.00412464 | descriptive_only_single_family_or_diffuse | BLD::Reactome::APOBEC3G mediated resistance to HIV-1 infection; BLD::regulon_DoRothEA::IRF3; BLD::signaling_PROGENy::EGFR; BLD::Reactome::Degradation of cysteine and homocysteine; BLD::Reactome::WNT5A-dependent internalization of FZD2, FZD5 and ROR2; BLD::Reactome::Beta-oxidation of very long chain fatty acids; BLD::Reactome::TNFs bind their physiological receptors; BLD::Reactome::Zinc influx into cells by the SLC39 gene family; BLD::Reactome::Base Excision Repair; BLD::Reactome::Sulfur amino acid metabolism                                                                           | BLD::Reactome::Signaling by CSF3 (G-CSF); BLD::Reactome::Cellular response to starvation; BLD::Reactome::Response of EIF2AK4 (GCN2) to amino acid deficiency; BLD::Reactome::MAP3K8 (TPL2)-dependent MAPK1/3 activation; BLD::Reactome::Influenza Viral RNA Transcription and Replication; BLD::Reactome::Nonsense Mediated Decay (NMD) independent of the Exon Junction Complex (EJC); BLD::Reactome::PELO:HBS1L and ABCE1 dissociate a ribosome on a non-stop mRNA; BLD::Reactome::Viral mRNA Translation; BLD::Reactome::Non-canonical inflammasome activation; BLD::Reactome::ZNF598 and the Ribosome-associated Quality Trigger (RQT) complex dissociate a ribosome stalled on a no-go mRNA |
| F8       | robust             | NL              |  0.00315309 |  0.0108957  |  9.01272    | descriptive_only_single_family_or_diffuse | NL::Reactome::Signaling by ERBB2 ECD mutants; NL::Reactome::Signaling by FGFR4 in disease; NL::Reactome::Constitutive Signaling by EGFRvIII; NL::Reactome::Signaling by EGFRvIII in Cancer; NL::Reactome::Constitutive Signaling by Ligand-Responsive EGFR Cancer Variants; NL::Reactome::Signaling by Ligand-Responsive EGFR Variants in Cancer; NL::Reactome::Signaling by FGFR3; NL::Hallmark::HALLMARK_PROTEIN_SECRETION; NL::Reactome::Signaling by NTRK2 (TRKB); NL::Reactome::Nuclear RNA decay                                                                                                      | NL::Reactome::Heme degradation; NL::Reactome::Retrograde neurotrophin signalling; NL::Reactome::Activation of Matrix Metalloproteinases; NL::Reactome::Post-chaperonin tubulin folding pathway; NL::Reactome::Post-translational modification: synthesis of GPI-anchored proteins; NL::regulon_DoRothEA::IRF3; NL::pathway::Oxidative_stress; NL::Reactome::Signaling by Retinoic Acid; NL::Reactome::Classical antibody-mediated complement activation; NL::Hallmark::HALLMARK_COMPLEMENT                                                                                                                                                                                                       |

## Internal skin replication

| factor   | view   |   n_common_features |   loading_vs_replication_mean_shift_spearman |   replication_projected_score_mean |   replication_projected_score_sd |
|:---------|:-------|--------------------:|---------------------------------------------:|-----------------------------------:|---------------------------------:|
| F1       | LS     |                 450 |                                    0.45681   |                         0.0107389  |                         0.52022  |
| F1       | NL     |                 450 |                                    0.0848971 |                         0.0107389  |                         0.52022  |
| F2       | LS     |                 450 |                                    0.187114  |                        -0.0122025  |                         0.567505 |
| F2       | NL     |                 450 |                                   -0.527544  |                        -0.0122025  |                         0.567505 |
| F3       | LS     |                 450 |                                   -0.0600722 |                         0.00407449 |                         0.177557 |
| F3       | NL     |                 450 |                                    0.220623  |                         0.00407449 |                         0.177557 |
| F4       | LS     |                 450 |                                    0.145683  |                         0.00190241 |                         0.210192 |
| F4       | NL     |                 450 |                                    0.0797118 |                         0.00190241 |                         0.210192 |
| F5       | LS     |                 450 |                                   -0.29607   |                        -0.00507665 |                         0.288276 |
| F5       | NL     |                 450 |                                    0.0456002 |                        -0.00507665 |                         0.288276 |
| F6       | LS     |                 450 |                                    0.125892  |                         0.00313365 |                         0.281927 |
| F6       | NL     |                 450 |                                    0.0272133 |                         0.00313365 |                         0.281927 |
| F7       | LS     |                 450 |                                    0.0373489 |                         0.00298244 |                         0.135237 |
| F7       | NL     |                 450 |                                    0.135281  |                         0.00298244 |                         0.135237 |
| F8       | LS     |                 450 |                                    0.0882937 |                         0.00615103 |                         0.24761  |
| F8       | NL     |                 450 |                                    0.272942  |                         0.00615103 |                         0.24761  |

## Discovery cross-tissue blood support

| factor   |   skin_weighted_score_vs_blood_weighted_score_pearson |   skin_weighted_score_vs_blood_weighted_score_spearman |   BLD_view_r2 |   LS_view_r2 |   NL_view_r2 |
|:---------|------------------------------------------------------:|-------------------------------------------------------:|--------------:|-------------:|-------------:|
| F1       |                                              0.559407 |                                               0.514258 |    0.787157   |  37.9776     |   0.0113785  |
| F2       |                                              0.687216 |                                               0.594313 |    0.00184774 |   0.792247   |  35.355      |
| F3       |                                              0.617387 |                                               0.582392 |   19.8354     |   0.371206   |   1.072      |
| F4       |                                              0.552287 |                                               0.544689 |   12.5861     |   0.0445008  |   0.704551   |
| F5       |                                              0.275026 |                                               0.306056 |    0.0109196  |  10.7937     |   0.00532269 |
| F6       |                                              0.571905 |                                               0.505263 |    0.00235438 |   8.61971    |   1.97383    |
| F7       |                                              0.607876 |                                               0.576815 |    9.65739    |   0.00228286 |   0.00412464 |
| F8       |                                              0.63064  |                                               0.628626 |    0.00315309 |   0.0108957  |   9.01272    |

## Clinical/confounding audit

Associations are multivariable standardized OLS coefficients for each axis against PASI, BMI, age, sex, and HLA-C*06:02 carrier status. These are not used to choose axes.

| factor   | covariate         |   n |       beta |     pvalue |   partial_r2 |   full_model_r2 |      fdr |
|:---------|:------------------|----:|-----------:|-----------:|-------------:|----------------:|---------:|
| F3       | bmi               |  76 |  0.331143  | 0.00917924 |   0.0930385  |       0.127047  | 0.36717  |
| F4       | age               |  76 | -0.258344  | 0.0284033  |   0.0667753  |       0.110117  | 0.568067 |
| F3       | pasi              |  76 | -0.220612  | 0.061766   |   0.0489639  |       0.127047  | 0.666333 |
| F2       | bmi               |  76 | -0.235996  | 0.0666333  |   0.0472485  |       0.0828616 | 0.666333 |
| F4       | hla_c0602_carrier |  76 |  0.196583  | 0.0935879  |   0.0396447  |       0.110117  | 0.748703 |
| F1       | bmi               |  76 | -0.198964  | 0.124847   |   0.0333218  |       0.0621464 | 0.832313 |
| F1       | sex               |  76 | -0.179761  | 0.153892   |   0.0288303  |       0.0621464 | 0.879383 |
| F5       | pasi              |  76 | -0.162751  | 0.186911   |   0.0247495  |       0.036153  | 0.934553 |
| F8       | age               |  76 | -0.124109  | 0.305949   |   0.0149667  |       0.0328488 | 0.936896 |
| F1       | age               |  76 | -0.118119  | 0.322321   |   0.0139943  |       0.0621464 | 0.936896 |
| F6       | hla_c0602_carrier |  76 | -0.105866  | 0.38592    |   0.010758   |       0.0203269 | 0.936896 |
| F6       | sex               |  76 | -0.109992  | 0.391074   |   0.010528   |       0.0203269 | 0.936896 |
| F2       | age               |  76 |  0.0997347 | 0.397638   |   0.0102412  |       0.0828616 | 0.936896 |
| F1       | hla_c0602_carrier |  76 | -0.0991033 | 0.406687   |   0.00985675 |       0.0621464 | 0.936896 |
| F7       | pasi              |  76 |  0.0903277 | 0.464825   |   0.00765737 |       0.0235823 | 0.936896 |
| F7       | hla_c0602_carrier |  76 | -0.0841616 | 0.489498   |   0.0068486  |       0.0235823 | 0.936896 |
| F7       | age               |  76 |  0.0822874 | 0.498414   |   0.00657253 |       0.0235823 | 0.936896 |
| F2       | pasi              |  76 | -0.0793889 | 0.507285   |   0.00630593 |       0.0828616 | 0.936896 |
| F8       | pasi              |  76 | -0.0766933 | 0.532701   |   0.00558471 |       0.0328488 | 0.936896 |
| F8       | sex               |  76 | -0.0773855 | 0.543113   |   0.00530658 |       0.0328488 | 0.936896 |

## Axes versus discrete clusters

| factor   |   cluster_auc_from_all_axes_cv |   endotype_mean_range_on_axis |   within_endotype_variance_mean |   total_axis_variance |   fraction_axis_variance_left_within_clusters |
|:---------|-------------------------------:|------------------------------:|--------------------------------:|----------------------:|----------------------------------------------:|
| F1       |                       0.907971 |                    0.107315   |                        1.40258  |              1.44066  |                                      0.973566 |
| F2       |                       0.907971 |                    1.49635    |                        0.59992  |              1.1399   |                                      0.526293 |
| F3       |                       0.907971 |                    0.548097   |                        1.59859  |              1.72246  |                                      0.928085 |
| F4       |                       0.907971 |                    0.253154   |                        1.32031  |              1.29224  |                                      1.02172  |
| F5       |                       0.907971 |                    0.00492998 |                        0.90987  |              0.934547 |                                      0.973595 |
| F6       |                       0.907971 |                    0.362626   |                        0.650534 |              0.730754 |                                      0.890223 |
| F7       |                       0.907971 |                    0.19112    |                        0.828119 |              0.83944  |                                      0.986514 |
| F8       |                       0.907971 |                    0.300061   |                        0.866893 |              0.943093 |                                      0.919202 |

## External dataset audit

External datasets were checked against official GEO records and cached with checksums. After the second external-replication pass, GSE244679 is analysis-ready as 48 raw per-sample count files from 24 paired lesional psoriatic and adjacent normal skin samples. GSE61281 was handled through its GEO series matrix and GPL6480 platform annotation rather than the 816 Mb raw tar; 30,723 mapped probes were aggregated to 19,553 gene symbols.

| accession   | tissue      | technology         | compatibility_role                          | download_status                         |
|:------------|:------------|:-------------------|:--------------------------------------------|:----------------------------------------|
| GSE121212   | skin        | RNA-seq            | external_skin_replication_candidate         | already_present                         |
| GSE244679   | skin        | RNA-seq            | external_skin_replication_candidate         | already_present_complete                |
| GSE54456    | skin        | RNA-seq            | external_skin_support_unpaired              | already_present                         |
| GSE147339   | whole blood | RNA-seq            | external_blood_support_candidate            | already_present                         |
| GSE61281    | whole blood | Agilent microarray | external_blood_support_microarray_candidate | analysis_ready_series_matrix_and_platform_annotation |

## External axis support

The external support analyses reused the frozen Phase 1B gene-set definitions, including corrected PROGENy and DoRothEA scores. Factor signs are arbitrary in latent-factor models, so the sign of each external correlation should be interpreted as orientation rather than biological direction unless an axis is later anchored to a named phenotype.

GSE121212 remained weak as an immediate paired-skin support dataset. GSE244679 added a stronger independent paired-skin test: several axes showed moderate-to-strong loading-vs-lesional-minus-adjacent correlations, especially F1-LS, F2-NL, F6-LS, F3-NL, and F5-LS.

| dataset   | axis   | view   |   n_pairs |   n_common_axis_features |   loading_vs_paired_lesional_minus_adjacent_spearman |
|:----------|:-------|:-------|----------:|-------------------------:|-----------------------------------------------------:|
| GSE244679 | F1     | LS     |        24 |                      424 |                                            -0.688398 |
| GSE244679 | F2     | NL     |        24 |                      423 |                                            -0.518229 |
| GSE244679 | F6     | LS     |        24 |                      424 |                                             0.375292 |
| GSE244679 | F3     | NL     |        24 |                      423 |                                            -0.356222 |
| GSE244679 | F5     | LS     |        24 |                      424 |                                            -0.355320 |
| GSE244679 | F7     | NL     |        24 |                      423 |                                             0.203905 |

External blood support was weaker and platform-dependent. GSE147339 whole-blood RNA-seq showed only small correlations across all axes. GSE61281, after GPL6480 probe-to-gene mapping, showed moderate support for F7 across PsC, PsA, and combined psoriasis-spectrum contrasts, plus smaller support for F3 and F2. Because GSE61281 is an Agilent two-color microarray study with PsA/PsC/control groups rather than the E-MTAB-14509 longitudinal RNA-seq design, these results are treated as external blood support rather than full blood replication.

| dataset   | contrast                                            | strongest_axis |   spearman |
|:----------|:----------------------------------------------------|:---------------|-----------:|
| GSE147339 | psoriasis_minus_control                             | F4             |  -0.173351 |
| GSE61281  | cutaneous_psoriasis_without_arthritis_minus_control | F7             |  -0.399880 |
| GSE61281  | psoriatic_arthritis_minus_control                   | F7             |  -0.435931 |
| GSE61281  | psoriasis_spectrum_minus_control                    | F7             |  -0.454939 |
| GSE61281  | psoriasis_spectrum_minus_control                    | F3             |   0.262383 |
| GSE61281  | psoriatic_arthritis_minus_control                   | F2             |  -0.258128 |

## Interpretation boundary

Phase 1B now supports a skin-primary molecular-axis manuscript with external paired-skin support. It still does not support a strong replicated multisystem endotype claim, because E-MTAB-14509 replication lacks blood RNA-seq and the two external blood datasets provide support rather than design-matched replication. Downstream single-cell/spatial, GWAS, MR, colocalization, or multisystem comorbidity phases should proceed only if the manuscript is framed around skin-primary continuous axes with cautious blood support.
