# Phase 4C Methods Text and Supplementary Table Captions

Date: 2026-08-16

## Status

This file provides manuscript-ready Methods text and table captions for Phase 4C. It follows the current project boundary:

- SMR/HEIDI is used for eQTL-linked candidate gene prioritization.
- The analysis is not formal Bayesian colocalization.
- The analysis is not Mendelian randomization of disease causality or mediation.
- Axis-specific transcriptomic factors are not used in the genetics main analysis.

## Draft Methods subsection

### Shared-locus eQTL gene prioritization

We prioritized candidate regulatory genes within psoriasis-comorbidity shared local genetic regions using GTEx v8 SMR/HEIDI. The input loci were restricted to Phase 4B-R local genetic-correlation loci that remained after LD-reference validation and were assigned Tier 1 or Tier 2 status. The Phase 4C outcomes were coronary artery disease (CAD), psoriatic arthritis (PsA), Crohn disease, and ulcerative colitis (UC). CAD was treated as the primary systemic outcome, PsA as a positive-control / near-neighbor outcome, and Crohn disease and UC as inflammatory bowel disease outcomes with local-direction heterogeneity.

GTEx v8 SMR-format BESD packages were audited before analysis. Usable priority tissues included sun-exposed skin, non-sun-exposed skin, whole blood, coronary artery, aorta, tibial artery, sigmoid colon, transverse colon, spleen, EBV-transformed lymphocytes, and cultured fibroblasts. Small intestine terminal ileum was excluded because the local GTEx BESD package was incomplete or corrupted. The GTEx BESD resources were used only for SMR/HEIDI-compatible eQTL prioritization and were not treated as complete coloc-ready eQTL association matrices.

GWAS summary statistics were converted to SMR `.ma` format with SNP ID, effect allele, other allele, allele frequency, effect estimate, standard error, P value, and sample size. Variants were harmonized to rsID where required using chromosome, position and allele information from the 1000 Genomes European LD reference. The project-local PLINK reference files were linked under the Phase 4C genetics reference directory and used for HEIDI LD calculations.

The first restricted SMR run used GWAS `.ma` files constructed from Phase 4C candidate LAVA loci. Because a probe's strongest cis-eQTL can fall outside a LAVA block, we then performed a stricter probe-centered sensitivity analysis. For this SMR2 run, each selected GTEx probe was expanded to a ±2 Mb cis window, overlapping windows were merged by trait, and GWAS summary statistics were rebuilt within the merged intervals. The SMR2 probe-window `.ma` files contained 174,979 CAD variants, 139,812 PsA variants, 170,443 Crohn disease variants, 146,455 UC variants, and 529,946 psoriasis variants after rsID and allele-frequency mapping.

SMR/HEIDI analyses were run with SMR version 1.03 through Rosetta (`arch -x86_64`) because the available macOS arm64 SMR 1.4.2 binary failed when reading the local GTEx v8 BESD files. For each outcome and tissue, SMR was run on the preselected probes from eligible Phase 4C loci. Primary SMR2 signals were defined as global SMR FDR < 0.05 with HEIDI pass, where HEIDI pass was defined as `p_HEIDI > 0.01` or unavailable HEIDI P value. Results were aggregated to one row per `outcome × locus × gene × probeID`.

Candidate genes were assigned evidence tiers using both the Phase 4B-R local-locus tier and tissue recurrence in SMR2. Tier A denoted Phase 4B-R Tier 1 loci with SMR2 support in at least two GTEx tissues. Tier B1 denoted Phase 4B-R Tier 1 loci with single-tissue SMR2 support. Tier B2 denoted Phase 4B-R Tier 2 loci with recurrent SMR2 support. Tier C denoted Phase 4B-R Tier 2 loci with single-tissue SMR2 support. The frozen Phase 4C gene table used SMR2 as the primary prioritization layer and retained SMR1 only as a sensitivity comparison.

The stability of the probe-centered SMR2 analysis was evaluated against the original restricted SMR1 run at two levels: `outcome + gene` and `outcome + tissue + gene`. Candidate retention was calculated as the intersection of primary SMR1 and SMR2 signals divided by the number of primary SMR1 signals. Genes or tissue-specific rows that were not retained after SMR2 were downgraded to sensitivity-only status and were not used as primary Phase 4C candidates.

## Table captions

### Main Table X. CAD Tier A shared-locus eQTL-prioritized candidate genes

