# Reproduce the research results

Run from this directory with Python 3.12 or newer:

```bash
python3 reproduce_manuscript.py --verify
```

The command checks the 22 archived CSV/SVG outputs, regenerates six manuscript tables and three vector figures in `../manuscript/assets/`, and compares their hashes with `manuscript_reference_outputs.json`. Calculations use the Python standard library and run offline. The six Results tables in Word match the exported CSV cells. PNG copies accompany the vector figures.

`../manuscript/NUMBER_SOURCES.csv` maps Results tables, figures and numerical claims to their evidence files. `input_manifest.json` checks source-data integrity. `reference_outputs.json` checks the historical exports. Generated intermediate results are written to `reproduced/`.

The original archive is in `data/`. Supplementary responses, explicit AI-assisted ratings, corpus and frozen protocol are in `supplement/`. The frozen input hashes and amendment history document the actual experiment. Human-rater agreement was not measured. Bekasyl's reported calculation check is preserved in `docs/reproduction_record.json`. Independent reproduction outside the team remains pending.

Project repository: https://github.com/bekasyl00/rmt-cs-accuracy-assignment4

Historical evidence release: `assignment-4-r1`. Final integrated course snapshot: tag `final`, directory `final_project/`. Code uses BSD-0-Clause. External documentation and model weights retain their own terms. Optional fresh model generation is described in `docs/fresh_generation.md`.
