#!/usr/bin/env python3
"""Audit local GTEx v8 SMR/BESD resources for Phase 4C."""

from __future__ import annotations

import subprocess
import zipfile
from pathlib import Path

import pandas as pd


ROOT = Path("/Volumes/EMPTY2TB/银屑病机制论文设计/psoriasis_endotype_comorbidity")
FULL_BESD = Path("/Volumes/EMPTY2TB/GTEx_v8_SMR/full_besd")
OUTDIR = ROOT / "results/phase4c_preparation"
AUDIT = OUTDIR / "phase4c_gtex_v8_smr_besd_audit.tsv"

PRIORITY_TISSUES = {
    "Skin_Sun_Exposed_Lower_leg": "skin",
    "Skin_Not_Sun_Exposed_Suprapubic": "skin",
    "Whole_Blood": "blood",
    "Artery_Coronary": "vascular_arterial",
    "Artery_Aorta": "vascular_arterial",
    "Artery_Tibial": "vascular_arterial",
    "Colon_Sigmoid": "intestinal",
    "Colon_Transverse": "intestinal",
    "Small_Intestine_Terminal_Ileum": "intestinal",
    "Cells_Cultured_fibroblasts": "stromal_cell_model",
    "Cells_EBV-transformed_lymphocytes": "immune_cell_model",
    "Spleen": "immune",
}


def smr_version() -> str:
    smr = Path("/Users/zy/.codex/tools/smr/smr")
    libs = Path("/Users/zy/.codex/tools/smr/smr-1.4.2-macOS-arm64/libs")
    if not smr.exists():
        return "SMR_NOT_FOUND"
    try:
        result = subprocess.run(
            [str(smr), "--version"],
            env={"DYLD_LIBRARY_PATH": str(libs)},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=15,
            check=False,
        )
    except Exception as exc:  # pragma: no cover
        return f"SMR_ERROR:{exc}"
    for line in result.stdout.splitlines():
        if "Version" in line:
            return line.strip("* ").strip()
    return "SMR_RUNNABLE_VERSION_LINE_NOT_FOUND"


def inspect_zip(path: Path) -> dict[str, object]:
    row: dict[str, object] = {
        "zip_path": str(path),
        "zip_exists": path.exists(),
        "zip_size_mb": round(path.stat().st_size / 1024 / 1024, 2) if path.exists() else None,
        "zip_status": "MISSING",
        "has_besd": False,
        "has_epi": False,
        "has_esi": False,
        "besd_uncompressed_mb": None,
        "epi_uncompressed_mb": None,
        "esi_uncompressed_mb": None,
    }
    if not path.exists():
        return row
    try:
        with zipfile.ZipFile(path) as zf:
            bad = zf.testzip()
            names = [info.filename for info in zf.infolist()]
            row["zip_status"] = "PASS" if bad is None else f"BAD_MEMBER:{bad}"
            for suffix, key in [(".besd", "besd"), (".epi", "epi"), (".esi", "esi")]:
                members = [info for info in zf.infolist() if info.filename.endswith(suffix)]
                row[f"has_{key}"] = bool(members)
                if members:
                    row[f"{key}_uncompressed_mb"] = round(members[0].file_size / 1024 / 1024, 2)
    except zipfile.BadZipFile:
        row["zip_status"] = "BAD_ZIP"
    except Exception as exc:  # pragma: no cover
        row["zip_status"] = f"ERROR:{exc}"
    return row


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    rows = []
    zip_files = sorted(p for p in FULL_BESD.glob("*.zip") if not p.name.startswith("._"))
    for path in zip_files:
        tissue = path.stem
        row = inspect_zip(path)
        row["tissue"] = tissue
        row["phase4c_tissue_group"] = PRIORITY_TISSUES.get(tissue, "non_priority")
        row["phase4c_relevant"] = tissue in PRIORITY_TISSUES
        row["smr_usable"] = (
            row["zip_status"] == "PASS" and row["has_besd"] and row["has_epi"] and row["has_esi"]
        )
        row["supports_formal_coloc"] = False
        row["supports_smr_heidi"] = row["smr_usable"]
        rows.append(row)
    audit = pd.DataFrame(rows)
    audit["smr_runtime"] = smr_version()
    audit.to_csv(AUDIT, sep="\t", index=False)
    print(f"Wrote {AUDIT}")
    print(audit.groupby(["phase4c_relevant", "zip_status", "smr_usable"]).size().to_string())


if __name__ == "__main__":
    main()
