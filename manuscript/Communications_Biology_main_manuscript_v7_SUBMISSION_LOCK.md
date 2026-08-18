# Molecular heterogeneity and multisystem shared genetic architecture define distinct biological layers of psoriasis

Yu Zhang1, Ying Chen2, Yue Liu2 and Da Lin1

1 Department of Ophthalmology, The Second Affiliated Hospital of Wenzhou Medical University, No. 109 Xueyuan West Road, Lucheng District, Wenzhou, Zhejiang Province, China

2 Wenzhou Medical University, Wenzhou, Zhejiang Province, China

Correspondence: Da Lin, 212574@wzhealth.com; ORCID 0009-0009-4410-0218




## Abstract

Psoriasis shows both marked tissue molecular heterogeneity and systemic genetic comorbidity, but whether these forms of heterogeneity reflect the same underlying biology remains unclear. We tested this correspondence by integrating cross-tissue psoriasis transcriptomics with independent bulk, cellular, spatial and genetic evidence under a prespecified analytical framework. A tested discrete k = 2 representation did not meet the prespecified stability criterion (minimum bootstrap Jaccard 0.562), whereas continuous multi-view modeling of 76 complete baseline patients yielded reproducible molecular programs. F1, F2 and F6 showed independent paired-skin replication and directional cellular/spatial contextualization, whereas F7 remained a systemic-supportive candidate. None of the four programs met prespecified criteria for robust axis-specific genetic anchoring. Overall psoriasis susceptibility nevertheless showed disease-specific shared genetic architecture, including positive sharing with coronary artery disease and strong near-neighbor sharing with psoriatic arthritis, while local analyses revealed directionally heterogeneous psoriasis-IBD architecture. Restricted regulatory prioritization and colocalization identified a limited set of supported or suggestive candidates, but these showed no direct gene-membership overlap with the retained molecular programs. These findings support a model in which reproducible psoriasis tissue states and inherited multisystem liability are connected but non-equivalent biological layers.

## Introduction

Psoriasis is increasingly being resolved at two biological scales: molecular heterogeneity within affected tissue and inherited susceptibility shared across organ systems. Recent transcriptomic studies have begun to define molecular states within clinically similar disease [2-4], and single-cell/spatial studies have mapped cellular ecosystems in psoriatic tissue [5,6]. Large-scale genetic studies have mapped psoriasis susceptibility and genetic sharing with inflammatory and cardiometabolic traits [1,7-10]. Yet these advances have largely proceeded in parallel. One map describes how lesional skin, clinically uninvolved skin and blood differ in transcriptional state. The other describes how inherited psoriasis liability covaries with psoriatic arthritis, cardiovascular disease and inflammatory bowel disease. These maps generate different biological expectations: tissue-state maps emphasize local inflammation, repair, cellular composition and disease activity, whereas genetic maps emphasize inherited covariance between disease liabilities. Whether these two maps coincide remains unclear. If they do, molecular states in skin could provide a tissue readout of systemic inherited risk. If they do not, psoriasis heterogeneity and comorbidity genetics must be interpreted as related but separable layers. Clinical and genetic comorbidity may reflect shared immune pathways, tissue-independent inherited susceptibility or downstream effects of chronic inflammation, but it does not establish that the molecular states observed within psoriatic tissue are themselves genetically encoded systemic disease states.

Molecular endotyping is an active frontier in psoriasis biology. Recent work in the PSORT cohort established a rich substrate for molecular stratification across skin and blood, identifying phenotype- and severity-associated gene modules, latent factors and predictive signatures in the same PSORT transcriptomic resource (E-MTAB-14509) used here [2]. Other transcriptomic studies have linked molecular profiles to disease severity and therapeutic response [4], while a recent Taiwanese study described a dual T helper 17/type 2 transcriptomic endotype with prominent IL-36 activation [3]. Single-cell and spatial studies have further shown that keratinocytes, fibroblasts and immune niches organize inflammatory signals across psoriatic tissue [5,6]. These studies establish that psoriasis contains substantial molecular heterogeneity. They do not, by themselves, determine the most appropriate mathematical representation of that heterogeneity. Disease states may vary continuously across tissue compartments, and unstable clustering can impose artificial boundaries on gradients of inflammation, remodeling or systemic immune activity. They leave open a narrower question: whether this heterogeneity forms reproducible discrete patient classes, whether continuous tissue programs provide a more stable representation, and whether either representation corresponds to inherited multisystem disease architecture.

Large-scale psoriasis genetics has also moved beyond locus discovery toward mapping cross-trait and systemic genetic architecture. A recent GWAS meta-analysis of 18 studies, including 36,466 cases and 458,078 controls, identified 109 distinct psoriasis susceptibility loci, connected psoriasis risk to immune regulation and therapeutic targets, and assessed genome-wide correlation with hundreds of disease and health-related traits [7]. Genetic studies have also separated aspects of psoriatic arthritis and cutaneous psoriasis architecture, identified shared psoriasis-Crohn disease loci, and reported shared genetic risk between psoriasis and coronary artery disease [8-10]. These analyses generally treat psoriasis as a single susceptibility phenotype. That design is powerful for mapping disease-level liability, but it does not reveal whether genetically shared comorbidity risk is concentrated in particular molecular states observed in skin or blood. Whether shared systemic genetic architecture is partitioned according to the molecular programs observed within psoriasis tissue remains unknown. This distinction is biologically important because tissue transcriptional states integrate inherited susceptibility with inflammation, cellular composition, environmental exposure, tissue injury and disease activity. Germline genetic correlation, by contrast, captures inherited covariance between disease liabilities. A reproducible tissue program therefore need not constitute an inherited genetic subtype, and systemic shared genetics need not map directly onto dominant transcriptional states in affected skin.

