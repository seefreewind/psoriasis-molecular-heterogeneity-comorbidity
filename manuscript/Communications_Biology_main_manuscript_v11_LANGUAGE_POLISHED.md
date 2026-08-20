# Molecular heterogeneity and multisystem shared genetic architecture define distinct biological layers of psoriasis

Yu Zhang1, Ying Chen2, Yue Liu2 and Da Lin1

1 Department of Ophthalmology, The Second Affiliated Hospital of Wenzhou Medical University, No. 109 Xueyuan West Road, Lucheng District, Wenzhou, Zhejiang Province, China

2 Wenzhou Medical University, Wenzhou, Zhejiang Province, China

Correspondence: Da Lin, 212574@wzhealth.com; ORCID 0009-0009-4410-0218




## Abstract

Psoriasis shows molecular heterogeneity in tissue and inherited susceptibility to systemic comorbidity, but the relationship between these layers remains unclear. We integrated cross-tissue psoriasis transcriptomics with independent bulk, single-cell, spatial and genetic evidence under a prespecified framework. A tested k = 2 discrete representation did not meet the stability criterion (minimum bootstrap Jaccard = 0.562). In contrast, multi-view modeling of 76 complete baseline patients identified reproducible continuous molecular programs. F1, F2 and F6 replicated in paired skin and showed cellular and spatial associations, while F7 remained a systemic-supportive program. The four programs did not meet criteria for axis-specific genetic anchoring. Comorbidity analyses therefore used overall psoriasis susceptibility, which shared genetic architecture with coronary artery disease and near-neighbor psoriatic arthritis and showed heterogeneous local sharing with inflammatory bowel disease. Restricted regulatory prioritization and colocalization identified a limited set of shared regulatory candidates, with no direct gene-membership overlap with the retained molecular programs. These findings separate reproducible psoriasis tissue states from inherited multisystem liability while showing where the two layers intersect.


## Introduction

Psoriasis can be viewed through two biological maps: molecular heterogeneity within affected tissue and inherited liability shared across organ systems. Cross-tissue transcriptomic work has identified molecular programs associated with psoriasis phenotype and severity [1]. Single-cell and spatial analyses have mapped coordinated keratinocyte, fibroblast and immune-cell states in psoriatic tissue [2]. Large-scale GWAS has expanded the inherited susceptibility map of psoriasis [3]. These molecular and genetic maps have mostly developed in parallel. Tissue-state maps describe how lesional skin, clinically uninvolved skin and blood differ in transcriptional state, cellular composition and inflammatory activity. Genetic maps describe how inherited psoriasis liability covaries with psoriatic arthritis, cardiovascular disease and inflammatory bowel disease. The unresolved question is whether these maps correspond. If they do, skin molecular programs could provide tissue readouts of systemic inherited risk. If they do not, molecular heterogeneity and comorbidity genetics need separate interpretation. This distinction matters because tissue transcription reflects inherited risk after local inflammation, repair, environment and disease activity have acted on it, whereas GWAS captures inherited covariance between disease liabilities.

Molecular endotyping studies provide a rich substrate for stratification, but they do not define the geometry of heterogeneity. Rider et al. identified phenotype- and severity-associated programs in the PSORT transcriptomic resource used here [1]. Shrotri et al. linked transcriptomic profiles to psoriasis severity and therapeutic response [4]. Chen et al. described a dual Th17/type 2 transcriptomic pattern with prominent IL-36 activation in a Taiwanese psoriasis cohort [5]. Spatial transcriptomics has linked emergent cellular ecosystems to psoriatic disease severity [6]. These studies establish substantial molecular heterogeneity, but they leave open whether heterogeneity forms stable patient classes or continuous tissue programs. Disease states can vary along gradients of inflammation, remodeling or systemic immune activity. Unstable clustering can turn such gradients into artificial boundaries.

Psoriasis genetics has also moved from locus discovery to cross-trait architecture. Psoriatic arthritis and cutaneous psoriasis show overlapping but distinguishable genetic architectures [7]. Psoriasis shares inherited susceptibility with coronary artery disease [8], and psoriasis-Crohn disease GWAS identified shared susceptibility loci [9]. More recent harmonized analyses further support positive psoriasis-IBD genetic sharing [10]. These studies usually operate at the level of overall disease susceptibility. They do not determine whether genetically shared comorbidity risk concentrates in specific molecular states measured in skin or blood.

Here, we asked whether reproducible molecular heterogeneity in psoriasis tissue corresponds to distinct inherited architectures of systemic comorbidity. We integrated cross-tissue transcriptomics with independent bulk, single-cell and spatial validation, tested whether retained molecular programs were genetically anchored, and then characterized genome-wide and local comorbidity sharing with restricted regulatory prioritization. This design separates tissue-state heterogeneity from inherited multisystem disease sharing while testing where the two layers converge.


## Results

### Continuous molecular programs capture reproducible psoriasis tissue heterogeneity

