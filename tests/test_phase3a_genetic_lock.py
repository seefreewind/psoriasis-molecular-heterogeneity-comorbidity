from pathlib import Path
import csv


ROOT = Path(__file__).resolve().parents[1]


EXPECTED_HASHES = {
    "F1": "c29e0bb8b8010fe99020352c693ec58b232943304ea7dc517a64b07f8ddd1034",
    "F2": "143103f5bc31d1d50f4ba9ab4d7500a4a9671335bc196a49770f59830f62da86",
    "F6": "3678368e2049e62a610dc820f8d0ac01b2f4244609c3ba4e4606edf28d590a21",
    "F7": "82493fc49127b44ce54933cc88be91231efea522bb9c0e5efd60c7a8685a66b9",
}


EXPECTED_COUNTS = {
    ("F1", "CORE"): 304,
    ("F1", "EXTENDED"): 809,
    ("F2", "CORE"): 725,
    ("F2", "EXTENDED"): 1184,
    ("F6", "CORE"): 134,
    ("F6", "EXTENDED"): 544,
    ("F7", "CORE"): 232,
    ("F7", "EXTENDED"): 507,
}


def read_tsv(path):
    with (ROOT / path).open(newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def test_frozen_gene_hashes_and_counts_unchanged():
    rows = read_tsv("results/phase3a/axis_gene_mapping_coverage.tsv")
    for row in rows:
        key = (row["axis"], row["program_type"])
        assert int(row["frozen_gene_count"]) == EXPECTED_COUNTS[key]
        assert row["gene_program_sha256"] == EXPECTED_HASHES[row["axis"]]


def test_core_and_extended_not_swapped():
    rows = read_tsv("results/phase3a/axis_gene_mapping_coverage.tsv")
    by_axis = {}
    for row in rows:
        by_axis.setdefault(row["axis"], {})[row["program_type"]] = int(row["frozen_gene_count"])
    for axis, counts in by_axis.items():
        assert counts["CORE"] < counts["EXTENDED"]


def test_mhc_exclusion_applied_to_primary_mapping():
    rows = read_tsv("results/phase3a/axis_gene_annotation_mapping.tsv")
    for row in rows:
        if row["program_type"] == "CORE" and row["MHC_status"] == "MHC":
            assert row["included_primary"] == "False"
            assert row["exclusion_reason"] == "MHC_excluded_primary"


def test_no_duplicate_gene_ids_within_axis_program_mapping():
    rows = read_tsv("results/phase3a/axis_gene_annotation_mapping.tsv")
    seen = set()
    for row in rows:
        if row["annotation_status"] != "mapped":
            continue
        key = (row["axis"], row["program_type"], row["gene_id"])
        assert key not in seen
        seen.add(key)


def test_candidate_genes_are_core_primary_mapped():
    mapping = read_tsv("results/phase3a/axis_gene_annotation_mapping.tsv")
    core = {(r["axis"], r["gene_symbol"]) for r in mapping if r["program_type"] == "CORE" and r["included_primary"] == "True"}
    for row in read_tsv("results/phase3a/phase3b_candidate_genes.tsv"):
        assert row["CORE_status"] == "CORE"
        assert (row["axis"], row["gene"]) in core


def test_no_comorbidity_gwas_outputs_created_in_phase3a():
    phase3a_files = [p.name.lower() for p in (ROOT / "results" / "phase3a").iterdir()]
    forbidden = ["crohn", "ulcerative", "cad", "stroke", "t2d", "masld", "depression", "uveitis", "ckd", "psa_gwas"]
    assert not any(any(term in name for term in forbidden) for name in phase3a_files)

