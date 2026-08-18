#!/usr/bin/env python3
"""Create Phase 3A figure drafts."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "phase3a"
FIG = ROOT / "results" / "figures" / "phase3a"
AXES = ["F1", "F2", "F6", "F7"]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def save(fig, name):
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / f"{name}.png", dpi=220, bbox_inches="tight")
    fig.savefig(FIG / f"{name}.svg", bbox_inches="tight")
    plt.close(fig)


def fig6a():
    steps = ["Frozen axes", "CORE gene programs", "GCST90472771", "MAGMA", "MHC excluded", "Matched null", "Evidence tier"]
    fig, ax = plt.subplots(figsize=(10, 2.2))
    ax.axis("off")
    xs = [i / (len(steps) - 1) for i in range(len(steps))]
    for i, (x, text) in enumerate(zip(xs, steps)):
        ax.text(x, 0.55, text, ha="center", va="center", fontsize=9, bbox=dict(boxstyle="round,pad=0.35", facecolor="#eef2f3", edgecolor="#5f6f73"))
        if i < len(steps) - 1:
            ax.annotate("", xy=(xs[i + 1] - 0.06, 0.55), xytext=(x + 0.06, 0.55), arrowprops=dict(arrowstyle="->", color="#4b5563", lw=1.4))
    ax.set_title("Figure 6A. Frozen-axis genetic anchoring design", fontsize=11, loc="left")
    save(fig, "Figure6A_genetic_anchoring_design")


def fig6b():
    rows = read_tsv(OUT / "magma_core_MHC_excluded.tsv")
    beta = [float(r["beta"]) for r in rows]
    se = [float(r["SE"]) for r in rows]
    fdr = [float(r["FDR"]) for r in rows]
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    colors = ["#3b6f8f" if q < 0.05 else "#9aa6ac" for q in fdr]
    ax.bar(AXES, beta, yerr=[1.96 * s for s in se], color=colors, edgecolor="#333333", linewidth=0.5)
    ax.axhline(0, color="#333333", lw=0.8)
    ax.set_ylabel("MAGMA beta (MHC excluded)")
    ax.set_title("Figure 6B. CORE axis enrichment", fontsize=11, loc="left")
    for i, q in enumerate(fdr):
        ax.text(i, beta[i] + (0.015 if beta[i] >= 0 else -0.025), f"FDR={q:.3g}", ha="center", va="bottom" if beta[i] >= 0 else "top", fontsize=8)
    save(fig, "Figure6B_axis_enrichment")


def fig6c():
    rows = read_tsv(OUT / "magma_core_MHC_excluded.tsv")
    pvals = [-__import__("math").log10(float(r["P"])) for r in rows]
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    ax.bar(AXES, pvals, color="#7c9b6f", edgecolor="#333333", linewidth=0.5)
    ax.axhline(-__import__("math").log10(0.05), color="#a33", lw=0.8, ls="--")
    ax.set_ylabel("-log10(P), MHC excluded")
    ax.set_title("Figure 6C. MHC-excluded primary P values", fontsize=11, loc="left")
    ax.text(0.02, 0.95, "MHC-included sensitivity not estimable\nfull chr6 MHC gene-level run stalled", transform=ax.transAxes, fontsize=8, va="top")
    save(fig, "Figure6C_MHC_sensitivity")


def fig6d():
    obs = {r["axis"]: float(r["observed_statistic"]) for r in read_tsv(OUT / "matched_null_results.tsv")}
    null_rows = []
    for line in (OUT / "magma_matched_null_core_MHC_excluded.gsa.out").read_text().splitlines():
        if not line or line.startswith("#") or line.startswith("VARIABLE"):
            continue
        p = line.split()
        if len(p) >= 7:
            null_rows.append((p[0].split("_")[0], float(p[3])))
    fig, axes = plt.subplots(2, 2, figsize=(7, 5), sharex=False)
    for ax, axis in zip(axes.ravel(), AXES):
        vals = [v for a, v in null_rows if a == axis]
        ax.hist(vals, bins=35, color="#d7dde0", edgecolor="#6b7280", linewidth=0.3)
        ax.axvline(obs[axis], color="#b42318", lw=1.4)
        ax.set_title(axis, fontsize=10)
    fig.suptitle("Figure 6D. Matched-null enrichment distributions", fontsize=11, x=0.02, ha="left")
    save(fig, "Figure6D_matched_null_distributions")


def fig6e_f():
    tab = read_tsv(OUT / "Table_axis_genetic_anchoring.tsv")
    fig, ax = plt.subplots(figsize=(8, 2.6))
    ax.axis("off")
    cols = ["MAGMA_FDR", "empirical_null_P", "unique_gene_signal", "conditional_signal"]
    data = [[r[c] for c in cols] for r in tab]
    table = ax.table(cellText=data, rowLabels=[r["axis"] for r in tab], colLabels=cols, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.35)
    ax.set_title("Figure 6E. Orthogonal genetic evidence matrix", fontsize=11, loc="left")
    save(fig, "Figure6E_evidence_matrix")

    rows = read_tsv(OUT / "shared_vs_unique_genetic_signal.tsv")
    fig, ax = plt.subplots(figsize=(7, 3.2))
    names = [r["component"].replace("_MHC_EXCLUDED", "").replace("_COMPONENT", "") for r in rows]
    beta = [float(r["beta"]) for r in rows]
    ax.bar(names, beta, color="#c7b37f", edgecolor="#333333", linewidth=0.5)
    ax.axhline(0, color="#333333", lw=0.8)
    ax.tick_params(axis="x", rotation=35)
    ax.set_ylabel("MAGMA beta")
    ax.set_title("Figure 6F. Shared versus axis-specific signal", fontsize=11, loc="left")
    save(fig, "Figure6F_shared_vs_axis_specific")


if __name__ == "__main__":
    fig6a()
    fig6b()
    fig6c()
    fig6d()
    fig6e_f()
