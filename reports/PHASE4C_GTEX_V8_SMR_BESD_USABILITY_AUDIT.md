# Phase 4C GTEx v8 SMR/BESD usability audit

Date: 2026-08-15

## Executive answer

`/Volumes/EMPTY2TB/GTEx_v8_SMR/full_besd/` is usable, but it should be used for **SMR/HEIDI**, not as a direct replacement for formal coloc all-association eQTL summary statistics.

The directory contains GTEx v8 SMR-format full BESD packages. These are appropriate for:

- gene-level SMR testing;
- HEIDI heterogeneity filtering;
- eQTL-mediated shared-locus prioritization;
- tissue-stratified follow-up of the UKB-stable Phase 4B-R loci.

They are not directly sufficient for standard `coloc.abf` / SuSiE coloc unless we first extract or obtain full SNP-gene association statistics in coloc-compatible tabular form.

## File audit

Audit table:

- `results/phase4c_preparation/phase4c_gtex_v8_smr_besd_audit.tsv`

SMR runtime:

- Installed at `/Users/zy/.codex/tools/smr/smr`
- Version: SMR 1.4.2 MacOS
- Requires local library path:

```bash
DYLD_LIBRARY_PATH=/Users/zy/.codex/tools/smr/smr-1.4.2-macOS-arm64/libs
```

Overall BESD package status:

| Status | Count |
|---|---:|
| PASS, SMR-usable | 46 |
| BAD_ZIP | 2 |

Bad packages:

| Tissue | Phase 4C relevance | Status |
|---|---|---|
| Small_Intestine_Terminal_Ileum | intestinal | BAD_ZIP |
| Pituitary_Gland | non-priority | BAD_ZIP |

The macOS `._*.zip` files are metadata/resource-fork sidecars and should be ignored.

## Phase 4C-relevant tissues

Usable priority tissues:

| Tissue | Group | SMR usable | Phase 4C role |
|---|---|---|---|
| Skin_Sun_Exposed_Lower_leg | skin | yes | CAD/PsA/IBD + psoriasis tissue context |
| Skin_Not_Sun_Exposed_Suprapubic | skin | yes | CAD/PsA/IBD + psoriasis tissue context |
| Whole_Blood | blood | yes | systemic immune support |
| Artery_Coronary | vascular/arterial | yes | CAD primary target |
| Artery_Aorta | vascular/arterial | yes | CAD primary target |
| Artery_Tibial | vascular/arterial | yes | CAD sensitivity target |
| Colon_Sigmoid | intestinal | yes | Crohn/UC target |
| Colon_Transverse | intestinal | yes | Crohn/UC target |
| Spleen | immune | yes | PsA/IBD immune target |
| Cells_EBV-transformed_lymphocytes | immune cell model | yes | immune sensitivity |
| Cells_Cultured_fibroblasts | stromal cell model | yes | skin/stromal sensitivity |

Unavailable priority tissue:

| Tissue | Group | Problem |
|---|---|---|
| Small_Intestine_Terminal_Ileum | intestinal | zip is corrupted or incomplete |

## Format check

Each usable zip contains the standard SMR triplet:

- `.besd`
- `.epi`
- `.esi`

Example from `Whole_Blood.esi`:

```text
1 rs554008981 0 13550 A G NA
```

This means eQTL SNPs are keyed by rsID, chromosome, position, and alleles.

Example from `Whole_Blood.epi`:

```text
1 ENSG00000227232 0 14363 WASH7P -
```

This means probes/genes are keyed by Ensembl gene ID and gene symbol.

## What is already ready

Phase 4C candidate loci are frozen:

- `results/phase4c_preparation/phase4c_coloc_candidate_loci.tsv`

GWAS-side locus extracts are ready:

