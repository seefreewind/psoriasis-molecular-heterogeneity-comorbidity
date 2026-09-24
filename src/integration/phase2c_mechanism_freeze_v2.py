#!/usr/bin/env python3
"""Create Phase 2B-R/2C mechanism triangulation and freeze v2 decision."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
P2C = ROOT / "results" / "phase2c"
P2BR = ROOT / "results" / "phase2br"
REPORTS = ROOT / "reports"


AXES = ["F1", "F2", "F6", "F7"]


def confidence_from(row: pd.Series) -> str:
    if row["axis"] == "F7":
        return "LOW"
    if row["single_cell_convergence"].startswith("yes") and row["spatial_convergence"].startswith("yes"):
        return "DIRECTIONAL_SUPPORT_ONLY"
    return "LOW"


def main() -> None:
    p2br = pd.read_csv(P2BR / "GSE228421_refined_axis_localization.tsv", sep="\t").set_index("axis")
    gse173706 = pd.read_csv(P2C / "GSE173706_independent_scRNA_localization.tsv", sep="\t").set_index("axis")
    gse225475 = pd.read_csv(P2C / "GSE225475_spatial_axis_localization.tsv", sep="\t").set_index("axis")
    gse202011 = pd.read_csv(P2C / "GSE202011_spatial_axis_localization.tsv", sep="\t").set_index("axis")

    rows = []
    for axis in AXES:
        sc1 = str(p2br.loc[axis, "dominant_refined_state"])
        sc2 = str(gse173706.loc[axis, "dominant_refined_state_paired"])
        sp1 = str(gse225475.loc[axis, "dominant_spatial_program"])
        sp2 = str(gse202011.loc[axis, "dominant_spatial_program"])
        single_cell_convergence = "yes_directional" if ("keratinocyte" in sc1 and "keratinocyte" in sc2) or (axis == "F7" and "B_cell" in sc1 and "B_cell" in sc2) else "no"
        spatial_convergence = "yes_spatial_program" if sp1 == sp2 else "partial"
        if axis in {"F1", "F2", "F6"}:
            final_name = "keratinocyte stress/inflammatory spatial program"
            freeze_decision = "retain_as_bulk_axis_with_directional_keratinocyte_spatial_support"
        else:
            final_name = "systemic/supportive immune axis; not skin-spatial-localized"
            freeze_decision = "retain_as_supportive_systemic_axis_only"
        rows.append(
            {
                "axis": axis,
                "phase2br_gse228421_state": sc1,
                "phase2br_confidence": p2br.loc[axis, "confidence"],
                "gse173706_independent_scrna_state": sc2,
                "gse173706_confidence": gse173706.loc[axis, "independent_scrna_confidence"],
                "gse225475_primary_spatial_program": sp1,
                "gse225475_median_spot_spearman": gse225475.loc[axis, "median_spot_spearman"],
                "gse202011_external_spatial_program": sp2,
                "gse202011_median_spot_spearman": gse202011.loc[axis, "median_spot_spearman"],
                "single_cell_convergence": single_cell_convergence,
                "spatial_convergence": spatial_convergence,
                "final_name_v2": final_name,
                "mechanism_confidence_v2": "pending",
                "freeze_decision": freeze_decision,
            }
        )
    tri = pd.DataFrame(rows)
    tri["mechanism_confidence_v2"] = tri.apply(confidence_from, axis=1)
    tri.to_csv(P2C / "Table_mechanism_triangulation.tsv", sep="\t", index=False)

    status = "SHRINK_TO_BULK_MOLECULAR_PROGRAMS_WITH_DIRECTIONAL_CELLULAR_SPATIAL_SUPPORT"
    freeze = [
        "# MECHANISM FREEZE V2",
        "",
        f"Final Phase 2B-R/2C status: **{status}**.",
        "",
        "Phase 2B-R and Phase 2C completed the final transcriptomics rescue attempt. No additional bulk RNA-seq, scRNA-seq, or spatial transcriptomics datasets should be introduced solely to rescue weak mechanism naming.",
        "",
        "## Frozen Interpretation",
        "",
        "- F1, F2, and F6 remain frozen skin-primary bulk molecular axes with directional keratinocyte/spatial support.",
        "- Across GSE228421 refinement and GSE173706 independent scRNA, F1/F2/F6 repeatedly point toward keratinocyte stress/inflammatory states, but donor-level FDR criteria remain unmet.",
        "- Across GSE225475 and GSE202011, F1/F2/F6 consistently co-localize most strongly with keratinocyte stress/hypoxia spatial programs.",
        "- F7 remains a systemic/supportive axis. Current skin scRNA/spatial evidence does not justify naming it as a skin-localized immune spatial mechanism.",
        "",
        "## Genetics Entry Decision",
        "",
        "Do not enter Phase 3 under a claim of validated cell-state mechanisms. Phase 3 may proceed only as axis-gene-program genetics for frozen bulk molecular programs, with cellular/spatial findings described as directional support. GWAS, MR, LDSC, LAVA, and colocalization must not be used to rename axes or revise gene membership.",
        "",
        "## Triangulation Table",
        "",
        tri.to_markdown(index=False),
    ]
    (ROOT / "MECHANISM_FREEZE_V2.md").write_text("\n".join(freeze) + "\n")

    report = [
        "# PHASE 2B-R + PHASE 2C Final Transcriptomics Validation Report",
        "",
        "## Executive Conclusion",
        "",
        f"**{status}.** The final transcriptomics validation block strengthens the directional keratinocyte/spatial interpretation for F1/F2/F6 but does not meet the locked threshold for formal mechanism naming. F7 remains systemic/supportive rather than skin-spatial localized.",
        "",
        "## What Was Completed",
        "",
        "- Accession audit and DATA_MANIFEST correction for GSE228421, GSE173706, GSE225475, and GSE202011.",
        "- Phase 2B-R one-pass GSE228421 marker/reference refinement.",
        "- Phase 2C independent scRNA validation using GSE173706.",
        "- Phase 2C primary spatial localization using GSE225475.",
        "- Phase 2C external spatial robustness using GSE202011 sample-level H5 files.",
        "- Mechanism triangulation and mechanism freeze v2.",
        "",
        "## Answers To The Locked Questions",
        "",
        "1. F1 is not formally validated as a named mechanism; it has directional keratinocyte inflammatory/stress support.",
        "2. F2 is not formally validated as fibroblast/stromal; it trends toward keratinocyte stress/hypoxia rather than a clean stromal-repair axis.",
        "3. F6 has the most coherent keratinocyte stress/hypoxia spatial support but remains below donor-level single-cell confidence thresholds.",
        "4. F7 is not confirmed as a skin-localized myeloid/IFN axis; retain it as systemic/supportive only.",
        "5. CORE remains primary; EXTENDED is sensitivity only.",
        "6. Donor/section-level inference was preserved; cells/spots were not treated as independent patients.",
        "7. GSE173706 supports directional independent scRNA validation but not formal MODERATE/HIGH mechanism confidence.",
        "8. GSE225475 supports keratinocyte stress/hypoxia spatial localization for F1/F2/F6.",
        "9. GSE202011 independently supports the same keratinocyte stress/hypoxia spatial program.",
        "10. GSE202011 was not used as a single-cell atlas.",
        "11. No GWAS, MR, LDSC, LAVA, colocalization, drug prediction, PPI, hub-gene, or LASSO analyses were run.",
        "12. No frozen gene programs were modified.",
        "13. No additional transcriptomics rescue datasets should be added after this block.",
        "14. Mechanism confidence v2 remains below formal naming threshold for all axes.",
        "15. F1/F2/F6 can be carried forward as frozen bulk molecular axes with directional cellular/spatial support.",
        "16. F7 can be carried forward only as a supportive/systemic candidate.",
        "17. Phase 3 can start only if claim language is shrunk to gene-program genetics rather than validated cell-state mechanisms.",
        "",
        "## Triangulation",
        "",
        tri.to_markdown(index=False),
        "",
        "## Final Status",
        "",
        status,
    ]
    (REPORTS / "PHASE2BR_2C_FINAL_TRANSCRIPTOMICS_VALIDATION_REPORT.md").write_text("\n".join(report) + "\n")

    current = [
        "# 当前情况：Phase 2B-R + Phase 2C 后",
        "",
        f"状态：**{status}**。",
        "",
        "项目已经完成最终 transcriptomics validation block。结论不是机制命名升级，而是 claim 收缩：F1/F2/F6 保留为 skin-primary bulk molecular axes，并有一致的 keratinocyte stress/inflammatory spatial support；F7 保留为 systemic/supportive axis。",
        "",
        "下一步可以进入 Phase 3 genetics，但只能按 frozen bulk axis gene programs 做 gene-set/genetic anchoring，不能宣称这些轴已经是 validated cell-state mechanisms。",
        "",
        "关键文件：",
        "",
        "- `reports/PHASE2BR_2C_FINAL_TRANSCRIPTOMICS_VALIDATION_REPORT.md`",
        "- `MECHANISM_FREEZE_V2.md`",
        "- `results/phase2c/Table_mechanism_triangulation.tsv`",
    ]
    (ROOT / "当前情况_Phase2BR_2C后_2026-08-11.md").write_text("\n".join(current) + "\n")
    print(status)
    print(tri.to_string(index=False))


if __name__ == "__main__":
    main()
