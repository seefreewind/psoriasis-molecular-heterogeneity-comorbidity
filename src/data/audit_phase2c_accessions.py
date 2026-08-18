from __future__ import annotations

import csv
import gzip
import re
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
GEO_DIR = ROOT / "data" / "external" / "geo"
RESULT_DIR = ROOT / "results" / "phase2c"
REPORT_DIR = ROOT / "reports"


DATASETS = {
    "GSE228421": {
        "role": "Phase 2B-R internal/mechanistic refinement scRNA-seq dataset",
        "technology": "10x Genomics single-cell RNA-seq",
        "doi": "not_resolved_from_series_matrix",
        "expected": "psoriasis scRNA-seq, 5 donors, baseline LS/NL plus treated lesional timepoints",
    },
    "GSE173706": {
        "role": "Phase 2C independent single-cell validation atlas",
        "technology": "single-cell RNA-seq with associated spatial-sequencing study",
        "doi": "not_resolved_from_series_matrix",
        "expected": "independent psoriasis scRNA-seq with healthy, peripheral normal, and psoriatic samples",
    },
    "GSE225475": {
        "role": "Phase 2C primary spatial localization candidate",
        "technology": "10x Visium spatial transcriptomics",
        "doi": "10.1038/s41467-023-39020-4",
        "expected": "spatial psoriasis and healthy skin sections",
    },
    "GSE202011": {
        "role": "Phase 2C external spatial robustness dataset",
        "technology": "spatial transcriptomics",
        "doi": "not_resolved_from_series_matrix",
        "expected": "independent psoriasis/PsA spatial transcriptomics with LS/NL/healthy samples",
    },
}


def split_geo_line(line: str) -> list[str]:
    return next(csv.reader([line], delimiter="\t"))


def read_series_matrix(accession: str) -> tuple[dict[str, list[str]], pd.DataFrame]:
    path = GEO_DIR / f"{accession}_series_matrix.txt.gz"
    if not path.exists():
        alt = GEO_DIR / accession / f"{accession}_series_matrix.txt.gz"
        path = alt if alt.exists() else path
    if not path.exists():
        return {}, pd.DataFrame()

    series: dict[str, list[str]] = defaultdict(list)
    sample_fields: dict[str, list[list[str]]] = defaultdict(list)
    with gzip.open(path, "rt", errors="replace") as handle:
        for raw in handle:
            line = raw.rstrip("\n")
            if line.startswith("!Series_"):
                parts = split_geo_line(line)
                series[parts[0]].extend([p.strip('"') for p in parts[1:]])
            elif line.startswith("!Sample_"):
                parts = split_geo_line(line)
                sample_fields[parts[0]].append([p.strip('"') for p in parts[1:]])

    accessions = sample_fields.get("!Sample_geo_accession", [[]])[0]
    rows = []
    for idx, gsm in enumerate(accessions):
        row = {"sample_accession": gsm}
        for key, values in sample_fields.items():
            if key == "!Sample_geo_accession":
                continue
            cleaned_key = key.replace("!Sample_", "").lower()
            if len(values) == 1:
                row[cleaned_key] = values[0][idx] if idx < len(values[0]) else ""
            else:
                for pos, vals in enumerate(values, start=1):
                    row[f"{cleaned_key}_{pos}"] = vals[idx] if idx < len(vals) else ""
        rows.append(row)
    return dict(series), pd.DataFrame(rows)


def first(series: dict[str, list[str]], key: str) -> str:
    values = series.get(key, [])
    return values[0] if values else ""


def joined_row_text(row: pd.Series) -> str:
    return " | ".join(str(x) for x in row.fillna("").tolist())


