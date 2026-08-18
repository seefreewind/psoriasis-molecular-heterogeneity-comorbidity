#!/usr/bin/env python3
"""Generate Communications Biology manuscript draft assets from frozen project results.

This script intentionally performs no new discovery analysis. It only reads frozen
tables/reports and assembles manuscript-facing Markdown/TSV assets.
"""

from __future__ import annotations

import csv
from pathlib import Path
from textwrap import dedent

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT = ROOT / "manuscript"
TABLES = MANUSCRIPT / "tables"
SUPP = MANUSCRIPT / "supplementary_tables"
REPORTS = ROOT / "reports"


def fmt_p(x: float) -> str:
    if pd.isna(x):
        return ""
    if x == 0:
        return "0"
    if abs(x) < 1e-3:
        return f"{x:.3e}"
    return f"{x:.4f}".rstrip("0").rstrip(".")


def fmt_num(x: float, nd: int = 3) -> str:
    if pd.isna(x):
        return ""
    return f"{x:.{nd}f}".rstrip("0").rstrip(".")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, str]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join(["---"] * len(cols)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(c, "")).replace("\n", "<br>") for c in cols) + " |")
    return "\n".join([header, sep] + body)


def load_optional_tsv(rel: str) -> pd.DataFrame:
    path = ROOT / rel
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t")


def build_tables() -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    table1_cols = [
        "Dataset/accession", "Modality", "Disease/group", "Sample size",
        "Tissue", "Role", "Primary analysis", "Key limitation",
    ]
    table1 = [
        {
            "Dataset/accession": "E-MTAB-14509",
            "Modality": "bulk RNA-seq",
            "Disease/group": "psoriasis baseline discovery/replication",
            "Sample size": "146 patients; 76 complete baseline three-view discovery patients; 57 paired-skin replication patients",
            "Tissue": "lesional skin, non-lesional skin, blood",
            "Role": "molecular-program discovery and internal replication",
            "Primary analysis": "cluster stability, MOFA factors, tissue contribution, paired-skin replication",
            "Key limitation": "baseline complete-case subset used for multi-view modeling",
        },
        {
            "Dataset/accession": "GSE244679",
            "Modality": "bulk RNA-seq",
            "Disease/group": "psoriasis paired skin",
            "Sample size": "24 paired lesional/adjacent normal samples",
            "Tissue": "lesional and non-lesional/adjacent skin",
            "Role": "independent paired-skin replication",
            "Primary analysis": "projection of frozen molecular-program signatures",
            "Key limitation": "skin-only validation; no systemic compartment",
        },
        {
            "Dataset/accession": "GSE228421",
            "Modality": "single-cell RNA-seq",
            "Disease/group": "psoriasis skin",
            "Sample size": "20 10x samples from 5 donors",
            "Tissue": "skin",
            "Role": "donor-level cellular contextualization",
            "Primary analysis": "per-cell scoring summarized by donor and cell type",
            "Key limitation": "directional support rather than definitive cell-state mechanism",
        },
        {
            "Dataset/accession": "GSE173706",
            "Modality": "single-cell RNA-seq",
            "Disease/group": "psoriasis skin",
            "Sample size": "33 samples",
            "Tissue": "skin",
            "Role": "independent single-cell sensitivity",
            "Primary analysis": "directional program localization sensitivity",
            "Key limitation": "used for support, not for reselecting programs",
        },
        {
            "Dataset/accession": "GSE225475",
            "Modality": "spatial transcriptomics",
            "Disease/group": "psoriasis and control skin",
            "Sample size": "6 spatial samples",
            "Tissue": "skin sections",
            "Role": "primary spatial contextualization",
            "Primary analysis": "spatial program correlations and epidermal/stress context",
            "Key limitation": "section/spot-level observations do not replace patient-level replication",
        },
        {
            "Dataset/accession": "GSE202011",
            "Modality": "spatial transcriptomics",
            "Disease/group": "psoriasis skin",
            "Sample size": "30 spatial samples",
            "Tissue": "skin sections",
            "Role": "external spatial robustness",
            "Primary analysis": "spatial program correlation sensitivity",
            "Key limitation": "spatial support is contextual and not a genetic anchor",
        },
        {
            "Dataset/accession": "GCST90472771",
            "Modality": "GWAS summary statistics",
            "Disease/group": "psoriasis",
            "Sample size": "36,466 cases and 458,078 controls",
            "Tissue": "germline",
            "Role": "overall psoriasis susceptibility exposure",
            "Primary analysis": "LDSC, restricted LAVA, SMR/HEIDI, coloc",
            "Key limitation": "overall susceptibility; not F1/F2/F6/F7-specific",
        },
        {
            "Dataset/accession": "Frozen comorbidity GWAS panel",
            "Modality": "GWAS summary statistics",
            "Disease/group": "PsA, Crohn disease, ulcerative colitis, CAD, ischemic stroke, CKD; T2D/MASLD/MDD/uveitis source-unresolved",
            "Sample size": "trait-specific; CAD 122,733 cases/424,528 controls; PsA 5,065 cases/21,286 controls; Crohn disease 12,194 cases/28,072 controls; UC 12,366 cases/33,609 controls",
            "Tissue": "germline",
            "Role": "multisystem shared genetic architecture",
            "Primary analysis": "LDSC genetic correlation and restricted local genetic correlation",
            "Key limitation": "unavailable primary sources are not biological null outcomes",
        },
        {
            "Dataset/accession": "GTEx v8",
            "Modality": "eQTL summary data",
            "Disease/group": "non-disease reference tissues",
            "Sample size": "tissue-specific GTEx v8 sample sizes",
            "Tissue": "skin, blood, vascular/arterial, spleen, intestinal and immune-relevant tissues",
            "Role": "restricted regulatory prioritization",
            "Primary analysis": "SMR/HEIDI and coloc for Tier 1/2 shared loci",
            "Key limitation": "reference eQTL tissue context may not match inflamed psoriasis tissue",
        },
    ]
    write_tsv(TABLES / "Table1_public_datasets_and_roles.tsv", table1, table1_cols)

    table2_cols = [
        "Program", "Dominant tissue", "Bulk replication", "Cellular support",
        "Spatial support", "Genetic anchoring", "Final role", "Allowed interpretation",
    ]
    table2 = [
        {
            "Program": "F1",
            "Dominant tissue": "skin-primary",
            "Bulk replication": "GSE244679 lesional skin |rho| = 0.688",
            "Cellular support": "directional keratinocyte/stress-inflammatory support",
            "Spatial support": "GSE225475 rho = 0.502; GSE202011 rho = 0.489",
            "Genetic anchoring": "Tier D; no robust axis-specific genetic anchoring",
            "Final role": "retained tissue molecular program",
            "Allowed interpretation": "skin tissue-state program with directional keratinocyte/spatial support; not a genetically anchored endotype",
        },
        {
            "Program": "F2",
            "Dominant tissue": "skin-primary",
            "Bulk replication": "GSE244679 non-lesional skin |rho| = 0.518",
            "Cellular support": "directional keratinocyte/stress-inflammatory support",
            "Spatial support": "GSE225475 rho = 0.506; GSE202011 rho = 0.491",
            "Genetic anchoring": "Tier D; no robust axis-specific genetic anchoring",
            "Final role": "retained tissue molecular program",
            "Allowed interpretation": "skin tissue-state program with possible field-state support; not a genetically anchored endotype",
        },
        {
            "Program": "F6",
            "Dominant tissue": "skin-primary",
            "Bulk replication": "GSE244679 lesional skin |rho| = 0.375",
            "Cellular support": "directional keratinocyte/stress support",
            "Spatial support": "GSE225475 rho = 0.546; GSE202011 rho = 0.496",
            "Genetic anchoring": "Tier D; no robust axis-specific genetic anchoring",
            "Final role": "retained tissue molecular program",
            "Allowed interpretation": "skin stress/hypoxia-like tissue program with directional support; not a genetically anchored endotype",
        },
        {
            "Program": "F7",
            "Dominant tissue": "systemic/supportive",
            "Bulk replication": "internal skin-blood support rho = 0.577; GSE61281 support |rho| = 0.455",
            "Cellular support": "low-confidence systemic immune/myeloid direction",
            "Spatial support": "GSE225475 rho = 0.505; GSE202011 rho = 0.485, but not coherent skin-spatial immune localization",
            "Genetic anchoring": "Tier D; no robust axis-specific genetic anchoring",
            "Final role": "supportive systemic candidate",
            "Allowed interpretation": "systemic-supportive immune candidate only; not a skin-spatial or genetic axis",
        },
    ]
    write_tsv(TABLES / "Table2_molecular_program_interpretation.tsv", table2, table2_cols)

    cand = load_optional_tsv("results/phase4d_coloc/manuscript_tables/phase4d_coloc_supported_and_suggestive_candidates.tsv")
    table3_cols = [
        "Outcome", "Locus", "Gene", "SMR/HEIDI tier", "Recurrence status",
        "coloc PP4", "Tissue", "Interpretation", "Sensitivity flag",
    ]
    table3: list[dict[str, str]] = []
    if not cand.empty:
        cand = cand.sort_values(["interpretation_tier", "PP.H4.abf"], ascending=[True, False])
        for _, r in cand.iterrows():
            tier = str(r.get("phase4c_eqtl_gene_tier", ""))
            rec = "recurrent SMR2" if "recurrent" in tier else "single-tissue/SNR-supported"
            flag = "eqtl MAF proxy" if str(r.get("maf_source", "")) == "eqtl_maf_proxy" else "standard coloc input"
            interp_tier = str(r.get("interpretation_tier", ""))
            interp = "PP4-supported shared regulatory signal" if "supported" in interp_tier else "suggestive regulatory signal; PP3/PP4 balance requires conservative wording"
            table3.append({
                "Outcome": str(r["outcome"]).upper() if str(r["outcome"]) in {"cad", "psa", "uc"} else str(r["outcome"]).capitalize(),
                "Locus": str(int(r["locus"])),
                "Gene": str(r["gene"]),
                "SMR/HEIDI tier": tier,
                "Recurrence status": rec,
                "coloc PP4": fmt_num(float(r["PP.H4.abf"]), 3),
                "Tissue": str(r["tissue"]),
                "Interpretation": interp,
                "Sensitivity flag": flag,
            })
    write_tsv(TABLES / "Table3_regulatory_prioritization_coloc.tsv", table3, table3_cols)
    return table1, table2, table3


