#!/usr/bin/env bash
set -euo pipefail

ROOT="/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity"
GTEX_SRC="/Volumes/EMPTY2TB/GTEx_v8_SMR/full_besd"
GTEX_DST="${ROOT}/data/genetics/reference/gtex_v8_smr_besd/extracted"
LD_SRC="/Volumes/EMPTY2TB/New project 12/data/reference/ld/g1000_eur"
LD_DST_DIR="${ROOT}/data/genetics/reference/ld/g1000_eur"
LOG_DIR="${ROOT}/logs/phase4c_smr"
MANIFEST="${ROOT}/results/phase4c_smr/phase4c_smr0_resource_manifest.tsv"

mkdir -p "${GTEX_DST}" "${LD_DST_DIR}" "${LOG_DIR}" "$(dirname "${MANIFEST}")"

{
  printf "resource\tstatus\tsource\tdestination\tnote\n"

  for ext in bed bim fam; do
    src="${LD_SRC}.${ext}"
    dst="${LD_DST_DIR}/g1000_eur.${ext}"
    if [[ ! -f "${src}" ]]; then
      printf "ld_reference_%s\tMISSING\t%s\t%s\tsource file not found\n" "${ext}" "${src}" "${dst}"
      continue
    fi
    if [[ ! -e "${dst}" ]]; then
      ln -s "${src}" "${dst}"
    fi
    printf "ld_reference_%s\tREADY\t%s\t%s\tproject-local symlink\n" "${ext}" "${src}" "${dst}"
  done

  tissues=(
    "Skin_Sun_Exposed_Lower_leg"
    "Skin_Not_Sun_Exposed_Suprapubic"
    "Whole_Blood"
    "Artery_Coronary"
    "Artery_Aorta"
    "Artery_Tibial"
    "Colon_Sigmoid"
    "Colon_Transverse"
    "Spleen"
    "Cells_EBV-transformed_lymphocytes"
    "Cells_Cultured_fibroblasts"
  )

  for tissue in "${tissues[@]}"; do
    zip_path="${GTEX_SRC}/${tissue}.zip"
    prefix="${GTEX_DST}/${tissue}/${tissue}"
    if [[ ! -f "${zip_path}" ]]; then
      printf "gtex_besd_%s\tMISSING\t%s\t%s\tzip not found\n" "${tissue}" "${zip_path}" "${prefix}"
      continue
    fi
    if [[ -f "${prefix}.besd" && -f "${prefix}.epi" && -f "${prefix}.esi" ]]; then
      printf "gtex_besd_%s\tREADY\t%s\t%s\talready extracted\n" "${tissue}" "${zip_path}" "${prefix}"
      continue
    fi
    unzip -n -q "${zip_path}" -d "${GTEX_DST}" > "${LOG_DIR}/${tissue}.unzip.log" 2>&1
    if [[ -f "${prefix}.besd" && -f "${prefix}.epi" && -f "${prefix}.esi" ]]; then
      printf "gtex_besd_%s\tREADY\t%s\t%s\textracted\n" "${tissue}" "${zip_path}" "${prefix}"
    else
      printf "gtex_besd_%s\tFAILED\t%s\t%s\textraction did not produce besd/epi/esi triplet\n" "${tissue}" "${zip_path}" "${prefix}"
    fi
  done
} > "${MANIFEST}"

echo "Wrote ${MANIFEST}"
