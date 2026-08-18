# PHASE 4D Colocalization Input Audit and Smoke Test

Date: 2026-08-16  
Status: `GO_TO_RESTRICTED_TIER_A_COLOC`  
Scope: input feasibility for formal coloc after Phase 4C SMR/HEIDI gene prioritization

## 1. Executive conclusion

Phase 4D should not use the local GTEx v8 SMR BESD files as coloc input. Those files remain suitable for SMR/HEIDI but are not standard per-variant eQTL association matrices.

The original GTEx Portal all-associations route is still blocked for this project: tested direct `storage.googleapis.com/gtex-resources/GTEx_Analysis_v8_eQTL_all_associations/*.v8.allpairs.txt.gz` URLs returned HTTP 403. The locally downloaded `GTEx_Analysis_v8_eQTL.tar` is not sufficient for coloc because it contains only two Adipose Subcutaneous significant-eQTL files and does not contain full all-variant association statistics for priority tissues.

However, eQTL Catalogue provides a usable alternative route. Its imported GTEx v8 tabix-indexed files are accessible for the required tissues and contain per-variant fields needed for coloc extraction: variant ID, P value, beta, SE, allele frequency, allele count, allele number, chromosome, position, REF, ALT and rsID. A CAD Tier A smoke test for `SMARCA4` in sun-exposed skin completed successfully after matching GWAS and eQTL variants by rsID.

Therefore:

> Phase 4D can proceed as a restricted coloc analysis through eQTL Catalogue imported GTEx v8 remote tabix files. Binary GWAS sample size and case fraction have now been recovered from Phase 4B LAVA metadata for psoriasis, CAD, PsA, Crohn disease and UC.

## 2. Files generated

Scripts:

- `src/genetics/phase4d_coloc_input_feasibility_audit.py`
- `src/genetics/phase4d_coloc_smoke_test.R`

Audit outputs:

- `results/phase4d_coloc/phase4d_coloc_input_feasibility_by_candidate_tissue.tsv`
- `results/phase4d_coloc/phase4d_coloc_input_feasibility_summary.tsv`
- `results/phase4d_coloc/phase4d_gtex_significant_tar_status.tsv`
- `results/phase4d_coloc/phase4d_prior_eqtl_source_audit_snapshot.tsv`
- `results/phase4d_coloc/phase4d_coloc_candidate_loci_snapshot.tsv`
- `results/phase4d_coloc/tabix_ftp_paths_imported.tsv`
- `results/phase4d_coloc/tabix_ftp_paths.tsv`
- `results/phase4d_coloc/phase4d_gwas_binary_trait_metadata.tsv`

Smoke-test outputs:

- `results/phase4d_coloc/phase4d_coloc_smoke_test_results.tsv`
- `results/phase4d_coloc/phase4d_smoke_cad_SMARCA4_Skin_Sun_Exposed_Lower_leg_merged.tsv`

## 3. Local GTEx resource audit

| Resource | Status | Interpretation |
|---|---|---|
| `/Volumes/EMPTY2TB/GTEx_v8_SMR/full_besd` | present, approximately 46G | SMR/HEIDI-compatible BESD packages; not direct coloc input |
| priority GTEx BESD tissues | mostly PASS | Skin, blood, artery, colon, spleen, EBV lymphocytes and fibroblasts are SMR-usable |
| Small Intestine Terminal Ileum BESD | BAD_ZIP | excluded from Phase 4C/4D intestinal tissue coverage |
| `GTEx_Analysis_v8_eQTL.tar` | present, 1.56G, 2 tar members | significant-only and incomplete for this coloc task |
| GTEx Portal all-associations direct URL | HTTP 403 for tested tissues | not usable without another access route |
| eQTL Catalogue imported GTEx v8 tabix | accessible | feasible coloc input route |

The `phase4d_gtex_significant_tar_status.tsv` audit reports that the current tar contains only:

- `GTEx_Analysis_v8_eQTL/Adipose_Subcutaneous.v8.egenes.txt.gz`
- `GTEx_Analysis_v8_eQTL/Adipose_Subcutaneous.v8.signif_variant_gene_pairs.txt.gz`

This is not a usable input for Phase 4D restricted coloc.

## 4. eQTL Catalogue route

Downloaded path tables:

- imported GTEx v8: `results/phase4d_coloc/tabix_ftp_paths_imported.tsv`
- uniformly processed eQTL Catalogue datasets: `results/phase4d_coloc/tabix_ftp_paths.tsv`

The imported GTEx v8 table contains 49 tissue/context rows, including Phase 4D priority tissues:

- `Skin_Sun_Exposed_Lower_leg`
- `Skin_Not_Sun_Exposed_Suprapubic`
- `Whole_Blood`
- `Artery_Aorta`
- `Artery_Coronary`
- `Artery_Tibial`
- `Colon_Sigmoid`
- `Colon_Transverse`
- `Spleen`
- `Cells_EBV-transformed_lymphocytes`
- `Cells_Cultured_fibroblasts`

Remote tabix tests returned regional rows for:

- `Whole_Blood`, locus 57 region `1:66778016-67761890`
- `Skin_Sun_Exposed_Lower_leg`, locus 2318 region `19:10028841-11681978`

The eQTL fields include:

`variant, r2, pvalue, molecular_trait_object_id, molecular_trait_id, maf, gene_id, median_tpm, beta, se, an, ac, chromosome, position, ref, alt, type, rsid`

This field set is sufficient to construct an eQTL coloc dataset with:

- `beta`
- `varbeta = se^2`
- `MAF`
- `N = an / 2`
- `snp = rsid` or unique coordinate key
- `type = "quant"`