Here, we asked whether reproducible molecular heterogeneity in psoriasis tissue corresponds to distinct inherited architectures of systemic comorbidity. We integrated cross-tissue transcriptomics with independent bulk, single-cell and spatial validation, tested whether retained molecular programs were independently anchored by psoriasis susceptibility genetics, and then characterized genome-wide and local comorbidity sharing with restricted regulatory prioritization. This design allowed us to test, rather than assume, whether tissue molecular heterogeneity and systemic inherited risk represent a common biological axis. By separating these questions, we sought to distinguish tissue-state molecular heterogeneity from inherited multisystem disease sharing in psoriasis.

## Results

### Continuous molecular programs capture reproducible psoriasis tissue heterogeneity

The initial transcriptomic analysis evaluated whether patients could be separated into stable discrete molecular endotypes. The k = 2 solution did not meet the predefined stability rule: the minimum bootstrap Jaccard index was 0.562, below the 0.75 threshold used to support stable cluster membership. This result did not support a discrete-endotype interpretation and prevented a categorical endotype claim.

The analysis then moved to continuous multi-view molecular modeling. MOFA modeled 76 complete baseline discovery patients across lesional skin, non-lesional skin and blood, and eight factors were stable across five random seeds. A prespecified prioritization matrix selected F1, F2, F6 and F7 for manuscript-level interpretation. F1, F2 and F6 were retained as skin-primary bulk molecular programs, whereas F7 was retained only as a systemic/supportive candidate. This selection was based on stability, tissue contribution, internal replication, external replication and biological interpretability, not on a single nominal association.

Independent paired-skin replication supported the skin-primary interpretation. In GSE244679, F1 showed the strongest lesional-skin support (|rho| = 0.688), F2 showed non-lesional support (|rho| = 0.518), and F6 showed lesional-skin support (|rho| = 0.375). These results support a continuous molecular-program framework while keeping mechanism naming conservative. The final molecular-program interpretation is summarized in Table 2.

### Selected molecular programs show directional cellular and spatial organization

Single-cell and spatial analyses were used to contextualize the retained programs, not to redefine them. The main statistical unit was donor or sample-level summarized signal rather than individual cells treated as independent observations. GSE228421 provided the primary donor-level single-cell localization analysis, with GSE173706 used as an independent sensitivity dataset. These analyses supported directional keratinocyte/stress-inflammatory localization for the skin-primary programs but did not justify strong cell-state naming.

Spatial transcriptomics provided consistent directional context. F1, F2 and F6 showed positive spatial correlations in both spatial datasets: F1 showed rho = 0.502 in GSE225475 and rho = 0.489 in GSE202011; F2 showed rho = 0.506 and rho = 0.491; F6 showed rho = 0.546 and rho = 0.496. F7 also showed positive spatial correlations (rho = 0.505 and rho = 0.485), but its broader evidence did not support coherent skin-spatial immune localization. It therefore remained a low-confidence systemic/supportive candidate.

These findings support directional cellular and spatial organization for the selected tissue programs. They do not support claims that F1, F2 or F6 are definitive keratinocyte endotypes, nor that F7 is a skin-localized immune axis.

### Reproducible molecular programs do not define independent inherited genetic axes

The retained F1, F2, F6 and F7 programs were next tested for axis-specific psoriasis genetic anchoring. This test was performed before multisystem genetics to avoid interpreting genetic results through mutable transcriptomic labels. All four programs fell into the lowest evidence category in the final genetic evidence table. No program met the predefined threshold for a robust genetically anchored molecular axis.

This result constrained the downstream genetic interpretation. The tissue programs remained valid transcriptomic findings with replication and contextual support, but they were not carried forward as axis-specific genetic variables. Subsequent comorbidity analyses therefore used overall psoriasis susceptibility from GCST90472771 as the genetic reference. This decision is central to the final interpretation: transcriptomic heterogeneity and inherited comorbidity architecture are not collapsed into a single axis-specific genetic mechanism.

### Overall psoriasis susceptibility shows disease-specific multisystem genetic sharing

The genome-wide genetic correlation analysis tested LDSC genetic correlation between overall psoriasis susceptibility and prespecified comorbidity outcomes. Six outcomes passed data availability and QC sufficiently for the formal LDSC table. Coronary artery disease provided the cleanest non-neighbor systemic signal, with rg = 0.1732, SE = 0.0274, P = 2.498e-10 and FDR = 7.494e-10, with QC status PASS.

Psoriatic arthritis behaved as a positive-control and near-neighbor phenotype rather than an independent multisystem discovery. It showed very high genetic correlation with psoriasis (rg = 1.1715, SE = 0.0751, P = 6.746e-55, FDR = 4.048e-54), but the result carried a near-neighbor and elevated cross-trait-intercept label. Crohn disease and ulcerative colitis showed significant negative genetic correlations: Crohn disease rg = -0.2717, SE = 0.0449, P = 1.434e-09, FDR = 2.868e-09; ulcerative colitis rg = -0.2233, SE = 0.0409, P = 4.820e-08, FDR = 7.229e-08. Both IBD outcomes were retained with QC flags because their h2 and cross-trait intercepts required cautious interpretation.