def derive_sample_fields(accession: str, samples: pd.DataFrame) -> pd.DataFrame:
    if samples.empty:
        return samples

    rows = []
    for _, row in samples.iterrows():
        focused_values = []
        for col in row.index:
            if col == "title" or col == "source_name_ch1" or col.startswith("characteristics_ch1"):
                focused_values.append(str(row.get(col, "")))
        text = " | ".join(focused_values)
        lower = text.lower()
        title = str(row.get("title", ""))

        donor_id = ""
        donor_patterns = [r"subject id:\s*donor\s+([A-Za-z0-9_-]+)", r"individual:\s*([A-Za-z ]+\d+)"]
        if accession == "GSE228421":
            donor_patterns.append(r"\b(P\d+)\b")
        for pat in donor_patterns:
            match = re.search(pat, text, flags=re.IGNORECASE)
            if match:
                donor_id = re.sub(r"\s+", "_", match.group(1).strip())
                break

        if "psoriatic arthritis" in lower or "psa" in lower:
            disease_group = "PsA"
        elif "psoriasis" in lower or "psoriatic" in lower or " pso " in f" {lower} " or " pp-" in lower or "pn-" in lower:
            disease_group = "PsO"
        elif "healthy" in lower or "normal skin from donor ar" in lower:
            disease_group = "Healthy"
        else:
            disease_group = "unresolved"

        if "healthy" in lower or "normal skin from donor ar" in lower:
            tissue_state = "healthy"
        elif "non-lesional" in lower or "non lesional" in lower or "peripheral normal" in lower or "pn-" in lower:
            tissue_state = "nonlesional"
        elif "lesional" in lower or "psoriatic skin" in lower or "pp-" in lower:
            tissue_state = "lesional"
        elif "psoriasis skin" in lower:
            tissue_state = "psoriasis_unqualified"
        else:
            tissue_state = "unresolved"

        timepoint_text = f"{title} | {row.get('characteristics_ch1_2', '')}".lower()
        if "day 14" in timepoint_text or re.search(r"\b[Pp]\d+-V3\b", title):
            timepoint = "day14"
        elif "day 3" in timepoint_text or re.search(r"\b[Pp]\d+-V2\b", title):
            timepoint = "day3"
        elif "baseline" in timepoint_text or re.search(r"\b[Pp]\d+-V1\b", title):
            timepoint = "baseline"
        else:
            timepoint = "not_reported"

        out = row.to_dict()
        out.update(
            {
                "derived_donor_id": donor_id or "unresolved",
                "derived_disease_group": disease_group,
                "derived_tissue_state": tissue_state,
                "derived_timepoint": timepoint,
            }
        )
        rows.append(out)
    return pd.DataFrame(rows)


def summarize_counts(samples: pd.DataFrame, column: str) -> str:
    if samples.empty or column not in samples:
        return "0"
    counts = Counter(samples[column].fillna("unresolved"))
    return "; ".join(f"{k}={v}" for k, v in sorted(counts.items()))


def availability_flags(accession: str, series: dict[str, list[str]], samples: pd.DataFrame) -> dict[str, str]:
    supp_values = []
    supp_values.extend(series.get("!Series_supplementary_file", []))
    if not samples.empty:
        supp_cols = [c for c in samples.columns if c.startswith("supplementary_file")]
        for col in supp_cols:
            supp_values.extend(samples[col].dropna().astype(str).tolist())
    supp_text = " ".join(supp_values).lower()

    matrix = any(token in supp_text for token in [".h5", "matrix.mtx", ".csv", ".h5ad", ".rds", ".tar"])
    spatial_image = any(token in supp_text for token in ["image", "st_images", "spatial", "tissue_positions"])
    annotation = any(token in supp_text for token in ["annotation", "celltype", "cell_type", "cluster", "metadata"])

    local_complete = "not_downloaded"
    if accession == "GSE228421" and (ROOT / "results" / "phase2b" / "GSE228421_cell_axis_scores.tsv.gz").exists():
        local_complete = "analysis_ready_phase2b_outputs_present"
    elif accession == "GSE202011" and (GEO_DIR / accession / "GSE202011_RAW.tar.incomplete").exists():
        local_complete = "series_matrix_only_raw_tar_incomplete"
    elif accession in {"GSE173706", "GSE225475"}:
        local_complete = "series_matrix_only"

    return {
        "matrix_availability": "available_from_GEO_supplementary" if matrix else "not_apparent_from_series_matrix",
        "processed_object_availability": "not_apparent_or_not_author_integrated_object",
        "cell_annotation_availability": "not_apparent_from_series_matrix" if not annotation else "supplementary_annotation_apparent",
        "spatial_image_availability": "available_or_indicated" if spatial_image else "not_applicable_or_not_apparent",
        "download_status": local_complete,
    }