The tested k = 2 discrete endotype representation did not meet the prespecified stability criterion. The minimum bootstrap Jaccard index was 0.562, below the 0.75 threshold for stable cluster membership. This result did not support a categorical claim for that tested representation. Continuous multi-view modeling then identified eight stable factors across five random seeds in 76 complete baseline discovery patients with lesional skin, non-lesional skin and blood. A prespecified prioritization matrix retained F1, F2, F6 and F7 for manuscript-level interpretation. Selection used stability, tissue contribution, internal replication, external replication and biological interpretability. It was not driven by a single nominal association. View-contribution analysis supported compartmentalization: F1 was dominated by lesional skin, F2 by non-lesional skin, F6 showed a smaller lesional contribution and F7 was blood-dominant. F1, F2 and F6 were skin-primary molecular programs, whereas F7 was retained as systemic-supportive. Independent paired-skin replication in GSE244679 supported the skin-primary classification. F1 replicated in lesional skin (|ρ| = 0.688), F2 in non-lesional skin (|ρ| = 0.518) and F6 in lesional skin (|ρ| = 0.375). Independent whole-blood support in GSE61281 was strongest for F7, with |ρ| = 0.455 for the psoriasis spectrum versus control comparison. Table 2 summarizes the retained programs.

### Molecular programs show consistent cellular and spatial associations

Donor-level single-cell analyses and spatial transcriptomics contextualized the retained programs without redefining their molecular identities. GSE228421 provided the primary donor-level single-cell analysis, and GSE173706 provided independent sensitivity support. The main statistical unit was donor-level or sample-level summarized signal rather than individual cells. Donor-level effects were directionally positive for F1, F2 and F6 in keratinocyte and stress-inflammatory contexts, whereas F7 showed less coherent skin immune localization. Spatial transcriptomics showed consistent positive within-sample spot-level Spearman correlations between prespecified CORE program scores and the dominant spatial marker program. Results were summarized as the median across samples in GSE225475 and GSE202011. F1 showed ρ = 0.502 and ρ = 0.489, F2 showed ρ = 0.506 and ρ = 0.491, and F6 showed ρ = 0.546 and ρ = 0.496. F7 also showed positive spatial correlations (ρ = 0.505 and ρ = 0.485). Positive correlation with the tested keratinocyte/stress contextual gradient was not equivalent to coherent skin-localized immune identity, so F7 remained a systemic-supportive candidate rather than a skin-localized immune program.

### Molecular programs lack axis-specific genetic anchoring

None of the retained programs met the prespecified threshold for axis-specific psoriasis genetic support. F1, F2, F6 and F7 had no robust axis-specific support in the final genetic evidence table. The tissue programs remained reproducible transcriptomic findings with replication and cellular/spatial associations, but they were not carried forward as program-specific genetic variables. This result set the downstream scope: the programs were treated as tissue-state variables rather than germline-defined subtypes. Subsequent comorbidity analyses used overall psoriasis susceptibility from GCST90472771. None of the four primary program tests survived FDR correction, and matched-random gene-set tests likewise provided no robust enrichment. This decision preserved the distinction between reproducible tissue programs and inherited comorbidity architecture.

### Psoriasis susceptibility shows disease-specific genetic sharing

LDSC tested genome-wide genetic correlation between overall psoriasis susceptibility and prespecified comorbidity outcomes. Six outcomes had sufficient data availability and QC for the formal table. Coronary artery disease showed the strongest QC-passing non-neighbor correlation (r_g = 0.1732, SE = 0.0274, P = 2.498 × 10⁻¹⁰, FDR = 7.494 × 10⁻¹⁰). Psoriatic arthritis, analyzed as a near-neighbor positive control, showed very high genetic correlation (r_g = 1.1715, SE = 0.0751, P = 6.746 × 10⁻⁵⁵, FDR = 4.048 × 10⁻⁵⁴). This estimate carried elevated cross-trait-intercept labeling, consistent with close phenotypic relatedness and possible overlap-related inflation. Crohn disease and ulcerative colitis showed negative global estimates with QC flags: Crohn disease r_g = -0.2717, SE = 0.0449, P = 1.434 × 10⁻⁹, FDR = 2.868 × 10⁻⁹; ulcerative colitis r_g = -0.2233, SE = 0.0409, P = 4.820 × 10⁻⁸, FDR = 7.229 × 10⁻⁸. Both IBD outcomes were retained with cautious interpretation because h² and cross-trait intercepts raised QC concerns. The negative IBD estimates were treated as analysis-specific global results, not as definitive evidence that psoriasis liability is globally protective against IBD. Ischemic stroke (r_g = 0.0255, P = 0.6647) and chronic kidney disease (r_g = 0.0118, P = 0.7912) were null or low-power references. Type 2 diabetes, MASLD, major depressive disorder and uveitis were source-unresolved and were not interpreted as null outcomes.

### Local genetic correlation reveals heterogeneous sharing

Restricted LAVA localized psoriasis-comorbidity sharing after global LDSC and sign/QC adjudication. CAD remained the primary systemic target, with 118 bivariate loci, 23 FDR-supported loci, median local ρ = 0.0787, 21 positive nominal signals, 10 negative nominal signals and a leading locus at ρ = 0.6508. Psoriatic arthritis showed the expected near-neighbor pattern: 40 bivariate loci, 31 FDR-supported loci, 36 nominal positive loci, no nominal negative loci and median ρ = 0.6315. Crohn disease and ulcerative colitis showed mixed local directions. Crohn disease had 131 bivariate loci, 49 FDR-supported loci, 9 nominal positive loci, 51 nominal negative loci and median ρ = -0.2078. Ulcerative colitis had 98 bivariate loci, 19 FDR-supported loci, 7 nominal positive loci, 18 nominal negative loci and median ρ = -0.0479. The shared chromosome 1 interval 66,778,016-67,761,890 (internal locus 57) was prominent in both IBD analyses with negative local ρ estimates. Psoriasis-IBD sharing was directionally heterogeneous at the locus level. These local results argue against reducing psoriasis-IBD genetics to a single genome-wide direction.

