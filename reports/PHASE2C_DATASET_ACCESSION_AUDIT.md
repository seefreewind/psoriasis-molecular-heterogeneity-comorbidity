# Phase 2C Dataset Accession Audit

本报告在进入 Phase 2B-R/2C 任何表达矩阵分析前生成，目的为锁定 accession、技术类型、样本结构和适用边界。所有判断均基于本地保存的官方 GEO series matrix 与项目内既有结果文件；未能从 series matrix 直接确认的信息标记为 unresolved，而不作隐含替代。

## 总体结论

- GSE228421：继续作为 Phase 2B-R 的内部单细胞精修数据集，不作为独立验证。
- GSE173706：可作为独立 psoriasis scRNA-seq 验证候选；donor、健康/PN/PP 样本结构可从 GEO metadata 恢复，但作者整合对象和细胞注释未在 series matrix 中直接显示，下载后需要透明注释策略。
- GSE225475：可作为 primary spatial localization 候选；它是 6 个 Visium 空间样本，不是单细胞，且 GEO metadata 不支持 LS/NL 配对分析。
- GSE202011：可作为 external spatial robustness；它是 psoriasis/PsA 空间转录组数据集，不得再描述为单细胞 atlas。本地 RAW tar 目前是不完整下载，分析前必须重新完整获取。

## 审计表

| Accession | Role | Technology | Samples | Donor status | Tissue/disease states | Matrix | Annotation | Suitability |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| GSE228421 | Phase 2B-R internal/mechanistic refinement scRNA-seq dataset | 10x Genomics single-cell RNA-seq | 20 | recoverable (5 unique derived IDs) | lesional=15; nonlesional=5 | available_from_GEO_supplementary | not_apparent_from_series_matrix | SUITABLE_FOR_PHASE2B_R |
| GSE173706 | Phase 2C independent single-cell validation atlas | single-cell RNA-seq with associated spatial-sequencing study | 33 | recoverable (23 unique derived IDs) | healthy=8; lesional=14; nonlesional=11 | available_from_GEO_supplementary | not_apparent_from_series_matrix | SUITABLE_PENDING_DOWNLOAD_AND_ANNOTATION_STRATEGY |
| GSE225475 | Phase 2C primary spatial localization candidate | 10x Visium spatial transcriptomics | 6 | not recoverable from parsed metadata | healthy=2; psoriasis_unqualified=4 | available_from_GEO_supplementary | not_apparent_from_series_matrix | SUITABLE_PENDING_DOWNLOAD |
| GSE202011 | Phase 2C external spatial robustness dataset | spatial transcriptomics | 30 | recoverable (9 unique derived IDs) | healthy=7; lesional=14; nonlesional=9 | available_from_GEO_supplementary | not_apparent_from_series_matrix | SUITABLE_PENDING_COMPLETE_DOWNLOAD |

## 数据集边界

### GSE228421

- Official URL: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE228421
- Title: Using single-cell transcriptomics to characterise early mechanisms of psoriasis resolution
- PubMed ID(s): 38291032
- DOI: not_resolved_from_series_matrix
- Repository: NCBI GEO
- Technology: 10x Genomics single-cell RNA-seq
- Role: Phase 2B-R internal/mechanistic refinement scRNA-seq dataset
- Samples/cells/spots: 20 samples; cell/spot count not resolved from series matrix.
- LS/NL/healthy and PsO/PsA: lesional=15; nonlesional=5; PsO=20
- Pairing/donor ID: recoverable (5 unique derived IDs); paired/repeated donor samples apparent
- Treatment/timepoint: risankizumab baseline/day3/day14; baseline=10; day14=5; day3=5
- Matrix availability: available_from_GEO_supplementary
- Processed object: not_apparent_or_not_author_integrated_object
- Cell annotation: not_apparent_from_series_matrix
- Spatial image: not_applicable_or_not_apparent
- Suitability: SUITABLE_FOR_PHASE2B_R
- Limitation: Already processed locally; suitable only for one-pass refinement, not independent validation.

### GSE173706