This table lists CAD candidate regulatory genes that met Tier A Phase 4C criteria. Tier A required a Phase 4B-R Tier 1 positive local genetic-correlation locus and recurrent SMR2 support in at least two GTEx tissues. Columns report the local locus, genomic interval, candidate gene, local genetic-correlation direction, UKB-reference local genetic-correlation statistics, GTEx tissue support, minimum SMR P value, global SMR FDR, HEIDI P value, and SMR effect direction. These genes are eQTL-prioritized candidates within robust shared local loci and should not be interpreted as formally colocalized or causal genes.

Source table:

`/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4c_smr/manuscript_tables/phase4c_main_cad_tierA_gene_table.tsv`

### Supplementary Table X. Frozen Phase 4C shared-locus eQTL candidate table

This table contains all 91 frozen Phase 4C candidate rows. Each row represents one `outcome × locus × gene × probeID` combination retained after SMR2 prioritization. The table includes CAD, PsA, Crohn disease and UC; Phase 4B-R local-locus tier; local genetic-correlation direction; GTEx tissue support; top SMR result; HEIDI status; and final evidence tier. Tier A indicates recurrent SMR2 support in a Phase 4B-R Tier 1 locus, Tier B1 indicates single-tissue support in a Tier 1 locus, Tier B2 indicates recurrent support in a Tier 2 locus, and Tier C indicates single-tissue support in a Tier 2 locus.

Source table:

`/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4c_smr/manuscript_tables/phase4c_supplementary_all_frozen_gene_table.tsv`

### Supplementary Table X. PsA positive-control Tier A candidate genes

This table lists PsA Tier A candidate regulatory genes identified within positive local genetic-correlation loci. PsA was analyzed as a positive-control / near-neighbor phenotype because of its close clinical and genetic relationship to psoriasis. These results are intended to support pipeline behavior and shared immune-neighbor architecture, not to serve as the primary evidence for multisystem comorbidity.

Source table:

`/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4c_smr/manuscript_tables/phase4c_positive_control_psa_tierA_gene_table.tsv`

### Supplementary Table X. IBD direction-heterogeneity Tier A candidate genes

This table lists Tier A candidate genes for Crohn disease and UC, stratified by positive or negative local genetic-correlation direction. Crohn disease and UC are shown separately because their Phase 4B/4C results support local-direction heterogeneity rather than a single genome-wide direction. Candidate genes in this table are prioritized eQTL-linked genes within robust shared local loci and do not establish formal colocalization or causal mediation.

Source table:

`/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4c_smr/manuscript_tables/phase4c_ibd_direction_heterogeneity_tierA_gene_table.tsv`

### Supplementary Table X. Phase 4C manuscript gene-table counts

This table summarizes the number of candidate genes by outcome, analysis role and final Phase 4C evidence tier. It provides a compact audit trail for the distribution shown in Fig. Xa.

Source table:

`/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4c_smr/manuscript_tables/phase4c_manuscript_gene_table_counts.tsv`

## Figure legend compatibility note

The Phase 4C figure legend should define Tier A/B1/B2/C exactly as in the Methods. The legend should also repeat that SMR2 primary signals required global SMR FDR < 0.05 and HEIDI pass. This is important because the figure uses compact labels inside the panels rather than a full external legend.

Figure report:

`/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/reports/PHASE4C_MANUSCRIPT_FIGURE_PANEL_REPORT.md`

## Methods-to-results consistency check

| Item | Methods wording | Results wording | Status |
|---|---|---|---|
| Primary gene layer | SMR2 probe-centered ±2 Mb analysis | SMR2 used as primary Phase 4C gene layer | Consistent |
| Primary threshold | global SMR FDR < 0.05 and HEIDI pass | same | Consistent |
| HEIDI pass | `p_HEIDI > 0.01` or unavailable | same | Consistent |
| CAD role | primary systemic outcome | primary systemic track | Consistent |
| PsA role | positive-control / near-neighbor outcome | positive-control / near-neighbor track | Consistent |
| IBD role | local-direction heterogeneity | local-direction heterogeneity | Consistent |
| Boundary | eQTL prioritization, not coloc or mediation | same | Consistent |

## Chinese notes

这版 Methods 的重点是让审稿人能复现 Phase 4C，而不是解释生物学机制。关键写法有三点：

1. **先限定 eligible loci。** 只有 Phase 4B-R Tier 1/2 robust local loci 进入 Phase 4C。
2. **SMR2 是主分析。** SMR1 只是历史 restricted run 和敏感性比较。
3. **边界写在 Methods 和 caption 里。** SMR/HEIDI 不能被说成 coloc，也不能被说成 mediation。

## Next recommended action

`PHASE4C_DISCUSSION_PARAGRAPH_AND_LIMITATION_INTEGRATION`

下一步建议写 Discussion 中关于 CAD、PsA、IBD 和 SMR/coloc/MR 边界的解释段。仍然不要启动 MR。