### Colocalization identifies a restricted set of shared regulatory signals

Restricted regulatory prioritization used prespecified shared-locus candidates and relevant GTEx v8 eQTL tissues. SMR/HEIDI prioritized 91 outcome-gene pairs, including 33 highest-tier outcome-gene pairs corresponding to 30 unique genes. A second probe-window sensitivity analysis retained 100% of genes prioritized in the primary SMR/HEIDI analysis, supporting stability of the restricted prioritization set. Colocalization identified few PP4-supported signals. PsA had three supported signals, including SLC22A5 in spleen (PP4 = 0.971), RP11-977G19.11 in lymphoblastoid cells (PP4 = 0.945) and SLC22A5 in lymphoblastoid cells (PP4 = 0.934). Ulcerative colitis had two supported RP11-973H7.1 signals in transverse and sigmoid colon (PP4 = 0.960 and 0.960), both using eQTL MAF proxy inputs. CAD had no PP4-supported gene-tissue pair; UBQLN4 and MEX3A at locus 113 were suggestive in skin (PP4 range 0.595-0.754). Crohn disease produced suggestive SLC22A5 and PARK7 signals (PP4 = 0.639 and 0.565), both with eQTL MAF proxy sensitivity flags. No supported or suggestive regulatory candidate directly overlapped the retained F1/F2/F6/F7 CORE or EXTENDED gene programs. This absence of direct gene-membership overlap separated inherited cis-regulatory candidates from emergent tissue programs. Regulatory candidates therefore contextualized overall psoriasis-comorbidity genetics without creating program-specific genetic claims.


## Discussion

This study resolves psoriasis heterogeneity at two distinct scales. A tested k = 2 representation did not meet the prespecified stability criterion, whereas continuous molecular programs were reproducible across cross-tissue modeling and independent skin replication. F1, F2 and F6 represented skin-primary tissue-state programs, and F7 remained systemic-supportive. These programs did not meet criteria for axis-specific genetic anchoring. Overall psoriasis susceptibility, by contrast, shared genome-wide and local architecture with selected comorbid diseases. The central result is a separation of scale: tissue-state heterogeneity and inherited multisystem liability intersect, but they do not collapse into the same biological layer. This distinction matters for molecular stratification because a reproducible tissue program can mark a disease state without defining a genetically separable patient subtype. It also clarifies the absence of robust axis-specific genetic support. That result constrains interpretation of the programs as tissue-state variables, while preserving their replication in paired skin and their cellular and spatial associations. Large-scale immune-cell mapping across immune-mediated inflammatory diseases similarly identifies shared and disease-specific inflammatory states across psoriasis, psoriatic arthritis, Crohn disease and ulcerative colitis [11]. Organ-wide single-cell spatial mapping of human skin further shows that epithelial, stromal and immune cells form multicellular neighborhoods that vary across anatomic sites and disease contexts [12]. These external maps provide context for tissue organization, not validation of the specific programs identified here.

A lack of one-to-one correspondence between molecular programs and germline liability is biologically plausible. Transcriptomic states are measured after lesion formation, immune recruitment, tissue repair, disease activity and sampling context have interacted. Germline genetic correlation captures inherited covariance before those downstream processes. Rider et al. identified phenotype- and severity-associated cross-tissue molecular programs [1]. Shrotri et al. linked transcriptional profiles with severity and treatment response [4]. Chen et al. described a dual Th17/type 2 inflammatory transcriptomic pattern in a Taiwanese cohort [5]. Together, these studies establish psoriasis molecular heterogeneity, but heterogeneity need not be discrete or genetically encoded. The k = 2 stability result narrows the endotype claim while leaving the molecular result intact. In these paired skin-blood data, continuous programs provided a more stable representation than categorical patient assignment. The retained programs therefore represent reproducible tissue states rather than germline-defined subtypes, supporting the use of overall psoriasis susceptibility for comorbidity genetics. This framing also avoids circular interpretation. Genetic analyses were not used to rename transcriptomic programs after the fact, and transcriptomic programs were not forced into genetic tests once prespecified support was absent. The transcriptomic and genetic analyses therefore answer related but different questions: one describes molecular state within affected tissue, and the other estimates inherited sharing between diagnoses.

CAD was the strongest QC-passing non-neighbor signal. Genome-wide genetic correlation and multiple positive local LAVA signals indicated shared polygenic architecture between psoriasis and CAD. Earlier work identified shared inherited architecture between psoriasis and CAD [8]. More recent analyses extended shared genetic evidence across a broader range of cardiovascular phenotypes [13]. This moves the cardiovascular finding beyond an epidemiological comorbidity statement. Psoriasis and CAD liabilities shared measurable polygenic covariance, and local analysis showed that the covariance concentrated at multiple loci. Regulatory follow-up narrowed the claim. CAD yielded recurrent SMR/HEIDI candidates but no gene-tissue pair meeting the prespecified PP4 threshold, supporting shared polygenic architecture without a resolved cis-regulatory mediator. This pattern is compatible with weak effects distributed across many loci, regulatory mechanisms absent from the tested tissues, or shared genetic influences that operate outside baseline cis-eQTL variation. The CAD signal is therefore a credible shared-architecture result, not yet a mapped psoriasis-to-CAD molecular mediator. GTEx provides broad bulk-tissue cis-eQTL coverage [14]. Disease-context single-cell eQTL mapping shows that immune-mediated regulatory effects can be cell-type- or state-restricted [15]. Context-specific regulation may therefore remain invisible to baseline GTEx-based colocalization.

