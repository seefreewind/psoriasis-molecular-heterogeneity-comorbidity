# Phase 4B-0 rg sign/QC adjudication

## Purpose

This audit adjudicates anomalous Phase 4A global rg results before restricted LAVA. It checks whether LDSC munge preserved signed effect directions after allele alignment and documents coordinate-to-rsID mapping quality for psoriasis, CD, and UC.

## Direction audit

| trait | checked SNPs | same orientation | flipped orientation | unresolved | sign concordance | median |Z diff| | p99 |Z diff| |
|---|---:|---:|---:|---:|---:|---:|---:|
| Psoriasis | 1175841 | 1175841 | 0 | 0 | 1.000000 | 0.00234021 | 0.0123548 |
| Psoriatic arthritis | 1182068 | 1182068 | 0 | 0 | 1.000000 | 0.014423 | 0.382722 |
| Crohn disease | 1144234 | 1144234 | 0 | 0 | 1.000000 | 0.00133663 | 0.00697632 |
| Ulcerative colitis | 1144294 | 1144294 | 0 | 0 | 1.000000 | 0.00134483 | 0.00685535 |
| Coronary artery disease | 1193559 | 1193559 | 0 | 1 | 1.000000 | 0.00389474 | 0.0215172 |

## Pairwise munged Z correlations with psoriasis

| trait | shared SNPs | Pearson r | Spearman r | mean z product |
|---|---:|---:|---:|---:|
| Psoriatic arthritis | 1171636 | 0.014504 | 0.014140 | 0.018611 |
| Crohn disease | 1137184 | -0.111249 | -0.091985 | -0.163595 |
| Ulcerative colitis | 1137148 | -0.094018 | -0.084462 | -0.131357 |
| Coronary artery disease | 1174643 | 0.070522 | 0.063297 | 0.109384 |

## Coordinate mapping QC

```text
### crohn_disease_GCST004132.hm3_mapping_qc.tsv
metric	value
hm3_position_missing_snplist_alleles	100358
mapped_hm3_allele_matched	1144234
no_hm3_position_match	7956757
non_acgt_or_non_snp	369438
total_rows	9570787
mapped_fraction_of_raw	0.119555
output_sumstats	results/phase4a/munge_inputs/crohn_disease_GCST004132.hm3_rsids.tsv.gz
ldsc_reference	/Users/zy/Documents/ChatGPT/银屑病机制论文设计/psoriasis_endotype_comorbidity/data/genetics/reference/ldsc/eur_w_ld_chr_zenodo18749273/eur_w_ld_chr

### psoriasis_GCST90472771.hm3_mapping_qc.tsv
metric	value
allele_pair_mismatch	1201
hm3_duplicate_positions	0
hm3_ldscore_rows	1290028
hm3_position_missing_snplist_alleles	105775
hm3_unique_positions	1290028
mapped_hm3_allele_matched	1184002
no_hm3_position_match	9348685
non_acgt_or_non_snp	1169294
total_gwas_rows	11808957
mapped_fraction_of_raw	0.100263
output_sumstats	/Users/zy/Documents/ChatGPT/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4a/munge_inputs/psoriasis_GCST90472771.hm3_rsids.tsv.gz
ldsc_reference	/Users/zy/Documents/ChatGPT/银屑病机制论文设计/psoriasis_endotype_comorbidity/data/genetics/reference/ldsc/eur_w_ld_chr_zenodo18749273/eur_w_ld_chr

### ulcerative_colitis_GCST004133.hm3_mapping_qc.tsv
metric	value
hm3_position_missing_snplist_alleles	100374
mapped_hm3_allele_matched	1144294
no_hm3_position_match	7973967
non_acgt_or_non_snp	369381
total_rows	9588016
mapped_fraction_of_raw	0.119346
output_sumstats	results/phase4a/munge_inputs/ulcerative_colitis_GCST004133.hm3_rsids.tsv.gz
ldsc_reference	/Users/zy/Documents/ChatGPT/银屑病机制论文设计/psoriasis_endotype_comorbidity/data/genetics/reference/ldsc/eur_w_ld_chr_zenodo18749273/eur_w_ld_chr

```

## Interim adjudication

Munge-direction audit is considered PASS when sign concordance is ~1.0, unresolved allele orientation is 0, and absolute Z differences are negligible after expected allele flips. If CD/UC remain negative under this audit, the negative rg should not be attributed to a simple A1/A2 flip in the LDSC input. The next adjudication layer is sensitivity LDSC after MHC exclusion and explicit CD/UC sign-flip stress tests.

- Direction audit table: `/Users/zy/Documents/ChatGPT/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4b0/phase4b0_direction_audit.tsv`
- Pairwise Z table: `/Users/zy/Documents/ChatGPT/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4b0/phase4b0_pairwise_z_correlation.tsv`

## LDSC sensitivity adjudication

| trait | sensitivity | rg | SE | P | cross-trait intercept |
|---|---|---:|---:|---:|---:|
| Psoriatic arthritis | explicit_no_MHC | 1.1715 | 0.0751 | 6.75e-55 | 0.3142 |
| Crohn disease | explicit_no_MHC | -0.2717 | 0.0449 | 1.43e-09 | -0.0636 |
| Ulcerative colitis | explicit_no_MHC | -0.2233 | 0.0409 | 4.82e-08 | -0.0625 |
| Coronary artery disease | explicit_no_MHC | 0.1732 | 0.0274 | 2.5e-10 | 0.0189 |
| Crohn disease | outcome_Z_sign_flipped | 0.2717 | 0.0449 | 1.43e-09 | 0.0636 |
| Ulcerative colitis | outcome_Z_sign_flipped | 0.2233 | 0.0409 | 4.82e-08 | 0.0625 |

## Final Phase 4B-0 adjudication

**PsA:** processing direction is PASS, but rg > 1 and cross-trait intercept remains high after explicit no-MHC sensitivity. Adjudication: keep as positive-control / near-neighbor sensitivity only; do not use as an independent multisystem comorbidity signal.

**CD/UC:** processing direction is PASS and explicit no-MHC sensitivity does not change the negative rg. Forced sign flipping mirrors rg to the same positive magnitude, confirming that LDSC is responding coherently to the signed input. Adjudication: no simple munge or allele-flip bug detected; retain CD/UC as QC-flagged targets. Their global negative rg should be interpreted only after restricted local rg checks for directional heterogeneity.

**CAD:** processing direction is PASS and no-MHC sensitivity is unchanged. Adjudication: clean primary systemic target for restricted LAVA.

**Phase 4B restricted LAVA scope:** CAD primary; PsA positive-control / near-neighbor sensitivity; CD and UC QC-flagged local-heterogeneity targets. Stroke and CKD remain null/low-power references and are not included in restricted LAVA main analysis.

- LDSC sensitivity table: `/Users/zy/Documents/ChatGPT/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4b0/phase4b0_ldsc_sensitivity_rg.tsv`