def build_supplementary_tables() -> None:
    sources = {
        "Supplementary_Table_1_phase4a_ldsc_rg_results.tsv": "results/phase4a/phase4a_ldsc_rg_results.tsv",
        "Supplementary_Table_2_phase4b_restricted_lava_summary.tsv": "results/phase4b_restricted_lava/phase4b_restricted_lava_summary.tsv",
        "Supplementary_Table_3_phase4b_restricted_lava_top_loci.tsv": "results/phase4b_restricted_lava/phase4b_restricted_lava_top_loci.tsv",
        "Supplementary_Table_4_phase4c_frozen_shared_locus_eqtl_gene_table.tsv": "results/phase4c_smr/phase4c_frozen_shared_locus_eqtl_gene_table.tsv",
        "Supplementary_Table_5_phase4d_coloc_supported_and_suggestive_candidates.tsv": "results/phase4d_coloc/manuscript_tables/phase4d_coloc_supported_and_suggestive_candidates.tsv",
        "Supplementary_Table_6_phase4d_coloc_supported_and_suggestive_counts.tsv": "results/phase4d_coloc/manuscript_tables/phase4d_coloc_supported_and_suggestive_counts.tsv",
        "Supplementary_Table_7_phase4e_coloc_axis_overlap_summary.tsv": "results/phase4e_contextualization/phase4e_coloc_axis_overlap_summary.tsv",
    }
    rows = []
    for out_name, rel in sources.items():
        src = ROOT / rel
        dst = SUPP / out_name
        if src.exists():
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            status = "copied"
        else:
            status = "missing"
        rows.append({"Supplementary table": out_name, "Source": rel, "Status": status})
    write_tsv(SUPP / "supplementary_table_manifest.tsv", rows, ["Supplementary table", "Source", "Status"])


