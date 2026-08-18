# Decision log

## Decision 001

Question:
What is the primary Phase 1 data source?

Evidence:
The project brief names PSORT / E-MTAB-14509. The official BioStudies record describes an RNA-seq study of PSORT discovery and refinement psoriasis cohorts with skin and blood samples during biologic treatment.

Decision:
Use E-MTAB-14509 as the locked primary dataset.

Reason:
It contains baseline and longitudinal psoriasis RNA-seq with patient identifiers, tissue labels, cohort-encoded count files, and limited clinical metadata.

Impact:
All Phase 1 inclusion, QC, feature construction, discovery, and replication steps are based on this dataset unless a blocking data-integrity issue is found.

## Decision 002

Question:
Can the primary Phase 1 claim be framed as replicated cross-tissue endotypes within E-MTAB-14509?

Evidence:
Official SDRF-derived baseline samples include discovery lesional skin, non-lesional skin, and whole blood, but replication baseline samples include lesional and non-lesional skin only. No replication whole-blood samples are listed in the SDRF/count-file mapping.

Decision:
Do not frame the current E-MTAB-14509-only Phase 1 as independently replicated three-tissue endotypes. Treat skin-paired replication as primary for replication, and treat blood as discovery-only/supporting unless an independent locked blood replication resource is added.

Reason:
Replication cannot test the blood view, so a strong cross-tissue replicated endotype claim would be vulnerable to review.

Impact:
The current project status is CONDITIONAL GO, not Strong GO. Later phases must wait for locked biological feature analysis and stronger replication evidence.

## Decision 003

Question:
Can the expression-axis smoke test be used as the primary endotype result?

Evidence:
The smoke test used lesional-minus-nonlesional normalized expression axes and did not implement the locked pathway/regulon/cell-state feature families. Its k=2 split had bootstrap Jaccard below the locked 0.75 threshold.

Decision:
Use the smoke test only to validate matrix alignment and frozen replication machinery.

Reason:
It does not satisfy the locked biological interpretability or stability criteria.

Impact:
The Phase 1 report remains CONDITIONAL GO and explicitly blocks progression to GWAS/MR/comorbidity phases.

## Decision 004

Question:
How many bootstrap/control iterations should the fallback sensitivity analysis use?

Evidence:
The primary skin-paired fallback analysis completed k=2-6 stability with 300 bootstrap iterations. Repeating the same 300-iteration grid inside each sensitivity analysis ran for more than 10 minutes and was disproportionate for a fallback workflow.

Decision:
Keep the primary stability analysis at 300 bootstrap iterations. Use fixed-k sensitivity analyses without nested bootstrap and 50 feature-value permutation controls.

Reason:
The primary conclusion is driven by the 300-iteration stability result. Sensitivity analyses are used to detect gross dependence on feature family/view choice, not to supersede the primary stability estimate.

Impact:
Runtime becomes tractable while preserving the locked primary stability audit. The lighter sensitivity/control procedure must be reported as a computational-cost adjustment.

## Decision 005

Question:
Should the project wait for the preferred R/MOFA2/GSVA workflow before issuing a Phase 1 decision?

Evidence:
User-level BiocManager installation failed for GSVA, MOFA2, ConsensusClusterPlus, and HDF5 dependencies after repeated download/build issues. A user-level micromamba binary was installed and bioconda/conda-forge package search showed no available `bioconductor-gsva` or `bioconductor-mofa2` package for the current osx-arm64 environment. The Python fallback workflow completed with baseline-only biological features, 300-bootstrap primary stability, frozen replication assignment, confounding audit, negative controls, sensitivity analyses, and figures.

Decision:
Do not block the Phase 1 decision on the unavailable preferred R stack. Mark the R/MOFA2/GSVA implementation as an environment limitation and use the completed Python fallback as the current reproducible result.

Reason:
The fallback result is sufficient to answer the immediate GO/NO-GO question conservatively: stability does not reach the locked threshold and replication lacks blood, so the project cannot move to later genetic/comorbidity phases as a strong endotype project.

