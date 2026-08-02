# Sampling protocol

## Candidate-frame construction

The initial frame contains 300 field-filtered OpenAlex records for each of five domains:
Physics and Astronomy, Chemistry, Medicine, Computer Science, and Mathematics. For every
domain, the preserved acquisition consists of 200 records from API page 1 and 100 records from
API page 3.

The raw request URLs do not document an explicit citation-based sorting parameter. The records
must therefore be treated as an auditable candidate frame, not as a verified list of the 300
most-cited articles.

## Screening and final benchmark construction

1. Screen bibliographic anomalies, duplicated manifestations, reviews or summaries that do not
   support reconstruction of a scientific-question episode, and records lacking sufficient
   historical provenance.
2. Reconstruct each retained question from primary scientific and historical sources.
3. Stratify the coded benchmark by field, historical period, subfield, and case type.
4. Include landmark, routine, failed, rediscovered, and non-discovery comparison episodes.
5. Use at least two independent coders and preserve disagreement records.
6. Freeze the codebook before confirmatory analysis.
7. Maintain separate training, calibration, held-out, and, where possible, external-field sets.

Citation count must not be used as the definition of discovery status, Discovery Complexity,
or Question Compression.
