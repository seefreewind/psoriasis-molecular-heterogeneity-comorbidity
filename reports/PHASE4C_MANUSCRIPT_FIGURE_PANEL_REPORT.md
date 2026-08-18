# Phase 4C Manuscript Figure Panel Report

Date: 2026-08-16

## Figure decision

The Phase 4C shared-locus eQTL prioritization figure is ready for manuscript drafting.

Core conclusion:

> Robust local psoriasis-comorbidity genetic-sharing loci resolve into a stable eQTL-prioritized regulatory-gene layer, with CAD as the clearest systemic track, PsA as a positive-control track, and IBD retaining local-direction heterogeneity.

## Figure files

- SVG: `/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/figures/phase4c/Figure_Phase4C_shared_locus_eqtl_prioritization.svg`
- TIFF: `/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/figures/phase4c/Figure_Phase4C_shared_locus_eqtl_prioritization.tiff`
- PNG preview: `/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/figures/phase4c/Figure_Phase4C_shared_locus_eqtl_prioritization.png`
- PDF export: `/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/figures/phase4c/Figure_Phase4C_shared_locus_eqtl_prioritization.pdf`
- R source: `/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/src/figures/phase4c_make_shared_locus_eqtl_panel.R`
- QA notes: `/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/figures/phase4c/Figure_Phase4C_shared_locus_eqtl_prioritization_QA.tsv`

## Source data

Source data were exported for each panel:

- Panel a: `/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/figures/phase4c/source_data/figure_phase4c_panel_a_tier_counts.tsv`
- Panel b: `/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/figures/phase4c/source_data/figure_phase4c_panel_b_cad_tierA.tsv`
- Panel c: `/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/figures/phase4c/source_data/figure_phase4c_panel_c_ibd_direction.tsv`
- Panel d: `/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/figures/phase4c/source_data/figure_phase4c_panel_d_smr_stability.tsv`

## Panel logic

| Panel | Claim | Data layer |
|---|---|---|
| a | The frozen Phase 4C table contains 91 eQTL-prioritized genes and separates evidence tiers across outcomes. | Frozen shared-locus eQTL gene table |
| b | CAD has recurrent Tier A candidates within robust positive local-rg loci. | CAD Tier A recurrent SMR2 genes |
| c | Crohn and UC retain both positive and negative local-rg candidate-gene architecture. | IBD candidate genes by local-rg direction and recurrent support |
| d | Probe-centered ±2Mb SMR2 sensitivity preserved the SMR1 gene-level result. | SMR1 versus SMR2 primary-signal counts |

## QA status

- R backend was used for all plotting, previewing and export.
- Source preflight: 0 FAIL.
- R parse: PASS.
- R render: PASS with no warnings after final patch.
- PNG visual inspection: PASS; no blank panels or major label collisions.
- Raster export: TIFF at 600 dpi and PNG preview at 300 dpi.
- PDF glyph audit: the `cairo_pdf` export is auditable but the automated checker reports 1 pt text runs because the R Cairo device stores text with transform scaling. The rendered PNG/SVG visual inspection and source-level font preflight support adequate text size. For final journal upload, prefer SVG/TIFF unless a PDF is specifically required and manually inspect the PDF in the target submission system.

## Draft legend

**Figure X. Shared-locus eQTL prioritization of psoriasis-comorbidity genetic architecture.**

**a,** Frozen Phase 4C gene table summarized by outcome and evidence tier. Tier A denotes Phase 4B-R Tier 1 loci with recurrent SMR2 support across at least two GTEx tissues. B1, B2 and C denote progressively weaker combinations of local-locus tier and tissue recurrence. **b,** CAD Tier A recurrent candidate genes ranked by global SMR FDR. Point labels indicate the number of supporting tissues. **c,** Crohn disease and ulcerative colitis candidate genes stratified by positive or negative local genetic-correlation direction; red indicates recurrent tissue support and grey indicates single-tissue support. **d,** Sensitivity comparison between the original LAVA-locus-restricted SMR1 analysis and the probe-centered ±2 Mb SMR2 analysis. SMR2 retained all primary `outcome + gene` candidates and 98.9% of primary `outcome + tissue + gene` candidates.

Statistics: SMR2 primary signals were defined as global SMR FDR < 0.05 with HEIDI pass (`p_HEIDI > 0.01` or unavailable). These results prioritize eQTL-linked candidate regulatory genes within robust shared local genetic regions and do not establish formal colocalization or causal mediation.

## Next step

Recommended next task:

`PHASE4C_RESULTS_TEXT_AND_TABLE_INTEGRATION`

This should write the Results subsection around:

1. CAD as the primary systemic track.
2. PsA as positive-control / near-neighbor evidence.
3. IBD as local-direction heterogeneity.
4. SMR2 as sensitivity support rather than formal colocalization.
