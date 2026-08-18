from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "data/metadata/EMTAB14509_sample_metadata.tsv"


def load_meta():
    assert META.exists(), "Run `make audit` before tests."
    return pd.read_csv(META, sep="\t")


def test_patient_not_cross_discovery_replication():
    meta = load_meta()
    assert (meta.groupby("patient_id")["cohort"].nunique() <= 1).all()


def test_no_post_treatment_samples_in_baseline_flag():
    meta = load_meta()
    baseline = meta[meta["baseline"].astype(str).isin(["True", "true", "1"])]
    assert baseline["timepoint"].eq(0).all()


def test_no_duplicated_sample_ids():
    meta = load_meta()
    assert not meta["sample_id"].duplicated().any()


def test_one_patient_one_tissue_at_baseline():
    meta = load_meta()
    baseline = meta[meta["timepoint"].eq(0)]
    counts = baseline.groupby(["patient_id", "tissue"]).size()
    assert (counts <= 1).all()


def test_replication_never_refits_clustering_policy_locked():
    text = (ROOT / "configs/phase1.yaml").read_text()
    assert "refit_clustering: false" in text

