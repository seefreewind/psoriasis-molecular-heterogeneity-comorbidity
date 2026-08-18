#!/usr/bin/env python3
"""Phase 2A axis triage and mechanism cards."""

from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PHASE1B = ROOT / "results" / "phase1b"
OUT = ROOT / "results" / "phase2a"
REPORT = ROOT / "reports" / "PHASE2A_AXIS_MECHANISM_PRIORITIZATION.md"


MECHANISM_KEYWORDS = {
    "T17/NF-kB inflammatory": [
        "IL6",
        "JAK",
        "STAT3",
        "TNFA",
        "NF",
        "NFKB",
        "inflamm",
        "Toll",
        "TLR",
        "MyD88",
        "interleukin",
        "cytokine",
        "T_cells",
    ],
    "keratinocyte/proliferation": [
        "keratin",
        "epiderm",
        "mitotic",
        "cell cycle",
        "MYC",
        "E2F",
        "G2M",
        "prolifer",
    ],
    "stromal/repair-remodeling": [
        "TGF",
        "myogenesis",
        "coagulation",
        "glycosaminoglycan",
        "matrix",
        "collagen",
        "fibro",
        "wound",
        "repair",
        "VEGF",
        "RHO",
        "RAC",
    ],
    "metabolic/hypoxia-stress": [
        "hypoxia",
        "AMPK",
        "glycolysis",
        "mitochond",
        "oxidative",
        "beta-oxidation",
        "starvation",
        "metabolism",
    ],
    "IFN/antiviral-myeloid": [
        "IRF",
        "interferon",
        "antiviral",
        "APOBEC",
        "viral",
        "influenza",
        "CSF3",
        "G-CSF",
        "myeloid",
        "inflammasome",
        "TNFs",
        "WNT5A",
    ],
    "DNA-damage/chromatin": [
        "DNA Damage",
        "Nucleotide Excision Repair",
        "telomere",
        "methylation",
        "chromatin",
        "CHD",
        "p53",
        "TP53",
    ],
}


def read_table(name: str) -> pd.DataFrame:
    return pd.read_csv(PHASE1B / name, sep="\t")


def safe_absmax(df: pd.DataFrame, col: str) -> float:
    if df.empty or col not in df:
        return float("nan")
    vals = pd.to_numeric(df[col], errors="coerce").abs().dropna()
    return float(vals.max()) if len(vals) else float("nan")


def signed_value_at_absmax(df: pd.DataFrame, col: str) -> float:
    if df.empty or col not in df:
        return float("nan")
    vals = pd.to_numeric(df[col], errors="coerce")
    if vals.dropna().empty:
        return float("nan")
    return float(vals.loc[vals.abs().idxmax()])


def score_threshold(value: float, high: float, mid: float) -> int:
    if not np.isfinite(value):
        return 0
    if value >= high:
        return 2
    if value >= mid:
        return 1
    return 0


def split_features(text: str) -> list[str]:
    if not isinstance(text, str) or not text:
        return []
    return [x.strip() for x in text.split(";") if x.strip()]


def top_feature_table(loadings: pd.DataFrame, factor: str, n: int = 12) -> pd.DataFrame:
    sub = loadings[loadings["factor"].eq(factor)].copy()
    sub["abs_loading"] = sub["loading"].abs()
    sub["direction"] = np.where(sub["loading"] >= 0, "positive", "negative")
    return sub.sort_values("abs_loading", ascending=False).head(n)


def family_support(loadings: pd.DataFrame, factor: str, n: int = 60) -> tuple[int, str]:
    top = top_feature_table(loadings, factor, n=n)
    counts = top["feature_family"].value_counts()
    strong = counts[counts >= 3]
    return int(len(strong)), json.dumps(counts.to_dict(), ensure_ascii=False)


