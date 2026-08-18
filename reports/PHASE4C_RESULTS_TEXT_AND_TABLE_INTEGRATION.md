# Phase 4C Results Text and Table Integration

Date: 2026-08-16

## Status

Phase 4C is ready to enter manuscript Results drafting.

The current evidence supports a shared-locus eQTL gene-prioritization layer for psoriasis-comorbidity genetic architecture. The strongest manuscript line remains CAD as the primary systemic track, PsA as a positive-control / near-neighbor track, and Crohn disease / ulcerative colitis as an IBD local-direction heterogeneity track.

This section must not describe SMR/HEIDI as formal colocalization or causal mediation.

## Terminology ledger

| Canonical term | First-use definition | Decision |
|---|---|---|
| psoriasis-comorbidity genetic architecture | Shared genetic architecture between psoriasis susceptibility and comorbidity outcomes | Use this for the broad Phase 4 frame |
| local genetic correlation | LAVA-based locus-level genetic correlation | Use `local genetic correlation` in prose; keep `local rg` for tables/figures |
| Phase 4B-R robust local loci | Loci retained after LD-reference validation | Use for loci eligible for Phase 4C |
| SMR/HEIDI | Summary-data-based Mendelian randomization with HEIDI heterogeneity filtering | Define once; do not call it colocalization |
| SMR2 | Probe-centered ±2 Mb SMR/HEIDI sensitivity analysis | Use as primary Phase 4C SMR layer |
| Tier A | Phase 4B-R Tier 1 locus with recurrent SMR2 support in at least two tissues | Main candidate gene tier |
| candidate regulatory genes | eQTL-linked genes prioritized within robust shared local loci | Use instead of causal genes |
| CAD | coronary artery disease | Primary systemic track |
| PsA | psoriatic arthritis | Positive-control / near-neighbor track |
| IBD | inflammatory bowel disease | Umbrella term for Crohn disease and ulcerative colitis |

## One-sentence argument

In robust psoriasis-comorbidity shared local genetic regions, GTEx v8 SMR/HEIDI prioritized a stable eQTL-linked regulatory-gene layer, highlighting CAD as the clearest systemic track while preserving PsA positive-control signals and IBD local-direction heterogeneity.

## Section outline

1. **Workflow opening:** State that Phase 4C moved from shared loci to candidate regulatory genes using GTEx v8 SMR/HEIDI.
2. **Frozen gene table:** Report the 91-row frozen table, evidence tiers and outcome-level distribution.
3. **CAD main track:** Lead with CAD Tier A recurrent genes and tissue support.
4. **PsA positive control:** Present PsA as near-neighbor support, not as the main multisystem claim.
5. **IBD direction heterogeneity:** Present Crohn disease and UC by positive/negative local genetic-correlation direction.
6. **SMR2 sensitivity:** Report that probe-centered ±2 Mb SMR2 retained all outcome-gene candidates and nearly all outcome-tissue-gene candidates.
7. **Boundary sentence:** State that this is eQTL-linked prioritization, not formal colocalization or causal mediation.

## Draft Results subsection

### Shared local genetic regions prioritized tissue-supported regulatory-gene candidates

We next asked whether robust psoriasis-comorbidity local genetic-sharing regions could be resolved into candidate regulatory genes. We restricted this analysis to Phase 4B-R loci that remained stable after LD-reference validation and applied GTEx v8 SMR/HEIDI using the probe-centered ±2 Mb SMR2 input. A gene was retained in the frozen Phase 4C table when it mapped to an eligible local locus, showed global SMR FDR < 0.05, and passed HEIDI filtering (`p_HEIDI > 0.01` or unavailable).

This procedure yielded 91 frozen `outcome × locus × gene × probe` rows, corresponding to 82 unique genes across 21 local loci (Fig. Xa; Supplementary Table X). The table separated candidates into four evidence tiers. Tier A contained 33 recurrent candidates from Phase 4B-R Tier 1 loci with SMR2 support in at least two GTEx tissues. The remaining rows comprised 44 Tier B1 single-tissue candidates from Tier 1 loci, 5 Tier B2 recurrent candidates from Tier 2 loci, and 9 Tier C single-tissue candidates from Tier 2 loci.

### CAD formed the primary systemic eQTL-prioritized track

CAD remained the clearest systemic track after eQTL-based gene prioritization. The CAD table contained 26 genes across 7 local loci, including 8 Tier A recurrent candidates from 4 Tier 1 positive local genetic-correlation loci (Fig. Xb; Table X). The strongest CAD Tier A signal was `SMARCA4` at locus 2318, supported in two skin tissues (minimum SMR `P = 7.35 × 10^-11`, global SMR FDR `= 6.94 × 10^-9`). CAD locus 1841 contributed multiple recurrent candidates, including `TMEM116` across blood/immune and vascular tissues, `MAPKAPK5` across skin and vascular tissues, and `ADAM1B` across skin and vascular tissues.

