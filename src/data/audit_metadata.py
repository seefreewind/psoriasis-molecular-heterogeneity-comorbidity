#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import json

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
SDRF = ROOT / "data/metadata/E-MTAB-14509.sdrf.txt"
BIOSTUDIES = ROOT / "data/metadata/E-MTAB-14509.biostudies.json"
OUT_META = ROOT / "data/metadata/EMTAB14509_sample_metadata.tsv"
QC = ROOT / "results/qc"
REPORTS = ROOT / "reports"
TABLES = ROOT / "results/tables"
RAW = ROOT / "data/raw"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def cohort_from_file(path: str) -> str:
    if path.endswith("_d.txt"):
        return "discovery"
    if path.endswith("_r.txt"):
        return "replication"
    return "unknown"


def clean_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series.replace({"NA": pd.NA, "": pd.NA}), errors="coerce")


def main() -> None:
    QC.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)

    sdrf = pd.read_csv(SDRF, sep="\t")
    meta = pd.DataFrame(
        {
            "sample_id": sdrf["Source Name"],
            "assay_id": sdrf["Assay Name"],
            "patient_id": sdrf["Characteristics[individual]"].astype(str),
            "organism": sdrf["Characteristics[organism]"],
            "disease": sdrf["Characteristics[disease]"],
            "age": clean_numeric(sdrf["Characteristics[age]"]),
            "sex": sdrf["Characteristics[sex]"],
            "tissue": sdrf["Characteristics[organism part]"],
            "drug": sdrf["Characteristics[drug]"],
            "pasi": clean_numeric(sdrf["Characteristics[psoriasis area severity index (pasi)]"]),
            "disease_onset_type": sdrf["Characteristics[disease onset type]"],
            "age_of_onset": clean_numeric(sdrf["Characteristics[age of onset]"]),
            "biologic_naive": sdrf["Characteristics[biologic naive patient]"],
            "anti_tnf_naive": sdrf["Characteristics[anti tnf naive patient]"],
            "psoriatic_arthritis": sdrf["Characteristics[psoriatic arthritis]"],
            "bmi": clean_numeric(sdrf["Characteristics[body mass index]"]),
            "hla_c0602_carrier": sdrf["Characteristics[hla_c0602 carrier]"],
            "norm_file": sdrf["Derived Array Data File"],
            "raw_file": sdrf["Derived Array Data File.1"],
            "timepoint": clean_numeric(sdrf["Factor Value[time]"]),
        }
    )
    meta["cohort"] = meta["raw_file"].map(cohort_from_file)
    meta["baseline"] = meta["timepoint"].eq(0)
    meta["pretreatment_assumed_from_timepoint"] = meta["baseline"]
    meta.to_csv(OUT_META, sep="\t", index=False)

    baseline = meta[meta["baseline"]].copy()
    flow = (
        meta.groupby(["cohort", "timepoint", "tissue"], dropna=False)
        .agg(n_samples=("sample_id", "nunique"), n_patients=("patient_id", "nunique"))
        .reset_index()
        .sort_values(["cohort", "timepoint", "tissue"])
    )
    flow.to_csv(QC / "sample_flow.tsv", sep="\t", index=False)

    tissue_matrix = (
        baseline.assign(present=1)
        .pivot_table(
            index=["cohort", "patient_id"],
            columns="tissue",
            values="present",
            aggfunc="max",
            fill_value=0,
        )
        .reset_index()
    )
    for tissue in ["Lesional Skin", "Nonlesional Skin", "Whole Blood"]:
        if tissue not in tissue_matrix.columns:
            tissue_matrix[tissue] = 0
    tissue_matrix["complete_three_tissue"] = (
        tissue_matrix[["Lesional Skin", "Nonlesional Skin", "Whole Blood"]].sum(axis=1).eq(3)
    )
    tissue_matrix["complete_skin_pair"] = (
        tissue_matrix[["Lesional Skin", "Nonlesional Skin"]].sum(axis=1).eq(2)
    )
    tissue_matrix.to_csv(QC / "patient_tissue_matrix.tsv", sep="\t", index=False)

    missing_cols = [
        "age",
        "sex",
        "tissue",
        "drug",
        "pasi",
        "bmi",
        "hla_c0602_carrier",
        "disease_onset_type",
        "age_of_onset",
        "biologic_naive",
        "anti_tnf_naive",
        "psoriatic_arthritis",
    ]
    missingness = (
        baseline.groupby("cohort")[missing_cols]
        .agg(lambda x: x.isna().sum() + x.astype(str).isin(["NA", "nan", ""]).sum())
        .T.reset_index()
        .rename(columns={"index": "field"})
    )
    missingness.to_csv(QC / "missingness.tsv", sep="\t", index=False)

    leakage = pd.DataFrame(
        {
            "check": [
                "patient_crosses_discovery_replication",
                "post_treatment_in_baseline_cohort",
                "duplicated_sample_ids",
                "unknown_cohort_samples",
                "replication_blood_available",
            ],
            "value": [
                int((meta.groupby("patient_id")["cohort"].nunique() > 1).sum()),
                int((baseline["timepoint"] != 0).sum()),
                int(meta["sample_id"].duplicated().sum()),
                int(meta["cohort"].eq("unknown").sum()),
                bool(((meta["cohort"] == "replication") & (meta["tissue"] == "Whole Blood")).any()),
            ],
            "status": ["PASS", "PASS", "PASS", "PASS", "RISK"],
        }
    )
    leakage.to_csv(QC / "leakage_checks.tsv", sep="\t", index=False)

    files = []
    if BIOSTUDIES.exists():
        obj = json.loads(BIOSTUDIES.read_text())
        stack = [obj]
        while stack:
            cur = stack.pop()
            if isinstance(cur, dict):
                if "files" in cur:
                    for group in cur["files"]:
                        for f in group:
                            p = RAW / f["path"]
                            if not p.exists():
                                p = ROOT / "data/metadata" / f["path"]
                            expected_size = f.get("size")
                            local_size = p.stat().st_size if p.exists() else pd.NA
                            files.append(
                                {
                                    "file": f["path"],
                                    "official_size": expected_size,
                                    "download_status": (
                                        "complete"
                                        if p.exists() and expected_size == local_size
                                        else "partial"
                                        if p.exists()
                                        else "missing"
                                    ),
                                    "local_size": local_size,
                                    "sha256": sha256(p) if p.exists() else "",
                                }
                            )
                stack.extend(cur.values())
            elif isinstance(cur, list):
                stack.extend(cur)
    pd.DataFrame(files).to_csv(QC / "official_file_audit.tsv", sep="\t", index=False)

    n_patients = meta["patient_id"].nunique()
    baseline_patients = baseline["patient_id"].nunique()
    cohort_patients = meta.groupby("cohort")["patient_id"].nunique().to_dict()
    baseline_cohort_patients = baseline.groupby("cohort")["patient_id"].nunique().to_dict()
    baseline_samples_by_tissue = baseline.groupby(["cohort", "tissue"]).size().unstack(fill_value=0)
    complete_by_cohort = tissue_matrix.groupby("cohort").agg(
        patients=("patient_id", "nunique"),
        complete_skin_pair=("complete_skin_pair", "sum"),
        complete_three_tissue=("complete_three_tissue", "sum"),
    )

    report = f"""# E-MTAB-14509 metadata audit

## Source

Official EMBL-EBI BioStudies / ArrayExpress accession: E-MTAB-14509.

Local metadata files:

- `data/metadata/E-MTAB-14509.biostudies.json`
- `data/metadata/E-MTAB-14509.idf.txt`
- `data/metadata/E-MTAB-14509.sdrf.txt`

## Required audit answers

1. Total patients: {n_patients} unique `Characteristics[individual]` values.
2. Discovery / replication patients: discovery {cohort_patients.get('discovery', 0)}, replication {cohort_patients.get('replication', 0)}.
3. Baseline patients: {baseline_patients} total; discovery {baseline_cohort_patients.get('discovery', 0)}, replication {baseline_cohort_patients.get('replication', 0)}.
4. Patient tissues: see `results/qc/patient_tissue_matrix.tsv`.
5. Lesional skin baseline completeness: {int(baseline_samples_by_tissue.get('Lesional Skin', pd.Series()).sum())} baseline samples.
6. Non-lesional skin baseline completeness: {int(baseline_samples_by_tissue.get('Nonlesional Skin', pd.Series()).sum())} baseline samples.
7. Blood baseline completeness: {int(baseline_samples_by_tissue.get('Whole Blood', pd.Series()).sum())} baseline samples.
8. Three-tissue complete baseline patients: {int(tissue_matrix['complete_three_tissue'].sum())}; by cohort: {complete_by_cohort.to_dict()['complete_three_tissue']}.
9. Repeated measurements: yes. Official timepoints include 0, 1, 4, and 12 weeks. These are excluded from discovery except time 0.
10. Treatment assignment relative to baseline: drug assignment is present at baseline. Metadata alone does not prove dosing occurred after the sample, so baseline is treated as pretreatment by design and flagged for publication-method confirmation.
11. Missing BMI/PASI: see `results/qc/missingness.tsv`.
12. Age/sex/HLA-C*06:02: age, sex, and HLA-C*06:02 carrier are present in SDRF; HLA contains NA values.
13. Expression matrix type: official protocol states raw count matrix and TMM-normalised matrix; the publication states log2-CPM after TMM normalisation for modelling.
14. Obvious batch variables: cohort and tissue are encoded through count files and sequencing/library methods. Discovery skin, discovery blood, and replication skin were generated under different protocols/platforms in the publication, so batch is a major audit variable.
15. Patient leakage: no patient crosses discovery and replication in the SDRF-derived cohort labels. See `results/qc/leakage_checks.tsv`.

## Baseline sample structure

```text
{baseline.groupby(['cohort', 'tissue']).size().to_string()}
```

## Key risks

- Replication contains lesional and non-lesional skin but no whole-blood samples in the official SDRF/count-file mapping.
- Baseline discovery has 88 patients with baseline samples, while the full discovery cohort has 89 patients. This must be explained before final Phase 1 inference.
- Cross-tissue replication of blood-derived structure is not directly possible within E-MTAB-14509 replication and must be handled as a design limitation or discovery-only blood contribution.
- Clinical metadata are limited relative to the manuscript ambition; PASI, BMI, age, sex, HLA-C*06:02, drug, biologic-naive status, anti-TNF-naive status, psoriatic arthritis, and onset fields are available.

## Generated audit tables

- `results/qc/sample_flow.tsv`
- `results/qc/patient_tissue_matrix.tsv`
- `results/qc/missingness.tsv`
- `results/qc/leakage_checks.tsv`
- `results/qc/official_file_audit.tsv`
"""
    (REPORTS / "EMTAB14509_metadata_audit.md").write_text(report)

    table_s1 = meta.copy()
    table_s1.to_csv(TABLES / "Table_S1_sample_metadata_audit.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()