def mechanism_votes(features: list[str]) -> tuple[str, str]:
    text = " | ".join(features)
    votes = {}
    for label, keywords in MECHANISM_KEYWORDS.items():
        pattern = re.compile("|".join(re.escape(k) for k in keywords), flags=re.IGNORECASE)
        votes[label] = len(pattern.findall(text))
    ranked = sorted(votes.items(), key=lambda x: (-x[1], x[0]))
    top = [f"{k}:{v}" for k, v in ranked if v > 0]
    if not top:
        return "uninterpretable_or_diffuse", ""
    if ranked[0][1] == 0:
        return "uninterpretable_or_diffuse", ""
    return ranked[0][0], "; ".join(top)


def evidence_tier(row: pd.Series) -> str:
    if row["priority_class"] == "primary_skin_axis":
        return "primary"
    if row["priority_class"] == "primary_systemic_candidate":
        return "primary_systemic_candidate"
    if row["priority_score"] >= 6:
        return "supplementary_high"
    return "supplementary"


def freeze_priority_classes(out: pd.DataFrame) -> pd.DataFrame:
    out = out.copy()
    out["priority_class"] = "supplementary_axis"

    skin_pool = out[
        out["dominant_view"].isin(["LS", "NL"])
        & (out["GSE244679_skin_abs_spearman_max"] >= 0.30)
    ].copy()
    skin_pool["formal_bonus"] = skin_pool["formal_naming_status"].eq("eligible_for_cautious_mechanism_name").astype(int)
    core_skin = skin_pool.sort_values(
        ["GSE244679_skin_abs_spearman_max", "internal_skin_abs_spearman_max", "priority_score"],
        ascending=False,
    ).head(2)["factor"].tolist()
    out.loc[out["factor"].isin(core_skin), "priority_class"] = "primary_skin_axis"

    extra_skin = skin_pool[~skin_pool["factor"].isin(core_skin)].sort_values(
        ["formal_bonus", "priority_score", "GSE244679_skin_abs_spearman_max"],
        ascending=False,
    ).head(1)["factor"].tolist()
    out.loc[out["factor"].isin(extra_skin), "priority_class"] = "primary_skin_axis"

    systemic_pool = out[out["dominant_view"].eq("BLD") & (out["GSE61281_blood_abs_spearman_max"] >= 0.35)]
    if not systemic_pool.empty:
        systemic = systemic_pool.sort_values(
            ["GSE61281_blood_abs_spearman_max", "priority_score"],
            ascending=False,
        ).head(1)["factor"].tolist()
        out.loc[out["factor"].isin(systemic), "priority_class"] = "primary_systemic_candidate"

    review_mask = out["priority_class"].eq("supplementary_axis") & (
        (out["priority_score"] >= 7)
        | (out["GSE244679_skin_abs_spearman_max"] >= 0.30)
        | (out["GSE61281_blood_abs_spearman_max"] >= 0.25)
    )
    out.loc[review_mask, "priority_class"] = "supplementary_axis_review"
    return out


