# Phase 4C preparation status

Date: 2026-08-14

## Current status

Phase 4C preparation has advanced as far as possible without a usable full eQTL summary-statistics source.

Completed:

- Phase 4B-R LD-reference validation with UKB LAVA v1.1 binary LD reference.
- Tier 1/2 coloc candidate locus freeze.
- Raw GWAS locus-level input extraction for psoriasis and all Phase 4C target outcomes.
- Lead variant extraction for each candidate locus and trait.
- Local R coloc runtime audit.
- eQTL source audit.

Blocked / waiting:

- Formal eQTL colocalization cannot start until full eQTL association statistics are available for relevant tissues.
- Direct access to tested GTEx v8 all-associations URLs returned HTTP 403.
- GTEx v8 significant eQTL tar is publicly reachable, but the download was paused because transfer speed was approximately 0.1 MB/s. This dataset can support candidate-gene annotation, but it is not sufficient for formal coloc because it contains significant pairs rather than all variants across each locus.

## Frozen Phase 4C candidate scope

Only Phase 4B-R Tier 1 and Tier 2 loci are eligible.

| Outcome | Tier 1 | Tier 2 | Eligible loci |
|---|---:|---:|---:|
| CAD | 5 | 7 | 12 |
| Crohn disease | 11 | 1 | 12 |
| PsA | 10 | 0 | 10 |
| Ulcerative colitis | 9 | 1 | 10 |
| Total | 35 | 9 | 44 |

Candidate files:

- `results/phase4c_preparation/phase4c_coloc_candidate_loci.tsv`
- `results/phase4c_preparation/phase4c_coloc_candidate_summary.tsv`

## GWAS inputs now ready

Raw GWAS locus files:

- `results/phase4c_preparation/gwas_loci/psoriasis_phase4c_locus_raw.tsv.gz`
- `results/phase4c_preparation/gwas_loci/cad_phase4c_locus_raw.tsv.gz`
- `results/phase4c_preparation/gwas_loci/psa_phase4c_locus_raw.tsv.gz`
- `results/phase4c_preparation/gwas_loci/crohn_phase4c_locus_raw.tsv.gz`
- `results/phase4c_preparation/gwas_loci/uc_phase4c_locus_raw.tsv.gz`

Manifest:

- `results/phase4c_preparation/phase4c_gwas_locus_input_manifest.tsv`

Lead variants:

- `results/phase4c_preparation/phase4c_gwas_locus_lead_variants.tsv`

Coverage:

| Trait | Candidate loci | Extracted rows | Loci with variants |
|---|---:|---:|---:|
| Psoriasis | 31 | 161,787 | 31 |
| CAD | 12 | 47,709 | 12 |
| PsA | 10 | 38,048 | 10 |
| Crohn disease | 12 | 44,401 | 12 |
| Ulcerative colitis | 10 | 40,209 | 10 |

## eQTL source audit

Audit file:

- `results/phase4c_preparation/phase4c_eqtl_source_audit.tsv`

Findings:

- `GTEx_v8_significant_eQTL`: public tar available, 1,562,828,800 bytes. Download was paused and can be resumed from `data/genetics/reference/gtex_v8_eqtl_significant/raw/GTEx_Analysis_v8_eQTL.tar.aria2`.
- `GTEx_v8_all_associations`: direct tested tissue URLs returned HTTP 403. Formal coloc requires these full association statistics or an equivalent full eQTL source.
- `R_coloc_runtime`: ready; `coloc`, `data.table`, and `susieR` are installed under R 4.4.3.

## Interpretation

The genetics pipeline is now in a clean handoff state:

- The local rg layer is UKB-reference checked.
- CAD is the primary systemic coloc target.
- PsA is a positive-control target.
- Crohn/UC are retained as direction-heterogeneity targets.
- GWAS-side coloc inputs are prepared.

The next operation is not another design change. It is obtaining full eQTL association data for the frozen tissues:

- CAD: skin, blood, vascular/arterial.
- PsA: skin, blood/immune.
- Crohn/UC: skin, blood, intestinal, immune.

Once full eQTL data are available, run:

`PHASE 4C — eQTL colocalization for UKB-stable Tier 1/2 loci`

Do not run MR before this step is complete.

