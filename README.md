# CS answer accuracy — Assignment 4

Team: Bekasyl Zhaksylyk, Zere Amantai, Mereke Myrzakhan, SE-2418. Start with **README_RU.md** for simple Russian instructions and **Assignment4_Report.docx** for the report.

The project preserves all 120 original archived responses and all 120 supplementary outputs: 40 keyword-search results, 40 Qwen responses without documents, and 40 responses from the same model with BM25-retrieved documents. Supplementary full-correct results are 4/40, 4/40 and 6/40. Cleanup changes filenames and organization, not responses, ratings or results.

## Reproduce saved results

Python 3.12 or newer; no packages, model access or network are needed after obtaining the package:

```sh
python3 reproduce_all.py --verify
```

Expected ending: `PASS: 22 CSV/SVG files match saved evidence`. Generated verification files go into `reproduced/`. The complete file guide is `docs/file_guide_ru.md`; optional fresh generation is documented in `docs/fresh_generation.md`.

## Provenance and integrity

Original archive SHA-256: `7ff20f027235b6d4c840b2ee82b0add6bb620b9374ada004779035bd2e34fe1d`.

Original release: https://github.com/zere0802/rmt-assignment-4/releases/tag/assignment-4 at commit `396789c99dc41c3526d1466d2683aa966cf7d01f`. Earlier instructions are preserved in `archive/README_original_release.md`. This repository's initial `assignment-4` tag is retained; the organized update is released as `assignment-4-r1`.

Raw supplementary outputs and explicit AI-assisted ratings remain in `supplement/raw/`. Protocol history, fixed settings and input hashes remain in `supplement/protocol/`. The full release ZIP includes the frozen corpus required for optional fresh generation; model weights are not included. The repository can reproduce saved results without that model or corpus download.

The question bank was already known and is not described as an unseen test set. Missing pre-run Moodle submission is disclosed. The initial three-seed supplementary plan was reduced to a single greedy run before any supplementary output; no artificial across-seed SD is claimed. Bekasyl's reported execution of the saved-data verification is recorded in `docs/reproduction_record.json`; it is not independent human re-rating.

Project analysis code is BSD-0-Clause. Model weights and source documentation retain their own terms and attribution. Responsibilities and AI assistance are explained in `docs/contributions.md`.