Impact:
Current status remains CONDITIONAL GO for a skin-paired molecular-state/axis framing. Later phases require either a successful preferred workflow in a compatible environment or an explicit human decision to accept the fallback framing.

## Decision 006

Question:
Should Phase 1B switch from discrete endotype rescue to continuous molecular axis testing?

Evidence:
The Phase 1 biological-feature analysis selected k = 2, but the minimum bootstrap Jaccard was 0.562, below the locked 0.75 threshold for strong discrete clusters. Discovery-to-replication signature concordance was high, indicating reproducible biology, but mean nearest-centroid assignment confidence was moderate, suggesting fuzzy patient boundaries. E-MTAB-14509 replication contains paired skin but no blood, preventing a fully replicated three-tissue subtype claim.

Decision:
Phase 1B will treat continuous latent molecular axes as the primary representation. The previous k = 2 clustering remains reported and will be compared against axes, but clustering is secondary and exploratory.

Reason:
The data pattern is more consistent with continuous or fuzzy molecular structure than robust discrete patient endotypes. The reframing follows the prespecified cluster stability failure and internal replication limitations, not any downstream genetics or comorbidity result.

Impact:
Phase 1B will fit discovery-only latent axes, freeze axis definitions, project replication skin data without refitting, test discovery-only blood support, audit external skin/blood datasets, and answer whether the manuscript should use “molecular axis,” “molecular state,” or “endotype.”

## Decision 007

Question:
Does Phase 1B provide enough evidence to proceed as strong replicated molecular endotypes?

Evidence:
Python `mofapy2` successfully fit discovery-only three-view molecular axes on 76 complete baseline patients across five seeds. The factors were stable under the current complete-case, top-variance feature filter, and frozen skin projection into E-MTAB-14509 replication produced moderate support for several axes. However, replication still lacks blood RNA-seq. External GEO audit confirmed GSE121212, GSE244679, GSE54456, GSE147339, and GSE61281 as relevant resources, but only GSE121212 could be immediately used for paired psoriasis skin support in this session; its axis-loading correlations were weak. GSE244679 is relevant but the 28.4 Mb tar download timed out and is not analysis-ready. GSE147339 and GSE61281 require separate blood-specific platform handling.

Decision:
Treat Phase 1B as a successful continuous-axis rescue but keep the project at CONDITIONAL GO. Do not describe the result as strong replicated multisystem or cross-tissue endotypes.

Reason:
The continuous axes solve the discrete-cluster stability problem inside discovery and allow frozen skin projection, but external replication and independent blood support remain insufficient for a strong endotype claim.

Impact:
The manuscript direction should be “skin-primary molecular axes with discovery-only blood support” unless the user chooses to invest in additional external replication processing. Downstream single-cell/spatial, GWAS, MR, colocalization, or multisystem comorbidity phases remain blocked until that boundary is accepted.

## Decision 008

Question:
After completing the selected external replication tasks, can Phase 1B be upgraded to strong replicated multisystem endotypes?

Evidence:
The user selected both pending actions: completing GSE244679 processing and building platform-specific blood support for GSE147339 and GSE61281. GSE244679 was fully downloaded, extracted, and processed as 24 paired lesional psoriatic versus adjacent normal skin samples. It showed moderate-to-strong external paired-skin support for several axes by absolute loading-vs-lesional-minus-adjacent Spearman correlation, especially F1-LS, F2-NL, F6-LS, F3-NL, and F5-LS. GSE147339 whole-blood RNA-seq showed weak correlations across axes. GSE61281 was processed through its GEO series matrix and GPL6480 platform annotation, mapping 30,723 probes to 19,553 gene symbols; it showed moderate blood support for F7 across PsC-control, PsA-control, and combined psoriasis-spectrum-control contrasts, with smaller support for F3 and F2.

Decision:
Upgrade the evidence from weak immediate external support to skin-primary external paired-skin support with cautious external blood support. Do not upgrade to strong replicated multisystem or cross-tissue endotypes.

