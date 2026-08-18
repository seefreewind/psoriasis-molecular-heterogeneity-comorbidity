# PHASE 4C Final Mini Manuscript Section Pack

Date: 2026-08-16  
Scope: Phase 4C shared-locus/eQTL gene prioritization  
Status: ready for manuscript integration, not yet formal colocalization  
Reference file: `literature/phase4c_reference_targets.bib`

## 1. Manuscript position

Phase 4C is the regulatory-gene prioritization layer after Phase 4A/4B/4B-R. It should be written as:

> robust psoriasis-comorbidity shared local loci → GTEx v8 SMR/HEIDI → candidate regulatory genes

It should not be written as:

> psoriasis molecular axes → genetic anchoring → causal mediation → drug targets

The main disease ordering is fixed:

1. CAD: primary systemic track.
2. PsA: positive-control / near-neighbor track.
3. Crohn disease and UC: IBD local-direction heterogeneity track.

F1/F2/F6/F7 remain outside the genetics main analysis and should only return later as transcriptomic contextualization.

## 2. One-sentence argument

Overall psoriasis susceptibility showed robust shared local genetic architecture with selected comorbidity outcomes, and GTEx v8 SMR/HEIDI prioritized a tissue-supported candidate regulatory-gene layer, with CAD as the cleanest systemic signal, PsA as a positive-control phenotype, and IBD showing local directional heterogeneity.

## 3. Methods subsection

### Shared-locus eQTL gene prioritization

We prioritized candidate regulatory genes within psoriasis-comorbidity shared local genetic regions using GTEx v8 SMR/HEIDI `[@Zhu2016SMR; @GTEx2020Atlas]`. The input loci were restricted to Phase 4B-R local genetic-correlation loci that remained after LD-reference validation and were assigned Tier 1 or Tier 2 status. The Phase 4C outcomes were coronary artery disease (CAD), psoriatic arthritis (PsA), Crohn disease and ulcerative colitis (UC). CAD was treated as the primary systemic outcome, PsA as a positive-control / near-neighbor outcome, and Crohn disease and UC as inflammatory bowel disease outcomes with local-direction heterogeneity.

GTEx v8 SMR-format BESD packages were audited before analysis. Usable priority tissues included sun-exposed skin, non-sun-exposed skin, whole blood, coronary artery, aorta, tibial artery, sigmoid colon, transverse colon, spleen, EBV-transformed lymphocytes and cultured fibroblasts. Small intestine terminal ileum was excluded because the local GTEx BESD package was incomplete or corrupted. The GTEx BESD resources were used only for SMR/HEIDI-compatible eQTL prioritization and were not treated as complete colocalization-ready eQTL association matrices.

GWAS summary statistics were converted to SMR `.ma` format with SNP ID, effect allele, other allele, allele frequency, effect estimate, standard error, P value and sample size. Variants were harmonized to rsID where required using chromosome, position and allele information from the 1000 Genomes European LD reference. The project-local PLINK reference files were linked under the Phase 4C genetics reference directory and used for HEIDI LD calculations.

The first restricted SMR run used GWAS `.ma` files constructed from Phase 4C candidate LAVA loci. Because a probe's strongest cis-eQTL can fall outside a LAVA block, we then performed a probe-centered sensitivity analysis. For this SMR2 run, each selected GTEx probe was expanded to a ±2 Mb cis window, overlapping windows were merged by trait, and GWAS summary statistics were rebuilt within the merged intervals. The SMR2 probe-window `.ma` files contained 174,979 CAD variants, 139,812 PsA variants, 170,443 Crohn disease variants, 146,455 UC variants and 529,946 psoriasis variants after rsID and allele-frequency mapping.

SMR/HEIDI analyses were run with SMR version 1.03 through Rosetta (`arch -x86_64`) because the available macOS arm64 SMR 1.4.2 binary failed when reading the local GTEx v8 BESD files. For each outcome and tissue, SMR was run on the preselected probes from eligible Phase 4C loci. Primary SMR2 signals were defined as global SMR FDR < 0.05 with HEIDI pass, where HEIDI pass was defined as `p_HEIDI > 0.01` or unavailable HEIDI P value. Results were aggregated to one row per `outcome × locus × gene × probeID`.

