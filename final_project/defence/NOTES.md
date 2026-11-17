# Final defence script

This script follows Final_Presentation.pdf, slides 1–10. Speak in simple English. The schedule totals 10 minutes, including slide changes and short pauses. Every author should understand the whole study.

| Speaker | Slides | Time |
|---|---|---|
| Zere | 1–3 and 10 | 3 minutes |
| Bekasyl | 4–6 | 3 minutes 30 seconds |
| Mereke | 7–9 | 3 minutes 30 seconds |

## Slide 1 — Title
Zere · 20 seconds

Hello. We are Bekasyl, Zere and Mereke. Our research studies the accuracy of AI answers about established concepts and recent software features. We also test whether official documentation helps a small local model. Our main contribution is a question bank with clear scoring rules and results that other people can check.

## Slide 2 — Why accuracy matters
Zere · 40 seconds

Students and developers use AI to explain concepts, solve problems and choose APIs. But a clear answer can still contain a wrong module name or an outdated rule. This matters because users may trust the explanation without checking the exact software version. We ask whether recent features are harder for these assistants than established concepts. We focus on factual explanations, rather than complete programs or user preferences.

## Slide 3 — Research gap
Zere · 60 seconds

Previous research gives us four useful starting points. Kabir and colleagues studied errors in ChatGPT answers to Stack Overflow questions. Kandpal and colleagues studied how knowledge frequency relates to factual accuracy. Vu and colleagues studied changing facts and search support. Wang and colleagues studied deprecated software APIs.

Our study connects these concerns in a smaller, specific setting. We compare established and recent software questions using the same scoring rules and official documentation. The questions are paired by ecosystem and task type. This does not mean that their difficulty is exactly equal. Our results also cannot be compared directly with percentages from those other datasets. Bekasyl will now explain our design and main results.

## Slide 4 — Research question and objectives
Bekasyl · 55 seconds

Our main question is: how does factual accuracy differ between established concepts and recent software features when assistants are instructed not to search?

We built forty questions: twenty established and twenty recent. We checked each question against official sources and defined three required facts, called checkpoints. We then compared the recorded answers and calculated paired statistical tests. Finally, we added a separate local experiment to explore whether documentation helps Qwen. This supplement answers an additional question; it does not replace the original comparison. The website lets us inspect all questions, answers and scores.

## Slide 5 — Methodology
Bekasyl · 80 seconds

We used five ecosystems: Python, PostgreSQL, TypeScript, Node.js and Git. Each has four established and four recent questions. The forty questions form twenty pairs. Established concepts were documented before 2020. The selected recent features first appeared in 2025.

The original archive contains forty answers from each of three recorded interfaces. We preserve their reported model labels, but cannot independently verify the actual backend versions. The prompt instructed them not to search.

The supplement has three conditions. The simple baseline returns keyword-matched documentation passages. Qwen answers without documents. RAG gives the same Qwen model three passages selected by BM25. The two Qwen conditions use the same model weights and generation settings.

An answer is fully correct only when it satisfies all three checkpoints and adds no important false claim. We also report partial credit. The ratings were AI-assisted, so independent human agreement is a limitation. We preserve every output, including errors.

## Slide 6 — Main results
Bekasyl · 75 seconds

The original experiment has 101 fully correct answers out of 120. Across all answers, 344 of 360 checkpoints were satisfied. These are different measures: an answer can earn some checkpoint points without being fully correct.

GPT scored twenty out of twenty on established questions and fifteen on recent questions. Sonnet scored nineteen and seventeen. Gemini scored eighteen and twelve. The accuracy gaps are twenty-five, ten and thirty percentage points.

We used exact McNemar tests for paired binary outcomes and Holm correction for multiple comparisons. The adjusted p-values are about 0.094, 0.25 and 0.094. None is below 0.05. We therefore report an observed direction, not a statistically established difference. The tests are exploratory because they were added retrospectively. Mereke will explain the supplementary experiment and what the results mean.

## Slide 7 — Supplementary experiment and error examples
Mereke · 80 seconds

All supplementary conditions answered the same forty questions. Keyword extraction and Qwen alone each scored four fully correct answers. Qwen with BM25 scored six. That is ten percent, ten percent and fifteen percent. The observed RAG improvement is five percentage points, but all between-method adjusted p-values are one. We cannot claim a reliable general improvement.

One example explains how documents can help. Question V2Q40 asks about Python 3.14. Qwen named the third-party zstandard package instead of the required standard-library module compression.zstd. With documentation, it supplied the correct module and improved from one checkpoint to three.

However, on V2Q01, RAG still made a wrong claim about TypeScript string-enum reverse mapping. It scored only one checkpoint. Finding a relevant document and correctly using it are separate challenges. These examples and their full answers are available on our website.

## Slide 8 — Discussion and meaning
Mereke · 60 seconds

In the original archive, every recorded condition performed better on established questions. This agrees with concerns in earlier work about freshness, knowledge coverage and changing APIs. But agreement in direction does not prove the same cause.

We did not randomly assign topic age, and the question pairs may differ in difficulty. The adjusted tests were not significant. We therefore cannot say that recentness itself caused the errors, or that one provider is generally better.

The practical message is to check exact software-version claims against official documentation. This is useful even when an AI answer sounds confident or includes retrieved passages. Our work makes those mistakes visible and traceable.

## Slide 9 — Contribution and limitations
Mereke · 70 seconds

Our contribution is an auditable benchmark for version-specific technical explanations. It contains forty source-linked questions, three checkpoints per question, saved answers, rating reasons and reproducible calculations. Another person can inspect a score and trace it to the answer and reference facts.

