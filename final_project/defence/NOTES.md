# Ten-minute defence

Total planned time: 600 seconds. Each person must also understand the whole study.

## Slide 1 — Accuracy of AI Answers

Zere · 45 seconds

Our study asks whether AI answers are equally accurate for old software concepts and recent features. We study short explanations, not complete applications. Our main contribution is a small question bank with official sources, clear scoring rules and reproducible results. We also test whether documents help a small local model.

## Slide 2 — Why this matters and what is missing

Zere · 60 seconds

A fluent answer can still be wrong about a software version. Kabir and colleagues studied ChatGPT answers to Stack Overflow questions. FreshLLMs studied changing facts and search support. Wang and colleagues studied deprecated APIs in code completion. Our study has a narrower focus: applied explanations of established and recent software features. We do not compare our percentages directly with their different datasets.

## Slide 3 — Questions and scoring

Bekasyl · 70 seconds

We used forty English questions and twenty pairs. Each ecosystem has four established and four recent questions. The pairs match the ecosystem and type of task, but we did not prove equal difficulty. Each question has three facts checked against official documentation. An answer is fully correct only if it gives all three facts and adds no important false claim. Partial credit is reported separately. The original research question asks whether established-topic accuracy is higher.

## Slide 4 — Two experiments with different purposes

Bekasyl · 65 seconds

The original archive records GPT, Sonnet and Gemini interface labels. We cannot independently verify the actual backend versions or all interface settings. The separate supplement uses Qwen2.5-Coder-3B on a local computer. The simple baseline returns keyword-matched documentation passages. Qwen alone answers without documents. RAG gives the same Qwen model the top three BM25 passages. The last two conditions share model weights and decoding settings. We use paired tests because conditions answer the same questions, and Holm correction because we make several comparisons.

## Slide 5 — Original results favor established topics

Bekasyl · 70 seconds

The original archive has 101 fully correct answers out of 120, and 344 successful checkpoints out of 360. GPT scored twenty established and fifteen recent answers correctly. Sonnet scored nineteen and seventeen. Gemini scored eighteen and twelve. This gives established-minus-recent gaps of twenty-five, ten and thirty percentage points. These are descriptive results on our selected questions, not a general ranking of model providers.

## Slide 6 — Observed gaps are not adjusted significance

Bekasyl · 60 seconds

The graph shows uncertainty around each gap. The adjusted p-values are about 0.094, 0.25 and 0.094. None is below 0.05. Therefore we cannot claim a statistically established effect after correcting for the three tests. Some individual intervals exclude zero, but they are pointwise intervals and are not adjusted for multiple comparisons. The tests were also added retrospectively, so we call the inference exploratory.

## Slide 7 — Retrieval produced a small uncertain gain

Mereke · 60 seconds

In the supplement, keyword extraction and Qwen alone each gave four fully correct answers out of forty. Qwen with retrieved documents gave six. The observed gain is five percentage points. The adjusted p-value for RAG versus Qwen is one, and the confidence interval includes both a loss and a gain. This result does not show that retrieval is useless or always helpful. It describes one small model, one short generation setting and one known question bank.

## Slide 8 — A document can help and still be misread

Mereke · 60 seconds

For the Python 3.14 question, Qwen named the third-party zstandard package. The question required the standard-library module compression.zstd. With retrieved documentation, the model supplied the correct module and functions and improved from one checkpoint to three. But on the TypeScript string-enum question, RAG still claimed reverse mapping incorrectly. These examples show the difference between finding a relevant document and using its content correctly.

## Slide 9 — What we can and cannot conclude

Mereke · 65 seconds

Our useful result is an auditable way to inspect version-specific technical answers. The evidence suggests extra caution with recent features in the original archive, but does not prove that recency caused the mistakes. We have a small purposive sample, imperfect matching and no independent human agreement study. A stronger follow-up should use unseen questions, independent raters, preregistered analysis and fully recorded settings. Users should verify exact API and version claims, even when an answer includes documents.

## Slide 10 — Journal fit and reproducibility

Zere · 45 seconds

Applied Sciences is our primary journal because it publishes programming-assistance and empirical AI-evaluation studies. Electronics is the backup. Both appear active in the official October Scopus list. Our package includes the data, ratings, scripts and exact table mapping. The command on the slide regenerates all Results tables and figures without downloading a model. The release is named final. Author approval, the university similarity check and an outside-team reproduction are still separate publication-readiness steps.

## Showing evidence

Run `python3 research/reproduce_manuscript.py --verify` from the project folder. Open `manuscript/NUMBER_SOURCES.csv` to find the export for a displayed table. The command recalculates saved judgments; it does not generate new model answers or measure human-rater agreement.
