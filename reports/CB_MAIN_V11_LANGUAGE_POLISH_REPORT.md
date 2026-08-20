# Communications Biology Main Manuscript v11 Language Polish

Status: `LANGUAGE_POLISHED_RENDER_QA_PASS`

Source: `manuscript/Communications_Biology_main_manuscript_v10_FINAL_LOW_LEVEL_QA.md`

Outputs:
- `manuscript/Communications_Biology_main_manuscript_v11_LANGUAGE_POLISHED.md`
- `manuscript/Communications_Biology_main_manuscript_v11_LANGUAGE_POLISHED.docx`

Scope:
- Polished confusing or mechanically repeated sentences across the main manuscript.
- Reduced defensive phrasing while retaining necessary methodological boundaries.
- Preserved all core numerical results, dataset accessions, figure/table structure and reference numbering.
- Removed em and en dashes from the Markdown source.

Main editorial decisions:
- Abstract now states the main separation of tissue states and inherited liability in a more direct final sentence.
- Introduction keeps the same four-paragraph logic but smooths transitions between tissue maps and genetic maps.
- Results now reports observations more directly and avoids repeated "not" constructions where a positive scope statement is clearer.
- Discussion keeps the layered interpretation but makes the CAD, IBD and colocalization paragraphs less defensive and easier to follow.
- Ethics/Data/Code sections were lightly tightened without changing availability statements.

Checks written:
- `reports/CB_MAIN_V11_LANGUAGE_POLISH_TERMINOLOGY_LEDGER.tsv`
- `reports/CB_MAIN_V11_LANGUAGE_POLISH_STYLE_AUDIT.tsv`
- `reports/CB_MAIN_V11_CLAIM_PRESERVATION_AUDIT.tsv`

Render QA:
- DOCX rendered successfully during final local QA.
- Rendered page count: 17.
- Visual spot checks covered the title/abstract page, figure-to-discussion transition, table pages and reference pages.
- The Tables section starts on a new page to avoid orphaned table headers.
