# Phase 5 Figure 5 Shared Genetic Architecture Report

Date: 2026-08-16

## Figure decision

Figure 5 has been generated to summarize Phase 4A/4B shared genetic architecture.

Core conclusion:

```text
Overall psoriasis susceptibility shows selected comorbidity-level sharing, and restricted LAVA resolves this into CAD-positive architecture, PsA positive-control sharing, and IBD directional heterogeneity.
```

## Outputs

Figure files:

| File | Use |
|---|---|
| `results/figures/phase4a4b/Figure5_shared_genetic_architecture.svg` | editable vector |
| `results/figures/phase4a4b/Figure5_shared_genetic_architecture.pdf` | vector PDF; see PDF audit note |
| `results/figures/phase4a4b/Figure5_shared_genetic_architecture.png` | visual QA / draft preview |
| `results/figures/phase4a4b/Figure5_shared_genetic_architecture.tiff` | high-resolution raster |
| `results/figures/phase4a4b/Figure5_shared_genetic_architecture_QA.tsv` | figure QA metadata |

Source data:

| File | Panel |
|---|---|
| `results/figures/phase4a4b/source_data/figure5_panel_a_ldsc_rg.tsv` | Panel A |
| `results/figures/phase4a4b/source_data/figure5_panel_b_lava_counts.tsv` | Panel B |
| `results/figures/phase4a4b/source_data/figure5_panel_c_selected_lava_loci.tsv` | Panel C |

Script:

```text
src/figures/phase4a4b_make_shared_architecture_panel.R
```

## Panel map

| Panel | Message |
|---|---|
| A | Genome-wide LDSC rg shows PsA, Crohn disease, UC and CAD as FDR-supported, with CAD the cleanest non-neighbor PASS signal |
| B | Restricted LAVA shows CAD positive local sharing, PsA strong positive-control architecture, and IBD mixed-direction local structure |
| C | Selected local rg loci show directional heterogeneity across outcomes, especially IBD loci with positive and negative local rho |

## Main values represented

Panel A:

| Outcome | rg | FDR | QC role |
|---|---:|---:|---|
| PsA | 1.1715 | 4.05e-54 | near-neighbor / QC label |
| Crohn disease | -0.2717 | 2.87e-09 | QC-flagged IBD |
| UC | -0.2233 | 7.23e-08 | QC-flagged IBD |
| CAD | 0.1732 | 7.49e-10 | PASS primary systemic target |
| Stroke | 0.0255 | 0.791 | PASS null/low-power reference |
| CKD | 0.0118 | 0.791 | PASS null/low-power reference |

Panel B:

| Outcome | FDR-supported local loci | Nominal positive | Nominal negative |
|---|---:|---:|---:|
| CAD | 23 | 21 | 10 |
| PsA | 31 | 36 | 0 |
| Crohn disease | 49 | 9 | 51 |
| UC | 19 | 7 | 18 |

Panel C:

Panel C displays selected FDR-supported and pre-specified key local loci. It is intended to show local direction rather than exhaustively list all significant loci. Full LAVA results remain in the supplementary table.

## QA

Static figure preflight:

```text
19 PASS
1 WARN
0 FAIL
verdict = READY_FOR_VISUAL_QA
```

Visual QA:

```text
PASS
```

The final PNG was inspected. Labels and panels are readable without obvious truncation. The figure is information-dense, but it is suitable as a manuscript-level summary of Phase 4A/4B.

PDF text audit:

```text
FAIL_BY_AUTOMATED_TF_SCAN
```

The PDF audit reported `Tf=1` for all text runs, the same issue observed for Figure 7. This likely reflects the R Cairo PDF encoding of font transforms rather than the intended rendered font size. Recommended production route:

```text
Use SVG for editable vector assembly.
Use TIFF for raster submission/export if needed.
Use PDF only after downstream layout software confirms text scaling.
```

## Manuscript legend draft

**Figure 5. Genome-wide and local shared genetic architecture between psoriasis and comorbid outcomes.**  
**A**, LDSC genome-wide genetic correlations between overall psoriasis susceptibility and frozen comorbidity outcomes. Points show rg and horizontal bars show 95% confidence intervals. Fill indicates FDR support; color indicates QC interpretation. **B**, Restricted LAVA local architecture among CAD, PsA, Crohn disease and UC after joint local heritability screening. Bars show FDR-supported loci and nominal positive or negative local rg loci. **C**, Selected FDR-supported and pre-specified key local loci showing local rho across outcomes. Orange indicates positive local rg and blue indicates negative local rg. CAD showed positive systemic local architecture, PsA served as a positive-control near-neighbor phenotype, and IBD showed directionally heterogeneous local architecture.

## Manuscript use

Recommended placement:

```text
Results section after Phase 3A NO-GO and before SMR/HEIDI.
```

Recommended accompanying sentence:

> These results supported a shift from axis-specific genetic anchoring to overall psoriasis comorbidity genetics, with CAD providing the cleanest systemic signal and IBD requiring local, direction-aware interpretation.