def build_main_manuscript(table1: list[dict[str, str]], table2: list[dict[str, str]], table3: list[dict[str, str]]) -> str:
    phase4a = load_optional_tsv("results/phase4a/phase4a_ldsc_rg_results.tsv")
    ldsc_rows = {}
    if not phase4a.empty:
        for _, r in phase4a.iterrows():
            ldsc_rows[str(r["Outcome"])] = r

    refs = dedent(
        """
        ## References

        1. Patrick, M. T. et al. Shared genetic risk factors and causal association between psoriasis and coronary artery disease. *Nature Communications* (2022). doi:10.1038/s41467-022-34323-4.
        2. Dand, N. et al. GWAS meta-analysis of psoriasis identifies new susceptibility alleles impacting disease mechanisms and therapeutic targets. *Nature Communications* (2025). doi:10.1038/s41467-025-56719-8.
        3. Stuart, P. E. et al. Genome-wide association analysis of psoriatic arthritis and cutaneous psoriasis reveals differences in their genetic architecture. *American Journal of Human Genetics* (2015). doi:10.1016/j.ajhg.2015.10.019.
        4. Ellinghaus, D. et al. Combined analysis of genome-wide association studies for Crohn disease and psoriasis identifies seven shared susceptibility loci. *American Journal of Human Genetics* (2012). doi:10.1016/j.ajhg.2012.02.020.
        5. Li, W.-Q., Han, J. & Qureshi, A. A. Psoriasis, psoriatic arthritis and increased risk of incident Crohn's disease in US women. *Annals of the Rheumatic Diseases* (2013). doi:10.1136/annrheumdis-2012-202143.
        6. Gelfand, J. M. et al. Risk of myocardial infarction in patients with psoriasis. *JAMA* (2006). doi:10.1001/jama.296.14.1735.
        7. Werme, J., van der Sluis, S., Posthuma, D. & de Leeuw, C. A. An integrated framework for local genetic correlation analysis. *Nature Genetics* (2022). doi:10.1038/s41588-022-01017-y.
        8. Zhu, Z. et al. Integration of summary data from GWAS and eQTL studies predicts complex trait gene targets. *Nature Genetics* (2016). doi:10.1038/ng.3538.
        9. The GTEx Consortium. The GTEx Consortium atlas of genetic regulatory effects across human tissues. *Science* (2020). doi:10.1126/science.aaz1776.
        10. Giambartolomei, C. et al. Bayesian test for colocalisation between pairs of genetic association studies using summary statistics. *PLoS Genetics* (2014). doi:10.1371/journal.pgen.1004383.
        """
    ).strip()

    text = f"""
# Molecular heterogeneity and multisystem shared genetic architecture define distinct biological layers of psoriasis

Alternative conservative title: Reproducible tissue molecular programs and shared comorbidity genetics in psoriasis

Alternative concise title: Distinct molecular and genetic layers of psoriasis

## Abstract

Psoriasis is clinically associated with inflammatory, cardiometabolic and musculoskeletal comorbidities, but it remains unclear whether tissue molecular heterogeneity and inherited multisystem risk represent the same biological layer. We integrated public psoriasis transcriptomic datasets, psoriasis GWAS summary statistics, comorbidity GWAS resources and GTEx v8 eQTL data under a locked analysis framework. Unsupervised discrete transcriptomic endotypes were unstable, with a minimum bootstrap Jaccard index of 0.562, below the predefined stability threshold. Multi-view modeling of 76 complete baseline discovery patients instead identified eight stable continuous factors, from which F1, F2, F6 and F7 were retained as frozen molecular programs. F1, F2 and F6 showed independent paired-skin replication and directional single-cell/spatial support, while F7 remained a systemic-supportive candidate. Axis-specific genetic anchoring failed for all four programs. Overall psoriasis susceptibility then showed disease-specific shared genetic architecture, including a clean positive genetic correlation with coronary artery disease and strong positive-control sharing with psoriatic arthritis. Restricted local genetic correlation, SMR/HEIDI and coloc prioritized a limited set of regulatory candidates, but these did not overlap the frozen molecular programs. These findings support a layered model in which reproducible psoriasis tissue states and inherited multisystem comorbidity architecture are partially separable.

## Introduction

Psoriasis is a chronic immune-mediated skin disease with genetic, immunological and tissue-remodeling components. Its systemic relevance is well established by associations with psoriatic arthritis, inflammatory bowel disease and cardiovascular outcomes, and prior genetic studies have reported shared susceptibility between psoriasis and coronary artery disease, psoriatic arthritis and Crohn disease. These findings indicate that psoriasis cannot be understood only as a skin-limited disorder. At the same time, systemic association does not imply that every tissue molecular state in psoriasis is directly encoded by inherited comorbidity risk.

Transcriptomic studies have repeatedly shown strong inflammatory and keratinocyte-response signals in psoriatic skin. A common next step is to divide patients into discrete molecular endotypes and then interpret those groups as biologically distinct disease states. That strategy is attractive for manuscript clarity, but it is vulnerable when cluster assignments are unstable, sample size is modest or tissue compartments contribute different sources of variation. In this project, the discrete endotype route was tested first and rejected by predefined stability criteria. This decision shifted the transcriptomic framework from categorical endotypes to continuous molecular programs.

The genetic analysis required a separate boundary. If frozen molecular programs were robustly enriched for psoriasis susceptibility genetics, they could support genetically anchored molecular axes. If not, the appropriate genetic question becomes whether overall psoriasis susceptibility shares inherited architecture with comorbid diseases. This distinction matters because post hoc genetic reinterpretation of transcriptomic factors can create circular mechanistic claims. We therefore tested axis-specific genetic anchoring before moving to comorbidity genetics and treated its failure as an informative result.

Here we assemble the final locked analysis into a Communications Biology manuscript framework. The study combines reproducible psoriasis tissue molecular heterogeneity, donor-level and spatial contextualization, overall psoriasis-comorbidity genetic correlation, restricted local genetic correlation and regulatory prioritization through GTEx v8 eQTL resources. The central claim is deliberately bounded: psoriasis tissue-state heterogeneity and inherited multisystem comorbidity architecture represent partially separable biological layers.

## Results

### Continuous molecular programs capture reproducible psoriasis tissue heterogeneity

The initial transcriptomic analysis evaluated whether patients could be separated into stable discrete molecular endotypes. The k = 2 solution did not meet the predefined stability rule: the minimum bootstrap Jaccard index was 0.562, below the 0.75 threshold used to support stable cluster membership. This result closed the discrete-endotype route and prevented a categorical endotype claim.

The analysis then moved to continuous multi-view molecular modeling. MOFA modeled 76 complete baseline discovery patients across lesional skin, non-lesional skin and blood, and eight factors were stable across five random seeds. A frozen prioritization matrix selected F1, F2, F6 and F7 for manuscript-level interpretation. F1, F2 and F6 were retained as skin-primary bulk molecular programs, whereas F7 was retained only as a systemic/supportive candidate. This selection was based on stability, tissue contribution, internal replication, external replication and biological interpretability, not on a single nominal association.

Independent paired-skin replication supported the skin-primary interpretation. In GSE244679, F1 showed the strongest lesional-skin support (|rho| = 0.688), F2 showed non-lesional support (|rho| = 0.518), and F6 showed lesional-skin support (|rho| = 0.375). These results support a continuous molecular-program framework while keeping mechanism naming conservative. The final molecular-program interpretation is summarized in Table 2.

### Selected molecular programs show directional cellular and spatial organization

Single-cell and spatial analyses were used to contextualize the frozen programs, not to redefine them. The main statistical unit was donor or sample-level summarized signal rather than individual cells treated as independent observations. GSE228421 provided the primary donor-level single-cell localization analysis, with GSE173706 used as an independent sensitivity dataset. These analyses supported directional keratinocyte/stress-inflammatory localization for the skin-primary programs but did not justify strong cell-state naming.

Spatial transcriptomics provided consistent directional context. F1, F2 and F6 showed positive spatial correlations in both spatial datasets: F1 showed rho = 0.502 in GSE225475 and rho = 0.489 in GSE202011; F2 showed rho = 0.506 and rho = 0.491; F6 showed rho = 0.546 and rho = 0.496. F7 also showed positive spatial correlations (rho = 0.505 and rho = 0.485), but its broader evidence did not support coherent skin-spatial immune localization. It therefore remained a low-confidence systemic/supportive candidate.

These findings support directional cellular and spatial organization for the selected tissue programs. They do not support claims that F1, F2 or F6 are definitive keratinocyte endotypes, nor that F7 is a skin-localized immune axis.

### Reproducible molecular programs do not define independent inherited genetic axes

The frozen F1, F2, F6 and F7 programs were next tested for axis-specific psoriasis genetic anchoring. This phase was deliberately placed before multisystem genetics to prevent interpreting genetic results through mutable transcriptomic labels. All four programs were assigned Tier D in the final genetic evidence table. No program met the predefined threshold for a robust genetically anchored molecular axis.

This negative result changed the manuscript logic. The tissue programs remained valid transcriptomic findings with replication and contextual support, but they were removed from the genetics main analysis. All subsequent genetic analyses therefore used overall psoriasis susceptibility from GCST90472771 as the exposure layer. This decision is central to the final interpretation: transcriptomic heterogeneity and inherited comorbidity architecture are not collapsed into a single axis-specific genetic mechanism.

### Overall psoriasis susceptibility shows disease-specific multisystem genetic sharing

The Phase 4A genetic analysis tested genome-wide LDSC genetic correlation between overall psoriasis susceptibility and frozen comorbidity outcomes. Six outcomes passed data availability and QC sufficiently for the formal LDSC table. Coronary artery disease provided the cleanest non-neighbor systemic signal, with rg = 0.1732, SE = 0.0274, P = 2.498e-10 and FDR = 7.494e-10, with QC status PASS.

Psoriatic arthritis behaved as a positive-control and near-neighbor phenotype rather than an independent multisystem discovery. It showed very high genetic correlation with psoriasis (rg = 1.1715, SE = 0.0751, P = 6.746e-55, FDR = 4.048e-54), but the result carried a near-neighbor and elevated cross-trait-intercept label. Crohn disease and ulcerative colitis showed significant negative genetic correlations: Crohn disease rg = -0.2717, SE = 0.0449, P = 1.434e-09, FDR = 2.868e-09; ulcerative colitis rg = -0.2233, SE = 0.0409, P = 4.820e-08, FDR = 7.229e-08. Both IBD outcomes were retained with QC flags because their h2 and cross-trait intercepts required cautious interpretation.

Ischemic stroke and chronic kidney disease were null or low-power references in the available data. Ischemic stroke showed rg = 0.0255 and P = 0.6647; chronic kidney disease showed rg = 0.0118 and P = 0.7912. Type 2 diabetes, MASLD, major depressive disorder and uveitis were not treated as null because their frozen primary data sources remained unresolved or unavailable in the completed analysis.

### Local genetic correlation reveals heterogeneous comorbidity architectures

Restricted LAVA was applied after the global LDSC analysis and after sign/QC adjudication. The aim was to identify where psoriasis-comorbidity sharing was concentrated and whether local architecture was concordant or heterogeneous across disease systems. CAD remained the primary systemic target. In CAD, 118 loci had bivariate local tests, 23 loci were FDR-supported in the full restricted report, and the median local rho was 0.0787. Positive nominal local signals outnumbered negative nominal signals (21 versus 10), and the leading CAD locus reached rho = 0.6508.

Psoriatic arthritis served as a positive-control local architecture. It showed strong positive sharing, with 40 bivariate loci, 31 FDR-supported loci, 36 nominal positive loci, no nominal negative loci and median rho = 0.6315. This pattern was consistent with the high global genetic correlation and the near-neighbor nature of the trait.

Crohn disease and ulcerative colitis showed directionally heterogeneous local architectures. Crohn disease had 131 bivariate loci, 49 FDR-supported loci, 9 nominal positive loci, 51 nominal negative loci and median rho = -0.2078. Ulcerative colitis had 98 bivariate loci, 19 FDR-supported loci, 7 nominal positive loci, 18 nominal negative loci and median rho = -0.0479. Locus 57 was prominent in both IBD analyses, with negative local rho estimates. These results argue against reducing psoriasis-IBD genetics to a single genome-wide direction and instead support locus-level heterogeneity.

### Restricted regulatory prioritization separates shared genetic architecture from shared regulatory signals

The final regulatory step used only frozen shared-locus candidates and relevant GTEx v8 eQTL tissues. SMR/HEIDI prioritized 91 outcome-gene rows, and the highest frozen tier contained 33 genes. A second probe-window sensitivity retained 100% of SMR1 outcome-gene candidates at the gene level, supporting the stability of the restricted prioritization set.

Colocalization further refined this set. Among manuscript-relevant candidates, PsA showed three PP4-supported signals, including SLC22A5 in spleen (PP4 = 0.971) and lymphoblastoid-cell RP11-977G19.11 (PP4 = 0.945), plus SLC22A5 in lymphoblastoid cells (PP4 = 0.934). Ulcerative colitis showed two PP4-supported RP11-973H7.1 signals in transverse and sigmoid colon (PP4 = 0.960 and 0.960), both using eQTL MAF proxy inputs. CAD did not yield a high-confidence PP4 signal in the restricted coloc analysis, but skin UBQLN4 and MEX3A at locus 113 were suggestive (PP4 range 0.595-0.754). Crohn disease produced suggestive SLC22A5 and PARK7 signals (PP4 = 0.639 and 0.565), both with eQTL MAF proxy sensitivity flags.

Phase 4E then tested whether PP4-supported or suggestive coloc genes overlapped the frozen F1/F2/F6/F7 CORE/EXTENDED gene programs. No supported or suggestive coloc gene overlapped these frozen programs. This result reinforces the layered interpretation: the regulatory candidates contextualize overall psoriasis-comorbidity genetics, while the tissue molecular programs contextualize transcriptomic heterogeneity. They should not be merged into axis-specific genetic claims.

## Discussion

This study resolves the project into a layered model of psoriasis biology. The transcriptomic analyses support reproducible continuous tissue molecular programs, especially F1, F2 and F6 as skin-primary programs and F7 as a systemic-supportive candidate. The genetic analyses do not support the same programs as independent inherited psoriasis axes. Instead, overall psoriasis susceptibility shows disease-specific shared genetic architecture with comorbid outcomes, most cleanly for coronary artery disease, strongly for psoriatic arthritis as a positive-control phenotype, and heterogeneously for inflammatory bowel disease. The final message is that psoriasis tissue-state heterogeneity and inherited multisystem comorbidity architecture are partially separable biological layers.

The rejection of discrete k = 2 endotypes is an important strength of the analysis. A categorical endotype framing would have produced a simpler story, but the cluster stability result did not justify it. Moving to continuous molecular programs preserved the reproducible transcriptomic signal while avoiding overinterpretation of unstable patient groups. This choice also matches the biological expectation that lesional inflammation, non-lesional field effects, blood immune variation and treatment-naive disease state may vary continuously rather than forming clean categories.

The single-cell and spatial analyses sharpened the tissue interpretation without overstating mechanism. F1, F2 and F6 showed directional keratinocyte/stress-inflammatory and spatial support, with independent paired-skin replication. These data support their use as tissue molecular programs. They do not establish them as definitive cell-state mechanisms, treatment-response classes or genetically encoded disease subtypes. F7 is particularly important as a boundary case: despite systemic-supportive evidence, it did not become a coherent skin-spatial immune axis and should remain a supportive candidate.

The failure of axis-specific genetic anchoring prevents a common interpretive error. A reproducible transcriptomic program is not automatically a germline risk axis. Environmental exposure, disease duration, tissue inflammation, cellular composition and local injury responses can all shape tissue programs without producing detectable enrichment in inherited susceptibility signals. By closing the axis-specific genetic route before testing comorbidities, the analysis avoids retrofitting genetic associations to flexible molecular labels.

The overall psoriasis susceptibility analysis still provides a meaningful multisystem result. CAD was the most robust non-neighbor systemic finding, consistent with epidemiological and genetic evidence connecting psoriasis with cardiovascular disease. PsA behaved as expected for a closely related phenotype and served as a positive-control architecture. The IBD results were more complex: negative genome-wide correlations and mixed local directions indicate that shared susceptibility cannot be described as uniformly concordant. Local genetic correlation is therefore essential for interpreting psoriasis-IBD relationships.

The restricted SMR/HEIDI and coloc analyses provide candidate regulatory links while also defining limits. PP4-supported signals were strongest for PsA and UC, whereas CAD and Crohn disease yielded suggestive rather than high-confidence coloc support in the manuscript-relevant candidate set. The absence of overlap between coloc-supported/suggestive genes and frozen F1/F2/F6/F7 programs argues against using these results to resurrect axis-specific genetics. Instead, the regulatory candidates should be presented as locus-level context for overall psoriasis-comorbidity sharing.

Several limitations define the final claim strength. The study uses public datasets with different platforms, tissues and ascertainment schemes. Spatial and single-cell analyses provide contextual support but are not interventional validation. Some intended comorbidity GWAS sources were unresolved and cannot be interpreted as null. LAVA and coloc depend on reference panels, locus definitions, variant coverage and eQTL tissue availability. GTEx tissues are useful regulatory references but do not fully represent inflamed psoriatic skin or disease-specific immune niches. These limitations do not erase the main result; they define it as a reproducible, public-data, genetic-statistical framework rather than a causal or clinically validated disease classification.

In conclusion, psoriasis can be represented by reproducible tissue molecular programs and by inherited multisystem shared genetic architecture, but these layers should not be forced into a single axis-specific genetic model. This separation provides a clearer foundation for future work: transcriptomic programs can be tested in perturbation and longitudinal tissue datasets, while shared genetic loci can be followed through ancestry-aware fine mapping, disease-relevant eQTL resources and functional validation.

## Methods

### Study design and analysis locks

All analyses were organized into sequential phases with frozen decision rules. Discrete endotype stability was evaluated before continuous molecular modeling. Molecular programs were frozen before single-cell, spatial and genetic contextualization. Axis-specific genetic anchoring was tested before overall comorbidity genetics. Broad MR, axis-specific MR/LDSC/LAVA/coloc, post hoc GWAS replacement, drug prediction, PPI, hub-gene analysis, LASSO and machine-learning marker selection were excluded from the final manuscript route.

### Transcriptomic discovery and replication

E-MTAB-14509 was used for bulk transcriptomic discovery and internal replication across lesional skin, non-lesional skin and blood. Discrete clustering was assessed by bootstrap stability. Continuous molecular programs were modeled using multi-view factor analysis across complete baseline patients. Program prioritization used stability, tissue contribution, independent paired-skin replication, biological interpretability, confounding independence and systemic support. GSE244679 was used for independent paired-skin replication of frozen signatures.

### Single-cell and spatial contextualization

Frozen CORE and EXTENDED gene programs were scored in single-cell datasets and summarized at donor/cell-type level. GSE228421 provided the primary donor-level single-cell contextualization, and GSE173706 provided independent sensitivity support. GSE225475 and GSE202011 were used for spatial contextualization. Spot/section-level spatial results were treated as contextual evidence and were not used as patient-level replication.

### Axis-specific genetic anchoring

Frozen F1, F2, F6 and F7 gene programs were tested for psoriasis genetic support using predefined enrichment and sensitivity criteria. The final evidence tier for each program was assigned before comorbidity genetics. Because all four programs were Tier D, they were excluded from genetic main analyses.

### Genome-wide genetic correlation

Overall psoriasis susceptibility was represented by GCST90472771. Frozen comorbidity GWAS outcomes included psoriatic arthritis, Crohn disease, ulcerative colitis, coronary artery disease, ischemic stroke, chronic kidney disease and additional prespecified outcomes whose primary data sources remained unresolved. Summary statistics were harmonized to a common LDSC-compatible framework. LDSC estimated genome-wide genetic correlation, standard error, Z statistic, P value, FDR, single-trait heritability and cross-trait intercept.

### Local genetic correlation

Restricted LAVA was applied only after Phase 4A and sign/QC adjudication. CAD was the primary systemic target, PsA was a positive-control/near-neighbor target, and Crohn disease and ulcerative colitis were retained as QC-flagged IBD targets. Local heritability screening preceded bivariate local genetic correlation. High-value loci were reviewed through LD-reference validation before downstream regulatory prioritization.

### Regulatory prioritization and colocalization

Restricted shared-locus candidates were prioritized with GTEx v8 eQTL data using SMR/HEIDI. Candidate tissues were selected according to outcome relevance: skin, blood and vascular/arterial tissues for CAD; skin and immune tissues for PsA; and skin, blood, intestinal and immune tissues for Crohn disease and ulcerative colitis. Colocalization was then applied to Tier A restricted candidates. PP4 >= 0.8 was treated as supported coloc evidence, PP4 from 0.5 to 0.8 as suggestive, and PP3 greater than PP4 as evidence favoring distinct association signals.

## Data Availability

All transcriptomic and spatial datasets used in the manuscript are public: E-MTAB-14509, GSE244679, GSE228421, GSE173706, GSE225475 and GSE202011. Psoriasis GWAS summary statistics were represented by GCST90472771. GTEx v8 eQTL resources were used for regulatory prioritization. Comorbidity GWAS sources were frozen before analysis; outcomes whose primary sources remained unresolved or restricted are reported as unavailable rather than biological null results. Processed result tables generated by this project are stored under the project `results/` and `manuscript/supplementary_tables/` directories.

## Code Availability

Analysis code and manuscript-generation scripts will be deposited before submission. Repository DOI: [repository DOI to be added before submission]. The current manuscript asset generator is `src/manuscript/generate_cb_manuscript_assets.py`.

## Author Contributions

[Author contribution statement to be completed before submission.]

## Competing Interests

[Competing interests statement to be completed before submission.]

## Acknowledgements

[Funding and acknowledgement statement to be completed before submission.]

## Figure Legends

**Figure 1. Study design and transition from unstable discrete endotypes to continuous molecular programs.** The figure should show the public dataset inputs, the failed k = 2 stability decision, the move to continuous MOFA programs and the frozen downstream analysis sequence.

**Figure 2. Molecular-program prioritization and independent bulk replication.** The figure should summarize the evidence matrix for F1, F2, F6 and F7, tissue contribution and GSE244679 paired-skin replication.

**Figure 3. Directional single-cell and spatial contextualization.** The figure should show donor-level single-cell localization and spatial correlation summaries for frozen programs, using contextual rather than definitive mechanism language.

**Figure 4. Axis-specific genetics fails while overall psoriasis susceptibility remains the genetic layer.** The figure should show Tier D assignment for F1/F2/F6/F7 and the conceptual pivot from molecular-axis genetics to overall psoriasis-comorbidity genetics.

**Figure 5. Genome-wide and local shared genetic architecture.** The figure should combine LDSC genetic correlations and restricted LAVA local architectures for CAD, PsA, Crohn disease and ulcerative colitis.

**Figure 6. Restricted regulatory prioritization and layered biological model.** The figure should combine SMR/HEIDI tiers, coloc-supported/suggestive candidates and the final model separating tissue molecular programs from inherited comorbidity architecture.

## Tables

### Table 1. Public datasets and analytical roles

{md_table(table1, list(table1[0].keys()))}

### Table 2. Final molecular-program interpretation and evidence boundaries

{md_table(table2, list(table2[0].keys()))}

### Table 3. Restricted regulatory prioritization and colocalization results

{md_table(table3, list(table3[0].keys()))}

{refs}
"""
    return dedent(text).strip()


