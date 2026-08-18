# Phase 4B-0 + Phase 4B 当前情况报告

生成日期：2026-08-13

## 一句话结论

Phase 4B-0 支持继续做限制性 LAVA：PsA 的 `rg > 1` 主要应作为近邻表型/正控制处理；Crohn 和 UC 的负向 global rg 未发现简单 effect-direction 翻转错误，但属于 QC-flagged IBD 信号；CAD 是当前最干净的 primary systemic target。Phase 4B restricted LAVA 显示：CAD 存在多个正向共享局部遗传区段，PsA 呈强正向 near-neighbor 共享，IBD 呈明显方向异质性，其中 Crohn 负向 local architecture 更突出。

## Phase 4B-0：global rg 异常裁决

已完成的方向/QC 审计显示：

| Trait | sign concordance | 结论 |
|---|---:|---|
| Psoriasis GCST90472771 | 1.000 | Z/BETA 方向构造通过 |
| PsA | 1.000 | 方向通过，但 `rg=1.17` 与 cross-trait intercept 升高，保留为 positive-control / near-neighbor |
| Crohn | 1.000 | 未发现简单 allele/effect-direction 翻转 |
| UC | 1.000 | 未发现简单 allele/effect-direction 翻转 |
| CAD | 1.000 | 方向与 QC 最干净 |

CD/UC 的 sign-flip stress test 将 global rg 镜像为正值，说明当前负向 rg 不是由脚本内单侧翻转造成。MHC 已在当前 LDSC reference 中排除，显式 no-MHC sensitivity 与主结果一致。

因此，Phase 4B 解释边界冻结为：

| Outcome | 角色 |
|---|---|
| CAD | primary systemic target |
| PsA | positive-control / near-neighbor sensitivity |
| Crohn | QC-flagged IBD local-heterogeneity target |
| UC | QC-flagged IBD local-heterogeneity target |

Stroke、CKD 暂不进入 LAVA；T2D、MASLD、MDD、uveitis 继续作为 data-access unresolved，不作为 null outcome。

## Phase 4B：restricted LAVA 方法

分析只使用 overall psoriasis susceptibility `GCST90472771`，不重新引入 F1/F2/F6/F7 axis-specific genetics。

流程：

1. 使用同一套 munged summary statistics 和 1000G EUR PLINK reference。
2. 使用 LAVA 官方 GRCh37/hg19 2495 locus 定义。
3. 先运行全基因组 univariate local h² screening。
4. 只对 psoriasis 与 outcome 均有强 local h² 的区段运行 bivariate local rg。
5. 本轮正式 bivariate 门槛固定为 `joint local h² p < 1e-5`。
6. 对每个 outcome 计算 within-outcome FDR，并对全部 restricted LAVA tests 计算 global FDR。

重要限制：LAVA 0.1.5 官方建议欧洲分析使用 UK Biobank binary LD reference；本轮使用项目内既有 1000G EUR reference，因此 local h² negative variance 和低覆盖 locus 需要作为 QC 限制报告。当前结果适合用于 Phase 4B 方向裁决和局部结构定位，后续共享位点/coloc 前建议用更合适的 binary LD reference 复核重点 locus。

## Local h² screening

| Outcome | tested loci with both traits | joint h² p<0.05 | joint h² p<1e-5 |
|---|---:|---:|---:|
| CAD | 2011 | 1031 | 118 |
| Crohn | 1981 | 940 | 131 |
| PsA | 1773 | 716 | 40 |
| UC | 1961 | 925 | 98 |

解读：四个 outcome 都有足够多的双性状 local h² 区段进入 restricted bivariate LAVA。PsA 和 IBD 的 negative local variance 警报较多，支持继续保留 QC-flagged 标签。

## Restricted bivariate LAVA 总表

| Outcome | Role | bivar loci | FDR<0.05 within outcome | FDR<0.05 all tests | nominal positive | nominal negative | median rho | min P | top locus | top rho |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CAD | primary systemic | 118 | 18 | 23 | 21 | 10 | 0.079 | 5.24e-08 | 347 | 0.651 |
| PsA | positive control | 40 | 36 | 31 | 36 | 0 | 0.631 | 9.91e-87 | 908 | 0.945 |
| Crohn | QC-flagged IBD | 131 | 49 | 49 | 9 | 51 | -0.208 | 8.19e-23 | 57 | -0.535 |
| UC | QC-flagged IBD | 98 | 17 | 19 | 7 | 18 | -0.048 | 7.62e-25 | 57 | -0.690 |

## 结果解释

### CAD：primary systemic signal 成立

CAD 是 Phase 4A 中最干净的非近邻系统性信号，restricted LAVA 进一步支持这一点。118 个强 local h² 候选中，18 个在 CAD within-outcome FDR<0.05，23 个在全部 restricted tests FDR<0.05。方向以正向为主，top locus 包括：