Candidate genes were assigned evidence tiers using both the Phase 4B-R local-locus tier and tissue recurrence in SMR2. Tier A denoted Phase 4B-R Tier 1 loci with SMR2 support in at least two GTEx tissues. Tier B1 denoted Phase 4B-R Tier 1 loci with single-tissue SMR2 support. Tier B2 denoted Phase 4B-R Tier 2 loci with recurrent SMR2 support. Tier C denoted Phase 4B-R Tier 2 loci with single-tissue SMR2 support. The frozen Phase 4C gene table used SMR2 as the primary prioritization layer and retained SMR1 only as a sensitivity comparison.

The stability of the probe-centered SMR2 analysis was evaluated against the original restricted SMR1 run at two levels: `outcome + gene` and `outcome + tissue + gene`. Candidate retention was calculated as the intersection of primary SMR1 and SMR2 signals divided by the number of primary SMR1 signals. Genes or tissue-specific rows that were not retained after SMR2 were downgraded to sensitivity-only status and were not used as primary Phase 4C candidates.

## 4. Results subsection

### Shared local genetic regions prioritized tissue-supported regulatory-gene candidates

We next asked whether robust psoriasis-comorbidity local genetic-sharing regions could be resolved into candidate regulatory genes. We restricted this analysis to Phase 4B-R loci that remained stable after LD-reference validation and applied GTEx v8 SMR/HEIDI using the probe-centered ±2 Mb SMR2 input. A gene was retained in the frozen Phase 4C table when it mapped to an eligible local locus, showed global SMR FDR < 0.05, and passed HEIDI filtering (`p_HEIDI > 0.01` or unavailable).

This procedure yielded 91 frozen `outcome × locus × gene × probe` rows, corresponding to 82 unique genes across 21 local loci (Fig. Xa; Supplementary Table X). The table separated candidates into four evidence tiers. Tier A contained 33 recurrent candidates from Phase 4B-R Tier 1 loci with SMR2 support in at least two GTEx tissues. The remaining rows comprised 44 Tier B1 single-tissue candidates from Tier 1 loci, 5 Tier B2 recurrent candidates from Tier 2 loci, and 9 Tier C single-tissue candidates from Tier 2 loci.

### CAD formed the primary systemic eQTL-prioritized track

CAD remained the clearest systemic track after eQTL-based gene prioritization. The CAD table contained 26 genes across 7 local loci, including 8 Tier A recurrent candidates from 4 Tier 1 positive local genetic-correlation loci (Fig. Xb; Table X). The strongest CAD Tier A signal was `SMARCA4` at locus 2318, supported in two skin tissues (minimum SMR `P = 7.35 × 10^-11`, global SMR FDR `= 6.94 × 10^-9`). CAD locus 1841 contributed multiple recurrent candidates, including `TMEM116` across blood/immune and vascular tissues, `MAPKAPK5` across skin and vascular tissues, and `ADAM1B` across skin and vascular tissues.

Additional CAD Tier A candidates included `RGL3`, `MEX3A`, `UBQLN4` and `AC007381.3`. These genes did not all share the same tissue pattern: some were supported mainly in skin, whereas others involved vascular or blood/immune tissues. This tissue distribution is consistent with CAD being the strongest cross-system track in Phase 4C, while still requiring gene-level interpretation to remain locus-specific.

### PsA behaved as a positive-control near-neighbor phenotype

PsA provided the expected near-neighbor signal and was retained as a positive-control track. The PsA frozen table contained 23 genes across 6 positive local genetic-correlation loci, including 12 Tier A recurrent candidates. Recurrent PsA candidates included `RP11-977G19.11`, `SLC22A5`, `C6orf3`, `TYK2`, `PDLIM4`, `ICAM5`, `RPS26`, `IFNLR1`, `MRPL4`, `SUOX`, `CDC42SE2` and `C5orf56`.

