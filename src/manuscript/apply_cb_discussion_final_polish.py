from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
V3 = ROOT / "manuscript" / "Communications_Biology_main_manuscript_v3.md"
V4 = ROOT / "manuscript" / "Communications_Biology_main_manuscript_v4.md"
REPORT_DIR = ROOT / "reports"


DISCUSSION = """## Discussion

This study separates two biological layers that can be conflated in molecular stratification studies of psoriasis: the molecular state of diseased tissue and the inherited liability that links psoriasis to systemic disease. Across bulk transcriptomic discovery, independent skin replication, donor-level single-cell contextualization and spatial transcriptomic support, the reproducible signal was not a stable categorical partition of patients. It was a set of continuous tissue molecular programs, strongest for skin-primary programs F1, F2 and F6, with F7 retained as a systemic-supportive candidate rather than as a skin-localized mechanism. The genetic analyses then drew a second boundary. These transcriptomic programs did not become genetically anchored psoriasis axes, whereas overall psoriasis susceptibility showed shared genome-wide and local architecture with selected comorbid diseases. This separation is important because a tissue-state signal and a liability signal answer different biological questions. The former describes the configuration of inflamed tissue at sampling, whereas the latter describes inherited covariance across disease risks. A useful model is therefore layered rather than linear: psoriasis contains reproducible inflammatory and tissue-remodelling states, while inherited susceptibility operates at a broader liability layer that can intersect cardiovascular, articular and intestinal disease systems. Recent large-scale immune-cell mapping across immune-mediated inflammatory diseases similarly emphasizes shared and disease-specific inflammatory states across conditions that include psoriasis, psoriatic arthritis, Crohn disease and ulcerative colitis, but those maps should be read here as conceptual context rather than validation of the factors identified in this study [17].

This layered view refines transcriptomic endotype work in psoriasis. Recent studies have reported psoriasis expression signatures associated with endotypes, disease severity, response and mixed inflammatory patterns [2-4]. Our analysis reached a different emphasis because the first decision point was not whether transcriptomic heterogeneity exists, but whether a discrete k = 2 patient boundary is stable enough to carry a mechanistic and translational claim. In the matched multi-tissue discovery setting used here, bootstrap stability did not support that categorical boundary, so we shifted the unit of interpretation from class labels to continuous molecular axes. This result should not be read as evidence that psoriasis has no categorical endotypes under any design. It shows that, in these paired skin-blood data, a binary endotype model was less robust than continuous programs. The biological consequences of these two models are different. A categorical endotype implies patient subgroup assignment and potential stratification. A continuous program supports language about graded tissue states, field effects and pathway intensity. The latter is a narrower claim, but it is also more faithful to the evidence generated here.

The absence of robust axis-specific genetic anchoring is biologically interpretable. Germline risk variants act before lesion formation, treatment exposure, local immune recruitment and tissue repair. Bulk and single-cell transcriptomic programs are measured after these processes have already interacted with microenvironment, disease activity and sampling context. It is therefore plausible for F1, F2 and F6 to be reproducible skin tissue-state variables without being independent inherited axes. F7 occupies a slightly different position. Its internal skin-blood support and external blood support make it the best systemic-supportive candidate in the molecular layer, but its low-confidence skin-spatial localization argues against treating it as a pan-inflammatory psoriasis axis. Large psoriasis GWAS meta-analysis continues to expand the set of inherited susceptibility loci and implicates immune and skin-relevant biology [7], yet those loci need not map one-to-one onto latent transcriptomic factors measured in diseased tissue. This negative genetic result does not diminish the reproducibility of the molecular programs. It constrains their interpretation as tissue-state variables rather than germline-defined subtypes, and it supports anchoring comorbidity genetics to overall psoriasis susceptibility.

Within the comorbidity layer, coronary artery disease was the cleanest non-neighbour signal. Psoriasis and coronary artery disease showed a positive genome-wide genetic correlation, passed the main LDSC quality-control criteria, and yielded multiple positive local LAVA signals. This finding is directionally consistent with previous evidence that psoriasis shares genetic risk with coronary artery disease and cardiovascular traits [8,18], and it provides a stronger basis for discussing cardiovascular comorbidity than the tissue-axis genetic analyses did. It also shifts the interpretation away from a generic epidemiological comorbidity statement. The CAD signal is a genetic-architecture result: psoriasis liability and CAD liability share measurable polygenic covariance, and that covariance is concentrated at multiple loci rather than being visible only as a diffuse genome-wide estimate. The regulatory follow-up places a clear limit on the interpretation. Although CAD had recurrent Tier A SMR/HEIDI-prioritized genes and suggestive coloc signals for UBQLN4 and MEX3A in skin tissues, no CAD gene-tissue pair reached the prespecified PP4-supported threshold. Thus, the CAD result supports shared polygenic architecture, not a single shared cis-eQTL mediator. Several explanations remain compatible with the data: the covariance may be distributed across many variants with small effects; shared loci may act through disease-, cell-state- or stimulation-dependent regulatory effects absent from baseline GTEx tissues [15,20]; or the relevant mediator may not be captured by the eQTL panels used here. The conservative claim is not that CAD lacks a shared regulatory mechanism with psoriasis. It is that this analysis did not identify a high-confidence shared CAD eQTL mediator after restricted coloc filtering.

The intestinal disease results require explicit handling because the direction of the genome-wide correlations differs from recent external literature. In our LDSC analysis, Crohn disease and ulcerative colitis showed significant negative genetic correlations with psoriasis, but both traits carried elevated heritability-intercept and cross-trait-intercept warnings. A 2026 harmonized population study reported positive genetic correlations of psoriasis with Crohn disease and ulcerative colitis [19], and older shared-locus work also supports genetic overlap between psoriasis and Crohn disease [10]. The discrepancy makes a simple directional statement inappropriate. The most defensible interpretation is that the current IBD results expose directional heterogeneity and quality-control sensitivity rather than a stable negative liability relationship. Restricted LAVA was informative in this respect: Crohn disease and ulcerative colitis contained both positive and negative local correlations, with negative local signals more prominent in the current analysis. That pattern is compatible with a genome in which different loci connect psoriasis and IBD through different immunological or regulatory directions. It is also compatible with residual differences in phenotype definition, ancestry or sample composition, sample overlap, variant coverage, LD reference structure and the balance of positive and negative local covariance. In practical terms, the IBD finding should be used to motivate locus-level follow-up and cross-source direction checks, not to rewrite the known clinical or genetic relationship between psoriasis and intestinal inflammation. For this reason, the IBD section should be framed around local directional heterogeneity and the need for adjudicated replication, not around a protective or globally inverse relationship.

The LDSC-to-LAVA-to-SMR/HEIDI-to-coloc sequence gives the genetic layer a useful hierarchy. LDSC defined the genome-wide liability relationship, LAVA localized where sharing was concentrated, SMR/HEIDI prioritized gene-level regulatory associations within frozen shared loci, and coloc evaluated whether the association patterns were compatible with a shared causal signal under the specified model. The 100% gene-level retention from SMR to SMR2 indicates prioritization stability under the recurrent SMR2 screen; it does not constitute causal replication. Among 91 frozen outcome-gene rows, 33 reached the highest SMR/HEIDI tier, but strong coloc support was restricted. PsA functioned as a positive-control near-neighbour phenotype with PP4-supported regulatory signals, and UC had PP4-supported RP11-973H7.1 signals under an eQTL MAF-proxy sensitivity setting. CAD and Crohn disease remained suggestive rather than PP4-supported in the restricted coloc table. The absence of direct overlap between these coloc-supported or suggestive genes and the frozen F1/F2/F6/F7 programs is also informative. It argues against a direct axis-to-coloc-gene narrative and supports a scale distinction: a coloc gene is a candidate inherited cis-regulatory perturbation at a locus, whereas a molecular program is an emergent multicellular tissue response. Disease-context and cell-type-resolved eQTL studies in IBD show that many regulatory effects are cell-type-specific or context-restricted and may be missed in bulk reference tissue maps [20]. This reinforces the need to interpret GTEx-based coloc as restricted regulatory prioritization rather than final mechanism assignment.

Several limitations define how far this model should be taken. First, the transcriptomic layer remains state- and sampling-dependent. The skin-primary programs were reproducible across bulk skin data and directionally supported by single-cell and spatial analyses, but the cellular and spatial evidence is contextual rather than definitive patient-level mechanistic validation. Treatment history, lesion age, body site, inflammation intensity and the availability of matched compartments can all influence the observed state. Second, the genetic layer is limited by summary-statistic availability, power and quality control. T2D, MASLD, MDD and uveitis were source-unresolved in the frozen primary panel at this stage and should not be interpreted as null outcomes. PsA is a near-neighbour phenotype with probable high shared liability and potential overlap-related inflation, while the Crohn disease and ulcerative colitis correlations require independent direction adjudication. Third, functional interpretation is constrained by reference eQTL context, MAF-proxy sensitivity in selected coloc analyses, and the fact that statistical sharing does not identify clinical mediation. The relevant question may therefore be less which transcriptomic endotype carries each comorbidity than how dynamic tissue states emerge on a partially shared, disease-specific inherited liability landscape. Separating these levels provides a more conservative and potentially more transferable framework for molecular stratification in psoriasis."""