Additional CAD Tier A candidates included `RGL3`, `MEX3A`, `UBQLN4`, and `AC007381.3`. These genes did not all share the same tissue pattern: some were supported mainly in skin, whereas others involved vascular or blood/immune tissues. This tissue distribution is consistent with CAD being the strongest cross-system track in Phase 4C, while still requiring gene-level interpretation to remain locus-specific.

### PsA behaved as a positive-control near-neighbor phenotype

PsA provided the expected near-neighbor signal and was retained as a positive-control track. The PsA frozen table contained 23 genes across 6 positive local genetic-correlation loci, including 12 Tier A recurrent candidates. Recurrent PsA candidates included `RP11-977G19.11`, `SLC22A5`, `C6orf3`, `TYK2`, `PDLIM4`, `ICAM5`, `RPS26`, `IFNLR1`, `MRPL4`, `SUOX`, `CDC42SE2`, and `C5orf56`.

These results supported the internal behavior of the Phase 4C pipeline because PsA is genetically and clinically closer to psoriasis than the other systemic outcomes. For this reason, PsA should be interpreted as a positive-control / near-neighbor analysis rather than the main evidence for multisystem comorbidity.

### IBD loci retained directionally heterogeneous local architecture

Crohn disease and ulcerative colitis retained local-direction heterogeneity after SMR2 gene prioritization. Crohn disease contributed 21 genes across 8 loci. Of these, 15 genes mapped to 4 negative local genetic-correlation loci and 6 genes mapped to 4 positive local genetic-correlation loci (Fig. Xc). The recurrent Crohn disease candidates included `SLC22A5`, `CDC42SE2`, `PARK7`, `KIF3A`, `VAMP3`, `TCTEX1D1`, and `HSPA4`.

Ulcerative colitis also showed a mixed local architecture. The UC frozen table contained 21 genes across 7 loci, with 17 genes in 5 negative local genetic-correlation loci and 4 genes in 2 positive local genetic-correlation loci. Recurrent UC candidates included `ORMDL3`, `GSDMB`, `GSDMA`, `SMARCE1`, `RP11-973H7.1`, and `TCTEX1D1`. The concentration of UC candidates in negative local genetic-correlation regions supports the Phase 4B conclusion that the IBD signal should not be summarized as a single positive or negative genome-wide relationship.

### Probe-centered SMR2 sensitivity supported the frozen gene layer

The SMR2 sensitivity analysis addressed the main limitation of the original locus-restricted SMR run. Instead of restricting the GWAS input to LAVA blocks, SMR2 rebuilt GWAS summary-statistic inputs around each selected GTEx probe using merged probe-centered ±2 Mb windows. All 25 outcome-by-tissue SMR/HEIDI jobs completed successfully.

The probe-window analysis preserved the gene-level candidate set. SMR1 identified 91 primary `outcome + gene` candidates, and SMR2 retained all 91 (100.0% retention; Fig. Xd). At the `outcome + tissue + gene` level, SMR2 retained 174 of 176 SMR1 primary signals (98.9% retention). The two non-retained rows were CAD-specific tissue-level signals, `PCBP1-AS1` in aorta and `RP11-347I19.8` in coronary artery. No new SMR2 primary genes were introduced. These results support using SMR2 as the primary Phase 4C gene-prioritization layer.

Together, these analyses linked robust psoriasis-comorbidity local genetic-sharing regions to tissue-supported eQTL candidate genes. The results nominate candidate regulatory genes within shared local loci, but they do not establish formal colocalization, causal mediation, or therapeutic directionality.

## Main text table plan

### Table X. CAD Tier A shared-locus eQTL-prioritized candidate genes

Use the existing table:

`/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4c_smr/manuscript_tables/phase4c_main_cad_tierA_gene_table.tsv`

Recommended display columns:

| Column | Manuscript label |
|---|---|
| `locus` | Local locus |
| `chr`, `start`, `stop` | Genomic interval |
| `gene` | Candidate gene |
| `phase4br_tier` | Local-locus tier |
| `local_direction_group` | Local rg direction |
| `rho_ukb`, `p_ukb` | UKB-reference local rg and P |
| `n_tissues`, `tissues` | GTEx tissue support |
| `min_p_smr`, `min_smr_fdr_global` | SMR evidence |
| `min_p_heidi` | HEIDI minimum P |
| `b_smr_direction` | SMR direction |

Rows to show in main table:

