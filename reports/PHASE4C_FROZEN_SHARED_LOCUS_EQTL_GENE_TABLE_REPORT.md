# Phase 4C Frozen Shared-Locus eQTL Gene Table Report

Date: 2026-08-15

## Decision

Phase 4C can proceed with a frozen shared-locus eQTL gene-prioritization table based on Phase 4B-R robust local loci and SMR2 probe-centered ±2Mb SMR/HEIDI results.

This table should be used as a candidate regulatory-gene layer, not as formal colocalization or causal mediation evidence.

## Frozen outputs

- Frozen gene table: `/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4c_smr/phase4c_frozen_shared_locus_eqtl_gene_table.tsv`
- Summary table: `/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4c_smr/phase4c_frozen_shared_locus_eqtl_gene_summary.tsv`
- Build script: `/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/src/genetics/phase4c_build_frozen_eqtl_gene_table.py`
- Script log: `/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/logs/phase4c_smr/phase4c_build_frozen_eqtl_gene_table.log`

## Inclusion rule

A gene entered the frozen table if it met all criteria:

1. The locus was selected for Phase 4C after Phase 4B-R LD-reference validation.
2. The locus was Tier 1 or Tier 2.
3. The gene had a primary SMR2 signal:
   - Global SMR FDR < 0.05.
   - HEIDI pass: `p_HEIDI > 0.01` or HEIDI not available.
4. The probe position mapped into the corresponding Phase 4C candidate locus.

The table is aggregated to one row per `outcome × locus × gene × probeID`. Tissue support, tissue class, top SMR result, HEIDI status and local-rg metadata are retained as columns.

## Evidence tiers

| Tier | Definition | Intended use |
|---|---|---|
| `A_local_Tier1_recurrent_SMR2` | Phase 4B-R Tier 1 locus and SMR2 support in at least 2 tissues | Main candidate gene table |
| `B_local_Tier1_single_tissue_SMR2` | Phase 4B-R Tier 1 locus and SMR2 support in 1 tissue | Supplementary or locus-specific discussion |
| `B_local_Tier2_recurrent_SMR2` | Phase 4B-R Tier 2 locus and SMR2 support in at least 2 tissues | Supplementary prioritized candidates |
| `C_local_Tier2_single_tissue_SMR2` | Phase 4B-R Tier 2 locus and SMR2 support in 1 tissue | Supplementary only |

## Overall table size

| Evidence tier | Gene-table rows |
|---|---:|
| `A_local_Tier1_recurrent_SMR2` | 33 |
| `B_local_Tier1_single_tissue_SMR2` | 44 |
| `B_local_Tier2_recurrent_SMR2` | 5 |
| `C_local_Tier2_single_tissue_SMR2` | 9 |

Total frozen rows: 91.

## Outcome-level summary

| Outcome | Role | Local direction | Locus tier | Loci with genes | Genes | Recurrent genes | Minimum SMR P | Minimum SMR FDR |
|---|---|---|---|---:|---:|---:|---:|---:|
| CAD | Primary systemic cardiovascular | Positive | Tier 1 | 4 | 15 | 8 | 7.35e-11 | 6.94e-09 |
| CAD | Primary systemic cardiovascular | Positive | Tier 2 | 3 | 11 | 4 | 3.51e-05 | 3.89e-04 |
| Crohn | IBD direction heterogeneity | Negative | Tier 1 | 4 | 15 | 5 | 2.05e-10 | 1.66e-08 |
| Crohn | IBD direction heterogeneity | Positive | Tier 1 | 4 | 6 | 2 | 2.91e-05 | 3.44e-04 |
| PsA | Positive control / near-neighbor | Positive | Tier 1 | 6 | 23 | 12 | 1.81e-14 | 5.11e-12 |
| UC | IBD direction heterogeneity | Negative | Tier 1 | 5 | 17 | 6 | 1.52e-11 | 2.15e-09 |
| UC | IBD direction heterogeneity | Positive | Tier 1 | 1 | 1 | 0 | 9.31e-03 | 4.47e-02 |
| UC | IBD direction heterogeneity | Positive | Tier 2 | 1 | 3 | 1 | 2.05e-04 | 1.82e-03 |