Reason:
The independent GSE244679 paired-skin result materially strengthens the skin-axis claim. Blood evidence remains support rather than full replication because E-MTAB-14509 replication lacks blood, GSE147339 is small, and GSE61281 differs in technology and clinical grouping.

Impact:
The manuscript can proceed as a skin-primary continuous molecular-axis study if the user accepts that boundary. Downstream single-cell/spatial, GWAS anchoring, MR, colocalization, and multisystem comorbidity phases should not proceed under a strong multisystem-endotype claim without additional design-matched blood or multi-tissue replication.

## Decision 009

Question:
After accepting the skin-primary continuous-axis boundary, what should the project do next?

Evidence:
The user explicitly accepted the current manuscript boundary and recommended moving away from additional cohort hunting. Phase 1B has already resolved the main instability problem by reframing unstable discrete k=2 endotypes as continuous molecular axes. GSE244679 provides independent paired-skin support, while GSE147339 and GSE61281 provide selective systemic support. Sending all eight axes directly into GWAS/MR would diffuse the story and increase multiple-testing and interpretation burden.

Decision:
Proceed to Phase 2A axis triage and mechanism-card construction before single-cell, spatial, GWAS, MR, or multisystem comorbidity analysis. Freeze 3-4 primary axes and move the remaining axes to supplementary review.

Reason:
The next bottleneck is interpretability and story focus, not additional bulk cohort quantity. A frozen priority matrix reduces cherry-picking risk and mechanism cards enforce the rule that an axis should not receive a formal biological name unless at least two independent feature families support the same interpretation.

Impact:
Phase 2A selected F1, F2, and F6 as primary skin-axis candidates and F7 as the primary systemic candidate. F3, F5, and F8 remain supplementary review axes, and F4 remains supplementary. The next analysis phase should be donor-level single-cell localization of the frozen primary axes.

## Decision 010

Question:
How should Phase 2A be locked to prevent circular downstream interpretation?

Evidence:
The Phase 2A master prompt requires a strict interpretation and prioritization phase, not a rediscovery phase. It explicitly prohibits prioritizing axes, renaming axes, or selecting genes based on future GWAS, MR, comorbidity, colocalization, drug, or downstream single-cell/spatial significance. It also requires axis-specific evidence matrices, standardized mechanism cards, redundancy analysis, frozen CORE/EXTENDED gene programs, single-cell and spatial readiness audits, and transparent evidence tiers.

Decision:
Lock Phase 2A as a pre-genetic, pre-comorbidity evidence-audit phase. Axis tiers, mechanism names, and gene programs must be frozen using only Phase 1B molecular-axis outputs, internal/external replication evidence, biological feature provenance, and confounding audits available before downstream analyses.

Reason:
This prevents circularity, cherry-picking, and post-hoc mechanism naming. It also creates a defensible bridge from bulk molecular axes to single-cell, spatial, and later genetic anchoring.

Impact:
The project will produce strict Phase 2A deliverables before entering Phase 2B: `axis_evidence_matrix.tsv`, per-factor mechanism cards, factor redundancy, frozen gene programs, readiness audits, figures, and `Table_axis_prioritization_master.tsv`. GWAS, MR, LDSC, LAVA, colocalization, drug prediction, PPI, hub-gene, and LASSO analyses remain prohibited in Phase 2A.

## Decision 011

Question:
Should the project proceed directly to Phase 2B single-cell localization, and what is the statistical design?

Evidence:
Strict Phase 2A froze F1, F2, and F6 as primary skin axes and F7 as a supportive/systemic axis. CORE and EXTENDED gene programs are frozen before any single-cell, spatial, or genetics analysis. GSE228421 provides longitudinal 10x single-cell RNA-seq of skin biopsies from five individuals with severe psoriasis, including paired baseline lesional and nonlesional skin plus day 3 and day 14 lesional samples during risankizumab treatment.

