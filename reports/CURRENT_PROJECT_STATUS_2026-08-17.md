# Current Project Status

Date: 2026-08-17

Project folder:

```text
/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity
```

## One-line status

The project has moved from analysis expansion to manuscript assembly.

Current decision:

```text
GO_TO_MANUSCRIPT_ASSEMBLY
CONDITIONAL_GO_TO_TARGETED_FIGURE_COMPLETION
NO_GO_TO_BROAD_MR
NO_GO_TO_AXIS_SPECIFIC_GENETICS
```

The manuscript spine is now:

```text
Reproducible psoriasis tissue molecular heterogeneity
    + overall psoriasis multisystem shared genetic architecture
    + restricted shared-locus/eQTL prioritization
    + transcriptomic contextualization without axis-specific genetic claims
```

## Core scientific position

Discrete k=2 transcriptomic endotypes were not stable enough to carry the paper. Continuous molecular axes were more reproducible and became the transcriptomic framework.

F1, F2 and F6 are retained as skin-primary bulk molecular programs with directional keratinocyte/spatial stress-inflammatory support. F7 is retained only as a systemic/supportive immune candidate. None of these axes reached the threshold for formal genetically anchored mechanistic endotypes.

Phase 3A closed the axis-specific genetics route:

```text
NO-GO_FOR_GENETICALLY_ANCHORED_AXES
```

The genetics main analysis therefore uses overall psoriasis susceptibility, not F1/F2/F6/F7 axis exposures.

## Phase-by-phase status

### Phase 1 / 1B

Status:

```text
COMPLETE
```

Main conclusion:

Discrete endotypes were unstable, but continuous molecular axes were usable. Independent paired-skin replication supported the continuous-axis route.

Key reports:

| File | Role |
|---|---|
| `reports/PHASE1_ENDOTYPE_GO_NOGO_REPORT.md` | discrete endotype decision |
| `reports/PHASE1B_MOLECULAR_AXIS_REPORT.md` | continuous molecular-axis report |

### Phase 2A / 2B / 2C

Status:

```text
COMPLETE_WITH_SHRINK
```

Final transcriptomic decision:

```text
SHRINK_TO_BULK_MOLECULAR_PROGRAMS_WITH_DIRECTIONAL_CELLULAR_SPATIAL_SUPPORT
```

Final axis interpretation:

| Axis | Final role | Confidence | Allowed claim |
|---|---|---|---|
| F1 | skin-primary bulk molecular program | directional only | keratinocyte/spatial stress-inflammatory support |
| F2 | skin-primary bulk molecular program | directional only | keratinocyte/spatial stress-inflammatory support |
| F6 | skin-primary bulk molecular program | directional only | keratinocyte/spatial stress-inflammatory support |
| F7 | systemic/supportive candidate | low | not skin-spatial localized |

Important boundary:

```text
Do not formally name F1/F2/F6/F7 as genetically anchored mechanistic endotypes.
Do not use them as GWAS/MR/LAVA/coloc exposures.
```

Key reports:

| File | Role |
|---|---|
| `reports/PHASE2A_AXIS_MECHANISM_PRIORITIZATION.md` | axis triage and prioritization |
| `reports/PHASE2B_GSE228421_SINGLE_CELL_LOCALIZATION.md` | donor-level single-cell localization |
| `reports/PHASE2BR_GSE228421_REFINEMENT.md` | refined single-cell validation |
| `reports/PHASE2BR_2C_FINAL_TRANSCRIPTOMICS_VALIDATION_REPORT.md` | final transcriptomic validation decision |

### Phase 3A

Status:

```text
COMPLETE_NO_GO
```

Main conclusion:

Axis-specific psoriasis GWAS anchoring did not meet the predefined threshold. This result is now part of the manuscript logic because it justifies the shift from molecular-axis genetics to overall psoriasis comorbidity genetics.

Key report:

| File | Role |
|---|---|
| `reports/PHASE3A_PSORIASIS_GENETIC_ANCHORING.md` | axis-specific genetic anchoring decision |

### Phase 4A

Status:

```text
COMPLETE
```

Main conclusion:

Overall psoriasis susceptibility showed genome-wide genetic correlation with selected comorbidities. CAD was the cleanest non-neighbor systemic signal. PsA was treated as a positive-control/near-neighbor phenotype. Crohn disease and ulcerative colitis were retained as QC-flagged IBD signals with unusual negative global rg.

Key LDSC results:

| Outcome | Role | Global rg interpretation |
|---|---|---|
| CAD | primary systemic target | positive, FDR-supported, QC PASS |
| PsA | positive control | very high rg, near-neighbor/QC label |
| Crohn disease | IBD target | negative rg, QC-flagged |
| UC | IBD target | negative rg, QC-flagged |
| Stroke | reference | null/low-power |
| CKD | reference | null/low-power |

Not completed because primary GWAS access/source was unresolved:

```text
T2D
MASLD
MDD
uveitis
```

These must not be described as biological null outcomes.

Key report:

| File | Role |
|---|---|
| `reports/PHASE4A_LDSC_GENETIC_CORRELATION_REPORT.md` | genome-wide rg result |

