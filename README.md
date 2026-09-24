# Psoriasis molecular heterogeneity: JDS reproducibility release

Version 1.1.0 accompanies the Journal of Dermatological Science submission, “Molecular heterogeneity and multisystem shared genetic architecture define distinct biological layers of psoriasis.” It contains the project analysis scripts, configuration files, environment specification, aggregated source data for the five main figures and Supplementary Tables S17–S18, and the final figure exports.

## Scope

The release supports inspection and regeneration of the manuscript figures from the included aggregate source tables. The analysis scripts document the broader workflow. Full re-execution of every upstream analysis requires the original input datasets, reference panels and, where applicable, access granted by the original data providers.

Raw expression/genotype data, controlled-access source files, GWAS summary-statistic files, GTEx BESD resources, local LD references, manuscript Word files and rendering/QA caches are not redistributed. Figure source tables contain aggregate results and de-identified donor-level derived scores used to reproduce plotted points; donor labels and any linkage key are omitted. Dataset accessions and source-specific access conditions are described in the manuscript and its Supplementary Information.

## Contents

- `src/`, `configs/`, `ANALYSIS_LOCK.md`: analysis scripts and project configuration.
- `environment/environment.yml`: conda environment specification; external genetics tools and reference data may require separate installation.
- `source_data/`: aggregate source tables for Figures 1–5 and Supplementary Tables S17–S18.
- `figures/`: final TIFF (600 dpi) and editable SVG figure files.
- `scripts/rebuild_figures.py`: regenerate Figures 1–5 from the included source tables.

## Regenerate figures

Create the documented conda environment or install Python 3.11 with NumPy, pandas and Matplotlib, then run from this directory:

```bash
python scripts/rebuild_figures.py
```

The script writes TIFF and SVG files to `figures/`. It does not rerun the upstream transcriptomic or genetic analyses.

## Data access

The study integrates E-MTAB-14509, GSE244679, GSE61281, GSE228421, GSE173706, GSE225475, GSE202011, psoriasis GWAS GCST90472771 and GTEx v8 regulatory resources, together with the prespecified comorbidity GWAS described in the article. Obtain original files directly from their source repositories and comply with the relevant access agreements. No raw or controlled-access participant-level data are included here.

## License and citation

Code and packaged source assets are released under the MIT License. Cite this version using the citation metadata in `CITATION.cff` or the version-specific Zenodo record associated with GitHub tag `v1.1.0`. The Zenodo concept DOI is https://doi.org/10.5281/zenodo.22020395. The earlier version-specific DOI 10.5281/zenodo.22020396 remains unchanged and refers to tag `v1.0.00`.
