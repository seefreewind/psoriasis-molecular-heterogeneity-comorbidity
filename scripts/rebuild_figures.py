#!/usr/bin/env python3
"""Regenerate JDS Figures 1-5 from the aggregate tables in this release."""
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source_data"
FIGURES = ROOT / "figures"
INK, MUTED, GRID = "#24313A", "#58646F", "#D7DDE2"
COLORS = {"F1": "#D95F59", "F2": "#2A8C82", "F6": "#D29A24", "F7": "#596A9E"}


def rows(name: str) -> list[dict[str, str]]:
    with (SOURCE / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def save(fig: plt.Figure, stem: str) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / f"{stem}.tiff", dpi=600, bbox_inches="tight",
                pil_kwargs={"compression": "tiff_lzw"})
    fig.savefig(FIGURES / f"{stem}.svg", bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, title, detail, edge, face):
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.012",
                                transform=ax.transAxes, facecolor=face, edgecolor=edge, linewidth=1.2))
    ax.text(x+w/2, y+h*.65, title, transform=ax.transAxes, ha="center", va="center",
            fontsize=8.2, weight="bold", color=INK)
    ax.text(x+w/2, y+h*.30, detail, transform=ax.transAxes, ha="center", va="center",
            fontsize=6.6, color=MUTED)


def panel(ax, label: str, title: str) -> None:
    ax.text(-.08, 1.04, label, transform=ax.transAxes, weight="bold", fontsize=12)
    ax.set_title(title, loc="left", weight="bold", pad=10, color=INK)


def figure1() -> None:
    flow = {r["branch"]: int(r["n"]) for r in rows("Figure1_cohort_flow.tsv")}
    stable = {r["metric"]: float(r["estimate"]) for r in rows("Figure1_categorical_stability.tsv")}
    plt.rcParams.update({"font.family": "Arial", "font.size": 8})
    fig = plt.figure(figsize=(11.8, 5.2), facecolor="white")
    gs = fig.add_gridspec(1, 3, width_ratios=[1.32, .88, 1.25], wspace=.34)
    a = fig.add_subplot(gs[0, 0]); a.axis("off"); panel(a, "a", "Cohort structure")
    box(a,.02,.80,.96,.14,"E-MTAB-14509",f"{flow['total']} total; baseline metadata for {flow['baseline']}","#55616E","#F7F9FA")
    box(a,.02,.55,.46,.16,"Discovery",f"{flow['discovery_total']} total; {flow['discovery_baseline']} with baseline",COLORS["F1"],"#FFF8F7")
    box(a,.52,.55,.46,.16,"Internal paired-skin set",f"{flow['internal_paired_skin']} participants",COLORS["F2"],"#F4FAF9")
    box(a,.02,.30,.46,.15,"Paired-skin discovery",f"{flow['paired_skin_discovery']} participants",COLORS["F1"],"#FFF8F7")
    box(a,.02,.06,.46,.15,"Complete three-view set",f"{flow['complete_three_view']} participants: skin and blood",COLORS["F7"],"#F6F7FB")
    for x,y0,y1 in [(.25,.80,.72),(.75,.80,.72),(.25,.55,.45),(.25,.30,.21)]:
        a.annotate("",xy=(x,y1),xytext=(x,y0),xycoords="axes fraction",arrowprops={"arrowstyle":"->","color":"#89939C"})
    a.text(.52,.37,"Participant IDs do not overlap",transform=a.transAxes,fontsize=6.7,color=MUTED,va="center")
    b=fig.add_subplot(gs[0,1]); panel(b,"b","Categorical stability")
    value=stable["minimum_bootstrap_jaccard"]; threshold=.75
    b.set_xlim(0,1); b.set_ylim(-.5,.5); b.set_yticks([]); b.axvline(threshold,color="#596A9E",ls="--",lw=1.2)
    b.hlines(0,0,1,color=GRID,lw=2); b.scatter([value],[0],s=70,color=COLORS["F1"],zorder=3)
    b.text(value,.15,f"{value:.3f}",ha="center",weight="bold",color=INK)
    b.text(threshold,-.2,f"criterion {threshold:.2f}",ha="center",fontsize=7,color="#596A9E")
    b.set_xlabel("Minimum bootstrap Jaccard"); b.set_xticks([0,.25,.5,.75,1]); b.grid(axis="x",color=GRID,lw=.5)
    for side in ("top","right","left"): b.spines[side].set_visible(False)
    c=fig.add_subplot(gs[0,2]); c.axis("off"); panel(c,"c","Continuous representation")
    box(c,.02,.72,.96,.17,"Three-view model","Lesional skin · non-lesional skin · whole blood","#55616E","#F7F9FA")
    box(c,.02,.45,.96,.17,"Eight factors","Stable alignment across five seeds",COLORS["F2"],"#F4FAF9")
    box(c,.02,.12,.96,.22,"Prioritized for interpretation","F1 · F2 · F6: skin-primary\nF7: blood-associated supportive program",COLORS["F7"],"#F6F7FB")
    c.annotate("",xy=(.5,.63),xytext=(.5,.72),xycoords="axes fraction",arrowprops={"arrowstyle":"->","color":"#89939C"})
    c.annotate("",xy=(.5,.34),xytext=(.5,.45),xycoords="axes fraction",arrowprops={"arrowstyle":"->","color":"#89939C"})
    save(fig,"Figure1_design_stability")


