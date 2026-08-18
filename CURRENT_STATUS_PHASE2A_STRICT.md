# 当前情况总结：Phase 2A 严格冻结版

更新时间：2026-08-11

## 一句话结论

项目已完成 Phase 1B 连续 molecular axes 救援，并完成严格版 Phase 2A 轴筛选、机制证据卡、冗余分析、CORE/EXTENDED gene program 冻结、single-cell/spatial readiness 审计和 Figure 2 草图。当前结论是：

**CONDITIONAL GO TO PHASE 2B**

可以进入 donor-level single-cell localization，但还不能宣称强机制命名、遗传锚定或多系统共病机制已经成立。

## 当前论文边界

当前主线应写作：

> Skin-primary continuous molecular axes of psoriasis with selective systemic blood support.

暂时不能作为当前结果主张：

- strong replicated cross-tissue endotypes
- clinically validated endotypes
- discrete patient subtypes
- causal comorbidity mechanisms
- therapeutic targets
- genetically anchored axes

这些可以作为后续目标，但不能写成已经完成的发现。

## Phase 2A 最终轴角色

| Factor | Final role | Dominant tissue | Candidate domain | Name confidence | Next use |
|---|---|---|---|---|---|
| F1 | PRIMARY AXIS | LS | metabolic/hypoxia-stress-like lesional skin axis | LOW | Phase 2B single-cell |
| F2 | PRIMARY AXIS | NL | stromal/repair-remodeling-like nonlesional skin axis | LOW | Phase 2B single-cell |
| F3 | SECONDARY AXIS | BLD | T17/NF-kB inflammatory-like blood axis | MODERATE | supplementary/review |
| F4 | UNINTERPRETABLE / RETIRE | BLD | DNA-damage/chromatin-like blood factor | LOW | retire from main story |
| F5 | SECONDARY AXIS | LS | stromal/repair-remodeling-like lesional skin axis | LOW | supplementary/review |
| F6 | PRIMARY AXIS | LS | metabolic/hypoxia-stress skin axis | MODERATE | Phase 2B single-cell |
| F7 | SUPPORTIVE/SYSTEMIC AXIS | BLD | IFN/antiviral-myeloid systemic blood candidate | LOW | Phase 2B systemic validation |
| F8 | SECONDARY AXIS | NL | growth-factor/stromal-remodeling nonlesional axis | LOW | supplementary/review |

## 保留进入 Phase 2B 的轴

进入 single-cell localization：

- F1
- F2
- F6
- F7

其中：

- F1、F2、F6 是 skin-primary axes。
- F7 是 supportive/systemic axis，不应强行写成 skin-primary。

## Frozen gene programs

已冻结 CORE/EXTENDED gene programs：

| Factor | CORE genes | EXTENDED genes | File |
|---|---:|---:|---|
| F1 | 304 | 809 | `results/phase2a/axis_gene_programs/F1_gene_program.tsv` |
| F2 | 725 | 1184 | `results/phase2a/axis_gene_programs/F2_gene_program.tsv` |
| F6 | 134 | 544 | `results/phase2a/axis_gene_programs/F6_gene_program.tsv` |
| F7 | 232 | 507 | `results/phase2a/axis_gene_programs/F7_gene_program.tsv` |

这些 gene programs 已冻结，后续 single-cell、spatial、MAGMA、LDSC、eQTL/colocalization 只能使用这些预先定义的集合或预先记录的敏感性规则，不能根据未来显著性结果回头改。

## 外部支持状态

### Skin replication

GSE244679 提供最强独立配对皮肤支持：

| Factor | Strongest support |
|---|---:|
| F1 | 0.688 |
| F2 | 0.518 |
| F6 | 0.375 |
| F3 | 0.356 |
| F5 | 0.355 |

F1、F2、F6 因此保留为 primary skin axes。

### Blood/systemic support

F7 是最明确的 systemic candidate：

- internal skin-blood support: 0.577
- GSE61281 strongest support: 0.455
- GSE147339 support weak

GSE61281 是 cross-platform microarray support，不是 design-matched blood replication。

## 混杂边界

当前没有证据显示保留轴主要由 PASI、BMI、age、sex 或 HLA-C*06:02 驱动。

