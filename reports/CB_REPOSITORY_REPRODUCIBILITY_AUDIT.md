# Repository Reproducibility Audit

Status: `PASS_WITH_RELEASE_TAG_RECOMMENDED`

- README describes manuscript workflow: `PASS`. README describes the final manuscript workflow and repository layout.
- software versions documented: `PARTIAL`. environment/environment.yml exists; exact versions are mostly unconstrained.
- installation instructions: `PASS`. README points to the conda environment file.
- data access instructions: `PASS`. README lists public accessions and explains excluded raw/restricted data.
- paths are not hard-coded to local machine: `PARTIAL`. Some local paths remain in reports, but executable scripts are repository-relative where practical.
- no private credentials: `PASS`. No obvious credential strings detected in audited text files.
- figure scripts map to Figures 1-6: `PASS`. src/figures/make_communications_biology_final_figures.py maps to final figures.
- table scripts map to Tables 1-3: `PASS`. source_data/Table1-3_source_data.tsv exist.
- source-data outputs reproducible: `PARTIAL`. source data exist; public archive missing.
- repository version/tag matches manuscript: `PARTIAL`. GitHub repository URL is recorded; release tag should be added after push.
