# CB Figure 6 Final Redesign Report

## Previous weaknesses
- Supported and suggestive categories were shown sequentially rather than as parallel coloc outcomes.
- Count units were ambiguous across local-rg, SMR/HEIDI, highest-tier genes and coloc results.
- The PP4 plot lacked a compact disease legend and used code-like tissue labels.
- The conceptual panel read like an analysis workflow rather than the manuscript synthesis model.
- Correspondence tests between tissue-state and inherited-liability layers were not visually centered.

## Count/unit audit
- FDR-supported local-rg sharing: n = 122 locus-trait pairs.
- SMR/HEIDI prioritization: n = 91 outcome-gene pairs.
- Highest-tier set: n = 33 outcome-gene pairs (30 unique genes).
- Restricted colocalization: n = 15 outcome-gene-tissue pairs.
- PP4-supported: n = 5 outcome-gene-tissue pairs.
- Suggestive: n = 10 outcome-gene-tissue pairs.

## Panel a changes
An evidence cascade was selected instead of a literal funnel because count units change across layers. Supported and suggestive coloc outcomes are parallel branches within the restricted colocalization layer.

## Panel b changes
Candidates are grouped by outcome, with disease color encoding and circle/triangle shape encoding standard versus MAF-proxy input. The PP4 = 0.80 line is labeled as a prespecified PP4 support threshold. Tissue labels were converted to manuscript-facing names and LCL is defined in the legend.

## Panel c changes
The lower panel now presents two observed biological layers: tissue-state programs and inherited multisystem liability. Axis-specific genetic anchoring and gene-membership overlap are shown as correspondence tests between layers, leading to the final interpretation that the layers are connected but non-equivalent.

## Publication-ready legend
Figure 6 | Restricted regulatory prioritization supports a layered model of psoriasis biology. a, Evidence cascade from FDR-supported local-rg locus-trait pairs to SMR/HEIDI-prioritized outcome-gene pairs, highest-tier genes and restricted colocalization. Supported and suggestive coloc results are parallel outcome-gene-tissue categories, not sequential stages. b, Restricted colocalization candidates grouped by outcome. Points show PP4, interpreted as posterior support for a model-compatible shared association signal under the coloc model. Colors indicate disease, circles indicate standard input, and triangles denote analyses using eQTL MAF as a proxy where GWAS EAF was unavailable. The dashed line marks the prespecified PP4 support threshold of 0.80. LCL, EBV-transformed lymphocytes. c, Final synthesis model separating tissue-state molecular programs from inherited-liability architecture. The study found no robust direct axis-specific genetic anchoring and no direct gene-membership overlap between regulatory candidates and the molecular programs, supporting connected but non-equivalent biological layers.

## Remaining limitations
- MAF-proxy sensitivity remains visible for UC/Crohn candidates and should not be interpreted as the same input certainty as standard coloc tests.
- GTEx baseline eQTL context may miss disease-state or cell-state-specific regulation.
- No direct program-candidate gene overlap does not imply no biological coupling between layers.

## Final main claim
Restricted regulatory prioritization refined shared genetic loci without establishing direct one-to-one correspondence with the transcriptomic programs, supporting a model in which psoriasis tissue-state heterogeneity and inherited multisystem liability are connected but non-equivalent biological layers.

## Final quality test
| Question | Answer |
|---|---|
| Does panel a represent supported and suggestive coloc outcomes as parallel categories? | YES |
| Are all count units explicit? | YES |
| Does the evidence cascade avoid false subset implications? | YES |
| Is disease identity clear in panel b? | YES |
| Is MAF-proxy sensitivity immediately visible? | YES |
| Is the PP4 threshold clearly prespecified? | YES |
| Are PsA/UC supported signals distinguished from CAD/Crohn suggestive signals? | YES |
| Does panel c prioritize biology over method names? | YES |
| Is axis-specific anchoring visually a test between layers? | YES |
| Is zero direct gene-membership overlap described precisely? | YES |
| Does the model avoid implying complete biological independence? | YES |
| Is connected but non-equivalent biological layers the visual takeaway? | YES |
| Are all displayed values source-traceable? | YES |
| Is the figure readable at normal manuscript size? | YES |

Final status: FIGURE6_FINAL_READY
