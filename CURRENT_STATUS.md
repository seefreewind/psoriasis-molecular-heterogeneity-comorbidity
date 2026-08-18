# 当前情况总结

更新时间：2026-08-11

## 一句话结论

Phase 1B 已经完成连续分子轴救援，并完成用户选择的两项外部支持工作：GSE244679 配对皮肤外部复制，以及 GSE147339/GSE61281 血液外部支持。Phase 2A 已完成轴筛选、机制卡和 CORE/EXTENDED gene-program freeze。Phase 2B 已完成 GSE228421 donor-level single-cell localization；结果支持 F1/F2/F6 的 keratinocyte 方向性线索和 F7 的皮肤免疫方向性线索，但四条轴均未达到 donor-level FDR 显著。当前路线已更新为有停止规则的 Phase 2B-R + Phase 2C，而不是直接进入 genetics。

## 当前 GO/NO-GO 状态

状态：NO-GO / SHRINK FOR PHASE 3 GENETICS ESCALATION FROM PHASE 2B ALONE

含义：

- 可以继续推进皮肤主导的 molecular axis 论文框架。
- 不建议继续使用“强多系统 endotype”“跨组织复制 endotype”作为主张。
- Phase 2B 只支持方向性 cell-type clues，不支持正式 cell-state mechanism naming。
- GWAS/MR/共定位/多系统共病阶段继续暂不启动。
- 下一步只允许一个 bounded transcriptomics block：GSE228421 有限高分辨率精炼 + GSE202011 spatial validation + 另行审计后的 independent scRNA validation。

## 已完成的核心工作

- 完成 E-MTAB-14509 官方元数据、样本、组织、队列和泄漏检查。
- 完成 Phase 1 早期离散聚类分析，结果显示 k=2 结构存在但稳定性不足，不适合作为强 endotype 主结果。
- 完成 Phase 1B 连续分子轴救援：
  - 使用 Python MOFA2 / `mofapy2`。
  - discovery complete-case 为 76 名患者。
  - 三个视图：lesional skin、nonlesional skin、whole blood。
  - 5 个随机种子均收敛。
  - F1-F8 八个轴在当前特征过滤下均为 robust。
- 完成 E-MTAB-14509 内部皮肤复制投影。
- 完成外部 GEO 数据集审计。
- 完成 GSE244679 配对皮肤 RNA-seq 下载、解包和复制分析。
- 完成 GSE147339 whole-blood RNA-seq 支持分析。
- 完成 GSE61281 Agilent microarray 血液支持分析，并使用 GPL6480 平台注释将探针映射到 gene symbol。
- 完成严格版 Phase 2A 轴筛选、mechanism cards、redundancy、gene-program freeze、single-cell/spatial readiness、Figure 2 草图和 master table。
- 冻结 3 条 primary skin axes：F1、F2 和 F6。
- F7 被单独保留为 supportive/systemic axis。
- 完成 GSE228421 20 个 10x supplementary sample 下载、QC、marker-based coarse annotation、CORE/EXTENDED scoring、donor x cell-type pseudobulk summary、baseline paired LS-vs-NL statistics、treatment/timepoint sensitivity 和 Phase 2B figures。

## 外部数据处理状态

| 数据集 | 组织 | 技术 | 当前状态 | 作用 |
|---|---|---|---|---|
| GSE121212 | skin | RNA-seq | 已下载并分析 | 配对皮肤支持，信号弱 |
| GSE244679 | skin | RNA-seq | 已完整下载并分析 | 独立配对皮肤复制，信号较强 |
| GSE54456 | skin | RNA-seq | 已下载 | unpaired skin support 候选 |
| GSE147339 | whole blood | RNA-seq | 已下载并分析 | 外部血液支持，信号弱 |
| GSE61281 | whole blood | Agilent microarray | 已完成平台映射并分析 | 外部血液支持，F7 信号较稳定 |

## 关键结果

### GSE244679：独立配对皮肤复制

GSE244679 包含 24 对 lesional psoriatic skin 与 adjacent normal skin。分析使用冻结的 Phase 1B gene-set 定义，将外部样本转换为 pathway/regulon/cell-state/signaling 分数，并与 discovery MOFA 轴 loading 做相关。

最强结果如下：

