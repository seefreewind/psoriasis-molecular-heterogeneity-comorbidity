# Phase 4C-SMR1 restricted SMR/HEIDI report

Date: 2026-08-15

## Executive decision

GTEx v8 SMR/BESD data are usable for a restricted SMR/HEIDI evidence layer. The pipeline now runs end to end with:

- frozen Phase 4B-R Tier 1/2 LAVA loci;
- GTEx v8 BESD tissues;
- 1000G EUR LD reference;
- GWAS summary statistics converted to SMR `.ma`;
- SMR/HEIDI using SMR 1.03 under Rosetta.

This is a valid **eQTL-mediated shared-locus prioritization layer**, not a replacement for formal coloc. Formal coloc still requires full eQTL all-association summary statistics.

## Important runtime finding

SMR 1.4.2 macOS arm64 was installed and starts, but it segfaults when reading the extracted GTEx v8 BESD files.

The working runtime is:

- `/Users/zy/.codex/tools/smr_x86/smr`
- SMR version 1.03
- run through Rosetta with `arch -x86_64`

This runtime successfully read `.epi`, `.esi`, `.besd`, GWAS `.ma`, and 1000G EUR PLINK LD files.

## Prepared resources

Resource manifest:

- `results/phase4c_smr/phase4c_smr0_resource_manifest.tsv`

Extracted GTEx v8 BESD tissues:

- `data/genetics/reference/gtex_v8_smr_besd/extracted/`

Usable priority tissues:

- Skin_Sun_Exposed_Lower_leg
- Skin_Not_Sun_Exposed_Suprapubic
- Whole_Blood
- Artery_Coronary
- Artery_Aorta
- Artery_Tibial
- Colon_Sigmoid
- Colon_Transverse
- Spleen
- Cells_EBV-transformed_lymphocytes
- Cells_Cultured_fibroblasts

Excluded tissue:

- Small_Intestine_Terminal_Ileum: BAD_ZIP / incomplete package.

Project-local LD reference symlinks:

- `data/genetics/reference/ld/g1000_eur/g1000_eur.bed`
- `data/genetics/reference/ld/g1000_eur/g1000_eur.bim`
- `data/genetics/reference/ld/g1000_eur/g1000_eur.fam`

LD read smoke test:

- PASS
- 146,297 candidate rsIDs matched the 1000G EUR reference.

## GWAS `.ma` conversion

GWAS `.ma` manifest:

- `results/phase4c_smr/gwas_ma/phase4c_smr0_gwas_ma_manifest.tsv`

Converted `.ma` files:

- `results/phase4c_smr/gwas_ma/psoriasis.phase4c_loci.ma`
- `results/phase4c_smr/gwas_ma/cad.phase4c_loci.ma`
- `results/phase4c_smr/gwas_ma/psa.phase4c_loci.ma`
- `results/phase4c_smr/gwas_ma/crohn.phase4c_loci.ma`
- `results/phase4c_smr/gwas_ma/uc.phase4c_loci.ma`

Conversion summary:

| Trait | Input rows | `.ma` rows | Rows with rsID | Rows with frequency | Missing rsID rows |
|---|---:|---:|---:|---:|---:|
| CAD | 47,709 | 47,709 | 47,709 | 47,709 | 0 |
| Crohn disease | 44,401 | 42,383 | 42,383 | 42,383 | 2,018 |
| PsA | 38,048 | 38,048 | 38,048 | 38,048 | 0 |
| Psoriasis | 161,787 | 142,515 | 142,515 | 142,515 | 19,272 |
| UC | 40,209 | 38,322 | 38,322 | 38,322 | 1,887 |

Interpretation:

- CAD and PsA are fully mapped.
- Crohn/UC are well mapped.
- Psoriasis has lower rsID recovery because the source GWAS lacks rsIDs, but the mapped set is large enough for restricted locus-level SMR.

## SMR/HEIDI smoke test

CAD Tier 1 × Artery_Coronary smoke test:

- Probe list: 195 probes.
- SMR ran successfully.
- 5 probes had cis-eQTL evidence at `p_eQTL < 5e-8`.
- Output: `results/phase4c_smr/smoke/cad_tier1_artery_coronary_smr103.smr`

Smoke-test signal examples:

| Gene | Locus | Tissue | P_SMR | P_HEIDI | Interpretation |
|---|---:|---|---:|---:|---|
| TMEM116 | 1841 | Artery_Coronary | 2.21e-05 | 0.055 | pipeline-validating CAD arterial candidate |
| MAPKAPK5 | 1841 | Artery_Coronary | 1.34e-02 | 0.916 | weaker SMR, HEIDI-consistent |