- Official URL: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE173706
- Title: Single Cell and Spatial Sequencing Characterizes Cell Type Composition and Cell-Cell Interaction in Psoriasis
- PubMed ID(s): 35862195;38051587;40164604
- DOI: not_resolved_from_series_matrix
- Repository: NCBI GEO
- Technology: single-cell RNA-seq with associated spatial-sequencing study
- Role: Phase 2C independent single-cell validation atlas
- Samples/cells/spots: 33 samples; cell/spot count not resolved from series matrix.
- LS/NL/healthy and PsO/PsA: healthy=8; lesional=14; nonlesional=11; Healthy=8; PsO=25
- Pairing/donor ID: recoverable (23 unique derived IDs); paired/repeated donor samples apparent
- Treatment/timepoint: baseline/cross-sectional or not reported; not_reported=33
- Matrix availability: available_from_GEO_supplementary
- Processed object: not_apparent_or_not_author_integrated_object
- Cell annotation: not_apparent_from_series_matrix
- Spatial image: not_applicable_or_not_apparent
- Suitability: SUITABLE_PENDING_DOWNLOAD_AND_ANNOTATION_STRATEGY
- Limitation: Independent scRNA validation candidate; author-integrated object/cell annotations are not apparent in the series matrix, so analysis must use downloadable sample matrices plus transparent annotation or separately verified annotations.

### GSE225475

- Official URL: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE225475
- Title: Single Cell and Spatial Sequencing Define Processes by which Keratinocytes and Fibroblasts Amplify Inflammatory Responses in Psoriasis
- PubMed ID(s): 37308489
- DOI: 10.1038/s41467-023-39020-4
- Repository: NCBI GEO
- Technology: 10x Visium spatial transcriptomics
- Role: Phase 2C primary spatial localization candidate
- Samples/cells/spots: 6 samples; cell/spot count not resolved from series matrix.
- LS/NL/healthy and PsO/PsA: healthy=2; psoriasis_unqualified=4; Healthy=2; PsO=4
- Pairing/donor ID: not recoverable from parsed metadata; no donor-level pairing apparent
- Treatment/timepoint: baseline/cross-sectional or not reported; not_reported=6
- Matrix availability: available_from_GEO_supplementary
- Processed object: not_apparent_or_not_author_integrated_object
- Cell annotation: not_apparent_from_series_matrix
- Spatial image: not_applicable_or_not_apparent
- Suitability: SUITABLE_PENDING_DOWNLOAD
- Limitation: Primary spatial candidate; small unpaired healthy-vs-psoriasis Visium design, no LS/NL pairing in GEO sample metadata.

### GSE202011

- Official URL: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE202011
- Title: Spatial transcriptomics stratifies psoriatic disease by emergent cellular ecosystems
- PubMed ID(s): 37267384;41743834
- DOI: not_resolved_from_series_matrix
- Repository: NCBI GEO
- Technology: spatial transcriptomics
- Role: Phase 2C external spatial robustness dataset
- Samples/cells/spots: 30 samples; cell/spot count not resolved from series matrix.
- LS/NL/healthy and PsO/PsA: healthy=7; lesional=14; nonlesional=9; Healthy=7; PsA=11; PsO=12
- Pairing/donor ID: recoverable (9 unique derived IDs); paired/repeated donor samples apparent
- Treatment/timepoint: baseline/cross-sectional or not reported; not_reported=30
- Matrix availability: available_from_GEO_supplementary
- Processed object: not_apparent_or_not_author_integrated_object
- Cell annotation: not_apparent_from_series_matrix
- Spatial image: available_or_indicated
- Suitability: SUITABLE_PENDING_COMPLETE_DOWNLOAD
- Limitation: External spatial robustness dataset; must not be described as a single-cell atlas. Local RAW tar is incomplete and cannot be analyzed.

## STOP 规则

若下载后的实际文件与本审计的样本结构不一致，相关数据集立即停止使用，直到 accession、样本标签、donor ID、矩阵格式和注释来源被重新解析并记录。不得用其他数据集静默替换。

本阶段是最后一次 transcriptomics rescue attempt。Phase 2B-R/2C 完成后，不能再仅为挽救机制命名而引入新的 bulk RNA、scRNA 或 spatial 数据集。
