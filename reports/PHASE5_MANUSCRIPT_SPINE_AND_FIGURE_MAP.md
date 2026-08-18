# Phase 5 Manuscript Spine and Figure Map

Date: 2026-08-16

## Current manuscript decision

The project should now move from analysis expansion to manuscript assembly.

Frozen spine:

```text
Reproducible psoriasis tissue molecular heterogeneity
    + overall psoriasis multisystem shared genetic architecture
    + restricted shared-locus/eQTL prioritization
    + transcriptomic contextualization without axis-specific genetic claims
```

Do not return to:

```text
discrete endotype rescue
axis-specific LDSC/LAVA/MR/coloc
broad unrestricted MR
drug prediction
PPI/hub-gene analysis
```

## Working title options

Preferred:

```text
Tissue molecular programs and shared genetic architecture of psoriasis comorbidity
```

Alternative:

```text
Layered transcriptomic and genetic evidence for multisystem comorbidity architecture in psoriasis
```

More conservative:

```text
Transcriptomic heterogeneity and shared comorbidity genetics in psoriasis
```

## Central claim

Psoriasis contains reproducible tissue-level molecular programs that are directionally supported by single-cell and spatial transcriptomics, but these programs are not genetically anchored as axis-specific GWAS signals. Overall psoriasis susceptibility, rather than individual molecular axes, shows shared genetic architecture with selected comorbidities, especially CAD and psoriatic disease, with local and eQTL analyses separating architecture-level sharing from coloc-supported causal-signal evidence.

## Abstract skeleton

### Background

Psoriasis is associated with inflammatory, cardiovascular and gastrointestinal comorbidities, but the relationship between tissue molecular heterogeneity and shared genetic susceptibility remains unclear.

### Methods

We integrated bulk transcriptomic factor modeling, external skin replication, donor-level single-cell and spatial transcriptomic validation, psoriasis GWAS enrichment tests, genome-wide and local genetic-correlation analyses, SMR/HEIDI expression prioritization, and restricted GTEx v8 eQTL colocalization.

### Results

Discrete transcriptomic endotypes were unstable, whereas continuous molecular axes were more reproducible. F1, F2 and F6 were retained as skin-primary bulk molecular programs with directional keratinocyte/spatial stress-inflammatory support, and F7 was retained as a systemic supportive program. Axis-specific genetic anchoring failed predefined criteria. Overall psoriasis susceptibility showed comorbidity-level shared genetic architecture, with CAD emerging as the cleanest non-neighbor systemic target. Restricted eQTL colocalization recovered strong positive-control PsA signals and a UC colon-specific RP11-973H7.1 candidate under an EAF-limited sensitivity framework, but no PP4-supported CAD gene-tissue pair.

### Conclusions

The study supports a layered model in which transcriptomic axes describe psoriasis tissue-state heterogeneity, while overall psoriasis susceptibility captures shared comorbidity genetics. This framework avoids overinterpreting molecular axes as genetic exposures and distinguishes shared local architecture from coloc-supported eQTL mechanisms.

## Results section map

### Result 1. Discrete endotypes were unstable, supporting a continuous-axis framework

Job:

```text
Explain why the study moved away from k=2 endotypes.
```

Main evidence:

| Evidence | Source |
|---|---|
| Phase 1 endotype GO/NO-GO | `reports/PHASE1_ENDOTYPE_GO_NOGO_REPORT.md` |
| continuous molecular-axis report | `reports/PHASE1B_MOLECULAR_AXIS_REPORT.md` |

Display:

| Figure/Table | Status |
|---|---|
| Figure 1A study flow | exists |
| Figure 1B patient/tissue structure | exists |
| Figure 1C latent scatter | exists |

### Result 2. F1/F2/F6/F7 were prioritized as frozen molecular programs with controlled claim strength

Job:

```text
Show how axes were triaged and why only a small set carried forward.
```

Main evidence:

| Evidence | Source |
|---|---|
| Phase 2A prioritization matrix | `reports/PHASE2A_AXIS_MECHANISM_PRIORITIZATION.md` |
| F1/F2/F6 skin-primary and F7 systemic/supportive decision | `results/phase2a/Table_axis_prioritization_master.tsv` |

Display:

| Figure/Table | Status |
|---|---|
| Figure 2A axis evidence matrix | exists |
| Figure 2B retained axis gene programs | exists |
| Figure 2C tissue contribution | exists |
| Figure 2D external replication support | exists |
| Figure 2E primary axis schematic | exists |

### Result 3. Single-cell and spatial analyses supported directional keratinocyte/spatial programs but not formal mechanism naming

Job:

```text
Anchor the axes at tissue/cell-state level while keeping confidence bounded.
```

Main evidence:

| Evidence | Source |
|---|---|
| GSE228421 donor-level single-cell localization | `reports/PHASE2B_GSE228421_SINGLE_CELL_LOCALIZATION.md` |
| GSE228421 refined validation | `reports/PHASE2BR_GSE228421_REFINEMENT.md` |
| GSE173706 and spatial validation | `reports/PHASE2BR_2C_FINAL_TRANSCRIPTOMICS_VALIDATION_REPORT.md` |

