# Phase 4E Transcriptomic Contextualization Report

Date: 2026-08-16

## Executive decision

Phase 4E transcriptomic contextualization can proceed, but only as a bounded interpretation layer.

Current status:

```text
PHASE4E_CONTEXTUALIZATION_READY
NO_AXIS_SPECIFIC_GENETIC_CLAIM
NO_AXIS_TO_COLOC_GENE_DIRECT_BRIDGE
```

The key result from the overlap audit is simple and important: Phase 4D PP4-supported or suggestive coloc candidates do not directly overlap the frozen F1/F2/F6/F7 CORE/EXTENDED molecular-axis gene programs.

This means the transcriptomic axes should not be used to claim that the identified coloc genes are axis genes or that any molecular axis is genetically anchored. The correct use is contextual: the axes describe reproducible psoriasis tissue-state heterogeneity, while Phase 4 genetics describes overall psoriasis susceptibility shared with comorbidity architectures.

## Inputs

Transcriptomic axis sources:

| Source | File |
|---|---|
| Phase 2A axis prioritization | `results/phase2a/Table_axis_prioritization_master.tsv` |
| Frozen axis gene programs | `results/phase2a/axis_gene_programs/F1_gene_program.tsv`; `F2_gene_program.tsv`; `F6_gene_program.tsv`; `F7_gene_program.tsv` |
| Final single-cell/spatial triangulation | `results/phase2c/Table_mechanism_triangulation.tsv` |

Genetic candidate source:

| Source | File |
|---|---|
| Phase 4D PP4-supported/suggestive candidates | `results/phase4d_coloc/manuscript_tables/phase4d_coloc_supported_and_suggestive_candidates.tsv` |

New Phase 4E outputs:

| File | Description |
|---|---|
| `results/phase4e_contextualization/phase4e_coloc_candidate_axis_program_overlap.tsv` | coloc candidate by frozen axis gene-program overlap |
| `results/phase4e_contextualization/phase4e_coloc_axis_overlap_summary.tsv` | compact overlap summary |

## Frozen transcriptomic boundary

Phase 2C ended with a shrink decision:

```text
SHRINK_TO_BULK_MOLECULAR_PROGRAMS_WITH_DIRECTIONAL_CELLULAR_SPATIAL_SUPPORT
```

The frozen axis interpretation is:

| Axis | Final transcriptomic interpretation | Confidence | Allowed role |
|---|---|---|---|
| F1 | keratinocyte stress/inflammatory spatial program | DIRECTIONAL_SUPPORT_ONLY | bulk axis with directional keratinocyte/spatial support |
| F2 | keratinocyte stress/inflammatory spatial program | DIRECTIONAL_SUPPORT_ONLY | bulk axis with directional keratinocyte/spatial support |
| F6 | keratinocyte stress/inflammatory spatial program | DIRECTIONAL_SUPPORT_ONLY | bulk axis with directional keratinocyte/spatial support |
| F7 | systemic/supportive immune axis; not skin-spatial-localized | LOW | supportive systemic axis only |

Important boundary:

```text
F1/F2/F6/F7 are not genetically anchored axes.
They are not exposures in Phase 4.
They cannot be used to relabel Phase 4D genes as axis genes.
```

## Direct gene-program overlap audit

The PP4-supported and suggestive Phase 4D candidate genes were compared against all frozen F1/F2/F6/F7 CORE and EXTENDED gene programs.

Genes tested:

| Outcome | Gene | Best coloc tier |
|---|---|---|
| CAD | UBQLN4 | suggestive |
| CAD | MEX3A | suggestive |
| Crohn disease | SLC22A5 | suggestive |
| Crohn disease | PARK7 | suggestive |
| PsA | SLC22A5 | coloc-supported |
| PsA | RP11-977G19.11 | coloc-supported |
| UC | RP11-973H7.1 | coloc-supported |

Result:

```text
No Phase 4D PP4-supported or suggestive candidate directly overlaps F1/F2/F6/F7 CORE/EXTENDED gene programs.
```

Interpretation:

The overlap audit blocks a direct axis-to-coloc-gene claim. This is a useful guardrail. It keeps the manuscript from implying that the psoriasis molecular axes explain the coloc genes at the gene-membership level.

## Contextualization logic

The correct Phase 4E narrative is layered:

