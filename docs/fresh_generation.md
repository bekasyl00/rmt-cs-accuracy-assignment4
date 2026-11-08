# Optional fresh generation on Apple Silicon

This is not needed for the reported result verification.

1. Extract the full release ZIP; it includes the frozen corpus/chunks.json, whose hash is verified by the generator. Building a new live corpus may change inputs and is not an exact reproduction.
2. Create a separate virtual environment and install the pinned generation requirements.
3. Download the exact model revision:

```sh
python -m pip install -r supplement/protocol/requirements-generation.txt
python -c "from huggingface_hub import snapshot_download; snapshot_download('mlx-community/Qwen2.5-Coder-3B-Instruct-4bit',revision='3dd939c621c08e5753d5b89f35a2642cd83b98ca',local_dir='models/qwen')"
python supplement/scripts/run_experiment.py --model models/qwen --output supplement/raw/answers_fresh.jsonl
```

The saved protocol/submission_status.json records that Moodle submission was not made; it is not a fabricated upload. One deterministic pass per condition produces 120 records. Every failure is logged; the script resumes only absent records and never retries low-scoring answers. Complete fresh ratings for changed responses before analysing them:

```sh
python supplement/scripts/analyze_supplement.py --answers supplement/raw/answers_fresh.jsonl --ratings supplement/raw/ratings_fresh.jsonl --out fresh_results
```

The fresh ratings file must actually be created by source-key review; it is not supplied or auto-invented. Output tokenization/runtime differences can change generations. Model weights require about 1.6 GiB; the generation environment also takes disk space. The observed host had 8 GB unified memory.