Decision:
Proceed to Phase 2B using GSE228421 as the first single-cell validation dataset. Use CORE gene programs as the primary analysis and EXTENDED gene programs as sensitivity. Use donor/patient as the inference unit, with per-cell scores summarized into donor x cell-type pseudobulk or mean-score summaries.

Reason:
The current bottleneck is cell-type and cell-state anchoring of frozen bulk axes, not more bulk cohort discovery. GSE228421 directly tests whether skin-primary axes localize to keratinocyte, stromal, endothelial, myeloid, or other cell states under a paired baseline design.

Impact:
Phase 2B will not run GWAS, MR, LDSC, LAVA, colocalization, drug prediction, PPI, hub-gene, or LASSO analyses. Baseline lesional versus nonlesional paired donor comparisons are primary; day 3/day 14 treatment samples are sensitivity or perturbation evidence only.

## Decision 012

Question:
Does Phase 2B GSE228421 single-cell localization provide enough confidence to enter Phase 3 genetics?

Evidence:
All 20 official GSE228421 10x supplementary samples were downloaded and processed. The frozen F1/F2/F6/F7 CORE and EXTENDED programs were scored per QC-passing cell and summarized at donor x cell-type level. Baseline paired LS-vs-NL statistics used 5 donors as the inference unit. F1, F2, and F6 showed directional keratinocyte-positive LS-vs-NL effects, and F7 showed a directional NK/B-cell skin immune effect. CORE and EXTENDED pseudobulk correlations were high across axes. However, all four final Phase 2B confidence calls remained LOW because donor-level FDR thresholds were not met.

Decision:
Do not proceed to Phase 3 GWAS/MR/LDSC/LAVA/colocalization from Phase 2B alone. Classify the current result as NO-GO / SHRINK for genetics escalation, while retaining directional cell-type clues for refinement.

Reason:
The user’s locked GO standard required donor-level cell-type localization, CORE/EXTENDED consistency, plausible LS/NL biology, bulk replication, and MODERATE/HIGH mechanism naming confidence for at least several axes. GSE228421 provides useful directional evidence but not statistically robust donor-level localization under the frozen criteria.

Impact:
The manuscript should not claim validated cell-state mechanisms from current Phase 2B. The next defensible step is Phase 2B refinement with reference mapping and finer keratinocyte/immune-state annotation, or a cautious shrink to bulk tissue molecular programs before exploratory spatial support. GWAS, MR, LDSC, LAVA, colocalization, drug prediction, PPI, hub-gene, and LASSO remain prohibited.

## Decision 013

Question:
After low-confidence GSE228421 Phase 2B results, should the project shrink immediately to a bulk-only paper or proceed to additional transcriptomic validation?

Evidence:
GSE228421 has only 5 donors but showed directionally coherent keratinocyte LS-vs-NL effects for F1, F2, and F6, with F6 strongest. These are not sufficient for formal cell-state mechanism naming, but they do not justify abandoning cellular validation entirely. Local and official GEO audit show that GSE202011 is an independent spatial transcriptomics dataset with 30 samples and supplementary H5/image files; its GEO description states that it integrated matched psoriatic spatial samples with publicly available scRNA-seq datasets. The Nature Communications psoriasis single-cell/spatial paper supports the biological rationale for testing keratinocyte-layer, inflammatory fibroblast, and immune-state localization, but its exact scRNA resource must be audited separately rather than assumed to be GSE202011.

Decision:
Proceed to a bounded Phase 2B-R + Phase 2C block. Phase 2B-R will perform one high-resolution refinement of GSE228421. Phase 2C will use GSE202011 as independent spatial validation and will use an independent scRNA atlas only after its accession/processed object and donor metadata are identified. After this block, stop adding transcriptomic datasets and freeze mechanism confidence v2.

Reason:
This preserves the biological opportunity created by directional keratinocyte signals while preventing overfitting to the same 5 donors or endless dataset hunting. It also corrects the data-boundary issue that GSE202011 is spatial, not automatically the independent scRNA atlas.