Ischemic stroke and chronic kidney disease were null or low-power references in the available data. Ischemic stroke showed rg = 0.0255 and P = 0.6647; chronic kidney disease showed rg = 0.0118 and P = 0.7912. Type 2 diabetes, MASLD, major depressive disorder and uveitis were not treated as null because their prespecified primary data sources remained unresolved or unavailable in the completed analysis.

### Local genetic correlation reveals heterogeneous comorbidity architectures

Restricted LAVA was applied after the global LDSC analysis and after sign/QC adjudication. The aim was to identify where psoriasis-comorbidity sharing was concentrated and whether local architecture was concordant or heterogeneous across disease systems. CAD remained the primary systemic target. In CAD, 118 loci had bivariate local tests, 23 loci were FDR-supported in the full restricted report, and the median local rho was 0.0787. Positive nominal local signals outnumbered negative nominal signals (21 versus 10), and the leading CAD locus reached rho = 0.6508.

Psoriatic arthritis served as a positive-control local architecture. It showed strong positive sharing, with 40 bivariate loci, 31 FDR-supported loci, 36 nominal positive loci, no nominal negative loci and median rho = 0.6315. This pattern was consistent with the high global genetic correlation and the near-neighbor nature of the trait.

Crohn disease and ulcerative colitis showed directionally heterogeneous local architectures. Crohn disease had 131 bivariate loci, 49 FDR-supported loci, 9 nominal positive loci, 51 nominal negative loci and median rho = -0.2078. Ulcerative colitis had 98 bivariate loci, 19 FDR-supported loci, 7 nominal positive loci, 18 nominal negative loci and median rho = -0.0479. Locus 57 was prominent in both IBD analyses, with negative local rho estimates. These results argue against reducing psoriasis-IBD genetics to a single genome-wide direction and instead support locus-level heterogeneity.

### Restricted regulatory prioritization separates shared genetic architecture from shared regulatory signals

The final regulatory step used only prespecified shared-locus candidates and relevant GTEx v8 eQTL tissues. SMR/HEIDI prioritized 91 outcome-gene rows, and the highest prespecified tier contained 33 genes. A second probe-window sensitivity retained 100% of SMR1 outcome-gene candidates at the gene level, supporting the stability of the restricted prioritization set.

Colocalization further refined this set. Among manuscript-relevant candidates, PsA showed three PP4-supported signals, including SLC22A5 in spleen (PP4 = 0.971) and lymphoblastoid-cell RP11-977G19.11 (PP4 = 0.945), plus SLC22A5 in lymphoblastoid cells (PP4 = 0.934). Ulcerative colitis showed two PP4-supported RP11-973H7.1 signals in transverse and sigmoid colon (PP4 = 0.960 and 0.960), both using eQTL MAF proxy inputs. CAD did not yield a high-confidence PP4 signal in the restricted coloc analysis, but skin UBQLN4 and MEX3A at locus 113 were suggestive (PP4 range 0.595-0.754). Crohn disease produced suggestive SLC22A5 and PARK7 signals (PP4 = 0.639 and 0.565), both with eQTL MAF proxy sensitivity flags.

We next tested whether PP4-supported or suggestive coloc genes overlapped the retained F1/F2/F6/F7 CORE/EXTENDED gene programs. No supported or suggestive regulatory candidate showed direct gene-membership overlap with the retained molecular programs. This result reinforces the layered interpretation: the regulatory candidates contextualize overall psoriasis-comorbidity genetics, while the tissue molecular programs contextualize transcriptomic heterogeneity. They should not be merged into axis-specific genetic claims.

## Discussion

This study separates two biological layers that can be conflated in molecular stratification studies of psoriasis: the molecular state of diseased tissue and the inherited liability that links psoriasis to systemic disease. Across bulk transcriptomic discovery, independent skin replication, donor-level single-cell contextualization and spatial transcriptomic support, the reproducible signal was not a stable categorical partition of patients. It was a set of continuous tissue molecular programs, strongest for skin-primary programs F1, F2 and F6, with F7 retained as a systemic-supportive candidate rather than as a skin-localized mechanism. The genetic analyses then drew a second boundary. These transcriptomic programs did not become genetically anchored psoriasis axes, whereas overall psoriasis susceptibility showed shared genome-wide and local architecture with selected comorbid diseases. This separation is important because a tissue-state signal and a liability signal answer different biological questions. The former describes the configuration of inflamed tissue at sampling, whereas the latter describes inherited covariance across disease risks. A useful model is therefore layered rather than linear: psoriasis contains reproducible inflammatory and tissue-remodelling states, while inherited susceptibility operates at a broader liability layer that can intersect cardiovascular, articular and intestinal disease systems. Recent large-scale immune-cell mapping across immune-mediated inflammatory diseases similarly emphasizes shared and disease-specific inflammatory states across conditions that include psoriasis, psoriatic arthritis, Crohn disease and ulcerative colitis, but those maps should be read here as conceptual context rather than validation of the factors identified in this study [17].

