# Final submission checklist

Target journal: Communications Biology

Manuscript title: Molecular heterogeneity and multisystem shared genetic architecture define distinct biological layers of psoriasis

## Files prepared

| Item | File or location | Status |
| --- | --- | --- |
| Main manuscript | `manuscript/Communications_Biology_main_manuscript_v11_LANGUAGE_POLISHED.docx` | READY |
| Main manuscript source | `manuscript/Communications_Biology_main_manuscript_v11_LANGUAGE_POLISHED.md` | READY |
| Supplementary Information | `manuscript/Communications_Biology_Supplementary_Information_v6_FINAL_QA.docx` | READY |
| Supplementary Information source | `manuscript/Communications_Biology_Supplementary_Information_v6_FINAL_QA.md` | READY |
| Cover letter | `submission/cover_letter_communications_biology.md` | READY |
| Submission declarations | `submission/declarations_for_submission_system.md` | READY |
| Main figures | `results/figures/communications_biology_final/Figure1-6.{svg,pdf,png}` | READY |
| Main figure source data | `results/figures/communications_biology_final/source_data/` | READY |
| Main table source data | `source_data/` and `manuscript/tables/` | READY |
| Supplementary data | `manuscript/supplementary_data/` | READY |
| Supplementary figures | `manuscript/supplementary_figures/` | READY |
| Supplementary tables | `manuscript/supplementary_tables/` | READY |
| Repository release tag | `v1.0.0-submission` | READY TO CREATE ON GITHUB PUSH |

## Submission-system fields

| Field | Status | Notes |
| --- | --- | --- |
| Authorship approval | READY | Text in `submission/declarations_for_submission_system.md` |
| Ethics statement | READY | Public/access-controlled secondary data only |
| Consent for publication | READY | Not applicable |
| Competing interests | READY | No competing interests |
| Funding | READY | No specific funding |
| Acknowledgements | READY | None |
| Data availability | READY | Includes data restrictions and repository paths |
| Code availability | READY | Points to GitHub and `v1.0.0-submission` |
| AI-use statement | NOT ADDED | Add only if the journal submission system explicitly requires it |
| Zenodo DOI | OPTIONAL AFTER RELEASE | GitHub release tag is sufficient for current upload; Zenodo can be bound after final GitHub release if desired |

## Exclusions from GitHub upload

The repository intentionally excludes large or restricted inputs:

- raw transcriptomic matrices;
- GWAS summary statistics and munged large intermediates;
- LD reference files;
- GTEx BESD source files and large index/source resources;
- virtual environments and tool binaries;
- rendered QA page images;
- macOS AppleDouble `._*` files and local Office lock files.

## Final local QA

| Check | Status |
| --- | --- |
| v11 manuscript language QA | PASS |
| v11 claim preservation audit | PASS |
| v11 DOCX render QA | PASS |
| Supplementary Information v6 final QA | PASS |
| Main figure redesign/source-data audit | PASS |
| Data/code restriction wording | READY |

Current status: READY_FOR_GITHUB_SUBMISSION_UPLOAD
