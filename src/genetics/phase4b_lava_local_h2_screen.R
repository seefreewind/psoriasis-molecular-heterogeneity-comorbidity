#!/usr/bin/env Rscript

suppressPackageStartupMessages(library(LAVA))
suppressPackageStartupMessages(library(parallel))

root <- getwd()
base.dir <- file.path(root, "results/phase4b_lava")
outdir <- file.path(root, "results/phase4b_lava_local_h2")
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)

sumstats.dir <- file.path(base.dir, "sumstats")
ref.prefix <- file.path(root, "data/genetics/reference/magma/g1000_eur/g1000_eur")
locus.file <- file.path(base.dir, "blocks_s2500_m25_f1_w200.GRCh37_hg19.locfile")
info.file <- file.path(base.dir, "input.info.tsv")
overlap.file <- file.path(base.dir, "sample.overlap.tsv")

phenos <- c("psoriasis", "psa", "crohn", "uc", "cad")
loci <- read.loci(locus.file)
max.loci <- as.integer(Sys.getenv("PHASE4B_LAVA_MAX_LOCI", "0"))
if (!is.na(max.loci) && max.loci > 0) {
  loci <- loci[seq_len(min(max.loci, nrow(loci))), ]
}
cores <- as.integer(Sys.getenv("PHASE4B_LAVA_CORES", "6"))
cores <- max(1, min(cores, parallel::detectCores(logical = FALSE), nrow(loci)))

message("Reading LAVA input for local h2 screening")
input <- process.input(
  input.info.file = info.file,
  sample.overlap.file = overlap.file,
  ref.prefix = ref.prefix,
  phenos = phenos,
  input.dir = sumstats.dir
)
message("Shared SNPs across all phenotypes: ", length(input$analysis.snps))

one_locus <- function(i) {
  loc <- loci[i, ]
  locus.id <- as.character(loc$LOC)
  status <- "START"
  out <- NULL
  tryCatch({
    locus <- process.locus(loc, input)
    available <- intersect(phenos, locus$phenos)
    if (!length(available)) {
      stop("no requested phenotype available after local variance filtering")
    }
    univ <- run.univ(locus, phenos = available)
    if (!is.null(univ) && nrow(univ) > 0) {
      univ$locus <- locus.id
      univ$chr <- loc$CHR
      univ$start <- loc$START
      univ$stop <- loc$STOP
      out <- univ
    }
    status <- "OK"
  }, error = function(e) {
    status <<- paste0("ERROR: ", conditionMessage(e))
  })
  list(
    univ = out,
    status = data.frame(
      locus = locus.id,
      chr = loc$CHR,
      start = loc$START,
      stop = loc$STOP,
      status = status
    )
  )
}

message("Running univariate local h2 across ", nrow(loci), " loci using ", cores, " cores")
res <- mclapply(seq_len(nrow(loci)), one_locus, mc.cores = cores, mc.preschedule = FALSE)
failed <- vapply(res, inherits, logical(1), what = "try-error")
if (any(failed)) {
  warning(sum(failed), " worker-level try-error results returned")
  res <- res[!failed]
}

univ <- lapply(res, `[[`, "univ")
univ <- univ[!vapply(univ, is.null, logical(1))]
status <- lapply(res, `[[`, "status")

univ.out <- if (length(univ)) do.call(rbind, univ) else data.frame()
status.out <- if (length(status)) do.call(rbind, status) else data.frame()
if (nrow(univ.out) > 0) {
  univ.out$fdr_within_pheno <- ave(
    univ.out$p,
    univ.out$phen,
    FUN = function(x) p.adjust(x, method = "BH")
  )
}

write.table(
  univ.out,
  file.path(outdir, "phase4b_lava_local_h2_univariate.tsv"),
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)
write.table(
  status.out,
  file.path(outdir, "phase4b_lava_local_h2_status.tsv"),
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

if (nrow(univ.out) > 0) {
  pair.rows <- list()
  outcomes <- setdiff(phenos, "psoriasis")
  for (outcome in outcomes) {
    ps <- univ.out[univ.out$phen == "psoriasis", ]
    ot <- univ.out[univ.out$phen == outcome, ]
    merged <- merge(
      ps[, c("locus", "chr", "start", "stop", "h2.obs", "p", "fdr_within_pheno")],
      ot[, c("locus", "h2.obs", "p", "fdr_within_pheno")],
      by = "locus",
      suffixes = c("_psoriasis", "_outcome")
    )
    merged$outcome <- outcome
    merged$local_h2_pass_p05 <- merged$p_psoriasis < 0.05 & merged$p_outcome < 0.05
    merged$local_h2_pass_fdr10 <- merged$fdr_within_pheno_psoriasis < 0.10 & merged$fdr_within_pheno_outcome < 0.10
    merged$min_h2_p <- pmax(merged$p_psoriasis, merged$p_outcome)
    pair.rows[[outcome]] <- merged
  }
  pair.out <- do.call(rbind, pair.rows)
  pair.out <- pair.out[order(pair.out$outcome, pair.out$min_h2_p), ]
  write.table(
    pair.out,
    file.path(outdir, "phase4b_lava_pairwise_local_h2_candidates.tsv"),
    sep = "\t",
    quote = FALSE,
    row.names = FALSE
  )

  summary.out <- do.call(rbind, lapply(split(pair.out, pair.out$outcome), function(x) {
    data.frame(
      outcome = unique(x$outcome),
      shared_loci_tested = nrow(x),
      local_h2_pass_p05 = sum(x$local_h2_pass_p05, na.rm = TRUE),
      local_h2_pass_fdr10 = sum(x$local_h2_pass_fdr10, na.rm = TRUE),
      min_joint_h2_p = min(x$min_h2_p, na.rm = TRUE)
    )
  }))
  write.table(
    summary.out,
    file.path(outdir, "phase4b_lava_local_h2_summary.tsv"),
    sep = "\t",
    quote = FALSE,
    row.names = FALSE
  )
}

message("Local h2 screening complete")
