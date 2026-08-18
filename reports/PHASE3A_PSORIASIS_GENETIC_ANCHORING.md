# PHASE 3A Psoriasis Genetic Anchoring

## Executive Conclusion

**NO-GO for "genetically anchored axes".** Frozen F1/F2/F6/F7 CORE programs did not show robust MHC-excluded psoriasis GWAS enrichment in MAGMA competitive gene-set analysis. F2 showed the closest signal, but it remained non-significant after FDR in CORE analysis and was not supported as a robust axis-specific genetic anchor by matched-null or conditional analyses.

This does not invalidate the transcriptomic axes. The correct interpretation is that these replicated psoriasis molecular programs are not detectably explained by distinct germline psoriasis susceptibility components under the current Phase 3A design.

## Frozen Transcriptomic Inputs

- Axes tested: F1, F2, F6, F7.
- CORE programs were primary.
- EXTENDED programs were sensitivity only.
- Gene membership was read from `results/phase2a/axis_gene_programs/` and was not modified.
- Mechanism boundary remained: bulk molecular axes with directional cellular/spatial support, not validated cell-state mechanisms.

## GWAS Audit

- Primary GWAS: GCST90472771.
- Phenotype: psoriasis susceptibility.
- Publication: Dand et al., Nature Communications, 2025.
- DOI: 10.1038/s41467-025-56719-8.
- Ancestry: European.
- Cases/controls: 36,466 / 458,078.
- Genome build: GRCh37, 1-based coordinates.
- Raw summary statistics: GWAS-SSF v1.0, not harmonised.
- Official MD5 matched local checksum.
- Variant count: 11,808,957, matching GWAS Catalog REST metadata.

## Gene Mapping

Fixed annotation: MAGMA `NCBI37.3.gene.loc`, protein-coding genes, GRCh37. Primary SNP-to-gene window: gene body only.

| Axis | CORE genes | Mapped | MHC genes | Primary tested genes |
|---|---:|---:|---:|---:|
| F1 | 304 | 257 | 1 | 256 |
| F2 | 725 | 705 | 5 | 700 |
| F6 | 134 | 129 | 1 | 128 |
| F7 | 232 | 214 | 1 | 213 |

## MHC Strategy

MHC was prespecified as GRCh37 chr6:25,000,000-34,000,000.

Primary analysis excluded MHC genes and MHC-region SNPs. This excluded 266 genes from the MAGMA annotation and 77,107 mapped SNPs from the p-value input. MHC-included MAGMA gene-level analysis was attempted but became computationally dominated by chr6/MHC and was stopped. The MHC-included sensitivity is therefore reported as not estimable, rather than replaced with a post-hoc shortcut.

## MAGMA Results

Primary CORE/MHC-excluded competitive MAGMA:

| Axis | Tested genes | Beta | SE | P | FDR | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| F1 | 252 | -0.0538 | 0.0613 | 0.810 | 0.810 | not significant |
| F2 | 674 | 0.0519 | 0.0392 | 0.0929 | 0.372 | not significant |
| F6 | 128 | 0.0423 | 0.0810 | 0.301 | 0.401 | not significant |
| F7 | 203 | 0.0443 | 0.0692 | 0.261 | 0.401 | not significant |

EXTENDED sensitivity did not rescue the result. F2 EXTENDED was nominal (P=0.044) but not FDR-significant and cannot override CORE.

## Matched-Null Analysis

2,000 matched random gene sets were generated per axis, matched on gene-set size, chromosome, gene length bins, and SNP-density bins.

| Axis | Observed beta | Null mean | Empirical P |
|---|---:|---:|---:|
| F1 | -0.0538 | -0.0006 | 0.822 |
| F2 | 0.0519 | 0.0048 | 0.0915 |
| F6 | 0.0423 | 0.0140 | 0.356 |
| F7 | 0.0443 | -0.0118 | 0.201 |

No axis reached empirical support.

## Axis Overlap

CORE overlap was moderate for some pairs but did not explain a positive shared genetic signal. The shared-by-two-or-more component was not enriched (P=0.560).

## Conditional/Unique-Gene Analyses

Conditional MAGMA adjusting each axis for the other three CORE axes remained non-significant:

| Axis | Conditional P |
|---|---:|
| F1 | 0.913 |
| F2 | 0.0646 |
| F6 | 0.286 |
| F7 | 0.278 |

F2 unique genes showed nominal sensitivity evidence (P=0.046), but this is not primary evidence because CORE was non-significant and matched-null support remained weak.

## S-LDSC

S-LDSC was not run in Phase 3A. It was classified as inconclusive because the local baselineLD model was not available, the primary MAGMA result was negative, and running S-LDSC would not be appropriate as a rescue analysis.

## Genetic Evidence Tiers

All axes are **Tier D: no detectable genetic anchoring** under Phase 3A.

## Candidate Genes For Phase 3B

`results/phase3a/phase3b_candidate_genes.tsv` records top CORE gene-level MAGMA signals per axis for future review only. These are not colocated, not causal, and not promoted into Phase 3B because the axes did not pass genetic anchoring.

## Negative Findings

- No CORE axis reached FDR significance.
- Matched random sets performed similarly to observed axes.
- Conditional models did not reveal axis-specific signal.
- Shared CORE genes did not show enrichment.
- EXTENDED-only nominal signal was not used to rescue an axis.

## Reviewer Attack Points

1. Gene sets are large, especially F2, but MAGMA conditioned on gene size, gene density, sample size, and inverse MAC; matched null also controlled gene-set size and gene-level properties.
2. Results were not driven by MHC in the primary analysis because MHC was excluded before enrichment testing.
3. Results were not driven by shared inflammatory genes; the shared component was not enriched.
4. Gene length/SNP density were addressed by MAGMA internal covariates and matched nulls.
5. F2 had the largest CORE set and the closest signal, but FDR and empirical null were not significant.
6. F6 was smaller and lower powered, but no sensitivity analysis upgraded it.
7. S-LDSC was not used as rescue evidence.
8. CORE/EXTENDED were not fully concordant; EXTENDED F2 was nominal only.
9. Transcriptomic axes were frozen before genetics.
10. No axis program was altered after GWAS results.

## Limitations

- GCST90472771 lacks rsID, EAF, and INFO columns; chr:position:allele mapping to g1000_eur recovered 88.343% of variants.
- MHC-included MAGMA sensitivity was not estimable in this run because full chr6/MHC gene-level computation stalled.
- Gene-level association does not identify causal genes.
- S-LDSC was not attempted because baselineLD reference setup was not locally available and primary MAGMA was negative.

## Phase 3B Recommendation

Do not proceed to eQTL colocalization or Phase 3B regulatory anchoring as an axis-specific program. If the project continues, it should pivot to a narrower claim: replicated psoriasis molecular axes with overall psoriasis genetic architecture assessed separately.

## Phase 4 Comorbidity Readiness

Do not enter axis-specific multisystem comorbidity genetics. The project can later consider overall psoriasis/comorbidity shared genetics, but not as F1/F2/F6/F7 genetically anchored axis architecture.

## GO / CONDITIONAL GO / NO-GO

**NO-GO FOR "GENETICALLY ANCHORED AXES".**

