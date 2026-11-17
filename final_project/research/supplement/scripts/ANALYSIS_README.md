# Supplementary result analysis

Run after actual generation and rating are complete:

```sh
python supplement/scripts/analyze_supplement.py
```

Paths are resolved from the script location, so the same command can also be invoked by absolute path. Python 3.12+ and the standard library suffice; analysis does not load the model.

Inputs: `supplement/raw/answers.jsonl` and `supplement/raw/ratings.jsonl`. Each must contain one record for every question in `protocol/questions_only.json` and every condition `simple`, `model`, `rag`. There must be exactly 120 unique condition–question records. `seed` is JSON null for deterministic extraction and integer 17 for both generated conditions.

Required rating fields:

```json
{"question_id":"V2Q01","condition":"model","seed":17,"checkpoint_points":[0,0,0],"material_additional_error":false,"category":"incorrect","reason":"Actual source-based reason must be supplied."}
```

This is a **schema illustration**, not a rating to copy into the study. Ratings may optionally include `points` (which must sum correctly), `error_type`/`code`, or additional audit fields. The program does not invent scores. Each rating requires three binary integer checkpoint values, a boolean additional-error flag, an explicit category, and a nonempty reason. Raw failed outputs must have category `missing` and zero points. Abstention with text requires an explicit `abstain` judgment and zero points. All other categories are recomputed from the fixed rubric.

Outputs in `supplement/results/`:

- `main_results.csv`: planned and observed denominators, categories, strict accuracy, Wilson 95% interval, checkpoint score.
- `sensitivity.csv`: strict versus checkpoint-only correctness.
- `paired_comparisons.csv`: the three method contrasts and two within-model topic contrasts; exact McNemar probabilities, one family of five Holm adjustments, exact empirical paired-bootstrap interval, and unrounded rational probabilities.
- `efficiency.csv`: actual successful-call median/Q1/Q3/IQR latency and token counts. Model load time is separate in `raw/model_load.json` and is not included in call latency.
- `answer_audit.csv` and `error_cases.csv`: all rating decisions and every answer below full correctness, including missing outputs.
- `retrieval_coverage.csv`: diagnostic overlap of retrieved source IDs with the original reference-source IDs. This is measured after retrieval and is not an accuracy score or proof that the retrieved passage contains the answer.

Missing outputs count as failures in the planned-item primary metric; the observed-answer percentage is separately retained. Rate intervals use Wilson's method on question outcomes, not checkpoint trials. Bootstrap intervals resample 40 complete questions for between-method contrasts and 20 established–recent pairs for topic contrasts. They are pointwise and not adjusted for multiplicity or ecosystem/block dependence. Confidence intervals and exact tests remain exploratory for this reused purposive question bank. No SD across duplicate deterministic passes is fabricated.

Contrast directions are `model − simple`, `rag − simple`, `rag − model` (two-sided exact tests), then established − recent within `model` and `rag` (one-sided greater tests). Positive effect sizes favor the first term. Fractions in the CSV preserve the exact p-values. Quartiles use linear interpolation (inclusive type 7).