The IBD results define a more complex architecture. Crohn disease and ulcerative colitis showed negative global LDSC estimates in this analysis, but both carried heritability-intercept and cross-trait-intercept warnings. Recent harmonized analyses reported positive psoriasis-IBD genetic correlations [10]. Earlier GWAS identified shared psoriasis-Crohn susceptibility regions [9]. The contrast argues against assigning one stable genome-wide direction to psoriasis-IBD genetics. Restricted LAVA resolved part of the discrepancy by identifying both positive and negative local correlations, with negative local signals more prominent in the current analysis. Different loci may connect psoriasis and IBD through different immunological or regulatory directions. Residual differences in phenotype definition, ancestry or sample composition, sample overlap, variant coverage and LD reference structure could also alter the genome-wide balance. The most useful interpretation is that psoriasis-IBD shared architecture may be directionally heterogeneous across loci and sensitive to GWAS and LD reference composition. This treatment keeps the IBD signal in the manuscript while reducing the risk of overstating a global direction that is not stable across evidence sources. The IBD findings support locus-level directional heterogeneity and QC-sensitive global estimates rather than a stable globally negative relationship.

The genetic follow-up separated three evidence scales. LDSC and LAVA identified shared liability architecture, SMR/HEIDI prioritized candidate regulatory genes, and coloc evaluated whether association patterns were compatible with a shared causal signal under the specified model. Polygenic sharing was broader than strong cis-regulatory colocalization. PsA and UC produced PP4-supported regulatory signals, whereas CAD and Crohn disease remained suggestive in the restricted coloc table. Coloc-supported or suggestive genes did not directly overlap the retained F1/F2/F6/F7 programs. This zero direct overlap indicates that inherited cis-regulatory candidates and emergent tissue programs operate at different analytical scales. It does not prove biological independence. A coloc gene is a candidate regulatory perturbation at a locus; a molecular program is a multicellular tissue response measured after disease processes unfold. These two outputs are not expected to share gene names systematically, especially when the tissue programs summarize coordinated inflammatory, epithelial and stromal responses. Shared germline liability, shared cis-regulatory signals and tissue-state programs therefore capture related but non-equivalent levels of psoriasis biology.

Three limitations bound the model. First, transcriptomic programs remain state- and sampling-dependent. Single-cell and spatial analyses localized programs, but they did not provide definitive patient-level mechanistic validation. Treatment history, lesion age, body site, inflammation intensity and matched-compartment availability may shape the observed state. Second, summary-statistic availability and phenotype QC limited the genetic analysis. T2D, MASLD, MDD and uveitis remained source-unresolved, PsA was a near-neighbor phenotype with possible inflation, and IBD estimates require independent direction adjudication. Third, regulatory interpretation was constrained by reference eQTL context, eQTL MAF-proxy sensitivity and the absence of clinical mediation estimates. These limitations mainly affect mechanism assignment and translational interpretation; they do not remove the evidence for reproducible molecular programs or for selected shared inherited architecture. Future work will need disease-context eQTL maps, larger harmonized comorbidity GWAS and longitudinal tissue sampling to connect these scales more directly. The central question is how dynamic tissue states emerge on a partially shared, disease-specific inherited liability background. Separating these levels provides a conservative and transferable framework for molecular stratification in psoriasis.


## Methods

### Study design and prespecified analysis framework

Analyses followed a prespecified sequence with predefined decision rules. Discrete endotype stability preceded continuous molecular modeling. Molecular programs were defined before single-cell, spatial and genetic contextualization. Axis-specific genetic anchoring preceded overall comorbidity genetics. Broad MR, axis-specific MR/LDSC/LAVA/coloc, post hoc GWAS replacement, drug prediction, PPI, hub-gene analysis, LASSO and machine-learning marker selection were excluded.

### Transcriptomic discovery and replication

E-MTAB-14509 supported bulk transcriptomic discovery and internal replication across lesional skin, non-lesional skin and blood. The tested k = 2 representation was assessed by bootstrap cluster stability using the bootstrap Jaccard index and a prespecified 0.75 stability threshold. Continuous molecular programs were modeled across complete baseline patients using MOFA-style latent factor modeling implemented through mofapy2 [16,22]. Program prioritization used stability, tissue contribution, paired-skin replication, biological interpretability, confounding independence and systemic support. GSE244679 provided independent paired-skin replication.

### External systemic support in GSE61281

GSE61281 was used as external systemic support for blood-associated molecular programs. The dataset contains 52 whole-blood Agilent GPL6480 two-colour microarray samples, including 20 cutaneous psoriasis without arthritis, 20 psoriatic arthritis and 12 unaffected controls. GEO series-matrix expression values were treated as normalized microarray measurements, probes were mapped through GPL6480 gene symbols and probe-level values were averaged to gene-level expression. Retained program scores were projected using shared genes, and blood support was summarized as the Spearman correlation between discovery factor loadings and case-control mean score differences. The main reported F7 value is the absolute correlation for psoriasis spectrum versus controls.

### Single-cell and spatial contextualization

