from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def test_phase1b_core_outputs_exist_and_are_axis_based():
    phase1b = ROOT / "results" / "phase1b"
    required = [
        "factor_stability.tsv",
        "factor_biology.tsv",
        "factor_loadings.tsv",
        "molecular_axis_scores_discovery.tsv",
        "replication_ETAB14509.tsv",
        "cross_tissue_discovery_support.tsv",
        "axes_vs_clusters.tsv",
        "external_dataset_audit.tsv",
        "external_axis_support.tsv",
        "external_GSE244679_skin_axis_replication.tsv",
        "external_GSE147339_blood_axis_support.tsv",
        "external_GSE61281_blood_axis_support.tsv",
        "external_axis_replication_and_blood_support.tsv",
    ]
    for name in required:
        assert (phase1b / name).exists(), name

    stability = pd.read_csv(phase1b / "factor_stability.tsv", sep="\t")
    assert stability["stability_status"].isin(["robust", "intermediate"]).sum() >= 2

    scores = pd.read_csv(phase1b / "molecular_axis_scores_discovery.tsv", sep="\t")
    assert scores.shape[0] == 76
    assert {f"F{i}" for i in range(1, 9)} <= set(scores.columns)


def test_external_replication_inputs_are_analysis_ready():
    audit = pd.read_csv(ROOT / "results" / "phase1b" / "external_dataset_audit.tsv", sep="\t")
    gse244679 = audit.loc[audit["accession"].eq("GSE244679")].iloc[0]
    assert gse244679["download_status"] == "already_present_complete"
    assert str(gse244679["local_file"]).endswith("GSE244679_RAW.tar")

    gse61281 = audit.loc[audit["accession"].eq("GSE61281")].iloc[0]
    assert gse61281["download_status"] == "analysis_ready_series_matrix_and_platform_annotation"


def test_external_axis_replication_outputs_have_expected_scope():
    phase1b = ROOT / "results" / "phase1b"
    skin = pd.read_csv(phase1b / "external_GSE244679_skin_axis_replication.tsv", sep="\t")
    assert skin.shape[0] == 16
    assert set(skin["view"]) == {"LS", "NL"}
    assert skin["n_pairs"].min() == 24

    blood = pd.read_csv(phase1b / "external_GSE61281_blood_axis_support.tsv", sep="\t")
    assert blood.shape[0] == 24
    assert set(blood["contrast"]) == {
        "cutaneous_psoriasis_without_arthritis_minus_control",
        "psoriatic_arthritis_minus_control",
        "psoriasis_spectrum_minus_control",
    }


def test_phase2a_axis_prioritization_outputs_are_frozen():
    phase2a = ROOT / "results" / "phase2a"
    assert (phase2a / "axis_priority_matrix.tsv").exists()
    assert (phase2a / "axis_evidence_matrix.tsv").exists()
    assert (phase2a / "axis_mechanism_cards.tsv").exists()
    assert (phase2a / "factor_redundancy.tsv").exists()
    assert (phase2a / "single_cell_readiness.tsv").exists()
    assert (phase2a / "Table_axis_prioritization_master.tsv").exists()
    assert (ROOT / "reports" / "PHASE2A_AXIS_MECHANISM_PRIORITIZATION.md").exists()
    for factor in [f"F{i}" for i in range(1, 9)]:
        assert (ROOT / "reports" / "mechanism_cards" / f"{factor}.md").exists()

    master = pd.read_csv(phase2a / "Table_axis_prioritization_master.tsv", sep="\t")
    assert set(master.loc[master["final_role"].eq("PRIMARY AXIS"), "factor"]) == {"F1", "F2", "F6"}
    assert master.loc[master["factor"].eq("F7"), "final_role"].iloc[0] == "SUPPORTIVE/SYSTEMIC AXIS"
    assert master.loc[master["factor"].eq("F4"), "final_role"].iloc[0] == "UNINTERPRETABLE / RETIRE"

    cards = pd.read_csv(phase2a / "axis_mechanism_cards.tsv", sep="\t")
    assert set(cards["factor"]) == {f"F{i}" for i in range(1, 9)}

    for factor in ["F1", "F2", "F6", "F7"]:
        assert (phase2a / "axis_gene_programs" / f"{factor}_gene_program.tsv").exists()


