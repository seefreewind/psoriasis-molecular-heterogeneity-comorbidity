#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REF_DIR="${ROOT}/data/genetics/reference/lava_ukb_v1.1"
RAW_DIR="${REF_DIR}/raw"
EXTRACT_DIR="${REF_DIR}/extracted"
LOG_DIR="${ROOT}/logs/phase4br_ld_reference"

mkdir -p "${EXTRACT_DIR}" "${LOG_DIR}"

for zip in "${RAW_DIR}"/lava-ukb-v1.1_chr*.zip; do
  [ -s "${zip}" ] || continue
  if [ -f "${zip}.aria2" ]; then
    echo "Skipping incomplete archive ${zip}"
    continue
  fi
  echo "Testing ${zip}"
  unzip -t "${zip}" | tee "${LOG_DIR}/$(basename "${zip}").test.log"
  echo "Extracting ${zip}"
  unzip -n "${zip}" -d "${EXTRACT_DIR}" | tee "${LOG_DIR}/$(basename "${zip}").extract.log"
done

find "${EXTRACT_DIR}" -maxdepth 3 -type f | sort > "${LOG_DIR}/ukb_lava_v1.1_extracted_files.txt"
echo "Extraction complete. File list: ${LOG_DIR}/ukb_lava_v1.1_extracted_files.txt"
