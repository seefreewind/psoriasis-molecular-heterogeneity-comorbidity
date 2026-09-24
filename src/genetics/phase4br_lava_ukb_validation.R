#!/usr/bin/env Rscript

suppressPackageStartupMessages(library(LAVA))

root <- getwd()
base.dir <- file.path(root, "results/phase4b_lava")
priority.file <- file.path(root, "results/phase4br_ld_reference_validation/phase4br_priority_loci.tsv")
outdir <- file.path(root, "results/phase4br_ld_reference_validation/ukb_lava")
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)
dir.create(file.path(outdir, "loci"), showWarnings = FALSE, recursive = TRUE)

sumstats.dir <- file.path(base.dir, "sumstats")
locus.file <- file.path(base.dir, "blocks_s2500_m25_f1_w200.GRCh37_hg19.locfile")
ukb.extract.dir <- file.path(root, "data/genetics/reference/lava_ukb_v1.1/extracted")
target <- "psoriasis"

args <- commandArgs(trailingOnly = TRUE)
requested.outcomes <- if (length(args) > 0) args else c("cad", "psa", "crohn", "uc")
chrom.filter <- Sys.getenv("PHASE4BR_CHROMS", "")
chrom.filter <- if (nzchar(chrom.filter)) as.integer(unlist(strsplit(chrom.filter, ","))) else integer(0)

phenomap <- list(
  psoriasis = list(cases = 36466, controls = 458078, filename = "psoriasis_GCST90472771.sumstats.gz"),
  psa = list(cases = 5065, controls = 21286, filename = "psoriatic_arthritis_GCST90243956.sumstats.gz"),
  crohn = list(cases = 12194, controls = 28072, filename = "crohn_disease_GCST004132.sumstats.gz"),
  uc = list(cases = 12366, controls = 33609, filename = "ulcerative_colitis_GCST004133.sumstats.gz"),
  cad = list(cases = 122733, controls = 424528, filename = "coronary_artery_disease_CADMETA_eu.sumstats.gz")
)
overlap <- c(psa = 0.3142, crohn = -0.0636, uc = -0.0625, cad = 0.0189)

find_ref_prefix <- function() {
  candidates <- c(
    file.path(ukb.extract.dir, "lava-ukb-v1.1"),
    file.path(ukb.extract.dir, "LAVA_UKB_v1.1", "lava-ukb-v1.1"),
    file.path(ukb.extract.dir, "lava-ukb-v1.1", "lava-ukb-v1.1")
  )
  for (prefix in candidates) {
    if (length(Sys.glob(paste0(prefix, "_chr*"))) > 0 || length(Sys.glob(paste0(prefix, ".chr*"))) > 0) {
      return(prefix)
    }
  }
  files <- list.files(ukb.extract.dir, recursive = TRUE, full.names = TRUE)
  hit <- files[grepl("lava-ukb-v1\\.1_chr1", basename(files))]
  if (length(hit) > 0) {
    return(sub("_chr1.*$", "", hit[[1]]))
  }
  stop("Could not find extracted UKB LAVA v1.1 reference prefix under ", ukb.extract.dir)
}

ref.prefix <- find_ref_prefix()
message("Using UKB reference prefix: ", ref.prefix)

priority <- read.table(priority.file, sep = "\t", header = TRUE)
priority$locus <- as.character(priority$locus)
loci <- read.loci(locus.file)
loci$LOC <- as.character(loci$LOC)

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

run_outcome <- function(outcome) {
  pair.dir <- write_pair_inputs(outcome)
  wanted <- priority[priority$outcome == outcome, ]
  if (length(chrom.filter) > 0) {
    wanted <- wanted[as.integer(wanted$chr) %in% chrom.filter, ]
  }
  wanted.loci <- unique(as.character(wanted$locus))
  pair.loci <- loci[loci$LOC %in% wanted.loci, ]
  pair.loci <- pair.loci[match(wanted.loci[wanted.loci %in% pair.loci$LOC], pair.loci$LOC), ]
  if (nrow(pair.loci) == 0) {
    message("No priority loci for ", outcome, " under current chromosome filter; skipping")
    return(invisible(NULL))
  }

  message("Processing UKB validation input: psoriasis vs ", outcome)
  input <- process.input(
    input.info.file = file.path(pair.dir, "input.info.tsv"),
    sample.overlap.file = file.path(pair.dir, "sample.overlap.tsv"),
    ref.prefix = ref.prefix,
    phenos = c(target, outcome),
    input.dir = sumstats.dir
  )
  message("Shared SNPs for ", outcome, ": ", length(input$analysis.snps))

  for (i in seq_len(nrow(pair.loci))) {
    loc <- pair.loci[i, ]
    locus.id <- as.character(loc$LOC)
    prefix <- file.path(outdir, "loci", paste0(outcome, "_locus_", locus.id))
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
      if (!all(univ$p[match(c(target, outcome), univ$phen)] < 0.05)) {
        stop("local h2 not reliable in both traits under UKB reference")
      }
      bivar <- run.bivar(
        locus,
        phenos = c(target, outcome),
        target = target,
        p.values = TRUE,
        CIs = FALSE,
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
      paste0(prefix, "_status.tsv"),
      sep = "\t",
      quote = FALSE,
      row.names = FALSE
    )
    message("UKB ", outcome, " locus ", i, "/", nrow(pair.loci), " (", locus.id, "): ", status)
  }
}

for (outcome in requested.outcomes) {
  run_outcome(outcome)
}

message("Phase 4B-R UKB reference validation complete")