def section_between(text: str, start: str, end: str) -> str:
    pattern = re.compile(rf"^{re.escape(start)}\n.*?(?=^{re.escape(end)}\n)", re.M | re.S)
    match = pattern.search(text)
    if not match:
        raise RuntimeError(f"Could not find section {start} to {end}")
    return match.group(0).rstrip()


def count_words(markdown: str) -> int:
    body = re.sub(r"^## .*$", "", markdown, flags=re.M)
    body = re.sub(r"\[[0-9,\- ]+\]", "", body)
    return len(re.findall(r"\b[\w'-]+\b", body))


def count_paragraphs(markdown: str) -> int:
    body = markdown.split("\n", 1)[1].strip()
    return len([p for p in body.split("\n\n") if p.strip()])


def replace_discussion(text: str) -> str:
    return re.sub(
        r"^## Discussion\n.*?(?=^## Methods\n)",
        DISCUSSION + "\n\n",
        text,
        flags=re.M | re.S,
    )


def write_report(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    source = V3.read_text(encoding="utf-8")
    target = replace_discussion(source)
    V4.write_text(target, encoding="utf-8")

    discussion = section_between(target, "## Discussion", "## Methods")
    words = count_words(discussion)
    paragraphs = count_paragraphs(discussion)

    write_report(
        REPORT_DIR / "CB_DISCUSSION_FINAL_POLISH_REPORT.md",
        f"""# Communications Biology Discussion Final Polish Report

## Output

- Source manuscript: `manuscript/Communications_Biology_main_manuscript_v3.md`
- Polished manuscript: `manuscript/Communications_Biology_main_manuscript_v4.md`
- Section changed: Discussion only
- References changed: no new references; CAD paragraph now cites `[15,20]` for reference-eQTL/context-specific regulation limits
- Methods/Results changed: no

## Length And Structure

| Item | Value |
| --- | ---: |
| Discussion paragraphs | {paragraphs} |
| Approximate Discussion word count | {words} |

## Targeted Polish Actions

| Issue | Action | Status |
| --- | --- | --- |
| Field-wide wording too broad | Replaced \"often collapsed\" with \"can be conflated\". | PASS |
| Residual manuscript/workflow language | Replaced internal phrasing with scientific interpretation language. | PASS |
| Axis genetics negative result wording | Reframed as interpretive constraint, not as a rescue/failure narrative. | PASS |
| CAD context-specific regulation support | Added `[15,20]` to the GTEx/context-specific regulation sentence. | PASS |
| IBD QC explanation | Removed allele-harmonization as a central explanation and emphasized phenotype, sample composition, overlap, variant coverage and LD/reference structure. | PASS |
| Coloc causality wording | Replaced direct causal-variant wording with model-compatible shared causal signal wording. | PASS |
| Post hoc hub/network language | Removed Discussion self-commentary about avoiding hub/network expansion. | PASS |
| Closing concept | Recast final two sentences around dynamic tissue states on inherited liability landscapes. | PASS |

## Seal Recommendation

Discussion is suitable to freeze after this pass. Further edits should be limited to copy-editing or journal-format changes unless new analyses change the evidence base.
""",
    )

    write_report(
        REPORT_DIR / "CB_CROSS_SECTION_CLAIM_CONSISTENCY_AUDIT.md",
        """# Abstract-Introduction-Results-Discussion Claim Consistency Audit

## Scope

Audit target: `manuscript/Communications_Biology_main_manuscript_v4.md`.

This audit checks whether the Abstract, Introduction, Results and Discussion use consistent claim strength for the same major findings.

## Findings

| Claim area | Abstract | Introduction | Results | Discussion | Consistency decision |
| --- | --- | --- | --- | --- | --- |
| Discrete endotypes | States unsupervised discrete transcriptomic endotypes were unstable. | Frames the need to test whether tissue heterogeneity and inherited risk are the same layer. | Reports k = 2 instability and pivot to continuous programs. | Interprets k = 2 as unsupported in this design, without denying all possible endotypes. | PASS |
| Continuous molecular programs | States F1/F2/F6/F7 were retained as frozen molecular programs. | Sets up molecular axes as a way to model heterogeneity. | Reports replication and contextual support for F1/F2/F6/F7. | Interprets F1/F2/F6 as tissue-state variables and F7 as systemic-supportive. | PASS |
| Axis-specific genetics | States axis-specific genetic anchoring failed for all four programs. | Separates tissue programs from inherited comorbidity architecture. | Reports Tier D/no robust genetic anchoring. | Treats negative genetics as an interpretation constraint, not invalidation of transcriptomic reproducibility. | PASS |
| CAD | States overall psoriasis susceptibility shows a clean positive CAD genetic correlation. | Positions cardiovascular comorbidity as a systemic question. | Reports CAD LDSC/LAVA/SMR-coloc pattern. | Interprets CAD as shared polygenic architecture without PP4-supported mediator. | PASS |
| PsA | States strong positive-control sharing with PsA. | Frames PsA as related but not the main multisystem proof. | Reports near-neighbour/positive-control behavior. | Keeps PsA as positive-control near-neighbour phenotype. | PASS |
| Crohn/UC | Abstract avoids overclaiming IBD direction. | Introduces IBD as comorbidity context. | Reports negative rg with QC flags and mixed local structure. | Explicitly contrasts external positive literature and frames result as local directional heterogeneity/QC-sensitive. | PASS |
| SMR/coloc | States restricted prioritization yielded limited candidates without overlap with frozen programs. | Sets up genetics as anchored to overall susceptibility. | Reports 91 rows, 33 Tier A, PP4-supported/suggestive candidates. | Describes SMR2 as prioritization stability and coloc as model-compatible shared signal evaluation. | PASS |
| Clinical/causal translation | Abstract uses layered model language. | Does not promise clinical validation. | Reports statistical evidence only. | States statistical sharing does not identify clinical mediation. | PASS |

## Residual Risks

| Risk | Severity | Recommendation |
| --- | --- | --- |
| Abstract is necessarily compact and may not mention the IBD external-direction discordance. | Low | Accept; detailed contradiction handling belongs in Discussion. |
| Figure legends still describe planned figures rather than final camera-ready legends. | Medium | Address during figure/table package preparation. |
| Data availability and source-unresolved outcomes require final submission-stage wording. | Medium | Address in Data/Code Availability audit. |

## Decision

No cross-section claim-strength contradiction requiring scientific revision was detected. The manuscript is ready for the next stage: reference accuracy, figure/table, supplementary and availability audits.
""",
    )

    print(f"Wrote {V4.relative_to(ROOT)}")
    print(f"Discussion paragraphs: {paragraphs}")
    print(f"Discussion words: {words}")
    print("Reports written:")
    print("- reports/CB_DISCUSSION_FINAL_POLISH_REPORT.md")
    print("- reports/CB_CROSS_SECTION_CLAIM_CONSISTENCY_AUDIT.md")


if __name__ == "__main__":
    main()
