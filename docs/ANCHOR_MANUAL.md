# DPT Operational Anchor Manual v1.0

## Status
These anchors are **declared operational conventions**, not universal physical units. They are
intended to improve transparency and intercoder reproducibility. A project may change an anchor
only before outcome inspection, with justification, versioning, and sensitivity analysis.

## Coding protocol
1. Two or more coders independently reconstruct the question episode.
2. Coders record evidence before selecting a score.
3. Use the highest anchor clearly supported when indicators disagree; retain all raw indicators.
4. Calculate reliability before adjudication.
5. Preserve dissent records and adjudication rationale.
6. Preregister component weights; always report the six-component vector before scalarisation.
7. Run alternative admissible weight and normalisation schemes.

Run `dpt anchors --domain generic` for the complete machine-readable table.

## Automated estimators
The toolkit offers UTF-8, zlib and simple graph-MDL description-length proxies. These are
triangulation tools, not semantic truth measures. An LLM may propose representations or anchors,
but its prompts, model/version, outputs, uncertainty and human review must be archived. LLM output
must never be the sole evidence for QC or final selection.
