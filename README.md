# DPT Toolkit

**A transparent, auditable and reproducible implementation of the complete 30-step Discovery Plane Theory workflow.**

DPT Toolkit evaluates candidate scientific questions through two declared coordinates:

- **Discovery Complexity (DC):** least admissible cost of making a question available.
- **Question Compression (QC):** nonnegative reduction in declared representational description length.

It implements operational anchors, procedure-set minimisation, manual and automated QC proxies,
dominance/frontier analysis, budget selection, distance and geodesics, utility, robustness,
reliability, dynamic coordinates, scarcity analysis, plots and an audit-ready report.

> DPT is a research-screening framework. It does not prove that a question is true, ethical,
> feasible, fundable, publishable, or historically important.

## Quick start

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -e .
dpt run examples/energy_case/project.yaml -o results/energy
```

Outputs:

- `REPORT.md` — readable 30-step report
- `report.json` — machine-readable audit record
- `coordinates.csv`, `dominance_matrix.csv`
- sensitivity, scarcity and dynamic CSVs
- `discovery_plane.png`

## Operational anchors

```bash
dpt anchors --domain generic
dpt anchors --domain medicine --json
```

The package supplies explicit 0-4 anchors for time, conceptual distance, search, experiment,
computation and coordination. These defaults are versioned conventions and should be adapted only
with preregistration, evidence, independent coding, reliability analysis and sensitivity checks.

## Optional graphical app

```bash
pip install -e '.[app]'
streamlit run app.py
```

## Automated QC

Supported transparent proxies:

- declared explanatory units;
- UTF-8 description length;
- zlib compressed length;
- simple graph-MDL proxy.

Use at least two independent evidence families for substantive studies. Human ratings may
supplement, but should not be the sole QC measure. LLM-based modules are intentionally not enabled
by default because model outputs are provider-dependent and require archived provenance and human review.

## DiscoveryBench integration

`data/discoverybench/` includes the real 1,500-record processed candidate frame and coding template
from DiscoveryBench v1.1.0, plus original codebook/protocol documents. Metadata records are candidate
anchors for historical reconstruction—not pre-labelled discoveries.

## Reliability

The Python API includes weighted Cohen's kappa, ordinal Krippendorff alpha and ICC(2,1). Calculate
reliability before adjudication and preserve dissent records.

## Repository structure

```text
src/dpt_toolkit/       core library and CLI
examples/              fully worked energy project
configs/domains/       domain adaptation notes
data/discoverybench/   processed benchmark integration
scripts/               reproducible runner
tests/                 unit tests
.github/workflows/     continuous integration
```

## Citation and licence

Software: Apache License 2.0. See `NOTICE` for DiscoveryBench/OpenAlex attribution. Cite the DPT
paper, this software release, and DiscoveryBench when using the bundled benchmark assets.

## Scientific safeguards

- Never infer discovery status from citations alone.
- Never use an LLM score as sole DC/QC evidence.
- Freeze anchors and codebooks before held-out outcome testing.
- Report vectors, weights, uncertainty, exclusions and failed harmonisation.
- Use final expert, ethical, feasibility and empirical review after DPT screening.
