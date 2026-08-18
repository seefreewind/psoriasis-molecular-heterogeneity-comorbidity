# Phase 4A LDSC genome-wide genetic correlation report

## Scope lock

暴露锁定为 overall psoriasis susceptibility `GCST90472771`。F1/F2/F6/F7 molecular axes 未进入 genetics 主分析。Phase 4A 只运行 genome-wide LDSC rg；未运行 LAVA、coloc、MR 或 axis-specific genetics。

## Download and munge status

6 个 frozen primary outcomes 完成下载、checksum、HapMap3/LDSC-compatible rsID harmonization、munge 和单性状 LDSC h² sanity check。4 个 frozen primary outcomes 因 primary access 或 archive integrity 问题未进入 rg；没有后验替换 backup。

未纳入 rg 的 frozen primary outcomes：

| Outcome | status | reason |
|---|---|---|
| Type 2 diabetes | DOWNLOAD_OR_ARCHIVE_FAIL | Frozen primary DIAMANTE EUR zip 请求返回不可解压/不完整 archive；未替换 backup。 |
| MASLD | PRIMARY_FILE_UNRESOLVED | Frozen primary Ghodsian2021/GCST90091033 来源仍存在页面/API/FTP 不一致或不可访问问题；Namjou GCST008471 继续被排除为 primary。 |
| Major depressive disorder | ACCESS_BLOCKED_403 | Frozen primary PGC MDD2 noUKBB/no23andMe Figshare/API 返回 403 或许可门槛。 |
| Uveitis | ACCESS_BLOCKED_FORM_REQUIRED | Frozen primary FinnGen/anterior uveitis 来源需要 access form/email；未替换 backup。 |

## LDSC rg results

| Outcome | system | rg | SE | P | FDR | h2_outcome | cross-trait intercept | QC |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Psoriatic arthritis | musculoskeletal_autoimmune | 1.1715 | 0.0751 | 6.75e-55 | 4.05e-54 | 0.1519 | 0.3142 | CROSS_TRAIT_INTERCEPT_ELEVATED;NEAR_NEIGHBOR_PHENOTYPE |
| Crohn disease | intestinal_autoimmune | -0.2717 | 0.0449 | 1.43e-09 | 2.87e-09 | 0.4184 | -0.0636 | ELEVATED_H2_INTERCEPT;CROSS_TRAIT_INTERCEPT_ELEVATED |
| Ulcerative colitis | intestinal_autoimmune | -0.2233 | 0.0409 | 4.82e-08 | 7.23e-08 | 0.2450 | -0.0625 | ELEVATED_H2_INTERCEPT;CROSS_TRAIT_INTERCEPT_ELEVATED |
| Coronary artery disease | cardiometabolic_vascular | 0.1732 | 0.0274 | 2.5e-10 | 7.49e-10 | 0.0583 | 0.0189 | PASS |
| Ischemic stroke | cardiometabolic_vascular | 0.0255 | 0.0589 | 0.665 | 0.791 | 0.0086 | 0.0156 | PASS |
| Chronic kidney disease | renal | 0.0118 | 0.0445 | 0.791 | 0.791 | 0.0136 | 0.0102 | PASS |

## GO decision

Decision: **GO TO PHASE 4B, with restricted disease scope and QC labels**。

本轮 6 个可运行 frozen primary outcomes 中，4 个 trait 达到 FDR-supported rg，覆盖 3 个 system domains：cardiometabolic_vascular、intestinal_autoimmune、musculoskeletal_autoimmune。

解释边界：PsA 是 near-neighbor phenotype，且 rg > 1、cross-trait intercept 明显升高；它支持 psoriasis/PsA 共享免疫遗传架构，但不能作为干净的独立 multisystem signal。CD 和 UC 在本轮 frozen run 中呈显著负 rg，同时 h² intercept 和 cross-trait intercept 偏高，进入 Phase 4B 前必须保留 QC 标签并做 source/build/phenotype sensitivity。CAD 为清晰正 rg 且 QC 较干净，是目前最适合进入 local rg 的非经典自身免疫系统信号。Stroke 和 CKD 未显著，且 observed-scale h² 较低，Phase 4A 判定为 low-power/null。

Phase 4B 不应把 10 个疾病全部展开。建议优先范围为：CAD（clean positive systemic signal）、PsA（near-neighbor positive control/sensitivity）、CD/UC（QC-flagged intestinal autoimmune signals）。Stroke、CKD 暂不进入主 LAVA，仅可作为预先声明的 null/low-power reference；T2D、MASLD、MDD、uveitis 需要 primary source 解决后才能补入。

## Output files

- LDSC rg table: `/Users/zy/Documents/ChatGPT/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4a/phase4a_ldsc_rg_results.tsv`
- Blocked primary outcome table: `/Users/zy/Documents/ChatGPT/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4a/phase4a_blocked_primary_outcomes.tsv`
- Psoriasis HapMap3 mapping QC: `/Users/zy/Documents/ChatGPT/银屑病机制论文设计/psoriasis_endotype_comorbidity/results/phase4a/munge_inputs/psoriasis_GCST90472771.hm3_mapping_qc.tsv`
- LDSC logs: `/Users/zy/Documents/ChatGPT/银屑病机制论文设计/psoriasis_endotype_comorbidity/logs/phase4a/ldsc`
