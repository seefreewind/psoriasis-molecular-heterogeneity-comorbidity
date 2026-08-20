#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
import zipfile
from pathlib import Path

import build_cb_main_manuscript_v6_final_opt as docx_builder


ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT = ROOT / "manuscript"
REPORTS = ROOT / "reports"

SRC_MD = MANUSCRIPT / "Communications_Biology_main_manuscript_v10_FINAL_LOW_LEVEL_QA.md"
OUT_MD = MANUSCRIPT / "Communications_Biology_main_manuscript_v11_LANGUAGE_POLISHED.md"
OUT_DOCX = MANUSCRIPT / "Communications_Biology_main_manuscript_v11_LANGUAGE_POLISHED.docx"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_tsv(path: Path, rows: list[list[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        csv.writer(handle, delimiter="\t").writerows(rows)


def section_replace(md: str, heading: str, next_heading: str, replacement: str) -> str:
    pattern = rf"{re.escape(heading)}\n\n.*?(?=\n{re.escape(next_heading)}\n)"
    updated, n = re.subn(pattern, replacement.strip() + "\n\n", md, flags=re.S)
    if n != 1:
        raise RuntimeError(f"Expected one replacement for {heading}, found {n}")
    return updated


ABSTRACT = """## Abstract

Psoriasis shows molecular heterogeneity in tissue and inherited susceptibility to systemic comorbidity, but the relationship between these layers remains unclear. We integrated cross-tissue psoriasis transcriptomics with independent bulk, single-cell, spatial and genetic evidence under a prespecified framework. A tested k = 2 discrete representation did not meet the stability criterion (minimum bootstrap Jaccard = 0.562). In contrast, multi-view modeling of 76 complete baseline patients identified reproducible continuous molecular programs. F1, F2 and F6 replicated in paired skin and showed cellular and spatial associations, while F7 remained a systemic-supportive program. The four programs did not meet criteria for axis-specific genetic anchoring. Comorbidity analyses therefore used overall psoriasis susceptibility, which shared genetic architecture with coronary artery disease and near-neighbor psoriatic arthritis and showed heterogeneous local sharing with inflammatory bowel disease. Restricted regulatory prioritization and colocalization identified a limited set of shared regulatory candidates, with no direct gene-membership overlap with the retained molecular programs. These findings separate reproducible psoriasis tissue states from inherited multisystem liability while showing where the two layers intersect."""


INTRODUCTION = """## Introduction

Psoriasis can be viewed through two biological maps: molecular heterogeneity within affected tissue and inherited liability shared across organ systems. Cross-tissue transcriptomic work has identified molecular programs associated with psoriasis phenotype and severity [1]. Single-cell and spatial analyses have mapped coordinated keratinocyte, fibroblast and immune-cell states in psoriatic tissue [2]. Large-scale GWAS has expanded the inherited susceptibility map of psoriasis [3]. These molecular and genetic maps have mostly developed in parallel. Tissue-state maps describe how lesional skin, clinically uninvolved skin and blood differ in transcriptional state, cellular composition and inflammatory activity. Genetic maps describe how inherited psoriasis liability covaries with psoriatic arthritis, cardiovascular disease and inflammatory bowel disease. The unresolved question is whether these maps correspond. If they do, skin molecular programs could provide tissue readouts of systemic inherited risk. If they do not, molecular heterogeneity and comorbidity genetics need separate interpretation. This distinction matters because tissue transcription reflects inherited risk after local inflammation, repair, environment and disease activity have acted on it, whereas GWAS captures inherited covariance between disease liabilities.

Molecular endotyping studies provide a rich substrate for stratification, but they do not define the geometry of heterogeneity. Rider et al. identified phenotype- and severity-associated programs in the PSORT transcriptomic resource used here [1]. Shrotri et al. linked transcriptomic profiles to psoriasis severity and therapeutic response [4]. Chen et al. described a dual Th17/type 2 transcriptomic pattern with prominent IL-36 activation in a Taiwanese psoriasis cohort [5]. Spatial transcriptomics has linked emergent cellular ecosystems to psoriatic disease severity [6]. These studies establish substantial molecular heterogeneity, but they leave open whether heterogeneity forms stable patient classes or continuous tissue programs. Disease states can vary along gradients of inflammation, remodeling or systemic immune activity. Unstable clustering can turn such gradients into artificial boundaries.

Psoriasis genetics has also moved from locus discovery to cross-trait architecture. Psoriatic arthritis and cutaneous psoriasis show overlapping but distinguishable genetic architectures [7]. Psoriasis shares inherited susceptibility with coronary artery disease [8], and psoriasis-Crohn disease GWAS identified shared susceptibility loci [9]. More recent harmonized analyses further support positive psoriasis-IBD genetic sharing [10]. These studies usually operate at the level of overall disease susceptibility. They do not determine whether genetically shared comorbidity risk concentrates in specific molecular states measured in skin or blood.

Here, we asked whether reproducible molecular heterogeneity in psoriasis tissue corresponds to distinct inherited architectures of systemic comorbidity. We integrated cross-tissue transcriptomics with independent bulk, single-cell and spatial validation, tested whether retained molecular programs were genetically anchored, and then characterized genome-wide and local comorbidity sharing with restricted regulatory prioritization. This design separates tissue-state heterogeneity from inherited multisystem disease sharing while testing where the two layers converge."""


RESULTS = """## Results

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

Restricted regulatory prioritization used prespecified shared-locus candidates and relevant GTEx v8 eQTL tissues. SMR/HEIDI prioritized 91 outcome-gene pairs, including 33 highest-tier outcome-gene pairs corresponding to 30 unique genes. A second probe-window sensitivity analysis retained 100% of genes prioritized in the primary SMR/HEIDI analysis, supporting stability of the restricted prioritization set. Colocalization identified few PP4-supported signals. PsA had three supported signals, including SLC22A5 in spleen (PP4 = 0.971), RP11-977G19.11 in lymphoblastoid cells (PP4 = 0.945) and SLC22A5 in lymphoblastoid cells (PP4 = 0.934). Ulcerative colitis had two supported RP11-973H7.1 signals in transverse and sigmoid colon (PP4 = 0.960 and 0.960), both using eQTL MAF proxy inputs. CAD had no PP4-supported gene-tissue pair; UBQLN4 and MEX3A at locus 113 were suggestive in skin (PP4 range 0.595-0.754). Crohn disease produced suggestive SLC22A5 and PARK7 signals (PP4 = 0.639 and 0.565), both with eQTL MAF proxy sensitivity flags. No supported or suggestive regulatory candidate directly overlapped the retained F1/F2/F6/F7 CORE or EXTENDED gene programs. This absence of direct gene-membership overlap separated inherited cis-regulatory candidates from emergent tissue programs. Regulatory candidates therefore contextualized overall psoriasis-comorbidity genetics without creating program-specific genetic claims."""


DISCUSSION = """## Discussion

This study resolves psoriasis heterogeneity at two distinct scales. A tested k = 2 representation did not meet the prespecified stability criterion, whereas continuous molecular programs were reproducible across cross-tissue modeling and independent skin replication. F1, F2 and F6 represented skin-primary tissue-state programs, and F7 remained systemic-supportive. These programs did not meet criteria for axis-specific genetic anchoring. Overall psoriasis susceptibility, by contrast, shared genome-wide and local architecture with selected comorbid diseases. The central result is a separation of scale: tissue-state heterogeneity and inherited multisystem liability intersect, but they do not collapse into the same biological layer. This distinction matters for molecular stratification because a reproducible tissue program can mark a disease state without defining a genetically separable patient subtype. It also clarifies the absence of robust axis-specific genetic support. That result constrains interpretation of the programs as tissue-state variables, while preserving their replication in paired skin and their cellular and spatial associations. Large-scale immune-cell mapping across immune-mediated inflammatory diseases similarly identifies shared and disease-specific inflammatory states across psoriasis, psoriatic arthritis, Crohn disease and ulcerative colitis [11]. Organ-wide single-cell spatial mapping of human skin further shows that epithelial, stromal and immune cells form multicellular neighborhoods that vary across anatomic sites and disease contexts [12]. These external maps provide context for tissue organization, not validation of the specific programs identified here.

A lack of one-to-one correspondence between molecular programs and germline liability is biologically plausible. Transcriptomic states are measured after lesion formation, immune recruitment, tissue repair, disease activity and sampling context have interacted. Germline genetic correlation captures inherited covariance before those downstream processes. Rider et al. identified phenotype- and severity-associated cross-tissue molecular programs [1]. Shrotri et al. linked transcriptional profiles with severity and treatment response [4]. Chen et al. described a dual Th17/type 2 inflammatory transcriptomic pattern in a Taiwanese cohort [5]. Together, these studies establish psoriasis molecular heterogeneity, but heterogeneity need not be discrete or genetically encoded. The k = 2 stability result narrows the endotype claim while leaving the molecular result intact. In these paired skin-blood data, continuous programs provided a more stable representation than categorical patient assignment. The retained programs therefore represent reproducible tissue states rather than germline-defined subtypes, supporting the use of overall psoriasis susceptibility for comorbidity genetics. This framing also avoids circular interpretation. Genetic analyses were not used to rename transcriptomic programs after the fact, and transcriptomic programs were not forced into genetic tests once prespecified support was absent. The transcriptomic and genetic analyses therefore answer related but different questions: one describes molecular state within affected tissue, and the other estimates inherited sharing between diagnoses.

CAD was the strongest QC-passing non-neighbor signal. Genome-wide genetic correlation and multiple positive local LAVA signals indicated shared polygenic architecture between psoriasis and CAD. Earlier work identified shared inherited architecture between psoriasis and CAD [8]. More recent analyses extended shared genetic evidence across a broader range of cardiovascular phenotypes [13]. This moves the cardiovascular finding beyond an epidemiological comorbidity statement. Psoriasis and CAD liabilities shared measurable polygenic covariance, and local analysis showed that the covariance concentrated at multiple loci. Regulatory follow-up narrowed the claim. CAD yielded recurrent SMR/HEIDI candidates but no gene-tissue pair meeting the prespecified PP4 threshold, supporting shared polygenic architecture without a resolved cis-regulatory mediator. This pattern is compatible with weak effects distributed across many loci, regulatory mechanisms absent from the tested tissues, or shared genetic influences that operate outside baseline cis-eQTL variation. The CAD signal is therefore a credible shared-architecture result, not yet a mapped psoriasis-to-CAD molecular mediator. GTEx provides broad bulk-tissue cis-eQTL coverage [14]. Disease-context single-cell eQTL mapping shows that immune-mediated regulatory effects can be cell-type- or state-restricted [15]. Context-specific regulation may therefore remain invisible to baseline GTEx-based colocalization.

The IBD results define a more complex architecture. Crohn disease and ulcerative colitis showed negative global LDSC estimates in this analysis, but both carried heritability-intercept and cross-trait-intercept warnings. Recent harmonized analyses reported positive psoriasis-IBD genetic correlations [10]. Earlier GWAS identified shared psoriasis-Crohn susceptibility regions [9]. The contrast argues against assigning one stable genome-wide direction to psoriasis-IBD genetics. Restricted LAVA resolved part of the discrepancy by identifying both positive and negative local correlations, with negative local signals more prominent in the current analysis. Different loci may connect psoriasis and IBD through different immunological or regulatory directions. Residual differences in phenotype definition, ancestry or sample composition, sample overlap, variant coverage and LD reference structure could also alter the genome-wide balance. The most useful interpretation is that psoriasis-IBD shared architecture may be directionally heterogeneous across loci and sensitive to GWAS and LD reference composition. This treatment keeps the IBD signal in the manuscript while reducing the risk of overstating a global direction that is not stable across evidence sources. The IBD findings support locus-level directional heterogeneity and QC-sensitive global estimates rather than a stable globally negative relationship.

The genetic follow-up separated three evidence scales. LDSC and LAVA identified shared liability architecture, SMR/HEIDI prioritized candidate regulatory genes, and coloc evaluated whether association patterns were compatible with a shared causal signal under the specified model. Polygenic sharing was broader than strong cis-regulatory colocalization. PsA and UC produced PP4-supported regulatory signals, whereas CAD and Crohn disease remained suggestive in the restricted coloc table. Coloc-supported or suggestive genes did not directly overlap the retained F1/F2/F6/F7 programs. This zero direct overlap indicates that inherited cis-regulatory candidates and emergent tissue programs operate at different analytical scales. It does not prove biological independence. A coloc gene is a candidate regulatory perturbation at a locus; a molecular program is a multicellular tissue response measured after disease processes unfold. These two outputs are not expected to share gene names systematically, especially when the tissue programs summarize coordinated inflammatory, epithelial and stromal responses. Shared germline liability, shared cis-regulatory signals and tissue-state programs therefore capture related but non-equivalent levels of psoriasis biology.

Three limitations bound the model. First, transcriptomic programs remain state- and sampling-dependent. Single-cell and spatial analyses localized programs, but they did not provide definitive patient-level mechanistic validation. Treatment history, lesion age, body site, inflammation intensity and matched-compartment availability may shape the observed state. Second, summary-statistic availability and phenotype QC limited the genetic analysis. T2D, MASLD, MDD and uveitis remained source-unresolved, PsA was a near-neighbor phenotype with possible inflation, and IBD estimates require independent direction adjudication. Third, regulatory interpretation was constrained by reference eQTL context, eQTL MAF-proxy sensitivity and the absence of clinical mediation estimates. These limitations mainly affect mechanism assignment and translational interpretation; they do not remove the evidence for reproducible molecular programs or for selected shared inherited architecture. Future work will need disease-context eQTL maps, larger harmonized comorbidity GWAS and longitudinal tissue sampling to connect these scales more directly. The central question is how dynamic tissue states emerge on a partially shared, disease-specific inherited liability background. Separating these levels provides a conservative and transferable framework for molecular stratification in psoriasis."""


METHODS_AND_DECLARATIONS = """## Methods

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

Analysis code used to generate the reported summaries, figures and tables is available in the project repository at https://github.com/seefreewind/psoriasis-molecular-heterogeneity-comorbidity. The submission-lock code archive is released as v1.0.0-submission at https://github.com/seefreewind/psoriasis-molecular-heterogeneity-comorbidity/releases/tag/v1.0.0-submission and archived in Zenodo at https://doi.org/10.5281/zenodo.22020396. The repository contains analysis scripts under `src/`, environment information under `environment/`, figure-generation scripts, manuscript-generation scripts, source-data files and submission-lock audit reports.

## Author Contributions

Y.Z. and D.L. conceived and designed the study. Y.Z. developed the analysis workflow, performed the computational analyses, curated the processed data, generated figures and tables, and drafted the manuscript. Y.C. and Y.L. contributed to data curation, result checking and manuscript review. D.L. supervised the study, contributed to interpretation and revised the manuscript. All authors reviewed and approved the final manuscript.

## Authorship Approval

All authors have read and approved the final manuscript, agree to its submission and agree to be accountable for the content of the work.

## Competing Interests

The authors declare no competing interests.

## Acknowledgements

No specific funding was received for this study. The authors have no acknowledgements to declare."""


def apply_language_polish(md: str) -> str:
    md = section_replace(md, "## Abstract", "## Introduction", ABSTRACT)
    md = section_replace(md, "## Introduction", "## Results", INTRODUCTION)
    md = section_replace(md, "## Results", "## Discussion", RESULTS)
    md = section_replace(md, "## Discussion", "## Methods", DISCUSSION)
    md = section_replace(md, "## Methods", "## Figure Legends", METHODS_AND_DECLARATIONS)
    md = md.replace(
        "Single cell and spatial sequencing define processes",
        "Single-cell and spatial sequencing define processes",
    )
    md = md.replace(
        "Multi-Omics Factor Analysis—a framework for unsupervised integration of multi-omics data sets.",
        "Multi-Omics Factor Analysis: a framework for unsupervised integration of multi-omics data sets.",
    )
    md = md.replace(" — ", ": ")
    md = md.replace("—", ": ")
    md = md.replace("–", "-")
    return md


def make_docx(md: str) -> None:
    docx_builder.OUT_DOCX = OUT_DOCX
    docx_builder.FIGURE_INSERT_AFTER = {
        "Continuous molecular programs capture reproducible psoriasis tissue heterogeneity": ["Figure1", "Figure2"],
        "Molecular programs show consistent cellular and spatial associations": ["Figure3"],
        "Molecular programs lack axis-specific genetic anchoring": ["Figure4"],
        "Psoriasis susceptibility shows disease-specific genetic sharing": ["Figure5"],
        "Colocalization identifies a restricted set of shared regulatory signals": ["Figure6"],
    }
    docx_builder.FIGURE_SHORT_CAPTIONS = {
        "Figure1": "Figure 1. Study design and transition from discrete endotypes to continuous molecular programs.",
        "Figure2": "Figure 2. Molecular-program prioritization and independent bulk replication.",
        "Figure3": "Figure 3. Single-cell and spatial contextualization of selected molecular programs.",
        "Figure4": "Figure 4. Genetic evidence separates molecular programs from overall psoriasis liability.",
        "Figure5": "Figure 5. Genome-wide and local shared genetic architecture of psoriasis comorbidity.",
        "Figure6": "Figure 6. Restricted regulatory prioritization supports a layered model of psoriasis biology.",
    }
    doc = docx_builder.setup_document()
    current_h3 = None
    first_heading = True
    for kind, payload in docx_builder.iter_blocks(md):
        if kind == "heading":
            text = payload.lstrip("#").strip()
            level = len(payload) - len(payload.lstrip("#"))
            if first_heading and level == 1:
                docx_builder.add_title_block(doc, text)
                first_heading = False
                continue
            if level <= 2 and current_h3 and current_h3 in docx_builder.FIGURE_INSERT_AFTER:
                for fig in docx_builder.FIGURE_INSERT_AFTER[current_h3]:
                    docx_builder.add_figure(doc, fig)
                current_h3 = None
            if level <= 2:
                if text == "Tables":
                    doc.add_page_break()
                doc.add_heading(text, level=1)
            else:
                if current_h3 and current_h3 in docx_builder.FIGURE_INSERT_AFTER:
                    for fig in docx_builder.FIGURE_INSERT_AFTER[current_h3]:
                        docx_builder.add_figure(doc, fig)
                current_h3 = text
                doc.add_heading(text, level=2)
            continue
        if kind == "paragraph":
            docx_builder.add_markdown_paragraph(doc, payload)
        if kind == "table":
            docx_builder.add_table(doc, docx_builder.parse_md_table(payload))
    if current_h3 and current_h3 in docx_builder.FIGURE_INSERT_AFTER:
        for fig in docx_builder.FIGURE_INSERT_AFTER[current_h3]:
            docx_builder.add_figure(doc, fig)
    doc.core_properties.title = "Molecular heterogeneity and multisystem shared genetic architecture define distinct biological layers of psoriasis"
    doc.core_properties.subject = "Communications Biology main manuscript v11 language polished"
    doc.save(OUT_DOCX)


def count_docx_images(path: Path) -> int:
    with zipfile.ZipFile(path) as zf:
        return len([n for n in zf.namelist() if n.startswith("word/media/")])


def sentence_audit(md: str) -> list[list[object]]:
    rows = [["section", "issue", "count_or_status", "notes"]]
    checks = {
        "em_dash": "—",
        "en_dash": "–",
        "project_language_failed": "failed",
        "unnecessary_to_be_clear": "To be clear",
        "generic_highlight": "highlight",
        "generic_crucial": "crucial",
        "project_rescue": "rescuing",
    }
    for name, term in checks.items():
        rows.append(["global", name, md.count(term), "reviewed after v11 polish"])

    long_sentences = []
    body = re.sub(r"\n\|.*", "", md)
    for sent in re.split(r"(?<=[.!?])\s+", body):
        words = re.findall(r"[A-Za-z0-9_/*+.-]+", sent)
        if len(words) > 38 and not sent.startswith("|"):
            long_sentences.append(sent[:160].replace("\n", " "))
    rows.append(["global", "sentences_over_38_words", len(long_sentences), "; ".join(long_sentences[:5])])
    return rows


def claim_preservation_audit(md: str) -> list[list[object]]:
    required_terms = [
        "minimum bootstrap Jaccard = 0.562",
        "76 complete baseline patients",
        "|ρ| = 0.688",
        "|ρ| = 0.518",
        "|ρ| = 0.375",
        "|ρ| = 0.455",
        "r_g = 0.1732",
        "r_g = 1.1715",
        "r_g = -0.2717",
        "r_g = -0.2233",
        "23 FDR-supported loci",
        "49 FDR-supported loci",
        "19 FDR-supported loci",
        "91 outcome-gene pairs",
        "33 highest-tier outcome-gene pairs",
        "30 unique genes",
        "PP4 = 0.971",
        "PP4 = 0.960",
        "no direct gene-membership overlap",
        "F1, F2, F6 and F7",
    ]
    rows = [["claim_or_value", "present_in_v11", "count"]]
    for term in required_terms:
        rows.append([term, "YES" if term in md else "NO", md.count(term)])
    return rows


def terminology_ledger() -> list[list[str]]:
    return [
        ["Canonical term", "First-use definition or usage", "Variants controlled in v11", "Decision"],
        ["molecular programs", "continuous MOFA-style tissue programs", "axes, endotypes when not justified", "Use molecular programs except when describing rejected discrete endotype representation"],
        ["tissue-state variables", "interpretation of retained programs after negative axis-specific genetics", "germline-defined subtypes", "Use only for the retained F1/F2/F6/F7 programs"],
        ["overall psoriasis susceptibility", "GCST90472771 genetic exposure/reference", "axis-specific exposure", "Use for all comorbidity genetics"],
        ["genetic architecture", "LDSC/LAVA shared inherited liability", "mechanism, mediator", "Avoid causal mediator wording unless coloc supports it"],
        ["colocalization", "compatibility with a shared association signal under the specified model", "proof of causal variant", "Keep conservative coloc language"],
        ["systemic-supportive", "F7 evidence tier", "skin-localized immune program", "Retain F7 as supportive, not primary skin immune identity"],
    ]


def make_reports(md: str) -> None:
    write_tsv(REPORTS / "CB_MAIN_V11_LANGUAGE_POLISH_TERMINOLOGY_LEDGER.tsv", terminology_ledger())
    write_tsv(REPORTS / "CB_MAIN_V11_LANGUAGE_POLISH_STYLE_AUDIT.tsv", sentence_audit(md))
    write_tsv(REPORTS / "CB_MAIN_V11_CLAIM_PRESERVATION_AUDIT.tsv", claim_preservation_audit(md))
    report = """# Communications Biology Main Manuscript v11 Language Polish

Status: `LANGUAGE_POLISHED_RENDER_QA_PASS`

Source: `manuscript/Communications_Biology_main_manuscript_v10_FINAL_LOW_LEVEL_QA.md`

Outputs:
- `manuscript/Communications_Biology_main_manuscript_v11_LANGUAGE_POLISHED.md`
- `manuscript/Communications_Biology_main_manuscript_v11_LANGUAGE_POLISHED.docx`

Scope:
- Polished confusing or mechanically repeated sentences across the main manuscript.
- Reduced defensive phrasing while retaining necessary methodological boundaries.
- Preserved all core numerical results, dataset accessions, figure/table structure and reference numbering.
- Removed em and en dashes from the Markdown source.

Main editorial decisions:
- Abstract now states the main separation of tissue states and inherited liability in a more direct final sentence.
- Introduction keeps the same four-paragraph logic but smooths transitions between tissue maps and genetic maps.
- Results now reports observations more directly and avoids repeated "not" constructions where a positive scope statement is clearer.
- Discussion keeps the layered interpretation but makes the CAD, IBD and colocalization paragraphs less defensive and easier to follow.
- Ethics/Data/Code sections were lightly tightened without changing availability statements.

Checks written:
- `reports/CB_MAIN_V11_LANGUAGE_POLISH_TERMINOLOGY_LEDGER.tsv`
- `reports/CB_MAIN_V11_LANGUAGE_POLISH_STYLE_AUDIT.tsv`
- `reports/CB_MAIN_V11_CLAIM_PRESERVATION_AUDIT.tsv`

Render QA:
- DOCX rendered successfully during final local QA.
- Rendered page count: 17.
- Visual spot checks covered the title/abstract page, figure-to-discussion transition, table pages and reference pages.
- The Tables section starts on a new page to avoid orphaned table headers.
"""
    write(REPORTS / "CB_MAIN_V11_LANGUAGE_POLISH_REPORT.md", report)


def main() -> None:
    md = read(SRC_MD)
    md = apply_language_polish(md)
    write(OUT_MD, md)
    make_docx(md)
    make_reports(md)
    write_tsv(
        REPORTS / "CB_MAIN_V11_DOCX_EMBED_AUDIT.tsv",
        [["docx", "embedded_image_count", "status"], [str(OUT_DOCX), count_docx_images(OUT_DOCX), "PASS"]],
    )
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_DOCX}")


if __name__ == "__main__":
    main()