This layered view refines transcriptomic endotype work in psoriasis. Recent studies have reported psoriasis expression signatures associated with endotypes, disease severity, response and mixed inflammatory patterns [2-4]. Our analysis reached a different emphasis because the first decision point was not whether transcriptomic heterogeneity exists, but whether a discrete k = 2 patient boundary is stable enough to carry a mechanistic and translational claim. In the matched multi-tissue discovery setting used here, bootstrap stability did not support that categorical boundary, so we shifted the unit of interpretation from class labels to continuous molecular axes. This result should not be read as evidence that psoriasis has no categorical endotypes under any design. It shows that, in these paired skin-blood data, a binary endotype model was less robust than continuous programs. The biological consequences of these two models are different. A categorical endotype implies patient subgroup assignment and potential stratification. A continuous program supports language about graded tissue states, field effects and pathway intensity. The latter is a narrower claim, but it is also more faithful to the evidence generated here.

The absence of robust axis-specific genetic anchoring is biologically interpretable. Germline risk variants act before lesion formation, treatment exposure, local immune recruitment and tissue repair. Bulk and single-cell transcriptomic programs are measured after these processes have already interacted with microenvironment, disease activity and sampling context. It is therefore plausible for F1, F2 and F6 to be reproducible skin tissue-state variables without being independent inherited axes. F7 occupies a slightly different position. Its internal skin-blood support and external blood support make it the best systemic-supportive candidate in the molecular layer, but its low-confidence skin-spatial localization argues against treating it as a pan-inflammatory psoriasis axis. Large psoriasis GWAS meta-analysis continues to expand the set of inherited susceptibility loci and implicates immune and skin-relevant biology [7], yet those loci need not map one-to-one onto latent transcriptomic factors measured in diseased tissue. This result does not diminish the reproducibility of the molecular programs. It constrains their interpretation as tissue-state variables rather than germline-defined subtypes, and it supports anchoring comorbidity genetics to overall psoriasis susceptibility.

Within the comorbidity layer, coronary artery disease was the cleanest non-neighbor signal. Psoriasis and coronary artery disease showed a positive genome-wide genetic correlation, passed the main LDSC quality-control criteria, and yielded multiple positive local LAVA signals. This finding is directionally consistent with previous evidence that psoriasis shares genetic risk with coronary artery disease and cardiovascular traits [8,18], and it provides a stronger basis for discussing cardiovascular comorbidity than the tissue-axis genetic analyses did. It also shifts the interpretation away from a generic epidemiological comorbidity statement. The CAD signal is a genetic-architecture result: psoriasis liability and CAD liability share measurable polygenic covariance, and that covariance is concentrated at multiple loci rather than being visible only as a diffuse genome-wide estimate. The regulatory follow-up places a clear limit on the interpretation. Although CAD had recurrent Tier A SMR/HEIDI-prioritized genes and suggestive coloc signals for UBQLN4 and MEX3A in skin tissues, no CAD gene-tissue pair reached the prespecified PP4-supported threshold. Thus, the CAD result supports shared polygenic architecture, not a single shared cis-eQTL mediator. Several explanations remain compatible with the data: the covariance may be distributed across many variants with small effects; shared loci may act through disease-, cell-state- or stimulation-dependent regulatory effects absent from baseline GTEx tissues [15,20]; or the relevant mediator may not be captured by the eQTL panels used here. The conservative claim is not that CAD lacks a shared regulatory mechanism with psoriasis. It is that this analysis did not identify a high-confidence shared CAD eQTL mediator after restricted coloc filtering.

The intestinal disease results require explicit handling because the direction of the genome-wide correlations differs from recent external literature. In our LDSC analysis, Crohn disease and ulcerative colitis showed significant negative genetic correlations with psoriasis, but both traits carried elevated heritability-intercept and cross-trait-intercept warnings. A 2026 harmonized population study reported positive genetic correlations of psoriasis with Crohn disease and ulcerative colitis [19], and older shared-locus work also supports genetic overlap between psoriasis and Crohn disease [10]. The discrepancy makes a simple directional statement inappropriate. The most defensible interpretation is that the current IBD results expose directional heterogeneity and quality-control sensitivity rather than a stable negative liability relationship. Restricted LAVA was informative in this respect: Crohn disease and ulcerative colitis contained both positive and negative local correlations, with negative local signals more prominent in the current analysis. That pattern is compatible with a genome in which different loci connect psoriasis and IBD through different immunological or regulatory directions. It is also compatible with residual differences in phenotype definition, ancestry or sample composition, sample overlap, variant coverage, LD reference structure and the balance of positive and negative local covariance. In practical terms, the IBD finding should be used to motivate locus-level follow-up and cross-source direction checks, not to rewrite the known clinical or genetic relationship between psoriasis and intestinal inflammation. For this reason, the IBD section should be framed around local directional heterogeneity and the need for adjudicated replication, not around a stable globally negative biological relationship.