def figure2() -> None:
    data=rows("Figure2_external_support.tsv"); factors=[r["program"] for r in data]
    matrix=np.array([[float(r[k]) for k in ("variance_R2_lesional_skin","variance_R2_nonlesional_skin","variance_R2_blood")] for r in data])
    paired=np.array([[float(r["GSE244679_LS_abs_rho"]),float(r["GSE244679_NL_abs_rho"])] for r in data])
    blood=np.array([float(r["GSE61281_abs_rho"]) for r in data])
    fig,axs=plt.subplots(1,3,figsize=(12,4.55),gridspec_kw={"width_ratios":[1.03,1.2,.9]},facecolor="white")
    ax=axs[0]; panel(ax,"a","Variance contribution (R², %)")
    ax.imshow(matrix,cmap="YlGnBu",vmin=0,vmax=38,aspect="auto")
    ax.set_xticks(range(3),["Lesional\nskin","Non-lesional\nskin","Blood"]); ax.set_yticks(range(4),factors)
    for i in range(4):
        for j in range(3): ax.text(j,i,f"{matrix[i,j]:.1f}",ha="center",va="center",fontsize=7,color="white" if matrix[i,j]>20 else INK)
    ax=axs[1]; panel(ax,"b","External paired-skin concordance"); y=np.arange(4); ax.axvline(0,color="#AEB7BF",lw=.7)
    for j,(label,color,off) in enumerate([("Lesional",COLORS["F1"],-.1),("Non-lesional",COLORS["F2"],.1)]):
        ax.scatter(paired[:,j],y+off,color=color,s=38,label=label,zorder=3)
        for yy,xx in zip(y+off,paired[:,j]): ax.text(xx+.016,yy,f"{xx:.3f}",fontsize=6.5,va="center",color=INK)
    ax.set_yticks(y,factors); ax.invert_yaxis(); ax.set_xlim(-.02,.83); ax.set_xlabel("Absolute Spearman ρ"); ax.legend(frameon=False,fontsize=7,loc="lower right")
    ax=axs[2]; panel(ax,"c","Whole-blood support")
    bars=ax.barh(y,blood,color=[COLORS[f] for f in factors],height=.56); ax.set_yticks(y,factors); ax.invert_yaxis(); ax.set_xlim(0,.62); ax.set_xlabel("Absolute Spearman ρ")
    for bar,val in zip(bars,blood): ax.text(val+.012,bar.get_y()+bar.get_height()/2,f"{val:.3f}",va="center",fontsize=7)
    for ax in axs:
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=7); ax.grid(axis="x",color=GRID,lw=.45,zorder=0)
    fig.tight_layout(w_pad=2.2); save(fig,"Figure2_program_support")