Display:

| Figure/Table | Status |
|---|---|
| Figure3A GSE228421 axis cell-type localization | exists |
| Figure3B donor paired effects | exists |
| Table mechanism triangulation | exists |

Required wording:

```text
directional cellular/spatial support
not formal MODERATE/HIGH mechanism naming
```

### Result 4. Axis-specific genetic anchoring failed predefined criteria

Job:

```text
Explain why F1/F2/F6/F7 exit the genetics main analysis.
```

Main evidence:

| Evidence | Source |
|---|---|
| Phase 3A genetic anchoring | `reports/PHASE3A_PSORIASIS_GENETIC_ANCHORING.md` |
| axis genetic anchoring table | `results/phase3a/Table_axis_genetic_anchoring.tsv` |

Display:

| Figure/Table | Status |
|---|---|
| Figure6A genetic anchoring design | exists |
| Figure6B axis enrichment | exists |
| Figure6F shared vs axis-specific | exists |

Required conclusion:

```text
NO-GO_FOR_GENETICALLY_ANCHORED_AXES
```

### Result 5. Overall psoriasis susceptibility showed selected comorbidity-level shared genetic architecture

Job:

```text
Reposition genetics around overall psoriasis susceptibility and comorbid outcomes.
```

Main evidence:

| Evidence | Source |
|---|---|
| Phase 4A LDSC report | `reports/PHASE4A_LDSC_GENETIC_CORRELATION_REPORT.md` |
| Phase 4B0 sign/QC adjudication | `reports/PHASE4B0_RG_SIGN_QC_ADJUDICATION.md` |
| restricted LAVA report | `reports/PHASE4B0_4B_RESTRICTED_LAVA_REPORT.md` |
| LD-reference validation | `reports/PHASE4BR_LD_REFERENCE_VALIDATION_AND_PHASE4C_PREP_REPORT.md` |

Main interpretation:

```text
CAD is the primary clean non-neighbor systemic signal.
PsA is a positive-control / near-neighbor sensitivity phenotype.
IBD is local-direction heterogeneous.
```

### Result 6. SMR/HEIDI prioritized expression-linked genes in robust shared loci

Job:

```text
Add gene/tissue hypotheses without calling them coloc-confirmed.
```

Main evidence:

| Evidence | Source |
|---|---|
| GTEx BESD audit | `reports/PHASE4C_GTEX_V8_SMR_BESD_USABILITY_AUDIT.md` |
| SMR1 report | `reports/PHASE4C_SMR1_RESTRICTED_SMR_HEIDI_REPORT.md` |
| SMR2 sensitivity | `reports/PHASE4C_SMR2_PROBE2MB_SENSITIVITY_REPORT.md` |
| frozen gene table | `reports/PHASE4C_FROZEN_SHARED_LOCUS_EQTL_GENE_TABLE_REPORT.md` |

Display:

| Figure/Table | Status |
|---|---|
| Figure Phase4C shared locus eQTL prioritization | exists |
| phase4c main CAD Tier A gene table | exists |
| phase4c PsA positive-control gene table | exists |
| phase4c IBD direction-heterogeneity gene table | exists |

### Result 7. Restricted coloc separated shared local architecture from shared eQTL causal-signal evidence

Job:

```text
Show what survived the stricter coloc layer and where evidence stops.
```

Main evidence:

| Evidence | Source |
|---|---|
| coloc input audit | `reports/PHASE4D_COLOCALIZATION_INPUT_AUDIT_AND_SMOKE_TEST.md` |
| final restricted coloc report | `reports/PHASE4D_RESTRICTED_TIERA_COLOC_FINAL_REPORT.md` |
| manuscript update | `reports/PHASE4D_MANUSCRIPT_RESULTS_AND_DISCUSSION_UPDATE.md` |

Main result:

| Outcome | Coloc conclusion |
|---|---|
| CAD | no PP4-supported Tier A pair; UBQLN4/MEX3A suggestive only |
| PsA | strong positive-control PP4 signals for SLC22A5 and RP11-977G19.11 |
| Crohn disease | suggestive only; MAF-proxy sensitivity |
| UC | RP11-973H7.1 colon-specific PP4 support; MAF-proxy sensitivity |

Needed display:

```text
New small Figure 7 or Table 2 summarizing PP4-supported/suggestive coloc findings.
```

### Result 8. Transcriptomic axes contextualized tissue biology but did not explain coloc genes by direct membership

Job:

```text
Integrate transcriptomics and genetics without circular interpretation.
```

Main evidence:

| Evidence | Source |
|---|---|
| Phase 4E contextualization | `reports/PHASE4E_TRANSCRIPTOMIC_CONTEXTUALIZATION_REPORT.md` |
| coloc-axis overlap table | `results/phase4e_contextualization/phase4e_coloc_candidate_axis_program_overlap.tsv` |

