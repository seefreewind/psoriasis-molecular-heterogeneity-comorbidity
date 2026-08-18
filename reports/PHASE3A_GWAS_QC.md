# PHASE 3A GWAS QC

## Summary

- Total variants read: 11,808,957
- Expected variants from GWAS Catalog REST: 11,808,957
- MD5 matched official checksum: True
- Missing P values: 0
- Invalid P values: 0
- Duplicate chr:pos:allele records: 7,045
- Duplicated rsIDs: not available because the file has no rsID column
- Multiallelic positions: 55,701
- Non-autosomal variants: 0
- Ambiguous A/T or C/G SNPs: 1,648,532
- Extreme absolute beta > 5: 0
- Extreme absolute beta > 10: 0
- INFO distribution: not available; no INFO/R2 column
- Sample-size distribution: see `results/phase3a/gwas_qc_numeric_distributions.tsv`
- Chromosome distribution: see `results/phase3a/gwas_qc_chromosome_distribution.tsv`
- Allele-pair distribution: see `results/phase3a/gwas_qc_allele_pair_distribution.tsv`

## Coordinate And Build Consistency

Official metadata records GRCh37, 1-based coordinates. The publication methods state that summary statistics were aligned using GRCh37 positions and alleles. The file contains autosomal chromosomes 1-22 only under the current QC.

## Phase 3A Consequence

The summary statistics pass basic file-integrity and field-level QC for an MHC-excluded primary gene-set analysis. The missing rsID, allele-frequency, and imputation-quality fields should be handled explicitly during any downstream harmonization. For MAGMA, chr:bp plus alleles can be converted or mapped to a reference SNP set if the reference panel and build are fixed before association results are inspected.
