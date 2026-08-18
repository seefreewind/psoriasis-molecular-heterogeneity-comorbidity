# Phase 4D Manuscript Results and Discussion Update

Date: 2026-08-16

## One-sentence argument

In psoriasis comorbidity genetics, we show that genome-wide and local shared genetic architecture does not uniformly translate into eQTL colocalization, using restricted Tier A GTEx v8 coloc across CAD, PsA, Crohn disease, and ulcerative colitis, with strong positive-control PsA signals and a UC colon-specific candidate but no PP4-supported CAD gene-tissue pair.

## Terminology ledger

| Canonical term | First-use definition | Use rule |
|---|---|---|
| psoriasis | psoriasis | Lowercase disease term unless starting a sentence |
| CAD | coronary artery disease (CAD) | Define once, then use CAD |
| PsA | psoriatic arthritis (PsA) | Define once, then use PsA |
| IBD | inflammatory bowel disease (IBD) | Use only when referring to Crohn disease and ulcerative colitis together |
| UC | ulcerative colitis (UC) | Define once, then use UC |
| LAVA | local analysis of variant association (LAVA) | Use for local genetic-correlation analysis |
| SMR | summary-data-based Mendelian randomization (SMR) | Use only for the expression-prioritization step, not causal MR claims |
| HEIDI | heterogeneity in dependent instruments (HEIDI) | Pair with SMR where relevant |
| coloc | Bayesian colocalization | Use `coloc` for the method and `colocalization` in prose |
| PP4 | posterior probability for a shared causal signal | Use as the main coloc evidence measure |
| PP3 | posterior probability for distinct causal signals | Use when PP3 > PP4 |
| GTEx v8 | Genotype-Tissue Expression version 8 | Use for eQTL source |
| eQTL MAF proxy | GTEx eQTL minor allele frequency used in place of missing GWAS EAF | Required label for Crohn disease and UC coloc runs |

## Placement in manuscript

Recommended placement:

| Manuscript section | Insert |
|---|---|
| Methods | Add the coloc methods paragraph after SMR/HEIDI or shared-locus prioritization methods |
| Results | Add a subsection after Phase 4C SMR/HEIDI results |
| Discussion | Add one paragraph on evidence hierarchy and one paragraph on disease-specific implications |
| Supplementary Information | Add captions for restricted coloc result tables and QC/sensitivity labels |

## Methods draft

### Restricted eQTL colocalization

To test whether prioritized shared loci were consistent with a shared eQTL-mediated causal signal, we performed a restricted Bayesian colocalization analysis on Tier A gene-tissue candidates selected from the LAVA and SMR/HEIDI layers. GTEx v8 eQTL summary statistics were accessed through eQTL Catalogue imported GTEx v8 remote tabix files. Local GTEx v8 SMR BESD files were retained for SMR/HEIDI analyses but were not used as direct coloc input because BESD is not a per-variant coloc-ready summary-statistic format.

The restricted coloc analysis included CAD as the primary systemic target, PsA as a near-neighbor positive control, and Crohn disease and UC as IBD direction-heterogeneity targets. CAD and PsA loci were matched to eQTL variants by rsID. For Crohn disease and UC, GWAS locus files were lifted from hg19 to hg38 and matched to eQTL variants by chromosome and position because rsID-level coloc matching was not available. Binary trait parameters were taken from the LAVA input metadata and used in coloc as case-control traits. For Crohn disease and UC, GWAS EAF was unavailable in the current locus files; these analyses used GTEx eQTL MAF as a proxy for variance specification and were labeled as MAF-proxy sensitivity analyses. We interpreted PP4 >= 0.80 as coloc-supported evidence for a shared causal signal, 0.50 <= PP4 < 0.80 as suggestive evidence, and PP3 > PP4 as evidence favoring distinct causal signals within the same locus.

## Results draft

### Restricted colocalization separated shared architecture from shared eQTL signals

We next asked whether the prioritized shared loci were supported by colocalization evidence consistent with the same causal variant influencing psoriasis, comorbidity risk, and local gene expression. The restricted Tier A coloc analysis tested 108 gene-tissue pairs across CAD, PsA, Crohn disease, and UC. PsA served as a positive-control phenotype, whereas CAD represented the primary non-neighbor systemic target and Crohn disease and UC represented the IBD direction-heterogeneity targets.