The LDSC-to-LAVA-to-SMR/HEIDI-to-coloc sequence gives the genetic layer a useful hierarchy. LDSC defined the genome-wide liability relationship, LAVA localized where sharing was concentrated, SMR/HEIDI prioritized gene-level regulatory associations within prespecified shared loci, and coloc evaluated whether the association patterns were compatible with a shared causal signal under the specified model. The 100% gene-level retention from SMR to SMR2 indicates prioritization stability under the recurrent SMR2 screen; it does not constitute causal replication. Among 91 prespecified outcome-gene rows, 33 reached the highest SMR/HEIDI tier, but strong coloc support was restricted. PsA functioned as a positive-control near-neighbor phenotype with PP4-supported regulatory signals, and UC had PP4-supported RP11-973H7.1 signals under an eQTL MAF-proxy sensitivity setting. CAD and Crohn disease remained suggestive rather than PP4-supported in the restricted coloc table. The absence of direct gene-membership overlap between these coloc-supported or suggestive genes and the retained F1/F2/F6/F7 programs is also informative. It argues against a direct axis-to-coloc-gene narrative and supports a scale distinction: a coloc gene is a candidate inherited cis-regulatory perturbation at a locus, whereas a molecular program is an emergent multicellular tissue response. Disease-context and cell-type-resolved eQTL studies in IBD show that many regulatory effects are cell-type-specific or context-restricted and may be missed in bulk reference tissue maps [20]. This reinforces the need to interpret GTEx-based coloc as restricted regulatory prioritization rather than final mechanism assignment.

Several limitations define how far this model should be taken. First, the transcriptomic layer remains state- and sampling-dependent. The skin-primary programs were reproducible across bulk skin data and directionally supported by single-cell and spatial analyses, but the cellular and spatial evidence is contextual rather than definitive patient-level mechanistic validation. Treatment history, lesion age, body site, inflammation intensity and the availability of matched compartments can all influence the observed state. Second, the genetic layer is limited by summary-statistic availability, power and quality control. T2D, MASLD, MDD and uveitis were source-unresolved in the prespecified primary panel at this stage and should not be interpreted as null outcomes. PsA is a near-neighbor phenotype with probable high shared liability and potential overlap-related inflation, while the Crohn disease and ulcerative colitis correlations require independent direction adjudication. Third, functional interpretation is constrained by reference eQTL context, MAF-proxy sensitivity in selected coloc analyses, and the fact that statistical sharing does not identify clinical mediation. The relevant question may therefore be less which transcriptomic endotype carries each comorbidity than how dynamic tissue states emerge on a partially shared, disease-specific inherited liability landscape. Separating these levels provides a more conservative and potentially more transferable framework for molecular stratification in psoriasis.

## Methods

### Study design and prespecified analysis framework

Analyses followed a prespecified sequence with predefined decision rules. Discrete endotype stability was evaluated before continuous molecular modeling. Molecular programs were defined before single-cell, spatial and genetic contextualization to prevent post hoc redefinition. Axis-specific genetic anchoring was tested before overall comorbidity genetics. Broad MR, axis-specific MR/LDSC/LAVA/coloc, post hoc GWAS replacement, drug prediction, PPI, hub-gene analysis, LASSO and machine-learning marker selection were excluded from the prespecified analysis plan.

### Transcriptomic discovery and replication

E-MTAB-14509 was used for bulk transcriptomic discovery and internal replication across lesional skin, non-lesional skin and blood. Discrete clustering was assessed by bootstrap stability. Continuous molecular programs were modeled using multi-view factor analysis across complete baseline patients using MOFA-style latent factor modeling [22]. Program prioritization used stability, tissue contribution, independent paired-skin replication, biological interpretability, confounding independence and systemic support. GSE244679 was used for independent paired-skin replication of retained signatures.

### Single-cell and spatial contextualization

Retained CORE and EXTENDED gene programs were scored in single-cell datasets and summarized at donor/cell-type level. GSE228421 provided the primary donor-level single-cell contextualization, and GSE173706 provided independent sensitivity support. GSE225475 and GSE202011 were used for spatial contextualization. Spot/section-level spatial results were treated as contextual evidence and were not used as patient-level replication.

### Axis-specific genetic anchoring

Retained F1, F2, F6 and F7 gene programs were tested for psoriasis genetic support using predefined enrichment and sensitivity criteria, including MAGMA gene-set enrichment [23]. The final evidence tier for each program was assigned before comorbidity genetics. Because no program met the robust-support threshold, they were excluded from genetic main analyses.

### Genome-wide genetic correlation

Overall psoriasis susceptibility was represented by GCST90472771. Prespecified comorbidity GWAS outcomes included psoriatic arthritis, Crohn disease, ulcerative colitis, coronary artery disease, ischemic stroke, chronic kidney disease and additional prespecified outcomes whose primary data sources remained unresolved. Summary statistics were harmonized to a common LDSC-compatible framework. LDSC estimated genome-wide genetic correlation [21], standard error, Z statistic, P value, FDR, single-trait heritability and cross-trait intercept.

### Local genetic correlation

Restricted LAVA was applied only after genome-wide genetic correlation [13] and sign/QC adjudication. CAD was the primary systemic target, PsA was a positive-control/near-neighbor target, and Crohn disease and ulcerative colitis were retained as QC-flagged IBD targets. Local heritability screening preceded bivariate local genetic correlation. High-value loci were reviewed through LD-reference validation before downstream regulatory prioritization.

### Regulatory prioritization and colocalization

Restricted shared-locus candidates were prioritized with GTEx v8 eQTL data using SMR/HEIDI [14,15]. Candidate tissues were selected according to outcome relevance: skin, blood and vascular/arterial tissues for CAD; skin and immune tissues for PsA; and skin, blood, intestinal and immune tissues for Crohn disease and ulcerative colitis. Colocalization was then applied to Tier A restricted candidates using coloc [16]. PP4 >= 0.8 was treated as supported coloc evidence, PP4 from 0.5 to 0.8 as suggestive, and PP3 greater than PP4 as evidence favoring distinct association signals.

