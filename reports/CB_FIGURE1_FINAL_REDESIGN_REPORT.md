# Figure 1 Final Redesign Report

## Previous Weaknesses
- Crossing arrows in the cohort/tissue schematic made the study architecture harder to parse.
- The previous bar plot compared non-equivalent analysis sets and did not clearly separate 82 paired-skin availability from 76 complete three-view modeling patients.
- The k = 2 minimum bootstrap Jaccard value was displayed as a filled area, even though 0.562 is a single statistic.
- The threshold label floated away from the 0.75 line.
- Tissue boxes reused colors that are reserved for F1/F2/F6/F7 programs.
- The layout left unused whitespace and made the decision step less prominent than the QC statistic.

## Changes Implemented
- Panel a was rebuilt as a neutral hierarchical cohort schematic: E-MTAB-14509 baseline cohort to discovery and skin-only replication.
- Panel b was replaced with an analysis-set availability matrix for lesional skin, non-lesional skin and blood.
- Panel b explicitly distinguishes 82 discovery paired-skin patients from 76 complete matched LS/NL/blood patients used for multi-view modeling.
- Panel c was redesigned as a lollipop-style single-statistic display with a point at 0.562 and a dashed threshold at 0.75.
- Panel d was rewritten as the visual destination: discrete k = 2 representation, criterion not met, continuous multi-view factor modeling, and retained F1/F2/F6/F7 programs.
- Program colors are used only for F1/F2/F6/F7; tissue/sample elements use neutral grey/blue-grey tones.

## Panels Moved to Supplementary
- PCA/latent scatter views and full clustering sensitivity diagnostics should remain supplementary rather than in the main Figure 1.
- Full bootstrap and clustering QC should remain in the supplementary stability material.

## Publication-ready Legend
Figure 1. Study design and transition from discrete endotypes to continuous molecular programs. a, E-MTAB-14509 contained 146 baseline psoriasis patients and was divided into a discovery analysis set and an internal paired-skin replication set. The discovery multi-view analysis used 76 patients with complete matched lesional skin, non-lesional skin and blood data; 82 discovery patients had paired skin available. The replication set contained 57 paired lesional/non-lesional skin samples and did not include a blood replication compartment. b, Analysis-set availability matrix showing the distinction between paired-skin availability and complete three-view data used for multi-view modeling. c, Prespecified discrete-cluster stability test for the tested k = 2 representation. The minimum bootstrap Jaccard index was 0.562, below the prespecified stability threshold of 0.75. d, Because the tested discrete k = 2 representation did not meet the prespecified stability criterion, downstream molecular heterogeneity was represented using continuous multi-view factor modeling. F1, F2, F6 and F7 were retained for downstream interpretation.

## Final Main Claim
The tested discrete k=2 representation did not meet the prespecified stability criterion, motivating a continuous multi-view representation of psoriasis molecular heterogeneity.

## Final Quality Test
| Item | Answer |
|---|---|
| Can the reader understand the cohort structure in <5 s? | YES |
| Is discovery three-view n=76 clearly distinguished from paired-skin n=82? | YES |
| Is replication clearly skin-only? | YES |
| Is 0.562 displayed as a single statistic rather than an area? | YES |
| Is the 0.75 threshold visually unambiguous? | YES |
| Is the direction from discrete to continuous visually obvious? | YES |
| Are program colors reserved for F1/F2/F6/F7? | YES |
| Does panel d prepare the reader for Figure 2? | YES |
| Does the figure avoid implying that psoriasis has no endotypes? | YES |
| Is the complete figure readable at realistic manuscript scale? | YES |