def figure3() -> None:
    donors=rows("Figure3_single_cell_donor_points.tsv"); summaries=rows("Figure3_single_cell_summary.tsv")
    spatial=rows("Figure3_spatial_summary.tsv"); names=[r["program"] for r in summaries]
    fig,axs=plt.subplots(1,2,figsize=(11,4.7),gridspec_kw={"width_ratios":[1.16,1]},facecolor="white")
    ax=axs[0]; panel(ax,"a","Five-donor single-cell contextualization")
    rng=np.random.default_rng(24)
    for i,s in enumerate(summaries):
        f=s["program"]; vals=[float(r["donor_level_LS_minus_NL_CORE_mean"]) for r in donors if r["program"]==f]
        m,lo,hi=(float(s[k]) for k in ("mean_LS_minus_NL","bootstrap_95CI_lower","bootstrap_95CI_upper"))
        ax.scatter(vals,np.full(len(vals),i)+rng.uniform(-.1,.1,len(vals)),s=32,color=COLORS[f],alpha=.85,edgecolors="white",linewidth=.5,zorder=3)
        ax.errorbar(m,i,xerr=[[m-lo],[hi-m]],fmt="D",color=INK,ecolor=INK,capsize=3,markersize=4,lw=1.3,zorder=4)
        ax.text(max(hi,max(vals))+.009,i,f"n = {s['n_donors']}",va="center",fontsize=7,color=MUTED)
    ax.axvline(0,color="#AEB7BF",lw=.8)
    ax.set_yticks(range(4),[f"{r['program']} · {r['cell_type'].replace('_',' ')}" for r in summaries]); ax.invert_yaxis()
    ax.set_xlabel("Donor-level lesional − non-lesional contrast"); ax.set_xlim(-.07,.43)
    ax.scatter([],[],marker="o",s=28,color="#89939C",label="Individual donor")
    ax.errorbar([],[],xerr=[[.02],[.02]],fmt="D",color=INK,ecolor=INK,capsize=3,markersize=4,label="Mean and 95% bootstrap interval")
    ax.legend(frameon=False,fontsize=6.5,loc="lower right")
    ax=axs[1]; panel(ax,"b","Spatial marker-program context")
    for i,r in enumerate(spatial):
        vals=[float(r["GSE225475_rho"]),float(r["GSE202011_rho"])]
        ax.plot(vals,[i-.09,i+.09],color="#B7C0C7",lw=1)
        ax.scatter(vals[0],i-.09,color=COLORS[r["program"]],s=32,label="GSE225475" if i==0 else None,zorder=3)
        ax.scatter(vals[1],i+.09,color=COLORS[r["program"]],marker="s",s=32,label="GSE202011" if i==0 else None,zorder=3)
        ax.text(max(vals)+.016,i,f"{vals[0]:.3f} / {vals[1]:.3f}",fontsize=6.5,va="center")
    ax.set_yticks(range(4),names); ax.invert_yaxis(); ax.set_xlim(0,.82); ax.set_xlabel("Median within-sample spot-level Spearman ρ")
    ax.text(.02,-.18,"F1, F2 and F6 converge on a keratinocyte stress/hypoxia context.",transform=ax.transAxes,fontsize=6.4,color=MUTED)
    ax.legend(frameon=False,fontsize=6.5,loc="lower right")
    for ax in axs:
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.grid(axis="x",color=GRID,lw=.45,zorder=0); ax.tick_params(labelsize=7)
    fig.tight_layout(w_pad=2.2); save(fig,"Figure3_cell_spatial_context")


def figure4() -> None:
    data=rows("Figure4_genetic_summary.tsv")
    magma=[r for r in data if r["analysis"]=="MAGMA"]
    global_rg={r["outcome_or_program"]:r for r in data if r["analysis"]=="LDSC"}
    lava=[r for r in data if r["analysis"]=="LAVA"]
    fig,axs=plt.subplots(1,3,figsize=(13,5.2),gridspec_kw={"width_ratios":[1,1.25,1.08]},facecolor="white")
    ax=axs[0]; panel(ax,"a","Program-specific tests")
    for i,r in enumerate(magma):
        b,se=float(r["estimate_or_positive_count"]),float(r["SE_or_negative_count"])
        ax.errorbar(b,i,xerr=1.96*se,fmt="o",color=COLORS[r["outcome_or_program"]],capsize=2.5,markersize=5,lw=1.2)
        ax.text(.235,i,r["FDR_or_threshold"],va="center",ha="right",fontsize=7)
    ax.axvline(0,color="#68737D",lw=.8); ax.set_yticks(range(len(magma)),[r["outcome_or_program"] for r in magma]); ax.invert_yaxis(); ax.set_xlim(-.27,.26); ax.set_xlabel("MAGMA β (95% CI)"); ax.text(.99,1.02,"FDR",transform=ax.transAxes,ha="right",fontsize=7,color=MUTED)
    ax=axs[1]; panel(ax,"b","Overall psoriasis susceptibility")
    order=["CAD","Ischaemic stroke","CKD","Crohn disease","Ulcerative colitis","Psoriatic arthritis"]
    shades={"CAD":"#2A8C82","Psoriatic arthritis":"#596A9E","Crohn disease":"#C55A54","Ulcerative colitis":"#C55A54"}
    for i,name in enumerate(order):
        r=global_rg[name]; v,se=float(r["estimate_or_positive_count"]),float(r["SE_or_negative_count"])
        ax.errorbar(v,i,xerr=1.96*se,fmt="o",color=shades.get(name,"#55616E"),capsize=2.5,markersize=5,lw=1.2)
    ax.axvline(0,color="#68737D",lw=.8); ax.set_yticks(range(len(order)),order); ax.invert_yaxis(); ax.set_xlim(-.5,1.5); ax.set_xlabel("Genome-wide genetic correlation (r_g)")
    ax.text(.02,-.20,"PsA is a near-neighbor positive control; IBD estimates carry QC flags.",transform=ax.transAxes,fontsize=6.6,color=MUTED)
    ax=axs[2]; panel(ax,"c","Local sharing (LAVA)")
    names=["CAD","PsA","Crohn disease","UC"]
    matched={"PsA":"PsA","Crohn disease":"Crohn disease","UC":"UC"}
    lava_map={r["outcome_or_program"]:r for r in lava}
    pos=[]; neg=[]
    for name in names:
        row=lava_map[matched.get(name,name)]; pos.append(int(float(row["estimate_or_positive_count"]))); neg.append(int(float(row["SE_or_negative_count"])))
    y=np.arange(len(names)); ax.barh(y,[-v for v in neg],color="#C55A54",height=.58,label="Negative local r_g"); ax.barh(y,pos,color="#2A8C82",height=.58,label="Positive local r_g")
    ax.axvline(0,color="#68737D",lw=.8); ax.set_yticks(y,names); ax.invert_yaxis(); ax.set_xlim(-46,36); ax.set_xlabel("All-tests FDR-supported local-r_g loci")
    for i,(p,n) in enumerate(zip(pos,neg)):
        if p: ax.text(p+.7,i,str(p),va="center",fontsize=7,color=INK)
        if n: ax.text(-n-.7,i,str(n),va="center",ha="right",fontsize=7,color=INK)
    ax.legend(frameon=False,fontsize=6.5,loc="lower right")
    for ax in axs:
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=7); ax.grid(axis="x",color=GRID,lw=.45,zorder=0)
    fig.tight_layout(w_pad=2.3); save(fig,"Figure4_genetic_evidence")


