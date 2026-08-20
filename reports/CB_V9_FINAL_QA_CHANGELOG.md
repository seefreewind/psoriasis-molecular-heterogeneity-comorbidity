# V9 Final QA Changelog

## Scientific claim correction

- original: "Discrete molecular endotypes were not reproducible."  
  revised: "The tested k = 2 discrete endotype representation did not meet the prespecified stability criterion."  
  reason: limits the claim to the tested representation.

## Dataset traceability

- original: GSE61281 appeared in Table 2 only.  
  revised: GSE61281 added to Table 1, Results and Methods.  
  reason: removes hybrid main/supplementary handling.

## Figure coverage

- original: short legends did not define panel metrics.  
  revised: Figures 1-6 legends rewritten panel-by-panel.  
  reason: improves self-contained figure interpretation.

## Table coverage

- original: Table 2 used abs(rho), field-state/stress-like labels and F7 as a stronger systemic statement.  
  revised: Table 2 uses |ρ|/ρ and conservative F2/F6/F7 interpretations.  
  reason: standardizes notation and claim strength.

## Methods completeness

- original: compact Methods did not define GSE61281 or spatial ρ.  
  revised: Methods now define GSE61281 scoring and spatial ρ.  
  reason: main metrics are reproducible from text plus source files.

## Reference correction

- original: Alegbe Nature 642, 1-23; Vestergaard/Jimenez-Gracia lacked diacritics.  
  revised: Alegbe Nature 656, 129-139; Vestergaard Alfaro-Núñez and Jiménez-Gracia corrected.  
  reason: publisher/Crossref/PubMed metadata audit.

## Citation redistribution

- original: several citation clusters remained.  
  revised: Introduction split into transcriptomic and genetic paragraphs; Discussion clusters reduced where possible.  
  reason: one literature claim should map to a matched citation.

## Statistical formatting

- original: rho, rg, h2, >=, <= and e-notation.  
  revised: ρ, r_g, h², ≥, ≤ and ×10 notation in main results.  
  reason: journal-facing statistical typography.

## Language/grammar

- original: failed/failure/rescue-style project language.  
  revised: prespecified criterion/support language.  
  reason: submission-facing academic tone.

## Submission formatting

- original: final QA version not created.  
  revised: v9 FINAL_QA MD and DOCX generated without overwriting prior files.  
  reason: submission-lock traceability.