def test_phase2b_gse228421_outputs_are_donor_level():
    phase2b = ROOT / "results" / "phase2b"
    assert (ROOT / "reports" / "PHASE2B_GSE228421_SINGLE_CELL_LOCALIZATION.md").exists()
    assert (phase2b / "GSE228421_sample_metadata.tsv").exists()
    assert (phase2b / "GSE228421_donor_celltype_axis_scores.tsv").exists()
    assert (phase2b / "GSE228421_baseline_LS_vs_NL_donor_statistics.tsv").exists()
    assert (phase2b / "GSE228421_treatment_timepoint_sensitivity.tsv").exists()
    assert (phase2b / "GSE228421_cell_type_localization.tsv").exists()
    assert (phase2b / "GSE228421_program_dropout_robustness.tsv").exists()
    assert (phase2b / "Table_phase2b_axis_cell_localization.tsv").exists()

    final = pd.read_csv(phase2b / "Table_phase2b_axis_cell_localization.tsv", sep="\t")
    assert set(final["axis"]) == {"F1", "F2", "F6", "F7"}
    assert set(final["confidence"]) <= {"LOW", "MODERATE", "HIGH"}
    assert final["confidence"].eq("LOW").all()

    paired = pd.read_csv(phase2b / "GSE228421_baseline_LS_vs_NL_donor_statistics.tsv", sep="\t")
    assert set(paired["program_type"]) == {"CORE", "EXTENDED"}
    assert paired["n_donors"].max() <= 5
    assert paired.loc[paired["n_donors"].ge(4), "n_donors"].min() >= 4

    donor_scores = pd.read_csv(phase2b / "GSE228421_donor_celltype_axis_scores.tsv", sep="\t")
    assert donor_scores["donor_id"].nunique() == 5
    assert {"baseline", "day3", "day14"} <= set(donor_scores["timepoint"])


def test_phase2br_2c_stop_rule_and_gse202011_spatial_audit_exist():
    phase2br = ROOT / "results" / "phase2br_2c"
    assert (ROOT / "reports" / "PHASE2BR_2C_STOP_RULE_ROADMAP.md").exists()
    assert (phase2br / "GSE202011_spatial_sample_audit.tsv").exists()
    assert (phase2br / "GSE202011_spatial_sample_summary.tsv").exists()

    summary = pd.read_csv(phase2br / "GSE202011_spatial_sample_summary.tsv", sep="\t")
    observed = {
        (row["disease_group"], row["tissue_state"]): row["n_samples"]
        for _, row in summary.iterrows()
    }
    assert observed[("Healthy", "healthy")] == 7
    assert observed[("PSO", "lesional")] == 7
    assert observed[("PSO", "nonlesional")] == 5
    assert observed[("PSA", "lesional")] == 7
    assert observed[("PSA", "nonlesional")] == 4


