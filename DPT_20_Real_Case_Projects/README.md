# DPT 20 Realistic Case Projects

This folder contains 20 ready-to-run YAML project files for the DPT Toolkit.

The cases cover computer science, medicine, agriculture, environmental science, finance,
cybersecurity, engineering, education, public health, transportation, economics, law,
disaster management, robotics, ecology, linguistics, and other fields.

## Run one case

```bash
dpt run projects/01_quantum_computing.yaml -o results/quantum
```

## Run all cases

```bash
mkdir -p results
for file in projects/*.yaml; do
  name=$(basename "$file" .yaml)
  dpt run "$file" -o "results/$name"
done
```

## Important note

These are realistic demonstration and teaching cases, not completed empirical studies.
The DC component values and QC description lengths are declared operational examples.
Researchers should replace them with independently justified anchors, evidence,
coders, reliability checks, and sensitivity analyses for substantive use.
