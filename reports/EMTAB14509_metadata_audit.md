# E-MTAB-14509 metadata audit

## Source

Official EMBL-EBI BioStudies / ArrayExpress accession: E-MTAB-14509.

Local metadata files:

- `data/metadata/E-MTAB-14509.biostudies.json`
- `data/metadata/E-MTAB-14509.idf.txt`
- `data/metadata/E-MTAB-14509.sdrf.txt`

## Required audit answers

1. Total patients: 146 unique `Characteristics[individual]` values.
2. Discovery / replication patients: discovery 89, replication 57.
3. Baseline patients: 145 total; discovery 88, replication 57.
4. Patient tissues: see `results/qc/patient_tissue_matrix.tsv`.
5. Lesional skin baseline completeness: 139 baseline samples.
6. Non-lesional skin baseline completeness: 139 baseline samples.
7. Blood baseline completeness: 82 baseline samples.
8. Three-tissue complete baseline patients: 76; by cohort: {'discovery': 76, 'replication': 0}.
9. Repeated measurements: yes. Official timepoints include 0, 1, 4, and 12 weeks. These are excluded from discovery except time 0.
10. Treatment assignment relative to baseline: drug assignment is present at baseline. Metadata alone does not prove dosing occurred after the sample, so baseline is treated as pretreatment by design and flagged for publication-method confirmation.
11. Missing BMI/PASI: see `results/qc/missingness.tsv`.
12. Age/sex/HLA-C*06:02: age, sex, and HLA-C*06:02 carrier are present in SDRF; HLA contains NA values.
13. Expression matrix type: official protocol states raw count matrix and TMM-normalised matrix; the publication states log2-CPM after TMM normalisation for modelling.
14. Obvious batch variables: cohort and tissue are encoded through count files and sequencing/library methods. Discovery skin, discovery blood, and replication skin were generated under different protocols/platforms in the publication, so batch is a major audit variable.
15. Patient leakage: no patient crosses discovery and replication in the SDRF-derived cohort labels. See `results/qc/leakage_checks.tsv`.

## Baseline sample structure

```text
cohort       tissue          
discovery    Lesional Skin       82
             Nonlesional Skin    82
             Whole Blood         82
replication  Lesional Skin       57
             Nonlesional Skin    57
```

## Key risks

- Replication contains lesional and non-lesional skin but no whole-blood samples in the official SDRF/count-file mapping.
- Baseline discovery has 88 patients with baseline samples, while the full discovery cohort has 89 patients. This must be explained before final Phase 1 inference.
- Cross-tissue replication of blood-derived structure is not directly possible within E-MTAB-14509 replication and must be handled as a design limitation or discovery-only blood contribution.
- Clinical metadata are limited relative to the manuscript ambition; PASI, BMI, age, sex, HLA-C*06:02, drug, biologic-naive status, anti-TNF-naive status, psoriatic arthritis, and onset fields are available.

## Generated audit tables

- `results/qc/sample_flow.tsv`
- `results/qc/patient_tissue_matrix.tsv`
- `results/qc/missingness.tsv`
- `results/qc/leakage_checks.tsv`
- `results/qc/official_file_audit.tsv`
