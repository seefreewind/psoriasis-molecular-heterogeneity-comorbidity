# Installation log

## R/Bioconductor preferred stack

Target packages:

- GSVA
- MOFA2
- ConsensusClusterPlus

Attempt 1 used user-level R library:

- Library: `/Users/zy/.codex/R/library`
- R: 4.4.3

Outcome:

- `GSVA`: failed.
- `MOFA2`: failed during package download.
- `ConsensusClusterPlus`: failed because `ALL` was unavailable after download failure.
- HDF5-related dependencies (`Rhdf5lib`, `rhdf5filters`, `rhdf5`, `HDF5Array`) failed after download interruption.
- `magick` failed because Magick++ headers were unavailable.

Attempt 2 installed micromamba:

- Binary: `/Users/zy/.codex/tools/bin/micromamba`
- Root prefix: `/Users/zy/.codex/tools/micromamba-root`

Outcome:

- `bioconductor-gsva` and `bioconductor-mofa2` were not available for the current conda/bioconda osx-arm64 solve.
- Package search found old `bioconductor-mofa` and Python `mofapy2`, but not the locked R `MOFA2` workflow.

Decision:

The preferred R/MOFA2/GSVA workflow is recorded as unavailable in the current environment. The Python fallback workflow is the current reproducible Phase 1 result.

