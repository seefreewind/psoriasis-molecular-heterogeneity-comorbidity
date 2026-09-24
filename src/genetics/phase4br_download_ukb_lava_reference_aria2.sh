#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REF_DIR="${ROOT}/data/genetics/reference/lava_ukb_v1.1"
RAW_DIR="${REF_DIR}/raw"
LOG_DIR="${ROOT}/logs/phase4br_ld_reference"
URL_LIST="${LOG_DIR}/ukb_lava_v1.1_aria2_urls.txt"

mkdir -p "${RAW_DIR}" "${LOG_DIR}"

cat > "${URL_LIST}" <<'TXT'
https://vu.data.surfsara.nl/index.php/s/7NBVIvtPRdu7Qhz/download
  out=lava-ukb-v1.1_chr1-2.zip
https://vu.data.surfsara.nl/index.php/s/fy6ITboMojHrQXr/download
  out=lava-ukb-v1.1_chr3-4.zip
https://vu.data.surfsara.nl/index.php/s/mRz31q0lq7KMcuI/download
  out=lava-ukb-v1.1_chr5-6.zip
https://vu.data.surfsara.nl/index.php/s/89RXxPN2BlOqxLs/download
  out=lava-ukb-v1.1_chr7-9.zip
https://vu.data.surfsara.nl/index.php/s/3dU1L2Hap43xuCs/download
  out=lava-ukb-v1.1_chr10-12.zip
https://vu.data.surfsara.nl/index.php/s/DQqJ2Sqr49RP4xe/download
  out=lava-ukb-v1.1_chr13-16.zip
https://vu.data.surfsara.nl/index.php/s/U8eg5XfTr8qPzPp/download
  out=lava-ukb-v1.1_chr17-23.zip
TXT

aria2c \
  --dir="${RAW_DIR}" \
  --input-file="${URL_LIST}" \
  --continue=true \
  --max-connection-per-server=8 \
  --split=8 \
  --min-split-size=16M \
  --max-concurrent-downloads=1 \
  --retry-wait=20 \
  --max-tries=10 \
  --summary-interval=30 \
  --file-allocation=none \
  --auto-file-renaming=false \
  --allow-overwrite=true \
  2>&1 | tee "${LOG_DIR}/aria2_download.log"

for zip in "${RAW_DIR}"/lava-ukb-v1.1_chr*.zip; do
  shasum -a 256 "${zip}" | tee "${zip}.sha256"
done