Retained CORE and EXTENDED gene programs were scored in single-cell datasets and summarized at donor/cell-type level. GSE228421 provided primary donor-level single-cell contextualization, and GSE173706 provided independent sensitivity support. GSE225475 and GSE202011 provided spatial contextualization. For each spatial sample, prespecified CORE program scores were correlated across spots with curated spatial marker programs using Spearman correlation. The reported spatial ρ is the median within-sample spot-level program-marker correlation across samples for the dominant spatial marker program in each dataset. Spot/section-level spatial results were treated as contextual evidence, not patient-level replication.

### Axis-specific genetic anchoring

Retained F1, F2, F6 and F7 gene programs were tested for psoriasis genetic support using predefined enrichment and sensitivity criteria, including MAGMA gene-set enrichment [17]. CORE programs were treated as primary tests and EXTENDED programs as sensitivity tests. MHC-excluded analyses were the primary genetic-anchoring tests, with MHC-included results used only for sensitivity. Multiple testing was controlled across the prespecified program-test family. Matched-random gene-set analyses were used as empirical sensitivity checks. Final evidence tiers were assigned before comorbidity genetics. Programs below the robust-support threshold were excluded from genetic main analyses.

### Genome-wide genetic correlation

Overall psoriasis susceptibility was represented by GCST90472771. Prespecified comorbidity GWAS outcomes included psoriatic arthritis, Crohn disease, ulcerative colitis, coronary artery disease, ischemic stroke, chronic kidney disease and additional outcomes whose primary data sources remained unresolved. Summary statistics were harmonized to an LDSC-compatible framework. LDSC estimated genome-wide genetic correlation [18], standard error, Z statistic, P value, FDR, single-trait h² and cross-trait intercept. QC flags were assigned using single-trait h², intercept behavior, SNP coverage and cross-trait-intercept diagnostics.

### Local genetic correlation

Restricted LAVA followed genome-wide genetic correlation [19] and sign/QC adjudication. CAD was the primary systemic target, PsA was the positive-control near-neighbor target, and Crohn disease and ulcerative colitis were QC-flagged IBD targets. Local h² screening preceded bivariate local genetic correlation. Displayed loci were selected from FDR-supported, LD-reference-robust results to illustrate CAD-positive architecture, PsA positive-control sharing and IBD directional heterogeneity. High-value loci underwent LD-reference validation before regulatory prioritization.

### Regulatory prioritization and colocalization

Restricted shared-locus candidates were prioritized with GTEx v8 eQTL data [14] using SMR/HEIDI [20]. Candidate tissues reflected outcome relevance: skin, blood and vascular/arterial tissues for CAD; skin and immune tissues for PsA; and skin, blood, intestinal and immune tissues for Crohn disease and ulcerative colitis. The primary SMR/HEIDI analysis used the prespecified probe window, and a second probe-window sensitivity analysis tested gene-level retention. Colocalization was applied to restricted high-priority candidates using coloc [21]. PP4 ≥ 0.80 was treated as supported coloc evidence, 0.50 ≤ PP4 < 0.80 as suggestive, and PP3 > PP4 as evidence favoring distinct association signals.


## Ethics Statement

This study used previously generated public or access-controlled datasets and summary statistics. It did not involve new participant recruitment, intervention or collection of identifiable human participant data. Dataset-specific ethics and consent were handled by the original studies.

## Consent for Publication

Not applicable. This study does not report identifiable individual-level information, images or clinical details requiring consent for publication.

## Data Availability

All transcriptomic and spatial datasets used in this study are public or publicly indexed: E-MTAB-14509, GSE244679, GSE61281, GSE228421, GSE173706, GSE225475 and GSE202011. Psoriasis GWAS summary statistics were represented by GCST90472771. GTEx v8 eQTL resources were used for regulatory prioritization. Comorbidity GWAS summary statistics were obtained from their original study sources subject to the corresponding access terms; source-resolved outcomes and unresolved prespecified outcomes are reported in Table 1 and the supplementary tables. Processed source data supporting the main figures and tables, together with analysis outputs required to reproduce the reported summaries, are available in the project repository at https://github.com/seefreewind/psoriasis-molecular-heterogeneity-comorbidity, including `source_data/`, `results/figures/communications_biology_final/source_data/` and `manuscript/supplementary_tables/`. Original public datasets, GWAS summary statistics and GTEx-derived resources are not redistributed when source terms, size or controlled-access conditions require access through the original provider.

## Code Availability

Analysis code used to generate the reported summaries, figures and tables is available in the project repository at https://github.com/seefreewind/psoriasis-molecular-heterogeneity-comorbidity. The submission-lock code archive is released as v1.0.0-submission at https://github.com/seefreewind/psoriasis-molecular-heterogeneity-comorbidity/releases/tag/v1.0.0-submission. The repository contains analysis scripts under `src/`, environment information under `environment/`, figure-generation scripts, manuscript-generation scripts, source-data files and submission-lock audit reports.

## Author Contributions

Y.Z. and D.L. conceived and designed the study. Y.Z. developed the analysis workflow, performed the computational analyses, curated the processed data, generated figures and tables, and drafted the manuscript. Y.C. and Y.L. contributed to data curation, result checking and manuscript review. D.L. supervised the study, contributed to interpretation and revised the manuscript. All authors reviewed and approved the final manuscript.

## Authorship Approval

All authors have read and approved the final manuscript, agree to its submission and agree to be accountable for the content of the work.

## Competing Interests

The authors declare no competing interests.

## Acknowledgements

No specific funding was received for this study. The authors have no acknowledgements to declare.


## Figure Legends

