# Phase 5 Figure 7 Restricted Coloc Contextualization Report

Date: 2026-08-16

## Figure decision

Figure 7 has been generated as a compact Phase 4D/4E integration panel.

Core conclusion:

```text
Restricted coloc separates shared local architecture from PP4-supported eQTL signals, and the frozen transcriptomic axes remain contextual layers rather than genetic exposures.
```

## Outputs

Figure files:

| File | Use |
|---|---|
| `results/figures/phase4d/Figure7_restricted_coloc_contextualization.svg` | editable vector |
| `results/figures/phase4d/Figure7_restricted_coloc_contextualization.pdf` | vector PDF; see PDF audit note |
| `results/figures/phase4d/Figure7_restricted_coloc_contextualization.png` | visual QA / draft preview |
| `results/figures/phase4d/Figure7_restricted_coloc_contextualization.tiff` | high-resolution raster |
| `results/figures/phase4d/Figure7_restricted_coloc_contextualization_QA.tsv` | figure QA metadata |

Source data:

| File | Panel |
|---|---|
| `results/figures/phase4d/source_data/figure7_panel_a_coloc_candidates.tsv` | Panel A |
| `results/figures/phase4d/source_data/figure7_panel_b_tier_counts.tsv` | Panel B |
| `results/figures/phase4d/source_data/figure7_panel_c_axis_overlap.tsv` | Panel C |

Script:

```text
src/figures/phase4d_make_coloc_contextualization_panel.R
```

## Panel map

| Panel | Message |
|---|---|
| A | PP4-supported and suggestive coloc candidates across CAD, PsA, Crohn disease and UC |
| B | Most restricted Tier A coloc tests favored distinct signals rather than shared causal signals |
| C | No PP4-supported/suggestive candidate directly overlapped frozen F1/F2/F6/F7 axis programs |

## Data shown

Panel A displays only PP4-supported or suggestive candidates:

| Outcome | Key message |
|---|---|
| CAD | UBQLN4 and MEX3A are suggestive only |
| PsA | SLC22A5 and RP11-977G19.11 provide positive-control PP4 support |
| Crohn disease | SLC22A5 and PARK7 are suggestive only |
| UC | RP11-973H7.1 is PP4-supported in colon, with MAF-proxy sensitivity label in the table |

Panel B displays all restricted Tier A coloc tests:

| Outcome | PP4 high | PP4 suggestive | PP3 dominant |
|---|---:|---:|---:|
| CAD | 0 | 4 | 15 |
| PsA | 3 | 4 | 32 |
| Crohn disease | 0 | 2 | 22 |
| UC | 2 | 0 | 24 |

Panel C displays direct overlap with frozen F1/F2/F6/F7 gene programs:

| Outcome | Direct overlaps / PP4-supported or suggestive candidates |
|---|---:|
| CAD | 0/4 |
| PsA | 0/7 |
| Crohn disease | 0/2 |
| UC | 0/2 |

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

The final PNG was inspected after shortening tissue labels and legend labels. The current version has no obvious text overlap or truncation in the rendered preview.

PDF text audit:

```text
FAIL_BY_AUTOMATED_TF_SCAN
```

The PDF audit reported `Tf=1` for all text runs. This is likely due to how the R Cairo PDF device encodes font transforms rather than the visually rendered font size. Because the PNG/SVG visual QA is acceptable and the static preflight detected no sub-5-pt text settings, the preferred production route is:

```text
Use SVG for editable vector assembly.
Use TIFF for raster submission/export if needed.
Use PDF only after downstream layout software confirms text scaling.
```

## Manuscript legend draft

**Figure 7. Restricted eQTL colocalization and transcriptomic contextualization of shared psoriasis-comorbidity loci.**  
**A**, PP4-supported and suggestive restricted coloc candidates among Phase 4C Tier A gene-tissue pairs. The dashed line marks PP4 = 0.80. Filled points indicate PP4-supported candidates; open points indicate suggestive candidates. **B**, Evidence-tier distribution across all restricted Tier A coloc tests. Most tested gene-tissue pairs favored distinct causal signals rather than shared causal signals. **C**, Direct overlap audit between PP4-supported or suggestive coloc candidates and frozen F1/F2/F6/F7 CORE/EXTENDED gene programs. No direct axis-gene overlap was detected, supporting the use of molecular axes as transcriptomic contextual layers rather than genetic exposures.

## Manuscript use

Recommended placement:

```text
End of Results, after restricted coloc subsection.
```

Recommended accompanying sentence:

> Together, these results separate shared local genetic architecture from coloc-supported eQTL evidence and show that the frozen molecular axes contextualize psoriasis tissue biology without serving as genetic exposures.

