suppressPackageStartupMessages({
  library(ggplot2)
  library(patchwork)
  library(dplyr)
  library(readr)
  library(tidyr)
  library(scales)
})

theme_set(
  theme_classic(base_size = 6.2, base_family = "Arial") +
    theme(
      axis.line = element_line(linewidth = 0.28, colour = "black"),
      axis.ticks = element_line(linewidth = 0.28, colour = "black"),
      axis.text = element_text(colour = "black"),
      legend.title = element_text(size = 6.2),
      legend.text = element_text(size = 5.8),
      strip.background = element_blank(),
      strip.text = element_text(size = 6.4, face = "bold"),
      plot.title = element_text(size = 7.0, face = "bold"),
      plot.subtitle = element_text(size = 5.8, colour = "#404040"),
      panel.grid = element_blank()
    )
)

dir.create("results/figures/phase4d/source_data", recursive = TRUE, showWarnings = FALSE)
dir.create("results/figures/phase4d", recursive = TRUE, showWarnings = FALSE)

coloc <- read_tsv(
  "results/phase4d_coloc/manuscript_tables/phase4d_coloc_supported_and_suggestive_candidates.tsv",
  show_col_types = FALSE
)

all_coloc <- read_tsv(
  "results/phase4d_coloc/phase4d_restricted_coloc_tierA_all_results.tsv",
  show_col_types = FALSE
)

overlap <- read_tsv(
  "results/phase4e_contextualization/phase4e_coloc_candidate_axis_program_overlap.tsv",
  show_col_types = FALSE
)

label_outcome <- c(
  cad = "CAD",
  crohn = "Crohn",
  psa = "PsA",
  uc = "UC"
)

tier_labels <- c(
  coloc_supported_PP4_ge_0p8 = "PP4 high",
  suggestive_PP4_0p5_to_0p8 = "PP4 sugg.",
  distinct_signal_PP3_gt_PP4 = "PP3 dominant"
)

outcome_levels <- c("cad", "psa", "crohn", "uc")

coloc_plot <- coloc %>%
  mutate(
    outcome = factor(outcome, levels = outcome_levels, labels = label_outcome[outcome_levels]),
    tier_label = factor(tier_labels[interpretation_tier],
      levels = c("PP4 high", "PP4 sugg.")
    ),
    tissue_short = recode(tissue,
      "Skin_Sun_Exposed_Lower_leg" = "skin-SE",
      "Skin_Not_Sun_Exposed_Suprapubic" = "skin-NSE",
      "Cells_EBV-transformed_lymphocytes" = "LCL",
      "Colon_Transverse" = "colon-trans",
      "Colon_Sigmoid" = "colon-sig",
      "Whole_Blood" = "blood",
      "Spleen" = "spleen",
      .default = tissue
    ),
    display_gene = paste0(gene, " | ", tissue_short),
    display_gene = factor(display_gene, levels = rev(unique(display_gene[order(outcome, PP.H4.abf)])))
  )

write_tsv(coloc_plot, "results/figures/phase4d/source_data/figure7_panel_a_coloc_candidates.tsv")

panel_a <- ggplot(coloc_plot, aes(x = PP.H4.abf, y = display_gene)) +
  geom_vline(xintercept = 0.8, linewidth = 0.35, linetype = "dashed", colour = "#7A7A7A") +
  geom_point(aes(colour = outcome, shape = tier_label), size = 2.2, stroke = 0.45) +
  scale_x_continuous(limits = c(0.48, 1.0), breaks = c(0.5, 0.65, 0.8, 0.95), expand = expansion(mult = c(0, 0.02))) +
  scale_colour_manual(values = c(CAD = "#3E6C9A", PsA = "#7A4E8A", Crohn = "#4F8A6A", UC = "#B36A3C")) +
  scale_shape_manual(values = c("PP4 high" = 16, "PP4 sugg." = 1)) +
  labs(
    title = "A  Restricted eQTL colocalization",
    subtitle = "Only PP4-supported and suggestive candidates are shown",
    x = "Coloc PP4",
    y = NULL,
    colour = "Outcome",
    shape = "Tier"
  ) +
  theme(
    legend.position = "bottom",
    legend.box = "horizontal",
    axis.text.y = element_text(size = 5.2),
    plot.margin = margin(4, 6, 4, 4)
  ) +
  guides(
    colour = guide_legend(nrow = 1, override.aes = list(size = 2.5)),
    shape = guide_legend(nrow = 1)
  )

count_data <- all_coloc %>%
  mutate(
    outcome = factor(outcome, levels = outcome_levels, labels = label_outcome[outcome_levels]),
    tier_label = factor(tier_labels[interpretation_tier],
      levels = c("PP4 high", "PP4 sugg.", "PP3 dominant")
    )
  ) %>%
  count(outcome, tier_label, name = "n")

write_tsv(count_data, "results/figures/phase4d/source_data/figure7_panel_b_tier_counts.tsv")