## Main candidate genes by outcome

### CAD

CAD remains the primary systemic cross-disease track. The strongest recurrent Tier A candidates are:

| Gene | Locus | Tissue count | Tissue classes | Minimum SMR P | Direction |
|---|---:|---:|---|---:|---|
| `SMARCA4` | 2318 | 2 | skin | 7.35e-11 | positive |
| `TMEM116` | 1841 | 4 | blood/immune; vascular | 7.39e-08 | negative |
| `MAPKAPK5` | 1841 | 3 | skin; vascular | 2.68e-05 | positive |
| `ADAM1B` | 1841 | 2 | skin; vascular | 6.01e-05 | negative |
| `RGL3` | 2318 | 2 | blood/immune; vascular | 3.25e-04 | positive |
| `MEX3A` | 113 | 2 | skin | 8.13e-04 | negative |
| `UBQLN4` | 113 | 2 | skin | 9.06e-04 | positive |
| `AC007381.3` | 267 | 2 | skin | 3.93e-03 | positive |

Single-tissue but strong CAD candidates include `ALDH2`, `YIPF2`, `C19orf52`, `MAPKAPK5-AS1`, `KANK2`, `CTC-510F12.2`, and `CDKN2D`.

Use in manuscript: CAD should anchor the main shared systemic genetic architecture narrative. Keep the wording to regulatory candidate genes within robust local-rg loci.

### PsA

PsA is retained as a positive-control / near-neighbor track. The recurrent Tier A candidates include:

`RP11-977G19.11`, `SLC22A5`, `C6orf3`, `TYK2`, `PDLIM4`, `ICAM5`, `RPS26`, `IFNLR1`, `MRPL4`, `SUOX`, `CDC42SE2`, and `C5orf56`.

Use in manuscript: show as method sanity and immune-neighbor support, not as the core evidence for multisystem comorbidity.

### Crohn

Crohn supports an IBD direction-heterogeneity track. Tier A recurrent candidates include:

`SLC22A5`, `CDC42SE2`, `PARK7`, `KIF3A`, `VAMP3`, `TCTEX1D1`, and `HSPA4`.

Crohn has both positive-local and negative-local loci. This supports a local-architecture interpretation rather than a single directional global conclusion.

### UC

UC also supports the IBD direction-heterogeneity track. Tier A recurrent candidates include:

`ORMDL3`, `GSDMB`, `GSDMA`, `SMARCE1`, `RP11-973H7.1`, and `TCTEX1D1`.

The 17q12/17q21 immune/regulatory region is prominent, but the result should be framed as locus-level prioritization within negative-local-rg architecture, not as causal proof.

## Manuscript-use rule

Recommended table placement:

- Main text: CAD Tier A genes, plus one compact PsA positive-control line and a compact IBD direction-heterogeneity line.
- Supplementary table: all 91 frozen rows.
- Supplementary sensitivity: SMR1 versus SMR2 stability comparison from `PHASE4C_SMR2_PROBE2MB_SENSITIVITY_REPORT.md`.

Recommended language:

> We prioritized candidate regulatory genes within robust psoriasis-comorbidity local genetic-sharing loci using GTEx v8 SMR/HEIDI. These analyses nominated tissue-supported eQTL-linked genes, but they do not establish formal colocalization or causal mediation.

## Remaining boundary before MR

MR should remain blocked until the Phase 4C locus/gene layer is finalized in the manuscript table. The current evidence supports candidate gene prioritization, not direction-of-effect causal inference.

Next recommended action:

`PHASE4C_MANUSCRIPT_TABLES_AND_FIGURE_PANEL`

This should produce:

1. Main CAD eQTL-prioritized gene table.
2. Supplementary all-outcome frozen gene table.
3. A compact figure panel linking global rg, local-rg tiers, and SMR2-prioritized genes.