**Figure 1. Study design and transition from discrete endotypes to continuous molecular programs.** a, Study architecture across public transcriptomic, single-cell, spatial, GWAS and eQTL resources. b, E-MTAB-14509 sample flow: 82 discovery patients with paired lesional/non-lesional skin, 76 patients with complete lesional/non-lesional/blood data, 57 replication patients with paired skin and no paired-blood replication compartment. c, Bootstrap stability assessment of the tested k = 2 representation. The minimum bootstrap Jaccard index was 0.562, below the prespecified 0.75 threshold. d, Prespecified transition from the tested discrete representation to continuous multi-view molecular modeling and downstream contextualization.

**Figure 2. Molecular-program prioritization and independent bulk replication.** a, Evidence summary for F1, F2, F6 and F7 across stability, independent bulk replication, biological interpretability and systemic support categories. b, View contribution, R² (%), across lesional skin, non-lesional skin and blood. c, Independent paired-skin replication in GSE244679, shown as |ρ| between projected program loading and paired lesional-minus-adjacent skin contrast. d, Conservative manuscript-level interpretation. F1, F2 and F6 are skin-primary programs, whereas F7 remains a systemic-supportive candidate; none is presented as a genetically anchored endotype.

**Figure 3. Single-cell and spatial contextualization of selected molecular programs.** a, Cell-type-specific lesional-minus-non-lesional program shifts; labels are shown for |effect| ≥ 0.03 and outlines mark the largest absolute shift per program. b, Donor-level lesional-minus-non-lesional effects are shown as point estimates with 95% bootstrap confidence intervals. c, Cross-dataset spatial concordance in GSE225475 and GSE202011. ρ denotes the median within-sample spot-level Spearman correlation between prespecified CORE program score and the dominant spatial marker program across spatial samples, ordered as GSE225475 then GSE202011 in the text and Table 2. d, Representative spatial distribution selected from samples with matched in-tissue coordinates and complete program scores. Positive F7 spatial ρ is interpreted as contextual concordance, not as coherent skin-localized immune identity.

**Figure 4. Genetic evidence separates molecular programs from overall psoriasis liability.** Axis-specific genetic anchoring was not robustly supported. a, Prespecified molecular programs F1, F2, F6 and F7 were tested for robust psoriasis genetic enrichment. b, Primary CORE, MHC-excluded MAGMA competitive gene-set results, shown as gene-set beta with 95% confidence intervals and FDR q values. c, Observed program statistics compared with matched-random gene-set null summaries; empirical P values quantify null robustness. d, None of the programs met the prespecified robust-support criteria. They were therefore retained as tissue-state molecular programs, while downstream multisystem genetics used overall psoriasis susceptibility.

**Figure 5. Genome-wide and local shared genetic architecture of psoriasis comorbidity.** a, LDSC genome-wide genetic correlation between overall psoriasis susceptibility and six comorbidity outcomes. Points indicate r_g estimates and error bars indicate 95% confidence intervals; aligned labels summarize QC interpretation. PsA is shown as a near-neighbor positive-control phenotype. b, Directional balance of restricted LAVA local r_g results for CAD, PsA, Crohn disease and UC. Leftward bars show nominal negative local r_g counts, rightward bars show nominal positive local r_g counts and the aligned column reports all-tests FDR-supported local r_g loci. c, Local genetic correlation at selected robust loci. Heatmap color encodes local ρ on a diverging scale centered at zero. Loci were selected from the prespecified robust display set; individual trait-locus cells are colored and numerically labeled only when they met the robust display criterion. Grey cells indicate that the selected locus-trait pair did not meet the robust display criterion and do not represent ρ = 0.

**Figure 6. Restricted regulatory prioritization supports a layered model of psoriasis biology.** a, Evidence cascade from FDR-supported local-r_g locus-trait pairs through SMR/HEIDI-prioritized outcome-gene pairs, highest-tier outcome-gene pairs and restricted colocalization. Count units are explicitly indicated at each evidence layer; PP4-supported and suggestive colocalization results are parallel outcome-gene-tissue categories. b, Manuscript-priority colocalization results. Color denotes comorbidity outcome and symbol shape denotes standard versus MAF-proxy input. The dashed line marks the prespecified PP4 = 0.80 support threshold. c, Integrated model separating the tissue-state layer from the inherited-liability layer. Axis-specific genetic anchoring was not robustly supported, and no direct gene-membership overlap was detected between regulatory candidates and retained molecular programs. These findings support connected but non-equivalent biological layers.


## Tables

### Table 1. Public datasets and analytical roles