def build_priority_matrix() -> pd.DataFrame:
    OUT.mkdir(parents=True, exist_ok=True)
    stability = read_table("factor_stability.tsv")
    biology = read_table("factor_biology.tsv")
    loadings = read_table("factor_loadings.tsv")
    internal = read_table("replication_ETAB14509.tsv")
    cross = read_table("cross_tissue_discovery_support.tsv")
    conf = read_table("factor_confounding.tsv")
    gse121212 = read_table("external_axis_support.tsv")
    gse244679 = read_table("external_GSE244679_skin_axis_replication.tsv")
    gse147339 = read_table("external_GSE147339_blood_axis_support.tsv")
    gse61281 = read_table("external_GSE61281_blood_axis_support.tsv")

    rows = []
    factors = sorted(stability["factor"].unique(), key=lambda x: int(x[1:]))
    for factor in factors:
        stab = stability.set_index("factor").loc[factor]
        bio = biology.set_index("factor").loc[factor]
        int_sub = internal[internal["factor"].eq(factor)]
        ext_skin = gse244679[gse244679["axis"].eq(factor)]
        ext_gse121212 = gse121212[gse121212["axis"].eq(factor)]
        b147 = gse147339[gse147339["axis"].eq(factor)]
        b612 = gse61281[gse61281["axis"].eq(factor)]
        conf_sub = conf[conf["factor"].eq(factor)]

        internal_skin_abs = safe_absmax(int_sub, "loading_vs_replication_mean_shift_spearman")
        gse244_abs = safe_absmax(ext_skin, "loading_vs_paired_lesional_minus_adjacent_spearman")
        gse121_abs = safe_absmax(ext_gse121212, "loading_vs_external_mean_score_spearman")
        gse147_abs = safe_absmax(b147, "loading_vs_psoriasis_minus_control_spearman")
        gse612_abs = safe_absmax(b612, "loading_vs_case_minus_control_spearman")
        cross_abs = abs(float(cross.set_index("factor").loc[factor, "skin_weighted_score_vs_blood_weighted_score_spearman"]))

        n_strong_families, top_family_counts = family_support(loadings, factor)
        biology_score = 2 if n_strong_families >= 2 and bio["biology_label_status"] == "labelable_multifamily" else (1 if n_strong_families >= 2 else 0)
        max_confound_partial = float(pd.to_numeric(conf_sub["partial_r2"], errors="coerce").max())
        min_confound_fdr = float(pd.to_numeric(conf_sub["fdr"], errors="coerce").min())
        confounding_score = 0 if (min_confound_fdr < 0.10 and max_confound_partial >= 0.05) else (1 if max_confound_partial >= 0.10 else 2)

        stability_score = 2 if stab["stability_status"] == "robust" else (1 if stab["stability_status"] == "intermediate" else 0)
        internal_score = score_threshold(internal_skin_abs, 0.40, 0.20)
        external_skin_score = score_threshold(gse244_abs, 0.50, 0.30)
        systemic_score = max(score_threshold(cross_abs, 0.55, 0.35), score_threshold(gse612_abs, 0.40, 0.25), score_threshold(gse147_abs, 0.25, 0.15))

        priority_score = (
            stability_score
            + internal_score
            + external_skin_score
            + biology_score
            + confounding_score
            + systemic_score
        )
        top = top_feature_table(loadings, factor, n=30)
        candidate_label, label_votes = mechanism_votes((top["view"] + "::" + top["feature"]).tolist())
        dominant_view = str(bio["dominant_view"])
        rows.append(
            {
                "factor": factor,
                "priority_score": priority_score,
                "priority_class": "unfrozen",
                "stability_score": stability_score,
                "internal_skin_replication_score": internal_score,
                "external_GSE244679_skin_score": external_skin_score,
                "biology_multifamily_score": biology_score,
                "confounding_independence_score": confounding_score,
                "systemic_support_score": systemic_score,
                "stability_status": stab["stability_status"],
                "dominant_view": dominant_view,
                "BLD_r2": bio["BLD_r2"],
                "LS_r2": bio["LS_r2"],
                "NL_r2": bio["NL_r2"],
                "internal_skin_abs_spearman_max": internal_skin_abs,
                "GSE244679_skin_abs_spearman_max": gse244_abs,
                "GSE121212_skin_abs_spearman_max": gse121_abs,
                "internal_skin_blood_abs_spearman": cross_abs,
                "GSE147339_blood_abs_spearman_max": gse147_abs,
                "GSE61281_blood_abs_spearman_max": gse612_abs,
                "max_confounder_partial_r2": max_confound_partial,
                "min_confounder_fdr": min_confound_fdr,
                "n_strong_feature_families_top60": n_strong_families,
                "top60_feature_family_counts": top_family_counts,
                "candidate_mechanism_label": candidate_label,
                "mechanism_keyword_votes": label_votes,
                "formal_naming_status": "eligible_for_cautious_mechanism_name" if biology_score == 2 else "descriptive_card_only",
            }
        )
    out = pd.DataFrame(rows)
    out = freeze_priority_classes(out)
    out["evidence_tier"] = out.apply(evidence_tier, axis=1)
    out = out.sort_values(["evidence_tier", "priority_score", "GSE244679_skin_abs_spearman_max", "GSE61281_blood_abs_spearman_max"], ascending=[True, False, False, False])
    out.to_csv(OUT / "axis_priority_matrix.tsv", sep="\t", index=False)
    return out


