# PHASE 2B-R + 2C Stop-Rule Roadmap

更新日期：2026-08-11

## Executive Decision

当前不直接进入 GWAS，也不继续在 GSE228421 上无限精修。项目进入一个有限的 **Phase 2B-R + Phase 2C** transcriptomic validation block：

```text
Phase 2B complete
GSE228421 low-confidence directional clues
        ↓
Phase 2B-R
one-pass high-resolution refinement of GSE228421
        ↓
Phase 2C
independent spatial validation using GSE202011
and, if available as a separate accession/resource,
independent psoriasis scRNA validation from the Ma et al. atlas
        ↓
Stop adding transcriptomic datasets
        ↓
Mechanism freeze v2
        ↓
Phase 3 genetics only after frozen programs and mechanism boundary are accepted
```

The central rule is simple:

> Phase 2B-R and Phase 2C are the final transcriptomics rescue/validation block. After this block, the project either upgrades selected axes to mechanistic axes or permanently shrinks them to bulk molecular axes with directional cellular clues.

## Why This Change Is Needed

GSE228421 provides useful but low-confidence evidence:

- F1, F2, and F6 all show positive keratinocyte LS-vs-NL donor-level effects.
- F6 has the strongest directional effect among the skin axes.
- F7 does not show clear skin myeloid/IFN localization and should remain a systemic/supportive axis.
- All four axes remain LOW confidence because donor-level FDR thresholds are not met with 5 donors.

This pattern is not a complete failure of cellular signal, but it is not enough for formal mechanism naming. Repeatedly subdividing the same 5 donors would create overfitting risk. The next step must be limited, externally anchored, and governed by stopping rules.

## Phase 2B-R: One-Pass GSE228421 Refinement

### Objective

Re-test frozen F1/F2/F6/F7 CORE programs in more biologically meaningful cell states, without rediscovering axes or changing gene programs.

### Allowed Refinement

Only the following compartments may be refined:

| Compartment | Allowed states |
|---|---|
| Keratinocyte | basal, spinous/suprabasal, proliferative, inflammatory, IFN-response, stress/hypoxia |
| Fibroblast | inflammatory, homeostatic/stromal |
| Myeloid | monocyte/macrophage/DC |
| T/NK | coarse T, NK, cytotoxic/Tc17-like enough to assess F7 |

### Not Allowed

- No new clustering intended to create a better story.
- No changing F1/F2/F6/F7 CORE genes.
- No switching CORE and EXTENDED based on which looks better.
- No GWAS/MR/LDSC/LAVA/coloc.
- No drug prediction, PPI, hub gene, or LASSO.

### Stop Rule

GSE228421 refinement is run once. If the result remains LOW confidence, this dataset is no longer used for rescue.

## Phase 2C: Independent Validation

### GSE202011 Spatial Validation

Local and GEO audit show that GSE202011 is a spatial transcriptomics dataset, not the primary 67,378-cell scRNA dataset itself.

Audited local/GEO properties:

- GEO accession: GSE202011.
- Title: spatial transcriptomics stratifies psoriatic disease by emergent cellular ecosystems.
- Samples: 30.
- Groups in local series matrix:
  - Healthy: 7.
  - PSO lesional: 7.
  - PSO non-lesional: 5.
  - PSA lesional: 7.
  - PSA non-lesional: 4.
- GEO supplementary files:
  - `GSE202011_RAW.tar`, custom H5 files.
  - `GSE202011_st_images.tar.gz`, spatial tissue images.

Therefore, GSE202011 should be used as independent spatial/compartment validation and not mislabeled as the independent scRNA atlas unless matching scRNA objects are obtained from the original study or an associated repository/accession.

### Independent scRNA Validation

The Ma et al. Nature Communications study reported single-cell and spatial sequencing in psoriasis and described keratinocyte differentiation layers, inflammatory fibroblast states, myeloid/T-cell compartments, and spatial localization of inflammatory programs. It is biologically well aligned with the current axes, but its scRNA data source must be handled as its own dataset/resource rather than assumed to be identical to GSE202011.

