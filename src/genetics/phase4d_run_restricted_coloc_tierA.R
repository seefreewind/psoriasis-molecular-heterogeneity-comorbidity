#!/usr/bin/env Rscript
suppressPackageStartupMessages({
  library(data.table)
  library(coloc)
})

root <- normalizePath(getwd())
outdir <- file.path(root, "results", "phase4d_coloc")
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)

eqtl_cols <- c(
  "variant", "r2", "pvalue", "molecular_trait_object_id",
  "molecular_trait_id", "maf", "gene_id", "median_tpm",
  "beta", "se", "an", "ac", "chromosome", "position",
  "ref", "alt", "type", "rsid"
)

fetch_eqtl <- function(ftp_path, region, selected_gene_id) {
  cmd <- sprintf("tabix %s %s", shQuote(ftp_path), shQuote(region))
  raw <- suppressWarnings(system(cmd, intern = TRUE))
  if (!length(raw)) return(data.table())
  dt <- fread(text = paste(raw, collapse = "\n"), header = FALSE, col.names = eqtl_cols)
  dt <- dt[gene_id == selected_gene_id & type == "SNP" & !is.na(se) & !is.na(beta) & !is.na(maf)]
  dt <- dt[!is.na(rsid) & rsid != "" & rsid != "NA"]
  dt[, coord_key := paste(chromosome, position, sep = ":")]
  unique(dt, by = c("rsid", "ref", "alt"))
}

prep_gwas <- function(path, trait_name, locus_id) {
  lifted_path <- file.path(
    root, "results", "phase4d_coloc", "gwas_loci_hg38",
    sprintf("%s_phase4c_locus_raw.hg38.tsv.gz", trait_name)
  )
  if (file.exists(lifted_path)) {
    path <- lifted_path
  }
  dt <- fread(cmd = paste("gzip -dc", shQuote(path)))
  dt <- dt[trait == trait_name & locus == locus_id]
  dt <- dt[!is.na(beta) & !is.na(se)]
  if ("liftover_status" %in% names(dt)) {
    dt <- dt[liftover_status == "PASS"]
  }
  dt[, has_rsid := !is.na(rsid) & rsid != "" & rsid != "NA"]
  if (sum(dt$has_rsid) >= 50) {
    dt <- dt[has_rsid == TRUE]
    dt[, match_key := rsid]
    dt[, match_mode := "rsid"]
  } else {
    chr_col <- if ("hg38_chr" %in% names(dt)) "hg38_chr" else "chr"
    bp_col <- if ("hg38_bp" %in% names(dt)) "hg38_bp" else "bp"
    dt <- dt[!is.na(get(chr_col)) & as.character(get(chr_col)) != "" & !is.na(get(bp_col)) & as.character(get(bp_col)) != ""]
    dt[, match_key := paste(as.character(get(chr_col)), as.character(get(bp_col)), sep = ":")]
    dt[, match_mode := "hg38_coord"]
  }
  unique(dt, by = c("match_key", "effect_allele", "other_allele"))
}

get_query_region <- function(outcome, locus_id, chr, start, stop) {
  lifted_path <- file.path(
    root, "results", "phase4d_coloc", "gwas_loci_hg38",
    sprintf("%s_phase4c_locus_raw.hg38.tsv.gz", outcome)
  )
  if (!file.exists(lifted_path)) {
    return(sprintf("%s:%s-%s", chr, start, stop))
  }
  dt <- fread(cmd = paste("gzip -dc", shQuote(lifted_path)), select = c("trait", "locus", "hg38_chr", "hg38_bp", "liftover_status"))
  dt <- dt[trait == outcome & locus == locus_id & liftover_status == "PASS"]
  if (!nrow(dt)) {
    return(sprintf("%s:%s-%s", chr, start, stop))
  }
  qchr <- dt$hg38_chr[which.max(tabulate(match(dt$hg38_chr, unique(dt$hg38_chr))))]
  dt <- dt[hg38_chr == qchr]
  sprintf("%s:%s-%s", qchr, min(as.integer(dt$hg38_bp), na.rm = TRUE), max(as.integer(dt$hg38_bp), na.rm = TRUE))
}

align_to_eqtl_alt <- function(gwas, eqtl) {
  mode <- gwas$match_mode[1]
  if (identical(mode, "rsid")) {
    eqtl[, match_key := rsid]
  } else {
    eqtl[, match_key := coord_key]
  }
  m <- merge(gwas, eqtl, by = "match_key", suffixes = c("_gwas", "_eqtl"))
  m <- m[
    (effect_allele == alt & other_allele == ref) |
      (effect_allele == ref & other_allele == alt)
  ]
  if (!nrow(m)) return(m)
  m[, beta_aligned := fifelse(effect_allele == alt, beta_gwas, -beta_gwas)]
  if ("eaf" %in% names(m) && any(!is.na(m$eaf))) {
    m[, eaf_aligned := fifelse(effect_allele == alt, eaf, 1 - eaf)]
    m[, maf_gwas := pmin(eaf_aligned, 1 - eaf_aligned)]
    m[, maf_source := "gwas_eaf"]
  } else {
    m[, maf_gwas := maf]
    m[, maf_source := "eqtl_maf_proxy"]
  }
  m <- m[maf_gwas > 0 & maf_gwas < 0.5 & maf > 0 & maf < 0.5]
  m[, coloc_snp := match_key]
  unique(m, by = "coloc_snp")
}