def build_supp_methods() -> str:
    return dedent(
        """
        # Communications Biology Supplementary Methods v1

        ## Analysis Governance

        The project used phase-specific locks to prevent post hoc redesign. The final manuscript preserves four decisions: `GO_TO_MANUSCRIPT_ASSEMBLY`, `CONDITIONAL_GO_TO_TARGETED_FIGURE_COMPLETION`, `NO_GO_TO_BROAD_MR` and `NO_GO_TO_AXIS_SPECIFIC_GENETICS`. No new discovery analysis was performed during manuscript assembly.

        ## Prohibited Analyses

        The final manuscript excludes broad MR, axis-specific MR/LDSC/LAVA/coloc, new cohort hunting, single-cell or spatial rescue analysis, drug prediction, PPI, hub-gene analysis, LASSO, machine-learning marker selection and post hoc GWAS replacement.

        ## Transcriptomic Program Definition

        Discrete k = 2 endotypes were rejected because the minimum bootstrap Jaccard index was 0.562, below the predefined 0.75 stability threshold. Continuous MOFA factors were then modeled in 76 complete baseline discovery patients. Eight factors were stable across five random seeds. F1, F2, F6 and F7 were retained after evidence-matrix prioritization. F1/F2/F6 were interpreted as skin-primary bulk molecular programs, and F7 as a systemic/supportive candidate.

        ## Single-cell and Spatial Contextualization

        Frozen CORE and EXTENDED signatures were scored in single-cell and spatial datasets. CORE results were primary; EXTENDED results were sensitivity checks. Single-cell inference used donor-level or sample-level summaries. Spatial spot/section signals were treated as directional contextual evidence.

        ## Genetic Architecture

        Axis-specific genetic anchoring was tested first and closed with all four programs assigned Tier D. Overall psoriasis susceptibility was then analyzed against frozen comorbidity outcomes using LDSC. Restricted LAVA was applied only to CAD, PsA, Crohn disease and ulcerative colitis after sign/QC adjudication. CAD was the primary systemic target; PsA was a near-neighbor positive control; Crohn disease and ulcerative colitis were retained as QC-flagged IBD targets.

        ## Regulatory Prioritization

        SMR/HEIDI used GTEx v8 eQTL data from outcome-relevant tissues. Coloc was restricted to Tier A shared-locus/eQTL candidates. PP4 >= 0.8 was interpreted as supported colocalization; 0.5 <= PP4 < 0.8 as suggestive; PP3 > PP4 as evidence favoring distinct signals. eQTL MAF proxy inputs are explicitly flagged in the main and supplementary tables.

        ## Missing or Unresolved Inputs

        T2D, MASLD, major depressive disorder and uveitis were prespecified but did not enter the final LDSC result table because frozen primary GWAS access or source resolution was incomplete. They must not be described as null outcomes.
        """
    ).strip()


