from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
V1 = ROOT / "manuscript" / "Communications_Biology_main_manuscript_v1.md"
V3 = ROOT / "manuscript" / "Communications_Biology_main_manuscript_v3.md"
REPORT_DIR = ROOT / "reports"


DISCUSSION = """## Discussion

This study separates two biological layers that are often collapsed into a single endotype narrative in psoriasis: the molecular state of diseased tissue and the inherited liability that links psoriasis to systemic disease. Across bulk transcriptomic discovery, independent skin replication, donor-level single-cell contextualization and spatial transcriptomic support, the reproducible signal was not a stable categorical partition of patients. It was a set of continuous tissue molecular programs, strongest for skin-primary programs F1, F2 and F6, with F7 retained as a systemic-supportive candidate rather than as a skin-localized mechanism. The genetic analyses then drew a second boundary. These transcriptomic programs did not become genetically anchored psoriasis axes, whereas overall psoriasis susceptibility showed shared genome-wide and local architecture with selected comorbid diseases. A useful model is therefore layered rather than linear: psoriasis contains reproducible inflammatory and tissue-remodelling states, while inherited susceptibility operates at a broader liability layer that can intersect cardiovascular, articular and intestinal disease systems. Recent large-scale immune-cell mapping across immune-mediated inflammatory diseases similarly emphasizes shared and disease-specific inflammatory states across conditions that include psoriasis, psoriatic arthritis, Crohn disease and ulcerative colitis, but those maps should be read here as conceptual context rather than validation of the factors identified in this study [17].

This layered view refines, rather than dismisses, transcriptomic endotype work in psoriasis. Recent studies have reported psoriasis expression signatures associated with endotypes, disease severity, response and mixed inflammatory patterns [2-4]. Our analysis reached a different emphasis because the first decision point was not whether transcriptomic heterogeneity exists, but whether a discrete k = 2 patient boundary is stable enough to carry a mechanistic and translational claim. In the matched multi-tissue discovery setting used here, bootstrap stability did not support that categorical boundary, so we shifted the unit of interpretation from class labels to continuous molecular axes. This result should not be read as evidence that psoriasis has no categorical endotypes under any design. It shows that, in these paired skin-blood data, a binary endotype model was less robust than continuous programs. That distinction matters for manuscript claims. A categorical endotype invites language about patient subgroups, assignment and clinical stratification. A continuous program supports language about graded tissue states, field effects and pathway intensity. The latter is a narrower claim, but it is also more faithful to the evidence generated here.

The absence of robust axis-specific genetic anchoring is biologically interpretable. Germline risk variants act before lesion formation, treatment exposure, local immune recruitment and tissue repair. Bulk and single-cell transcriptomic programs are measured after these processes have already interacted with microenvironment, disease activity and sampling context. It is therefore plausible for F1, F2 and F6 to be reproducible skin tissue-state variables without being independent inherited axes. F7 occupies a slightly different position. Its internal skin-blood support and external blood support make it the best systemic-supportive candidate in the molecular layer, but its low-confidence skin-spatial localization argues against treating it as a pan-inflammatory psoriasis axis. Large psoriasis GWAS meta-analysis continues to expand the set of inherited susceptibility loci and implicates immune and skin-relevant biology [7], yet those loci need not map one-to-one onto latent transcriptomic factors measured in diseased tissue. In this study, the failure of axis-specific genetics is therefore not a failed rescue problem. It is a boundary condition: the frozen molecular programs describe reproducible tissue and supportive systemic states, while the comorbidity genetics should be anchored to overall psoriasis susceptibility.

Within the comorbidity layer, coronary artery disease was the cleanest non-neighbour signal. Psoriasis and coronary artery disease showed a positive genome-wide genetic correlation, passed the main LDSC quality-control criteria, and yielded multiple positive local LAVA signals. This finding is directionally consistent with previous evidence that psoriasis shares genetic risk with coronary artery disease and cardiovascular traits [8,18], and it provides a stronger basis for discussing cardiovascular comorbidity than the tissue-axis genetic analyses did. It also shifts the interpretation away from a generic epidemiological comorbidity statement. The CAD signal is a genetic-architecture result: psoriasis liability and CAD liability share measurable polygenic covariance, and that covariance is concentrated at multiple loci rather than being visible only as a diffuse genome-wide estimate. The regulatory follow-up places a clear limit on the interpretation. Although CAD had recurrent Tier A SMR/HEIDI-prioritized genes and suggestive coloc signals for UBQLN4 and MEX3A in skin tissues, no CAD gene-tissue pair reached the prespecified PP4-supported threshold. Thus, the CAD result supports shared polygenic architecture, not a single shared cis-eQTL mediator. Several explanations remain compatible with the data: the covariance may be distributed across many variants with small effects; shared loci may act through disease-, cell-state- or stimulation-dependent regulatory effects absent from baseline GTEx tissues; or the relevant mediator may not be captured by the eQTL panels used here. The conservative claim is not that CAD lacks a shared regulatory mechanism with psoriasis. It is that this analysis did not identify a high-confidence shared CAD eQTL mediator after restricted coloc filtering.

The intestinal disease results require even more explicit handling because the direction of the genome-wide correlations differs from recent external literature. In our LDSC analysis, Crohn disease and ulcerative colitis showed significant negative genetic correlations with psoriasis, but both traits carried elevated heritability-intercept and cross-trait-intercept warnings. A 2026 harmonized population study reported positive genetic correlations of psoriasis with Crohn disease and ulcerative colitis [19], and older shared-locus work also supports genetic overlap between psoriasis and Crohn disease [10]. The discrepancy makes a simple directional statement inappropriate. The most defensible interpretation is that the current IBD results expose directional heterogeneity and quality-control sensitivity rather than a stable negative liability relationship. Restricted LAVA was informative in this respect: Crohn disease and ulcerative colitis contained both positive and negative local correlations, with negative local signals more prominent in the current analysis. That pattern is compatible with a genome in which different loci connect psoriasis and IBD through different immunological or regulatory directions. It is also compatible with residual differences in case definition, sample composition, allele harmonization, polygenicity and overlap correction. In practical terms, the IBD finding should be used to motivate locus-level follow-up and cross-source direction checks, not to rewrite the known clinical or genetic relationship between psoriasis and intestinal inflammation. For this reason, the IBD section should be framed around local directional heterogeneity and the need for adjudicated replication, not around a protective or globally inverse relationship.

The LDSC-to-LAVA-to-SMR/HEIDI-to-coloc sequence gives the genetic layer a useful hierarchy. LDSC defined the genome-wide liability relationship, LAVA localized where sharing was concentrated, SMR/HEIDI prioritized gene-level regulatory associations within frozen shared loci, and coloc asked whether the psoriasis and outcome signals were likely to share a causal variant in a relevant eQTL tissue. The 100% gene-level retention from SMR to SMR2 indicates prioritization stability under the recurrent SMR2 screen; it does not constitute causal replication. Among 91 frozen outcome-gene rows, 33 reached the highest SMR/HEIDI tier, but strong coloc support was restricted. PsA functioned as a positive-control near-neighbour phenotype with PP4-supported regulatory signals, and UC had PP4-supported RP11-973H7.1 signals under an eQTL MAF-proxy sensitivity setting. CAD and Crohn disease remained suggestive rather than PP4-supported in the restricted coloc table. The absence of direct overlap between these coloc-supported or suggestive genes and the frozen F1/F2/F6/F7 programs is also informative. It argues against a direct axis-to-coloc-gene narrative and supports a scale distinction: a coloc gene is a candidate inherited cis-regulatory perturbation at a locus, whereas a molecular program is an emergent multicellular tissue response. Disease-context and cell-type-resolved eQTL studies in IBD show that many regulatory effects are cell-type-specific or context-restricted and may be missed in bulk reference tissue maps [20]. This reinforces the need to interpret GTEx-based coloc as restricted regulatory prioritization rather than final mechanism assignment. Avoiding post hoc network or hub-gene expansion preserved that separation.

Several limitations define how far this model should be taken. First, the transcriptomic layer remains state- and sampling-dependent. The skin-primary programs were reproducible across bulk skin data and directionally supported by single-cell and spatial analyses, but the cellular and spatial evidence is contextual rather than definitive patient-level mechanistic validation. Treatment history, lesion age, body site, inflammation intensity and the availability of matched compartments can all influence the observed state. Second, the genetic layer is limited by summary-statistic availability, power and quality control. T2D, MASLD, MDD and uveitis were source-unresolved in the frozen primary panel at this stage and should not be interpreted as null outcomes. PsA is a near-neighbour phenotype with probable high shared liability and potential overlap-related inflation, while the Crohn disease and ulcerative colitis correlations require independent direction adjudication. Third, functional interpretation is constrained by reference eQTL context, MAF-proxy sensitivity in selected coloc analyses, and the fact that statistical sharing does not identify clinical mediation. Taken together, the results support a focused model for psoriasis comorbidity research: reproducible tissue molecular programs describe the inflammatory and repair states of psoriasis skin, whereas multisystem comorbidity is better investigated through overall psoriasis susceptibility and locus-level genetic architecture. This model does not reduce psoriasis to either transcriptomic state or inherited liability. It treats the two as connected but non-equivalent layers that can be integrated only after their evidential boundaries are kept separate."""