def figure5() -> None:
    from matplotlib.patches import FancyBboxPatch
    fig,ax=plt.subplots(figsize=(10.5,5.55),facecolor="white"); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.text(.04,.95,"TISSUE-STATE LAYER",fontsize=10.5,weight="bold",color=INK,va="top")
    ax.text(.04,.40,"INHERITED-LIABILITY LAYER",fontsize=10.5,weight="bold",color=INK,va="top")
    box(ax,.04,.68,.60,.18,"Skin-primary programs","F1 · lesional skin     F2 · non-lesional skin     F6 · lesional skin",COLORS["F1"],"#FFF8F7")
    box(ax,.69,.68,.27,.18,"F7","Blood-associated supportive program",COLORS["F7"],"#F6F7FB")
    ax.text(.05,.61,"External paired-skin concordance · cellular and spatial context",fontsize=7.8,color=MUTED)
    ax.plot([.50,.50],[.57,.49],color="#7C8791",lw=1.1,ls=(0,(2,2))); ax.scatter([.5],[.53],s=34,facecolor="white",edgecolor="#7C8791",zorder=3)
    ax.text(.52,.54,"No robust program-specific genetic enrichment detected",fontsize=7.2,va="center",color="#46515C")
    ax.text(.52,.49,"Related, non-equivalent evidence layers",fontsize=7.2,va="center",color="#46515C")
    box(ax,.04,.10,.29,.22,"Overall psoriasis susceptibility","Genome-wide inherited liability","#55616E","#F8FAFB")
    ax.annotate("",xy=(.39,.21),xytext=(.33,.21),arrowprops={"arrowstyle":"->","color":"#79848E","lw":1.2})
    ax.add_patch(FancyBboxPatch((.40,.07),.56,.28,boxstyle="round,pad=.012,rounding_size=.015",transform=ax.transAxes,facecolor="#FBFCFD",edgecolor="#B9C2C9",lw=1))
    ax.text(.68,.295,"Shared architecture with selected outcomes",transform=ax.transAxes,ha="center",va="center",fontsize=8.2,weight="bold",color=INK)
    ax.text(.44,.215,"CAD",transform=ax.transAxes,fontsize=8.2,weight="bold",color="#2A8C82",va="center")
    ax.text(.57,.215,"Clearest QC-passing non-neighbor signal",transform=ax.transAxes,fontsize=7.1,color="#46515C",va="center")
    ax.text(.44,.135,"PsA: near-neighbor positive control · IBD: QC-sensitive, mixed local directions",transform=ax.transAxes,fontsize=6.6,color="#46515C",va="center")
    ax.text(.04,.015,"Tissue expression describes sampled state; genetic correlation summarizes inherited covariance.",fontsize=7.6,color="#46515C")
    save(fig,"Figure5_two_layer_model")


def main() -> None:
    figure1(); figure2(); figure3(); figure4(); figure5()
    print(f"Wrote five TIFF/SVG figure pairs to {FIGURES}")


if __name__ == "__main__":
    main()
