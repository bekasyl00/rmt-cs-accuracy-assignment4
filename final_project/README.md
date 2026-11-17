# Final research project

- `manuscript/Final_Manuscript.docx` — integrated article in the Applied Sciences template (local course package).
- `journal/` — Journal Fit Statement, one-page cover letter, readiness checklist and verification evidence.
- `defence/Final_Presentation.pdf` — 10 slides. `NOTES.md` gives a 10-minute speaking allocation.
- `research/` — original and supplementary saved data, ratings, protocols and calculation scripts.

## Interactive evidence browser

https://elaborate-starship-e9c848.netlify.app/

Open `site/index.html` locally for the same offline browser: 40 questions, all 240 answers, original and supplementary conditions, three checkpoints, rating reasons and retrieved passages. No installation is needed. The site is an interface to saved evidence, not a new experiment.

## Reproduce every Results table and figure

From this folder, with Python 3.12 or newer:

```bash
python3 research/reproduce_manuscript.py --verify
```

No installation, model download or network is required. This recalculates the 22 archived CSV/SVG outputs and six manuscript tables plus three vector figures from saved answers and ratings. It does not generate new AI answers or perform independent human scoring.

| Article item | Output in manuscript/assets |
|---|---|
| Table 2 Original accuracy | Table_1_original_accuracy.csv |
| Table 3 Original paired tests | Table_2_original_tests.csv |
| Table 4 Supplement accuracy | Table_3_supplement_accuracy.csv |
| Table 5 Supplement comparisons | Table_4_supplement_tests.csv |
| Table 6 Scoring sensitivity | Table_5_scoring_sensitivity.csv |
| Table 7 Efficiency | Table_6_efficiency.csv |
| Figures 1–3 | Figure_1.svg, Figure_2.svg, Figure_3.svg |

Table 1 is a literature comparison, not an experimental result; its source is `manuscript/Literature_comparison.csv`. The Word tables match the CSV cells. Historical export filenames remain unchanged to preserve their verified hashes. `manuscript/NUMBER_SOURCES.csv` records the final article numbering.

Expected totals: original 101/120 fully correct and 344/360 checkpoints; supplement keyword 4/40, Qwen 4/40, Qwen+BM25 6/40. All observations, including errors, are retained. `research/docs/fresh_generation.md` describes optional fresh local generation, which is separate from saved-data reproduction.

## Archive and licence

Repository: https://github.com/bekasyl00/rmt-cs-accuracy-assignment4
Final snapshot: tag `final`, directory `final_project/`.

BSD-0-Clause applies to software. Documentation excerpts and model weights retain their own terms. No model weights or private account records are bundled. Publisher-formatted Word manuscripts are kept in the local course package; the public repository contains the plain-text article and reproducibility evidence.

## Remaining author and university checks

Confirm competing interests and final authorship approval; each author must read the cited sources. Obtain the university similarity check. Team reproduction was reported by Bekasyl; an outside-team reproduction and a direct live Scopus category/percentile check remain open. The official October 2026 Scopus source list and Retraction Watch ISSN check are documented in `journal/evidence/`. No journal submission has occurred.
