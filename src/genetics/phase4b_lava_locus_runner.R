#!/usr/bin/env Rscript

suppressPackageStartupMessages(library(LAVA))

root <- getwd()
base.dir <- file.path(root, "results/phase4b_lava")
outdir <- file.path(root, "results/phase4b_lava_locuswise")
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)

sumstats.dir <- file.path(base.dir, "sumstats")
ref.prefix <- file.path(root, "data/genetics/reference/magma/g1000_eur/g1000_eur")
locus.file <- file.path(base.dir, "blocks_s2500_m25_f1_w200.GRCh37_hg19.locfile")
candidate.file <- file.path(root, "results/phase4b_lava_local_h2/phase4b_lava_pairwise_local_h2_candidates.tsv")
target <- "psoriasis"

args <- commandArgs(trailingOnly = TRUE)
outcome <- if (length(args) >= 1) args[[1]] else stop("Usage: phase4b_lava_locus_runner.R <outcome> [max_loci]")
max.n <- if (length(args) >= 2) as.integer(args[[2]]) else 0L
threshold <- as.numeric(Sys.getenv("PHASE4B_LAVA_CANDIDATE_THRESHOLD", "1e-5"))
skip.done <- Sys.getenv("PHASE4B_LAVA_SKIP_DONE", "1") == "1"
ci.mode <- Sys.getenv("PHASE4B_LAVA_CI", "0") == "1"

phenomap <- list(
  psoriasis = list(cases = 36466, controls = 458078, filename = "psoriasis_GCST90472771.sumstats.gz"),
  psa = list(cases = 5065, controls = 21286, filename = "psoriatic_arthritis_GCST90243956.sumstats.gz"),
  crohn = list(cases = 12194, controls = 28072, filename = "crohn_disease_GCST004132.sumstats.gz"),
  uc = list(cases = 12366, controls = 33609, filename = "ulcerative_colitis_GCST004133.sumstats.gz"),
  cad = list(cases = 122733, controls = 424528, filename = "coronary_artery_disease_CADMETA_eu.sumstats.gz")
)
overlap <- c(psa = 0.3142, crohn = -0.0636, uc = -0.0625, cad = 0.0189)
if (!(outcome %in% names(phenomap))) stop("Unknown outcome: ", outcome)

pair.dir <- file.path(outdir, outcome)
dir.create(pair.dir, showWarnings = FALSE, recursive = TRUE)
dir.create(file.path(pair.dir, "loci"), showWarnings = FALSE, recursive = TRUE)

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

loci <- read.loci(locus.file)
candidates <- read.table(candidate.file, sep = "\t", header = TRUE)
candidates <- candidates[candidates$outcome == outcome & candidates$min_h2_p < threshold, ]
candidates <- candidates[order(candidates$min_h2_p), ]
if (!is.na(max.n) && max.n > 0) candidates <- candidates[seq_len(min(max.n, nrow(candidates))), ]
keep <- as.character(candidates$locus)
loci <- loci[as.character(loci$LOC) %in% keep, ]
loci <- loci[match(keep[keep %in% as.character(loci$LOC)], as.character(loci$LOC)), ]
if (nrow(loci) == 0) stop("No candidate loci retained for ", outcome)

message("Reading input for psoriasis vs ", outcome)
input <- process.input(
  input.info.file = file.path(pair.dir, "input.info.tsv"),
  sample.overlap.file = file.path(pair.dir, "sample.overlap.tsv"),
  ref.prefix = ref.prefix,
  phenos = c(target, outcome),
  input.dir = sumstats.dir
)
message("Shared SNPs: ", length(input$analysis.snps))
message("Retained loci: ", nrow(loci), " with threshold ", threshold)

for (i in seq_len(nrow(loci))) {
  loc <- loci[i, ]
  locus.id <- as.character(loc$LOC)
  prefix <- file.path(pair.dir, "loci", paste0("locus_", locus.id))
  status.path <- paste0(prefix, "_status.tsv")
  if (skip.done && file.exists(status.path)) next
  status <- "START"
  univ.out <- data.frame()
  bivar.out <- data.frame()
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
    ok <- all(univ$p[match(c(target, outcome), univ$phen)] < 0.05)
    if (!ok) stop("candidate failed rerun local h2 threshold")
    bivar <- run.bivar(
      locus,
      phenos = c(target, outcome),
      target = target,
      p.values = TRUE,
      CIs = ci.mode,
      adap.thresh = c(1e-4, 1e-6)
    )
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
      bivar$z_approx <- ifelse(!is.na(bivar$p) & bivar$p > 0, qnorm(bivar$p / 2, lower.tail = FALSE), NA_real_)
      bivar$se_approx <- ifelse(!is.na(bivar$z_approx) & bivar$z_approx > 0, abs(bivar$rho) / bivar$z_approx, NA_real_)
      bivar.out <- bivar
    }
    status <- "OK"
  }, error = function(e) {
    status <<- paste0("ERROR: ", conditionMessage(e))
  })
  if (nrow(univ.out) > 0) write.table(univ.out, paste0(prefix, "_univ.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
  if (nrow(bivar.out) > 0) write.table(bivar.out, paste0(prefix, "_bivar.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
  write.table(
    data.frame(locus = locus.id, chr = loc$CHR, start = loc$START, stop = loc$STOP, outcome = outcome, status = status),
    status.path,
    sep = "\t",
    quote = FALSE,
    row.names = FALSE
  )
  message("Outcome ", outcome, " locus ", i, "/", nrow(loci), " (", locus.id, "): ", status)
}

message("Locuswise runner complete for ", outcome)