| 轴 | 视图 | 绝对 Spearman 相关 |
|---|---|---:|
| F1 | LS | 0.688 |
| F2 | NL | 0.518 |
| F6 | LS | 0.375 |
| F3 | NL | 0.356 |
| F5 | LS | 0.355 |

解释：

GSE244679 明显加强了皮肤主导 molecular axes 的外部证据，尤其支持 F1、F2、F6、F3、F5 等轴在独立配对皮肤数据中的可重复性。由于 MOFA latent factor 的方向符号本身可任意翻转，相关方向不应直接解释为生物学正负方向，除非后续把轴锚定到明确表型或机制。

### GSE147339：whole-blood RNA-seq 支持

GSE147339 包含 10 个 psoriasis 与 10 个 control whole-blood RNA-seq 样本。

结果整体较弱，最大绝对相关约为 0.173。

解释：

该数据集样本量小，能够作为外部血液支持的可行性检查，但不能单独支撑强血液复制结论。

### GSE61281：whole-blood microarray 支持

GSE61281 包含 20 个 PsA、20 个 cutaneous psoriasis without arthritis、12 个 unaffected controls。平台为 GPL6480。分析已将 30,723 个有 gene symbol 的探针聚合到 19,553 个 gene symbols。

最强结果如下：

| 对比 | 最强轴 | 绝对 Spearman 相关 |
|---|---|---:|
| psoriasis spectrum vs control | F7 | 0.455 |
| PsA vs control | F7 | 0.436 |
| PsC vs control | F7 | 0.400 |
| psoriasis spectrum vs control | F3 | 0.262 |
| PsA vs control | F2 | 0.258 |

解释：

GSE61281 对 F7 的血液支持最稳定，F3 和 F2 也有较小支持。但该数据集是 Agilent two-color microarray，且病例构成为 PsA/PsC/control，与 E-MTAB-14509 的 RNA-seq 设计不完全匹配。因此它应写作“外部血液支持”，不应写作“设计匹配的血液复制”。

## 当前证据边界

可以支持的表述：

- Skin-primary continuous molecular axes in psoriasis。
- Continuous molecular axes are more defensible than discrete patient endotypes。
- Independent paired-skin external data support several axes。
- Blood data provide supportive, cross-platform evidence for selected axes, especially F7 in GSE61281。

不建议支持的表述：

- Strong replicated multisystem endotypes。
- Fully replicated cross-tissue endotypes。
- Clinically validated endotypes。
- Causal mechanisms or therapeutic targets without additional validation。
- Comorbidity-driving mechanisms before GWAS/MR/colocalization or independent multisystem validation。

## Phase 2A 轴筛选结果

| 轴 | 当前等级 | 主导视图 | 候选解释 | 当前命名状态 |
|---|---|---|---|---|
| F1 | primary skin axis | LS | metabolic/hypoxia-stress-like skin axis | descriptive card only |
| F2 | primary skin axis | NL | stromal/repair-remodeling-like nonlesional axis | descriptive card only |
| F6 | primary skin axis | LS | metabolic/hypoxia-stress skin axis | eligible for cautious mechanism naming |
| F7 | supportive/systemic axis | BLD | IFN/antiviral-myeloid systemic candidate | descriptive card only |
| F3 | supplementary review | BLD | T17/NF-kB inflammatory-like blood axis | eligible for cautious mechanism naming |
| F5 | supplementary review | LS | stromal/repair-remodeling-like skin axis | descriptive card only |
| F8 | supplementary review | NL | stromal/repair-remodeling-like nonlesional axis | descriptive card only |
| F4 | uninterpretable / retire | BLD | DNA-damage/chromatin-like blood factor | descriptive card only |

解释：

Phase 2A 不把候选解释当作最终机制命名。正式命名仍需要 Phase 2B 单细胞 donor-level localization 支持，尤其要避免仅凭 Reactome-heavy loading 给轴贴机制标签。

## Phase 2B 单细胞定位结果

| Axis | Dominant cell | Secondary cell | Donor effect | 95% bootstrap CI | FDR | Confidence |
|---|---|---|---:|---|---:|---|
| F1 | keratinocyte | T_cell | 0.035 | 0.025 to 0.046 | 0.364 | LOW |
| F2 | keratinocyte | NK_cell | 0.015 | 0.010 to 0.020 | 0.364 | LOW |
| F6 | keratinocyte | NK_cell | 0.049 | 0.039 to 0.062 | 0.364 | LOW |
| F7 | NK_cell | B_cell | 0.121 | 0.009 to 0.259 | 0.424 | LOW |

