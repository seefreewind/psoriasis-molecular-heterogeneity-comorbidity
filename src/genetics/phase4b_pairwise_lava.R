#!/usr/bin/env Rscript

suppressPackageStartupMessages(library(LAVA))
suppressPackageStartupMessages(library(parallel))

root <- getwd()
outdir <- file.path(root, "results/phase4b_lava_pairwise")
logdir <- file.path(root, "logs/phase4b_lava")
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)
dir.create(logdir, showWarnings = FALSE, recursive = TRUE)

base.dir <- file.path(root, "results/phase4b_lava")
sumstats.dir <- file.path(base.dir, "sumstats")
ref.prefix <- file.path(root, "data/genetics/reference/magma/g1000_eur/g1000_eur")
locus.file <- file.path(base.dir, "blocks_s2500_m25_f1_w200.GRCh37_hg19.locfile")
loci <- read.loci(locus.file)
max.loci <- as.integer(Sys.getenv("PHASE4B_LAVA_MAX_LOCI", "0"))
if (!is.na(max.loci) && max.loci > 0) {
  loci <- loci[seq_len(min(max.loci, nrow(loci))), ]
}

target <- "psoriasis"
requested <- commandArgs(trailingOnly = TRUE)
outcomes <- if (length(requested) > 0) requested else c("cad", "psa", "crohn", "uc")
univ.thresh <- 0.05
cores <- as.integer(Sys.getenv("PHASE4B_LAVA_CORES", "6"))
cores <- max(1, min(cores, parallel::detectCores(logical = FALSE), nrow(loci)))
chunk.size <- as.integer(Sys.getenv("PHASE4B_LAVA_CHUNK_SIZE", "0"))
fast.mode <- Sys.getenv("PHASE4B_LAVA_FAST", "0") == "1"
ci.mode <- Sys.getenv("PHASE4B_LAVA_CI", "0") == "1"
candidate.threshold <- as.numeric(Sys.getenv("PHASE4B_LAVA_CANDIDATE_THRESHOLD", "0"))
candidate.file <- file.path(root, "results/phase4b_lava_local_h2/phase4b_lava_pairwise_local_h2_candidates.tsv")

phenomap <- list(
  psoriasis = list(cases = 36466, controls = 458078, filename = "psoriasis_GCST90472771.sumstats.gz"),
  psa = list(cases = 5065, controls = 21286, filename = "psoriatic_arthritis_GCST90243956.sumstats.gz"),
  crohn = list(cases = 12194, controls = 28072, filename = "crohn_disease_GCST004132.sumstats.gz"),
  uc = list(cases = 12366, controls = 33609, filename = "ulcerative_colitis_GCST004133.sumstats.gz"),
  cad = list(cases = 122733, controls = 424528, filename = "coronary_artery_disease_CADMETA_eu.sumstats.gz")
)

overlap <- c(psa = 0.3142, crohn = -0.0636, uc = -0.0625, cad = 0.0189)

