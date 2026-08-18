# Communications Biology Supplementary Methods v2

## Analysis Governance

Analyses followed a prespecified sequence designed to prevent post hoc redefinition of molecular programs, outcomes or genetic interpretation. Discrete transcriptomic representation was evaluated before continuous molecular modeling; retained molecular programs were then contextualized in cellular, spatial and genetic analyses before overall psoriasis comorbidity genetics was interpreted.

## Analyses Not Pursued

The final manuscript did not perform broad MR, axis-specific MR/LDSC/LAVA/coloc, new cohort hunting, post hoc single-cell or spatial redefinition, drug prediction, PPI, hub-gene analysis, LASSO, machine-learning marker selection or post hoc GWAS replacement.

## Transcriptomic Program Definition

The tested discrete k = 2 representation did not meet the prespecified stability criterion because the minimum bootstrap Jaccard index was 0.562, below the predefined 0.75 stability threshold. Continuous MOFA-style factors were then modeled in 76 complete baseline discovery patients. Eight factors were stable across five random seeds. F1, F2, F6 and F7 were retained after evidence-matrix prioritization. F1/F2/F6 were interpreted as skin-primary bulk molecular programs, and F7 as a systemic/supportive candidate.

## Single-cell and Spatial Contextualization

Retained CORE and EXTENDED signatures were scored in single-cell and spatial datasets. CORE results were primary, and EXTENDED results were sensitivity checks. Single-cell inference used donor-level or sample-level summaries. Spatial spot/section signals were treated as directional contextual evidence.

## Genetic Architecture

Axis-specific genetic anchoring was tested first. None of the four retained molecular programs met prespecified criteria for robust axis-specific genetic anchoring. Overall psoriasis susceptibility was then analyzed against prespecified comorbidity outcomes using LDSC. Restricted LAVA was applied only to CAD, PsA, Crohn disease and ulcerative colitis after sign/QC adjudication. CAD was the primary systemic target; PsA was a near-neighbor positive control; Crohn disease and ulcerative colitis were retained as QC-flagged IBD targets.

## Regulatory Prioritization

SMR/HEIDI used GTEx v8 eQTL data from outcome-relevant tissues. Coloc was restricted to Tier A shared-locus/eQTL candidates. PP4 >= 0.8 was interpreted as supported colocalization; 0.5 <= PP4 < 0.8 as suggestive; PP3 > PP4 as evidence favoring distinct signals. eQTL MAF proxy inputs are explicitly flagged in the main and supplementary tables.

## Missing or Unresolved Inputs

T2D, MASLD, major depressive disorder and uveitis were prespecified but did not enter the final LDSC result table because prespecified primary GWAS access or source resolution was incomplete. They must not be described as null outcomes.
