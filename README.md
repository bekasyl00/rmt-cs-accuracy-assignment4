# CS answer accuracy Assignment 4

This completed package preserves the original 120 archived answers from three reported commercial model conditions and adds 120 real local outputs: keyword extraction, Qwen2.5-Coder-3B-Instruct without documents, and the same model with BM25-retrieved documentation. The original research question and results remain distinct from the supplementary extension.

## Reproduce all saved-data results

Python 3.12 or newer; no third-party packages, model download, account or network are needed after obtaining this repository.

```sh
python3 -m venv .venv-check
source .venv-check/bin/activate
python reproduce_all.py --verify
```

Expected final output: `PASS: 22 CSV/SVG files match saved evidence`. This reruns the original metrics, independent arithmetic audit, ecosystem sensitivity, supplementary five-test Holm family, and all SVGs. It validates saved explicit ratings; it does not generate new model answers or independently re-rate them.

## Actual supplementary results

| Condition | Fully correct | Checkpoint points |
|---|---:|---:|
| Keyword extraction | 4/40 (10%) | 52/120 (43.3%) |
| Qwen without documents | 4/40 (10%) | 44/120 (36.7%) |
| Qwen with BM25 documents | 6/40 (15%) | 65/120 (54.2%) |

The local model is a resource-feasible literature-backed code-model baseline, not a claim of equal capacity to the original commercial conditions. None of the five supplementary comparisons rejects at Holm-adjusted alpha=0.05. Greedy decoding, one fixed pass per condition, 192-token cap; 13 generated outputs reached that cap and were scored without repair. Every generated answer and every error remains visible.

## Files and provenance

- `data/`: unchanged original archive, SHA-256 `7ff20f027235b6d4c840b2ee82b0add6bb620b9374ada004779035bd2e34fe1d`, and original error codes.
- `results/`: five original CSVs; `diagnostics/`: additional ecosystem checks.
- `supplement/raw/answers.jsonl`: all 120 real supplementary outputs, prompts, retrieved passages, timings and token counts.
- `supplement/raw/ratings.jsonl`: all 120 explicit AI-assisted checkpoint ratings, response hashes and reasons. No independent human-rater agreement is claimed.
- `supplement/results/`: seven supplementary CSVs, including all 106 answers below full correctness.
- `supplement/protocol/`: protocol, pre-output amendment history, exact dependencies, model revision and input hashes. The initial three-seed plan was reduced to one greedy pass BEFORE any supplementary response, not after viewing results.
- `supplement/corpus/manifest.json`: all 56 source URLs, status and hashes. The full frozen chunk file is in the release ZIP; raw scraped HTML is not redistributed in this repository.
- `figures/`, `report_figures/`, `supplement/figures/`: regenerated SVGs.
- `verification_completed.txt`: automated clean-environment check, not a teammate attestation.
- `TEAMMATE_REPRODUCTION_RECORD.md`: blank record to complete after an actual personal run.

Original release: https://github.com/zere0802/rmt-assignment-4/releases/tag/assignment-4 at commit `396789c99dc41c3526d1466d2683aa966cf7d01f`. This new repository preserves that provenance instead of rewriting the original tag. See `README_ORIGINAL_RELEASE.md` for the earlier instructions.

## Fresh generation

Fresh generation is optional and distinct from saved-data reproduction. Download the full release ZIP to retain the exact frozen corpus, install `supplement/protocol/requirements-generation.txt` on Apple Silicon, obtain the pinned model snapshot, and use a NEW output filename. See `FRESH_GENERATION.md`. Do not reuse old ratings for changed answers.

## Limitations and integrity

The question bank and original results were known before the supplement. They are not described as an unseen test set. The historical source list was chosen for the instrument, which may favor retrieval. All new inference is limited to this small purposive question bank and a single deterministic run; intervals do not measure variation across new chats. Missing pre-run Moodle submission and unconfirmed instructor approval are disclosed, not fabricated. The three-author allocation is retained according to the user’s correction of the template’s two-person limit.

The BSD-0-Clause license covers project analysis code. Original model weights and third-party documentation retain their own terms and attribution; no ownership over them is claimed. Model weights are not included.

Russian instructions: `README_START_HERE_RU.md`.
