# Phase 4C-SMR2 Probe-Centered ±2Mb Sensitivity Report

Date: 2026-08-15

## Executive decision

The probe-centered ±2Mb sensitivity analysis supports proceeding with a frozen Phase 4C SMR/HEIDI gene-prioritization table.

Compared with the previous LAVA-locus-restricted GWAS input, the stricter probe-window run preserved all SMR1 primary candidate genes at the `outcome + Gene` level and retained 174 of 176 primary `outcome + tissue + Gene` signals. The two non-retained SMR1 primary tissue-level signals were CAD-specific borderline entries: `PCBP1-AS1` in aorta and `RP11-347I19.8` in coronary artery. No new primary signals were introduced by the broader probe-window input.

Interpretation: gene-level evidence is stable; two tissue-level CAD rows should be downgraded from primary to sensitivity-only.

## Analysis boundary

This analysis is an eQTL-mediated prioritization step using SMR/HEIDI with GTEx v8 BESD resources. It is not formal Bayesian colocalization and must not be described as causal mediation.

Current genetics boundary remains:

- Exposure context: psoriasis-shared comorbidity loci from Phase 4B/4B-R.
- SMR use: prioritize candidate genes within robust shared local-genetic regions.
- Do not run MR yet.
- Do not revive axis-specific genetics for F1/F2/F6/F7.
- Transcriptomic axes remain reserved for later contextualization.

## Inputs

### SMR runtime

- SMR binary: `/Users/zy/.codex/tools/smr_x86/smr`
- Invocation: `arch -x86_64 /Users/zy/.codex/tools/smr_x86/smr`
- Version: SMR 1.03
- Reason: official SMR 1.4.2 arm64 was installed but segfaulted when reading GTEx v8 BESD files; SMR 1.03 x86_64 worked under Rosetta.

### eQTL resources

- Source directory: `/Volumes/EMPTY2TB/GTEx_v8_SMR/full_besd/`
- Extracted usable priority tissues: `/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/data/genetics/reference/gtex_v8_smr_besd/extracted/`
- Excluded known bad priority tissue: `Small_Intestine_Terminal_Ileum.zip`
- LD reference: 1000G EUR symlinked under `/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/data/genetics/reference/ld/g1000_eur/`

### Probe-window GWAS `.ma` files

The sensitivity run rebuilt GWAS `.ma` files around each selected GTEx probe using merged probe-centered ±2Mb windows. This directly addresses the main limitation of SMR1, where the GWAS input was restricted to LAVA blocks and could miss a probe's top cis-eQTL when it lay outside the local-rg block.

| Trait | Merged intervals | Raw rows in windows | `.ma` rows | Rows with rsID | Rows with freq | Missing rsID rows |
|---|---:|---:|---:|---:|---:|---:|
| CAD | 12 | 174,979 | 174,979 | 174,979 | 174,979 | 0 |
| Crohn | 10 | 178,475 | 170,443 | 170,443 | 170,443 | 8,032 |
| PsA | 10 | 139,812 | 139,812 | 139,812 | 139,812 | 0 |
| Psoriasis | 28 | 602,522 | 529,946 | 529,946 | 529,946 | 72,576 |
| UC | 9 | 153,461 | 146,455 | 146,455 | 146,455 | 7,006 |

Manifest:

`/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4c_smr/gwas_ma_probe2mb/phase4c_smr2_probe2mb_gwas_ma_manifest.tsv`

## Batch status

All 25 outcome-by-tissue SMR/HEIDI jobs completed with `PASS`.

| Outcome | Tissue jobs | SMR result rows |
|---|---:|---:|
| CAD | 6 | 425 |
| Crohn | 7 | 218 |
| PsA | 5 | 318 |
| UC | 7 | 172 |

Run manifest:

`/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4c_smr/phase4c_smr2_probe2mb_run_manifest.tsv`

## SMR2 signal summary

Primary signal definition:

- Global SMR FDR < 0.05
- HEIDI pass: `p_HEIDI > 0.01` or HEIDI missing

| Outcome | Total SMR rows | Global-FDR rows | Global-FDR + HEIDI rows | Tissues | Minimum SMR P | Minimum global FDR |
|---|---:|---:|---:|---:|---:|---:|
| CAD | 425 | 52 | 44 | 6 | 7.35e-11 | 6.94e-09 |
| Crohn | 218 | 69 | 38 | 7 | 8.32e-19 | 9.42e-16 |
| PsA | 318 | 65 | 50 | 5 | 1.81e-14 | 5.11e-12 |
| UC | 172 | 60 | 42 | 7 | 3.55e-12 | 5.75e-10 |

Result tables:

- All results: `/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4c_smr/phase4c_smr2_probe2mb_all_results.tsv`
- Top results: `/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4c_smr/phase4c_smr2_probe2mb_top_results.tsv`
- Summary: `/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4c_smr/phase4c_smr2_probe2mb_summary.tsv`