但要注意：

- batch association 当前模型中不可用。
- F3 的 BMI partial R2 相对较高，需在 supplementary 中谨慎解释。
- F1/F2/F7 命名置信度仍低，不能跳过 single-cell 直接正式命名。

## 已生成的主要文件

### 报告

- `reports/PHASE2A_AXIS_MECHANISM_PRIORITIZATION.md`
- `reports/mechanism_cards/F1.md`
- `reports/mechanism_cards/F2.md`
- `reports/mechanism_cards/F3.md`
- `reports/mechanism_cards/F4.md`
- `reports/mechanism_cards/F5.md`
- `reports/mechanism_cards/F6.md`
- `reports/mechanism_cards/F7.md`
- `reports/mechanism_cards/F8.md`

### 表格

- `results/phase2a/axis_evidence_matrix.tsv`
- `results/phase2a/Table_axis_prioritization_master.tsv`
- `results/phase2a/factor_redundancy.tsv`
- `results/phase2a/axis_gene_program_summary.tsv`
- `results/phase2a/axis_gene_program_overlap.tsv`
- `results/phase2a/single_cell_readiness.tsv`
- `results/phase2a/candidate_single_cell_dataset_audit.tsv`
- `results/phase2a/candidate_spatial_dataset_audit.tsv`

### Gene programs

- `results/phase2a/axis_gene_programs/F1_gene_program.tsv`
- `results/phase2a/axis_gene_programs/F2_gene_program.tsv`
- `results/phase2a/axis_gene_programs/F6_gene_program.tsv`
- `results/phase2a/axis_gene_programs/F7_gene_program.tsv`

### Figures

- `results/figures/Figure2A_axis_evidence_matrix.png`
- `results/figures/Figure2A_axis_evidence_matrix.svg`
- `results/figures/Figure2B_retained_axis_gene_programs.png`
- `results/figures/Figure2B_retained_axis_gene_programs.svg`
- `results/figures/Figure2C_tissue_contribution.png`
- `results/figures/Figure2C_tissue_contribution.svg`
- `results/figures/Figure2D_external_replication_support.png`
- `results/figures/Figure2D_external_replication_support.svg`
- `results/figures/Figure2E_primary_axis_schematic.png`
- `results/figures/Figure2E_primary_axis_schematic.svg`

## 候选下一阶段数据

### Single-cell candidate

GSE228421 已完成 series-matrix 元数据审计。

当前判断：

- 有 lesional/nonlesional 信息。
- 有 timepoint/treatment 相关信息。
- 可作为 Phase 2B 候选。
- 需要进一步确认 donor metadata 和可用表达矩阵。
- 后续统计单位必须是 donor/patient，不是 cell。

### Spatial candidate

GSE202011 已完成 series-matrix 元数据审计。

当前判断：

- 有 psoriasis lesional/nonlesional 信息。
- 有 patient/section 信息。
- 可作为 spatial readiness 候选。
- 后续不能把 spot/section 当成独立患者。

## 下一步

进入 Phase 2B：

> Bulk frozen axis gene program → per-cell scoring → cell-type pseudobulk / donor summary → donor-level statistical testing.

优先问题：

1. F1 是否定位到 keratinocyte/stress 或 epidermal metabolic state？
2. F2 是否定位到 fibroblast/endothelial/repair 或 nonlesional stromal state？
3. F6 是否定位到 keratinocyte hypoxia/stress 或 epithelial response state？
4. F7 是否定位到 myeloid/monocyte/neutrophil/IFN-response systemic immune state？

## 暂时不要做

Phase 2A 后仍然不要立即做：

- GWAS
- MR
- LDSC / LAVA
- colocalization
- drug prediction
- PPI / hub gene
- LASSO
- comorbidity genetics

这些必须等 Phase 2B 单细胞定位完成后再进入。

## 验证状态

测试已通过：

```bash
environment/phase1b_venv/bin/python -m pytest tests
```

结果：

```text
9 passed
```

## 当前最终判断

**CONDITIONAL GO TO PHASE 2B**

项目值得继续，但必须严格控制 claim 强度。当前已经有足够证据进入 single-cell localization；还没有足够证据宣称遗传锚定、多系统共病机制或临床转化结论。