### Phase 4B / 4B-R

Status:

```text
COMPLETE
```

Main conclusion:

Restricted LAVA supported a disease-specific local architecture:

| Outcome | Local architecture |
|---|---|
| CAD | multiple positive local rg loci; primary systemic route retained |
| PsA | strong positive-control sharing |
| Crohn disease | directionally heterogeneous, negative local architecture prominent |
| UC | directionally heterogeneous, mixed local architecture |

Phase 4B-R performed LD-reference validation of priority loci before Phase 4C. Only robust loci moved forward.

Key reports:

| File | Role |
|---|---|
| `reports/PHASE4B0_RG_SIGN_QC_ADJUDICATION.md` | CD/UC/PsA sign/QC adjudication |
| `reports/PHASE4B0_4B_RESTRICTED_LAVA_REPORT.md` | restricted LAVA report |
| `reports/PHASE4BR_LD_REFERENCE_VALIDATION_AND_PHASE4C_PREP_REPORT.md` | LD-reference validation and Phase 4C preparation |

### Phase 4C

Status:

```text
COMPLETE
```

Main conclusion:

SMR/HEIDI prioritized expression-linked genes in robust shared loci. This was treated as expression prioritization, not as causal MR.

Important boundary:

```text
SMR here is used for expression-linked prioritization.
It is not the same as broad causal MR.
```

Key reports:

| File | Role |
|---|---|
| `reports/PHASE4C_GTEX_V8_SMR_BESD_USABILITY_AUDIT.md` | GTEx BESD usability audit |
| `reports/PHASE4C_SMR1_RESTRICTED_SMR_HEIDI_REPORT.md` | restricted SMR/HEIDI |
| `reports/PHASE4C_SMR2_PROBE2MB_SENSITIVITY_REPORT.md` | probe-centered sensitivity |
| `reports/PHASE4C_FROZEN_SHARED_LOCUS_EQTL_GENE_TABLE_REPORT.md` | frozen gene table |
| `reports/PHASE4C_FINAL_MINI_MANUSCRIPT_SECTION_PACK.md` | manuscript-ready Phase 4C pack |

### Phase 4D

Status:

```text
COMPLETE_RESTRICTED_COLOC
```

Main conclusion:

Restricted Tier A coloc separated shared local architecture from shared eQTL causal-signal evidence.

Key coloc results:

| Outcome | Result | Interpretation |
|---|---|---|
| CAD | no PP4-supported Tier A pair | CAD remains architecture-level, not coloc-confirmed |
| CAD | UBQLN4/MEX3A skin signals suggestive | useful but below PP4 >= 0.80 |
| PsA | SLC22A5 and RP11-977G19.11 PP4-supported | positive-control validation |
| Crohn disease | SLC22A5 and PARK7 suggestive only | not coloc-confirmed |
| UC | RP11-973H7.1 colon-specific PP4-supported | high-value candidate with MAF-proxy sensitivity label |

Important IBD caveat:

```text
Crohn disease and UC coloc used eQTL MAF proxy because GWAS EAF was unavailable.
UC RP11-973H7.1 should remain sensitivity-labeled until EAF-complete reanalysis.
```

Key reports:

| File | Role |
|---|---|
| `reports/PHASE4D_COLOCALIZATION_INPUT_AUDIT_AND_SMOKE_TEST.md` | coloc input audit and smoke test |
| `reports/PHASE4D_RESTRICTED_TIERA_COLOC_FINAL_REPORT.md` | final restricted coloc report |
| `reports/PHASE4D_MANUSCRIPT_RESULTS_AND_DISCUSSION_UPDATE.md` | manuscript Results/Discussion update |

Key tables:

| File | Role |
|---|---|
| `results/phase4d_coloc/phase4d_restricted_coloc_tierA_all_results.tsv` | all restricted Tier A coloc results |
| `results/phase4d_coloc/manuscript_tables/phase4d_coloc_supported_and_suggestive_candidates.tsv` | PP4-supported and suggestive candidates |

### Phase 4E

Status:

```text
COMPLETE
```

Main conclusion:

Phase 4D PP4-supported or suggestive genes did not directly overlap the frozen F1/F2/F6/F7 CORE/EXTENDED molecular-axis gene programs.

This blocks a direct axis-to-coloc-gene claim.

Correct interpretation:

```text
Transcriptomic axes = contextual tissue-state layer
Overall psoriasis GWAS = genetic anchor
LDSC/LAVA/SMR/coloc = comorbidity genetics layer
```

Key report:

| File | Role |
|---|---|
| `reports/PHASE4E_TRANSCRIPTOMIC_CONTEXTUALIZATION_REPORT.md` | transcriptomic contextualization boundary |

Key tables:

| File | Role |
|---|---|
| `results/phase4e_contextualization/phase4e_coloc_candidate_axis_program_overlap.tsv` | coloc candidate vs axis program overlap |
| `results/phase4e_contextualization/phase4e_coloc_axis_overlap_summary.tsv` | overlap summary |

## Figure status

### Existing / ready figures

