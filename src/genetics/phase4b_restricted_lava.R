#!/usr/bin/env Rscript

suppressPackageStartupMessages(library(LAVA))
suppressPackageStartupMessages(library(parallel))

root <- getwd()
outdir <- file.path(root, "results/phase4b_lava")
logdir <- file.path(root, "logs/phase4b_lava")
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)
dir.create(logdir, showWarnings = FALSE, recursive = TRUE)

input.info <- file.path(outdir, "input.info.tsv")
sample.overlap <- file.path(outdir, "sample.overlap.tsv")
sumstats.dir <- file.path(outdir, "sumstats")
ref.prefix <- file.path(root, "data/genetics/reference/magma/g1000_eur/g1000_eur")
locus.file <- file.path(outdir, "blocks_s2500_m25_f1_w200.GRCh37_hg19.locfile")

target <- "psoriasis"
outcomes <- c("cad", "psa", "crohn", "uc")
univ.thresh <- 0.05

message("Processing LAVA input")
input <- process.input(
  input.info.file = input.info,
  sample.overlap.file = sample.overlap,
  ref.prefix = ref.prefix,
  phenos = c(target, outcomes),
  input.dir = sumstats.dir
)
loci <- read.loci(locus.file)

cores <- as.integer(Sys.getenv("PHASE4B_LAVA_CORES", "4"))
cores <- max(1, min(cores, parallel::detectCores(logical = FALSE), nrow(loci)))

process_one_locus <- function(i) {
  loc <- loci[i, ]
  locus.id <- as.character(loc$LOC)
  status <- "START"
  univ.out <- NULL
  bivar.out <- NULL
  tryCatch({
    locus <- process.locus(loc, input)
    available.phenos <- intersect(c(target, outcomes), locus$phenos)
    if (length(available.phenos) == 0 || !(target %in% available.phenos)) {
      stop("target phenotype unavailable after local variance filtering")
    }
    univ <- run.univ(locus, phenos = available.phenos)
    univ$locus <- locus.id
    univ$chr <- loc$CHR
    univ$start <- loc$START
    univ$stop <- loc$STOP
    univ.out <- univ

    psoriasis.ok <- any(univ$phen == target & univ$p < univ.thresh)
    local.bivar <- list()
    for (outcome in outcomes) {
      if (!(outcome %in% available.phenos)) {
        next
      }
      outcome.ok <- any(univ$phen == outcome & univ$p < univ.thresh)
      if (psoriasis.ok && outcome.ok) {
        bivar <- run.bivar(locus, phenos = c(target, outcome), target = target)
        if (!is.null(bivar) && nrow(bivar) > 0) {
          bivar$locus <- locus.id
          bivar$chr <- loc$CHR
          bivar$start <- loc$START
          bivar$stop <- loc$STOP
          bivar$outcome <- outcome
          bivar$univ_p_psoriasis <- univ$p[match(target, univ$phen)]
          bivar$univ_p_outcome <- univ$p[match(outcome, univ$phen)]
          bivar$h2_psoriasis <- univ$h2.obs[match(target, univ$phen)]
          bivar$h2_outcome <- univ$h2.obs[match(outcome, univ$phen)]
          local.bivar[[length(local.bivar) + 1]] <- bivar
        }
      }
    }
    if (length(local.bivar)) {
      bivar.out <- do.call(rbind, local.bivar)
    }
    status <- "OK"
  }, error = function(e) {
    status <<- paste0("ERROR: ", conditionMessage(e))
  })
  status.out <- data.frame(
    locus = locus.id,
    chr = loc$CHR,
    start = loc$START,
    stop = loc$STOP,
    status = status,
    stringsAsFactors = FALSE
  )
  list(univ = univ.out, bivar = bivar.out, status = status.out)
}

message("Running loci in parallel: ", cores, " cores across ", nrow(loci), " loci")
res <- mclapply(seq_len(nrow(loci)), process_one_locus, mc.cores = cores, mc.preschedule = FALSE)

univ.rows <- lapply(res, `[[`, "univ")
univ.rows <- univ.rows[!vapply(univ.rows, is.null, logical(1))]
bivar.rows <- lapply(res, `[[`, "bivar")
bivar.rows <- bivar.rows[!vapply(bivar.rows, is.null, logical(1))]
status.rows <- lapply(res, `[[`, "status")

univ.out <- if (length(univ.rows)) do.call(rbind, univ.rows) else data.frame()
bivar.out <- if (length(bivar.rows)) do.call(rbind, bivar.rows) else data.frame()
status.out <- do.call(rbind, status.rows)

if (nrow(bivar.out) > 0) {
  bivar.out$pair_scope <- ifelse(
    bivar.out$outcome == "cad", "primary_systemic",
    ifelse(bivar.out$outcome == "psa", "positive_control_near_neighbor", "qc_flagged_ibd")
  )
  bivar.out$fdr_within_outcome <- ave(
    bivar.out$p,
    bivar.out$outcome,
    FUN = function(x) p.adjust(x, method = "BH")
  )
  bivar.out$fdr_all_tests <- p.adjust(bivar.out$p, method = "BH")
  bivar.out$direction <- ifelse(bivar.out$rho > 0, "positive", "negative")
}

write.table(univ.out, file.path(outdir, "phase4b_lava_univariate_local_h2.tsv"),
            sep = "\t", quote = FALSE, row.names = FALSE)
write.table(bivar.out, file.path(outdir, "phase4b_lava_bivariate_local_rg.tsv"),
            sep = "\t", quote = FALSE, row.names = FALSE)
write.table(status.out, file.path(outdir, "phase4b_lava_locus_status.tsv"),
            sep = "\t", quote = FALSE, row.names = FALSE)

summary.rows <- data.frame()
if (nrow(bivar.out) > 0) {
  for (outcome in outcomes) {
    x <- bivar.out[bivar.out$outcome == outcome, , drop = FALSE]
    if (nrow(x) > 0) {
      summary.rows <- rbind(summary.rows, data.frame(
        outcome = outcome,
        tested_loci = nrow(x),
        fdr05_within_outcome = sum(x$fdr_within_outcome < 0.05, na.rm = TRUE),
        nominal_positive = sum(x$p < 0.05 & x$rho > 0, na.rm = TRUE),
        nominal_negative = sum(x$p < 0.05 & x$rho < 0, na.rm = TRUE),
        median_rho = median(x$rho, na.rm = TRUE),
        min_p = min(x$p, na.rm = TRUE),
        stringsAsFactors = FALSE
      ))
    }
  }
}
write.table(summary.rows, file.path(outdir, "phase4b_lava_outcome_summary.tsv"),
            sep = "\t", quote = FALSE, row.names = FALSE)

message("Done")