These results supported the internal behavior of the Phase 4C pipeline because PsA is genetically and clinically closer to psoriasis than the other systemic outcomes. For this reason, PsA should be interpreted as a positive-control / near-neighbor analysis rather than the main evidence for multisystem comorbidity.

### IBD loci retained directionally heterogeneous local architecture

Crohn disease and UC retained local-direction heterogeneity after SMR2 gene prioritization. Crohn disease contributed 21 genes across 8 loci. Of these, 15 genes mapped to 4 negative local genetic-correlation loci and 6 genes mapped to 4 positive local genetic-correlation loci (Fig. Xc). The recurrent Crohn disease candidates included `SLC22A5`, `CDC42SE2`, `PARK7`, `KIF3A`, `VAMP3`, `TCTEX1D1` and `HSPA4`.

UC also showed a mixed local architecture. The UC frozen table contained 21 genes across 7 loci, with 17 genes in 5 negative local genetic-correlation loci and 4 genes in 2 positive local genetic-correlation loci. Recurrent UC candidates included `ORMDL3`, `GSDMB`, `GSDMA`, `SMARCE1`, `RP11-973H7.1` and `TCTEX1D1`. The concentration of UC candidates in negative local genetic-correlation regions supports the Phase 4B conclusion that the IBD signal should not be summarized as a single positive or negative genome-wide relationship.

### Probe-centered SMR2 sensitivity supported the frozen gene layer

The SMR2 sensitivity analysis addressed the main limitation of the original locus-restricted SMR run. Instead of restricting the GWAS input to LAVA blocks, SMR2 rebuilt GWAS summary-statistic inputs around each selected GTEx probe using merged probe-centered ±2 Mb windows. All 25 outcome-by-tissue SMR/HEIDI jobs completed successfully.

The probe-window analysis preserved the gene-level candidate set. SMR1 identified 91 primary `outcome + gene` candidates, and SMR2 retained all 91 (100.0% retention; Fig. Xd). At the `outcome + tissue + gene` level, SMR2 retained 174 of 176 SMR1 primary signals (98.9% retention). The two non-retained rows were CAD-specific tissue-level signals, `PCBP1-AS1` in aorta and `RP11-347I19.8` in coronary artery. No new SMR2 primary genes were introduced. These results support using SMR2 as the primary Phase 4C gene-prioritization layer.

Together, these analyses linked robust psoriasis-comorbidity local genetic-sharing regions to tissue-supported eQTL candidate genes. The results nominate candidate regulatory genes within shared local loci, but they do not establish formal colocalization, causal mediation or therapeutic directionality.

## 5. Discussion integration

The Phase 4 analyses reposition the study from axis-specific genetic anchoring to comorbidity-level shared architecture. This shift is supported by the negative Phase 3A result: F1/F2/F6/F7 remained useful as transcriptomic programs but did not provide stable genetically anchored axes for GWAS interpretation. In contrast, overall psoriasis susceptibility showed a cleaner systemic connection with CAD than with most other comorbidity outcomes. This is biologically and clinically plausible, because psoriasis has long been linked to myocardial infarction risk in population-based data, and recent genetic analyses have reported shared risk between psoriasis and CAD `[@Gelfand2006PsoriasisMI; @Patrick2022PsoriasisCAD]`. Our contribution is narrower than those prior studies: rather than claiming a causal cardiovascular pathway, we localize where genome-wide sharing is concentrated and then prioritize regulatory genes in robust shared local loci.