| Gene | Locus | Tissue count | Tissue classes | Minimum SMR P | Global SMR FDR | Direction |
|---|---:|---:|---|---:|---:|---|
| `SMARCA4` | 2318 | 2 | skin | 7.35e-11 | 6.94e-09 | positive |
| `TMEM116` | 1841 | 4 | blood/immune; vascular | 7.39e-08 | 2.46e-06 | negative |
| `MAPKAPK5` | 1841 | 3 | skin; vascular | 2.68e-05 | 3.31e-04 | positive |
| `ADAM1B` | 1841 | 2 | skin; vascular | 6.01e-05 | 6.08e-04 | negative |
| `RGL3` | 2318 | 2 | blood/immune; vascular | 3.25e-04 | 2.71e-03 | positive |
| `MEX3A` | 113 | 2 | skin | 8.13e-04 | 5.68e-03 | negative |
| `UBQLN4` | 113 | 2 | skin | 9.06e-04 | 6.30e-03 | positive |
| `AC007381.3` | 267 | 2 | skin | 3.93e-03 | 2.12e-02 | positive |

### Supplementary Table X. All frozen Phase 4C shared-locus eQTL candidates

Use:

`/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4c_smr/manuscript_tables/phase4c_supplementary_all_frozen_gene_table.tsv`

This table should include all 91 frozen rows.

### Supplementary Table X. IBD direction-heterogeneity Tier A candidates

Use:

`/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4c_smr/manuscript_tables/phase4c_ibd_direction_heterogeneity_tierA_gene_table.tsv`

This table should keep Crohn disease and UC separated and retain local genetic-correlation direction.

### Supplementary Table X. PsA positive-control Tier A candidates

Use:

`/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4c_smr/manuscript_tables/phase4c_positive_control_psa_tierA_gene_table.tsv`

This table should be explicitly labeled as a positive-control / near-neighbor result.

## Figure integration

Figure file:

`/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/figures/phase4c/Figure_Phase4C_shared_locus_eqtl_prioritization.svg`

Recommended callout order:

1. Cite Fig. Xa in the frozen gene-table paragraph.
2. Cite Fig. Xb in the CAD paragraph.
3. Cite Fig. Xc in the IBD paragraph.
4. Cite Fig. Xd in the sensitivity paragraph.

Draft legend is available in:

`/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/reports/PHASE4C_MANUSCRIPT_FIGURE_PANEL_REPORT.md`

## Claim-evidence map

| Claim | Evidence | Status |
|---|---|---|
| Phase 4C generated a stable eQTL candidate-gene layer | 91 frozen rows, 82 unique genes, 21 loci; SMR2 primary definition and HEIDI filter | Supported |
| CAD is the primary systemic track | 26 CAD genes across 7 loci; 8 CAD Tier A recurrent candidates; CAD Tier A figure panel | Supported |
| PsA behaves as a near-neighbor positive control | 23 PsA genes across 6 positive local genetic-correlation loci; 12 Tier A recurrent candidates | Supported |
| Crohn disease and UC show local-direction heterogeneity | Crohn: 15 negative-local and 6 positive-local genes; UC: 17 negative-local and 4 positive-local genes | Supported |
| SMR2 sensitivity supports the gene layer | 91/91 outcome-gene retention and 174/176 outcome-tissue-gene retention | Supported |
| SMR/HEIDI proves causal mediation | Not supported by current design | Exclude from manuscript |
| Candidate genes are formally colocalized genes | Not supported by SMR/HEIDI alone | Exclude unless later coloc is completed |

## Assumptions or missing inputs

- Target journal is still unspecified. This draft uses a generic research-article Results style.
- Figure numbering is left as `Fig. X` and table numbering as `Table X`.
- The text assumes Phase 4C coloc has not yet been completed. If formal coloc is later run, this Results subsection should be updated rather than retrofitted.
- No references are inserted in this Results draft, consistent with the current manuscript rule that Methods and Results should primarily report analyses and observations.

## Chinese notes

这版 Results 的主线已经从“能不能找到共病遗传相关”推进到“稳健 shared local loci 能不能落到候选调控基因”。写作上保持三条边界：

1. **CAD 是正文主线。** CAD 是最清楚的非近邻 systemic signal，所以正文表只放 CAD Tier A。
2. **PsA 是 positive control。** PsA 信号强，但不拿它证明多系统共病。
3. **IBD 是方向异质性。** Crohn/UC 不能写成单纯正相关或负相关，要写 local architecture heterogeneous。

最重要的限制句已经放在最后：SMR/HEIDI 是候选基因优先级，不是 formal colocalization，也不是 causal mediation。

## Next recommended action

`PHASE4C_METHODS_TEXT_AND_SUPPLEMENTARY_TABLE_CAPTIONS`

下一步建议写 Methods 中的 Phase 4C 小节，并给主表/补充表写 caption。暂时仍不进入 MR。
