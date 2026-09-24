#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data/raw"
META = ROOT / "data/metadata/EMTAB14509_sample_metadata.tsv"
QC = ROOT / "results/qc"
FIG = ROOT / "results/figures"
TABLES = ROOT / "results/tables"


MATRICES = [
    ("Skin_norm_counts_d.txt", "norm", "skin", "discovery"),
    ("Skin_norm_counts_r.txt", "norm", "skin", "replication"),
    ("Blood_norm_counts_d.txt", "norm", "blood", "discovery"),
    ("Skin_raw_counts_d.txt", "raw", "skin", "discovery"),
    ("Skin_raw_counts_r.txt", "raw", "skin", "replication"),
    ("Blood_raw_counts_d.txt", "raw", "blood", "discovery"),
]


def read_matrix(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", index_col=0)


def qc_one(file_name: str, matrix_type: str, tissue_group: str, cohort: str) -> pd.DataFrame:
    path = RAW / file_name
    if not path.exists():
        return pd.DataFrame()
    audit_path = QC / "official_file_audit.tsv"
    if audit_path.exists():
        audit = pd.read_csv(audit_path, sep="\t")
        status = audit.loc[audit["file"].eq(file_name), "download_status"]
        if len(status) and status.iloc[0] != "complete":
            return pd.DataFrame(
                [
                    {
                        "sample_id": pd.NA,
                        "source_file": file_name,
                        "matrix_type": matrix_type,
                        "tissue_group": tissue_group,
                        "cohort_from_file": cohort,
                        "download_status": status.iloc[0],
                    }
                ]
            )
    df = read_matrix(path)
    vals = df.select_dtypes(include=[np.number])
    if matrix_type == "raw":
        detected = (vals > 0).sum(axis=0)
        total = vals.sum(axis=0)
    else:
        detected = vals.notna().sum(axis=0)
        total = vals.sum(axis=0)
    out = pd.DataFrame(
        {
            "sample_id": vals.columns,
            "source_file": file_name,
            "matrix_type": matrix_type,
            "tissue_group": tissue_group,
            "cohort_from_file": cohort,
            "n_features": vals.shape[0],
            "detected_features": detected.values,
            "total_signal": total.values,
            "missing_values": vals.isna().sum(axis=0).values,
        }
    )
    return out


def main() -> None:
    QC.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    meta = pd.read_csv(META, sep="\t")
    rows = [qc_one(*x) for x in MATRICES]
    sample_qc = pd.concat([x for x in rows if len(x)], ignore_index=True)
    sample_qc = sample_qc.merge(
        meta[
            [
                "sample_id",
                "patient_id",
                "cohort",
                "tissue",
                "timepoint",
                "pasi",
                "bmi",
                "age",
                "sex",
                "hla_c0602_carrier",
            ]
        ],
        on="sample_id",
        how="left",
    )
    sample_qc["is_baseline"] = sample_qc["timepoint"].eq(0)
    sample_qc.to_csv(QC / "expression_sample_qc.tsv", sep="\t", index=False)

    exclusions = []
    complete_raw = set(
        pd.read_csv(QC / "official_file_audit.tsv", sep="\t")
        .query("download_status == 'complete'")["file"]
        .tolist()
    )
    if not {"Skin_raw_counts_d.txt", "Skin_raw_counts_r.txt", "Blood_raw_counts_d.txt"}.issubset(complete_raw):
        exclusions.append(
            {
                "sample": "ALL",
                "reason": "Raw-count QC is incomplete until all official raw matrices are fully downloaded.",
                "rule": "No sample-level raw-count exclusion before complete raw data availability.",
                "date": pd.Timestamp.today().date().isoformat(),
                "downstream_impact": "Normalized-matrix analyses may proceed as exploratory/locked-feature input, but raw library-size QC exclusions are deferred.",
            }
        )
    pd.DataFrame(exclusions).to_csv(TABLES / "Table_S2_QC_exclusions.tsv", sep="\t", index=False)

    baseline = sample_qc[sample_qc["is_baseline"] & sample_qc["matrix_type"].eq("norm")].copy()
    pca_rows = []
    for file_name, _, tissue_group, cohort in [x for x in MATRICES if x[1] == "norm"]:
        path = RAW / file_name
        if not path.exists():
            continue
        df = read_matrix(path)
        cols = baseline.loc[baseline["source_file"].eq(file_name), "sample_id"]
        cols = [c for c in cols if c in df.columns]
        if len(cols) < 5:
            continue
        x = df[cols].T
        x = x.loc[:, x.var(axis=0).sort_values(ascending=False).head(min(2000, x.shape[1])).index]
        x = (x - x.mean(axis=0)) / x.std(axis=0).replace(0, np.nan)
        x = x.fillna(0)
        p = PCA(n_components=2, random_state=20260810).fit_transform(x)
        for sample_id, pc in zip(cols, p):
            pca_rows.append(
                {
                    "sample_id": sample_id,
                    "source_file": file_name,
                    "pc1": pc[0],
                    "pc2": pc[1],
                    "pca_scope": f"{cohort}_{tissue_group}_baseline_norm",
                }
            )
    pd.DataFrame(pca_rows).to_csv(QC / "baseline_norm_pca.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()