Action before analysis:

1. Identify the exact scRNA accession or processed object for the Ma et al. atlas.
2. Audit sample-level metadata, donor counts, disease states, and whether donor-level statistics are possible.
3. Only then score frozen CORE programs and summarize by donor x cell state.

## Axis-Specific Handling

| Axis | Current status after GSE228421 | Phase 2B-R/2C question | Rule after validation |
|---|---|---|---|
| F1 | keratinocyte directional clue, LOW confidence | basal IFN/stress vs suprabasal inflammatory/metabolic keratinocyte state | Upgrade only if independent scRNA/spatial state localization is coherent |
| F2 | keratinocyte directional clue, not stromal in GSE228421 | keratinocyte vs fibroblast/stromal/endothelial in independent data | If still keratinocyte, abandon stromal naming |
| F6 | strongest keratinocyte directional clue | stress/hypoxia/inflammatory keratinocyte state | Highest priority for mechanism upgrade |
| F7 | skin NK/B-cell directional clue; blood support stronger | exploratory skin immune signal; true validation should be PBMC/systemic atlas | Lack of skin localization is not failure |

## Upgrade Criteria

An axis can be upgraded to a mechanistic axis only if it meets all of the following:

1. Stable bulk axis in E-MTAB-14509.
2. Independent bulk support, especially GSE244679 for skin axes or GSE61281 for F7.
3. At least one independent single-cell dataset with donor-level coherent localization.
4. Localization resolves to a cell state, not only a broad cell type.
5. CORE and EXTENDED are directionally consistent.
6. The cell-state interpretation is concordant with pre-frozen pathway/regulon biology.

If these criteria are met:

```text
mechanism confidence = MODERATE/HIGH
```

## Shrink Criteria

An axis remains a bulk molecular axis if:

- GSE228421 remains only directional.
- Independent scRNA does not resolve a coherent cell state.
- Spatial evidence is diffuse or inconsistent.
- CORE and EXTENDED disagree in direction or state.

If this happens, the permanent wording is:

> bulk tissue molecular axis with directional cellular clues

No third or fourth transcriptomic dataset should be added to rescue the axis.

## When Genetics Can Start

Genetics does not require all axes to become perfect cell-state mechanisms. A reasonable Phase 3 entry state could be:

```text
F6 = strong or moderate mechanistic axis
F1 = moderate mechanistic axis or replicated bulk axis
F2 = replicated bulk molecular axis
F7 = systemic blood-supported axis
```

The non-negotiable requirement is that all gene programs remain frozen before genetics. GWAS/MR results must not be used to revise F1/F2/F6/F7 gene programs or rename axes post hoc.

## Updated Claim Boundary

Allowed after current Phase 2B:

- F1/F2/F6 show directional keratinocyte clues in GSE228421.
- F6 is the strongest candidate for mechanism upgrade.
- F2 must be re-tested without assuming stromal identity.
- F7 remains systemic/supportive and should not be forced to prove itself in skin.

Not allowed:

- Confirmed keratinocyte mechanism.
- Confirmed fibroblast/stromal F2.
- Confirmed myeloid/IFN F7 in skin.
- Genetics or comorbidity claims before mechanism freeze v2.

## Generated Local Audit Files

- `results/phase2br_2c/GSE202011_spatial_sample_audit.tsv`
- `results/phase2br_2c/GSE202011_spatial_sample_summary.tsv`

## Primary Source Notes

- GEO GSE202011 confirms the spatial transcriptomics design, 30 samples, H5 supplementary files, ST images, and integration with publicly available scRNA-seq datasets.
- The Nature Communications psoriasis single-cell/spatial paper supports the biological rationale for testing keratinocyte layers, inflammatory fibroblast states, and spatial inflammatory compartments, but its exact scRNA data accession must be audited before being treated as an independent single-cell validation set.
