#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
QC = ROOT / "results/qc"
TABLES = ROOT / "results/tables"
PHASE = ROOT / "results/phase1"
FIG = ROOT / "results/figures"


def save(fig, name: str) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    for ext in ["png", "svg", "pdf"]:
        fig.savefig(FIG / f"{name}.{ext}", dpi=300)
    plt.close(fig)


def fig_sample_flow() -> None:
    flow = pd.read_csv(QC / "sample_flow.tsv", sep="\t")
    base = flow[flow["timepoint"].eq(0)].copy()
    labels = base["cohort"] + "\n" + base["tissue"]
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.bar(range(len(base)), base["n_patients"], color="#4C78A8")
    ax.set_xticks(range(len(base)), labels, rotation=35, ha="right")
    ax.set_ylabel("Patients")
    ax.set_title("Baseline sample flow")
    save(fig, "Figure1A_study_flow")


def fig_tissue_matrix() -> None:
    mat = pd.read_csv(QC / "patient_tissue_matrix.tsv", sep="\t")
    summary = mat.groupby("cohort")[["Lesional Skin", "Nonlesional Skin", "Whole Blood"]].sum()
    fig, ax = plt.subplots(figsize=(5, 3.5))
    im = ax.imshow(summary.values, cmap="Blues", aspect="auto")
    ax.set_xticks(range(summary.shape[1]), summary.columns, rotation=30, ha="right")
    ax.set_yticks(range(summary.shape[0]), summary.index)
    for i in range(summary.shape[0]):
        for j in range(summary.shape[1]):
            ax.text(j, i, int(summary.iloc[i, j]), ha="center", va="center", color="black")
    ax.set_title("Baseline tissue availability")
    fig.colorbar(im, ax=ax, label="Patients")
    save(fig, "Figure1B_patient_tissue_structure")


def fig_stability() -> None:
    st = pd.read_csv(TABLES / "Table_S4_cluster_stability.tsv", sep="\t")
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.plot(st["k"], st["min_bootstrap_jaccard"], marker="o", color="#F58518")
    ax.axhline(0.75, color="black", linestyle="--", linewidth=1)
    ax.set_xlabel("k")
    ax.set_ylabel("Minimum cluster Jaccard")
    ax.set_title("Cluster stability")
    ax.set_ylim(0, 1)
    save(fig, "Figure2B_cluster_stability")


def fig_replication() -> None:
    rep = pd.read_csv(TABLES / "Table_S7_replication_metrics.tsv", sep="\t")
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    ax.bar(rep["endotype"], rep["spearman_signature_concordance"], color="#54A24B")
    ax.set_ylim(0, 1)
    ax.set_ylabel("Spearman concordance")
    ax.set_title("Frozen replication signature concordance")
    save(fig, "Figure3B_discovery_replication_concordance")


def fig_heatmap() -> None:
    sig = pd.read_csv(TABLES / "Table_S5_endotype_signatures.tsv", sep="\t")
    top = sig.groupby("endotype").head(12)
    mat = top.pivot_table(index="feature", columns="endotype", values="discovery_effect", aggfunc="first").fillna(0)
    fig_h = max(4, 0.18 * len(mat))
    fig, ax = plt.subplots(figsize=(5, fig_h))
    vmax = np.nanmax(np.abs(mat.values))
    im = ax.imshow(mat.values, cmap="vlag" if "vlag" in plt.colormaps() else "coolwarm", vmin=-vmax, vmax=vmax, aspect="auto")
    ax.set_xticks(range(mat.shape[1]), mat.columns)
    ax.set_yticks(range(mat.shape[0]), [x.replace("Hallmark::HALLMARK_", "H_").replace("pathway::", "P_").replace("regulon::", "R_").replace("cell_state::", "C_") for x in mat.index], fontsize=7)
    ax.set_title("Top discovery feature effects")
    fig.colorbar(im, ax=ax, label="Effect")
    save(fig, "Figure2C_endotype_biological_heatmap")


def fig_sensitivity() -> None:
    sens = pd.read_csv(TABLES / "Table_S8_sensitivity_analyses.tsv", sep="\t")
    sens = sens[sens["status"].eq("run")]
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    ax.bar(sens["sensitivity"], sens["ari_vs_primary"], color="#B279A2")
    ax.set_xticks(range(len(sens)), sens["sensitivity"], rotation=25, ha="right")
    ax.set_ylim(0, 1)
    ax.set_ylabel("ARI vs primary")
    ax.set_title("Sensitivity agreement")
    save(fig, "Figure3C_sensitivity_analysis")


def main() -> None:
    fig_sample_flow()
    fig_tissue_matrix()
    fig_stability()
    fig_replication()
    fig_heatmap()
    fig_sensitivity()


if __name__ == "__main__":
    main()