REFERENCES = """## References

1. Armstrong, A. W., Blauvelt, A., Callis Duffin, K. et al. Psoriasis. *Nature Reviews Disease Primers* 11, 45 (2025). doi:10.1038/s41572-025-00630-5.
2. Rider, A., Grantham, H. J., Smith, G. R. et al. Transcriptomic profiling and machine learning uncover gene signatures of psoriasis endotypes and disease severity. *Communications Medicine* 6, 65 (2026). doi:10.1038/s43856-025-01325-4.
3. Chen, C. H., Lee, M. S., Chang, W. Y. et al. Uncovering a dual T helper 17/type 2 transcriptomic endotype in psoriasis. *Journal of the American Academy of Dermatology* (2026). doi:10.1016/j.jaad.2026.06.131.
4. Shrotri, S., Daamen, A., Kingsmore, K. et al. Transcriptomic Analysis Identifies Disease Severity and Therapeutic Response in Psoriasis. *JID Innovations* 5, 100333 (2025). doi:10.1016/j.xjidi.2024.100333.
5. Ma, F., Plazyo, O., Billi, A. C. et al. Single cell and spatial sequencing define processes by which keratinocytes and fibroblasts amplify inflammatory responses in psoriasis. *Nature Communications* 14, 3455 (2023). doi:10.1038/s41467-023-39020-4.
6. Castillo, R. L., Sidhu, I., Dolgalev, I. et al. Spatial transcriptomics stratifies psoriatic disease severity by emergent cellular ecosystems. *Science Immunology* 8, eabq7991 (2023). doi:10.1126/sciimmunol.abq7991.
7. Dand, N. et al. GWAS meta-analysis of psoriasis identifies new susceptibility alleles impacting disease mechanisms and therapeutic targets. *Nature Communications* 16, 2051 (2025). doi:10.1038/s41467-025-56719-8.
8. Patrick, M. T. et al. Shared genetic risk factors and causal association between psoriasis and coronary artery disease. *Nature Communications* 13, 6565 (2022). doi:10.1038/s41467-022-34323-4.
9. Stuart, P. E. et al. Genome-wide association analysis of psoriatic arthritis and cutaneous psoriasis reveals differences in their genetic architecture. *American Journal of Human Genetics* 97, 816-836 (2015). doi:10.1016/j.ajhg.2015.10.019.
10. Ellinghaus, D. et al. Combined analysis of genome-wide association studies for Crohn disease and psoriasis identifies seven shared susceptibility loci. *American Journal of Human Genetics* 90, 636-647 (2012). doi:10.1016/j.ajhg.2012.02.020.
11. Li, W.-Q., Han, J. & Qureshi, A. A. Psoriasis, psoriatic arthritis and increased risk of incident Crohn's disease in US women. *Annals of the Rheumatic Diseases* 72, 1200-1205 (2013). doi:10.1136/annrheumdis-2012-202143.
12. Gelfand, J. M. et al. Risk of myocardial infarction in patients with psoriasis. *JAMA* 296, 1735-1741 (2006). doi:10.1001/jama.296.14.1735.
13. Werme, J., van der Sluis, S., Posthuma, D. & de Leeuw, C. A. An integrated framework for local genetic correlation analysis. *Nature Genetics* (2022). doi:10.1038/s41588-022-01017-y.
14. Zhu, Z. et al. Integration of summary data from GWAS and eQTL studies predicts complex trait gene targets. *Nature Genetics* (2016). doi:10.1038/ng.3538.
15. The GTEx Consortium. The GTEx Consortium atlas of genetic regulatory effects across human tissues. *Science* 369, 1318-1330 (2020). doi:10.1126/science.aaz1776.
16. Giambartolomei, C. et al. Bayesian test for colocalisation between pairs of genetic association studies using summary statistics. *PLoS Genetics* (2014). doi:10.1371/journal.pgen.1004383.
17. Jimenez-Gracia, B. et al. Interpretable inflammation landscape of circulating immune cells. *Nature Medicine* 32, 633-644 (2026). doi:10.1038/s41591-025-04126-3.
18. Li, X., Yan, Z., Lan, H. et al. Genetic comorbidity of psoriasis and four cardiovascular diseases: uncovering shared mechanisms and potential therapeutic targets. *Experimental Dermatology* 34, e70158 (2025). doi:10.1111/exd.70158.
19. Vestergaard, M. D. et al. Multimodal analysis disentangles the genetic and microbial associations between inflammatory bowel disease and other immune-mediated diseases across a harmonized population framework. *Nature Communications* 17, 1849 (2026). doi:10.1038/s41467-026-68564-4.
20. Alegbe, T. et al. Cell-type-resolved genetic variation shapes inflammatory bowel disease risk. *Nature* (2026). doi:10.1038/s41586-026-10627-z."""


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


