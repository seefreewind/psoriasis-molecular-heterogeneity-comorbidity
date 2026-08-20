# Matched-Null MAGMA Method Audit

Matched-null gene sets were generated for F1, F2, F6 and F7 using 2,000 random sets per axis (8,000 total). The random seed was 20260811. The gene universe came from the MHC-excluded MAGMA gene-level output for the psoriasis GWAS. Random sets were matched on chromosome, gene length and the number of SNPs assigned to each gene. Gene length and SNP count were divided into five quantile bins each.

Sampling first used the exact `(chromosome, length_bin, nsnp_bin)` stratum. If a stratum had insufficient eligible genes, sampling fell back to `(length_bin, nsnp_bin)`, and then to the remaining universe if needed. Axis genes and genes already sampled in the same random set were excluded. Empirical P values were computed as `(number of null beta values >= observed beta + 1) / (number of null sets + 1)`.

Matched-null generation rows: 8000. Maximum fallback draws in any random set: 2.

Observed matched-null summary:

| axis   |   observed_statistic |    null_mean |   null_SD |   empirical_percentile |   empirical_P |   n_random_sets |
|:-------|---------------------:|-------------:|----------:|-----------------------:|--------------:|----------------:|
| F1     |            -0.053787 | -0.000584955 | 0.0581531 |                   17.8 |     0.822089  |            2000 |
| F2     |             0.05185  |  0.00482435  | 0.0360302 |                   90.9 |     0.0914543 |            2000 |
| F6     |             0.042266 |  0.0140349   | 0.0771859 |                   64.4 |     0.356322  |            2000 |
| F7     |             0.04433  | -0.0118252   | 0.0625853 |                   79.9 |     0.201399  |            2000 |