def suitability(accession: str, samples: pd.DataFrame, flags: dict[str, str]) -> tuple[str, str]:
    n = len(samples)
    donor_ok = (not samples.empty) and samples["derived_donor_id"].ne("unresolved").any()
    states = set(samples.get("derived_tissue_state", pd.Series(dtype=str)))
    groups = set(samples.get("derived_disease_group", pd.Series(dtype=str)))

    if accession == "GSE228421":
        ok = n == 20 and donor_ok and {"lesional", "nonlesional"} <= states
        return (
            "SUITABLE_FOR_PHASE2B_R" if ok else "AUDIT_FAIL",
            "Already processed locally; suitable only for one-pass refinement, not independent validation.",
        )
    if accession == "GSE173706":
        ok = n > 0 and donor_ok and {"healthy", "nonlesional", "lesional"} <= states and {"Healthy", "PsO"} <= groups
        return (
            "SUITABLE_PENDING_DOWNLOAD_AND_ANNOTATION_STRATEGY" if ok else "STOP_UNTIL_METADATA_RESOLVED",
            "Independent scRNA validation candidate; author-integrated object/cell annotations are not apparent in the series matrix, so analysis must use downloadable sample matrices plus transparent annotation or separately verified annotations.",
        )
    if accession == "GSE225475":
        ok = n == 6 and {"Healthy", "PsO"} <= groups and flags["matrix_availability"].startswith("available")
        return (
            "SUITABLE_PENDING_DOWNLOAD" if ok else "STOP_UNTIL_METADATA_RESOLVED",
            "Primary spatial candidate; small unpaired healthy-vs-psoriasis Visium design, no LS/NL pairing in GEO sample metadata.",
        )
    if accession == "GSE202011":
        ok = n == 30 and {"Healthy", "PsO", "PsA"} <= groups and {"lesional", "nonlesional", "healthy"} <= states
        return (
            "SUITABLE_PENDING_COMPLETE_DOWNLOAD" if ok else "STOP_UNTIL_METADATA_RESOLVED",
            "External spatial robustness dataset; must not be described as a single-cell atlas. Local RAW tar is incomplete and cannot be analyzed.",
        )
    return "UNRESOLVED", "Dataset role not configured."


def collect_supplementary_files(accession: str, series: dict[str, list[str]], samples: pd.DataFrame) -> list[dict[str, str]]:
    rows = []
    for url in series.get("!Series_supplementary_file", []):
        rows.append({"accession": accession, "level": "series", "sample_accession": "", "url": url})
    if not samples.empty:
        supp_cols = [c for c in samples.columns if c.startswith("supplementary_file")]
        for _, row in samples.iterrows():
            for col in supp_cols:
                url = str(row.get(col, ""))
                if url:
                    rows.append({"accession": accession, "level": "sample", "sample_accession": row["sample_accession"], "url": url})
    return rows


