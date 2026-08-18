# PHASE 3A GWAS Data Audit

## Official Source Verification

- GWAS Catalog accession: GCST90472771
- Official GWAS Catalog REST endpoint: https://www.ebi.ac.uk/gwas/rest/api/studies/GCST90472771
- Official FTP directory: https://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCST90472001-GCST90473000/GCST90472771/
- Publication: GWAS meta-analysis of psoriasis identifies new susceptibility alleles impacting disease mechanisms and therapeutic targets.
- PubMed ID: 40021644
- Journal/date: Nat Commun / 2025-02-28
- Primary phenotype: Psoriasis
- Ancestry: European
- Cases/controls: 36,466 cases and 458,078 controls
- Total sample size: 494,544
- Genome build: GRCh37
- Coordinate system: 1-based
- Summary-statistics file type: GWAS-SSF v1.0
- Harmonization status: raw file is not harmonised
- Raw file: `data/genetics/psoriasis_GCST90472771/GCST90472771.tsv.gz`
- Local MD5: `00dcc6096819d85ea856ffc8b14fb442`
- Official MD5: `00dcc6096819d85ea856ffc8b14fb442`
- MD5 match: True
- SHA256: `4fb534184d7290b4a918d7b64adbff5a4e45229497ee3f87cd952cc07263dd62`

## Column Audit

| Required field | Status | File column |
|---|---|---|
| chromosome | available | `chromosome` |
| position | available | `base_pair_location` |
| SNP identifier | not available | no rsID column |
| effect allele | available | `effect_allele` |
| non-effect allele | available | `other_allele` |
| effect statistic | available | `beta` |
| standard error | available | `standard_error` |
| P value | available | `p_value` |
| allele frequency | not available | no EAF/RAF column |
| sample size | available as effective sample size | `cum_eff_sample_size` |
| imputation quality | not available per variant | no INFO/R2 column |
| per-study direction | available | `direction` |

## Interpretation Boundary

This audit verifies that GCST90472771 is suitable for Phase 3A summary-statistics QC and potential MAGMA-style gene-set anchoring after downstream tool/reference feasibility is checked. Missing rsID, EAF, and INFO fields must be carried forward as limitations. The raw file is preserved unchanged.