- `results/phase4c_preparation/gwas_loci/psoriasis_phase4c_locus_raw.tsv.gz`
- `results/phase4c_preparation/gwas_loci/cad_phase4c_locus_raw.tsv.gz`
- `results/phase4c_preparation/gwas_loci/psa_phase4c_locus_raw.tsv.gz`
- `results/phase4c_preparation/gwas_loci/crohn_phase4c_locus_raw.tsv.gz`
- `results/phase4c_preparation/gwas_loci/uc_phase4c_locus_raw.tsv.gz`

Sample sizes for SMR conversion:

| Trait | Cases | Controls | N |
|---|---:|---:|---:|
| Psoriasis | 36,466 | 458,078 | 494,544 |
| PsA | 5,065 | 21,286 | 26,351 |
| Crohn disease | 12,194 | 28,072 | 40,266 |
| UC | 12,366 | 33,609 | 45,975 |
| CAD | 122,733 | 424,528 | 547,261 |

LD reference found:

- `/Volumes/EMPTY2TB/New project 12/data/reference/ld/g1000_eur.bed`
- `/Volumes/EMPTY2TB/New project 12/data/reference/ld/g1000_eur.bim`
- `/Volumes/EMPTY2TB/New project 12/data/reference/ld/g1000_eur.fam`

This can likely be used for HEIDI, but it should be linked or copied into the project reference directory and documented before analysis.

## What is still missing

### Required for SMR/HEIDI

1. Extract the usable priority BESD zips.

   The relevant packages are large. Approximate uncompressed size for the 11 usable priority tissues is about 30 GB, which is acceptable because the external drive has about 1.5 TB free.

2. Convert GWAS locus or genome-wide summary statistics into SMR `.ma` format.

   Required fields:

   - SNP
   - A1
   - A2
   - freq
   - b
   - se
   - p
   - N

3. Add or map rsIDs for traits currently missing them.

   Current status:

   | Trait | beta/se/p | alleles | rsID | EAF |
   |---|---|---|---|---|
   | CAD | yes | yes | yes | yes |
   | PsA | yes | yes | yes | yes |
   | Psoriasis | yes | yes | missing | missing |
   | Crohn disease | yes | yes | missing | missing |
   | UC | yes | yes | missing | missing |

   Because GTEx BESD `.esi` uses rsIDs, psoriasis/Crohn/UC need chr:bp:allele to rsID mapping before SMR.

4. Confirm genome build compatibility.

   The Phase 4B/4C project uses GRCh37/hg19 loci. The GTEx v8 SMR BESD positions appear compatible with GRCh37-style coordinate usage, but this should be documented in the SMR manifest.

5. Define analysis scope.

   Recommended immediate scope:

   - CAD: skin, whole blood, artery coronary/aorta/tibial.
   - PsA: skin, whole blood, spleen, EBV lymphocytes.
   - Crohn/UC: skin, whole blood, colon sigmoid/transverse, spleen, EBV lymphocytes.
   - Small intestine terminal ileum should be excluded until re-downloaded.

### Required for formal coloc

The BESD packages do not replace full coloc-ready eQTL association matrices. Formal coloc still needs, for each gene-locus-tissue pair:

- eQTL beta;
- eQTL standard error;
- eQTL p value;
- effect allele and other allele;
- allele frequency or MAF;
- sample size;
- complete SNP coverage across the locus, not only top or significant associations.

If using standard `coloc.abf` or SuSiE coloc, we still need GTEx all-associations or an equivalent full eQTL summary-statistics source. The current BESD resource supports SMR/HEIDI first.

## Recommended next action

Proceed with:

`PHASE 4C-SMR0 — GTEx v8 BESD preparation + GWAS .ma conversion + rsID harmonization`

Do not run MR yet.

The immediate technical tasks are:

1. Create a project-local reference path or symlink for the 1000G EUR LD reference.
2. Extract only the 11 usable priority tissue BESD packages.
3. Build a chr:bp:allele to rsID mapping from `g1000_eur.bim` and GTEx `.esi`.
4. Convert psoriasis, CAD, PsA, Crohn, and UC GWAS to SMR `.ma`.
5. Run a small smoke test on one CAD Tier 1 locus in `Artery_Coronary` and `Whole_Blood`.