def build_mechanism_cards(priority: pd.DataFrame) -> pd.DataFrame:
    biology = read_table("factor_biology.tsv").set_index("factor")
    loadings = read_table("factor_loadings.tsv")
    internal = read_table("replication_ETAB14509.tsv")
    cross = read_table("cross_tissue_discovery_support.tsv").set_index("factor")
    conf = read_table("factor_confounding.tsv")
    gse121212 = read_table("external_axis_support.tsv")
    gse244679 = read_table("external_GSE244679_skin_axis_replication.tsv")
    gse147339 = read_table("external_GSE147339_blood_axis_support.tsv")
    gse61281 = read_table("external_GSE61281_blood_axis_support.tsv")

    rows = []
    for factor in sorted(priority["factor"].unique(), key=lambda x: int(x[1:])):
        top = top_feature_table(loadings, factor, n=16)
        top_pos = loadings[loadings["factor"].eq(factor)].sort_values("loading", ascending=False).head(10)
        top_neg = loadings[loadings["factor"].eq(factor)].sort_values("loading", ascending=True).head(10)
        fam_counts = top["feature_family"].value_counts().to_dict()
        conf_sub = conf[conf["factor"].eq(factor)].sort_values("partial_r2", ascending=False)
        int_sub = internal[internal["factor"].eq(factor)].copy()
        g244 = gse244679[gse244679["axis"].eq(factor)].copy()
        b147 = gse147339[gse147339["axis"].eq(factor)].copy()
        b612 = gse61281[gse61281["axis"].eq(factor)].copy()
        p = priority.set_index("factor").loc[factor]
        conf_terms = []
        for _, r in conf_sub.head(3).iterrows():
            conf_terms.append(f"{r['covariate']}:partial_r2={r['partial_r2']:.3f},fdr={r['fdr']:.3f}")

        rows.append(
            {
                "factor": factor,
                "priority_class": p["priority_class"],
                "priority_score": p["priority_score"],
                "candidate_mechanism_label": p["candidate_mechanism_label"],
                "formal_naming_status": p["formal_naming_status"],
                "dominant_view": biology.loc[factor, "dominant_view"],
                "view_contribution": f"LS_r2={biology.loc[factor, 'LS_r2']:.3f}; NL_r2={biology.loc[factor, 'NL_r2']:.3f}; BLD_r2={biology.loc[factor, 'BLD_r2']:.3f}",
                "top_feature_family_counts_top16": json.dumps(fam_counts, ensure_ascii=False),
                "top_positive_loadings": "; ".join(top_pos["view"] + "::" + top_pos["feature"] + " (" + top_pos["loading"].round(3).astype(str) + ")"),
                "top_negative_loadings": "; ".join(top_neg["view"] + "::" + top_neg["feature"] + " (" + top_neg["loading"].round(3).astype(str) + ")"),
                "internal_replication": "; ".join(int_sub["view"] + "=" + int_sub["loading_vs_replication_mean_shift_spearman"].round(3).astype(str)),
                "GSE244679_replication": "; ".join(g244["view"] + "=" + g244["loading_vs_paired_lesional_minus_adjacent_spearman"].round(3).astype(str)),
                "GSE121212_support_abs_max": safe_absmax(gse121212[gse121212["axis"].eq(factor)], "loading_vs_external_mean_score_spearman"),
                "internal_blood_support": f"skin-blood Spearman={cross.loc[factor, 'skin_weighted_score_vs_blood_weighted_score_spearman']:.3f}",
                "GSE147339_blood_support": signed_value_at_absmax(b147, "loading_vs_psoriasis_minus_control_spearman"),
                "GSE61281_blood_support_abs_max": safe_absmax(b612, "loading_vs_case_minus_control_spearman"),
                "GSE61281_strongest_contrast": "" if b612.empty else str(b612.loc[pd.to_numeric(b612["loading_vs_case_minus_control_spearman"]).abs().idxmax(), "contrast"]),
                "top_confounding_terms": "; ".join(conf_terms),
                "interpretation_boundary": "name cautiously only after single-cell donor-level localization" if p["formal_naming_status"] == "eligible_for_cautious_mechanism_name" else "do not assign formal mechanism name yet",
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "axis_mechanism_cards.tsv", sep="\t", index=False)
    return out


def md_table(df: pd.DataFrame, cols: list[str]) -> str:
    return df[cols].to_markdown(index=False)


def write_report(priority: pd.DataFrame, cards: pd.DataFrame) -> None:
    primary = priority[priority["priority_class"].isin(["primary_skin_axis", "primary_systemic_candidate"])]
    supp = priority[~priority["factor"].isin(primary["factor"])]
    lines = [
        "# PHASE 2A Axis Mechanism Prioritization",
        "",
        "## 1. Research Question",
        "",
        "研究问题：在 Phase 1B 已确立连续 molecular axes 且接受 skin-primary 论文边界后，如何从 F1-F8 中冻结 3-4 个主轴，并为每个轴建立可审计的机制证据卡？",
        "",
        "方案类型：疾病机制型 + 多组学整合型。当前阶段不做 GWAS/MR，不做 drug prediction，不把全部 8 个轴并列作为主线。",
        "",
        "## 2. Data Requirement",
        "",
        "| Data Type | Required | Optional | Purpose |",
        "|---|---|---|---|",
        "| Phase 1B MOFA loadings and view R2 | Yes | No | 定义每个轴的组织贡献和 leading features |",
        "| E-MTAB-14509 internal skin projection | Yes | No | 检查冻结轴在内部 replication skin 中的支持 |",
        "| GSE244679 paired skin RNA-seq | Yes | No | 检查独立配对皮肤外部复制 |",
        "| GSE121212 paired skin RNA-seq | Yes | No | 辅助外部皮肤支持，已知较弱 |",
        "| GSE147339/GSE61281 blood data | Yes | No | 作为 selective systemic support |",
        "| scRNA-seq/spatial/GWAS | No | Later | Phase 2B/2C/3 使用，不参与当前轴筛选打分 |",
        "",
        "## 3. Overall Workflow",
        "",
        "Step 1: 汇总每个轴的 MOFA 稳定性、组织贡献、top loadings、feature families、内部复制、外部复制、混杂和血液支持。",
        "",
        "Step 2: 使用冻结优先级矩阵打分。每个维度最高 2 分：MOFA 稳定性、内部皮肤复制、GSE244679 外部皮肤复制、生物学多家族一致性、混杂独立性、系统性支持。",
        "",
        "Step 3: 输出每个 factor 的 mechanism card。只有至少两个独立 feature families 支持同一机制时，才允许进入谨慎机制命名；否则只保留描述性证据卡。",
        "",
        "Step 4: 冻结 primary axes 与 supplementary axes，为后续 single-cell donor-level localization 和 GWAS anchoring 准备输入。",
        "",
        "## 4. Core Analysis Modules",
        "",
        "### Module 1",
        "",
        "名称：Axis evidence aggregation",
        "",
        "输入：`factor_loadings.tsv`、`factor_biology.tsv`、`factor_stability.tsv`、内部复制和外部支持结果表。",
        "",
        "方法：按 factor 合并稳定性、view R2、top feature family、内部/外部相关和混杂 partial R2。",
        "",
        "工具：Python / pandas。",
        "",
        "输出：`results/phase2a/axis_priority_matrix.tsv`。",
        "",
        "验证：检查 F1-F8 均有完整记录，外部结果行数与 Phase 1B 输出一致。",
        "",
        "对应 Figure：Figure 2A axis triage heatmap。",
        "",
        "风险：不同 evidence source 的相关方向不可直接解释为生物学方向，因为 MOFA factor sign 可翻转。",
        "",
        "### Module 2",
        "",
        "名称：Mechanism card construction",
        "",
        "输入：每个 factor 的 top positive/negative loadings、feature family、view contribution、复制和混杂结果。",
        "",
        "方法：为每个 factor 提取 top loadings、候选机制关键词、支持数据集和解释边界。",
        "",
        "工具：Python / pandas。",
        "",
        "输出：`results/phase2a/axis_mechanism_cards.tsv`。",
        "",
        "验证：正式机制命名必须满足多 feature-family 支持；否则标记为 descriptive card only。",
        "",
        "对应 Figure：Figure 2B-D primary-axis evidence cards；Supplementary Figure S2 all-axis cards。",
        "",
        "风险：Reactome-heavy 轴容易被过度命名；需要 single-cell donor-level localization 进一步锚定。",
        "",
        "### Module 3",
        "",
        "名称：Primary-axis freeze",
        "",
        "输入：优先级矩阵和 mechanism cards。",
        "",
        "方法：按证据等级选择 primary skin axes、primary systemic candidate 和 supplementary axes。",
        "",
        "工具：规则矩阵，不使用单一 P 值。",
        "",
        "输出：本报告的 primary/supplementary axis list。",
        "",
        "验证：主轴数量控制在 3-4 条；保留 F7 为 systemic candidate 时明确其 supportive 而非 full replication 边界。",
        "",
        "对应 Figure：Figure 1 study overview；Figure 2 axis prioritization。",
        "",
        "风险：若后续 scRNA-seq 不能定位某轴，应降级为 supplementary 或 diffuse axis。",
        "",
        "## 5. Required vs Optional Analysis",
        "",
        "| Analysis | Required or Optional | Reason |",
        "|---|---|---|",
        "| Frozen axis priority matrix | Required | 防止按单个 P 值或单个数据集挑轴 |",
        "| Mechanism cards for all F1-F8 | Required | 保证 primary 和 supplementary 轴都可审计 |",
        "| Donor-level scRNA-seq localization | Required next phase | 机制命名必须落到 cell type/state |",
        "| Spatial niche analysis | Optional next phase | 增强 niche claim，但取决于数据可获得性 |",
        "| GWAS/MR/coloc | Later required | 只能在 primary axes 冻结后进入 |",
        "| Drug prediction / PPI / LASSO | Not recommended | 当前会分散主线且容易低质量堆砌 |",
        "",
        "## 6. Validation Strategy",
        "",
        "- internal validation: E-MTAB-14509 frozen skin projection。",
        "- external validation: GSE244679 paired-skin replication；GSE121212 作为弱外部皮肤支持。",
        "- biological validation: Phase 2B 使用 psoriasis scRNA-seq，必须 donor-level pseudobulk/statistics。",
        "- sensitivity analysis: 检查不同 top-loading 阈值、feature family 去除、单视图去除后 primary-axis 排名是否稳定。",
        "- negative control: 后续 scRNA-seq/GWAS 阶段加入 shuffled axis genes 或 non-primary axes 作为对照。",
        "",
        "## 7. Expected Figure Mapping",
        "",
        "| Figure | Analysis Source | Main Message |",
        "|---|---|---|",
        "| Figure 1 | Phase 1B + Phase 2A overview | 离散 endotype 降级，连续 skin-primary axes 成为主线 |",
        "| Figure 2A | `axis_priority_matrix.tsv` | F1/F2/F6/F7 是当前最值得主线审查的轴 |",
        "| Figure 2B-D | `axis_mechanism_cards.tsv` | 每条主轴的 pathway/regulon/cell-state/replication evidence card |",
        "| Supplementary Figure S2 | all-axis cards | F3/F5/F8 等 supplementary axes 的证据边界 |",
        "| Future Figure 3 | scRNA-seq donor-level localization | primary axes 映射到 cell type/state |",
        "| Future Figure 4 | spatial niche or external cell-state validation | 机制轴是否位于合理组织 niche |",
        "",
        "## 8. Risk and Alternative Plan",
        "",
        "- 数据是否支持研究问题：支持 axis triage；暂不支持强机制命名或因果声明。",
        "- 是否缺少外部验证：皮肤外部验证已有 GSE244679；血液为 supportive，不是 design-matched replication。",
        "- 是否有 batch/center/platform confounding：GSE61281 为 microarray，必须保持 supportive wording。",
        "- 是否有 sample leakage 或 label leakage：当前使用外部 GEO 数据和 frozen axis definitions，未重新训练外部轴。",
        "- 是否存在方法堆砌：本阶段明确不做 GWAS/MR/drug/PPI/LASSO。",
        "- 是否有关键发现无法对应 Figure：所有主输出均映射到 Figure 2 或 Supplementary Figure S2。",
        "",
        "## 9. Next Step Recommendation",
        "",
        "建议下一步进入 Phase 2B：single-cell localization。输入应为 primary axes 的 leading-edge gene programs，统计单位必须是 patient/donor-level pseudobulk，而不是 cell-level n。",
        "",
        "## Frozen Axis Priority Matrix",
        "",
        md_table(
            priority.sort_values("priority_score", ascending=False),
            [
                "factor",
                "priority_score",
                "priority_class",
                "dominant_view",
                "internal_skin_abs_spearman_max",
                "GSE244679_skin_abs_spearman_max",
                "GSE61281_blood_abs_spearman_max",
                "candidate_mechanism_label",
                "formal_naming_status",
            ],
        ),
        "",
        "## Primary Axis Set",
        "",
        md_table(
            primary.sort_values("priority_score", ascending=False),
            [
                "factor",
                "priority_class",
                "priority_score",
                "dominant_view",
                "candidate_mechanism_label",
                "GSE244679_skin_abs_spearman_max",
                "GSE61281_blood_abs_spearman_max",
                "formal_naming_status",
            ],
        ),
        "",
        "## Supplementary Axis Set",
        "",
        md_table(
            supp.sort_values("priority_score", ascending=False),
            [
                "factor",
                "priority_class",
                "priority_score",
                "dominant_view",
                "candidate_mechanism_label",
                "GSE244679_skin_abs_spearman_max",
                "GSE61281_blood_abs_spearman_max",
                "formal_naming_status",
            ],
        ),
        "",
        "## Mechanism Cards",
        "",
    ]
    for _, card in cards.sort_values("factor", key=lambda s: s.str[1:].astype(int)).iterrows():
        lines.extend(
            [
                f"### Factor {card['factor']}",
                "",
                f"- priority: {card['priority_class']} / score {card['priority_score']}",
                f"- candidate label: {card['candidate_mechanism_label']}",
                f"- naming status: {card['formal_naming_status']}",
                f"- view contribution: {card['view_contribution']}",
                f"- feature families: {card['top_feature_family_counts_top16']}",
                f"- internal replication: {card['internal_replication']}",
                f"- GSE244679 replication: {card['GSE244679_replication']}",
                f"- blood support: {card['internal_blood_support']}; GSE147339={card['GSE147339_blood_support']:.3f}; GSE61281_abs_max={card['GSE61281_blood_support_abs_max']:.3f}",
                f"- confounding: {card['top_confounding_terms']}",
                f"- interpretation boundary: {card['interpretation_boundary']}",
                "",
                "Top positive loadings:",
                "",
                card["top_positive_loadings"],
                "",
                "Top negative loadings:",
                "",
                card["top_negative_loadings"],
                "",
            ]
        )
    REPORT.write_text("\n".join(lines) + "\n")


def main() -> None:
    priority = build_priority_matrix()
    cards = build_mechanism_cards(priority)
    write_report(priority, cards)


if __name__ == "__main__":
    main()