def test_phase2c_accession_audit_and_manifest_are_locked():
    phase2c = ROOT / "results" / "phase2c"
    assert (ROOT / "reports" / "PHASE2C_DATASET_ACCESSION_AUDIT.md").exists()
    assert (phase2c / "dataset_accession_audit.tsv").exists()
    assert (phase2c / "dataset_supplementary_files.tsv").exists()

    audit = pd.read_csv(phase2c / "dataset_accession_audit.tsv", sep="\t")
    assert set(audit["accession"]) == {"GSE228421", "GSE173706", "GSE225475", "GSE202011"}

    by_acc = audit.set_index("accession")
    assert by_acc.loc["GSE228421", "suitability"] == "SUITABLE_FOR_PHASE2B_R"
    assert by_acc.loc["GSE173706", "suitability"] == "SUITABLE_PENDING_DOWNLOAD_AND_ANNOTATION_STRATEGY"
    assert by_acc.loc["GSE225475", "suitability"] == "SUITABLE_PENDING_DOWNLOAD"
    assert by_acc.loc["GSE202011", "suitability"] == "SUITABLE_PENDING_COMPLETE_DOWNLOAD"

    gse173706 = pd.read_csv(phase2c / "GSE173706_sample_metadata_audit.tsv", sep="\t")
    assert gse173706["derived_tissue_state"].value_counts().to_dict() == {
        "lesional": 14,
        "nonlesional": 11,
        "healthy": 8,
    }

    gse202011 = pd.read_csv(phase2c / "GSE202011_sample_metadata_audit.tsv", sep="\t")
    assert gse202011["derived_tissue_state"].value_counts().to_dict() == {
        "lesional": 14,
        "nonlesional": 9,
        "healthy": 7,
    }

    manifest = pd.read_csv(ROOT / "DATA_MANIFEST.tsv", sep="\t")
    assert {"GSE228421", "GSE173706", "GSE225475", "GSE202011"} <= set(manifest["dataset_id"])


def test_phase2br_gse228421_refinement_outputs_are_bounded():
    phase2br = ROOT / "results" / "phase2br"
    assert (ROOT / "reports" / "PHASE2BR_GSE228421_REFINEMENT.md").exists()
    assert (phase2br / "GSE228421_cell_axis_scores.tsv").exists()
    assert (phase2br / "GSE228421_donor_refined_state_axis_scores.tsv").exists()
    assert (phase2br / "GSE228421_refined_axis_localization.tsv").exists()
    assert (phase2br / "GSE228421_refined_state_donor_statistics.tsv").exists()
    assert (phase2br / "GSE228421_refined_state_score_localization.tsv").exists()

    final = pd.read_csv(phase2br / "GSE228421_refined_axis_localization.tsv", sep="\t")
    assert set(final["axis"]) == {"F1", "F2", "F6", "F7"}
    assert final["confidence"].eq("LOW").all()
    assert final["parent_cell_type"].isin(["keratinocyte", "B_cell", "T_cell", "NK_cell", "dendritic", "myeloid_monocyte"]).all()
    assert final["dominant_refined_state"].str.contains("keratinocyte|B_cell|T_cell|NK|myeloid|dendritic").all()


def test_phase2c_gse173706_independent_scrna_outputs_are_donor_level():
    phase2c = ROOT / "results" / "phase2c"
    assert (ROOT / "reports" / "PHASE2C_GSE173706_INDEPENDENT_SCRNA_VALIDATION.md").exists()
    assert (phase2c / "GSE173706_download_manifest.tsv").exists()
    assert (phase2c / "GSE173706_cell_axis_scores.tsv.gz").exists()
    assert (phase2c / "GSE173706_donor_cellstate_axis_scores.tsv").exists()
    assert (phase2c / "GSE173706_LS_vs_NL_donor_statistics.tsv").exists()
    assert (phase2c / "GSE173706_lesional_vs_healthy_statistics.tsv").exists()
    assert (phase2c / "GSE173706_independent_scRNA_localization.tsv").exists()

    manifest = pd.read_csv(phase2c / "GSE173706_download_manifest.tsv", sep="\t")
    assert manifest.shape[0] == 33
    assert manifest["bytes"].min() > 0

    final = pd.read_csv(phase2c / "GSE173706_independent_scRNA_localization.tsv", sep="\t")
    assert set(final["axis"]) == {"F1", "F2", "F6", "F7"}
    assert final["independent_scrna_confidence"].eq("LOW").all()
    assert final["parent_cell_type"].isin(["keratinocyte", "B_cell", "T_cell", "NK_cell", "dendritic", "myeloid_monocyte"]).all()
    assert final["n_paired_donors"].min() >= 8