| Dataset/accession | Modality/cohort | Sample size | Tissue/compartment | Study role | Key limitation |
| --- | --- | --- | --- | --- | --- |
| E-MTAB-14509 | Bulk RNA-seq; psoriasis baseline discovery and replication | 146 baseline patients; 76 complete LS/NL/blood discovery; 57 paired-skin replication | LS, NL and blood | Molecular-program discovery, stability testing and internal replication | Complete-case subset used for multi-view modeling |
| GSE244679 | Bulk RNA-seq; paired psoriasis skin | 24 paired lesional/adjacent-normal samples | Paired skin | Independent paired-skin replication of retained signatures | Skin-only validation; no systemic compartment |
| GSE61281 | Whole-blood Agilent GPL6480 microarray; psoriasis spectrum/control | 52 samples: 20 cutaneous psoriasis without arthritis, 20 PsA and 12 controls | Whole blood | External systemic support for blood-associated retained programs | Cross-platform microarray support only; not used for program selection |
| GSE228421 | Single-cell RNA-seq; psoriasis skin | 20 10x samples from 5 donors | Skin cells | Primary donor-level cellular contextualization | Directional support, not definitive cell-state mechanism |
| GSE173706 | Single-cell RNA-seq; psoriasis skin | 33 samples | Skin cells | Independent single-cell sensitivity analysis | Used for support, not for reselecting programs |
| GSE225475 | Spatial transcriptomics; psoriasis/control skin | 6 spatial samples | Skin sections | Primary spatial contextualization | Section/spot-level observations do not replace patient-level replication |
| GSE202011 | Spatial transcriptomics; psoriasis skin | 30 spatial samples | Skin sections | External spatial robustness analysis | Spatial support is contextual and not a genetic anchor |
| GCST90472771 | GWAS summary statistics; psoriasis | 36,466 cases and 458,078 controls | Germline | Overall psoriasis susceptibility GWAS for comorbidity genetics | Overall susceptibility; not F1/F2/F6/F7-specific |
| Prespecified comorbidity GWAS panel | GWAS summary statistics; comorbid outcomes | CAD 122,733/424,528; PsA 5,065/21,286; Crohn 12,194/28,072; UC 12,366/33,609; stroke and CKD analyzed | Germline | PsA, CAD, Crohn disease, UC, ischemic stroke and CKD analyzed for shared genetic architecture | Additional prespecified outcomes remained source-unresolved and were not interpreted as biological nulls |
| GTEx v8 | eQTL summary data; non-disease reference tissues | Tissue-specific GTEx v8 sample sizes | Skin, blood, vascular/arterial, spleen, intestinal and immune-relevant tissues | Restricted SMR/HEIDI and coloc regulatory prioritization | Reference eQTL contexts may not match inflamed psoriasis tissue |

Footnote: LS, lesional skin; NL, non-lesional skin; PsA, psoriatic arthritis; CAD, coronary artery disease; UC, ulcerative colitis; CKD, chronic kidney disease; T2D, type 2 diabetes; MASLD, metabolic dysfunction-associated steatotic liver disease; MDD, major depressive disorder.

### Table 2. Evidence and final interpretation of retained molecular programs

| Program | Dominant compartment | Independent/external support | Cellular/spatial context | Genetic anchoring | Final interpretation |
| --- | --- | --- | --- | --- | --- |
| F1 | Skin-primary | GSE244679 paired-skin LS support, absolute ρ = 0.688 | Directional keratinocyte/stress-inflammatory support; spatial ρ = 0.502 and 0.489 | No robust axis-specific genetic support | Skin-primary tissue-state program |
| F2 | Skin-primary | GSE244679 paired-skin NL support, absolute ρ = 0.518 | Directional keratinocyte/stress-inflammatory support; spatial ρ = 0.506 and 0.491 | No robust axis-specific genetic support | Skin-primary program with possible field-state support |
| F6 | Skin-primary | GSE244679 paired-skin LS support, absolute ρ = 0.375 | Directional keratinocyte/stress support; spatial ρ = 0.546 and 0.496 | No robust axis-specific genetic support | Skin-primary program with stress-like features |
| F7 | Systemic/supportive | Internal skin-blood support; external cross-platform whole-blood support in GSE61281, absolute ρ = 0.455 | Low-confidence systemic immune/myeloid direction; positive spatial ρ but not coherent skin-spatial immune localization | No robust axis-specific genetic support | Systemic-supportive candidate |

Footnote: Absolute ρ denotes |ρ| for replication/support contrasts. Spatial ρ values are median within-sample spot-level Spearman correlations between prespecified CORE program scores and the dominant spatial marker program, reported for GSE225475 and GSE202011, respectively. Genetic anchoring refers to prespecified axis-specific psoriasis genetic support, not overall psoriasis susceptibility.


### Table 3. Manuscript-priority regulatory candidates

| Outcome | Locus | Gene | Representative tissue and PP4 | Evidence level | Sensitivity note |
| --- | --- | --- | --- | --- | --- |
| PsA | 887 | SLC22A5 | Spleen, PP4 = 0.971 | Supported | Standard coloc input |
| PsA | 1793 | RP11-977G19.11 | EBV-transformed lymphocytes, PP4 = 0.945 | Supported | Standard coloc input |
| UC | 2251 | RP11-973H7.1 | Transverse colon, PP4 = 0.960; sigmoid colon, PP4 = 0.960 | Supported | eQTL MAF proxy |
| CAD | 113 | UBQLN4 | Sun-exposed skin, PP4 = 0.754; non-sun-exposed skin, PP4 = 0.746 | Suggestive | Standard coloc input |
| CAD | 113 | MEX3A | Sun-exposed skin, PP4 = 0.597; non-sun-exposed skin, PP4 = 0.595 | Suggestive | Standard coloc input |
| Crohn disease | 887 | SLC22A5 | Sigmoid colon, PP4 = 0.639 | Suggestive | eQTL MAF proxy |
| Crohn disease | 10 | PARK7 | Whole blood, PP4 = 0.565 | Suggestive | eQTL MAF proxy |

Footnote: The main table is non-exhaustive. Complete tissue-level colocalization results are provided in Supplementary Data. Supported denotes PP4 ≥ 0.80. Suggestive denotes 0.50 ≤ PP4 < 0.80. eQTL MAF proxy indicates that eQTL-derived MAF was used because matched GWAS MAF was unavailable. PP4, posterior probability for a shared association signal under the coloc model.