These are smoke-test results and should not be treated as final gene claims without the full restricted summary below.

## Restricted SMR/HEIDI batch run

Probe-list manifest:

- `results/phase4c_smr/phase4c_smr1_probe_list_manifest.tsv`

Run manifest:

- `results/phase4c_smr/phase4c_smr1_run_manifest.tsv`

All result table:

- `results/phase4c_smr/phase4c_smr1_all_results.tsv`

Top result table:

- `results/phase4c_smr/phase4c_smr1_top_results.tsv`

Outcome × tissue summary:

- `results/phase4c_smr/phase4c_smr1_summary.tsv`

All 25 outcome × tissue combinations completed with PASS status.

| Outcome | SMR result rows | Global FDR + HEIDI primary rows | Unique primary genes |
|---|---:|---:|---:|
| CAD | 421 | 46 | 26 |
| PsA | 312 | 50 | 23 |
| Crohn disease | 209 | 38 | 21 |
| UC | 167 | 42 | 21 |
| Total | 1,109 | 176 | NA |

Primary signal definition:

- `smr_fdr_global < 0.05`
- and `p_HEIDI > 0.01` or HEIDI not available.

## Main result patterns

### CAD

CAD shows a coherent positive local-rg SMR layer, consistent with its Phase 4A/4B role as the cleanest non-neighbor systemic signal.

Top recurrent candidates include:

- SMARCA4 at locus 2318.
- ALDH2 at locus 1841.
- TMEM116 at locus 1841 across artery and blood tissues.
- MAPKAPK5 / MAPKAPK5-AS1 at locus 1841.
- RNF114 at Tier 2 locus 2412.

CAD signals are strongest in skin and vascular/blood tissues. This supports using CAD as the primary systemic Phase 4C target.

### PsA

PsA behaves as a positive-control phenotype, with strong immune and skin SMR signals.

Top candidates include:

- SLC22A5 at locus 887.
- TYK2 at locus 2318.
- C6orf3 at locus 1041.
- RPS26 and RP11-977G19.11 at locus 1793.

This supports the positive-control role of PsA, but it should not be used as the main multisystem comorbidity claim.

### Crohn disease

Crohn disease preserves local direction heterogeneity.

Primary SMR signals occur in both:

- negative local-rg loci, including PDLIM4, SLC22A5, IL12RB2, RP11-973H7.1;
- positive local-rg loci, including PARK7, KSR1, UBLCP1, TIMD4, VAMP3.

This supports the earlier interpretation that Crohn should not be summarized as uniformly negative. The stronger story is mixed local architecture.

### Ulcerative colitis

UC is dominated by the negative local-rg locus 2203, with strong immune/blood/intestinal signals.

Top candidates include:

- ORMDL3.
- GSDMB.
- GSDMA.
- IKZF3.
- SMARCE1.
- PGAP3.

This is a biologically coherent IBD-local signal and should be treated as a shared-locus/eQTL-mediated candidate layer, not causal proof.

## Critical limitation

This run is **restricted locus-level SMR**, because the GWAS `.ma` files were built from Phase 4C candidate LAVA loci.

This is appropriate for:

- prioritizing genes inside UKB-stable LAVA loci;
- checking whether local genetic sharing has eQTL-mediated candidate genes;
- generating a Phase 4C candidate table.

It is not yet equivalent to a full SMR scan, because a probe's strongest cis-eQTL can lie outside the LAVA block. A stricter next analysis would rebuild GWAS `.ma` files using either:

1. full genome-wide GWAS summary statistics; or
2. probe-centered cis windows, for example probe ±2 Mb across all selected tissues.

This would increase coverage and reduce edge effects.

## Current GO decision

GO for manuscript-level Phase 4C candidate-gene prioritization, with controlled claim strength.

Do not claim:

- causal mediation;
- definitive colocalization;
- therapeutic target validation;
- axis-specific genetic mechanism.

Allowed claim:

> UKB-reference-stable local genetic sharing can be prioritized to candidate eQTL-linked genes in disease-relevant GTEx tissues using restricted SMR/HEIDI.

## Recommended next step

The next decision requires method-boundary input:

Option A:

- Accept restricted SMR/HEIDI as a Phase 4C gene-prioritization layer.
- Move to manuscript figure/table construction and cautious interpretation.

Option B:

- Build expanded probe-centered cis-window GWAS `.ma` files.
- Re-run SMR/HEIDI as a stricter sensitivity analysis.
- This is computationally larger and will supersede some restricted results.

Do not start MR until this Phase 4C boundary is settled.