## Ethics Statement

This study used previously generated public or access-controlled datasets and summary statistics and did not involve new participant recruitment, intervention or collection of identifiable human participant data. No new ethics approval is claimed here; dataset-specific ethics and consent were handled by the original studies.

## Data Availability

All transcriptomic and spatial datasets used in this study are public or publicly indexed: E-MTAB-14509, GSE244679, GSE228421, GSE173706, GSE225475 and GSE202011. Psoriasis GWAS summary statistics were represented by GCST90472771. GTEx v8 eQTL resources were used for regulatory prioritization. Comorbidity GWAS summary statistics were obtained from their original study sources subject to the corresponding access terms; source-resolved outcomes and unresolved prespecified outcomes are reported in Table 1 and the supplementary tables. Processed source data supporting the main figures and tables, together with analysis outputs required to reproduce the reported summaries, are available in the project repository at https://github.com/seefreewind/psoriasis-molecular-heterogeneity-comorbidity, including `source_data/`, `results/figures/communications_biology_final/source_data/` and `manuscript/supplementary_tables/`.

## Code Availability

Analysis code used to generate the reported summaries, figures and tables is available in the project repository at https://github.com/seefreewind/psoriasis-molecular-heterogeneity-comorbidity. The submission-lock code archive is released as v0.1.1 at https://github.com/seefreewind/psoriasis-molecular-heterogeneity-comorbidity/releases/tag/v0.1.1. The repository contains analysis scripts under `src/`, environment information under `environment/`, figure-generation scripts, manuscript-generation scripts, source-data files and submission-lock audit reports.

## Author Contributions

Y.Z. and D.L. conceived and designed the study. Y.Z. developed the analysis workflow, performed the computational analyses, curated the processed data, generated figures and tables, and drafted the manuscript. Y.C. and Y.L. contributed to data curation, result checking and manuscript review. D.L. supervised the study, contributed to interpretation and revised the manuscript. All authors reviewed and approved the final manuscript.

## Competing Interests

The authors declare no competing interests.

## Acknowledgements

No specific funding was received for this study. The authors have no acknowledgements to declare.

## Figure Legends

**Figure 1. Study design and transition from discrete endotypes to continuous molecular programs.** Public transcriptomic, single-cell, spatial, GWAS and eQTL resources were organized into a prespecified sequence. The initial k = 2 discrete endotype analysis did not meet the bootstrap stability threshold, leading to continuous multi-view molecular modeling and downstream retained-program contextualization.

**Figure 2. Molecular-program prioritization and independent bulk replication.** Evidence for F1, F2, F6 and F7 is summarized across program stability, tissue contribution, internal support, independent paired-skin replication and biological interpretability. F1, F2 and F6 were retained as skin-primary tissue programs, whereas F7 was retained as a systemic-supportive candidate.

**Figure 3. Directional single-cell and spatial contextualization of selected molecular programs.** Retained program scores were examined in donor-level single-cell summaries and spatial transcriptomic contexts. The figure shows directional cellular and spatial support for the selected programs while preserving contextual rather than definitive cell-state language.

**Figure 4. Axis-specific genetics was not robustly supported while overall psoriasis susceptibility remained the genetic reference.** Retained F1, F2, F6 and F7 programs were tested for psoriasis genetic anchoring before comorbidity genetics. None met the predefined support threshold, motivating the downstream use of overall psoriasis susceptibility rather than axis-specific genetic analyses.

**Figure 5. Genome-wide and local shared genetic architecture of psoriasis comorbidity.** LDSC genetic correlation and restricted LAVA local genetic correlation show disease-specific sharing between overall psoriasis susceptibility and comorbid outcomes. CAD provides the cleanest non-neighbor systemic signal, PsA acts as a near-neighbor positive control, and Crohn disease/ulcerative colitis show directionally heterogeneous local architectures.

**Figure 6. Restricted regulatory prioritization supports a layered model of psoriasis biology.** Restricted local-rg signals were narrowed through SMR/HEIDI prioritization and coloc. Supported and suggestive regulatory candidates did not show direct gene-membership overlap with the molecular programs, supporting a model in which tissue-state heterogeneity and inherited multisystem liability are connected but non-equivalent biological layers.

## Tables

### Table 1. Public datasets and analytical roles