Main result:

```text
No PP4-supported/suggestive Phase 4D candidate directly overlapped F1/F2/F6/F7 CORE/EXTENDED gene programs.
```

Required conclusion:

```text
Axes are contextual transcriptomic layers, not genetic exposures.
```

## Main figure map

| Figure | Current role | Status | Action |
|---|---|---|---|
| Figure 1 | Study design and shift from discrete endotypes to continuous axes | mostly exists | assemble panels |
| Figure 2 | Axis prioritization and external replication | exists | assemble panels |
| Figure 3 | single-cell/spatial directional validation | partly exists | may need one combined spatial panel |
| Figure 4 | Phase 3A NO-GO for axis-specific genetics | exists as Figure6 panels | renumber and compress |
| Figure 5 | Phase 4A/4B shared comorbidity genetics | needs assembly from existing tables | likely required |
| Figure 6 | Phase 4C SMR/HEIDI expression prioritization | exists | use current Phase4C panel |
| Figure 7 | Phase 4D/4E coloc and contextualization | missing | create compact summary panel/table |

## Main table map

| Table | Content | Source |
|---|---|---|
| Table 1 | datasets and analysis layers | compile from all phase reports |
| Table 2 | frozen molecular axes and final confidence | `results/phase2c/Table_mechanism_triangulation.tsv` |
| Table 3 | Phase 4D coloc-supported/suggestive candidates | `results/phase4d_coloc/manuscript_tables/phase4d_coloc_supported_and_suggestive_candidates.tsv` |

## Supplementary table map

| Supplementary table | Content |
|---|---|
| Supplementary Table 1 | dataset provenance and sample metadata |
| Supplementary Table 2 | Phase 2A axis prioritization matrix |
| Supplementary Table 3 | frozen axis gene programs |
| Supplementary Table 4 | single-cell donor-level statistics |
| Supplementary Table 5 | spatial validation statistics |
| Supplementary Table 6 | Phase 3A axis-specific genetic anchoring tests |
| Supplementary Table 7 | Phase 4A LDSC rg and QC |
| Supplementary Table 8 | Phase 4B LAVA local rg |
| Supplementary Table 9 | Phase 4B-R LD-reference validation |
| Supplementary Table 10 | Phase 4C SMR/HEIDI all results |
| Supplementary Table 11 | Phase 4D restricted coloc all results |
| Supplementary Table 12 | Phase 4E coloc-axis overlap audit |

## Methods structure

Recommended BMC-style Methods order:

1. Study design and analysis overview.
2. Bulk transcriptomic preprocessing and latent factor modeling.
3. External bulk skin and blood replication.
4. Axis prioritization and frozen gene-program construction.
5. Donor-level single-cell localization.
6. Spatial transcriptomic validation.
7. Axis-specific GWAS enrichment and predefined NO-GO criteria.
8. GWAS outcome selection and harmonization.
9. LDSC genome-wide genetic correlation.
10. Restricted LAVA local genetic correlation and LD-reference validation.
11. GTEx v8 SMR/HEIDI expression prioritization.
12. Restricted GTEx v8 eQTL colocalization.
13. Transcriptomic contextualization and overlap audit.
14. Multiple-testing and decision thresholds.

## Discussion structure

Recommended Discussion jobs:

1. Open with the final model: transcriptomic heterogeneity and genetic comorbidity sharing are complementary layers.
2. Interpret the failure of discrete endotypes and the value of continuous axes.
3. Discuss why directional cell/spatial support is useful but not enough for formal mechanism naming.
4. Explain the Phase 3A NO-GO and why overall psoriasis GWAS became the correct genetic anchor.
5. Discuss CAD as the cleanest systemic shared-architecture signal, with no strong CAD coloc gene.
6. Discuss PsA as positive control and IBD as local-direction heterogeneous, with UC RP11-973H7.1 as sensitivity-labeled.
7. State strengths: multi-layer stop rules, independent replication, donor-level statistics, strict evidence hierarchy.
8. State limitations: public-data integration, GTEx tissue limits, EAF-limited IBD coloc, no clinical validation, no causal MR yet.
9. Close with the value of a layered framework.

## Remaining work before full manuscript draft

Required:

1. Build Figure 5 for Phase 4A/4B shared genetic architecture.
2. Build Figure 7 or Table 3 for Phase 4D/4E coloc/contextualization.
3. Compile Table 1 dataset/analysis-layer provenance.
4. Decide target journal and exact word/table/figure limits.

Not required now:

1. MR.
2. Additional transcriptomic cohort hunting.
3. More axis-specific genetic tests.
4. Drug/PPI/hub-gene analysis.

## Current GO decision

```text
GO_TO_MANUSCRIPT_ASSEMBLY
CONDITIONAL_GO_TO_TARGETED_FIGURE_COMPLETION
NO_GO_TO_BROAD_MR
```