The PsA positive-control analysis recovered strong PP4-supported signals in immune-relevant tissues. SLC22A5 showed colocalization in spleen (PP4 = 0.971) and EBV-transformed lymphocytes (PP4 = 0.934), and RP11-977G19.11 showed colocalization in EBV-transformed lymphocytes (PP4 = 0.945). These results confirmed that the restricted coloc workflow could detect shared eQTL signals in a closely related psoriatic disease phenotype.

In CAD, no Tier A candidate reached the PP4 >= 0.80 coloc-supported threshold. The strongest CAD signals were suggestive skin eQTL coloc results at locus 113, including UBQLN4 in sun-exposed skin (PP4 = 0.754) and non-sun-exposed skin (PP4 = 0.746), and MEX3A in sun-exposed skin (PP4 = 0.597) and non-sun-exposed skin (PP4 = 0.595). The remaining CAD candidates were predominantly PP3-dominant. Thus, CAD retained evidence for shared genetic architecture and expression-prioritized loci from LAVA and SMR/HEIDI, but not strong eQTL-coloc support among the restricted Tier A candidates.

IBD showed disease-specific coloc patterns. Crohn disease did not produce PP4-supported Tier A signals; the strongest results were suggestive SLC22A5 in sigmoid colon (PP4 = 0.639) and PARK7 in whole blood (PP4 = 0.565). In contrast, UC produced a strong colon-specific signal for RP11-973H7.1 at locus 2251 in transverse colon (PP4 = 0.960) and sigmoid colon (PP4 = 0.960). Because Crohn disease and UC coloc analyses used eQTL MAF as a proxy for missing GWAS EAF, these IBD results were retained as sensitivity-labeled candidates pending EAF-complete reanalysis.

Across outcomes, coloc results showed that local genetic sharing and expression prioritization do not necessarily imply a single shared causal eQTL signal. CAD had the cleanest systemic architecture-level evidence but lacked strong coloc support, PsA recovered strong coloc evidence as expected for a near-neighbor positive control, and UC highlighted a colon-specific candidate within the IBD analysis. These findings support an evidence hierarchy in which LDSC/LAVA, SMR/HEIDI, and coloc address related but non-equivalent questions.

## Discussion draft

The restricted coloc analysis refined the interpretation of shared psoriasis-comorbidity genetics. The main implication is that genome-wide and local genetic correlation should not be collapsed into eQTL-mediated colocalization. CAD remained the strongest non-neighbor systemic target at the architecture level, but the absence of PP4-supported CAD gene-tissue pairs indicates that the current evidence does not identify a specific coloc-confirmed eQTL mechanism for CAD. This boundary is important because it preserves CAD as a robust shared-architecture signal while avoiding an unsupported mediation claim.

The positive-control PsA results provide an internal calibration point for the coloc workflow. Strong PP4-supported SLC22A5 and RP11-977G19.11 signals in immune-relevant tissues show that the analysis can recover shared eQTL evidence when a close psoriatic phenotype is tested. This makes the CAD null-coloc result more interpretable: it is less likely to reflect a global failure of the eQTL source or matching pipeline, and more likely to reflect either distinct causal variants, non-eQTL mechanisms, tissue contexts not captured by GTEx, or insufficient power within the restricted candidate set.

The IBD results support a local-architecture interpretation rather than a single genome-wide direction. Crohn disease showed only suggestive coloc results, whereas UC showed a strong colon-specific RP11-973H7.1 signal. This pattern is consistent with the earlier LAVA observation that psoriasis-IBD sharing can be locally heterogeneous. The UC signal is biologically tissue-concordant, but it should remain sensitivity-labeled because the current UC coloc file lacked GWAS EAF and used eQTL MAF as a proxy. An EAF-complete reanalysis should be treated as a required sensitivity step before promoting this candidate to the highest-confidence mechanistic table.

These findings also clarify the role of the transcriptomic axes in the final paper. F1, F2, F6, and F7 should remain transcriptomic-contextualization features rather than genetic exposures. The genetics layer now supports a revised manuscript spine: reproducible psoriasis tissue molecular heterogeneity, overall psoriasis susceptibility shared with selected comorbidity architectures, and a restricted eQTL-coloc layer that identifies where shared architecture does or does not converge on expression-linked causal signals.