| Dataset/accession | Modality/cohort | Sample size | Tissue/compartment | Study role | Key limitation |
| --- | --- | --- | --- | --- | --- |
| E-MTAB-14509 | Bulk RNA-seq; psoriasis baseline discovery and replication | 146 baseline patients; 76 complete LS/NL/blood discovery; 57 paired-skin replication | LS, NL and blood | Molecular-program discovery, stability testing and internal replication | Complete-case subset used for multi-view modeling |
| GSE244679 | Bulk RNA-seq; paired psoriasis skin | 24 paired lesional/adjacent-normal samples | Paired skin | Independent paired-skin replication of retained signatures | Skin-only validation; no systemic compartment |
| GSE228421 | Single-cell RNA-seq; psoriasis skin | 20 10x samples from 5 donors | Skin cells | Primary donor-level cellular contextualization | Directional support, not definitive cell-state mechanism |
| GSE173706 | Single-cell RNA-seq; psoriasis skin | 33 samples | Skin cells | Independent single-cell sensitivity analysis | Used for support, not for reselecting programs |
| GSE225475 | Spatial transcriptomics; psoriasis/control skin | 6 spatial samples | Skin sections | Primary spatial contextualization | Section/spot-level observations do not replace patient-level replication |
| GSE202011 | Spatial transcriptomics; psoriasis skin | 30 spatial samples | Skin sections | External spatial robustness analysis | Spatial support is contextual and not a genetic anchor |
| GCST90472771 | GWAS summary statistics; psoriasis | 36,466 cases and 458,078 controls | Germline | Overall psoriasis susceptibility GWAS for comorbidity genetics | Overall susceptibility; not F1/F2/F6/F7-specific |
| Prespecified comorbidity GWAS panel | GWAS summary statistics; comorbid outcomes | CAD 122,733/424,528; PsA 5,065/21,286; Crohn 12,194/28,072; UC 12,366/33,609; stroke and CKD analyzed | Germline | PsA, CAD, Crohn disease, UC, ischemic stroke and CKD analyzed for shared genetic architecture | Additional prespecified outcomes remained source-unresolved and were not interpreted as biological nulls |
| GTEx v8 | eQTL summary data; non-disease reference tissues | Tissue-specific GTEx v8 sample sizes | Skin, blood, vascular/arterial, spleen, intestinal and immune-relevant tissues | Restricted SMR/HEIDI and coloc regulatory prioritization | Reference eQTL contexts may not match inflamed psoriasis tissue |

Footnote: LS, lesional skin; NL, non-lesional skin; PsA, psoriatic arthritis; CAD, coronary artery disease; UC, ulcerative colitis; CKD, chronic kidney disease; T2D, type 2 diabetes; MASLD, metabolic dysfunction-associated steatotic liver disease; MDD, major depressive disorder.

### Table 2. Evidence and final interpretation of retained molecular programs

| Program | Dominant compartment | Independent replication | Cellular/spatial context | Genetic anchoring | Final interpretation |
| --- | --- | --- | --- | --- | --- |
| F1 | Skin-primary | GSE244679 LS abs(rho) = 0.688 | Directional keratinocyte/stress-inflammatory support; spatial rho = 0.502 and 0.489 | No robust axis-specific genetic support | Skin-primary tissue-state program with directional keratinocyte/spatial support; not a genetically anchored endotype |
| F2 | Skin-primary | GSE244679 NL abs(rho) = 0.518 | Directional keratinocyte/stress-inflammatory support; spatial rho = 0.506 and 0.491 | No robust axis-specific genetic support | Skin-primary program with possible field-state support; not a genetically anchored endotype |
| F6 | Skin-primary | GSE244679 LS abs(rho) = 0.375 | Directional keratinocyte/stress support; spatial rho = 0.546 and 0.496 | No robust axis-specific genetic support | Skin-primary program with stress/hypoxia-like features and directional support; not a genetically anchored endotype |
| F7 | Systemic/supportive | Internal skin-blood rho = 0.577; GSE61281 abs(rho) = 0.455 | Low-confidence systemic immune/myeloid direction; spatial correlations positive but not coherent for skin-spatial immune localization | No robust axis-specific genetic support | Systemic-supportive candidate only; not a coherent skin-spatial or genetically anchored axis |

Footnote: Spatial rho values are reported for GSE225475 and GSE202011, respectively. Genetic anchoring refers to prespecified axis-specific psoriasis genetic support, not overall psoriasis susceptibility.

### Table 3. Manuscript-priority regulatory candidates

| Outcome | Locus | Gene | Representative tissue | PP4 | Evidence level | Sensitivity note |
| --- | --- | --- | --- | --- | --- | --- |
| PsA | 887 | SLC22A5 | Spleen | 0.971 | Supported | Standard coloc input |
| PsA | 1793 | RP11-977G19.11 | EBV-transformed lymphocytes | 0.945 | Supported | Standard coloc input |
| UC | 2251 | RP11-973H7.1 | Transverse and sigmoid colon | 0.960 in both | Supported | eQTL MAF proxy |
| CAD | 113 | UBQLN4 | Sun-exposed and non-sun-exposed skin | 0.754; 0.746 | Suggestive | Standard coloc input |
| CAD | 113 | MEX3A | Sun-exposed and non-sun-exposed skin | 0.597; 0.595 | Suggestive | Standard coloc input |
| Crohn disease | 887 | SLC22A5 | Sigmoid colon | 0.639 | Suggestive | eQTL MAF proxy |
| Crohn disease | 10 | PARK7 | Whole blood | 0.565 | Suggestive | eQTL MAF proxy |

Footnote: All displayed candidates were drawn from the recurrent highest-priority restricted SMR/HEIDI set. Supported denotes PP4 >= 0.80. Suggestive denotes 0.50 <= PP4 < 0.80 and is interpreted with PP3 and input sensitivity. eQTL MAF proxy indicates that eQTL-derived MAF was used because matched GWAS MAF was unavailable; these entries require conservative interpretation. PP4, posterior probability for a shared association signal under the coloc model; LCL, lymphoblastoid cell line.

## References

1. Armstrong, A. W., Blauvelt, A., Callis Duffin, K. et al. Psoriasis. *Nature Reviews Disease Primers* 11, 45 (2025). doi:10.1038/s41572-025-00630-5.

