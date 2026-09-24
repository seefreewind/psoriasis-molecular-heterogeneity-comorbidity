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
      legend.title = element_text(size = 6.1),
      legend.text = element_text(size = 5.7),
      strip.background = element_blank(),
      strip.text = element_text(size = 6.2, face = "bold"),
      plot.title = element_text(size = 7.0, face = "bold"),
      plot.subtitle = element_text(size = 5.8, colour = "#404040"),
      panel.grid = element_blank()
    )
)

dir.create("results/figures/phase4a4b/source_data", recursive = TRUE, showWarnings = FALSE)
dir.create("results/figures/phase4a4b", recursive = TRUE, showWarnings = FALSE)

rg <- read_tsv("results/phase4a/phase4a_ldsc_rg_results.tsv", show_col_types = FALSE)
lava_summary <- read_tsv("results/phase4b_restricted_lava/phase4b_restricted_lava_summary.tsv", show_col_types = FALSE)
lava <- read_tsv("results/phase4b_restricted_lava/phase4b_restricted_lava_bivariate.tsv", show_col_types = FALSE)

outcome_map <- c(
  "Coronary artery disease" = "CAD",
  "Psoriatic arthritis" = "PsA",
  "Crohn disease" = "Crohn",
  "Ulcerative colitis" = "UC",
  "Ischemic stroke" = "Stroke",
  "Chronic kidney disease" = "CKD"
)

lava_outcome_map <- c(cad = "CAD", psa = "PsA", crohn = "Crohn", uc = "UC")

rg_plot <- rg %>%
  mutate(
    outcome_label = recode(Outcome, !!!outcome_map),
    ci_low = rg - 1.96 * SE,
    ci_high = rg + 1.96 * SE,
    fdr_sig = FDR < 0.05,
    qc_group = case_when(
      QC_status == "PASS" ~ "PASS",
      grepl("NEAR_NEIGHBOR", QC_status) ~ "Near-neighbor/QC label",
      TRUE ~ "QC label"
    ),
    outcome_label = factor(outcome_label, levels = rev(c("PsA", "Crohn", "UC", "CAD", "Stroke", "CKD")))
  )

write_tsv(rg_plot, "results/figures/phase4a4b/source_data/figure5_panel_a_ldsc_rg.tsv")

panel_a <- ggplot(rg_plot, aes(x = rg, y = outcome_label)) +
  geom_vline(xintercept = 0, linewidth = 0.3, colour = "#8A8A8A") +
  geom_errorbar(aes(xmin = ci_low, xmax = ci_high, colour = qc_group), orientation = "y", width = 0.18, linewidth = 0.42) +
  geom_point(aes(fill = fdr_sig, colour = qc_group), shape = 21, size = 2.25, stroke = 0.5) +
  scale_colour_manual(values = c("PASS" = "#355C7D", "QC label" = "#8E6C42", "Near-neighbor/QC label" = "#7B4F8A")) +
  scale_fill_manual(values = c(`TRUE` = "white", `FALSE` = "#D8DDE3"), labels = c(`TRUE` = "FDR < 0.05", `FALSE` = "FDR >= 0.05")) +
  labs(
    title = "A  Genome-wide genetic correlation",
    subtitle = "Overall psoriasis susceptibility versus frozen outcomes",
    x = "LDSC rg (95% CI)",
    y = NULL,
    colour = "QC",
    fill = "Genome-wide"
  ) +
  theme(
    legend.position = "bottom",
    legend.box = "vertical",
    axis.text.y = element_text(size = 5.8),
    plot.margin = margin(4, 5, 4, 4)
  )

lava_counts <- lava_summary %>%
  mutate(
    outcome_label = factor(recode(outcome, !!!lava_outcome_map), levels = c("CAD", "PsA", "Crohn", "UC"))
  ) %>%
  select(outcome_label, nominal_positive, nominal_negative, fdr05_all_tests) %>%
  pivot_longer(c(nominal_positive, nominal_negative, fdr05_all_tests), names_to = "metric", values_to = "n") %>%
  mutate(metric = recode(metric,
    nominal_positive = "Nominal positive",
    nominal_negative = "Nominal negative",
    fdr05_all_tests = "FDR-supported"
  ))

write_tsv(lava_counts, "results/figures/phase4a4b/source_data/figure5_panel_b_lava_counts.tsv")

