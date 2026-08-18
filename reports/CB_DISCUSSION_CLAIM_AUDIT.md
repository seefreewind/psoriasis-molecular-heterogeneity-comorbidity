# Communications Biology Discussion Claim Audit

## Claim Classification Rules

- `DIRECT_RESULT`: directly observed in this project.
- `LITERATURE_SUPPORTED_INTERPRETATION`: supported by cited external literature.
- `REASONABLE_INFERENCE`: biologically plausible synthesis from direct results and literature.
- `SPECULATIVE`: plausible but not used as a main claim.
- `PROHIBITED`: unsupported or overclaimed; none should remain.

## Audited Claims

| Paragraph | Claim | Classification | Evidence basis | Status |
| --- | --- | --- | --- | --- |
| 1 | The study separates tissue molecular state from inherited comorbidity liability. | REASONABLE_INFERENCE | Phase 1B-4E results integrated across transcriptomics and genetics. | Retained with bounded language. |
| 1 | Immune-mediated disease atlases provide conceptual context for shared inflammatory states. | LITERATURE_SUPPORTED_INTERPRETATION | Jimenez-Gracia et al. 2026. | Stated as context only. |
| 2 | The unstable k = 2 result does not disprove all psoriasis endotypes. | REASONABLE_INFERENCE | Internal clustering stability plus comparison with transcriptomic endotype literature. | Retained to prevent contradiction. |
| 3 | F1/F2/F6 are reproducible tissue-state variables rather than independent inherited axes. | DIRECT_RESULT | Phase 2A-3A frozen program and genetics reports. | Retained. |
| 3 | F7 is systemic-supportive, not a pan-inflammatory skin-spatial axis. | DIRECT_RESULT | Internal blood support, GSE61281 support, weak/coarse skin-spatial localization. | Retained. |
| 4 | CAD is the cleanest non-neighbour systemic genetic signal. | DIRECT_RESULT | LDSC QC PASS, positive rg and LAVA local architecture. | Retained. |
| 4 | CAD lacks a high-confidence PP4-supported eQTL mediator in this analysis. | DIRECT_RESULT | Phase 4D restricted coloc. | Retained; avoids claiming absence of mechanism. |
| 5 | Crohn/UC negative rg should not be interpreted as settled inverse liability. | REASONABLE_INFERENCE | Internal QC flags and discordant external positive genetic correlations. | Retained. |
| 5 | IBD results are best framed as local directional heterogeneity. | DIRECT_RESULT | Restricted LAVA positive and negative local signals. | Retained. |
| 6 | SMR2 retention indicates prioritization stability, not causal replication. | DIRECT_RESULT | Phase 4C SMR/HEIDI workflow. | Retained. |
| 6 | Coloc genes and molecular programs operate at different biological scales. | REASONABLE_INFERENCE | Phase 4E no-overlap result plus eQTL context literature. | Retained. |
| 7 | T2D, MASLD, MDD and uveitis cannot be called null outcomes. | DIRECT_RESULT | Primary-source unresolved status in Phase 4A. | Retained. |

## Prohibited Claim Scan

| Prohibited claim type | Present in v3? | Note |
| --- | --- | --- |
| Discrete endotypes rescued | No | Continuous programs are the interpretation unit. |
| F1/F2/F6/F7 genetically anchored | No | All remain non-genetically anchored tissue/supportive programs. |
| CAD regulatory mediator proven | No | CAD coloc is suggestive only. |
| Crohn/UC protective or globally inverse conclusion | No | Directional heterogeneity and QC sensitivity are emphasized. |
| MR, causality or clinical validation overclaim | No | No MR or clinical validation claim is made. |
