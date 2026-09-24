#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REF_DIR="${ROOT}/data/genetics/reference/lava_ukb_v1.1"
RAW_DIR="${REF_DIR}/raw"
LOG_DIR="${ROOT}/logs/phase4br_ld_reference"
MANIFEST="${LOG_DIR}/ukb_lava_v1.1_download_manifest.tsv"

mkdir -p "${RAW_DIR}" "${LOG_DIR}"

cat > "${MANIFEST}" <<'TSV'
archive	url	expected_filename
chr1-2	https://vu.data.surfsara.nl/index.php/s/7NBVIvtPRdu7Qhz/download	lava-ukb-v1.1_chr1-2.zip
chr3-4	https://vu.data.surfsara.nl/index.php/s/fy6ITboMojHrQXr/download	lava-ukb-v1.1_chr3-4.zip
chr5-6	https://vu.data.surfsara.nl/index.php/s/mRz31q0lq7KMcuI/download	lava-ukb-v1.1_chr5-6.zip
chr7-9	https://vu.data.surfsara.nl/index.php/s/89RXxPN2BlOqxLs/download	lava-ukb-v1.1_chr7-9.zip
chr10-12	https://vu.data.surfsara.nl/index.php/s/3dU1L2Hap43xuCs/download	lava-ukb-v1.1_chr10-12.zip
chr13-16	https://vu.data.surfsara.nl/index.php/s/DQqJ2Sqr49RP4xe/download	lava-ukb-v1.1_chr13-16.zip
chr17-23	https://vu.data.surfsara.nl/index.php/s/U8eg5XfTr8qPzPp/download	lava-ukb-v1.1_chr17-23.zip
TSV

tail -n +2 "${MANIFEST}" | while IFS=$'\t' read -r archive url filename; do
  out="${RAW_DIR}/${filename}"
  log="${LOG_DIR}/download_${archive}.log"
  echo "Downloading ${archive} -> ${out}"
  curl -L --fail --retry 5 --retry-delay 20 --continue-at - "${url}" -o "${out}" 2>&1 | tee "${log}"
  shasum -a 256 "${out}" | tee "${out}.sha256"
done

echo "UKB LAVA v1.1 reference archive download complete."