## Stability versus SMR1

| Comparison unit | SMR1 primary | SMR2 primary | Intersection | SMR2 retention |
|---|---:|---:|---:|---:|
| `outcome + tissue + Gene` | 176 | 174 | 174 | 98.9% |
| `outcome + Gene` | 91 | 91 | 91 | 100.0% |

SMR1 primary rows not retained in SMR2:

| Outcome | Tissue | Gene |
|---|---|---|
| CAD | Artery_Aorta | PCBP1-AS1 |
| CAD | Artery_Coronary | RP11-347I19.8 |

No SMR2 primary rows were newly introduced relative to SMR1.

## Recurrent SMR2 candidates

The following recurrent genes are useful for the Phase 4C candidate table because they appear in multiple relevant tissues after the probe-window sensitivity run.

| Outcome | Recurrent genes and tissue counts |
|---|---|
| CAD | `TMEM116` (4), `MAPKAPK5` (3), `RNF114` (3), `GFPT1` (3), `PCBP1-AS1` (3), `SMARCA4` (2), `ADAM1B` (2), `RGL3` (2), `MEX3A` (2), `UBQLN4` (2), `ASPRV1` (2), `AC007381.3` (2) |
| Crohn | `PARK7` (5), `KIF3A` (4), `VAMP3` (4), `TCTEX1D1` (4), `HSPA4` (3), `SLC22A5` (2), `CDC42SE2` (2) |
| PsA | `RPS26` (5), `RP11-977G19.11` (4), `TYK2` (4), `ICAM5` (4), `SUOX` (4), `SLC22A5` (3), `C6orf3` (3), `PDLIM4` (3), `C5orf56` (3), `IFNLR1` (2), `MRPL4` (2), `CDC42SE2` (2) |
| UC | `SMARCE1` (6), `TCTEX1D1` (5), `GSDMB` (4), `GSDMA` (4), `RP11-973H7.1` (4), `ORMDL3` (3), `RP11-290F20.3` (2) |

## Outcome-level interpretation

### CAD

CAD remains the cleanest cross-system systemic target. SMR2 retained 26 CAD primary genes across 7 shared loci and 6 tissues. The strongest CAD signals include `SMARCA4`, `ALDH2`, `TMEM116`, and several recurrent multi-tissue candidates. The two tissue-level rows lost under SMR2 should be treated as sensitivity-only, but the CAD gene-level set remains stable.

Phase 4C priority: CAD should remain the primary shared-locus/eQTL interpretation track.

### PsA

PsA remains a positive-control / near-neighbor trait. The strong immune-region signals are expected and useful for method sanity checking, but they should not be used as the main evidence for multisystem comorbidity. Recurrent candidates include `RPS26`, `TYK2`, `SLC22A5`, `C6orf3`, and `IFNLR1`.

Phase 4C priority: keep PsA as a positive-control table, separated from the cross-system CAD narrative.

### Crohn and UC

Crohn and UC retain multiple SMR/HEIDI-supported candidates after the probe-window sensitivity run. This supports continuing the IBD track, but interpretation must stay tied to the earlier Phase 4B/4B-R direction-QC caution. The evidence is best framed as directionally heterogeneous local architecture with candidate regulatory genes, not as simple positive or negative global sharing.

Crohn recurrent candidates include `PARK7`, `KIF3A`, `VAMP3`, `TCTEX1D1`, `HSPA4`, and `SLC22A5`. UC recurrent candidates include the 17q12/17q21 region genes `ORMDL3`, `GSDMB`, `GSDMA`, plus `SMARCE1` and `TCTEX1D1`.

Phase 4C priority: split IBD loci by local direction group and present positive-local and negative-local candidates separately.

## Final adjudication

Status: `GO_TO_PHASE4C_FROZEN_SMR_GENE_TABLE`

Rules for the next step:

1. Use SMR2 as the primary SMR/HEIDI sensitivity-backed result table.
2. Keep SMR1 as the historical restricted-locus run and cite it only as an internal sensitivity comparison.
3. Freeze Tier 1/2 local loci that passed Phase 4B-R and have SMR2-supported candidate genes.
4. Downgrade the two non-retained CAD tissue rows to sensitivity-only.
5. Do not call SMR/HEIDI results colocalization.
6. Do not start MR until the Phase 4C shared-locus gene table is frozen.

Recommended immediate next deliverable:

`PHASE4C_FROZEN_SHARED_LOCUS_EQTL_GENE_TABLE`

This should merge:

- Phase 4B-R local-locus tiers and local direction groups.
- SMR2 candidate genes.
- Tissue class: skin, blood/immune, vascular, colon.
- HEIDI status.
- Recurrent-tissue support.
- Final evidence tier for manuscript tables.
