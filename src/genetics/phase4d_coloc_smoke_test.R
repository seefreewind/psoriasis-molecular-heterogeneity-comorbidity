#!/usr/bin/env Rscript
suppressPackageStartupMessages({
  library(data.table)
  library(coloc)
})

root <- normalizePath(getwd())
outdir <- file.path(root, "results", "phase4d_coloc")
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)

fetch_eqtl <- function(ftp_path, region, selected_gene_id) {
  cmd <- sprintf("tabix %s %s", shQuote(ftp_path), shQuote(region))
  raw <- suppressWarnings(system(cmd, intern = TRUE))
  if (!length(raw)) {
    return(data.table())
  }
  dt <- fread(
    text = paste(raw, collapse = "\n"),
    header = FALSE,
    col.names = c(
      "variant", "r2", "pvalue", "molecular_trait_object_id",
      "molecular_trait_id", "maf", "gene_id", "median_tpm",
      "beta", "se", "an", "ac", "chromosome", "position",
      "ref", "alt", "type", "rsid"
    )
  )
  dt <- dt[gene_id == selected_gene_id & type == "SNP" & !is.na(se) & !is.na(beta) & !is.na(maf)]
  dt[, snp_key := paste(chromosome, position, sep = ":")]
  dt <- dt[!is.na(rsid) & rsid != "" & rsid != "NA"]
  unique(dt, by = c("snp_key", "ref", "alt"))
}

prep_gwas <- function(path, trait_name, locus_id) {
  dt <- fread(cmd = paste("gzip -dc", shQuote(path)))
  dt <- dt[trait == trait_name & locus == locus_id]
  dt <- dt[!is.na(beta) & !is.na(se) & !is.na(eaf)]
  dt[, snp_key := paste(chr, bp, sep = ":")]
  dt <- dt[!is.na(rsid) & rsid != "" & rsid != "NA"]
  unique(dt, by = c("snp_key", "effect_allele", "other_allele"))
}

align_to_eqtl_alt <- function(gwas, eqtl) {
  m <- merge(gwas, eqtl, by = "rsid", suffixes = c("_gwas", "_eqtl"))
  m <- m[
    (effect_allele == alt & other_allele == ref) |
      (effect_allele == ref & other_allele == alt)
  ]
  m[, beta_aligned := fifelse(effect_allele == alt, beta_gwas, -beta_gwas)]
  m[, eaf_aligned := fifelse(effect_allele == alt, eaf, 1 - eaf)]
  m[, maf_gwas := pmin(eaf_aligned, 1 - eaf_aligned)]
  m <- m[maf_gwas > 0 & maf_gwas < 0.5 & maf > 0 & maf < 0.5]
  m[, coloc_snp := rsid]
  unique(m, by = "coloc_snp")
}

run_smoke <- function(outcome, tissue, gene, gene_id, locus, chr, start, stop) {
  paths <- fread(file.path(outdir, "tabix_ftp_paths_imported.tsv"))
  ftp <- paths[qtl_group == tissue, ftp_path][1]
  region <- sprintf("%s:%s-%s", chr, start, stop)
  eqtl <- fetch_eqtl(ftp, region, gene_id)
  gwas_path <- file.path(root, "results", "phase4c_preparation", "gwas_loci", sprintf("%s_phase4c_locus_raw.tsv.gz", outcome))
  gwas <- prep_gwas(gwas_path, outcome, locus)
  merged <- align_to_eqtl_alt(gwas, eqtl)
  fwrite(merged, file.path(outdir, sprintf("phase4d_smoke_%s_%s_%s_merged.tsv", outcome, gene, tissue)), sep = "\t")
  meta <- fread(file.path(outdir, "phase4d_gwas_binary_trait_metadata.tsv"))
  meta <- meta[phenotype == outcome][1]

  status <- "PASS"
  note <- "Restricted coloc smoke test using rsID matching, allele harmonization, and binary GWAS N/case fraction from Phase 4B LAVA metadata."
  res <- NULL
  if (nrow(merged) < 50) {
    status <- "LOW_OVERLAP_FAIL"
    note <- "Fewer than 50 matched variants after allele alignment."
  } else {
    d1 <- list(
      beta = merged$beta_aligned,
      varbeta = merged$se_gwas^2,
      snp = merged$coloc_snp,
      MAF = merged$maf_gwas,
      N = meta$total_n,
      s = meta$case_fraction,
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
    coloc_res <- coloc.abf(d1, d2)
    res <- as.data.table(as.list(coloc_res$summary))
  }

  if (is.null(res)) {
    res <- data.table(nsnps = nrow(merged), PP.H0.abf = NA_real_, PP.H1.abf = NA_real_, PP.H2.abf = NA_real_, PP.H3.abf = NA_real_, PP.H4.abf = NA_real_)
  }
  res[, `:=`(
    outcome = outcome,
    tissue = tissue,
    gene = gene,
    gene_id = gene_id,
    locus = locus,
    region = region,
    status = status,
    note = note,
    n_eqtl_variants = nrow(eqtl),
    n_gwas_variants = nrow(gwas),
    n_matched_variants = nrow(merged)
  )]
  setcolorder(res, c("outcome", "tissue", "gene", "gene_id", "locus", "region", "status", "n_eqtl_variants", "n_gwas_variants", "n_matched_variants", "nsnps", "PP.H0.abf", "PP.H1.abf", "PP.H2.abf", "PP.H3.abf", "PP.H4.abf", "note"))
  res
}

smoke <- run_smoke(
  outcome = "cad",
  tissue = "Skin_Sun_Exposed_Lower_leg",
  gene = "SMARCA4",
  gene_id = "ENSG00000127616",
  locus = 2318,
  chr = 19,
  start = 10028841,
  stop = 11681978
)

fwrite(smoke, file.path(outdir, "phase4d_coloc_smoke_test_results.tsv"), sep = "\t")
print(smoke)