Impact:
The project should not enter GWAS/MR yet, but genetics is not permanently blocked. Phase 3 can start after mechanism freeze v2 if frozen axis programs and claim boundaries are accepted, even if some axes remain replicated bulk molecular axes rather than perfect cell-state mechanisms.

## Decision 014

Question:
Which datasets are allowed for the final Phase 2B-R/2C transcriptomics validation block, and what accession boundaries prevent mislabeling or endless rescue?

Evidence:
Official GEO series matrices were parsed for GSE228421, GSE173706, GSE225475, and GSE202011. GSE228421 contains 20 psoriasis scRNA-seq samples from 5 donors with baseline lesional/nonlesional and treated lesional timepoints and has already been processed in Phase 2B. GSE173706 contains 33 single-cell samples with recoverable donor IDs and healthy, peripheral-normal/nonlesional, and psoriatic/lesional skin structure. GSE225475 contains 6 Visium spatial samples, with 2 healthy controls and 4 psoriasis skin sections, but no LS/NL pairing in GEO metadata. GSE202011 contains 30 spatial transcriptomics samples with healthy, PsO, and PsA skin and recoverable donor/sample labels; it is spatial transcriptomics, not a single-cell atlas. The local GSE202011 RAW tar is incomplete and cannot be analyzed until re-downloaded completely.

Decision:
Proceed with the locked Phase 2B-R/2C accession set only. Use GSE228421 for one-pass internal single-cell refinement, GSE173706 for independent single-cell validation after download and annotation strategy confirmation, GSE225475 for primary spatial localization after download, and GSE202011 for external spatial robustness after complete download. Do not introduce additional bulk RNA-seq, scRNA-seq, or spatial datasets solely to rescue weak mechanism naming after this block.

Reason:
This resolves the prior ambiguity that GSE202011 was spatial rather than the independent scRNA atlas and prevents silent substitution among related psoriasis resources. It preserves a final opportunity for cell/spatial triangulation while enforcing a hard stop before genetics.

Impact:
`DATA_MANIFEST.tsv` now distinguishes each accession and its role. `reports/PHASE2C_DATASET_ACCESSION_AUDIT.md` is the required gate before expression analysis. If downloaded files or annotations conflict with the audit, the affected dataset must be paused until resolved. GWAS, MR, LDSC, LAVA, colocalization, drug prediction, PPI, hub-gene, and LASSO remain prohibited until mechanism freeze v2 is written.

## Decision 015

Question:
After Phase 2B-R and Phase 2C, should the project upgrade F1/F2/F6/F7 into named cell-state mechanisms, proceed to genetics, or shrink the claim?

Evidence:
Phase 2B-R GSE228421 refinement kept all four axes at LOW confidence under donor-level criteria. GSE173706 independent scRNA validation provided directional support for keratinocyte inflammatory/stress states for F1/F2/F6 and B-cell/immune direction for F7, but all axes remained LOW after donor-level FDR control. GSE225475 primary spatial localization and GSE202011 external spatial robustness consistently placed F1/F2/F6 closest to keratinocyte stress/hypoxia spatial programs. F7 did not show coherent skin-spatial immune localization and remains better supported by previous blood/systemic evidence than by skin spatial data.

Decision:
Freeze mechanism confidence v2 as `SHRINK_TO_BULK_MOLECULAR_PROGRAMS_WITH_DIRECTIONAL_CELLULAR_SPATIAL_SUPPORT`. Do not formally name F1/F2/F6 as validated cell-state mechanisms. Retain F1/F2/F6 as frozen skin-primary bulk molecular axes with directional keratinocyte/spatial support. Retain F7 as a supportive/systemic axis only.

Reason:
The final transcriptomics validation block produced convergent biological direction but did not satisfy the locked standard for donor-level MODERATE/HIGH mechanism confidence. The correct manuscript move is to preserve the robust bulk-axis finding and report single-cell/spatial localization as supportive, not definitive.

