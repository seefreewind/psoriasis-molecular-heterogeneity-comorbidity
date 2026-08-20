# Matched-null fallback hierarchy

Authoritative script: `src/genetics/phase3a_matched_null.py`.

The actual fallback order was:

1. Exact matching on chromosome, gene-length quintile and NSNP quintile.
2. If the exact bin was insufficient, matching on gene-length quintile and NSNP quintile across chromosomes.
3. If the broad bin was still insufficient, sampling from the genome-wide MAGMA gene universe after excluding the axis genes and already sampled genes.
4. If the sampled set was still short, random fill from the remaining genome-wide universe excluding the axis genes and already sampled genes.

There was no intermediate same-chromosome relaxed-quintile step in the archived implementation.

Generation parameters: 2,000 null sets per axis; seed 20260811.

Fallback summary:

| axis   |   min |   median |   max |
|:-------|------:|---------:|------:|
| F1     |     1 |        1 |     1 |
| F2     |     2 |        2 |     2 |
| F6     |     0 |        0 |     0 |
| F7     |     1 |        1 |     1 |