run_one <- function(row, paths, meta) {
  outcome <- row$outcome
  tissue <- row$tissue
  gene <- row$gene
  gene_id <- row$probeID
  locus <- row$locus
  region <- get_query_region(outcome, locus, row$chr, row$start, row$stop)
  ftp <- paths[qtl_group == tissue, ftp_path][1]
  gwas_path <- file.path(root, "results", "phase4c_preparation", "gwas_loci", sprintf("%s_phase4c_locus_raw.tsv.gz", outcome))
  trait_meta <- meta[phenotype == outcome][1]

  eqtl <- fetch_eqtl(ftp, region, gene_id)
  gwas <- prep_gwas(gwas_path, outcome, locus)
  merged <- align_to_eqtl_alt(gwas, eqtl)

  base <- data.table(
    outcome = outcome,
    tissue = tissue,
    gene = gene,
    gene_id = gene_id,
    locus = locus,
    region = region,
    phase4br_tier = row$phase4br_tier,
    local_direction_group = row$local_direction_group,
    phase4c_eqtl_gene_tier = row$phase4c_eqtl_gene_tier,
    n_eqtl_variants = nrow(eqtl),
    n_gwas_variants = nrow(gwas),
    n_matched_variants = nrow(merged),
    nsnps = nrow(merged),
    gwas_n = trait_meta$total_n,
    gwas_case_fraction = trait_meta$case_fraction,
    eqtl_n = if (nrow(merged)) median(merged$an, na.rm = TRUE) / 2 else NA_real_
  )
  base[, maf_source := if (nrow(merged) && "maf_source" %in% names(merged)) merged$maf_source[1] else NA_character_]

  if (nrow(merged) < 50) {
    base[, `:=`(
      status = "LOW_OVERLAP_FAIL",
      PP.H0.abf = NA_real_, PP.H1.abf = NA_real_, PP.H2.abf = NA_real_,
      PP.H3.abf = NA_real_, PP.H4.abf = NA_real_,
      note = "Fewer than 50 matched variants after rsID and allele alignment."
    )]
    return(base)
  }

  d1 <- list(
    beta = merged$beta_aligned,
    varbeta = merged$se_gwas^2,
    snp = merged$coloc_snp,
    MAF = merged$maf_gwas,
    N = trait_meta$total_n,
    s = trait_meta$case_fraction,
    type = "cc"
  )
  d2 <- list(
    beta = merged$beta_eqtl,
    varbeta = merged$se_eqtl^2,
    snp = merged$coloc_snp,
    MAF = merged$maf,
    N = median(merged$an, na.rm = TRUE) / 2,
    type = "quant"
  )

  coloc_res <- tryCatch(coloc.abf(d1, d2), error = function(e) e)
  if (inherits(coloc_res, "error")) {
    base[, `:=`(
      status = "COLOC_ERROR",
      PP.H0.abf = NA_real_, PP.H1.abf = NA_real_, PP.H2.abf = NA_real_,
      PP.H3.abf = NA_real_, PP.H4.abf = NA_real_,
      note = coloc_res$message
    )]
    return(base)
  }

  s <- as.list(coloc_res$summary)
  base[, `:=`(
    status = "PASS",
    PP.H0.abf = as.numeric(s$PP.H0.abf),
    PP.H1.abf = as.numeric(s$PP.H1.abf),
    PP.H2.abf = as.numeric(s$PP.H2.abf),
    PP.H3.abf = as.numeric(s$PP.H3.abf),
    PP.H4.abf = as.numeric(s$PP.H4.abf),
    note = "Restricted coloc completed."
  )]
  base[]
}

args <- commandArgs(trailingOnly = TRUE)
outcome_filter <- if (length(args) >= 1) args[1] else "cad"
tier_filter <- if (length(args) >= 2) args[2] else "A_local_Tier1_recurrent_SMR2"

candidate <- fread(file.path(root, "results", "phase4d_coloc", "phase4d_coloc_input_feasibility_by_candidate_tissue.tsv"))
candidate <- candidate[outcome == outcome_filter & phase4c_eqtl_gene_tier == tier_filter]
paths <- fread(file.path(outdir, "tabix_ftp_paths_imported.tsv"))
meta <- fread(file.path(outdir, "phase4d_gwas_binary_trait_metadata.tsv"))

res <- rbindlist(lapply(seq_len(nrow(candidate)), function(i) {
  message(sprintf("[%s/%s] %s %s %s", i, nrow(candidate), candidate$gene[i], candidate$tissue[i], candidate$locus[i]))
  run_one(candidate[i], paths, meta)
}), fill = TRUE)

res[, interpretation_tier := fifelse(
  status != "PASS", "input_or_runtime_fail",
  fifelse(PP.H4.abf >= 0.8, "coloc_supported_PP4_ge_0p8",
    fifelse(PP.H4.abf >= 0.5, "suggestive_PP4_0p5_to_0p8",
      fifelse(PP.H3.abf > PP.H4.abf, "distinct_signal_PP3_gt_PP4", "not_coloc_supported")
    )
  )
)]

outfile <- file.path(outdir, sprintf("phase4d_restricted_coloc_%s_tierA_results.tsv", outcome_filter))
fwrite(res, outfile, sep = "\t")
print(res[order(-PP.H4.abf)][, .(outcome, gene, tissue, locus, n_matched_variants, PP.H3.abf, PP.H4.abf, interpretation_tier)])
