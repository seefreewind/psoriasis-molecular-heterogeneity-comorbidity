# Communications Biology Supplementary Methods v1

## Analysis Governance

The project used phase-specific locks to prevent post hoc redesign. The final manuscript preserves four decisions: `GO_TO_MANUSCRIPT_ASSEMBLY`, `CONDITIONAL_GO_TO_TARGETED_FIGURE_COMPLETION`, `NO_GO_TO_BROAD_MR` and `NO_GO_TO_AXIS_SPECIFIC_GENETICS`. No new discovery analysis was performed during manuscript assembly.

## Prohibited Analyses

The final manuscript excludes broad MR, axis-specific MR/LDSC/LAVA/coloc, new cohort hunting, single-cell or spatial rescue analysis, drug prediction, PPI, hub-gene analysis, LASSO, machine-learning marker selection and post hoc GWAS replacement.

## Transcriptomic Program Definition

Discrete k = 2 endotypes were rejected because the minimum bootstrap Jaccard index was 0.562, below the predefined 0.75 stability threshold. Continuous MOFA factors were then modeled in 76 complete baseline discovery patients. Eight factors were stable across five random seeds. F1, F2, F6 and F7 were retained after evidence-matrix prioritization. F1/F2/F6 were interpreted as skin-primary bulk molecular programs, and F7 as a systemic/supportive candidate.

## Single-cell and Spatial Contextualization

Frozen CORE and EXTENDED signatures were scored in single-cell and spatial datasets. CORE results were primary; EXTENDED results were sensitivity checks. Single-cell inference used donor-level or sample-level summaries. Spatial spot/section signals were treated as directional contextual evidence.

## Genetic Architecture

Axis-specific genetic anchoring was tested first and closed with all four programs assigned Tier D. Overall psoriasis susceptibility was then analyzed against frozen comorbidity outcomes using LDSC. Restricted LAVA was applied only to CAD, PsA, Crohn disease and ulcerative colitis after sign/QC adjudication. CAD was the primary systemic target; PsA was a near-neighbor positive control; Crohn disease and ulcerative colitis were retained as QC-flagged IBD targets.

## Regulatory Prioritization

SMR/HEIDI used GTEx v8 eQTL data from outcome-relevant tissues. Coloc was restricted to Tier A shared-locus/eQTL candidates. PP4 >= 0.8 was interpreted as supported colocalization; 0.5 <= PP4 < 0.8 as suggestive; PP3 > PP4 as evidence favoring distinct signals. eQTL MAF proxy inputs are explicitly flagged in the main and supplementary tables.

## Missing or Unresolved Inputs

T2D, MASLD, major depressive disorder and uveitis were prespecified but did not enter the final LDSC result table because frozen primary GWAS access or source resolution was incomplete. They must not be described as null outcomes.