PsA and IBD require different interpretation. PsA is a useful near-neighbor positive control because its genetic architecture overlaps with cutaneous psoriasis while remaining distinguishable from it `[@Stuart2015PsAGWAS]`. Crohn disease and UC should be framed as a directional-heterogeneity result rather than as a simple positive or negative global correlation. Previous work has identified shared susceptibility loci between psoriasis and Crohn disease, and epidemiological data support links among psoriasis, PsA and Crohn disease `[@Ellinghaus2012PsoriasisCrohn; @Li2013PsoriasisPsACrohn]`. The present LAVA results extend this literature by showing that local positive and negative signals can coexist across genomic regions. This interpretation follows the rationale of local genetic correlation analysis, where regional sharing may be missed or obscured by a single genome-wide estimate `[@Werme2022LAVA]`.

The Phase 4C gene-prioritization layer should also remain explicitly bounded. SMR/HEIDI integrates GWAS and eQTL summary statistics to prioritize genes whose genetically regulated expression is associated with a trait, while HEIDI screens for heterogeneity patterns consistent with linkage rather than a shared regulatory signal `[@Zhu2016SMR]`. Using GTEx v8 allowed us to evaluate relevant skin, blood, vascular and intestinal tissues across robust shared local loci `[@GTEx2020Atlas]`. These results are best described as candidate regulatory genes, not as proven mediators. Formal colocalization tests ask whether association signals are consistent with a shared causal variant and will be needed before promoting any locus to a causal regulatory mechanism `[@Giambartolomei2014Coloc]`.

Several technical constraints limit interpretation. First, the GTEx v8 BESD resources were suitable for SMR/HEIDI but not directly sufficient for standard colocalization workflows. Second, small intestine terminal ileum was excluded because the local BESD package was unusable, limiting intestinal tissue coverage for IBD. Third, SMR analyses were run with SMR 1.03 under Rosetta because the available macOS arm64 SMR 1.4.2 binary failed on the local GTEx BESD files. Fourth, the Phase 4C gene table was restricted to loci already selected by Phase 4B-R; this design prioritizes interpretability within robust shared local regions but does not constitute a genome-wide gene scan.

These boundaries define the next step. CAD Tier A genes provide the most defensible entry point for formal shared-locus follow-up, including colocalization-ready eQTL extraction, fine-mapping and tissue-specific interpretation. PsA should remain a positive-control track. Crohn disease and UC should be analyzed by local direction group rather than pooled into a single IBD claim. Bidirectional MR should remain downstream of formal shared-locus resolution, because running MR before confirming shared causal signals would risk interpreting linkage or regulatory correlation as mediation.

## 6. Figure legend

**Figure X. Shared-locus eQTL prioritization of psoriasis-comorbidity genetic architecture.**

**a,** Frozen Phase 4C gene table summarized by outcome and evidence tier. Tier A denotes Phase 4B-R Tier 1 loci with recurrent SMR2 support across at least two GTEx tissues. B1, B2 and C denote progressively weaker combinations of local-locus tier and tissue recurrence. **b,** CAD Tier A recurrent candidate genes ranked by global SMR FDR. Point labels indicate the number of supporting tissues. **c,** Crohn disease and ulcerative colitis candidate genes stratified by positive or negative local genetic-correlation direction; red indicates recurrent tissue support and grey indicates single-tissue support. **d,** Sensitivity comparison between the original LAVA-locus-restricted SMR1 analysis and the probe-centered ±2 Mb SMR2 analysis. SMR2 retained all primary `outcome + gene` candidates and 98.9% of primary `outcome + tissue + gene` candidates.

Statistics: SMR2 primary signals were defined as global SMR FDR < 0.05 with HEIDI pass (`p_HEIDI > 0.01` or unavailable). These results prioritize eQTL-linked candidate regulatory genes within robust shared local genetic regions and do not establish formal colocalization or causal mediation.

Figure files:

- SVG: `results/figures/phase4c/Figure_Phase4C_shared_locus_eqtl_prioritization.svg`
- TIFF: `results/figures/phase4c/Figure_Phase4C_shared_locus_eqtl_prioritization.tiff`
- PNG preview: `results/figures/phase4c/Figure_Phase4C_shared_locus_eqtl_prioritization.png`

## 7. Table package

### Main Table X. CAD Tier A shared-locus eQTL-prioritized candidate genes

