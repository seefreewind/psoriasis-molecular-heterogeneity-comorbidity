# GSE244679 statistic definition

Authoritative script: `src/integration/phase1b_external_replication.py`.

Sample unit: 24 paired replicate IDs, with 48 total specimens in the analyzed metadata. Each valid pair contributed one lesional psoriatic sample and one adjacent-normal sample.

Scoring:

1. Raw counts were aggregated by gene symbol and transformed to log2 CPM.
2. For each sample, genes were converted to within-sample percentile ranks.
3. For each archived gene set feature, the score was the mean percentile rank of genes present in that sample; scores were then z-scored across samples.
4. For each pair and feature, the external contrast was score(lesional psoriatic skin) − score(adjacent-normal skin).
5. The paired feature-level contrasts were averaged across the 24 pairs.

Reported statistic:

ρ = Spearman correlation across common axis features between the discovery factor loading vector for a given factor/view and the GSE244679 mean paired feature-level contrast vector.

It is not a donor-score versus phenotype correlation. Absolute |ρ| was reported because factor sign is arbitrary in latent-factor models.

Source rows:

| dataset   | axis   | view   |   n_pairs |   n_common_axis_features |   loading_vs_paired_lesional_minus_adjacent_spearman | external_effect_definition                                                       |
|:----------|:-------|:-------|----------:|-------------------------:|-----------------------------------------------------:|:---------------------------------------------------------------------------------|
| GSE244679 | F1     | LS     |        24 |                      424 |                                           -0.688398  | mean paired score difference: lesional psoriatic skin minus adjacent normal skin |
| GSE244679 | F1     | NL     |        24 |                      423 |                                           -0.0458274 | mean paired score difference: lesional psoriatic skin minus adjacent normal skin |
| GSE244679 | F2     | LS     |        24 |                      424 |                                            0.0831148 | mean paired score difference: lesional psoriatic skin minus adjacent normal skin |
| GSE244679 | F2     | NL     |        24 |                      423 |                                           -0.518229  | mean paired score difference: lesional psoriatic skin minus adjacent normal skin |
| GSE244679 | F6     | LS     |        24 |                      424 |                                            0.375292  | mean paired score difference: lesional psoriatic skin minus adjacent normal skin |
| GSE244679 | F6     | NL     |        24 |                      423 |                                            0.184443  | mean paired score difference: lesional psoriatic skin minus adjacent normal skin |
| GSE244679 | F7     | LS     |        24 |                      424 |                                            0.119979  | mean paired score difference: lesional psoriatic skin minus adjacent normal skin |
| GSE244679 | F7     | NL     |        24 |                      423 |                                            0.203905  | mean paired score difference: lesional psoriatic skin minus adjacent normal skin |
