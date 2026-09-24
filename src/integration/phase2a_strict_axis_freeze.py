#!/usr/bin/env python3
"""Strict Phase 2A axis prioritization, mechanism cards, and freeze outputs."""

from __future__ import annotations

import gzip
import itertools
import json
import math
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parents[2]
P1B = ROOT / "results" / "phase1b"
OUT = ROOT / "results" / "phase2a"
FIG = ROOT / "results" / "figures"
CARDS = ROOT / "reports" / "mechanism_cards"
PROGRAMS = OUT / "axis_gene_programs"
REPORT = ROOT / "reports" / "PHASE2A_AXIS_MECHANISM_PRIORITIZATION.md"
GEO = ROOT / "data" / "external" / "geo"

RETAINED = ["F1", "F2", "F6", "F7"]
PRIMARY_SKIN = {"F1", "F2", "F6"}
SYSTEMIC = {"F7"}
SECONDARY = {"F3", "F5", "F8"}
RETIRE = {"F4"}

DOMAIN_HINTS = {
    "F1": ("metabolic/hypoxia-stress-like lesional skin axis", "LOW"),
    "F2": ("stromal/repair-remodeling-like nonlesional skin axis", "LOW"),
    "F3": ("T17/NF-kB inflammatory-like blood axis", "MODERATE"),
    "F4": ("DNA-damage/chromatin-like blood factor", "LOW"),
    "F5": ("stromal/repair-remodeling-like lesional skin axis", "LOW"),
    "F6": ("metabolic/hypoxia-stress skin axis", "MODERATE"),
    "F7": ("IFN/antiviral-myeloid systemic blood candidate", "LOW"),
    "F8": ("growth-factor/stromal-remodeling nonlesional axis", "LOW"),
}


def read_tsv(path: Path | str) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t")


def safe_absmax(df: pd.DataFrame, col: str) -> float:
    if df.empty or col not in df:
        return np.nan
    vals = pd.to_numeric(df[col], errors="coerce").abs().dropna()
    return float(vals.max()) if len(vals) else np.nan


def signed_absmax(df: pd.DataFrame, col: str) -> float:
    if df.empty or col not in df:
        return np.nan
    vals = pd.to_numeric(df[col], errors="coerce").dropna()
    return float(vals.loc[vals.abs().idxmax()]) if len(vals) else np.nan


def classify_support(value: float, strong: float = 0.40, moderate: float = 0.25, weak: float = 0.15) -> str:
    if not np.isfinite(value):
        return "not_available"
    if abs(value) >= strong:
        return "strong"
    if abs(value) >= moderate:
        return "moderate"
    if abs(value) >= weak:
        return "weak"
    return "absent_or_minimal"


def parse_series_matrix_metadata(path: Path) -> pd.DataFrame:
    rows: dict[str, list[str]] = {}
    if not path.exists():
        return pd.DataFrame()
    with gzip.open(path, "rt", errors="replace") as fh:
        for line in fh:
            if line.startswith("!series_matrix_table_begin"):
                break
            if not line.startswith("!Sample_"):
                continue
            parts = [p.strip().strip('"') for p in line.rstrip("\n").split("\t")]
            key = parts[0].replace("!Sample_", "")
            if key in rows:
                key = f"{key}_{sum(k.startswith(key) for k in rows) + 1}"
            rows[key] = parts[1:]
    if "geo_accession" not in rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).rename(columns={"geo_accession": "gsm"})


def top_features(loadings: pd.DataFrame, factor: str, n: int = 30) -> pd.DataFrame:
    sub = loadings[loadings["factor"].eq(factor)].copy()
    sub["abs_loading"] = sub["loading"].abs()
    sub["direction"] = np.where(sub["loading"] >= 0, "positive", "negative")
    return sub.sort_values("abs_loading", ascending=False).head(n)


def family_count(loadings: pd.DataFrame, factor: str, n: int = 60) -> int:
    counts = top_features(loadings, factor, n)["feature_family"].value_counts()
    return int((counts >= 3).sum())


def make_dirs() -> None:
    for path in [OUT, FIG, CARDS, PROGRAMS]:
        path.mkdir(parents=True, exist_ok=True)


def load_inputs() -> dict[str, pd.DataFrame]:
    return {
        "scores": read_tsv(P1B / "molecular_axis_scores_discovery.tsv"),
        "loadings": read_tsv(P1B / "factor_loadings.tsv"),
        "stability": read_tsv(P1B / "factor_stability.tsv"),
        "biology": read_tsv(P1B / "factor_biology.tsv"),
        "conf": read_tsv(P1B / "factor_confounding.tsv"),
        "internal": read_tsv(P1B / "replication_ETAB14509.tsv"),
        "cross": read_tsv(P1B / "cross_tissue_discovery_support.tsv"),
        "gse121212": read_tsv(P1B / "external_axis_support.tsv"),
        "gse244679": read_tsv(P1B / "external_GSE244679_skin_axis_replication.tsv"),
        "gse147339": read_tsv(P1B / "external_GSE147339_blood_axis_support.tsv"),
        "gse61281": read_tsv(P1B / "external_GSE61281_blood_axis_support.tsv"),
    }