def replace_discussion_and_references(text: str) -> str:
    text = re.sub(
        r"^## Discussion\n.*?(?=^## Methods\n)",
        DISCUSSION + "\n\n",
        text,
        flags=re.M | re.S,
    )
    text = re.sub(
        r"^## References\n.*\Z",
        REFERENCES + "\n",
        text,
        flags=re.M | re.S,
    )
    return text


def write_report(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    old = V1.read_text(encoding="utf-8")
    old_discussion = section_between(old, "## Discussion", "## Methods")
    new = replace_discussion_and_references(old)
    V3.write_text(new, encoding="utf-8")

    new_discussion = section_between(new, "## Discussion", "## Methods")
    old_words = count_words(old_discussion)
    new_words = count_words(new_discussion)
    new_paragraphs = count_paragraphs(new_discussion)

    write_report(
        REPORT_DIR / "CB_DISCUSSION_DEEP_REWRITE_REPORT.md",
        f"""# Communications Biology Discussion Deep Rewrite Report

## Output

- Source manuscript: `manuscript/Communications_Biology_main_manuscript_v1.md`
- Revised manuscript: `manuscript/Communications_Biology_main_manuscript_v3.md`
- Section changed: Discussion only
- References updated: yes, refs 17-20 added
- Methods/Results changed: no

## Length And Structure

| Version | Paragraphs | Approximate word count | Main issue |
| --- | ---: | ---: | --- |
| v1 Discussion | 8 | {old_words} | Sequential project recap; limited conceptual interpretation |
| v3 Discussion | {new_paragraphs} | {new_words} | Layered interpretation around tissue state versus inherited liability |

## Rewrite Goals Completed

| Requirement | Status | Note |
| --- | --- | --- |
| Build the Discussion around state versus liability | PASS | Opening and closing paragraphs explicitly define the layered model. |
| Avoid rescuing discrete k = 2 endotypes | PASS | k = 2 is interpreted as unstable in this design, without claiming endotypes cannot exist. |
| Preserve F1/F2/F6/F7 boundaries | PASS | F1/F2/F6 are tissue-state programs; F7 is systemic-supportive only. |
| Treat axis-specific genetics as NO-GO | PASS | Discussion states that comorbidity genetics should use overall psoriasis susceptibility. |
| CAD framed as cleanest non-neighbour systemic signal | PASS | CAD is interpreted as shared polygenic architecture with no PP4-supported mediator. |
| IBD negative rg handled cautiously | PASS | Discordance with external positive correlations is stated; interpretation centers on local directional heterogeneity. |
| SMR2/coloc wording controlled | PASS | SMR2 retention is prioritization stability, not causal replication. |
| No PPI/hub rescue | PASS | Discussion explicitly avoids post hoc network or hub-gene expansion. |

## Added Discussion References

| Ref | Role in Discussion |
| --- | --- |
| 17 | Conceptual context for immune-mediated inflammatory disease state landscapes. |
| 18 | Recent psoriasis-cardiovascular shared-genetics context. |
| 19 | External positive psoriasis-IBD genetic correlation used to audit discordance. |
| 20 | Disease-context and cell-type-resolved eQTL context for regulatory interpretation limits. |
""",
    )

    write_report(
        REPORT_DIR / "CB_DISCUSSION_CONTRADICTION_AUDIT.md",
        """# Communications Biology Discussion Contradiction Audit

## Purpose

This audit checks whether the revised Discussion acknowledges apparent contradictions without overstating the study's evidence.

| Topic | Current-study result | External literature or expectation | Concordance status | Allowed interpretation in v3 | Prohibited interpretation avoided |
| --- | --- | --- | --- | --- | --- |
| Endotypes | k = 2 clustering was not stable in matched multi-tissue data; continuous molecular programs were reproducible. | Recent transcriptomic studies report psoriasis endotype-like signatures and response/severity-related expression patterns. | Partly divergent framing. | This design does not support a stable binary patient partition; it supports continuous programs. | \"Psoriasis has no endotypes\" or \"previous endotype studies are wrong\". |
| CAD architecture and coloc | CAD showed positive genome-wide rg, QC PASS, and multiple positive local LAVA signals; no CAD PP4-supported eQTL mediator. | Prior studies support shared psoriasis-CAD genetic risk and cardiovascular comorbidity. | Concordant at genetic architecture level, unresolved at regulatory mediator level. | CAD is the cleanest non-neighbour shared-architecture signal; regulatory mediators remain suggestive. | \"CAD has no shared regulatory mechanism\" or \"UBQLN4/MEX3A are proven mediators\". |
| IBD direction | Crohn disease and ulcerative colitis showed negative global rg with QC warnings and mixed local directions. | A 2026 harmonized study reported positive psoriasis-Crohn and psoriasis-UC genetic correlations. | Explicitly discordant. | The safest interpretation is local directional heterogeneity plus need for independent direction adjudication. | \"IBD is genetically protective against psoriasis\" or \"the negative rg is settled\". |
| Regulatory genes versus transcriptomic programs | Coloc-supported/suggestive candidates did not directly overlap frozen F1/F2/F6/F7 programs. | Functional genetics often maps risk variants to regulatory targets, while transcriptomic states capture tissue responses. | Compatible if analyzed at different biological scales. | Coloc genes are candidate cis-regulatory perturbations; molecular programs are emergent multicellular states. | \"The coloc genes explain F1/F2/F6/F7\" or post hoc PPI/hub rescue. |

## Overall Decision

No unresolved contradiction remains in the revised Discussion. The main tension, psoriasis-IBD directionality, is kept as an explicit interpretation boundary rather than smoothed over.
""",
    )

    write_report(
        REPORT_DIR / "CB_DISCUSSION_CLAIM_AUDIT.md",
        """# Communications Biology Discussion Claim Audit

## Claim Classification Rules

- `DIRECT_RESULT`: directly observed in this project.
- `LITERATURE_SUPPORTED_INTERPRETATION`: supported by cited external literature.
- `REASONABLE_INFERENCE`: biologically plausible synthesis from direct results and literature.
- `SPECULATIVE`: plausible but not used as a main claim.
- `PROHIBITED`: unsupported or overclaimed; none should remain.

## Audited Claims

| Paragraph | Claim | Classification | Evidence basis | Status |
| --- | --- | --- | --- | --- |
| 1 | The study separates tissue molecular state from inherited comorbidity liability. | REASONABLE_INFERENCE | Phase 1B-4E results integrated across transcriptomics and genetics. | Retained with bounded language. |
| 1 | Immune-mediated disease atlases provide conceptual context for shared inflammatory states. | LITERATURE_SUPPORTED_INTERPRETATION | Jimenez-Gracia et al. 2026. | Stated as context only. |
| 2 | The unstable k = 2 result does not disprove all psoriasis endotypes. | REASONABLE_INFERENCE | Internal clustering stability plus comparison with transcriptomic endotype literature. | Retained to prevent contradiction. |
| 3 | F1/F2/F6 are reproducible tissue-state variables rather than independent inherited axes. | DIRECT_RESULT | Phase 2A-3A frozen program and genetics reports. | Retained. |
| 3 | F7 is systemic-supportive, not a pan-inflammatory skin-spatial axis. | DIRECT_RESULT | Internal blood support, GSE61281 support, weak/coarse skin-spatial localization. | Retained. |
| 4 | CAD is the cleanest non-neighbour systemic genetic signal. | DIRECT_RESULT | LDSC QC PASS, positive rg and LAVA local architecture. | Retained. |
| 4 | CAD lacks a high-confidence PP4-supported eQTL mediator in this analysis. | DIRECT_RESULT | Phase 4D restricted coloc. | Retained; avoids claiming absence of mechanism. |
| 5 | Crohn/UC negative rg should not be interpreted as settled inverse liability. | REASONABLE_INFERENCE | Internal QC flags and discordant external positive genetic correlations. | Retained. |
| 5 | IBD results are best framed as local directional heterogeneity. | DIRECT_RESULT | Restricted LAVA positive and negative local signals. | Retained. |
| 6 | SMR2 retention indicates prioritization stability, not causal replication. | DIRECT_RESULT | Phase 4C SMR/HEIDI workflow. | Retained. |
| 6 | Coloc genes and molecular programs operate at different biological scales. | REASONABLE_INFERENCE | Phase 4E no-overlap result plus eQTL context literature. | Retained. |
| 7 | T2D, MASLD, MDD and uveitis cannot be called null outcomes. | DIRECT_RESULT | Primary-source unresolved status in Phase 4A. | Retained. |

## Prohibited Claim Scan

| Prohibited claim type | Present in v3? | Note |
| --- | --- | --- |
| Discrete endotypes rescued | No | Continuous programs are the interpretation unit. |
| F1/F2/F6/F7 genetically anchored | No | All remain non-genetically anchored tissue/supportive programs. |
| CAD regulatory mediator proven | No | CAD coloc is suggestive only. |
| Crohn/UC protective or globally inverse conclusion | No | Directional heterogeneity and QC sensitivity are emphasized. |
| MR, causality or clinical validation overclaim | No | No MR or clinical validation claim is made. |
""",
    )

    reference_audit = REPORT_DIR / "CB_REFERENCE_AUDIT.md"
    addition = """\n\n## Discussion Deep-Rewrite Reference Update\n\n| Ref | Source | Verified role | Claim supported | Boundary |\n| --- | --- | --- | --- | --- |\n| 17 | Jimenez-Gracia et al., *Nature Medicine* 2026, doi:10.1038/s41591-025-04126-3 | Added to Discussion | Immune-mediated inflammatory diseases can be conceptualized through shared and disease-specific inflammatory state landscapes. | Used as conceptual context only; not validation of F1/F2/F6/F7. |\n| 18 | Li et al., *Experimental Dermatology* 2025, doi:10.1111/exd.70158 | Added to Discussion | Recent evidence supports psoriasis-cardiovascular shared genetic context. | Does not establish CAD regulatory mediation in this study. |\n| 19 | Vestergaard et al., *Nature Communications* 2026, doi:10.1038/s41467-026-68564-4 | Added to Discussion | External positive psoriasis-Crohn and psoriasis-UC genetic correlations contrast with current negative rg. | Used to frame discordance and QC adjudication, not to replace current results. |\n| 20 | Alegbe et al., *Nature* 2026, doi:10.1038/s41586-026-10627-z | Added to Discussion | Cell-type and disease-context eQTL effects can be missed by bulk reference tissue maps. | Used to limit GTEx-based coloc interpretation, not to assign mechanisms. |\n"""
    if reference_audit.exists():
        current = reference_audit.read_text(encoding="utf-8").rstrip()
        marker = "## Discussion Deep-Rewrite Reference Update"
        if marker in current:
            current = current.split(marker)[0].rstrip()
        reference_audit.write_text(current + addition, encoding="utf-8")
    else:
        reference_audit.write_text("# Communications Biology Reference Audit\n" + addition, encoding="utf-8")

    print(f"Wrote {V3.relative_to(ROOT)}")
    print(f"Discussion paragraphs: {new_paragraphs}")
    print(f"Discussion words: {new_words}")
    print("Reports written:")
    for name in [
        "CB_DISCUSSION_DEEP_REWRITE_REPORT.md",
        "CB_DISCUSSION_CONTRADICTION_AUDIT.md",
        "CB_DISCUSSION_CLAIM_AUDIT.md",
        "CB_REFERENCE_AUDIT.md",
    ]:
        print(f"- reports/{name}")


if __name__ == "__main__":
    main()
