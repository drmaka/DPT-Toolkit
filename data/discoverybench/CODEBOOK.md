# DiscoveryBench Coding Codebook

## Unit of analysis
A scientifically meaningful **question episode**, linked to one or more publications. A publication is only a candidate carrier of a question.

## Required case types
Landmark discovery; routine question; failed question; rediscovery; non-discovery/comparison.

## Question reconstruction
Two coders independently write the central scientific question using primary historical or scientific sources. Coders remain blinded to downstream citation and impact labels during initial coding. Record the source and uncertainty.

## Discovery-cost vector
Use ordinal 0-4 ratings with written evidence for each component:
- `C_time`: time/resources needed to make the question available.
- `C_concept`: conceptual novelty and departure from available categories.
- `C_search`: search-space burden.
- `C_experiment`: experimental/instrumental burden.
- `C_compute`: computational burden.
- `C_coordination`: coordination, team, institution, or infrastructure burden.

Do not combine components until the weight scheme is preregistered. A default pilot scalar is an equal-weight mean, used only for calibration.

## Representation measures
- `L_R`: declared description length of the pre-question representation.
- `L_Rq`: description length after applying the question-induced representation.
- `delta_L = L_R - L_Rq`.
- `QC_raw = max(0, delta_L)`.
- `compression_explanatory = Yes` when `L_Rq <= L_R`.
- `kg_reorganisation_score`: independent time-indexed knowledge-graph evidence.
- `human_compression_rating`: supplementary expert rating; never the sole QC measure.

## Uncertainty
Record low/high bounds, coding confidence, model/version, and provenance. Do not delete dissenting coder records after adjudication.

## Inclusion
Include only cases with identifiable question, traceable evidence, stable bibliographic identity, and adequate historical context.

## Exclusion
Exclude reviews, guidelines, datasets, tools, or highly cited methods when no defensible discovery-question episode can be reconstructed; retain the exclusion reason.