write_pair_inputs <- function(outcome) {
  pair.dir <- file.path(outdir, outcome)
  dir.create(pair.dir, showWarnings = FALSE, recursive = TRUE)
  info <- data.frame(
    phenotype = c(target, outcome),
    cases = c(phenomap[[target]]$cases, phenomap[[outcome]]$cases),
    controls = c(phenomap[[target]]$controls, phenomap[[outcome]]$controls),
    filename = c(phenomap[[target]]$filename, phenomap[[outcome]]$filename)
  )
  write.table(info, file.path(pair.dir, "input.info.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
  ov <- matrix(c(1, overlap[[outcome]], overlap[[outcome]], 1), nrow = 2, byrow = TRUE)
  colnames(ov) <- rownames(ov) <- c(target, outcome)
  write.table(ov, file.path(pair.dir, "sample.overlap.tsv"), sep = " ", quote = FALSE, col.names = NA)
  pair.dir
}

process_pair <- function(outcome) {
  pair.dir <- write_pair_inputs(outcome)
  message("Processing pair: psoriasis vs ", outcome)
  input <- process.input(
    input.info.file = file.path(pair.dir, "input.info.tsv"),
    sample.overlap.file = file.path(pair.dir, "sample.overlap.tsv"),
    ref.prefix = ref.prefix,
    phenos = c(target, outcome),
    input.dir = sumstats.dir
  )
  message("Pair ", outcome, ": shared SNPs = ", length(input$analysis.snps))
  pair.loci <- loci
  if (!is.na(candidate.threshold) && candidate.threshold > 0 && file.exists(candidate.file)) {
    candidates <- read.table(candidate.file, sep = "\t", header = TRUE)
    candidates <- candidates[candidates$outcome == outcome & candidates$min_h2_p < candidate.threshold, ]
    keep <- as.character(candidates$locus)
    pair.loci <- loci[as.character(loci$LOC) %in% keep, ]
    pair.loci <- pair.loci[match(keep[keep %in% as.character(pair.loci$LOC)], as.character(pair.loci$LOC)), ]
    message("Pair ", outcome, ": candidate local-h2 threshold ", candidate.threshold,
            " retained ", nrow(pair.loci), " loci")
  }
  if (nrow(pair.loci) == 0) {
    stop("No loci retained for outcome ", outcome)
  }

  one_locus <- function(i) {
    loc <- pair.loci[i, ]
    locus.id <- as.character(loc$LOC)
    status <- "START"
    univ.out <- NULL
    bivar.out <- NULL
    tryCatch({
      locus <- process.locus(loc, input)
      available <- intersect(c(target, outcome), locus$phenos)
      if (!(target %in% available) || !(outcome %in% available)) {
        stop("required phenotype unavailable after local variance filtering")
      }
      univ <- run.univ(locus, phenos = c(target, outcome))
      univ$locus <- locus.id
      univ$chr <- loc$CHR
      univ$start <- loc$START
      univ$stop <- loc$STOP
      univ$outcome <- outcome
      univ.out <- univ
      ok <- all(univ$p[match(c(target, outcome), univ$phen)] < univ.thresh)
      if (ok) {
        bivar <- run.bivar(
          locus,
          phenos = c(target, outcome),
          target = target,
          p.values = !fast.mode,
          CIs = ci.mode && !fast.mode,
          adap.thresh = if (fast.mode) NULL else c(1e-4, 1e-6)
        )
        if (!is.null(bivar) && nrow(bivar) > 0) {
          if (!("p" %in% colnames(bivar))) {
            bivar$p <- NA_real_
          }
          bivar$locus <- locus.id
          bivar$chr <- loc$CHR
          bivar$start <- loc$START
          bivar$stop <- loc$STOP
          bivar$outcome <- outcome
          bivar$univ_p_psoriasis <- univ$p[match(target, univ$phen)]
          bivar$univ_p_outcome <- univ$p[match(outcome, univ$phen)]
          bivar$h2_psoriasis <- univ$h2.obs[match(target, univ$phen)]
          bivar$h2_outcome <- univ$h2.obs[match(outcome, univ$phen)]
          bivar.out <- bivar
        }
      }
      status <- "OK"
    }, error = function(e) {
      status <<- paste0("ERROR: ", conditionMessage(e))
    })
    list(
      univ = univ.out,
      bivar = bivar.out,
      status = data.frame(locus = locus.id, chr = loc$CHR, start = loc$START, stop = loc$STOP, outcome = outcome, status = status)
    )
  }

  chunk.dir <- file.path(pair.dir, "chunks")
  dir.create(chunk.dir, showWarnings = FALSE, recursive = TRUE)
  index <- seq_len(nrow(pair.loci))
  chunks <- if (!is.na(chunk.size) && chunk.size > 0) split(index, ceiling(index / chunk.size)) else list(index)
  all.res <- list()
  for (chunk.name in names(chunks)) {
    chunk.idx <- chunks[[chunk.name]]
    message("Pair ", outcome, ": chunk ", chunk.name, " loci ", min(chunk.idx), "-", max(chunk.idx), " / ", nrow(pair.loci))
    res <- mclapply(chunk.idx, one_locus, mc.cores = cores, mc.preschedule = FALSE, mc.silent = FALSE)
    failed <- vapply(res, inherits, logical(1), what = "try-error")
    if (any(failed)) {
      warning(sum(failed), " worker-level try-error results returned in chunk ", chunk.name)
      res <- res[!failed]
    }
    if (!length(res)) {
      warning("No locus results returned for outcome ", outcome, " chunk ", chunk.name)
      next
    }
    all.res <- c(all.res, res)
    chunk.univ <- lapply(res, `[[`, "univ")
    chunk.univ <- chunk.univ[!vapply(chunk.univ, is.null, logical(1))]
    chunk.bivar <- lapply(res, `[[`, "bivar")
    chunk.bivar <- chunk.bivar[!vapply(chunk.bivar, is.null, logical(1))]
    chunk.status <- lapply(res, `[[`, "status")
    if (length(chunk.univ)) write.table(do.call(rbind, chunk.univ), file.path(chunk.dir, paste0("univ_", outcome, "_chunk_", chunk.name, ".tsv")), sep = "\t", quote = FALSE, row.names = FALSE)
    if (length(chunk.bivar)) write.table(do.call(rbind, chunk.bivar), file.path(chunk.dir, paste0("bivar_", outcome, "_chunk_", chunk.name, ".tsv")), sep = "\t", quote = FALSE, row.names = FALSE)
    if (length(chunk.status)) write.table(do.call(rbind, chunk.status), file.path(chunk.dir, paste0("status_", outcome, "_chunk_", chunk.name, ".tsv")), sep = "\t", quote = FALSE, row.names = FALSE)
  }
  res <- all.res
  if (!length(res)) {
    stop("No locus results returned for outcome ", outcome)
  }
  univ <- lapply(res, `[[`, "univ")
  univ <- univ[!vapply(univ, is.null, logical(1))]
  bivar <- lapply(res, `[[`, "bivar")
  bivar <- bivar[!vapply(bivar, is.null, logical(1))]
  status <- lapply(res, `[[`, "status")

  univ.out <- if (length(univ)) do.call(rbind, univ) else data.frame()
  bivar.out <- if (length(bivar)) do.call(rbind, bivar) else data.frame()
  status.out <- do.call(rbind, status)
  if (nrow(bivar.out) > 0) {
    bivar.out$fdr_within_outcome <- p.adjust(bivar.out$p, method = "BH")
    bivar.out$z_approx <- ifelse(!is.na(bivar.out$p) & bivar.out$p > 0, qnorm(bivar.out$p / 2, lower.tail = FALSE), NA_real_)
    bivar.out$se_approx <- ifelse(!is.na(bivar.out$z_approx) & bivar.out$z_approx > 0, abs(bivar.out$rho) / bivar.out$z_approx, NA_real_)
    bivar.out$direction <- ifelse(bivar.out$rho > 0, "positive", "negative")
    bivar.out$pair_scope <- ifelse(outcome == "cad", "primary_systemic",
                                   ifelse(outcome == "psa", "positive_control_near_neighbor", "qc_flagged_ibd"))
  }
  write.table(univ.out, file.path(pair.dir, paste0("lava_univariate_", outcome, ".tsv")), sep = "\t", quote = FALSE, row.names = FALSE)
  write.table(bivar.out, file.path(pair.dir, paste0("lava_bivariate_", outcome, ".tsv")), sep = "\t", quote = FALSE, row.names = FALSE)
  write.table(status.out, file.path(pair.dir, paste0("lava_status_", outcome, ".tsv")), sep = "\t", quote = FALSE, row.names = FALSE)

  data.frame(
    outcome = outcome,
    shared_snps = length(input$analysis.snps),
    univ_rows = nrow(univ.out),
    loci_with_bivar = nrow(bivar.out),
    fdr05_within_outcome = if (nrow(bivar.out) && "fdr_within_outcome" %in% colnames(bivar.out)) sum(bivar.out$fdr_within_outcome < 0.05, na.rm = TRUE) else 0,
    nominal_positive = if (nrow(bivar.out) && "p" %in% colnames(bivar.out)) sum(bivar.out$p < 0.05 & bivar.out$rho > 0, na.rm = TRUE) else 0,
    nominal_negative = if (nrow(bivar.out) && "p" %in% colnames(bivar.out)) sum(bivar.out$p < 0.05 & bivar.out$rho < 0, na.rm = TRUE) else 0,
    median_rho = if (nrow(bivar.out)) median(bivar.out$rho, na.rm = TRUE) else NA,
    min_p = if (nrow(bivar.out) && "p" %in% colnames(bivar.out)) min(bivar.out$p, na.rm = TRUE) else NA
  )
}

summary.rows <- do.call(rbind, lapply(outcomes, process_pair))
write.table(summary.rows, file.path(outdir, "phase4b_pairwise_lava_summary.tsv"),
            sep = "\t", quote = FALSE, row.names = FALSE)

all.bivar <- list()
all.univ <- list()
all.status <- list()
for (outcome in outcomes) {
  pair.dir <- file.path(outdir, outcome)
  bivar.path <- file.path(pair.dir, paste0("lava_bivariate_", outcome, ".tsv"))
  univ.path <- file.path(pair.dir, paste0("lava_univariate_", outcome, ".tsv"))
  status.path <- file.path(pair.dir, paste0("lava_status_", outcome, ".tsv"))
  if (file.exists(bivar.path) && file.info(bivar.path)$size > 0) all.bivar[[outcome]] <- read.table(bivar.path, sep = "\t", header = TRUE)
  if (file.exists(univ.path) && file.info(univ.path)$size > 0) all.univ[[outcome]] <- read.table(univ.path, sep = "\t", header = TRUE)
  if (file.exists(status.path) && file.info(status.path)$size > 0) all.status[[outcome]] <- read.table(status.path, sep = "\t", header = TRUE)
}
if (length(all.bivar)) {
  combined <- do.call(rbind, all.bivar)
  combined$fdr_all_tests <- p.adjust(combined$p, method = "BH")
  write.table(combined, file.path(outdir, "phase4b_pairwise_lava_bivariate_all.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
}
if (length(all.univ)) write.table(do.call(rbind, all.univ), file.path(outdir, "phase4b_pairwise_lava_univariate_all.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
if (length(all.status)) write.table(do.call(rbind, all.status), file.path(outdir, "phase4b_pairwise_lava_status_all.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)

message("Pairwise restricted LAVA complete")