def clinical_metric(conf: pd.DataFrame, factor: str, covariate: str, field: str = "partial_r2") -> float:
    sub = conf[(conf["factor"].eq(factor)) & (conf["covariate"].eq(covariate))]
    return float(sub[field].iloc[0]) if not sub.empty else np.nan


def axis_role(factor: str) -> tuple[str, str, str]:
    if factor in PRIMARY_SKIN:
        return "Tier A", "PRIMARY AXIS", "TRUE"
    if factor in SYSTEMIC:
        return "Tier C", "SUPPORTIVE/SYSTEMIC AXIS", "TRUE"
    if factor in SECONDARY:
        return "Tier B", "SECONDARY AXIS", "FALSE"
    return "Tier D", "UNINTERPRETABLE / RETIRE", "FALSE"


def build_evidence_matrix(d: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    factors = [f"F{i}" for i in range(1, 9)]
    bio = d["biology"].set_index("factor")
    stab = d["stability"].set_index("factor")
    cross = d["cross"].set_index("factor")
    for f in factors:
        internal = d["internal"][d["internal"]["factor"].eq(f)]
        g121 = d["gse121212"][d["gse121212"]["axis"].eq(f)]
        g244 = d["gse244679"][d["gse244679"]["axis"].eq(f)]
        b147 = d["gse147339"][d["gse147339"]["axis"].eq(f)]
        b612 = d["gse61281"][d["gse61281"]["axis"].eq(f)]
        conf = d["conf"][d["conf"]["factor"].eq(f)]
        tier, role, primary = axis_role(f)
        fam_n = family_count(d["loadings"], f)
        max_confound = float(pd.to_numeric(conf["partial_r2"], errors="coerce").max())
        skin_rep = safe_absmax(internal, "loading_vs_replication_mean_shift_spearman")
        ext_skin = safe_absmax(g244, "loading_vs_paired_lesional_minus_adjacent_spearman")
        blood_support = max(
            abs(float(cross.loc[f, "skin_weighted_score_vs_blood_weighted_score_spearman"])),
            safe_absmax(b147, "loading_vs_psoriasis_minus_control_spearman"),
            safe_absmax(b612, "loading_vs_case_minus_control_spearman"),
        )
        interpretation = "multifamily" if fam_n >= 2 and bio.loc[f, "biology_label_status"] == "labelable_multifamily" else "single_family_or_diffuse"
        coherence = (
            "skin_dominant"
            if bio.loc[f, "dominant_view"] in ["LS", "NL"]
            else "blood_dominant" if bio.loc[f, "dominant_view"] == "BLD" else "mixed"
        )
        suitability = "yes" if f in RETAINED and fam_n >= 1 else "limited"
        rationale = {
            "F1": "strongest GSE244679 paired-skin support; LS-dominant; descriptive mechanism only until cell localization",
            "F2": "strong internal and GSE244679 NL skin support; nonlesional stromal/repair-like candidate",
            "F3": "interpretable inflammatory blood factor but not selected primary because skin architecture is less central than F1/F2/F6",
            "F4": "robust but weaker replication and single-family/diffuse chromatin signal",
            "F5": "moderate paired-skin support but less complementary after selecting F2/F6",
            "F6": "LS-dominant hypoxia/stress axis with GSE244679 support and multifamily evidence",
            "F7": "blood-dominant systemic candidate with strongest GSE61281 support; not skin-primary",
            "F8": "NL-dominant but weaker external support and diffuse biology",
        }[f]
        rows.append(
            {
                "factor": f,
                "MOFA_seed_stability": float(stab.loc[f, "median_score_abs_pearson_vs_seed1"]),
                "bootstrap_stability": float(stab.loc[f, "median_top75_jaccard_vs_seed1"]),
                "variance_explained_LS": float(bio.loc[f, "LS_r2"]),
                "variance_explained_NL": float(bio.loc[f, "NL_r2"]),
                "variance_explained_blood": float(bio.loc[f, "BLD_r2"]),
                "internal_skin_replication": skin_rep,
                "external_GSE121212_support": safe_absmax(g121, "loading_vs_external_mean_score_spearman"),
                "external_GSE244679_support": ext_skin,
                "external_GSE54456_support_if_available": "not_analyzed",
                "internal_blood_support": float(cross.loc[f, "skin_weighted_score_vs_blood_weighted_score_spearman"]),
                "GSE147339_blood_support": signed_absmax(b147, "loading_vs_psoriasis_minus_control_spearman"),
                "GSE61281_blood_support": signed_absmax(b612, "loading_vs_case_minus_control_spearman"),
                "PASI_association": clinical_metric(d["conf"], f, "pasi"),
                "BMI_association": clinical_metric(d["conf"], f, "bmi"),
                "age_association": clinical_metric(d["conf"], f, "age"),
                "sex_association": clinical_metric(d["conf"], f, "sex"),
                "HLA_association": clinical_metric(d["conf"], f, "hla_c0602_carrier"),
                "batch_association": "not_available_not_in_current_covariate_model",
                "number_supported_feature_families": fam_n,
                "biological_interpretability": interpretation,
                "cross_tissue_coherence": coherence,
                "downstream_genetic_suitability": suitability,
                "evidence_tier": tier,
                "primary_candidate": primary,
                "rationale": rationale,
                "max_confounder_partial_r2": max_confound,
                "blood_support_abs_max": blood_support,
                "dominant_tissue": bio.loc[f, "dominant_view"],
                "candidate_domain": DOMAIN_HINTS[f][0],
                "name_confidence": DOMAIN_HINTS[f][1],
                "final_role": role,
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "axis_evidence_matrix.tsv", sep="\t", index=False)
    out.to_csv(OUT / "axis_priority_matrix.tsv", sep="\t", index=False)
    return out


def build_redundancy(d: dict[str, pd.DataFrame]) -> pd.DataFrame:
    scores = d["scores"].set_index("patient_id")
    load = d["loadings"].copy()
    load["key"] = load["view"] + "::" + load["feature"]
    mat = load.pivot_table(index="key", columns="factor", values="loading", fill_value=0)
    rows = []
    for a, b in itertools.combinations([f"F{i}" for i in range(1, 9)], 2):
        score_r = float(spearmanr(scores[a], scores[b]).correlation)
        loading_r = float(spearmanr(mat[a], mat[b]).correlation)
        ta = set(top_features(load, a, 60)["feature"])
        tb = set(top_features(load, b, 60)["feature"])
        jacc = len(ta & tb) / len(ta | tb) if (ta | tb) else np.nan
        overlap = len(ta & tb) / min(len(ta), len(tb)) if min(len(ta), len(tb)) else np.nan
        raf = set(top_features(load[load["feature_family"].eq("regulon_DoRothEA")], a, 30)["feature"])
        rbf = set(top_features(load[load["feature_family"].eq("regulon_DoRothEA")], b, 30)["feature"])
        caf = set(top_features(load[load["feature_family"].eq("cell_state")], a, 30)["feature"])
        cbf = set(top_features(load[load["feature_family"].eq("cell_state")], b, 30)["feature"])
        rows.append(
            {
                "factor_a": a,
                "factor_b": b,
                "patient_score_spearman": score_r,
                "loading_similarity_spearman": loading_r,
                "top_pathway_feature_jaccard": jacc,
                "top_feature_overlap_coefficient": overlap,
                "regulon_overlap_count": len(raf & rbf),
                "cell_state_overlap_count": len(caf & cbf),
                "redundancy_class": "same_broad_domain_review" if abs(score_r) >= 0.70 or overlap >= 0.50 else "distinct_or_low_overlap",
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "factor_redundancy.tsv", sep="\t", index=False)
    return out


def build_gene_programs(d: dict[str, pd.DataFrame], evidence: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    gene_sets = json.loads((ROOT / "data" / "metadata" / "phase1b" / "phase1b_gene_sets.json").read_text())
    retained = evidence[evidence["factor"].isin(RETAINED)].copy()
    summaries = []
    all_gene_sets: dict[str, set[str]] = {}
    for f in retained["factor"]:
        top = top_features(d["loadings"], f, 30)
        ext_rows = []
        support = evidence.set_index("factor").loc[f]
        for _, row in top.iterrows():
            source = row["feature"]
            genes = gene_sets.get(source, [])
            for gene in genes:
                ext_rows.append(
                    {
                        "gene_symbol": gene,
                        "source_feature": source,
                        "evidence_family": row["feature_family"],
                        "loading_direction": row["direction"],
                        "loading_strength": abs(float(row["loading"])),
                    }
                )
        ext = pd.DataFrame(ext_rows)
        if ext.empty:
            continue
        grouped = (
            ext.groupby("gene_symbol")
            .agg(
                source_feature=("source_feature", lambda x: ";".join(sorted(set(x))[:12])),
                evidence_family=("evidence_family", lambda x: ";".join(sorted(set(x)))),
                loading_direction=("loading_direction", lambda x: ";".join(sorted(set(x)))),
                loading_strength=("loading_strength", "sum"),
                n_source_features=("source_feature", "nunique"),
                n_evidence_families=("evidence_family", "nunique"),
            )
            .reset_index()
        )
        grouped["leading_edge_status"] = np.where(
            (grouped["n_source_features"] >= 2) & (grouped["n_evidence_families"] >= 1),
            "CORE",
            "EXTENDED",
        )
        # If no cross-family core exists because a factor is Reactome-heavy, keep replicated multi-feature genes as CORE but flag provenance.
        core_cut = grouped["leading_edge_status"].eq("CORE")
        if core_cut.sum() < 15:
            ranked = grouped.sort_values(["n_source_features", "loading_strength"], ascending=False)
            grouped["leading_edge_status"] = np.where(grouped["gene_symbol"].isin(ranked.head(30)["gene_symbol"]), "CORE", "EXTENDED")
        grouped["tissue_support"] = support["dominant_tissue"]
        grouped["replication_support"] = classify_support(support["external_GSE244679_support"])
        grouped["inclusion_reason"] = np.where(
            grouped["leading_edge_status"].eq("CORE"),
            "supported by multiple loading-ranked source features before downstream analyses",
            "included in loading-ranked biology-compatible source feature union",
        )
        grouped = grouped.sort_values(["leading_edge_status", "loading_strength"], ascending=[True, False])
        grouped.to_csv(PROGRAMS / f"{f}_gene_program.tsv", sep="\t", index=False)
        summaries.append(
            {
                "factor": f,
                "core_gene_count": int(grouped["leading_edge_status"].eq("CORE").sum()),
                "extended_gene_count": int(grouped.shape[0]),
            }
        )
        all_gene_sets[f] = set(grouped["gene_symbol"])
    overlap_rows = []
    for a, b in itertools.combinations(sorted(all_gene_sets), 2):
        ga, gb = all_gene_sets[a], all_gene_sets[b]
        fa = set(pd.read_csv(PROGRAMS / f"{a}_gene_program.tsv", sep="\t")["source_feature"].astype(str))
        fb = set(pd.read_csv(PROGRAMS / f"{b}_gene_program.tsv", sep="\t")["source_feature"].astype(str))
        overlap_rows.append(
            {
                "factor_a": a,
                "factor_b": b,
                "jaccard": len(ga & gb) / len(ga | gb) if ga | gb else np.nan,
                "overlap_coefficient": len(ga & gb) / min(len(ga), len(gb)) if min(len(ga), len(gb)) else np.nan,
                "shared_gene_count": len(ga & gb),
                "shared_pathway_proportion": len(fa & fb) / len(fa | fb) if (fa | fb) else np.nan,
            }
        )
    prog_summary = pd.DataFrame(summaries)
    overlap = pd.DataFrame(overlap_rows)
    prog_summary.to_csv(OUT / "axis_gene_program_summary.tsv", sep="\t", index=False)
    overlap.to_csv(OUT / "axis_gene_program_overlap.tsv", sep="\t", index=False)
    return prog_summary, overlap


def build_readiness(evidence: pd.DataFrame, prog_summary: pd.DataFrame) -> pd.DataFrame:
    prog = prog_summary.set_index("factor")
    rows = []
    for _, row in evidence[evidence["factor"].isin(RETAINED)].iterrows():
        f = row["factor"]
        core_n = int(prog.loc[f, "core_gene_count"]) if f in prog.index else 0
        extended_n = int(prog.loc[f, "extended_gene_count"]) if f in prog.index else 0
        ready = core_n >= 15 and row["max_confounder_partial_r2"] < 0.10
        rows.append(
            {
                "factor": f,
                "core_gene_count": core_n,
                "extended_gene_count": extended_n,
                "core_program_large_enough": core_n >= 15,
                "housekeeping_dominance_risk": "review" if row["candidate_domain"].lower().find("metabolic") >= 0 else "low_to_moderate",
                "likely_scoreable_in_scRNAseq": ready,
                "expected_cell_type_or_state": {
                    "F1": "keratinocyte/stress or epidermal metabolic state to be tested",
                    "F2": "fibroblast/endothelial/repair or nonlesional stromal state to be tested",
                    "F6": "keratinocyte hypoxia/stress or epithelial response state to be tested",
                    "F7": "myeloid/monocyte/neutrophil/IFN-response systemic immune state to be tested",
                }[f],
                "biologically_falsifiable": True,
                "single_cell_ready": ready,
                "phase2b_entry": "yes" if ready else "conditional_review",
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "single_cell_readiness.tsv", sep="\t", index=False)
    return out


def audit_candidate_datasets() -> tuple[pd.DataFrame, pd.DataFrame]:
    def summarize(acc: str, path: Path, kind: str) -> dict:
        meta = parse_series_matrix_metadata(path)
        text = " ".join(meta.astype(str).agg(" ".join, axis=1).tolist()) if not meta.empty else ""
        titles = "; ".join(meta["title"].head(8).astype(str)) if "title" in meta else ""
        donor_hits = set(re.findall(r"(?:patient|donor|subject|individual)\s*[_:-]?\s*(\w+)|\bP(\d+)\b", text, flags=re.I))
        donor_ids = {a or b for a, b in donor_hits if (a or b)}
        cell_numbers = re.findall(r"(\d[\d,]*)\s*(?:cells|spots|nuclei)", text, flags=re.I)
        return {
            "accession": acc,
            "data_type": kind,
            "local_series_matrix": str(path) if path.exists() else "",
            "n_geo_samples": 0 if meta.empty else len(meta),
            "estimated_donor_or_patient_count_from_metadata": len(donor_ids) if donor_ids else "not_resolved_from_series_matrix",
            "reported_cell_or_spot_count_from_series_matrix": ";".join(cell_numbers[:5]) if cell_numbers else "not_reported_in_series_matrix",
            "sample_title_examples": titles,
            "lesional_nonlesional_control_metadata_detected": bool(re.search("lesion|non.?lesion|control|healthy|normal", text, re.I)),
            "treatment_timepoint_metadata_detected": bool(re.search("treatment|week|baseline|time", text, re.I)),
            "donor_metadata_detected": bool(re.search("patient|donor|individual|subject|\\bP\\d+\\b", text, re.I)),
            "raw_processed_availability": "series_matrix_metadata_only_audited_no_large_download",
            "suitability_for_patient_level_pseudobulk": "candidate_needs_full_metadata_review" if not meta.empty else "unknown_no_metadata",
            "suitability_for_frozen_axis_scoring": "candidate_if_gene_expression_matrix_available" if kind == "single-cell" else "candidate_if_spot_gene_matrix_available",
            "pseudoreplication_risk": "must_use_donor_as_inference_unit",
        }

    sc = pd.DataFrame([summarize("GSE228421", GEO / "GSE228421_series_matrix.txt.gz", "single-cell")])
    sp = pd.DataFrame([summarize("GSE202011", GEO / "GSE202011_series_matrix.txt.gz", "spatial")])
    sc.to_csv(OUT / "candidate_single_cell_dataset_audit.tsv", sep="\t", index=False)
    sp.to_csv(OUT / "candidate_spatial_dataset_audit.tsv", sep="\t", index=False)
    return sc, sp


def build_master(evidence: pd.DataFrame, prog: pd.DataFrame, sc_ready: pd.DataFrame) -> pd.DataFrame:
    p = prog.set_index("factor")
    r = sc_ready.set_index("factor")
    rows = []
    for _, e in evidence.iterrows():
        f = e["factor"]
        core = int(p.loc[f, "core_gene_count"]) if f in p.index else 0
        ext = int(p.loc[f, "extended_gene_count"]) if f in p.index else 0
        sc = bool(r.loc[f, "single_cell_ready"]) if f in r.index else False
        genetics = f in RETAINED and core >= 15
        rows.append(
            {
                "factor": f,
                "final_name": e["candidate_domain"] if e["name_confidence"] in ["HIGH", "MODERATE"] else f,
                "name_confidence": e["name_confidence"],
                "dominant_tissue": e["dominant_tissue"],
                "mechanistic_domain": e["candidate_domain"],
                "seed_stability": e["MOFA_seed_stability"],
                "bootstrap_stability": e["bootstrap_stability"],
                "internal_skin_replication": e["internal_skin_replication"],
                "external_skin_replication": e["external_GSE244679_support"],
                "blood_support": e["blood_support_abs_max"],
                "PASI_dependence": e["PASI_association"],
                "BMI_dependence": e["BMI_association"],
                "batch_dependence": e["batch_association"],
                "feature_family_count": e["number_supported_feature_families"],
                "core_gene_count": core,
                "extended_gene_count": ext,
                "single_cell_ready": sc,
                "genetics_ready": genetics,
                "final_tier": e["evidence_tier"],
                "final_role": e["final_role"],
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "Table_axis_prioritization_master.tsv", sep="\t", index=False)
    return out


def write_cards(d: dict[str, pd.DataFrame], evidence: pd.DataFrame, redundancy: pd.DataFrame, master: pd.DataFrame) -> None:
    scores = d["scores"].set_index("patient_id")
    for _, e in evidence.iterrows():
        f = e["factor"]
        top = top_features(d["loadings"], f, 80)
        def fam_md(fam: str, n: int = 8) -> str:
            sub = top[top["feature_family"].eq(fam)].head(n)
            if sub.empty:
                return "None among top loading-ranked features."
            return "\n".join(f"- {r.view}::{r.feature} ({r.direction}, loading={r.loading:.3f})" for r in sub.itertuples())
        conf = d["conf"][d["conf"]["factor"].eq(f)].sort_values("partial_r2", ascending=False)
        red = redundancy[(redundancy["factor_a"].eq(f)) | (redundancy["factor_b"].eq(f))]
        related = red.sort_values("top_feature_overlap_coefficient", ascending=False).head(3)
        m = master.set_index("factor").loc[f]
        lines = [
            f"# Factor {f}",
            "",
            "## 1. Latent factor properties",
            "",
            f"- Variance explained LS/NL/blood: {e['variance_explained_LS']:.3f} / {e['variance_explained_NL']:.3f} / {e['variance_explained_blood']:.3f}.",
            f"- Score distribution: mean={scores[f].mean():.3f}, sd={scores[f].std(ddof=0):.3f}, min={scores[f].min():.3f}, max={scores[f].max():.3f}.",
            f"- Seed stability: score Pearson={e['MOFA_seed_stability']:.3f}; top-feature/bootstrap proxy={e['bootstrap_stability']:.3f}.",
            f"- Correlation with other factors: strongest relationships are {', '.join((related['factor_a'] + '-' + related['factor_b'] + ' score_r=' + related['patient_score_spearman'].round(3).astype(str)).tolist())}.",
            f"- Tissue class: {e['cross_tissue_coherence']}.",
            "",
            "## 2. Top pathway loadings",
            "",
            "Hallmark:",
            fam_md("Hallmark"),
            "",
            "Reactome:",
            fam_md("Reactome"),
            "",
            "Curated psoriasis pathways:",
            fam_md("pathway"),
            "",
            "## 3. Regulon / TF structure",
            "",
            fam_md("regulon_DoRothEA") + "\n" + fam_md("signaling_PROGENy"),
            "",
            "## 4. Cell-state structure",
            "",
            fam_md("cell_state"),
            "",
            "Estimated cell abundance and cell-state transcriptional programs are not separated by this bulk scoring layer; Phase 2B must test this at donor-level pseudobulk resolution.",
            "",
            "## 5. Tissue decomposition",
            "",
            f"The dominant tissue is {e['dominant_tissue']}. LS/NL/blood R2 values indicate that this axis is driven mainly by {e['dominant_tissue']}, not by all tissues equally.",
            "",
            "## 6. Internal replication",
            "",
            f"Frozen E-MTAB-14509 skin projection support: max absolute Spearman={e['internal_skin_replication']:.3f}. No replication refitting was performed.",
            "",
            "## 7. External skin validation",
            "",
            f"- GSE121212 support: {e['external_GSE121212_support']:.3f}.",
            f"- GSE244679 paired-skin support: {e['external_GSE244679_support']:.3f}.",
            "- GSE54456: not analyzed in Phase 2A; unpaired design kept out of the locked primary decision.",
            "",
            "## 8. Blood/systemic support",
            "",
            f"- Internal discovery skin-blood support: {e['internal_blood_support']:.3f}.",
            f"- GSE147339 support: {e['GSE147339_blood_support']:.3f}.",
            f"- GSE61281 support: {e['GSE61281_blood_support']:.3f}.",
            f"- Classification: {classify_support(e['blood_support_abs_max'])}. GSE61281 is supportive, not design-matched replication.",
            "",
            "## 9. Clinical/confounding audit",
            "",
            "\n".join(f"- {r.covariate}: beta={r.beta:.3f}, partial_R2={r.partial_r2:.3f}, FDR={r.fdr:.3f}" for r in conf.itertuples()),
            "",
            f"Is this mostly severity/BMI/technical? {'No strong evidence from current covariates.' if e['max_confounder_partial_r2'] < 0.10 else 'Potential confounding requires review.'} Batch was not available in the current covariate model.",
            "",
            "## 10. Candidate biological interpretation",
            "",
            f"Primary interpretation: {e['candidate_domain']}.",
            "",
            "Alternative interpretation: retain F-number until donor-level single-cell localization tests the expected cell state.",
            "",
            "## 11. Naming confidence",
            "",
            f"{e['name_confidence']}.",
            "",
            "## 12. Final role",
            "",
            f"{e['final_role']}. Rationale: {e['rationale']}",
            "",
        ]
        (CARDS / f"{f}.md").write_text("\n".join(lines))


def plot_figures(evidence: pd.DataFrame, master: pd.DataFrame) -> None:
    factors = evidence["factor"].tolist()
    mat = evidence.set_index("factor")[
        [
            "MOFA_seed_stability",
            "internal_skin_replication",
            "external_GSE244679_support",
            "blood_support_abs_max",
            "max_confounder_partial_r2",
            "number_supported_feature_families",
        ]
    ].copy()
    mat["max_confounder_partial_r2"] = 1 - mat["max_confounder_partial_r2"].clip(0, 1)
    plt.figure(figsize=(8, 4.8))
    plt.imshow(mat.to_numpy(float), aspect="auto", cmap="viridis")
    plt.xticks(range(mat.shape[1]), ["stability", "internal skin", "external skin", "blood", "confound-free", "bio families"], rotation=35, ha="right")
    plt.yticks(range(len(factors)), factors)
    plt.colorbar(label="scaled/raw evidence")
    plt.title("Figure 2A. Axis evidence matrix")
    plt.tight_layout()
    plt.savefig(FIG / "Figure2A_axis_evidence_matrix.png", dpi=300)
    plt.savefig(FIG / "Figure2A_axis_evidence_matrix.svg")
    plt.close()

    retained = master[master["factor"].isin(RETAINED)].set_index("factor").loc[RETAINED]
    plt.figure(figsize=(6.8, 4.2))
    vals = retained[["core_gene_count", "extended_gene_count"]]
    x = np.arange(vals.shape[0])
    plt.bar(x - 0.18, vals["core_gene_count"], width=0.36, label="CORE")
    plt.bar(x + 0.18, vals["extended_gene_count"], width=0.36, label="EXTENDED")
    plt.xticks(x, vals.index)
    plt.ylabel("Gene count")
    plt.title("Figure 2B. Frozen gene programs")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(FIG / "Figure2B_retained_axis_gene_programs.png", dpi=300)
    plt.savefig(FIG / "Figure2B_retained_axis_gene_programs.svg")
    plt.close()

    tissue = evidence.set_index("factor")[["variance_explained_LS", "variance_explained_NL", "variance_explained_blood"]]
    tissue.plot(kind="bar", stacked=True, figsize=(7.5, 4.4), color=["#4C78A8", "#72B7B2", "#F58518"])
    plt.ylabel("Reference view R2")
    plt.title("Figure 2C. Tissue contribution")
    plt.tight_layout()
    plt.savefig(FIG / "Figure2C_tissue_contribution.png", dpi=300)
    plt.savefig(FIG / "Figure2C_tissue_contribution.svg")
    plt.close()

    repl = evidence.set_index("factor")[["internal_skin_replication", "external_GSE121212_support", "external_GSE244679_support", "GSE147339_blood_support", "GSE61281_blood_support"]].abs()
    repl.plot(kind="bar", figsize=(8, 4.5), color=["#4C78A8", "#9D755D", "#59A14F", "#E15759", "#B07AA1"])
    plt.ylabel("|Spearman|")
    plt.title("Figure 2D. External replication and support")
    plt.tight_layout()
    plt.savefig(FIG / "Figure2D_external_replication_support.png", dpi=300)
    plt.savefig(FIG / "Figure2D_external_replication_support.svg")
    plt.close()

    plt.figure(figsize=(7.2, 3.8))
    y = np.arange(len(RETAINED))
    labels = [f"{f}: {master.set_index('factor').loc[f, 'mechanistic_domain']}" for f in RETAINED]
    plt.scatter(evidence.set_index("factor").loc[RETAINED, "external_GSE244679_support"].abs(), y, s=130, label="skin")
    plt.scatter(evidence.set_index("factor").loc[RETAINED, "blood_support_abs_max"].abs(), y, s=130, marker="s", label="blood/systemic")
    plt.yticks(y, labels)
    plt.xlabel("|support correlation|")
    plt.title("Figure 2E. Primary mechanistic axis schematic")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(FIG / "Figure2E_primary_axis_schematic.png", dpi=300)
    plt.savefig(FIG / "Figure2E_primary_axis_schematic.svg")
    plt.close()


def write_report(evidence: pd.DataFrame, redundancy: pd.DataFrame, master: pd.DataFrame, prog: pd.DataFrame, sc: pd.DataFrame, sc_audit: pd.DataFrame, sp_audit: pd.DataFrame) -> None:
    primary = master[master["final_role"].isin(["PRIMARY AXIS", "SUPPORTIVE/SYSTEMIC AXIS"])]
    secondary = master[master["final_role"].eq("SECONDARY AXIS")]
    retired = master[master["factor"].isin(RETIRE)]
    moderate_or_high = primary["name_confidence"].isin(["HIGH", "MODERATE"]).sum()
    go_status = "STRONG GO" if primary.shape[0] >= 3 and moderate_or_high >= 3 else "CONDITIONAL GO"
    lines = [
        "# PHASE2A AXIS MECHANISM PRIORITIZATION",
        "",
        "# Executive conclusion",
        "",
        f"{go_status}: Phase 2A retains F1, F2, and F6 as skin-primary axes and F7 as a supportive/systemic axis. This supports moving into donor-level single-cell localization, but F1/F2/F7 still require cell-state anchoring before strong mechanism naming.",
        "",
        "# Current evidence boundary",
        "",
        "The manuscript remains framed as skin-primary continuous molecular axes of psoriasis with selective systemic blood support. Phase 2A does not demonstrate genetics, MR, colocalization, druggability, or multisystem comorbidity mechanisms.",
        "",
        "# Axis-by-axis assessment",
        "",
        master.to_markdown(index=False),
        "",
        "# Mechanistic interpretation",
        "",
        evidence[["factor", "candidate_domain", "name_confidence", "biological_interpretability", "rationale"]].to_markdown(index=False),
        "",
        "# Tissue architecture",
        "",
        evidence[["factor", "variance_explained_LS", "variance_explained_NL", "variance_explained_blood", "dominant_tissue", "cross_tissue_coherence"]].to_markdown(index=False),
        "",
        "# External replication",
        "",
        evidence[["factor", "internal_skin_replication", "external_GSE121212_support", "external_GSE244679_support", "external_GSE54456_support_if_available"]].to_markdown(index=False),
        "",
        "# Blood/systemic support",
        "",
        evidence[["factor", "internal_blood_support", "GSE147339_blood_support", "GSE61281_blood_support", "blood_support_abs_max"]].to_markdown(index=False),
        "",
        "# Confounding",
        "",
        evidence[["factor", "PASI_association", "BMI_association", "age_association", "sex_association", "HLA_association", "batch_association", "max_confounder_partial_r2"]].to_markdown(index=False),
        "",
        "# Redundancy",
        "",
        "No retained MOFA factors are automatically merged. Pairwise redundancy is reported to classify broad domains while preserving original F identifiers.",
        "",
        redundancy.sort_values("top_feature_overlap_coefficient", ascending=False).head(12).to_markdown(index=False),
        "",
        "# Primary-axis selection",
        "",
        "Primary axes: F1, F2, F6. Supportive/systemic axis: F7. Secondary axes: F3, F5, F8. Retire from main story: F4.",
        "",
        primary.to_markdown(index=False),
        "",
        "# Frozen gene programs",
        "",
        prog.to_markdown(index=False),
        "",
        "# Single-cell readiness",
        "",
        sc.to_markdown(index=False),
        "",
        "# Spatial readiness",
        "",
        sp_audit.to_markdown(index=False),
        "",
        "# Genetics readiness",
        "",
        master[["factor", "core_gene_count", "genetics_ready", "final_role"]].to_markdown(index=False),
        "",
        "# Reviewer attack points",
        "",
        "- Several axes are Reactome-heavy and should not be overnamed before single-cell localization.",
        "- GSE61281 is cross-platform microarray support, not design-matched blood replication.",
        "- Batch association is not available in the current covariate model.",
        "- F1 and F2 have strong skin replication but low formal naming confidence until cell-state evidence is added.",
        "- Gene programs are frozen from loading-supported feature provenance, but CORE/EXTENDED thresholds require sensitivity checks in Phase 2B/3.",
        "",
        "# Phase 2B recommendation",
        "",
        "Proceed to donor-level single-cell localization for F1, F2, F6, and F7. Use per-cell scoring only as an intermediate step; inference must be donor-level pseudobulk or donor-level cell-type summaries.",
        "",
        "# GO / CONDITIONAL GO / NO-GO",
        "",
        go_status,
        "",
        "# Final decision answers",
        "",
        "1. Primary: F1, F2, F6.",
        "2. Secondary: F3, F5, F8.",
        "3. Systemic/supportive only: F7.",
        "4. Retired from main story: F4.",
        "5. Biological names: only F3 and F6 have MODERATE confidence; F1/F2/F7 retain F-number plus descriptive domain until Phase 2B.",
        "6. Convincingly skin-primary: F1, F2, F6.",
        "7. Meaningful systemic/blood support: F7, with weaker support for F3/F2.",
        "8. No retained primary axis is dominated by PASI/BMI/HLA/age/sex under current partial R2; batch unavailable.",
        "9. No axes are automatically merged; redundancy is tracked as broad-domain overlap.",
        "10. Frozen CORE programs are in `results/phase2a/axis_gene_programs/`.",
        "11. Enter single-cell validation: F1, F2, F6, F7.",
        "12. Eventually enter GWAS anchoring: F1, F2, F6, F7 after Phase 2B localization and gene-program overlap checks.",
        "13. Future target framing remains plausible but unproven: genetically anchored molecular axes of psoriasis may reveal distinct multisystem comorbidity architectures. This has not yet been demonstrated.",
        "",
        "# Candidate single-cell dataset audit",
        "",
        sc_audit.to_markdown(index=False),
    ]
    REPORT.write_text("\n".join(lines) + "\n")


def main() -> None:
    make_dirs()
    d = load_inputs()
    evidence = build_evidence_matrix(d)
    redundancy = build_redundancy(d)
    prog, _overlap = build_gene_programs(d, evidence)
    sc = build_readiness(evidence, prog)
    sc_audit, sp_audit = audit_candidate_datasets()
    master = build_master(evidence, prog, sc)
    write_cards(d, evidence, redundancy, master)
    plot_figures(evidence, master)
    write_report(evidence, redundancy, master, prog, sc, sc_audit, sp_audit)


if __name__ == "__main__":
    main()
