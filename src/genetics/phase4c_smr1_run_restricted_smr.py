#!/usr/bin/env python3
"""Run restricted Phase 4C SMR/HEIDI across frozen outcome-tissue pairs."""

from __future__ import annotations

import subprocess
import os
from pathlib import Path

import pandas as pd


ROOT = Path("/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity")
MANIFEST = Path(os.environ.get("PHASE4C_SMR_PROBE_MANIFEST", ROOT / "results/phase4c_smr/phase4c_smr1_probe_list_manifest.tsv"))
OUTDIR = Path(os.environ.get("PHASE4C_SMR_OUTDIR", ROOT / "results/phase4c_smr/restricted"))
LOGDIR = Path(os.environ.get("PHASE4C_SMR_LOGDIR", ROOT / "logs/phase4c_smr/restricted"))
SUMMARY = Path(os.environ.get("PHASE4C_SMR_RUN_MANIFEST", ROOT / "results/phase4c_smr/phase4c_smr1_run_manifest.tsv"))
BFILE = ROOT / "data/genetics/reference/ld/g1000_eur/g1000_eur"
SMR = Path("/Users/zy/.codex/tools/smr_x86/smr")


def run_one(row: pd.Series) -> dict[str, object]:
    outcome = row["outcome"]
    tissue = row["tissue"]
    stem = f"{outcome}__{tissue}"
    out_prefix = OUTDIR / stem
    log_file = LOGDIR / f"{stem}.log"

    result = {
        "outcome": outcome,
        "tissue": tissue,
        "n_candidate_loci": row["n_candidate_loci"],
        "n_probes_requested": row["n_probes"],
        "status": "NOT_RUN",
        "exit_code": None,
        "output_prefix": str(out_prefix),
        "smr_file": str(out_prefix) + ".smr",
        "log_file": str(log_file),
        "n_smr_results": 0,
    }
    if int(row["n_probes"]) == 0:
        result["status"] = "NO_PROBES"
        return result

    cmd = [
        "arch",
        "-x86_64",
        str(SMR),
        "--bfile",
        str(BFILE),
        "--gwas-summary",
        str(row["gwas_ma"]),
        "--beqtl-summary",
        str(row["besd_prefix"]),
        "--extract-probe",
        str(row["probe_id_file"]),
        "--out",
        str(out_prefix),
        "--thread-num",
        "4",
        "--peqtl-smr",
        "5e-8",
        "--heidi-min-m",
        "3",
    ]

    with open(log_file, "wt") as handle:
        proc = subprocess.run(cmd, stdout=handle, stderr=subprocess.STDOUT, text=True, check=False)
    result["exit_code"] = proc.returncode
    result["status"] = "PASS" if proc.returncode == 0 else "FAIL"
    smr_path = Path(str(out_prefix) + ".smr")
    if smr_path.exists():
        with open(smr_path) as handle:
            result["n_smr_results"] = max(sum(1 for _ in handle) - 1, 0)
    return result


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    LOGDIR.mkdir(parents=True, exist_ok=True)
    manifest = pd.read_csv(MANIFEST, sep="\t")
    rows = []
    for row in manifest.itertuples(index=False):
        series = pd.Series(row._asdict())
        print(f"Running {series['outcome']} x {series['tissue']} ({series['n_probes']} probes)", flush=True)
        rows.append(run_one(series))
        pd.DataFrame(rows).to_csv(SUMMARY, sep="\t", index=False)
    summary = pd.DataFrame(rows)
    summary.to_csv(SUMMARY, sep="\t", index=False)
    print(summary.groupby(["outcome", "status"])["n_smr_results"].sum().to_string())


if __name__ == "__main__":
    main()
