# Clustering Parameter Audit

The archived discrete endotype smoke-test used discovery lesional-minus-nonlesional normalized expression, selected the top 1,000 variable genes, standardized features in the discovery set, and reduced the data by PCA. K-means was evaluated for k=2 to k=6 on the first five PCs, using `random_state=20260810` and `n_init=100` for the primary fit. Bootstrap stability used 100 bootstrap resamples, k-means `n_init=20` inside each resample, and best-match Jaccard overlap between original and bootstrap clusters. The eligibility rule required minimum cluster size >=10 and minimum bootstrap Jaccard >=0.75; if no k met both criteria, the highest-silhouette k was selected for smoke-test assignment only.

This clustering branch was not used to define the final manuscript claims. The final manuscript treats continuous molecular axes as the molecular phenotype.
