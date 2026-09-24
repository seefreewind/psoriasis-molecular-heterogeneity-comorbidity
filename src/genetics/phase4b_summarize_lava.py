#!/usr/bin/env python3

from pathlib import Path

import pandas as pd


ROOT = Path.cwd()
OUT = ROOT / "results/phase4b_restricted_lava"
OUT.mkdir(parents=True, exist_ok=True)


def read_many(paths):
    frames = []
    for path in paths:
        if path.exists() and path.stat().st_size > 0:
            frames.append(pd.read_csv(path, sep="\t"))
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def collect_pairwise(outcome):
    pair_dir = ROOT / "results/phase4b_lava_pairwise" / outcome
    paths = []
    final_path = pair_dir / f"lava_bivariate_{outcome}.tsv"
    if final_path.exists():
        paths.append(final_path)
    chunk_dir = pair_dir / "chunks"
    if chunk_dir.exists():
        paths.extend(sorted(chunk_dir.glob(f"bivar_{outcome}_chunk_*.tsv")))
    return read_many(paths)


def collect_locuswise(outcome):
    locus_dir = ROOT / "results/phase4b_lava_locuswise" / outcome / "loci"
    paths = sorted(locus_dir.glob("locus_*_bivar.tsv")) if locus_dir.exists() else []
    return read_many(paths)


frames = []
for outcome in ["cad", "psa"]:
    df = collect_pairwise(outcome)
    if not df.empty:
        frames.append(df)
for outcome in ["crohn", "uc"]:
    df = collect_locuswise(outcome)
    if not df.empty:
        frames.append(df)

if not frames:
    raise SystemExit("No LAVA bivariate result files found")

bivar = pd.concat(frames, ignore_index=True)
bivar["locus"] = bivar["locus"].astype(str)
bivar = bivar.drop_duplicates(["outcome", "locus"], keep="first").copy()
bivar["direction"] = bivar["rho"].map(lambda x: "positive" if x > 0 else "negative")
bivar["pair_scope"] = bivar["outcome"].map(
    {
        "cad": "primary_systemic",
        "psa": "positive_control_near_neighbor",
        "crohn": "qc_flagged_ibd",
        "uc": "qc_flagged_ibd",
    }
)
bivar["fdr_within_outcome"] = bivar.groupby("outcome")["p"].transform(
    lambda s: pd.Series(pd.Series(s).rank(method="first"), index=s.index)
)
for outcome, idx in bivar.groupby("outcome").groups.items():
    p = bivar.loc[idx, "p"].astype(float)
    order = p.sort_values().index
    m = len(order)
    q = pd.Series(index=order, dtype=float)
    prev = 1.0
    for rank, ix in reversed(list(enumerate(order, start=1))):
        val = min(prev, float(p.loc[ix]) * m / rank)
        q.loc[ix] = val
        prev = val
    bivar.loc[order, "fdr_within_outcome"] = q.loc[order]

p = bivar["p"].astype(float)
order = p.sort_values().index
m = len(order)
q = pd.Series(index=order, dtype=float)
prev = 1.0
for rank, ix in reversed(list(enumerate(order, start=1))):
    val = min(prev, float(p.loc[ix]) * m / rank)
    q.loc[ix] = val
    prev = val
bivar["fdr_all_tests"] = pd.NA
bivar.loc[order, "fdr_all_tests"] = q.loc[order]

if "se_approx" not in bivar.columns:
    bivar["se_approx"] = pd.NA
if "z_approx" not in bivar.columns:
    bivar["z_approx"] = pd.NA

cols = [
    "outcome",
    "pair_scope",
    "locus",
    "chr",
    "start",
    "stop",
    "rho",
    "se_approx",
    "z_approx",
    "p",
    "fdr_within_outcome",
    "fdr_all_tests",
    "direction",
    "h2_psoriasis",
    "h2_outcome",
    "univ_p_psoriasis",
    "univ_p_outcome",
]
for col in cols:
    if col not in bivar.columns:
        bivar[col] = pd.NA
bivar = bivar[cols].sort_values(["outcome", "p"])
bivar.to_csv(OUT / "phase4b_restricted_lava_bivariate.tsv", sep="\t", index=False)

local_h2 = pd.read_csv(
    ROOT / "results/phase4b_lava_local_h2/phase4b_lava_pairwise_local_h2_candidates.tsv",
    sep="\t",
)
local_h2_summary = pd.read_csv(
    ROOT / "results/phase4b_lava_local_h2/phase4b_lava_local_h2_summary.tsv",
    sep="\t",
)

summary_rows = []
for outcome, x in bivar.groupby("outcome"):
    h2x = local_h2[local_h2["outcome"] == outcome]
    summary_rows.append(
        {
            "outcome": outcome,
            "scope": x["pair_scope"].iloc[0],
            "shared_loci_tested_local_h2": int(local_h2_summary.loc[local_h2_summary["outcome"] == outcome, "shared_loci_tested"].iloc[0]),
            "joint_h2_p05": int((h2x["min_h2_p"] < 0.05).sum()),
            "joint_h2_1e5": int((h2x["min_h2_p"] < 1e-5).sum()),
            "bivar_loci_tested": int(len(x)),
            "fdr05_within_outcome": int((x["fdr_within_outcome"] < 0.05).sum()),
            "fdr05_all_tests": int((x["fdr_all_tests"].astype(float) < 0.05).sum()),
            "nominal_positive": int(((x["p"] < 0.05) & (x["rho"] > 0)).sum()),
            "nominal_negative": int(((x["p"] < 0.05) & (x["rho"] < 0)).sum()),
            "median_rho": float(x["rho"].median()),
            "min_p": float(x["p"].min()),
            "top_locus": str(x.sort_values("p").iloc[0]["locus"]),
            "top_rho": float(x.sort_values("p").iloc[0]["rho"]),
        }
    )
summary = pd.DataFrame(summary_rows).sort_values("outcome")
summary.to_csv(OUT / "phase4b_restricted_lava_summary.tsv", sep="\t", index=False)

top = bivar.sort_values("p").groupby("outcome").head(15)
top.to_csv(OUT / "phase4b_restricted_lava_top_loci.tsv", sep="\t", index=False)

print(summary.to_string(index=False))