Impact:
The final transcriptomics rescue attempt is complete. No additional bulk RNA-seq, scRNA-seq, or spatial transcriptomics datasets should be added solely to rescue mechanism naming. Phase 3 genetics may proceed only as frozen axis-gene-program genetics for bulk molecular programs; GWAS, MR, LDSC, LAVA, or colocalization results must not be used to rename axes or alter gene-program membership.

## Decision 016

Question:
How should Phase 3A genetic anchoring be locked before inspecting psoriasis GWAS enrichment results?

Evidence:
Mechanism freeze v2 concluded `SHRINK_TO_BULK_MOLECULAR_PROGRAMS_WITH_DIRECTIONAL_CELLULAR_SPATIAL_SUPPORT`. F1, F2, and F6 remain frozen skin-primary bulk molecular axes with directional keratinocyte/spatial support, while F7 remains supportive/systemic. The Phase 3A master prompt defines the objective as testing whether previously frozen molecular-axis gene programs capture inherited psoriasis susceptibility, and whether enrichment is axis-specific rather than a generic consequence of inflammatory gene composition, MHC effects, gene length, SNP density, or overlapping gene membership.

Decision:
Proceed to Phase 3A only as frozen gene-program genetic anchoring. CORE programs are primary and EXTENDED programs are sensitivity only. The primary phenotype is psoriasis susceptibility GWAS, with GCST90472771 as the primary GWAS after official metadata verification. The primary analysis is MAGMA competitive gene-set analysis with MHC excluded; MHC-included analysis is sensitivity. Stratified LDSC or partitioned heritability may be attempted only after technical appropriateness and reference-data feasibility are audited.

Reason:
This lock prevents circular reinterpretation. Genetic results can support or fail to support a frozen bulk molecular program, but they cannot rename axes, change gene membership, merge axes, choose CORE/EXTENDED status, or change MHC handling after results are known.

Impact:
Phase 3A starts with official GWAS metadata audit, raw summary-statistics download, checksum, metadata snapshot, manifest update, and formal summary-statistics QC. Multisystem comorbidity analysis, MR, causal mediator analysis, colocalization, drug-target analysis, PPI, hub-gene, and LASSO remain out of scope.

## Decision 017

Question:
Do the frozen F1/F2/F6/F7 psoriasis molecular-axis CORE programs show robust inherited psoriasis genetic anchoring?

Evidence:
GCST90472771 was audited from GWAS Catalog and downloaded from the official EMBL-EBI FTP. The raw file MD5 matched the official checksum and contained 11,808,957 variants, matching official REST metadata. Variants were mapped to the European 1000 Genomes MAGMA reference using GRCh37 chr:position:alleles, with 88.343% mapped. Primary MAGMA used NCBI37.3 gene body annotation and prespecified MHC exclusion (chr6:25,000,000-34,000,000). CORE/MHC-excluded competitive MAGMA did not identify FDR-significant enrichment for F1, F2, F6, or F7. Matched-null empirical tests using 2,000 random matched sets per axis were not significant. Shared-gene, unique-gene, and conditional comparative analyses did not provide robust axis-specific support.

Decision:
Freeze Phase 3A as `NO-GO_FOR_GENETICALLY_ANCHORED_AXES`. Assign all retained axes to Tier D for genetic anchoring. Do not proceed to axis-specific Phase 3B colocalization, MR, or Phase 4 multisystem comorbidity genetics as if F1/F2/F6/F7 are genetically anchored axes.

Reason:
The primary question was whether independently derived and transcriptomically frozen molecular programs capture distinct components of inherited psoriasis susceptibility. The frozen CORE gene programs did not pass primary MAGMA, matched-null, or conditional support. Nominal sensitivity signals, especially F2 EXTENDED/unique, are not sufficient because CORE remained non-robust and EXTENDED is sensitivity only.

Impact:
The project can continue only under a narrower genetics framing: replicated psoriasis molecular axes plus overall psoriasis genetic architecture, not axis-specific inherited susceptibility. Negative genetic anchoring should be reported as evidence that transcriptomic heterogeneity may be partly downstream, acquired, environmental, or disease-state related rather than germline-defined.

