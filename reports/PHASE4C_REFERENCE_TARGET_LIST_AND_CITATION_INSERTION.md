# PHASE 4C Reference Target List and Citation Insertion

Date: 2026-08-16  
Project phase: Phase 4C shared-locus/eQTL prioritization  
Citation file: `literature/phase4c_reference_targets.bib`

## 1. Current purpose

This file freezes the first reference backbone for the Phase 4C manuscript text. The goal is not to create a full 50-reference bibliography yet. The goal is to attach verified citations to the major interpretive and methodological claims that now define the paper:

1. psoriasis has epidemiological and genetic links to coronary artery disease (CAD);
2. psoriasis, psoriatic arthritis (PsA), Crohn's disease and ulcerative colitis can share immune-genetic architecture, but the direction and locality of sharing need careful handling;
3. local genetic correlation, SMR/HEIDI and colocalization answer related but non-identical questions;
4. Phase 4C should describe SMR-supported eQTL gene prioritization, not causal mediation or formal colocalization.

## 2. One-sentence manuscript argument

In psoriasis comorbidity genetics, we show that reproducible tissue molecular heterogeneity does not translate into genetically anchored molecular axes, but overall psoriasis susceptibility shows shared genome-wide and local genetic architecture with selected comorbid systems, with CAD providing the cleanest systemic signal and IBD showing local directional heterogeneity.

## 3. Terminology ledger

| Canonical term | Use |
|---|---|
| overall psoriasis susceptibility | GWAS exposure after Phase 3A axis-specific genetics was stopped |
| genome-wide genetic correlation | LDSC-level global `rg` |
| local genetic correlation | LAVA locus-level `rho`/local `rg` |
| shared local locus | Phase 4B-R robust locus entering Phase 4C |
| SMR/HEIDI | summary-data eQTL prioritization and heterogeneity filtering |
| candidate regulatory gene | gene prioritized by SMR/HEIDI within a robust shared local locus |
| formal colocalization | Bayesian/fine-mapping based shared-causal-signal test; not completed in current Phase 4C |
| transcriptomic contextualization | final use of F1/F2/F6/F7; not a genetics main analysis |

## 4. Verified reference targets

| Citation key | Main use in manuscript | Identifier status | Notes |
|---|---|---|---|
| `Gelfand2006PsoriasisMI` | Epidemiological motivation for psoriasis-CAD/MI link | PMID 17032986; DOI 10.1001/jama.296.14.1735 | Population-based MI risk paper; use in Background/Discussion, not as genetic evidence |
| `Patrick2022PsoriasisCAD` | Prior genetic work linking psoriasis and CAD | PMID 36323703; DOI 10.1038/s41467-022-34323-4 | Strong anchor for CAD shared genetics and coloc-style prior work |
| `Dand2025PsoriasisGWAS` | Current large psoriasis GWAS context | PMID 40021644; DOI 10.1038/s41467-025-56719-8 | Use to justify modern psoriasis susceptibility map and scale |
| `Stuart2015PsAGWAS` | PsA as near-neighbor/positive-control genetic phenotype | PMID 26626624; DOI 10.1016/j.ajhg.2015.10.019 | Supports distinction between PsA and cutaneous psoriasis architecture |
| `Ellinghaus2012PsoriasisCrohn` | Shared psoriasis-Crohn susceptibility loci | PMID 22482804; DOI 10.1016/j.ajhg.2012.02.020 | Use for IBD shared-locus precedent |
| `Li2013PsoriasisPsACrohn` | Clinical/epidemiological psoriasis-PsA-Crohn association | PMID 22941766; DOI 10.1136/annrheumdis-2012-202143 | Use sparingly; not genetic evidence |
| `Werme2022LAVA` | Local genetic correlation method | PMID 35288712; DOI 10.1038/s41588-022-01017-y | Key citation for global-vs-local architecture and opposing local directions |
| `Zhu2016SMR` | SMR/HEIDI method | PMID 27019110; DOI 10.1038/ng.3538 | Use in Methods; do not describe as proof of causality |
| `GTEx2020Atlas` | GTEx v8 regulatory atlas | PMID 32913098; DOI 10.1126/science.aaz1776 | Use for GTEx tissue eQTL resource |
| `Giambartolomei2014Coloc` | Formal coloc concept and future Phase 4C extension | PMID 24830394; DOI 10.1371/journal.pgen.1004383 | Use when distinguishing SMR/HEIDI from coloc |

## 5. Citation insertion: Discussion draft

### Recommended long paragraph with citation keys

The Phase 4 genetic analyses reposition the study from axis-specific genetic anchoring to comorbidity-level shared architecture. This shift is supported by the negative Phase 3A result: F1/F2/F6/F7 remained useful as transcriptomic programs but did not provide stable genetically anchored axes for GWAS interpretation. In contrast, overall psoriasis susceptibility showed a cleaner systemic connection with CAD than with most other comorbidity outcomes. This is biologically and clinically plausible, because psoriasis has long been linked to myocardial infarction risk in population-based data, and recent genetic analyses have reported shared risk between psoriasis and CAD `[@Gelfand2006PsoriasisMI; @Patrick2022PsoriasisCAD]`. Our contribution is narrower than those prior studies: rather than claiming a causal cardiovascular pathway, we localize where genome-wide sharing is concentrated and then prioritize regulatory genes in robust shared local loci.

