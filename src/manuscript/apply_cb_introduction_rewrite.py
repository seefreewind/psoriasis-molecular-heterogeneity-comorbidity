#!/usr/bin/env python3
"""Apply the Communications Biology Introduction rewrite.

This script performs no analysis. It replaces only the Introduction and
References sections of the current Markdown manuscript with the verified
Introduction rewrite produced on 2026-08-17.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT = ROOT / "manuscript" / "Communications_Biology_main_manuscript_v1.md"


INTRODUCTION = """## Introduction

Psoriasis is increasingly being resolved at two biological scales: molecular heterogeneity within affected tissue and inherited susceptibility shared across organ systems. Recent transcriptomic and spatial studies have begun to define molecular states within clinically similar disease [2-6], while large-scale genetic studies have mapped extensive sharing with inflammatory and cardiometabolic traits [1,7,8]. Yet these advances have largely proceeded in parallel. One map describes how lesional skin, clinically uninvolved skin and blood differ in transcriptional state. The other describes how inherited psoriasis liability covaries with psoriatic arthritis, cardiovascular disease and inflammatory bowel disease. These maps generate different biological expectations: tissue-state maps emphasize local inflammation, repair, cellular composition and disease activity, whereas genetic maps emphasize inherited covariance between disease liabilities. Whether these two maps coincide remains unclear. If they do, molecular states in skin could provide a tissue readout of systemic inherited risk. If they do not, psoriasis heterogeneity and comorbidity genetics must be interpreted as related but separable layers. Clinical and genetic comorbidity may reflect shared immune pathways, tissue-independent inherited susceptibility or downstream effects of chronic inflammation, but it does not establish that the molecular states observed within psoriatic tissue are themselves genetically encoded systemic disease states.

Molecular endotyping is an active frontier in psoriasis biology. Recent work in the PSORT cohort established a rich substrate for molecular stratification across skin and blood, identifying phenotype- and severity-associated gene modules, latent factors and predictive signatures in the same PSORT transcriptomic resource (E-MTAB-14509) used here [2]. Other transcriptomic studies have linked molecular profiles to disease severity and therapeutic response [4], while a recent Taiwanese study described a dual T helper 17/type 2 transcriptomic endotype with prominent IL-36 activation [3]. Single-cell and spatial studies have further shown that keratinocytes, fibroblasts and immune niches organize inflammatory signals across psoriatic tissue [5,6]. These studies establish that psoriasis contains substantial molecular heterogeneity. They do not, by themselves, determine the most appropriate mathematical representation of that heterogeneity. Disease states may vary continuously across tissue compartments, and unstable clustering can impose artificial boundaries on gradients of inflammation, remodeling or systemic immune activity. They leave open a narrower question: whether this heterogeneity forms reproducible discrete patient classes, whether continuous tissue programs provide a more stable representation, and whether either representation corresponds to inherited multisystem disease architecture.

Large-scale psoriasis genetics has also moved beyond locus discovery toward mapping cross-trait and systemic genetic architecture. A recent GWAS meta-analysis of 18 studies, including 36,466 cases and 458,078 controls, identified 109 distinct psoriasis susceptibility loci, connected psoriasis risk to immune regulation and therapeutic targets, and assessed genome-wide correlation with hundreds of disease and health-related traits [7]. Genetic studies have also separated aspects of psoriatic arthritis and cutaneous psoriasis architecture, identified shared psoriasis-Crohn disease loci, and reported shared genetic risk between psoriasis and coronary artery disease [8-10]. These analyses generally treat psoriasis as a single susceptibility phenotype. That design is powerful for mapping disease-level liability, but it does not reveal whether genetically shared comorbidity risk is concentrated in particular molecular states observed in skin or blood. Whether shared systemic genetic architecture is partitioned according to the molecular programs observed within psoriasis tissue remains unknown. This distinction is biologically important because tissue transcriptional states integrate inherited susceptibility with inflammation, cellular composition, environmental exposure, tissue injury and disease activity. Germline genetic correlation, by contrast, captures inherited covariance between disease liabilities. A reproducible tissue program therefore need not constitute an inherited genetic subtype, and systemic shared genetics need not map directly onto dominant transcriptional states in affected skin.

Here, we asked whether reproducible molecular heterogeneity in psoriasis tissue corresponds to distinct inherited architectures of systemic comorbidity. We integrated cross-tissue transcriptomics with independent bulk, single-cell and spatial validation, tested whether frozen molecular programs were independently anchored by psoriasis susceptibility genetics, and then characterized genome-wide and local comorbidity sharing with restricted regulatory prioritization. This design allowed us to test, rather than assume, whether tissue molecular heterogeneity and systemic inherited risk represent a common biological axis. By separating these questions, we sought to distinguish tissue-state molecular heterogeneity from inherited multisystem disease sharing in psoriasis.
"""


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
"""


def main() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    intro_start = text.index("## Introduction")
    results_start = text.index("## Results")
    text = text[:intro_start] + INTRODUCTION.rstrip() + "\n\n" + text[results_start:]
    refs_start = text.index("## References")
    text = text[:refs_start] + REFERENCES.rstrip() + "\n"
    MANUSCRIPT.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