panel_b <- ggplot(lava_counts, aes(x = outcome_label, y = n, fill = metric)) +
  geom_col(position = position_dodge(width = 0.72), width = 0.64, colour = "white", linewidth = 0.2) +
  scale_fill_manual(values = c(
    "FDR-supported" = "#5D7890",
    "Nominal positive" = "#A56A43",
    "Nominal negative" = "#6B7A8C"
  )) +
  labs(
    title = "B  Restricted LAVA local architecture",
    subtitle = "Local signal counts after joint local h2 screening",
    x = NULL,
    y = "Loci",
    fill = NULL
  ) +
  theme(
    legend.position = "bottom",
    axis.text.x = element_text(size = 6),
    plot.margin = margin(4, 4, 4, 6)
  )

selected_loci <- lava %>%
  filter(fdr_all_tests < 0.05) %>%
  group_by(outcome) %>%
  slice_min(order_by = p, n = 5, with_ties = FALSE) %>%
  ungroup() %>%
  pull(locus) %>%
  unique()

selected_loci <- union(selected_loci, c(57, 347, 887, 908, 1215, 1841))

heat <- lava %>%
  filter(locus %in% selected_loci) %>%
  mutate(
    outcome_label = factor(recode(outcome, !!!lava_outcome_map), levels = c("CAD", "PsA", "Crohn", "UC")),
    locus_label = paste0("L", locus, " chr", chr, ":", round(start / 1e6, 1), "-", round(stop / 1e6, 1), "Mb"),
    locus_label = factor(locus_label, levels = rev(unique(locus_label[order(chr, start, locus)]))),
    show_text = ifelse(fdr_all_tests < 0.05, sprintf("%.2f", rho), "")
  )

write_tsv(heat, "results/figures/phase4a4b/source_data/figure5_panel_c_selected_lava_loci.tsv")

panel_c <- ggplot(heat, aes(x = outcome_label, y = locus_label, fill = rho)) +
  geom_tile(colour = "white", linewidth = 0.25) +
  geom_text(aes(label = show_text), size = 1.9, colour = "black") +
  scale_fill_gradient2(
    low = "#4E7396",
    mid = "#F2F2F2",
    high = "#B46A44",
    midpoint = 0,
    limits = c(-1, 1),
    oob = squish
  ) +
  labs(
    title = "C  Directional local rg heterogeneity",
    subtitle = "Selected FDR-supported and pre-specified key loci",
    x = NULL,
    y = NULL,
    fill = "Local rho"
  ) +
  theme(
    legend.position = "bottom",
    axis.text.y = element_text(size = 5.2),
    axis.text.x = element_text(size = 6),
    plot.margin = margin(4, 4, 4, 6)
  )

combined <- (panel_a | panel_b) / panel_c + plot_layout(heights = c(1, 1.25), widths = c(1.05, 1))

base <- "results/figures/phase4a4b/Figure5_shared_genetic_architecture"

svglite::svglite(paste0(base, ".svg"), width = 183 / 25.4, height = 145 / 25.4)
print(combined)
dev.off()

grDevices::cairo_pdf(paste0(base, ".pdf"), width = 183 / 25.4, height = 145 / 25.4, family = "Arial")
print(combined)
dev.off()

ragg::agg_png(paste0(base, ".png"), width = 183 / 25.4, height = 145 / 25.4, units = "in", res = 600)
print(combined)
dev.off()

ragg::agg_tiff(paste0(base, ".tiff"), width = 183 / 25.4, height = 145 / 25.4, units = "in", res = 600, compression = "lzw")
print(combined)
dev.off()

qa <- tibble::tibble(
  figure = "Figure5_shared_genetic_architecture",
  width_mm = 183,
  height_mm = 145,
  backend = "R ggplot2 patchwork",
  n_ldsc_outcomes = nrow(rg_plot),
  n_lava_outcomes = n_distinct(lava_summary$outcome),
  n_selected_loci = length(selected_loci),
  conclusion = "Overall psoriasis susceptibility shows selected comorbidity-level sharing; restricted LAVA reveals CAD positive local architecture, PsA positive-control sharing, and IBD directional heterogeneity."
)
write_tsv(qa, "results/figures/phase4a4b/Figure5_shared_genetic_architecture_QA.tsv")