PsA and IBD require different interpretation. PsA is a useful near-neighbor positive control because its genetic architecture overlaps with cutaneous psoriasis while remaining distinguishable from it `[@Stuart2015PsAGWAS]`. Crohn's disease and ulcerative colitis should be framed as a directional-heterogeneity result rather than as a simple positive or negative global correlation. Previous work has identified shared susceptibility loci between psoriasis and Crohn's disease, and epidemiological data support links among psoriasis, PsA and Crohn's disease `[@Ellinghaus2012PsoriasisCrohn; @Li2013PsoriasisPsACrohn]`. The present LAVA results extend this literature by showing that local positive and negative signals can coexist across genomic regions. This interpretation follows the rationale of local genetic correlation analysis, where regional sharing may be missed or obscured by a single genome-wide estimate `[@Werme2022LAVA]`.

The Phase 4C gene-prioritization layer should also remain explicitly bounded. SMR/HEIDI integrates GWAS and eQTL summary statistics to prioritize genes whose genetically regulated expression is associated with a trait, while HEIDI screens for heterogeneity patterns consistent with linkage rather than a shared regulatory signal `[@Zhu2016SMR]`. Using GTEx v8 allowed us to evaluate relevant skin, blood, vascular and intestinal tissues across robust shared local loci `[@GTEx2020Atlas]`. These results are best described as candidate regulatory genes, not as proven mediators. Formal colocalization tests ask whether association signals are consistent with a shared causal variant and will be needed before promoting any locus to a causal regulatory mechanism `[@Giambartolomei2014Coloc]`.

### Shorter version for a tighter Discussion

Phase 4 shifts the manuscript from axis-specific genetic anchoring to comorbidity-level shared architecture. Overall psoriasis susceptibility showed the cleanest systemic signal with CAD, consistent with epidemiological MI-risk evidence and prior psoriasis-CAD genetic analyses `[@Gelfand2006PsoriasisMI; @Patrick2022PsoriasisCAD]`. PsA is best treated as a near-neighbor positive control, while Crohn's disease and ulcerative colitis support a local-direction heterogeneity model rather than a simple global-correlation claim `[@Stuart2015PsAGWAS; @Ellinghaus2012PsoriasisCrohn; @Werme2022LAVA]`. Phase 4C then uses GTEx v8 SMR/HEIDI to prioritize candidate regulatory genes within robust shared local loci, but these findings should not be described as formal colocalization or causal mediation without additional coloc/fine-mapping evidence `[@Zhu2016SMR; @GTEx2020Atlas; @Giambartolomei2014Coloc]`.

## 6. Citation insertion: Methods text

### SMR/HEIDI and GTEx resource sentence

For each Phase 4B-R robust shared local locus, we used summary-data-based Mendelian randomization (SMR) with HEIDI heterogeneity filtering to prioritize eQTL-linked genes whose genetically predicted expression showed evidence of association with the comorbidity GWAS signal `[@Zhu2016SMR]`. GTEx v8 tissue-level eQTL BESD files were used as the regulatory reference, focusing on disease-relevant tissues including skin, whole blood, vascular tissues and intestinal tissues where available `[@GTEx2020Atlas]`.

### Local genetic correlation sentence

Local genetic correlation was estimated using LAVA, which partitions genome-wide signal into predefined local regions and can identify region-specific sharing that is obscured in genome-wide genetic correlation estimates `[@Werme2022LAVA]`.

### Colocalization boundary sentence

Because SMR/HEIDI and formal colocalization test different assumptions, SMR-supported genes were interpreted as candidate regulatory genes rather than confirmed shared causal signals; Bayesian colocalization will be used in the next analysis layer to test whether GWAS and eQTL signals are consistent with a shared causal variant `[@Giambartolomei2014Coloc]`.

## 7. Claim-evidence map

| Manuscript claim | Recommended citation(s) | Claim strength |
|---|---|---|
| Psoriasis is linked to cardiovascular/MI risk | `Gelfand2006PsoriasisMI` | epidemiological association |
| Psoriasis and CAD share genetic risk | `Patrick2022PsoriasisCAD` | prior genetic evidence |
| Modern psoriasis GWAS has expanded susceptibility locus discovery | `Dand2025PsoriasisGWAS` | GWAS context |
| PsA can act as a psoriasis-neighbor positive control | `Stuart2015PsAGWAS` | genetic architecture support |
| Psoriasis and Crohn's disease have shared susceptibility loci | `Ellinghaus2012PsoriasisCrohn` | shared-locus precedent |
| Local signals may have directions that differ from global `rg` | `Werme2022LAVA` | method rationale |
| SMR/HEIDI prioritizes eQTL-linked genes but does not prove mediation | `Zhu2016SMR` | method boundary |
| GTEx v8 provides multi-tissue human regulatory reference data | `GTEx2020Atlas` | data resource |
| Formal coloc tests shared causal-variant consistency | `Giambartolomei2014Coloc` | method boundary |

## 8. Current citation status

`literature/phase4c_reference_targets.bib` now contains 10 verified entries. All entries have PMID and/or DOI identifiers. The only deliberate incompleteness is author expansion: several entries use `and others` and should be expanded automatically later if the manuscript is moved into a formal LaTeX/BibTeX build.

## 9. Next action

Proceed to `PHASE4C_FINAL_MINI_MANUSCRIPT_SECTION_PACK`: assemble the current Results, Methods, Discussion, figure callouts, table callouts and citation keys into one manuscript-ready mini-package. Do not start MR. Do not restart axis-specific genetics.