def update_data_manifest(audit: pd.DataFrame) -> None:
    manifest_path = ROOT / "DATA_MANIFEST.tsv"
    existing = pd.read_csv(manifest_path, sep="\t") if manifest_path.exists() else pd.DataFrame()
    columns = list(existing.columns)
    if not columns:
        raise RuntimeError("DATA_MANIFEST.tsv columns are required for controlled update")

    rows = []
    for _, row in audit.iterrows():
        rows.append(
            {
                "dataset_id": row["accession"],
                "repository": "NCBI GEO",
                "official_url": row["official_url"],
                "publication": row["title"],
                "doi": row["doi"],
                "data_type": row["technology"],
                "organism": "Homo sapiens",
                "disease": row["disease_scope"],
                "n_patients_reported": row["donor_summary"],
                "n_samples_reported": row["n_samples"],
                "tissues": "skin",
                "timepoints": row["timepoint_summary"],
                "treatment": row["treatment_status"],
                "raw_data_available": row["raw_data_available"],
                "processed_data_available": row["matrix_availability"],
                "metadata_available": "Yes, GEO series/sample metadata parsed",
                "patient_id_available": row["donor_id_status"],
                "discovery_replication_label": row["role"],
                "download_status": row["download_status"],
                "license": "not stated in GEO series matrix",
                "access_restriction": row["access_restriction"],
                "checksum": "not recorded",
                "notes": row["suitability"] + " | " + row["limitations"],
            }
        )

    update = pd.DataFrame(rows)
    if not existing.empty:
        existing = existing.loc[~existing["dataset_id"].isin(update["dataset_id"])]
    combined = pd.concat([existing, update], ignore_index=True)
    combined = combined.reindex(columns=columns)
    combined.to_csv(manifest_path, sep="\t", index=False)


def write_report(audit: pd.DataFrame) -> None:
    report = REPORT_DIR / "PHASE2C_DATASET_ACCESSION_AUDIT.md"
    lines = [
        "# Phase 2C Dataset Accession Audit",
        "",
        "本报告在进入 Phase 2B-R/2C 任何表达矩阵分析前生成，目的为锁定 accession、技术类型、样本结构和适用边界。所有判断均基于本地保存的官方 GEO series matrix 与项目内既有结果文件；未能从 series matrix 直接确认的信息标记为 unresolved，而不作隐含替代。",
        "",
        "## 总体结论",
        "",
        "- GSE228421：继续作为 Phase 2B-R 的内部单细胞精修数据集，不作为独立验证。",
        "- GSE173706：可作为独立 psoriasis scRNA-seq 验证候选；donor、健康/PN/PP 样本结构可从 GEO metadata 恢复，但作者整合对象和细胞注释未在 series matrix 中直接显示，下载后需要透明注释策略。",
        "- GSE225475：可作为 primary spatial localization 候选；它是 6 个 Visium 空间样本，不是单细胞，且 GEO metadata 不支持 LS/NL 配对分析。",
        "- GSE202011：可作为 external spatial robustness；它是 psoriasis/PsA 空间转录组数据集，不得再描述为单细胞 atlas。本地 RAW tar 目前是不完整下载，分析前必须重新完整获取。",
        "",
        "## 审计表",
        "",
        "| Accession | Role | Technology | Samples | Donor status | Tissue/disease states | Matrix | Annotation | Suitability |",
        "| --- | --- | --- | ---: | --- | --- | --- | --- | --- |",
    ]
    for _, row in audit.iterrows():
        lines.append(
            f"| {row['accession']} | {row['role']} | {row['technology']} | {row['n_samples']} | "
            f"{row['donor_id_status']} | {row['state_summary']} | {row['matrix_availability']} | "
            f"{row['cell_annotation_availability']} | {row['suitability']} |"
        )

    lines.extend(["", "## 数据集边界", ""])
    for _, row in audit.iterrows():
        lines.extend(
            [
                f"### {row['accession']}",
                "",
                f"- Official URL: {row['official_url']}",
                f"- Title: {row['title']}",
                f"- PubMed ID(s): {row['pubmed_ids']}",
                f"- DOI: {row['doi']}",
                f"- Repository: NCBI GEO",
                f"- Technology: {row['technology']}",
                f"- Role: {row['role']}",
                f"- Samples/cells/spots: {row['n_samples']} samples; cell/spot count not resolved from series matrix.",
                f"- LS/NL/healthy and PsO/PsA: {row['state_summary']}; {row['disease_scope']}",
                f"- Pairing/donor ID: {row['donor_id_status']}; {row['pairing_status']}",
                f"- Treatment/timepoint: {row['treatment_status']}; {row['timepoint_summary']}",
                f"- Matrix availability: {row['matrix_availability']}",
                f"- Processed object: {row['processed_object_availability']}",
                f"- Cell annotation: {row['cell_annotation_availability']}",
                f"- Spatial image: {row['spatial_image_availability']}",
                f"- Suitability: {row['suitability']}",
                f"- Limitation: {row['limitations']}",
                "",
            ]
        )

    lines.extend(
        [
            "## STOP 规则",
            "",
            "若下载后的实际文件与本审计的样本结构不一致，相关数据集立即停止使用，直到 accession、样本标签、donor ID、矩阵格式和注释来源被重新解析并记录。不得用其他数据集静默替换。",
            "",
            "本阶段是最后一次 transcriptomics rescue attempt。Phase 2B-R/2C 完成后，不能再仅为挽救机制命名而引入新的 bulk RNA、scRNA 或 spatial 数据集。",
        ]
    )
    report.write_text("\n".join(lines) + "\n")