The main limitations are the small selected question bank, imperfect difficulty matching, uncertain original backend settings and AI-assisted ratings. The supplement reused a known bank and tested only one small quantized model in one pass. These conditions limit how far we can generalize.

Future work should use unseen questions, independent human raters and broader model and retrieval settings. It should also record the analysis plan before collecting responses. Zere will finish with our conclusion, journal choice and reproducibility package.

## Slide 10 — Conclusion and journal
Zere · 60 seconds

Our conclusion is that recent software features had lower observed accuracy in all three original conditions. However, the differences were not significant after Holm correction. Retrieval helped some answers, but the small overall gain was uncertain.

Our primary journal is Applied Sciences, and Electronics is the backup. Applied Sciences publishes empirical work on programming assistance and AI evaluation. Both journals are active in the official October 2026 Scopus source list. Direct category and percentile verification remains open.

The command on this slide reproduces all Results tables and figures from saved evidence. Zere and Mereke also successfully checked the final project on 17 November, as confirmed by Bekasyl. The website contains all 240 answers. Submission to a journal is separate from this course project. Thank you. We are ready for your questions.

## Showing evidence during questions

Run from the extracted Final_Project folder:

```bash
python3 research/reproduce_manuscript.py --verify
```

Expected final message: `PASS: 6 manuscript tables and 3 vector figures reproduced from checked evidence.` Earlier output also verifies 22 CSV/SVG files. This recalculates saved ratings; it does not generate new answers or measure agreement between human raters.

Open `manuscript/NUMBER_SOURCES.csv` to trace a table to its output file. Use the website for answer-level evidence:

- Helpful retrieval example: https://elaborate-starship-e9c848.netlify.app/?experiment=supplement&item=V2Q40
- Remaining error: https://elaborate-starship-e9c848.netlify.app/?experiment=supplement&item=V2Q01
- Offline backup: open `site/index.html`.

Keep the live demonstration for questions unless the presentation is running ahead of schedule.

## Short answers for individual defence

**What is the contribution in one sentence?**
We provide a small, inspectable benchmark for version-specific AI explanations, with source-backed scoring and reproducible comparisons.

**What is a benchmark?**
A fixed set of tasks, reference answers and scoring rules used to compare systems.

**What is a baseline, and why is yours appropriate?**
A baseline is a reference method. Keyword extraction shows what document matching alone can provide. Qwen alone lets us compare the same model with and without retrieved documents. Qwen is a practical local baseline, not a claim of state-of-the-art strength.

**Is the comparison completely fair?**
The Qwen versus RAG comparison holds model weights and decoding settings constant. Keyword extraction uses a different retrieval method and does not generate an explanation, so that comparison changes more than one component. We state this limitation. We do not rank the proprietary and local models as one controlled experiment.

**What are RAG and BM25?**
RAG means retrieval-augmented generation. We retrieve documents and give them to a model as context. BM25 ranks passages using query-word matches, word rarity and document length. It is a lexical method, not an embedding model.

**Why use McNemar instead of comparing two unrelated percentages?**
The outcomes are binary and paired. McNemar uses discordant pairs, where one outcome is correct and the other is not. We use the exact test because the counts are small. Original pairs connect established and recent questions; supplementary pairs compare methods on the same question.

**What does Holm correction do?**
It adjusts a family of p-values to reduce the risk of false positive findings from multiple tests. The original family has three tests. The supplementary family has five.

**Does a p-value of one prove that methods are equal?**
No. It means this test does not provide evidence against its null hypothesis. Our small sample can miss real differences. RAG versus Qwen has a paired interval from minus 7.5 to plus 17.5 percentage points.

**Why can a confidence interval exclude zero while the adjusted test is not significant?**
The displayed original bootstrap intervals are pointwise and unadjusted. Holm adjusts the test family. They answer different inferential questions, so we follow the adjusted tests for our significance claims.

**Where does 101/120 come from?**
The original strict correct counts are 35, 36 and 30. Their sum is 101. There are forty answers per condition, so the denominator is 120. The verification script checks these counts against saved ratings.

**Why are checkpoint accuracy and full-answer accuracy different?**
Checkpoint accuracy gives partial credit for individual required facts. Full-answer accuracy requires all three facts and no material added error. Therefore 344/360 checkpoint points does not mean 344 correct answers.

**Why are the local scores low?**
They are observed results for one small four-bit model, a short generation budget and a strict rubric. The question bank includes recent, specific features. These factors may contribute, but we did not isolate their causal effects.

**Which prior study is closest?**
Kabir and colleagues are close in evaluating factual problems in developer-facing AI explanations. Our narrower contribution compares established and recent version-specific questions using explicit checkpoints. Their dataset and percentages are not directly comparable with ours.

**What is the main threat to validity?**
The small purposive question bank may not represent other software questions, and difficulty may differ between topic groups. AI-assisted ratings and unknown original backend settings add uncertainty.

**Did the team repeat model generation during verification?**
No. Verification reruns the analysis of saved outputs and ratings. Fresh generation is a different procedure that needs the local model and its environment.

**Was the protocol preregistered in Moodle?**
No. The original protocol was not uploaded before collection. A local supplementary manifest preceded supplementary generation, but it was not Moodle preregistration. We describe the analysis as exploratory.

**Why Applied Sciences?**
It publishes empirical studies on programming assistance and AI evaluation, including Christakis and Drikakis and Taneski and colleagues. We use its template and discuss three recent related articles in Appendix A. Journal acceptance is not guaranteed.