Source: `results/phase4c_smr/manuscript_tables/phase4c_main_cad_tierA_gene_table.tsv`

This table lists CAD candidate regulatory genes that met Tier A Phase 4C criteria. Tier A required a Phase 4B-R Tier 1 positive local genetic-correlation locus and recurrent SMR2 support in at least two GTEx tissues. Columns report the local locus, genomic interval, candidate gene, local genetic-correlation direction, UKB-reference local genetic-correlation statistics, GTEx tissue support, minimum SMR P value, global SMR FDR, HEIDI P value and SMR effect direction. These genes are eQTL-prioritized candidates within robust shared local loci and should not be interpreted as formally colocalized or causal genes.

### Supplementary Table X. Frozen Phase 4C shared-locus eQTL candidate table

Source: `results/phase4c_smr/manuscript_tables/phase4c_supplementary_all_frozen_gene_table.tsv`

This table contains all 91 frozen Phase 4C candidate rows. Each row represents one `outcome × locus × gene × probeID` combination retained after SMR2 prioritization. The table includes CAD, PsA, Crohn disease and UC; Phase 4B-R local-locus tier; local genetic-correlation direction; GTEx tissue support; top SMR result; HEIDI status; and final evidence tier.

### Supplementary Table X. PsA positive-control Tier A candidate genes

Source: `results/phase4c_smr/manuscript_tables/phase4c_positive_control_psa_tierA_gene_table.tsv`

This table lists PsA Tier A candidate regulatory genes identified within positive local genetic-correlation loci. PsA was analyzed as a positive-control / near-neighbor phenotype because of its close clinical and genetic relationship to psoriasis.

### Supplementary Table X. IBD direction-heterogeneity Tier A candidate genes

Source: `results/phase4c_smr/manuscript_tables/phase4c_ibd_direction_heterogeneity_tierA_gene_table.tsv`

This table lists Tier A candidate genes for Crohn disease and UC, stratified by positive or negative local genetic-correlation direction. Crohn disease and UC are shown separately because their Phase 4B/4C results support local-direction heterogeneity rather than a single genome-wide direction.

### Supplementary Table X. Phase 4C manuscript gene-table counts

Source: `results/phase4c_smr/manuscript_tables/phase4c_manuscript_gene_table_counts.tsv`

This table summarizes the number of candidate genes by outcome, analysis role and final Phase 4C evidence tier.

## 8. Claim boundaries

| Claim | Allowed wording | Avoid |
|---|---|---|
| CAD | `CAD is the clearest systemic shared-genetic track in Phase 4C` | `CAD risk is mediated by psoriasis genes` |
| PsA | `PsA is a near-neighbor positive-control phenotype` | `PsA proves broad multisystem comorbidity` |
| IBD | `IBD shows local-direction heterogeneity` | `IBD is simply negatively correlated with psoriasis` |
| SMR/HEIDI | `prioritized eQTL-linked candidate regulatory genes` | `confirmed colocalization` |
| GTEx tissues | `provided tissue-supported regulatory context` | `identified the causal tissue` |
| MR | `should remain downstream of formal shared-locus resolution` | `ready to run now` |

## 9. Integration checklist

| Item | Status |
|---|---|
| Results subsection | ready |
| Methods subsection | ready |
| Discussion integration | ready |
| Figure legend | ready |
| Main table caption | ready |
| Supplementary table captions | ready |
| BibTeX target file | ready |
| Formal coloc | not done |
| MR | explicitly deferred |

## 10. Next recommended action

Proceed to `PHASE4D_COLOCALIZATION_INPUT_AUDIT_AND_FEASIBILITY`, not MR.

The next task should determine whether coloc-ready eQTL summary data can be produced from GTEx v8 or another verified eQTL source for the frozen Phase 4C Tier A/Tier B candidate loci. If coloc-ready per-variant eQTL matrices cannot be obtained, Phase 4D should become a feasibility report and the manuscript should retain SMR/HEIDI as the terminal gene-prioritization layer.