def main() -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    audit_rows = []
    supp_rows = []
    for accession, config in DATASETS.items():
        series, samples = read_series_matrix(accession)
        samples = derive_sample_fields(accession, samples)
        if not samples.empty:
            samples.to_csv(RESULT_DIR / f"{accession}_sample_metadata_audit.tsv", sep="\t", index=False)
        supp_rows.extend(collect_supplementary_files(accession, series, samples))

        flags = availability_flags(accession, series, samples)
        fit, limitations = suitability(accession, samples, flags)
        recoverable_donors = (
            samples.loc[samples["derived_donor_id"].ne("unresolved"), "derived_donor_id"]
            if not samples.empty
            else pd.Series(dtype=str)
        )
        donor_counts = recoverable_donors.nunique()
        donor_status = (
            f"recoverable ({donor_counts} unique derived IDs)"
            if donor_counts > 0
            else "not recoverable from parsed metadata"
        )
        repeated_donors = recoverable_donors.value_counts()
        pairing = "paired/repeated donor samples apparent" if (not repeated_donors.empty and repeated_donors.max() > 1) else "no donor-level pairing apparent"
        raw_available = "series/sample supplementary files available" if series.get("!Series_supplementary_file") else "not apparent"
        access_restriction = "raw sequencing restricted per GEO note" if accession == "GSE228421" else "not apparent from series matrix"

        audit_rows.append(
            {
                "accession": accession,
                "official_url": f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={accession}",
                "title": first(series, "!Series_title"),
                "pubmed_ids": ";".join(series.get("!Series_pubmed_id", [])) or "not_reported",
                "doi": config["doi"],
                "repository": "NCBI GEO",
                "technology": config["technology"],
                "role": config["role"],
                "expected_role_check": config["expected"],
                "n_samples": len(samples),
                "donor_summary": f"{donor_counts} unique derived donor IDs",
                "donor_id_status": donor_status,
                "pairing_status": pairing,
                "state_summary": summarize_counts(samples, "derived_tissue_state"),
                "disease_scope": summarize_counts(samples, "derived_disease_group"),
                "timepoint_summary": summarize_counts(samples, "derived_timepoint"),
                "treatment_status": "risankizumab baseline/day3/day14" if accession == "GSE228421" else "baseline/cross-sectional or not reported",
                "raw_data_available": raw_available,
                "access_restriction": access_restriction,
                "matrix_availability": flags["matrix_availability"],
                "processed_object_availability": flags["processed_object_availability"],
                "cell_annotation_availability": flags["cell_annotation_availability"],
                "spatial_image_availability": flags["spatial_image_availability"],
                "download_status": flags["download_status"],
                "suitability": fit,
                "limitations": limitations,
            }
        )

    audit = pd.DataFrame(audit_rows)
    audit.to_csv(RESULT_DIR / "dataset_accession_audit.tsv", sep="\t", index=False)
    pd.DataFrame(supp_rows).to_csv(RESULT_DIR / "dataset_supplementary_files.tsv", sep="\t", index=False)
    update_data_manifest(audit)
    write_report(audit)
    print(audit[["accession", "n_samples", "state_summary", "disease_scope", "suitability"]].to_string(index=False))


if __name__ == "__main__":
    main()