panel_b <- ggplot(count_data, aes(x = outcome, y = n, fill = tier_label)) +
  geom_col(width = 0.68, colour = "white", linewidth = 0.25) +
  geom_text(aes(label = ifelse(n > 0, n, "")), position = position_stack(vjust = 0.5), size = 2.1, colour = "white") +
  scale_fill_manual(values = c(
    "PP4 high" = "#965A79",
    "PP4 sugg." = "#C58C5C",
    "PP3 dominant" = "#8D9AA6"
  )) +
  labs(
    title = "B  Coloc evidence tiers",
    subtitle = "Most Tier A tests favoured distinct signals",
    x = NULL,
    y = "Gene-tissue pairs",
    fill = "Interpretation"
  ) +
  theme(
    legend.position = "bottom",
    axis.text.x = element_text(size = 6.2),
    plot.margin = margin(4, 4, 4, 6)
  )

overlap_summary <- overlap %>%
  distinct(outcome, gene, tissue, interpretation_tier, axis_overlap_status) %>%
  mutate(
    direct_axis_overlap = axis_overlap_status != "no_overlap_with_F1_F2_F6_F7_programs",
    outcome = factor(outcome, levels = outcome_levels, labels = label_outcome[outcome_levels])
  ) %>%
  group_by(outcome) %>%
  summarise(
    candidates = n(),
    direct_overlaps = sum(direct_axis_overlap),
    .groups = "drop"
  ) %>%
  mutate(
    label = paste0(direct_overlaps, "/", candidates),
    status = ifelse(direct_overlaps == 0, "No direct axis-gene overlap", "Direct overlap detected")
  )

write_tsv(overlap_summary, "results/figures/phase4d/source_data/figure7_panel_c_axis_overlap.tsv")

panel_c <- ggplot(overlap_summary, aes(x = outcome, y = 1, fill = status)) +
  geom_tile(width = 0.86, height = 0.58, colour = "white", linewidth = 0.4) +
  geom_text(aes(label = label), size = 2.4, fontface = "bold", colour = "#303030") +
  scale_fill_manual(values = c("No direct axis-gene overlap" = "#D9DFE5")) +
  scale_y_continuous(limits = c(0.55, 1.45), breaks = NULL) +
  labs(
    title = "C  Axis-program overlap audit",
    subtitle = "Candidates versus frozen F1/F2/F6/F7 programs",
    x = NULL,
    y = NULL,
    fill = NULL
  ) +
  theme(
    legend.position = "bottom",
    axis.line = element_blank(),
    axis.ticks = element_blank(),
    axis.text.x = element_text(size = 6.2),
    plot.margin = margin(4, 4, 4, 6)
  )

panel_note <- ggplot() +
  annotate(
    "text",
    x = 0,
    y = 1,
    hjust = 0,
    vjust = 1,
    size = 1.95,
    lineheight = 1.05,
    label = paste(
      "Interpretation:",
      "PsA validates the coloc workflow.",
      "UC has a colon-specific",
      "sensitivity-labelled candidate.",
      "CAD remains architecture-level.",
      "F1/F2/F6/F7 are contextual",
      "layers, not genetic exposures.",
      sep = "\n"
    )
  ) +
  coord_cartesian(xlim = c(0, 1), ylim = c(0, 1), clip = "off") +
  theme_void(base_family = "Arial") +
  theme(plot.margin = margin(4, 4, 4, 6))

combined <- panel_a | ((panel_b / panel_c / panel_note) + plot_layout(heights = c(1.0, 0.58, 0.62)))
combined <- combined + plot_layout(widths = c(1.25, 1))

base <- "results/figures/phase4d/Figure7_restricted_coloc_contextualization"

svglite::svglite(paste0(base, ".svg"), width = 183 / 25.4, height = 130 / 25.4)
print(combined)
dev.off()

grDevices::cairo_pdf(paste0(base, ".pdf"), width = 183 / 25.4, height = 130 / 25.4, family = "Arial")
print(combined)
dev.off()

ragg::agg_png(paste0(base, ".png"), width = 183 / 25.4, height = 130 / 25.4, units = "in", res = 600)
print(combined)
dev.off()

ragg::agg_tiff(paste0(base, ".tiff"), width = 183 / 25.4, height = 130 / 25.4, units = "in", res = 600, compression = "lzw")
print(combined)
dev.off()

qa <- tibble::tibble(
  figure = "Figure7_restricted_coloc_contextualization",
  width_mm = 183,
  height_mm = 130,
  backend = "R ggplot2 patchwork",
  n_displayed_candidates = nrow(coloc_plot),
  n_all_tests = nrow(all_coloc),
  n_direct_axis_program_overlaps = sum(overlap_summary$direct_overlaps),
  conclusion = "Restricted coloc separates shared local architecture from PP4-supported eQTL signals; no direct F1/F2/F6/F7 gene-program overlap among PP4-supported/suggestive candidates."
)
write_tsv(qa, "results/figures/phase4d/Figure7_restricted_coloc_contextualization_QA.tsv")