```text
Bulk psoriasis molecular axes
    -> describe reproducible tissue-state heterogeneity
    -> show directional keratinocyte/stress/spatial support

Overall psoriasis genetic susceptibility
    -> shows shared architecture with selected comorbidities
    -> localizes architecture through LAVA
    -> prioritizes expression-linked genes through SMR/HEIDI
    -> tests shared causal-signal evidence through restricted coloc

Contextualization
    -> asks whether the tissues and disease systems are biologically coherent
    -> does not claim that axes are genetically anchored
```

## Disease-level interpretation

### CAD

CAD remains the cleanest non-neighbor systemic architecture signal from Phase 4A/4B, but Phase 4D coloc did not identify a PP4-supported CAD gene-tissue pair. UBQLN4 and MEX3A were suggestive skin eQTL candidates at locus 113, but neither gene overlapped the frozen F1/F2/F6/F7 gene programs.

Allowed interpretation:

```text
CAD supports psoriasis systemic shared genetic architecture.
The CAD eQTL-coloc layer is suggestive only.
The CAD candidates can be discussed alongside psoriasis skin-state biology, but not as direct molecular-axis genes.
```

Blocked interpretation:

```text
F1/F2/F6 genetically mediate psoriasis-CAD sharing.
UBQLN4 or MEX3A are F1/F2/F6 axis genes.
```

### PsA

PsA recovered strong PP4-supported positive-control signals for SLC22A5 and RP11-977G19.11 in immune-relevant tissues. These genes did not overlap the frozen axis programs.

Allowed interpretation:

```text
PsA validates the coloc workflow and supports immune/eQTL sharing in a near-neighbor psoriatic phenotype.
```

Blocked interpretation:

```text
F7 is genetically anchored by PsA coloc.
SLC22A5 is an F7 axis gene.
```

### IBD

Crohn disease had only suggestive coloc candidates. UC produced strong colon-specific RP11-973H7.1 coloc under the eQTL MAF-proxy sensitivity framework. None of the IBD candidates overlapped F1/F2/F6/F7 programs.

Allowed interpretation:

```text
IBD supports local-direction heterogeneity and tissue-specific shared architecture.
UC has a high-value colon-specific coloc candidate requiring EAF-complete sensitivity.
```

Blocked interpretation:

```text
F1/F2/F6 explain psoriasis-IBD genetic sharing.
UC RP11-973H7.1 is a frozen psoriasis axis gene.
```

## Manuscript-ready paragraph

The transcriptomic and genetic layers converged at the level of tissue context rather than gene membership. F1, F2 and F6 were retained as bulk psoriasis molecular programs with directional keratinocyte and spatial stress/inflammatory support, and F7 was retained only as a systemic supportive program. In contrast, the Phase 4 genetic analyses used overall psoriasis susceptibility rather than molecular-axis exposures. A direct overlap audit showed that PP4-supported or suggestive Phase 4D coloc candidates did not overlap the frozen F1/F2/F6/F7 CORE or EXTENDED gene programs. These results argue against presenting the comorbidity genetics as genetically anchored molecular axes. Instead, the axes provide transcriptomic context for psoriasis tissue heterogeneity, whereas the genetics layer identifies overall psoriasis shared architecture and a narrower set of expression-linked candidate loci across CAD, PsA and IBD.

## Figure/story integration

Recommended final figure logic:

| Panel | Message |
|---|---|
| Transcriptomic panel | F1/F2/F6 are directional keratinocyte/spatial bulk programs; F7 is supportive/systemic |
| Genetic architecture panel | Overall psoriasis susceptibility shares genome-wide/local architecture with selected outcomes |
| SMR/coloc panel | Some shared loci yield expression-prioritized genes, but CAD lacks strong PP4 and IBD is heterogeneous |
| Integration panel | Transcriptomic axes contextualize psoriasis biology but do not serve as genetic exposures |

Recommended visual annotation:

```text
Transcriptomic axes: contextual layer
Overall psoriasis GWAS: genetic anchor
LAVA/SMR/coloc: comorbidity genetics layer
```

## Final manuscript boundary statement

Use this sentence near the end of Results or early in Discussion:

> We therefore treated the molecular axes and comorbidity genetics as complementary but non-interchangeable evidence layers: the axes summarize reproducible psoriasis tissue-state heterogeneity, whereas the genetic analyses test shared susceptibility architecture for overall psoriasis.

## Next action

The next step should be manuscript assembly or figure consolidation.

Recommended next task:

```text
PHASE5_MANUSCRIPT_SPINE_AND_FIGURE_MAP
```

Do not start MR unless a new decision is made to run a restricted, PP4-supported, EAF-complete sensitivity analysis. At the current evidence level, broad MR would add more interpretive risk than value.