| Figure | Topic | Status |
|---|---|---|
| Figure 1 | study design and endotype-to-axis transition | existing |
| Figure 2 | axis prioritization and external replication | existing |
| Figure 3 | single-cell / spatial directional validation | existing / partly assembled |
| Figure 4 | Phase 3A axis-specific genetics NO-GO | existing as Phase 3A panels, may need renumbering |
| Figure 5 | Phase 4A/4B shared genetic architecture | generated |
| Figure 6 | Phase 4C SMR/HEIDI expression prioritization | generated |
| Figure 7 | Phase 4D/4E restricted coloc and contextualization | generated |

### Newly generated Figure 5

Files:

```text
results/figures/phase4a4b/Figure5_shared_genetic_architecture.svg
results/figures/phase4a4b/Figure5_shared_genetic_architecture.png
results/figures/phase4a4b/Figure5_shared_genetic_architecture.tiff
results/figures/phase4a4b/Figure5_shared_genetic_architecture.pdf
```

Report:

```text
reports/PHASE5_FIGURE5_SHARED_GENETIC_ARCHITECTURE_REPORT.md
```

Message:

Figure 5 shows genome-wide LDSC rg and restricted LAVA local architecture. It supports the shift from axis-specific genetic anchoring to overall psoriasis comorbidity genetics.

### Newly generated Figure 7

Files:

```text
results/figures/phase4d/Figure7_restricted_coloc_contextualization.svg
results/figures/phase4d/Figure7_restricted_coloc_contextualization.png
results/figures/phase4d/Figure7_restricted_coloc_contextualization.tiff
results/figures/phase4d/Figure7_restricted_coloc_contextualization.pdf
```

Report:

```text
reports/PHASE5_FIGURE7_RESTRICTED_COLOC_CONTEXTUALIZATION_REPORT.md
```

Message:

Figure 7 shows that restricted coloc recovered positive-control PsA signals and a sensitivity-labeled UC colon candidate, while CAD lacks PP4-supported eQTL coloc and molecular axes remain contextual layers.

### Figure export caveat

For Figures 5 and 7, static preflight and PNG visual QA passed. The automated PDF text audit flagged Cairo PDF `Tf=1` font encoding, likely due to PDF font-transform representation. Preferred production route:

```text
Use SVG for editable vector assembly.
Use TIFF for raster submission/export if needed.
Use PDF only after downstream layout software confirms text scaling.
```

## Manuscript spine

Current manuscript assembly file:

```text
reports/PHASE5_MANUSCRIPT_SPINE_AND_FIGURE_MAP.md
```

Recommended Results order:

1. Discrete endotypes were unstable, supporting continuous axes.
2. F1/F2/F6/F7 were prioritized with controlled claim strength.
3. Single-cell and spatial analyses gave directional cellular/spatial support.
4. Axis-specific genetic anchoring failed predefined criteria.
5. Overall psoriasis susceptibility showed selected comorbidity-level genetic sharing.
6. SMR/HEIDI prioritized expression-linked genes in robust shared loci.
7. Restricted coloc separated shared local architecture from shared eQTL causal-signal evidence.
8. Transcriptomic axes contextualized tissue biology but did not explain coloc genes by direct membership.

## Current claim boundaries

Allowed claims:

```text
Continuous molecular axes are more reproducible than discrete k=2 endotypes.
F1/F2/F6 have directional keratinocyte/spatial stress-inflammatory support.
F7 is a supportive systemic candidate.
Overall psoriasis susceptibility shares genetic architecture with selected outcomes.
CAD is the cleanest non-neighbor systemic shared-architecture signal.
PsA validates the genetic pipeline as a near-neighbor positive control.
IBD shows local directional heterogeneity.
UC RP11-973H7.1 is a high-value colon-specific coloc candidate under MAF-proxy sensitivity.
```

Blocked claims:

```text
F1/F2/F6/F7 are genetically anchored endotypes.
Any molecular axis mediates psoriasis-CAD/IBD/PsA genetic sharing.
CAD has a PP4-supported eQTL coloc gene.
UC RP11-973H7.1 is definitive without EAF-complete sensitivity.
SMR/HEIDI proves causality.
Broad MR should begin now.
T2D/MASLD/MDD/uveitis are null outcomes.
```

## Next best action

The next step should be manuscript assembly, not more discovery analysis.

Recommended next task:

```text
PHASE6_FULL_MANUSCRIPT_DRAFT_ASSEMBLY
```

Suggested immediate subtasks:

1. Compile Table 1: dataset and analysis-layer provenance.
2. Compile Table 2: frozen molecular axes and final confidence.
3. Compile Table 3: Phase 4D coloc-supported/suggestive candidates.
4. Assemble Figures 1-7 into final manuscript numbering.
5. Draft full BMC-style manuscript sections: Title, Abstract, Background, Methods, Results, Discussion, Conclusions.
6. Keep citations from the existing Phase 4C bibliography and add only verified references as needed.

Still not recommended:

```text
MR
new transcriptomics cohort hunting
axis-specific genetics rescue
drug prediction
PPI / hub gene / LASSO
post-hoc replacement of GWAS outcomes based on significance
```