2. Rider, A., Grantham, H. J., Smith, G. R. et al. Transcriptomic profiling and machine learning uncover gene signatures of psoriasis endotypes and disease severity. *Communications Medicine* 6, 65 (2026). doi:10.1038/s43856-025-01325-4.

3. Chen, C. H., Lee, M. S., Chang, W. Y. et al. Uncovering a dual T helper 17/type 2 transcriptomic endotype in psoriasis. *Journal of the American Academy of Dermatology* (2026). doi:10.1016/j.jaad.2026.06.131.

4. Shrotri, S., Daamen, A., Kingsmore, K. et al. Transcriptomic analysis identifies disease severity and therapeutic response in psoriasis. *JID Innovations* 5, 100333 (2025). doi:10.1016/j.xjidi.2024.100333.

5. Ma, F., Plazyo, O., Billi, A. C. et al. Single cell and spatial sequencing define processes by which keratinocytes and fibroblasts amplify inflammatory responses in psoriasis. *Nature Communications* 14, 3455 (2023). doi:10.1038/s41467-023-39020-4.

6. Castillo, R. L., Sidhu, I., Dolgalev, I. et al. Spatial transcriptomics stratifies psoriatic disease severity by emergent cellular ecosystems. *Science Immunology* 8, eabq7991 (2023). doi:10.1126/sciimmunol.abq7991.

7. Dand, N. et al. GWAS meta-analysis of psoriasis identifies new susceptibility alleles impacting disease mechanisms and therapeutic targets. *Nature Communications* 16, 2051 (2025). doi:10.1038/s41467-025-56719-8.

8. Patrick, M. T. et al. Shared genetic risk factors and causal association between psoriasis and coronary artery disease. *Nature Communications* 13, 6565 (2022). doi:10.1038/s41467-022-34323-4.

9. Stuart, P. E. et al. Genome-wide association analysis of psoriatic arthritis and cutaneous psoriasis reveals differences in their genetic architecture. *American Journal of Human Genetics* 97, 816-836 (2015). doi:10.1016/j.ajhg.2015.10.019.

10. Ellinghaus, D. et al. Combined analysis of genome-wide association studies for Crohn disease and psoriasis identifies seven shared susceptibility loci. *American Journal of Human Genetics* 90, 636-647 (2012). doi:10.1016/j.ajhg.2012.02.020.

11. Li, W.-Q., Han, J. & Qureshi, A. A. Psoriasis, psoriatic arthritis and increased risk of incident Crohn's disease in US women. *Annals of the Rheumatic Diseases* 72, 1200-1205 (2013). doi:10.1136/annrheumdis-2012-202143.

12. Gelfand, J. M. et al. Risk of myocardial infarction in patients with psoriasis. *JAMA* 296, 1735-1741 (2006). doi:10.1001/jama.296.14.1735.

13. Werme, J., van der Sluis, S., Posthuma, D. & de Leeuw, C. A. An integrated framework for local genetic correlation analysis. *Nature Genetics* 54, 274-282 (2022). doi:10.1038/s41588-022-01017-y.

14. Zhu, Z. et al. Integration of summary data from GWAS and eQTL studies predicts complex trait gene targets. *Nature Genetics* 48, 481-487 (2016). doi:10.1038/ng.3538.

15. The GTEx Consortium. The GTEx Consortium atlas of genetic regulatory effects across human tissues. *Science* 369, 1318-1330 (2020). doi:10.1126/science.aaz1776.

16. Giambartolomei, C. et al. Bayesian test for colocalisation between pairs of genetic association studies using summary statistics. *PLoS Genetics* 10, e1004383 (2014). doi:10.1371/journal.pgen.1004383.

17. Jimenez-Gracia, L. et al. Interpretable inflammation landscape of circulating immune cells. *Nature Medicine* 32, 633-644 (2026). doi:10.1038/s41591-025-04126-3.

18. Li, X., Yan, Z., Lan, H. et al. Genetic comorbidity of psoriasis and four cardiovascular diseases: uncovering shared mechanisms and potential therapeutic targets. *Experimental Dermatology* 34, e70158 (2025). doi:10.1111/exd.70158.

19. Vestergaard, M. V., Nunez, A. A., Sazonovs, A., Athanasiadis, G. & Jess, T. Multimodal analysis disentangles the genetic and microbial associations between inflammatory bowel disease and other immune-mediated diseases across a harmonized population framework. *Nature Communications* 17, 1849 (2026). doi:10.1038/s41467-026-68564-4.

20. Alegbe, T. et al. Cell-type-resolved genetic variation shapes inflammatory bowel disease risk. *Nature* 642, 1-23 (2026). doi:10.1038/s41586-026-10627-z.

21. Bulik-Sullivan, B. et al. An atlas of genetic correlations across human diseases and traits. *Nature Genetics* 47, 1236-1241 (2015). doi:10.1038/ng.3406.

22. Argelaguet, R. et al. Multi-Omics Factor Analysis-a framework for unsupervised integration of multi-omics data sets. *Molecular Systems Biology* 14, e8124 (2018). doi:10.15252/msb.20178124.

23. de Leeuw, C. A., Mooij, J. M., Heskes, T. & Posthuma, D. MAGMA: generalized gene-set analysis of GWAS data. *PLoS Computational Biology* 11, e1004219 (2015). doi:10.1371/journal.pcbi.1004219.