def test_phase2c_gse225475_primary_spatial_outputs_are_section_level():
    phase2c = ROOT / "results" / "phase2c"
    assert (ROOT / "reports" / "PHASE2C_GSE225475_PRIMARY_SPATIAL_LOCALIZATION.md").exists()
    assert (phase2c / "GSE225475_download_manifest.tsv").exists()
    assert (phase2c / "GSE225475_spot_axis_scores.tsv.gz").exists()
    assert (phase2c / "GSE225475_sample_axis_scores.tsv").exists()
    assert (phase2c / "GSE225475_spot_axis_marker_correlations.tsv").exists()
    assert (phase2c / "GSE225475_spatial_axis_localization.tsv").exists()

    manifest = pd.read_csv(phase2c / "GSE225475_download_manifest.tsv", sep="\t")
    assert manifest.shape[0] == 6
    assert manifest["bytes"].min() > 0

    loc = pd.read_csv(phase2c / "GSE225475_spatial_axis_localization.tsv", sep="\t")
    assert set(loc["axis"]) == {"F1", "F2", "F6", "F7"}
    assert loc["count"].min() == 6
    assert loc["median_spot_spearman"].notna().all()


def test_phase2c_gse202011_external_spatial_outputs_are_complete():
    phase2c = ROOT / "results" / "phase2c"
    assert (ROOT / "reports" / "PHASE2C_GSE202011_EXTERNAL_SPATIAL_ROBUSTNESS.md").exists()
    assert (phase2c / "GSE202011_download_manifest.tsv").exists()
    assert (phase2c / "GSE202011_spot_axis_scores.tsv.gz").exists()
    assert (phase2c / "GSE202011_sample_axis_scores.tsv").exists()
    assert (phase2c / "GSE202011_lesional_vs_nonlesional_axis_scores.tsv").exists()
    assert (phase2c / "GSE202011_spot_axis_marker_correlations.tsv").exists()
    assert (phase2c / "GSE202011_spatial_axis_localization.tsv").exists()

    manifest = pd.read_csv(phase2c / "GSE202011_download_manifest.tsv", sep="\t")
    assert manifest.shape[0] == 30
    assert manifest["bytes"].min() > 0

    loc = pd.read_csv(phase2c / "GSE202011_spatial_axis_localization.tsv", sep="\t")
    assert set(loc["axis"]) == {"F1", "F2", "F6", "F7"}
    assert loc["count"].min() == 30
    assert loc["median_spot_spearman"].notna().all()


def test_phase2c_mechanism_freeze_v2_is_shrunk_not_mechanism_named():
    phase2c = ROOT / "results" / "phase2c"
    assert (phase2c / "Table_mechanism_triangulation.tsv").exists()
    assert (ROOT / "MECHANISM_FREEZE_V2.md").exists()
    assert (ROOT / "reports" / "PHASE2BR_2C_FINAL_TRANSCRIPTOMICS_VALIDATION_REPORT.md").exists()
    assert (ROOT / "当前情况_Phase2BR_2C后_2026-08-11.md").exists()

    tri = pd.read_csv(phase2c / "Table_mechanism_triangulation.tsv", sep="\t")
    assert set(tri["axis"]) == {"F1", "F2", "F6", "F7"}
    assert tri.loc[tri["axis"].isin(["F1", "F2", "F6"]), "freeze_decision"].eq(
        "retain_as_bulk_axis_with_directional_keratinocyte_spatial_support"
    ).all()
    assert tri.loc[tri["axis"].eq("F7"), "freeze_decision"].iloc[0] == "retain_as_supportive_systemic_axis_only"
    assert "DIRECTIONAL_SUPPORT_ONLY" in set(tri["mechanism_confidence_v2"])

    freeze_text = (ROOT / "MECHANISM_FREEZE_V2.md").read_text()
    assert "SHRINK_TO_BULK_MOLECULAR_PROGRAMS_WITH_DIRECTIONAL_CELLULAR_SPATIAL_SUPPORT" in freeze_text
    assert "Do not enter Phase 3 under a claim of validated cell-state mechanisms" in freeze_text