def build_figure_map() -> str:
    return dedent(
        """
        # Communications Biology Supplementary Figure Map v1

        | Main figure | Current source assets | Status | Notes |
        |---|---|---|---|
        | Figure 1 | `results/figures/Figure1A_study_flow.svg`, `Figure1B_patient_tissue_structure.svg`, `Figure2B_cluster_stability.svg` | needs assembly | Combine study design and failed discrete endotype decision. |
        | Figure 2 | `results/figures/Figure2A_axis_evidence_matrix.svg`, `Figure2B_retained_axis_gene_programs.svg`, `Figure2C_tissue_contribution.svg`, `Figure2D_external_replication_support.svg` | needs assembly | Use F1/F2/F6/F7 only. |
        | Figure 3 | `results/figures/phase2b/Figure3A_GSE228421_axis_celltype_localization.svg`, `Figure3B_GSE228421_donor_paired_effects.svg`; spatial panels from Phase 2C reports | needs assembly | Use donor-level and spatial-context wording. |
        | Figure 4 | `results/figures/phase3a/Figure6A_genetic_anchoring_design.svg`, `Figure6E_evidence_matrix.svg`, `Figure6F_shared_vs_axis_specific.svg` | needs relabeling | Rename as conceptual pivot from axis genetics to overall susceptibility genetics. |
        | Figure 5 | `results/figures/phase4a4b/Figure5_shared_genetic_architecture.svg`, `.tiff`, source data | ready with editorial review | Prefer SVG/TIFF; avoid Cairo PDF as submission source. |
        | Figure 6 | `results/figures/phase4c/Figure_Phase4C_shared_locus_eqtl_prioritization.svg`; `results/figures/phase4d/Figure7_restricted_coloc_contextualization.svg` | needs merge | Merge Phase 4C and legacy Figure 7 into final regulatory/model figure. |

        Submission note: Communications Biology accepts common editable/vector formats, and the journal guidance recommends RGB color, standard fonts such as Arial/Helvetica and >=300 dpi for photographic/raster elements. Final figure export should prefer SVG plus high-resolution TIFF where available.
        """
    ).strip()


