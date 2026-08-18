# Phase 4C Discussion Paragraph and Limitation Integration

Date: 2026-08-16

## Status

This file provides a manuscript-ready Discussion block for Phase 4C. It is written as a draft section segment, not a final literature-cited Discussion. Citation placeholders are retained because formal reference insertion should be performed after the manuscript narrative is fixed.

## Discussion draft

The shared-locus eQTL analysis adds a gene-prioritization layer to the psoriasis-comorbidity genetic architecture. Earlier phases established that psoriasis susceptibility showed cross-trait genetic sharing with selected comorbidities and that local genetic architecture was more informative than a single genome-wide summary for some outcomes. Phase 4C extends this by asking whether robust local loci can be linked to tissue-supported regulatory candidates. The resulting gene layer was most coherent for CAD, where recurrent Tier A candidates were detected across skin, blood/immune and vascular tissues. This pattern supports CAD as the strongest non-neighbor systemic track in the current study, while keeping the interpretation at the level of shared regulatory architecture rather than disease causality. [Citations needed: psoriasis cardiovascular comorbidity genetics; vascular inflammation and psoriasis]

The CAD results also help define the manuscript's main biological boundary. Several CAD-prioritized genes were supported in tissues outside the skin, including vascular and blood/immune contexts, whereas other candidates were skin-supported. This mixed tissue pattern is compatible with a model in which psoriasis-related inherited risk overlaps with cardiovascular pathways through multiple regulatory contexts. It does not establish that lesional skin molecular axes mediate cardiovascular disease, and it does not identify a single causal tissue. The stronger claim is that psoriasis-CAD genetic sharing can be resolved into local regions containing eQTL-linked genes with relevant tissue support. [Citations needed: GTEx/eQTL interpretation; local genetic correlation or shared-locus methods]

PsA behaved as an internal positive-control phenotype rather than as the central multisystem claim. This distinction is important because PsA is close to psoriasis clinically and genetically, and strong PsA sharing is expected. Retaining PsA as a near-neighbor control strengthens confidence that the shared-locus and SMR/HEIDI workflow can recover immune-adjacent signals. It should not be used as the main evidence that psoriasis has broad multisystem genetic architecture, because that argument depends on outcomes farther from the psoriasis disease spectrum.

The IBD results point to a different interpretation from CAD. Crohn disease and UC retained both positive and negative local genetic-correlation regions after eQTL prioritization. This argues against summarizing the psoriasis-IBD relationship as a single direction of genetic sharing. A more precise interpretation is that psoriasis and IBD share a heterogeneous local architecture, where some loci may align disease risk directions and others may oppose them or reflect different allelic effects across immune contexts. This local heterogeneity is especially important because the Phase 4A genome-wide IBD correlations raised direction and QC concerns; the Phase 4C results do not erase that caution, but they provide a structured way to interpret IBD loci by direction group. [Citations needed: psoriasis-IBD genetic overlap; local genetic heterogeneity]

The main limitation of Phase 4C is that SMR/HEIDI prioritizes eQTL-linked candidate genes but does not replace formal colocalization. HEIDI filtering reduces the chance that an SMR association is driven by strong heterogeneity across linked variants, but it does not provide posterior support for a shared causal variant. The local gene table should therefore be interpreted as a prioritized regulatory candidate layer for downstream analysis. Formal coloc or fine-mapping with full eQTL association matrices would be needed before claiming shared causal regulatory signals at individual gene-trait pairs.

Several technical constraints also limit interpretation. First, the GTEx v8 BESD resources were suitable for SMR/HEIDI but not directly sufficient for standard coloc workflows. Second, small intestine terminal ileum was excluded because the local BESD package was unusable, which limits intestinal tissue coverage for IBD. Third, SMR analyses were run with SMR 1.03 under Rosetta because the available macOS arm64 SMR 1.4.2 binary failed on the local GTEx BESD files. Fourth, the Phase 4C gene table was restricted to loci already selected by Phase 4B-R; this design prioritizes interpretability within robust shared local regions but does not constitute a genome-wide gene scan.

These boundaries define the next step. CAD Tier A genes provide the most defensible entry point for formal shared-locus follow-up, including coloc-ready eQTL extraction, fine-mapping and tissue-specific interpretation. PsA should remain a positive-control track. Crohn disease and UC should be analyzed by local direction group rather than pooled into a single IBD claim. Bidirectional MR should remain downstream of formal shared-locus resolution, because running MR before confirming shared causal signals would risk interpreting linkage or regulatory correlation as mediation.

## Shorter Discussion version

Phase 4C adds a candidate regulatory-gene layer to the psoriasis-comorbidity genetic architecture. CAD showed the clearest systemic pattern, with recurrent Tier A eQTL-prioritized genes in skin, blood/immune and vascular contexts. PsA behaved as a near-neighbor positive control, supporting the behavior of the pipeline without serving as the main multisystem claim. Crohn disease and UC retained both positive and negative local genetic-correlation regions, indicating that the psoriasis-IBD relationship is better described as local-direction heterogeneity than as a single genome-wide direction.

The interpretation remains bounded. SMR/HEIDI prioritized eQTL-linked candidate genes within robust shared local loci, but it did not establish formal colocalization, mediation or therapeutic directionality. Full coloc-ready eQTL association matrices, fine-mapping and tissue-specific follow-up are required before individual gene-trait pairs can be described as shared causal regulatory signals. Until that step is completed, CAD should anchor the systemic genetic architecture narrative, PsA should remain a positive-control analysis, and IBD should be presented as heterogeneous local architecture.

## Limitation bullets for final Discussion

- SMR/HEIDI provided eQTL-linked prioritization, not formal Bayesian colocalization.
- GTEx v8 BESD files were SMR-compatible but not directly coloc-ready.
- Small intestine terminal ileum was unavailable because the local BESD package failed audit.
- Phase 4C was restricted to Phase 4B-R robust local loci, not a genome-wide gene scan.
- SMR 1.03 under Rosetta was used because SMR 1.4.2 arm64 failed on the local GTEx BESD files.
- MR remains inappropriate until coloc/fine-mapping clarifies whether candidate genes and comorbidity outcomes share causal regulatory signals.

## Claim calibration

| Stronger wording to avoid | Use instead |
|---|---|
| `CAD genes mediate psoriasis cardiovascular risk` | `CAD shared loci contained eQTL-prioritized candidate regulatory genes` |
| `SMR confirmed colocalization` | `SMR/HEIDI prioritized candidate genes with heterogeneity filtering` |
| `IBD is negatively genetically correlated with psoriasis` | `IBD retained directionally heterogeneous local architecture` |
| `PsA proves multisystem comorbidity sharing` | `PsA served as a positive-control / near-neighbor phenotype` |
| `These genes are therapeutic targets` | `These genes are candidates for downstream shared-locus follow-up` |

## Citation placeholders to resolve later

The final Discussion should add citations for:

1. Psoriasis and cardiovascular comorbidity / CAD risk.
2. Psoriasis and PsA shared genetics.
3. Psoriasis and IBD shared immune-genetic architecture.
4. Local genetic correlation / LAVA-style interpretation.
5. SMR/HEIDI and the distinction from formal colocalization.
6. GTEx eQTL interpretation and tissue specificity.

## Next recommended action

`PHASE4C_REFERENCE_TARGET_LIST_AND_CITATION_INSERTION`

下一步建议先生成引用需求清单，再补文献。不要直接开始 MR。
