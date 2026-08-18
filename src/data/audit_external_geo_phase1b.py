#!/usr/bin/env python3
"""Audit and fetch feasible external GEO resources for Phase 1B."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "phase1b"
EXT = ROOT / "data" / "external" / "geo"


DATASETS = [
    {
        "accession": "GSE121212",
        "tissue": "skin",
        "technology": "RNA-seq",
        "design": "AD, psoriasis and controls; psoriasis lesional/non-lesional skin available",
        "official_sample_count": 147,
        "psoriasis_relevant_count": "28 psoriasis patients; mostly paired lesional/non-lesional skin",
        "compatibility_role": "external_skin_replication_candidate",
        "geo_url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE121212",
        "download_url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE121nnn/GSE121212/suppl/GSE121212_readcount.txt.gz",
        "download_policy": "fetch_processed",
    },
    {
        "accession": "GSE244679",
        "tissue": "skin",
        "technology": "RNA-seq",
        "design": "24 paired lesional psoriatic and adjacent normal skin samples",
        "official_sample_count": 48,
        "psoriasis_relevant_count": "24 paired lesional/adjacent normal",
        "compatibility_role": "external_skin_replication_candidate",
        "geo_url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE244679",
        "download_url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE244nnn/GSE244679/suppl/GSE244679_RAW.tar",
        "download_policy": "fetch_if_present_or_size_permits",
    },
    {
        "accession": "GSE54456",
        "tissue": "skin",
        "technology": "RNA-seq",
        "design": "92 lesional psoriatic and 82 normal punch biopsies; unpaired case-control",
        "official_sample_count": 174,
        "psoriasis_relevant_count": "92 psoriasis skin, 82 normal skin",
        "compatibility_role": "external_skin_support_unpaired",
        "geo_url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE54456",
        "download_url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE54nnn/GSE54456/suppl/GSE54456_RPKM_samples.txt.gz",
        "download_policy": "fetch_processed",
    },
    {
        "accession": "GSE147339",
        "tissue": "whole blood",
        "technology": "RNA-seq",
        "design": "cross-sectional psoriasis versus control whole-blood RNA-seq",
        "official_sample_count": 20,
        "psoriasis_relevant_count": "10 psoriasis, 10 controls inferred from sample titles",
        "compatibility_role": "external_blood_support_candidate",
        "geo_url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE147339",
        "download_url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE147nnn/GSE147339/suppl/GSE147339_counts.fpkm.csv.gz",
        "download_policy": "fetch_processed",
    },
    {
        "accession": "GSE61281",
        "tissue": "whole blood",
        "technology": "Agilent microarray",
        "design": "20 PsA, 20 cutaneous psoriasis without arthritis, 12 unaffected controls",
        "official_sample_count": 52,
        "psoriasis_relevant_count": "20 PsC; 20 PsA; 12 controls",
        "compatibility_role": "external_blood_support_microarray_candidate",
        "geo_url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE61281",
        "download_url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE61nnn/GSE61281/suppl/GSE61281_RAW.tar",
        "download_policy": "use_series_matrix_and_platform_annotation",
    },
]

SUPPORTING_FILES = {
    "GSE147339": [
        "GSE147339_series_matrix.txt.gz",
    ],
    "GSE244679": [
        "GSE244679_series_matrix.txt.gz",
    ],
    "GSE61281": [
        "GSE61281_series_matrix.txt.gz",
        "GPL6480.annot.gz",
    ],
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def fetch(url: str, dest: Path, max_mb: int = 100) -> tuple[str, int | None, str | None]:
    if dest.exists():
        return "already_present", dest.stat().st_size, sha256(dest)
    head = requests.head(url, allow_redirects=True, timeout=30)
    size = int(head.headers.get("content-length", "0") or 0)
    if size and size > max_mb * 1024 * 1024:
        return f"skipped_size_gt_{max_mb}mb", size, None
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with dest.open("wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
    return "downloaded", dest.stat().st_size, sha256(dest)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    EXT.mkdir(parents=True, exist_ok=True)
    rows = []
    for ds in DATASETS:
        filename = ds["download_url"].rsplit("/", 1)[-1]
        dest = EXT / filename
        if ds["download_policy"] == "fetch_if_present_or_size_permits":
            if dest.exists():
                status, size, checksum = "already_present_complete", dest.stat().st_size, sha256(dest)
            else:
                status, size, checksum = fetch(ds["download_url"], dest)
        elif ds["download_policy"] == "use_series_matrix_and_platform_annotation":
            support = [EXT / name for name in SUPPORTING_FILES.get(ds["accession"], [])]
            present = [p for p in support if p.exists()]
            if len(present) == len(support):
                status = "analysis_ready_series_matrix_and_platform_annotation"
                size = sum(p.stat().st_size for p in present)
                checksum = ";".join(f"{p.name}:{sha256(p)}" for p in present)
                dest = present[0]
            else:
                status, size, checksum = ds["download_policy"], None, None
        elif ds["download_policy"].startswith("skip"):
            partial = dest.with_suffix(dest.suffix + ".partial")
            if partial.exists():
                status, size, checksum = ds["download_policy"], partial.stat().st_size, None
                dest = partial
            else:
                status, size, checksum = ds["download_policy"], None, None
        else:
            status, size, checksum = fetch(ds["download_url"], dest)
        support_files = [str(EXT / name) for name in SUPPORTING_FILES.get(ds["accession"], []) if (EXT / name).exists()]
        rows.append({**ds, "local_file": str(dest) if dest.exists() else "", "supporting_files": ";".join(support_files), "download_status": status, "download_bytes": size, "sha256": checksum})
    pd.DataFrame(rows).to_csv(OUT / "external_dataset_audit.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()