def build_audits(table3: list[dict[str, str]]) -> None:
    code_check = dedent(
        """
        # Communications Biology Code Release Checklist

        ## Required before submission

        - [ ] Freeze repository path and public archive target.
        - [ ] Add repository DOI in Code Availability: `[repository DOI to be added before submission]`.
        - [ ] Include scripts for transcriptomic preprocessing, MOFA modeling, single-cell/spatial contextualization, LDSC, LAVA, SMR/HEIDI, coloc and manuscript asset generation.
        - [ ] Include environment files or install logs for R/Python tools.
        - [ ] Include checksums or manifests for raw summary statistics where redistribution is permitted.
        - [ ] Exclude restricted raw GWAS files if licensing prevents redistribution.
        - [ ] Add a README that reproduces the locked phase sequence and prohibited-analysis boundaries.
        - [ ] Include processed result tables used by the manuscript.

        ## Current status

        `NEEDS_CODE_ARCHIVE_BEFORE_SUBMISSION`. The manuscript draft can proceed, but the repository DOI and final code archive are not yet available.
        """
    ).strip()
    write_text(REPORTS / "COMMUNICATIONS_BIOLOGY_CODE_RELEASE_CHECKLIST.md", code_check)

    ref_audit = dedent(
        """
        # Communications Biology Reference Audit

        ## Verified local bibliography

        The local bibliography file `literature/phase4c_reference_targets.bib` contains verified citation metadata for the current manuscript v1. The manuscript uses these references conservatively and does not fabricate additional citations.

        ## References currently used

        - Patrick et al., 2022, Nature Communications, doi:10.1038/s41467-022-34323-4.
        - Dand et al., 2025, Nature Communications, doi:10.1038/s41467-025-56719-8.
        - Stuart et al., 2015, American Journal of Human Genetics, doi:10.1016/j.ajhg.2015.10.019.
        - Ellinghaus et al., 2012, American Journal of Human Genetics, doi:10.1016/j.ajhg.2012.02.020.
        - Li et al., 2013, Annals of the Rheumatic Diseases, doi:10.1136/annrheumdis-2012-202143.
        - Gelfand et al., 2006, JAMA, doi:10.1001/jama.296.14.1735.
        - Werme et al., 2022, Nature Genetics, doi:10.1038/s41588-022-01017-y.
        - Zhu et al., 2016, Nature Genetics, doi:10.1038/ng.3538.
        - GTEx Consortium, 2020, Science, doi:10.1126/science.aaz1776.
        - Giambartolomei et al., 2014, PLoS Genetics, doi:10.1371/journal.pgen.1004383.

        ## Gap

        The current reference set is sufficient for a restrained v1 assembly but is not enough for final Communications Biology submission. A full reference expansion should add dataset accession papers, LDSC source citation, MOFA citation, psoriasis tissue transcriptomics references and any official GWAS source references not already captured.
        """
    ).strip()
    write_text(REPORTS / "CB_REFERENCE_AUDIT.md", ref_audit)

    numeric_rows = [
        {"claim_id": "N001", "claim": "Discrete k=2 endotype min bootstrap Jaccard", "value": "0.562", "source": "reports/PHASE1_ENDOTYPE_GO_NOGO_REPORT.md", "status": "locked"},
        {"claim_id": "N002", "claim": "MOFA complete baseline discovery patients", "value": "76", "source": "reports/PHASE1B_MOLECULAR_AXIS_REPORT.md", "status": "locked"},
        {"claim_id": "N003", "claim": "Stable MOFA factors across seeds", "value": "8 factors across 5 random seeds", "source": "reports/PHASE1B_MOLECULAR_AXIS_REPORT.md", "status": "locked"},
        {"claim_id": "N004", "claim": "F1 GSE244679 paired-skin support", "value": "|rho|=0.688", "source": "reports/PHASE1B_MOLECULAR_AXIS_REPORT.md", "status": "locked"},
        {"claim_id": "N005", "claim": "F2 GSE244679 paired-skin support", "value": "|rho|=0.518", "source": "reports/PHASE1B_MOLECULAR_AXIS_REPORT.md", "status": "locked"},
        {"claim_id": "N006", "claim": "F6 GSE244679 paired-skin support", "value": "|rho|=0.375", "source": "reports/PHASE2A_AXIS_MECHANISM_PRIORITIZATION.md", "status": "locked"},
        {"claim_id": "N007", "claim": "F1 spatial correlations", "value": "GSE225475 rho=0.502309; GSE202011 rho=0.489475", "source": "MECHANISM_FREEZE_V2.md", "status": "locked"},
        {"claim_id": "N008", "claim": "F2 spatial correlations", "value": "GSE225475 rho=0.506033; GSE202011 rho=0.490773", "source": "MECHANISM_FREEZE_V2.md", "status": "locked"},
        {"claim_id": "N009", "claim": "F6 spatial correlations", "value": "GSE225475 rho=0.545790; GSE202011 rho=0.496115", "source": "MECHANISM_FREEZE_V2.md", "status": "locked"},
        {"claim_id": "N010", "claim": "F7 spatial correlations", "value": "GSE225475 rho=0.504906; GSE202011 rho=0.484714", "source": "MECHANISM_FREEZE_V2.md", "status": "locked"},
        {"claim_id": "N011", "claim": "F1/F2/F6/F7 genetic anchoring tier", "value": "all Tier D", "source": "reports/PHASE3A_PSORIASIS_GENETIC_ANCHORING.md", "status": "locked"},
        {"claim_id": "N012", "claim": "CAD LDSC genetic correlation", "value": "rg=0.1732; SE=0.0274; P=2.4979e-10; FDR=7.4937e-10", "source": "results/phase4a/phase4a_ldsc_rg_results.tsv", "status": "locked"},
        {"claim_id": "N013", "claim": "PsA LDSC genetic correlation", "value": "rg=1.1715; SE=0.0751; P=6.7461e-55; FDR=4.04766e-54", "source": "results/phase4a/phase4a_ldsc_rg_results.tsv", "status": "locked"},
        {"claim_id": "N014", "claim": "Crohn disease LDSC genetic correlation", "value": "rg=-0.2717; SE=0.0449; P=1.434e-09; FDR=2.868e-09", "source": "results/phase4a/phase4a_ldsc_rg_results.tsv", "status": "locked"},
        {"claim_id": "N015", "claim": "Ulcerative colitis LDSC genetic correlation", "value": "rg=-0.2233; SE=0.0409; P=4.8195e-08; FDR=7.22925e-08", "source": "results/phase4a/phase4a_ldsc_rg_results.tsv", "status": "locked"},
        {"claim_id": "N016", "claim": "Phase4D coloc supported/suggestive candidates", "value": f"{len(table3)} manuscript candidates", "source": "results/phase4d_coloc/manuscript_tables/phase4d_coloc_supported_and_suggestive_candidates.tsv", "status": "locked"},
        {"claim_id": "N017", "claim": "Phase4E coloc-axis overlap", "value": "no supported/suggestive coloc gene overlapped F1/F2/F6/F7 programs", "source": "results/phase4e_contextualization/phase4e_coloc_axis_overlap_summary.tsv", "status": "locked"},
    ]
    write_tsv(REPORTS / "CB_NUMERIC_CLAIM_AUDIT.tsv", numeric_rows, ["claim_id", "claim", "value", "source", "status"])

    claim_boundary = dedent(
        """
        # Communications Biology Claim Boundary Audit

        ## Allowed central claim

        Reproducible psoriasis tissue molecular heterogeneity and inherited multisystem shared genetic architecture are partially separable biological layers.

        ## Allowed result claims

        - F1, F2 and F6 are skin-primary bulk molecular programs with independent paired-skin replication and directional cellular/spatial support.
        - F7 is a systemic/supportive candidate with low-confidence skin-spatial interpretation.
        - F1/F2/F6/F7 are not genetically anchored molecular endotypes.
        - Overall psoriasis susceptibility shows genome-wide and local shared genetic architecture with selected comorbidities.
        - CAD is the cleanest non-neighbor systemic signal in the completed LDSC analysis.
        - PsA is a positive-control/near-neighbor phenotype.
        - Crohn disease and ulcerative colitis show QC-flagged and directionally heterogeneous architecture.
        - Restricted SMR/HEIDI and coloc prioritize candidate regulatory signals but do not connect them directly to the frozen tissue programs.

        ## Disallowed claims

        - Do not call F1/F2/F6/F7 definitive endotypes.
        - Do not claim axis-specific causality, MR support or independent genetic anchoring.
        - Do not claim T2D, MASLD, MDD or uveitis are null outcomes.
        - Do not claim CAD coloc is high-confidence PP4-supported; current CAD coloc is suggestive only.
        - Do not claim clinical validation, therapeutic readiness or diagnostic utility.
        """
    ).strip()
    write_text(REPORTS / "CB_CLAIM_BOUNDARY_AUDIT.md", claim_boundary)

    gap_audit = dedent(
        """
        # Communications Biology Manuscript Gap Audit

        ## Status

        `NEEDS_TARGETED_MANUSCRIPT_FIXES_BEFORE_SUBMISSION`

        ## Completed in this Phase 6 assembly

        - Main manuscript v1 generated.
        - Supplementary methods v1 generated.
        - Main Tables 1-3 generated as TSV and embedded in the manuscript.
        - Supplementary TSV table collection generated.
        - Figure map generated.
        - Code release, reference, numeric-claim and claim-boundary audits generated.

        ## Remaining author-side inputs

        - Author list, affiliations, author contributions, funding and competing-interest statements.
        - Repository DOI and final public code archive.
        - Final reference expansion beyond the 10 verified core references.
        - Final figure assembly for Figures 1-4 and merged Figure 6; Figure 5 is closest to ready.
        - Optional DOCX conversion after figure/table placement decisions.
        - Journal-specific word count and display-item trim after author review.

        ## Nonblocking project-file issue

        Root `CURRENT_PROJECT_STATUS.md` is absent, but `reports/CURRENT_PROJECT_STATUS_2026-08-17.md` exists and was used as the current dated status file.
        """
    ).strip()
    write_text(REPORTS / "CB_MANUSCRIPT_GAP_AUDIT.md", gap_audit)


