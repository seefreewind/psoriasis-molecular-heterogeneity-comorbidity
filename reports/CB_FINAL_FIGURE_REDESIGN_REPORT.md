# Communications Biology Final Figure Redesign Report

## Figure 1
- Changes made: rebuilt as a study-decision figure with data architecture, tissue availability, k = 2 stability and transition to continuous programs.
- Panels retained: study/sample architecture and matched tissue availability.
- Panels moved to supplementary: PCA/latent scatter and full clustering QC.
- Main claim: discrete k = 2 classes did not meet the prespecified stability criterion, motivating continuous molecular programs.

## Figure 2
- Changes made: simplified the evidence matrix, emphasized tissue contribution, GSE244679 replication and final program interpretation.
- Panels retained: evidence matrix, tissue contribution and independent paired-skin replication.
- Panels moved to supplementary: gene-count bars and extended program details.
- Main claim: F1/F2/F6 are skin-primary tissue programs and F7 is systemic-supportive.

## Figure 3
- Changes made: rebuilt as single-cell plus spatial contextualization with donor-level effects and a spot-level contextual view.
- Panels retained: cell-type localization and donor-level effects.
- Panels moved to supplementary: full sensitivity, dropout robustness, treatment/timepoint panels and all spatial sections.
- Main claim: frozen programs show directional cellular and spatial support without becoming definitive cell-state mechanisms.
- Boundary note: the available spot-score table does not contain tissue x/y coordinates, so panel d is a representative spot-level contextual strip rather than a histology-aligned spatial map.

## Figure 4
- Changes made: rebuilt as a deliberate hypothesis-test boundary, with genetic evidence, matched-null summary and pivot to overall psoriasis susceptibility.
- Panels retained: primary enrichment and matched-null evidence.
- Panels moved to supplementary: full histograms, MHC sensitivity and negative-control diagnostics.
- Main claim: molecular programs lack robust axis-specific genetic anchoring, so overall psoriasis susceptibility is the genetics layer.

## Figure 5
- Changes made: retained LDSC forest plot but replaced grouped bars with directional local-architecture counts and a reduced local-rg heatmap.
- Panels retained: LDSC and selected local-rg heatmap.
- Panels moved to supplementary: full LAVA locus list and LD-reference sensitivity details.
- Main claim: overall psoriasis susceptibility shows disease-specific genome-wide and local shared architecture.

## Figure 6
- Changes made: rebuilt from dense Phase 4C/4D composites into a synthesis figure with evidence funnel, PP4 candidate dot plot and layered biological model.
- Panels retained: restricted coloc candidates and no-overlap interpretation.
- Panels moved to supplementary: full SMR tables, HEIDI distributions, all PP3/PP4 candidates and MAF-proxy diagnostics.
- Main claim: restricted regulatory prioritization supports a layered model while preserving incomplete coloc and no direct program-gene overlap.

## Final Story Test
- 1. YES: Figure 1 explains the discrete-to-continuous transition.
- 2. YES: Figure 2 makes F1/F2/F6/F7 interpretable without Table 2.
- 3. YES: Figure 3 contains single-cell and spatial evidence.
- 4. YES: Figure 3 uses donor-level effects and avoids cell-level inference.
- 5. YES: Figure 4 is framed as a deliberate hypothesis test.
- 6. YES: Figure 4 motivates overall psoriasis susceptibility as the downstream genetic layer.
- 7. YES: Figure 5 shows CAD/PsA/IBD differences visibly.
- 8. YES: Figure 5 avoids protective IBD wording.
- 9. YES: Figure 6 separates local sharing from coloc evidence.
- 10. YES: Figure 6 marks MAF-proxy signals with triangles.
- 11. YES: Figure 6 makes the state-vs-liability model explicit.
- 12. YES: All figures are designed as full-width manuscript figures.
- 13. YES: Displayed numbers are recorded in numeric audit/source data.
- 14. YES: Internal phase labels are removed from final visual text.
- 15. YES: QC/sensitivity analyses are retained for supplementary use, not deleted.

## QA Summary
- Vector outputs: SVG and PDF generated with editable text.
- Raster outputs: PNG and TIFF generated at 600 dpi.
- PDF font audit: all six PDFs passed the 5 pt minimum text-size check.
- Nature-figure source validation: PASS-ready, with one non-blocking missing-data exclusion warning from rank-correlation pairwise `dropna()`.
- Visual inspection: contact-sheet review completed; no obvious clipping, duplicated legends, or unsupported visual claims detected.

## Decision

FINAL_FIGURE_SET_READY
