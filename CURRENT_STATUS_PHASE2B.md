# 当前情况：Phase 2B GSE228421 单细胞定位

更新时间：2026-08-11

## 一句话结论

Phase 2B 已完成 GSE228421 donor-level single-cell localization。F1、F2、F6 在 baseline lesional versus non-lesional 比较中均显示 keratinocyte 正向趋势，F7 显示皮肤免疫细胞趋势，但四条轴均未达到 donor-level FDR 显著，因此当前结论是 **NO-GO / SHRINK for genetics escalation**，暂不进入 GWAS/MR/LDSC/LAVA/coloc。

## 数据与统计锁定

- 数据集：GSE228421。
- 设计：5 名 severe psoriasis donor，baseline lesional/non-lesional，risankizumab day 3/day 14 lesional timepoints。
- 输入：Phase 2A 冻结的 F1、F2、F6、F7 CORE 和 EXTENDED gene programs。
- 主分析：baseline paired LS-vs-NL。
- 敏感性分析：day 3/day 14 treatment timepoint shift。
- 统计单位：donor/patient，不使用 cell-level n 作为显著性重复。
- 注释策略：marker-based coarse cell-type annotation，后续仍需 refined annotation/reference mapping。

## 主要结果表

| Axis | Dominant cell | Secondary cell | Donor effect | 95% bootstrap CI | FDR | CORE/EXTENDED rho | Confidence |
|---|---|---|---:|---|---:|---:|---|
| F1 | keratinocyte | T_cell | 0.035 | 0.025 to 0.046 | 0.364 | 0.955 | LOW |
| F2 | keratinocyte | NK_cell | 0.015 | 0.010 to 0.020 | 0.364 | 0.973 | LOW |
| F6 | keratinocyte | NK_cell | 0.049 | 0.039 to 0.062 | 0.364 | 0.946 | LOW |
| F7 | NK_cell | B_cell | 0.121 | 0.009 to 0.259 | 0.424 | 0.976 | LOW |

解释：

- F1/F2/F6 的方向与 keratinocyte/stress skin-primary 线索一致，但 donor 数只有 5，精确符号检验和多细胞类型 FDR 后不能作为正式机制定位。
- F7 没有在皮肤中显示明确 monocyte/myeloid 定位；当前仍应主要依赖 bulk blood support，将其称为 supportive/systemic axis。
- CORE 与 EXTENDED 的 pseudobulk concordance 很高，说明 gene-program scoring 稳定，但不能弥补 donor-level 显著性不足。

## 当前 GO/NO-GO

状态：**NO-GO / SHRINK for Phase 3 genetics escalation**

含义：

- 暂不启动 GWAS、MR、LDSC、LAVA、coloc、drug prediction、PPI、hub gene 或 LASSO。
- 不应把 F1/F2/F6/F7 写成已经明确定位的 cell-state mechanisms。
- 可以写作：bulk tissue molecular axes show directional cell-type clues in GSE228421, especially keratinocyte-associated LS-vs-NL shifts for F1/F2/F6.

## 路线更新：Phase 2B-R + Phase 2C

当前不直接进入 Phase 3 genetics，也不只在 GSE228421 上无限精修。新的正式路线是一个有停止规则的 Phase 2B-R + Phase 2C block：

```text
Phase 2B complete
GSE228421 low-confidence directional clues
        ↓
Phase 2B-R
one-pass high-resolution refinement of GSE228421
        ↓
Phase 2C
GSE202011 independent spatial validation
        +
independent scRNA validation only after exact accession/object audit
        ↓
Stop adding transcriptomic datasets
        ↓
Mechanism freeze v2
        ↓
Phase 3 genetics only after claim boundary is accepted
```

Phase 2B-R 只允许做一次有限精炼：

- keratinocyte：basal、spinous/suprabasal、proliferative、inflammatory、IFN-response、stress/hypoxia；
- fibroblast：inflammatory versus homeostatic/stromal；
- myeloid：monocyte/macrophage/DC；
- T/NK：粗分到足够评估 F7。

GSE202011 的当前审计结论：

- 本地和 GEO metadata 显示 GSE202011 是 spatial transcriptomics 数据集；
- 共 30 个样本；
- 本地 series matrix 拆分为 Healthy 7、PSO lesional 7、PSO non-lesional 5、PSA lesional 7、PSA non-lesional 4；
- supplementary 包括 `GSE202011_RAW.tar` 和 `GSE202011_st_images.tar.gz`；
- 不能直接把 GSE202011 称为 67,378-cell scRNA atlas，独立 scRNA 对象/ accession 需要另行确认。

停止规则：

如果 Phase 2B-R + Phase 2C 后仍无法明确 cell state，则停止继续寻找 transcriptomic datasets，并把相关轴永久写成 bulk tissue molecular axis with directional cellular clues。

## 主要文件

- `reports/PHASE2B_GSE228421_SINGLE_CELL_LOCALIZATION.md`
- `results/phase2b/Table_phase2b_axis_cell_localization.tsv`
- `results/phase2b/GSE228421_baseline_LS_vs_NL_donor_statistics.tsv`
- `results/phase2b/GSE228421_cell_type_localization.tsv`
- `results/phase2b/GSE228421_donor_celltype_axis_scores.tsv`
- `results/phase2b/GSE228421_treatment_timepoint_sensitivity.tsv`
- `results/phase2b/GSE228421_program_dropout_robustness.tsv`
- `results/figures/phase2b/Figure3A_GSE228421_axis_celltype_localization.png`
- `results/figures/phase2b/Figure3B_GSE228421_donor_paired_effects.png`
- `reports/PHASE2BR_2C_STOP_RULE_ROADMAP.md`
- `results/phase2br_2c/GSE202011_spatial_sample_audit.tsv`
- `results/phase2br_2c/GSE202011_spatial_sample_summary.tsv`