## 5. Feasibility by frozen Phase 4C candidate tier

All Phase 4C candidate-tissue rows now have a remote eQTL Catalogue GTEx path.

| Outcome | Evidence tier | gene-tissue rows | genes | loci | tissues | remote-tabix rows | Feasibility |
|---|---|---:|---:|---:|---:|---:|---|
| CAD | Tier A | 19 | 8 | 4 | 6 | 19 | feasible |
| CAD | Tier B1/B2/C | 25 | 18 | 7 | 6 | 25 | feasible |
| Crohn disease | Tier A | 24 | 7 | 3 | 6 | 24 | feasible |
| Crohn disease | Tier B1 | 14 | 14 | 7 | 6 | 14 | feasible |
| PsA | Tier A | 39 | 12 | 5 | 5 | 39 | feasible |
| PsA | Tier B1 | 11 | 11 | 6 | 3 | 11 | feasible |
| UC | Tier A | 26 | 6 | 3 | 7 | 26 | feasible |
| UC | Tier B1/B2/C | 16 | 15 | 6 | 4 | 16 | feasible |

## 6. CAD SMARCA4 smoke test

Smoke test target:

- outcome: CAD
- locus: 2318
- region: `19:10028841-11681978`
- gene: `SMARCA4`
- Ensembl ID: `ENSG00000127616`
- tissue: `Skin_Sun_Exposed_Lower_leg`
- eQTL source: eQTL Catalogue imported GTEx v8 remote tabix

Results:

| Metric | Value |
|---|---:|
| eQTL variants for gene in region | 5089 |
| CAD GWAS variants in locus | 4445 |
| matched variants after rsID and allele alignment | 3660 |
| smoke-test status | PASS |

The first coordinate-based attempt matched only 3 SNPs, indicating build/coordinate mismatch between the current GWAS locus files and eQTL Catalogue coordinates. Matching by rsID resolved this for CAD and produced 3660 aligned variants. This strongly suggests that formal Phase 4D should either:

1. use rsID-based matching with allele harmonization; or
2. liftover GWAS coordinates into the eQTL Catalogue coordinate system before coordinate matching.

The corrected smoke test ran `coloc.abf` using CAD binary-trait metadata (`N = 547,261`, case fraction `= 0.2243`) and produced a PP3-dominant result (`PP3 ≈ 1.00`, `PP4 = 6.17e-20`). This confirms that the extraction, rsID matching, allele harmonization and coloc execution path is functional. It also shows that `SMARCA4`, despite strong SMR support, is not coloc-supported in this CAD-skin test under the proposed PP4 threshold.

Important correction: an earlier interface-only smoke run used an overly broad eQTL extraction and returned PP4 ≈ 0.40. That value is superseded by the corrected gene-filtered smoke test and should not be cited.

## 7. GWAS metadata now available

The required binary-trait metadata table has been generated:

`results/phase4d_coloc/phase4d_gwas_binary_trait_metadata.tsv`

| Outcome | Required metadata |
|---|---|
| psoriasis | 36,466 cases; 458,078 controls; total N 494,544; case fraction 0.0737 |
| CAD | 122,733 cases; 424,528 controls; total N 547,261; case fraction 0.2243 |
| PsA | 5,065 cases; 21,286 controls; total N 26,351; case fraction 0.1922 |
| Crohn disease | 12,194 cases; 28,072 controls; total N 40,266; case fraction 0.3028 |
| UC | 12,366 cases; 33,609 controls; total N 45,975; case fraction 0.2690 |

Then update the coloc runner to use:

```r
dataset_gwas <- list(
  beta = beta,
  varbeta = se^2,
  snp = rsid,
  MAF = gwas_maf,
  N = N_total,
  s = N_cases / N_total,
  type = "cc"
)
```

For eQTL:

```r
dataset_eqtl <- list(
  beta = beta,
  varbeta = se^2,
  snp = rsid,
  MAF = maf,
  N = an / 2,
  type = "quant"
)
```

## 8. Proposed formal Phase 4D design

Do not run coloc for all 174 candidate-tissue rows at once. Freeze a restricted order:

1. CAD Tier A only as primary systemic formal coloc.
2. PsA Tier A only as positive-control formal coloc.
3. Crohn/UC Tier A stratified by positive and negative local-rg direction.
4. Tier B/C only as sensitivity after primary runs are stable.

Primary output table:

`Outcome | locus | direction | gene | tissue | nsnps | PP0 | PP1 | PP2 | PP3 | PP4 | max_snp | GWAS_N | GWAS_s | eQTL_N | input_status | interpretation_tier`

Suggested interpretation:

- `PP4 >= 0.8`: coloc-supported candidate regulatory signal.
- `0.5 <= PP4 < 0.8`: suggestive, sensitivity-only unless replicated across tissues or supported by fine-mapping.
- `PP3 > PP4`: distinct signals, not coloc-supported.
- low matched SNP count: input/QC failure, not biological null.

## 9. Manuscript consequence

Current Phase 4C manuscript wording remains valid:

> SMR/HEIDI prioritized candidate regulatory genes but did not establish formal colocalization.

After formal Phase 4D restricted coloc is run, only gene-tissue pairs with adequate SNP overlap and high PP4 should be upgraded to:

> coloc-supported regulatory candidate.

Do not call any gene a causal mediator unless additional mediation or MR evidence is later obtained.

## 10. Decision

`GO_TO_RESTRICTED_TIER_A_COLOC`

Outcome-level GWAS sample size and case fraction are now available. The next step is a restricted Tier A coloc analysis through eQTL Catalogue imported GTEx v8 remote tabix.

MR remains prohibited at this point.