| Locus | chr:start-stop | rho | P | FDR all |
|---:|---|---:|---:|---:|
| 347 | chr2:161432090-163607635 | 0.651 | 5.24e-08 | 8.17e-07 |
| 1215 | chr7:138755108-140217630 | 0.841 | 1.23e-06 | 1.53e-05 |
| 1841 | chr12:111592382-113947983 | 0.605 | 3.36e-06 | 3.61e-05 |

结论：CAD 可以作为 Phase 4C shared loci + colocalization 的首要疾病。下一步应围绕这些 FDR-supported positive local rg loci 做 locus annotation、sentinel/credible variant mapping、skin/blood/vascular eQTL coloc。

### PsA：强正控制，不作为独立多系统证据

PsA 在 restricted LAVA 中表现为几乎纯正向结构：40 个候选 locus 中 36 个 within-outcome FDR<0.05，nominal negative 为 0。这符合银屑病与 PsA 的近邻表型关系，也解释了 Phase 4A 中 `rg > 1` 的高协方差背景。

结论：PsA 是方法学 sanity check 和 near-neighbor positive control。它可以进入 Phase 4C 作为免疫共享位点参考，但不能作为“多系统共病”主证据。

### Crohn/UC：不是简单负相关，而是方向异质性 local architecture

Crohn 的 restricted LAVA 显示负向 local rg 更强：131 个候选 locus 中 49 个 within-outcome FDR<0.05，nominal negative 51 个，nominal positive 9 个。UC 也显示负向为主但更弱：98 个候选 locus 中 17 个 within-outcome FDR<0.05，nominal negative 18 个，nominal positive 7 个。

两个 IBD outcome 的 top locus 都是 locus 57：

| Outcome | Locus | chr:start-stop | rho | P | FDR all |
|---|---:|---|---:|---:|---:|
| Crohn | 57 | chr1:66778016-67761890 | -0.535 | 8.19e-23 | 7.92e-21 |
| UC | 57 | chr1:66778016-67761890 | -0.690 | 7.62e-25 | 9.83e-23 |

同时也存在正向局部区段，例如 Crohn locus 908 rho=0.382，UC locus 347 rho=0.829。这说明 IBD 不应写成简单的 genome-wide 负相关，而应写成“global negative rg plus local directional heterogeneity”。

结论：Crohn/UC 可以进入 Phase 4C，但必须保留 QC-flagged 和 direction-heterogeneous 标签。优先检查共同出现、方向稳定、local h² 强且 FDR-supported 的 IBD loci，而不是按 global rg 直接做单向解释。

## Phase 4B GO/SHRINK 判断

当前判断：**GO TO PHASE 4C，限定范围推进。**

理由：

- CAD 提供了清洁的 primary systemic evidence。
- PsA positive-control 通过，说明 pipeline 能捕捉预期近邻共享结构。
- Crohn/UC 的异常 global rg 经方向审计后未被简单 QC 错误解释，restricted LAVA 提供了可进一步拆解的方向异质性 local architecture。

推进边界：

| Disease | Phase 4C 优先级 |
|---|---|
| CAD | Highest priority |
| PsA | Positive-control / near-neighbor reference |
| Crohn | QC-flagged, direction-heterogeneous |
| UC | QC-flagged, direction-heterogeneous |
| Stroke/CKD | 暂不进入 Phase 4C |
| T2D/MASLD/MDD/uveitis | 等 primary GWAS 获取后补做 LDSC；现在不作为 null |

## Phase 4C 建议

下一步只做 shared loci + colocalization，不做 MR。

建议顺序：

1. 对 CAD 的 FDR-supported positive local rg loci 做 locus annotation。
2. 对 PsA 的强正向 loci 做 positive-control annotation。
3. 对 Crohn/UC 分为 positive-local 和 negative-local 两组，分别做 locus annotation。
4. 每个 locus 输出：lead SNP、credible set 或 proxy SNP、nearest/priority genes、skin/blood/vascular/immune eQTL、coloc PP4。
5. 只有 coloc 支持的 gene-trait pair 才进入 manuscript 的 mechanistic genetic table。

仍然禁止：

- MR
- axis-specific LDSC/LAVA/MR/coloc
- drug prediction
- PPI/hub gene
- 因显著性改换 outcome GWAS source

## 输出文件

| 文件 | 内容 |
|---|---|
| `results/phase4b_lava_local_h2/phase4b_lava_local_h2_summary.tsv` | 全基因组 local h² 筛查汇总 |
| `results/phase4b_lava_local_h2/phase4b_lava_pairwise_local_h2_candidates.tsv` | 每个 outcome 的双性状 local h² 候选 |
| `results/phase4b_restricted_lava/phase4b_restricted_lava_summary.tsv` | restricted LAVA 总结 |
| `results/phase4b_restricted_lava/phase4b_restricted_lava_bivariate.tsv` | 全部 restricted bivariate local rg 结果 |
| `results/phase4b_restricted_lava/phase4b_restricted_lava_top_loci.tsv` | 每个 outcome 的 top loci |
| `reports/PHASE4B0_4B_RESTRICTED_LAVA_REPORT.md` | 当前报告 |