def main() -> None:
    for p in [MANUSCRIPT, TABLES, SUPP, REPORTS]:
        p.mkdir(parents=True, exist_ok=True)
    for stale in SUPP.glob("Supplementary_Table_*.tsv"):
        stale.unlink()
    for stale in SUPP.glob("._Supplementary_Table_*.tsv"):
        stale.unlink()
    for stale in SUPP.glob("._supplementary_table_manifest.tsv"):
        stale.unlink()
    table1, table2, table3 = build_tables()
    build_supplementary_tables()
    write_text(MANUSCRIPT / "Communications_Biology_main_manuscript_v1.md", build_main_manuscript(table1, table2, table3))
    write_text(MANUSCRIPT / "Communications_Biology_supplementary_methods_v1.md", build_supp_methods())
    write_text(MANUSCRIPT / "Communications_Biology_supplementary_figure_map.md", build_figure_map())
    build_audits(table3)
    summary = dedent(
        f"""
        # Phase 6 Communications Biology Manuscript Assembly Summary

        Status: `NEEDS_TARGETED_MANUSCRIPT_FIXES_BEFORE_SUBMISSION`

        Generated:

        - `manuscript/Communications_Biology_main_manuscript_v1.md`
        - `manuscript/Communications_Biology_supplementary_methods_v1.md`
        - `manuscript/Communications_Biology_supplementary_figure_map.md`
        - `manuscript/tables/Table1_public_datasets_and_roles.tsv`
        - `manuscript/tables/Table2_molecular_program_interpretation.tsv`
        - `manuscript/tables/Table3_regulatory_prioritization_coloc.tsv`
        - `manuscript/supplementary_tables/` TSV collection
        - `reports/COMMUNICATIONS_BIOLOGY_CODE_RELEASE_CHECKLIST.md`
        - `reports/CB_REFERENCE_AUDIT.md`
        - `reports/CB_NUMERIC_CLAIM_AUDIT.tsv`
        - `reports/CB_CLAIM_BOUNDARY_AUDIT.md`
        - `reports/CB_MANUSCRIPT_GAP_AUDIT.md`
        """
    ).strip()
    write_text(REPORTS / "PHASE6_CB_MANUSCRIPT_ASSEMBLY_SUMMARY.md", summary)


if __name__ == "__main__":
    main()
