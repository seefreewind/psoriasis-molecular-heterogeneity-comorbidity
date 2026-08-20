# CB Figure 6 Count And Unit Audit

| displayed_count | scientific_unit | unique_or_nonunique | subset_relation_to_previous_stage | source | allowed_visual_representation |
|---:|---|---|---|---|---|
| 122 | FDR-supported local-rg locus-trait pairs | nonunique across traits; summed across CAD/PsA/Crohn/UC | no | phase4b_restricted_lava_summary.tsv | Evidence cascade layer |
| 91 | SMR/HEIDI-prioritized outcome-gene pairs | unique outcome-gene pairs | partial | phase4c_frozen_shared_locus_eqtl_gene_table.tsv | Next evidence layer, not a one-to-one subset |
| 33 | highest-tier outcome-gene pairs (30 unique genes) | unique outcome-gene pairs | partial | phase4c_frozen_shared_locus_eqtl_gene_table.tsv | Highest-tier prioritization node |
| 15 | restricted colocalization outcome-gene-tissue pairs | unique outcome-gene-tissue pairs | partial | phase4d_coloc_supported_and_suggestive_candidates.tsv | Colocalization layer |
| 5 | PP4-supported outcome-gene-tissue pairs | nonunique genes; tissue-specific tests | parallel coloc category | phase4d_coloc_supported_and_suggestive_candidates.tsv | Parallel branch |
| 10 | suggestive outcome-gene-tissue pairs | nonunique genes; tissue-specific tests | parallel coloc category | phase4d_coloc_supported_and_suggestive_candidates.tsv | Parallel branch |

Conclusion: panel a uses an evidence cascade rather than a literal geometric funnel because the unit changes across layers.
Supported and suggestive colocalization outcomes are parallel categories within the restricted colocalization layer.