## Decision 018

Question:
After Phase 3A NO-GO, should the project continue trying to rescue axis-specific genetics or pivot to overall psoriasis multisystem shared genetics?

Evidence:
Phase 3A followed a prespecified frozen CORE/MHC-excluded MAGMA design using official GCST90472771 psoriasis GWAS summary statistics. F1, F2, F6, and F7 did not pass primary MAGMA FDR, matched-null empirical testing, shared/unique analysis, or conditional MAGMA. The strongest F2 signal remained nominal and sensitivity-level only. This blocks claims that the frozen transcriptomic axes are distinct inherited psoriasis susceptibility components. At the same time, prior phases still support reproducible skin-primary bulk molecular programs with directional cellular/spatial support and selective systemic evidence, so the project remains scientifically viable under a two-layer model.

Decision:
Accept Phase 3A as `NO-GO_FOR_GENETICALLY_ANCHORED_AXES` and stop axis-specific genetics rescue. Start Phase 4A as a separate analysis of overall psoriasis genetic liability across 10 prespecified multisystem comorbidities: psoriatic arthritis, Crohn disease, ulcerative colitis, coronary artery disease, ischemic stroke, type 2 diabetes, metabolic dysfunction-associated steatotic liver disease, major depression, uveitis, and chronic kidney disease.

Reason:
Trying more psoriasis GWAS datasets, EXTENDED gene sets, altered MAGMA windows, axis-specific MR, or axis-specific colocalization would increase researcher degrees of freedom after a clear negative primary test. A cleaner design separates the transcriptomic tissue-heterogeneity layer from the shared germline genetic architecture layer.

Impact:
Phase 4A exposure is overall psoriasis susceptibility GWAS liability, not F1/F2/F6/F7. LDSC genome-wide genetic correlation is the first analysis layer, LAVA local genetic correlation is the second layer, and shared loci/colocalization/MR are deferred to supported disease pairs. Transcriptomic axes can only be used later as exploratory contextualization of independently identified shared loci.

## Decision 019

Question:
How should Phase 4A be executed after locking the overall psoriasis shared-genetics route?

Evidence:
The user explicitly directed the project to enter `PHASE 4A — AUDIT AND HARMONIZE 10 COMORBIDITY GWAS + LDSC GENOME-WIDE GENETIC CORRELATION`, while preserving the boundary that F1/F2/F6/F7 cannot be used for axis-specific LDSC, LAVA, MR, colocalization, or genetic rescue. Web and GWAS Catalog/consortium source checks identified usable primary candidates for PsA, Crohn disease, ulcerative colitis, CAD, ischemic stroke, T2D, MDD, and CKD, with MASLD and uveitis requiring conditional handling because of phenotype-definition, access, or ancestry issues.

Decision:
Execute Phase 4A in three locked steps: first audit and lock the 10 outcome GWAS sources, then harmonize/munge all files into a common LDSC/HapMap3 framework with one QC report per GWAS, and only then run psoriasis x 10 outcome LDSC genome-wide genetic correlations. Phase 4A stops at LDSC rg. LAVA, shared loci, colocalization, MR, and transcriptomic contextualization are explicitly deferred.

Reason:
This preserves the frozen disease panel, avoids post-hoc disease switching, and prevents LDSC rg interpretation from being contaminated by downstream local or causal analyses. It also keeps MASLD and uveitis from being forced into weak or ancestry-mismatched primary analyses without audit.

Impact:
`reports/PHASE4A_AUDIT_AND_HARMONIZATION_LOCK.md`, `results/phase4a/phase4a_gwas_audit_matrix.tsv`, and `configs/phase4a_harmonization_spec.tsv` define the Phase 4A execution contract. Any replacement of a primary GWAS must be justified by access failure, essential-column failure, severe QC failure, ancestry mismatch, or phenotype mismatch before rg results are inspected.
