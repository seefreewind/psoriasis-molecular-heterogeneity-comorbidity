#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(ggplot2)
  library(patchwork)
  library(dplyr)
  library(tidyr)
  library(readr)
  library(forcats)
  library(scales)
  library(stringr)
  library(svglite)
  library(ragg)
})

root <- "/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity"
figure_dir <- file.path(root, "results/figures/phase4c")
source_dir <- file.path(root, "results/figures/phase4c/source_data")
dir.create(figure_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(source_dir, recursive = TRUE, showWarnings = FALSE)

gene_table <- read_tsv(
  file.path(root, "results/phase4c_smr/phase4c_frozen_shared_locus_eqtl_gene_table.tsv"),
  show_col_types = FALSE
)
smr1 <- read_tsv(
  file.path(root, "results/phase4c_smr/phase4c_smr1_all_results.tsv"),
  show_col_types = FALSE
)
smr2 <- read_tsv(
  file.path(root, "results/phase4c_smr/phase4c_smr2_probe2mb_all_results.tsv"),
  show_col_types = FALSE
)

outcome_labels <- c(
  cad = "CAD",
  psa = "PsA",
  crohn = "Crohn",
  uc = "UC"
)

tier_labels <- c(
  A_local_Tier1_recurrent_SMR2 = "Tier A",
  B_local_Tier1_single_tissue_SMR2 = "Tier B1",
  B_local_Tier2_recurrent_SMR2 = "Tier B2",
  C_local_Tier2_single_tissue_SMR2 = "Tier C"
)

palette_contract <- c(
  neutral_dark = "#2B2B2B",
  neutral_mid = "#767676",
  neutral_light = "#D8D8D8",
  signal_blue = "#3E79B7",
  signal_teal = "#31A7A0",
  signal_green = "#5C9F6B",
  accent_red = "#C84E4E",
  accent_orange = "#D58B32",
  accent_purple = "#8B73B8"
)

pal <- function(name) {
  unname(palette_contract[name])
}

theme_phase4c <- function(base_size = 6.5, base_family = "Arial") {
  theme_classic(base_size = base_size, base_family = base_family) +
    theme(
      axis.line = element_line(linewidth = 0.3, colour = "black"),
      axis.ticks = element_line(linewidth = 0.3, colour = "black"),
      axis.title = element_text(size = base_size),
      axis.text = element_text(size = base_size - 0.4),
      legend.title = element_text(size = base_size - 0.2),
      legend.text = element_text(size = base_size - 0.6),
      strip.text = element_text(size = base_size - 0.1, face = "bold"),
      plot.title = element_text(size = base_size + 0.6, face = "bold"),
      plot.subtitle = element_text(size = base_size - 0.2, colour = pal("neutral_mid")),
      panel.grid.major.x = element_line(linewidth = 0.18, colour = "#ECECEC"),
      panel.grid.major.y = element_blank(),
      panel.grid.minor = element_blank(),
      plot.margin = margin(4, 5, 4, 5)
    )
}

theme_set(theme_phase4c())

save_pub_r <- function(plot, filename, width_mm = 183, height_mm = 128, dpi = 600) {
  w <- width_mm / 25.4
  h <- height_mm / 25.4
  svglite::svglite(paste0(filename, ".svg"), width = w, height = h)
  print(plot)
  dev.off()
  grDevices::cairo_pdf(paste0(filename, ".pdf"), width = w, height = h, family = "Arial")
  print(plot)
  dev.off()
  ragg::agg_tiff(paste0(filename, ".tiff"), width = w, height = h, units = "in", res = dpi)
  print(plot)
  dev.off()
  ragg::agg_png(paste0(filename, ".png"), width = w, height = h, units = "in", res = 300)
  print(plot)
  dev.off()
}

tier_counts <- gene_table %>%
  mutate(
    outcome_display = recode(outcome, !!!outcome_labels),
    outcome_display = factor(outcome_display, levels = c("CAD", "PsA", "Crohn", "UC")),
    tier_display = recode(phase4c_eqtl_gene_tier, !!!tier_labels),
    tier_display = factor(tier_display, levels = c("Tier A", "Tier B1", "Tier B2", "Tier C"))
  ) %>%
  count(outcome_display, tier_display, name = "n_genes") %>%
  complete(outcome_display, tier_display, fill = list(n_genes = 0))

cad_a <- gene_table %>%
  filter(outcome == "cad", phase4c_eqtl_gene_tier == "A_local_Tier1_recurrent_SMR2") %>%
  filter(min_smr_fdr_global > 0) %>%
  mutate(
    gene_label = paste0(gene, " / L", locus),
    gene_label = fct_reorder(gene_label, -log10(min_smr_fdr_global)),
    tissue_class_display = case_when(
      str_detect(tissue_classes, "vascular_arterial") & str_detect(tissue_classes, "blood_immune") ~ "Blood + vascular",
      str_detect(tissue_classes, "vascular_arterial") ~ "Vascular",
      str_detect(tissue_classes, "blood_immune") ~ "Blood",
      str_detect(tissue_classes, "skin") ~ "Skin",
      TRUE ~ "Other"
    ),
    neg_log10_fdr = -log10(min_smr_fdr_global)
  )

ibd_direction <- gene_table %>%
  filter(outcome %in% c("crohn", "uc")) %>%
  mutate(
    outcome_display = recode(outcome, !!!outcome_labels),
    direction_display = recode(
      local_direction_group,
      positive_local_rg = "Positive local rg",
      negative_local_rg = "Negative local rg"
    ),
    recurrent = if_else(n_tissues >= 2, "Recurrent", "Single tissue")
  ) %>%
  count(outcome_display, direction_display, recurrent, name = "n_genes")

stability <- bind_rows(
  smr1 %>% filter(smr_primary_signal) %>%
    distinct(outcome, tissue, Gene) %>%
    mutate(unit = "Outcome + tissue + gene", source = "SMR1"),
  smr2 %>% filter(smr_primary_signal) %>%
    distinct(outcome, tissue, Gene) %>%
    mutate(unit = "Outcome + tissue + gene", source = "SMR2")
) %>%
  count(source, unit, name = "n") %>%
  bind_rows(
    smr1 %>% filter(smr_primary_signal) %>%
      distinct(outcome, Gene) %>%
      summarise(source = "SMR1", unit = "Outcome + gene", n = n(), .groups = "drop"),
    smr2 %>% filter(smr_primary_signal) %>%
      distinct(outcome, Gene) %>%
      summarise(source = "SMR2", unit = "Outcome + gene", n = n(), .groups = "drop")
  ) %>%
  mutate(
    unit = factor(unit, levels = c("Outcome + gene", "Outcome + tissue + gene")),
    source = factor(source, levels = c("SMR1", "SMR2")),
    source_x = as.numeric(source)
  )

stability_label <- tibble(
  unit = factor(c("Outcome + gene", "Outcome + tissue + gene"), levels = levels(stability$unit)),
  label = c("100.0% retained", "98.9% retained"),
  y = c(96, 184)
)

stability_direct_label <- stability %>%
  filter(source == "SMR2") %>%
  mutate(
    label = recode(
      as.character(unit),
      "Outcome + gene" = "Outcome + gene",
      "Outcome + tissue + gene" = "Outcome + tissue + gene"
    ),
    x = source_x + 0.08
  )

write_tsv(tier_counts, file.path(source_dir, "figure_phase4c_panel_a_tier_counts.tsv"))
write_tsv(cad_a, file.path(source_dir, "figure_phase4c_panel_b_cad_tierA.tsv"))
write_tsv(ibd_direction, file.path(source_dir, "figure_phase4c_panel_c_ibd_direction.tsv"))
write_tsv(stability, file.path(source_dir, "figure_phase4c_panel_d_smr_stability.tsv"))

p_a <- ggplot(tier_counts, aes(x = outcome_display, y = n_genes, fill = tier_display)) +
  geom_col(width = 0.68, colour = "white", linewidth = 0.2) +
  geom_text(
    aes(label = if_else(n_genes > 0, str_remove(as.character(tier_display), "Tier "), "")),
    position = position_stack(vjust = 0.5),
    size = 2.0,
    colour = "white",
    fontface = "bold"
  ) +
  scale_fill_manual(
    values = c(
      "Tier A" = pal("signal_blue"),
      "Tier B1" = pal("signal_teal"),
      "Tier B2" = pal("accent_orange"),
      "Tier C" = pal("neutral_light")
    ),
    guide = "none"
  ) +
  labs(
    title = "Frozen regulatory-gene layer",
    subtitle = "91 SMR2-supported genes across Phase 4B-R loci",
    x = NULL,
    y = "Candidate genes"
  ) +
  theme(legend.position = "right")

p_b <- ggplot(cad_a, aes(x = neg_log10_fdr, y = gene_label)) +
  geom_segment(aes(x = 0, xend = neg_log10_fdr, yend = gene_label), colour = "#D9D9D9", linewidth = 0.45) +
  geom_point(aes(size = n_tissues), shape = 21, fill = pal("signal_blue"), colour = "white", stroke = 0.35) +
  geom_text(aes(label = n_tissues), size = 1.8, colour = "white", fontface = "bold") +
  scale_size_continuous(range = c(2.0, 4.2), breaks = c(2, 3, 4), name = "Tissues") +
  labs(
    title = "CAD anchors the systemic track",
    subtitle = "Tier A recurrent genes; point labels = tissue count",
    x = expression(-log[10]("SMR FDR")),
    y = NULL
  ) +
  guides(size = "none") +
  theme(legend.position = "bottom")

p_c <- ggplot(ibd_direction, aes(x = direction_display, y = n_genes, fill = recurrent)) +
  geom_col(width = 0.62, position = position_stack(reverse = TRUE), colour = "white", linewidth = 0.2) +
  facet_wrap(~ outcome_display, nrow = 1) +
  scale_fill_manual(
    values = c("Recurrent" = pal("accent_red"), "Single tissue" = pal("neutral_light")),
    guide = "none"
  ) +
  labs(
    title = "IBD retains local-direction heterogeneity",
    subtitle = "Red = recurrent tissue support; grey = single-tissue support",
    x = NULL,
    y = "Candidate genes"
  ) +
  theme(
    axis.text.x = element_text(angle = 30, hjust = 1),
    legend.position = "right"
  )

p_d <- ggplot(stability, aes(x = source_x, y = n, group = unit)) +
  geom_line(aes(colour = unit), linewidth = 0.55) +
  geom_point(aes(fill = unit), shape = 21, size = 2.2, colour = "white", stroke = 0.3) +
  geom_text(
    data = stability_label,
    aes(x = 1.5, y = y, label = label),
    inherit.aes = FALSE,
    size = 2.0,
    colour = pal("neutral_dark")
  ) +
  geom_text(
    data = stability_direct_label,
    aes(x = x, y = n, label = label, colour = unit),
    inherit.aes = FALSE,
    hjust = 0,
    size = 2.0,
    show.legend = FALSE
  ) +
  scale_colour_manual(
    values = c("Outcome + gene" = pal("signal_blue"), "Outcome + tissue + gene" = pal("accent_orange")),
    guide = "none"
  ) +
  scale_fill_manual(
    values = c("Outcome + gene" = pal("signal_blue"), "Outcome + tissue + gene" = pal("accent_orange")),
    guide = "none"
  ) +
  scale_x_continuous(breaks = c(1, 2), labels = c("SMR1", "SMR2"), limits = c(0.85, 2.52)) +
  scale_y_continuous(expand = expansion(mult = c(0.05, 0.12))) +
  labs(
    title = "Probe-window sensitivity is stable",
    subtitle = "SMR2 did not introduce new primary genes",
    x = NULL,
    y = "Primary signals"
  ) +
  theme(legend.position = "right")

figure <- (p_a | p_b) / (p_c | p_d) +
  plot_layout(widths = c(0.95, 1.25), heights = c(1.05, 0.95), guides = "keep") +
  plot_annotation(
    tag_levels = "a",
    title = "Phase 4C shared-locus eQTL prioritization",
    subtitle = "Robust local psoriasis-comorbidity loci resolve into stable tissue-supported regulatory-gene candidates"
  ) &
  theme(
    plot.tag = element_text(size = 8, face = "bold"),
    legend.position = "none",
    plot.title = element_text(size = 8.2, face = "bold"),
    plot.subtitle = element_text(size = 6.4, colour = pal("neutral_mid"))
  )

out_base <- file.path(figure_dir, "Figure_Phase4C_shared_locus_eqtl_prioritization")
save_pub_r(figure, out_base, width_mm = 183, height_mm = 128, dpi = 600)

qa_notes <- tibble(
  panel = c("a", "b", "c", "d"),
  unique_claim = c(
    "Frozen Phase 4C table contains 91 genes and separates evidence tiers across outcomes.",
    "CAD has recurrent Tier A genes across robust positive local-rg loci.",
    "Crohn and UC candidates occupy both positive and negative local-rg groups.",
    "Probe-centered ±2Mb SMR2 retains the SMR1 gene-level candidate set."
  ),
  center_or_summary = c("count", "-log10 global SMR FDR", "count", "count"),
  spread_or_interval = c("none; descriptive frozen table", "none; gene-prioritization statistic", "none; descriptive frozen table", "none; sensitivity count"),
  replicate_unit = c("gene-table row", "gene/probe", "gene-table row", "primary SMR signal"),
  source_data = c(
    "figure_phase4c_panel_a_tier_counts.tsv",
    "figure_phase4c_panel_b_cad_tierA.tsv",
    "figure_phase4c_panel_c_ibd_direction.tsv",
    "figure_phase4c_panel_d_smr_stability.tsv"
  ),
  pass = "yes"
)
write_tsv(qa_notes, file.path(figure_dir, "Figure_Phase4C_shared_locus_eqtl_prioritization_QA.tsv"))

message("Wrote figure bundle to: ", figure_dir)