解释：

F1、F2、F6 的方向与 keratinocyte/stress skin-primary 假设一致，且 CORE/EXTENDED pseudobulk concordance 很高。但 GSE228421 只有 5 个 donor，经过多细胞类型 FDR 后不能称为显著定位。F7 在皮肤中没有形成 monocyte/myeloid 主定位，仍应作为 supportive/systemic axis，主要依赖既有 bulk blood support。

## Phase 2B-R + 2C 停止规则

当前不把项目立刻缩成纯 bulk 文章，但也不继续无限寻找 transcriptomic datasets。

锁定路线：

```text
Phase 2B completed
        ↓
Phase 2B-R
one-pass high-resolution refinement of GSE228421
        ↓
Phase 2C
GSE202011 independent spatial validation
and independent scRNA only after exact accession/object audit
        ↓
Stop adding transcriptomic datasets
        ↓
Mechanism freeze v2
        ↓
Phase 3 genetics if claim boundary is accepted
```

GSE202011 当前审计结论：

- 它是 spatial transcriptomics 数据集；
- GEO/local metadata 有 30 个样本；
- local sample split：Healthy 7、PSO lesional 7、PSO non-lesional 5、PSA lesional 7、PSA non-lesional 4；
- supplementary 包括 H5 tar 和 ST image tar；
- 不能直接把 GSE202011 当作 67,378-cell scRNA atlas，本体 scRNA 数据源需要另行确认。

## 主要文件

- `reports/PHASE1B_MOLECULAR_AXIS_REPORT.md`
- `PROJECT_STATUS.md`
- `DECISION_LOG.md`
- `results/phase1b/external_GSE244679_skin_axis_replication.tsv`
- `results/phase1b/external_GSE147339_blood_axis_support.tsv`
- `results/phase1b/external_GSE61281_blood_axis_support.tsv`
- `results/phase1b/external_axis_replication_and_blood_support.tsv`
- `results/phase1b/external_dataset_audit.tsv`
- `reports/PHASE2A_AXIS_MECHANISM_PRIORITIZATION.md`
- `reports/mechanism_cards/F1.md` 到 `reports/mechanism_cards/F8.md`
- `results/phase2a/axis_evidence_matrix.tsv`
- `results/phase2a/axis_priority_matrix.tsv`
- `results/phase2a/axis_mechanism_cards.tsv`
- `results/phase2a/factor_redundancy.tsv`
- `results/phase2a/Table_axis_prioritization_master.tsv`
- `results/phase2a/single_cell_readiness.tsv`
- `results/phase2a/axis_gene_programs/F1_gene_program.tsv`
- `results/phase2a/axis_gene_programs/F2_gene_program.tsv`
- `results/phase2a/axis_gene_programs/F6_gene_program.tsv`
- `results/phase2a/axis_gene_programs/F7_gene_program.tsv`
- `CURRENT_STATUS_PHASE2B.md`
- `reports/PHASE2B_GSE228421_SINGLE_CELL_LOCALIZATION.md`
- `results/phase2b/Table_phase2b_axis_cell_localization.tsv`
- `results/phase2b/GSE228421_baseline_LS_vs_NL_donor_statistics.tsv`
- `results/phase2b/GSE228421_cell_type_localization.tsv`
- `results/phase2b/GSE228421_donor_celltype_axis_scores.tsv`
- `reports/PHASE2BR_2C_STOP_RULE_ROADMAP.md`
- `results/phase2br_2c/GSE202011_spatial_sample_audit.tsv`
- `results/phase2br_2c/GSE202011_spatial_sample_summary.tsv`

## 验证状态

测试已通过：

```bash
environment/phase1b_venv/bin/python -m pytest tests
```

结果：

```text
9 passed
```

## 下一步

已接受当前论文边界：

> 以“皮肤主导的连续 molecular axes，并带有谨慎外部血液支持”为主线继续推进。

下一步建议不是直接进入 GWAS，而是执行 bounded Phase 2B-R + 2C：一次性精炼 GSE228421、用 GSE202011 做 spatial validation、并在确认 exact scRNA data source 后再做独立 scRNA validation。该 block 结束后停止继续增加 transcriptomic datasets，进入 mechanism freeze v2。