## References

1. Rider, A., Grantham, H. J., Smith, G. R. et al. Transcriptomic profiling and machine learning uncover gene signatures of psoriasis endotypes and disease severity. *Communications Medicine* 6, 65 (2026). doi:10.1038/s43856-025-01325-4.

2. Ma, F., Plazyo, O., Billi, A. C. et al. Single-cell and spatial sequencing define processes by which keratinocytes and fibroblasts amplify inflammatory responses in psoriasis. *Nature Communications* 14, 3455 (2023). doi:10.1038/s41467-023-39020-4.

3. Dand, N. et al. GWAS meta-analysis of psoriasis identifies new susceptibility alleles impacting disease mechanisms and therapeutic targets. *Nature Communications* 16, 2051 (2025). doi:10.1038/s41467-025-56719-8.

4. Shrotri, S., Daamen, A., Kingsmore, K. et al. Transcriptomic analysis identifies disease severity and therapeutic response in psoriasis. *JID Innovations* 5, 100333 (2025). doi:10.1016/j.xjidi.2024.100333.

5. Chen, C. H., Lee, M. S., Chang, W. Y. et al. Uncovering a Dual Th17/Type 2 Transcriptomic Endotype in Psoriasis. *Journal of the American Academy of Dermatology* (2026). doi:10.1016/j.jaad.2026.06.131.

6. Castillo, R. L., Sidhu, I., Dolgalev, I. et al. Spatial transcriptomics stratifies psoriatic disease severity by emergent cellular ecosystems. *Science Immunology* 8, eabq7991 (2023). doi:10.1126/sciimmunol.abq7991.

7. Stuart, P. E. et al. Genome-wide association analysis of psoriatic arthritis and cutaneous psoriasis reveals differences in their genetic architecture. *American Journal of Human Genetics* 97, 816-836 (2015). doi:10.1016/j.ajhg.2015.10.019.

8. Patrick, M. T. et al. Shared genetic risk factors and causal association between psoriasis and coronary artery disease. *Nature Communications* 13, 6565 (2022). doi:10.1038/s41467-022-34323-4.

9. Ellinghaus, D. et al. Combined analysis of genome-wide association studies for Crohn disease and psoriasis identifies seven shared susceptibility loci. *American Journal of Human Genetics* 90, 636-647 (2012). doi:10.1016/j.ajhg.2012.02.020.

10. Vestergaard, M. V., Alfaro-Núñez, A., Sazonovs, A., Athanasiadis, G. & Jess, T. Multimodal analysis disentangles the genetic and microbial associations between inflammatory bowel disease and other immune-mediated diseases across a harmonized population framework. *Nature Communications* 17, 1849 (2026). doi:10.1038/s41467-026-68564-4.

11. Jiménez-Gracia, L. et al. Interpretable inflammation landscape of circulating immune cells. *Nature Medicine* 32, 633-644 (2026). doi:10.1038/s41591-025-04126-3.

12. Restrepo, P., Wilder, A., Houser, A. et al. Single-cell spatial transcriptomic analysis of human skin anatomy. *Nature Genetics* 58, 903-915 (2026). doi:10.1038/s41588-026-02552-8.

13. Li, X., Yan, Z., Lan, H. et al. Genetic comorbidity of psoriasis and four cardiovascular diseases: uncovering shared mechanisms and potential therapeutic targets. *Experimental Dermatology* 34, e70158 (2025). doi:10.1111/exd.70158.

14. The GTEx Consortium. The GTEx Consortium atlas of genetic regulatory effects across human tissues. *Science* 369, 1318-1330 (2020). doi:10.1126/science.aaz1776.

15. Alegbe, T. et al. Cell-type-resolved genetic variation shapes inflammatory bowel disease risk. *Nature* 656, 129-139 (2026). doi:10.1038/s41586-026-10627-z.

16. Argelaguet, R. et al. Multi-Omics Factor Analysis: a framework for unsupervised integration of multi-omics data sets. *Molecular Systems Biology* 14, e8124 (2018). doi:10.15252/msb.20178124.

17. de Leeuw, C. A., Mooij, J. M., Heskes, T. & Posthuma, D. MAGMA: generalized gene-set analysis of GWAS data. *PLoS Computational Biology* 11, e1004219 (2015). doi:10.1371/journal.pcbi.1004219.

18. Bulik-Sullivan, B. et al. An atlas of genetic correlations across human diseases and traits. *Nature Genetics* 47, 1236-1241 (2015). doi:10.1038/ng.3406.

19. Werme, J., van der Sluis, S., Posthuma, D. & de Leeuw, C. A. An integrated framework for local genetic correlation analysis. *Nature Genetics* 54, 274-282 (2022). doi:10.1038/s41588-022-01017-y.

20. Zhu, Z. et al. Integration of summary data from GWAS and eQTL studies predicts complex trait gene targets. *Nature Genetics* 48, 481-487 (2016). doi:10.1038/ng.3538.

21. Giambartolomei, C. et al. Bayesian test for colocalisation between pairs of genetic association studies using summary statistics. *PLoS Genetics* 10, e1004383 (2014). doi:10.1371/journal.pgen.1004383.

22. Argelaguet, R., Arnol, D., Bredikhin, D. et al. MOFA+: a statistical framework for comprehensive integration of multi-modal single-cell data. *Genome Biology* 21, 111 (2020). doi:10.1186/s13059-020-02015-1.
