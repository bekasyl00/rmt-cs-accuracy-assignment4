# Historical preparation note

This note predates the completed supplement. Use README.md and README_START_HERE_RU.md for current results and commands.

# Assignment 4 quantitative analysis supplement

This package completes the quantitative section of the joint report using the existing RMT-CS-v2 answers and ratings. No model responses, participants, runs or rating decisions were invented or added.

## Provenance

- Original release: https://github.com/zere0802/rmt-assignment-4/releases/tag/assignment-4
- Original commit: `396789c99dc41c3526d1466d2683aa966cf7d01f`.
- Original JSON SHA-256: `7ff20f027235b6d4c840b2ee82b0add6bb620b9374ada004779035bd2e34fe1d`.
- On 8 November 2026, the JSON embedded in https://elaborate-starship-e9c848.netlify.app/ was parsed and found equal to the released JSON data structure.
- The original scripts, source data, reference results, reference figures, environment file, README and license are retained unchanged. The supplement is local and is not claimed to be published under the original GitHub tag.

## Reproduce

Python 3.12 or newer is required. All calculation and SVG scripts use only the standard library. No package installation, credentials or model access is needed.

Run from this folder:

```sh
python3 -m venv .venv
source .venv/bin/activate
python reproduce.py --verify
python figures.py --results reproduced --out reproduced/figures
diff -r figures reproduced/figures
python audit_bekasyl.py
python robustness.py
python figures_bekasyl.py --results reproduced --out reproduced/report_figures
diff -r report_figures reproduced/report_figures
```

An empty `diff` result means the files match. On Windows, activate with `.venv\Scripts\activate`; compare the files with a byte comparison tool instead of `diff`.

## Report to data map

| Evidence | Reproduction file |
|---|---|
| Table 2, 101/120 full answers and 344/360 points | `results/main_results.csv` |
| Table 3, exact tests, Holm correction and 95% intervals | `results/paired_topic_comparisons.csv` |
| Table 4, strict and checkpoint-only sensitivity | `results/sensitivity.csv` |
| Appendix B category counts and all 19 cases | `results/error_summary.csv`, `results/error_audit.csv`, `data/error_codes.csv` |
| Figure 1, six topic-group accuracies | `report_figures/accuracy_by_topic.svg` |
| Figure 2, topic gaps with pointwise intervals | `report_figures/topic_gap_intervals.svg` |
| Figure 3, error category counts | `report_figures/error_categories.svg` |
| Every scored answer with checkpoint flags | `audit/answer_level.csv` |
| Every matched pair and its signed difference | `audit/matched_pairs.csv` |
| Unrounded p-values as exact fractions | `audit/statistics_exact.json` |
| Ecosystem diagnostics and stratified intervals | `diagnostics/`, generated with `robustness.py` |
| Current execution record | `verification_bekasyl.txt` |

The audit recomputes each main-results and sensitivity cell and checks the complete answer grid, quotas, scores and error coverage. It independently obtains the bootstrap endpoints by multinomial enumeration, rather than the original script's convolution. The audit checks the archived scoring decisions; it is not a new independent human assessment of answer correctness.

## Statistical details

The observation for full correctness is an answer; the resampling unit is an established–recent question pair. Each condition has 20 pairs. There is one archived generation per question per condition. The 360 checkpoints are not 360 independent observations.

For discordant pairs, let `b` count established-only correct and `c` recent-only correct. The one-sided exact McNemar probability is `Pr[Binomial(b+c, 0.5) >= b]`. The three raw values are `1/32`, `1/4`, and `9/256`. Holm adjustment across these three comparisons gives `3/32`, `1/4`, and `3/32`. No adjusted result is below 0.05.

The confidence intervals are percentile intervals from the exact empirical distribution of resampling 20 pairs with replacement. This is deterministic and requires no random seed. The intervals are pointwise, assume independent pairs, and do not adjust for the shared ten-question blocks. They do not estimate repeated-generation variation or justify inference to all CS questions. Both tests and intervals were added after the archived results were available.

## What changed in the report

- Clarified the archived freeze record, retrospective statistical plan, and absence of separate simple/strong baselines.
- Completed and tightened Parts 1–3 with operational hypotheses, setup details, formulas, exact probabilities, multiplicity and uncertainty explanations.
- Regenerated the accuracy chart, added the interval chart, and placed the error chart beside the category table in Appendix B.
- Preserved the participants' Additional Analysis, research-question answer, Discussion, sensitivity values, hypothesis table and Appendix B.
- Updated shared reproduction details and the automated-check column in Appendix C; preserved the supplied Mereke record as a report of the earlier release check.

## Items the team must resolve before submission

1. Team size is three. The user clarified that the two-student limit in the assignment sheet is an error and must be ignored; it is not treated as an unresolved requirement.
2. The team confirmed that no protocol was uploaded to Moodle before collection. The question-bank registration is retained, but does not satisfy that separate submission requirement. The report states this deviation. A retrospective form or a ZIP cannot recreate a pre-run upload; do not backdate it.
3. The archived study has three peer conditions, with no separately run simple baseline or literature baseline. This limitation is declared. If the instructor requires new conditions, plan and collect them as new experiments with an appropriate prospective protocol.
4. The supplied RMT_Assignment1_Bekasyl.docx defines the original question but contains no literature review. The subsequently supplied Assignment2_Zhaksylyk_Amantai_Myrzakhan (2).docx contains all four studies discussed here, as well as the directional hypotheses; it confirms the review previously located in Downloads. The report states this provenance accurately. The requirement sheet refers to an Assignment 1 literature review; this numbering mismatch should be clarified if the instructor treats it literally.
5. Original data and results are already tagged upstream. The new supplemental scripts and report figures are not in that remote tag. To publish the supplement, integrate it into the team's repository without silently rewriting the provenance of the original tag.
6. Mereke's earlier reproduction is retained as a supplied record. It is not represented as a fresh human check of this supplement. The students remain responsible for verifying AI-assisted ratings and explaining the report during defence.

No report was uploaded to Moodle, and no remote repository was modified by this preparation.

## Additional robustness evidence

`python robustness.py` regenerates the three CSVs in `diagnostics/`. The exact stratified bootstrap preserves four matched pairs per ecosystem. Removing each ecosystem gives fifteen positive overall gaps; the direction survives all these exclusions. Subgroup results are heterogeneous: Gemini has a -25 pp TypeScript gap, and all three conditions have a zero PostgreSQL gap. These descriptive diagnostics do not establish a causal effect and do not address shared prompt-block dependence. They were added after the original results were known.