## Supplementary table captions

### Supplementary Table X. Restricted Tier A coloc results

Restricted Bayesian colocalization results for Phase 4C Tier A gene-tissue candidates across CAD, PsA, Crohn disease, and UC. Columns include outcome, locus, gene, GTEx v8 tissue, variant matching counts, GWAS sample size, eQTL sample size, posterior probabilities PP0-PP4, interpretation tier, and MAF source. PP4 >= 0.80 was considered coloc-supported evidence for a shared causal signal, 0.50 <= PP4 < 0.80 was considered suggestive, and PP3 > PP4 was interpreted as evidence favoring distinct causal signals.

### Supplementary Table Y. Coloc input feasibility and harmonization audit

Input feasibility and harmonization audit for restricted Tier A coloc. The table records eQTL source availability, GTEx v8 tissue mapping, matching mode, genome-build handling, GWAS binary trait metadata, variant matching strategy, and MAF source. CAD and PsA were matched by rsID. Crohn disease and UC were lifted from hg19 to hg38 and matched by coordinate; these IBD analyses used eQTL MAF as a proxy because GWAS EAF was unavailable in the current locus files.

### Supplementary Table Z. Coloc-supported and suggestive gene-tissue candidates

Filtered coloc candidate table containing all PP4-supported and suggestive gene-tissue pairs. PsA positive-control signals included SLC22A5 in spleen and EBV-transformed lymphocytes and RP11-977G19.11 in EBV-transformed lymphocytes. UC showed colon-specific RP11-973H7.1 colocalization under the eQTL MAF-proxy sensitivity framework. CAD showed suggestive UBQLN4 and MEX3A skin eQTL signals but no PP4-supported Tier A candidate.

## Claim-evidence map

| Claim | Evidence | Status |
|---|---|---|
| PsA validates the coloc pipeline as a positive control | SLC22A5 PP4 = 0.971 in spleen; RP11-977G19.11 PP4 = 0.945 in EBV-transformed lymphocytes; SLC22A5 PP4 = 0.934 in EBV-transformed lymphocytes | Supported |
| CAD does not have a strong Tier A coloc-supported eQTL signal | CAD max PP4 = 0.754; no PP4 >= 0.80 among 19 CAD pairs | Supported |
| CAD should remain an architecture-level systemic target | Phase 4A/4B evidence plus Phase 4D lack of PP4 support | Supported, but requires cross-reference to Phase 4A/4B tables |
| UC has a strong colon-specific coloc candidate | RP11-973H7.1 PP4 = 0.960 in transverse colon and sigmoid colon | Supported under MAF-proxy sensitivity label |
| Crohn disease remains suggestive only in coloc | SLC22A5 PP4 = 0.639; PARK7 PP4 = 0.565; no PP4 >= 0.80 | Supported under MAF-proxy sensitivity label |
| Transcriptomic axes should not enter genetics main analyses | Phase 3A NO-GO and current Phase 4 design boundary | Supported by project decision |

## MR gate

Current decision:

```text
NO_GO_TO_UNRESTRICTED_MR
```

Rationale:

1. CAD, the primary systemic target, lacks PP4-supported eQTL-coloc evidence among restricted Tier A candidates.
2. UC has strong PP4-supported coloc only under an eQTL MAF-proxy sensitivity framework.
3. PsA is a positive control and should not drive the multisystem comorbidity claim.
4. Crohn disease is suggestive only.

Permissible future MR scope, if reopened:

```text
PP4-supported loci only
EAF-complete GWAS preferred
No axis-specific MR
No broad phenome-wide MR expansion
```

## 中文说明

这份更新的核心是把 Phase 4D 写成“证据分层”而不是“所有结果都服务于一个机制”。CAD 仍是正文的主要跨系统遗传架构结果，但不能写成 coloc 已确认的 eQTL 机制。PsA 的作用是正控制，证明流程能检出强信号。UC 的 RP11-973H7.1 是最值得保留的 IBD coloc 候选，但必须带上 eQTL MAF proxy 标签，后面如果能拿到 EAF 完整的 UC GWAS，应优先复核它。

