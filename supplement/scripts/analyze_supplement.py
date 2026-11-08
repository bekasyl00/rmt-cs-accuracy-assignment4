"""Rebuild supplementary results from actual saved outputs and explicit ratings.

This program never generates model responses or fills absent ratings.
"""
from __future__ import annotations

import argparse
import hashlib
from collections import Counter
import csv
from fractions import Fraction
from itertools import combinations
import json
from math import comb, sqrt
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parents[2]
SUP = ROOT / "supplement"
sys.path.insert(0, str(ROOT / "analysis"))
from original_results import paired_interval

CONDITIONS = ("simple", "model", "rag")
GROUPS = ("overall", "established", "recent")
CATEGORIES = {"correct", "partial", "incorrect", "abstain", "missing"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_jsonl(path):
    require(path.is_file(), f"Required input missing: {path}")
    result = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            result.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid JSON at {path}:{line_number}: {error}") from error
    return result


def record_key(row):
    condition = row.get("condition")
    require(condition in CONDITIONS, f"Unknown condition: {condition!r}")
    expected_seed = None if condition == "simple" else 17
    require("seed" in row and row["seed"] == expected_seed,
            f"Expected seed {expected_seed!r} for {condition}; got {row.get('seed')!r}")
    question_id = row.get("question_id")
    require(isinstance(question_id, str), "Missing string question_id")
    return condition, question_id


def read_inputs(answers_path, ratings_path):
    question_rows = json.loads((SUP / "protocol/questions_only.json").read_text())
    questions = {q["display_id"]: q for q in question_rows}
    require(len(question_rows) == len(questions) == 40, "Expected 40 unique frozen questions")
    require(Counter(q["group"] for q in questions.values()) == {"established": 20, "recent": 20},
            "Expected 20 questions per topic group")
    expected = {(c, q) for c in CONDITIONS for q in questions}
    answers = {}
    for row in read_jsonl(answers_path):
        key = record_key(row)
        require(key not in answers, f"Duplicate output record: {key}")
        require(key in expected, f"Unexpected output record: {key}")
        require(row.get("status") in {"ok", "failed"}, f"Invalid raw status for {key}")
        q = questions[key[1]]
        for field in ("group", "ecosystem", "pair_id"):
            require(row.get(field) == q[field], f"Raw {field} mismatch for {key}")
        elapsed = row.get("elapsed_seconds")
        require(isinstance(elapsed, (int, float)) and elapsed >= 0, f"Invalid elapsed_seconds for {key}")
        if row["status"] == "ok":
            require(isinstance(row.get("response"), str), f"Successful output has no response for {key}")
        for field in ("generated_tokens", "prompt_tokens"):
            if field in row:
                require(type(row[field]) is int and row[field] >= 0, f"Invalid {field} for {key}")
        answers[key] = row
    require(set(answers) == expected,
            f"Output grid incomplete: missing {sorted(expected-set(answers))}; extra {sorted(set(answers)-expected)}")
    ratings = {}
    for rating in read_jsonl(ratings_path):
        key = record_key(rating)
        require(key in expected and key not in ratings, f"Unexpected or duplicate rating: {key}")
        checkpoints = rating.get("checkpoint_points")
        require(isinstance(checkpoints, list) and len(checkpoints) == 3
                and all(type(value) is int and value in (0, 1) for value in checkpoints),
                f"Expected three binary integer checkpoints for {key}")
        extra = rating.get("material_additional_error")
        require(type(extra) is bool, f"Expected boolean additional-error flag for {key}")
        category = rating.get("category")
        require(category in CATEGORIES, f"Unknown category for {key}: {category!r}")
        require(isinstance(rating.get("reason"), str) and rating["reason"].strip(),
                f"A rating reason is required for {key}")
        points = sum(checkpoints)
        if "points" in rating:
            require(rating["points"] == points, f"Supplied points do not sum for {key}")
        if answers[key]["status"] == "failed":
            computed = "missing"
            require(points == 0 and not extra, f"Failed output cannot earn points for {key}")
        elif category == "abstain":
            computed = "abstain"
            require(points == 0 and not extra, f"Abstention cannot earn points or add a claim error for {key}")
        elif points == 3 and not extra:
            computed = "correct"
        elif points > 0:
            computed = "partial"
        else:
            computed = "incorrect"
        require(category == computed, f"Category/rubric mismatch for {key}: {category} versus {computed}")
        if "response_sha256" in rating:
            digest=hashlib.sha256((answers[key].get("response") or "").encode()).hexdigest()
            require(digest == rating["response_sha256"], f"Rating refers to a different response for {key}")
        ratings[key] = dict(rating, points=points, fully_correct=int(computed == "correct"))
    require(set(ratings) == expected,
            f"Rating grid incomplete: missing {sorted(expected-set(ratings))}; extra {sorted(set(ratings)-expected)}")
    pairs = {}
    for qid, q in questions.items():
        pair = pairs.setdefault(q["pair_id"], {})
        require(q["group"] not in pair, f"Duplicate topic group in pair {q['pair_id']}")
        pair[q["group"]] = qid
    require(len(pairs) == 20 and all(set(p) == {"established", "recent"} for p in pairs.values()),
            "Expected 20 complete established–recent pairs")
    return questions, answers, ratings, pairs


def percent(numerator, denominator):
    return 100 * numerator / denominator if denominator else None


def wilson(successes, n):
    """Two-sided 95% Wilson score interval; never treat checkpoint trials as independent."""
    z = 1.959963984540054
    p = successes / n
    denominator = 1 + z*z/n
    center = (p + z*z/(2*n)) / denominator
    half = z * sqrt(p*(1-p)/n + z*z/(4*n*n)) / denominator
    return max(0, center-half)*100, min(1, center+half)*100


def main_metrics(questions, ratings):
    main, sensitivity = [], []
    for condition in CONDITIONS:
        for group in GROUPS:
            selected = [ratings[condition, qid] for qid, q in questions.items()
                        if group == "overall" or q["group"] == group]
            counts = Counter(r["category"] for r in selected)
            n = len(selected)
            correct = counts["correct"]
            observed = n-counts["missing"]
            points = sum(r["points"] for r in selected)
            low, high = wilson(correct, n)
            main.append(dict(condition=condition, group=group, n=n, observed=observed,
                             fully_correct=correct, partial=counts["partial"], incorrect=counts["incorrect"],
                             abstain=counts["abstain"], missing=counts["missing"],
                             strict_percent=percent(correct,n), ci_low_percent=low, ci_high_percent=high,
                             checkpoint_points=points, checkpoint_max=3*n,
                             checkpoint_percent=percent(points,3*n), observed_strict_percent=percent(correct,observed)))
            checkpoint_only = sum(r["points"] == 3 for r in selected)
            sensitivity.append(dict(condition=condition,group=group,n=n,strict_correct=correct,
                                    checkpoint_only_correct=checkpoint_only,strict_percent=percent(correct,n),
                                    checkpoint_only_percent=percent(checkpoint_only,n),
                                    added_error_penalties=checkpoint_only-correct))
    return main, sensitivity


def exact_mcnemar(b, c, alternative):
    discordant = b+c
    if not discordant:
        return Fraction(1)
    if alternative == "greater":
        return Fraction(sum(comb(discordant,k) for k in range(b,discordant+1)),2**discordant)
    require(alternative == "two-sided", "Unsupported alternative")
    return min(Fraction(1),2*Fraction(sum(comb(discordant,k) for k in range(min(b,c)+1)),2**discordant))


def paired_metrics(questions, ratings, pairs):
    comparisons = []
    for first,second in (("model","simple"),("rag","simple"),("rag","model")):
        differences = [ratings[first,qid]["fully_correct"]-ratings[second,qid]["fully_correct"]
                       for qid in questions]
        comparisons.append((f"{first}_minus_{second}","between_methods",first,second,"two-sided",differences))
    for condition in ("model","rag"):
        differences = [ratings[condition,p["established"]]["fully_correct"]
                       -ratings[condition,p["recent"]]["fully_correct"] for p in pairs.values()]
        comparisons.append((f"{condition}_established_minus_recent","within_condition_topics",
                            condition+":established",condition+":recent","greater",differences))
    rows = []
    probabilities = []
    for identifier,kind,first,second,alternative,differences in comparisons:
        n = len(differences)
        b,c = differences.count(1),differences.count(-1)
        raw_p = exact_mcnemar(b,c,alternative)
        low,high = paired_interval(differences)
        probabilities.append(raw_p)
        rows.append(dict(comparison=identifier,comparison_type=kind,first=first,second=second,
                         alternative=alternative,n=n,first_only=b,second_only=c,
                         gap_pp=100*sum(differences)/n,ci_low_pp=float(low),ci_high_pp=float(high),
                         raw_p=float(raw_p),holm_p=None,raw_p_fraction=str(raw_p),holm_p_fraction=None))
    previous = Fraction(0)
    for rank,index in enumerate(sorted(range(len(rows)),key=lambda i: probabilities[i])):
        adjusted = min(Fraction(1),max(previous,(len(rows)-rank)*probabilities[index]))
        rows[index]["holm_p"] = float(adjusted)
        rows[index]["holm_p_fraction"] = str(adjusted)
        previous = adjusted
    return rows


def quantile(values, probability):
    """Linear-interpolated empirical quantile, equivalent to inclusive type 7."""
    ordered = sorted(values)
    if not ordered:
        return None
    position = (len(ordered)-1)*probability
    lower = int(position)
    upper = min(lower+1,len(ordered)-1)
    return ordered[lower]+(position-lower)*(ordered[upper]-ordered[lower])


def efficiency_metrics(answers):
    rows=[]
    for condition in CONDITIONS:
        all_records=[r for (c,_),r in answers.items() if c==condition]
        successful=[r for r in all_records if r["status"]=="ok"]
        elapsed=[r["elapsed_seconds"] for r in successful]
        q1,q3=quantile(elapsed,.25),quantile(elapsed,.75)
        rows.append(dict(condition=condition,n_successful=len(successful),
                         latency_median_seconds=statistics.median(elapsed) if elapsed else None,
                         latency_q1_seconds=q1,latency_q3_seconds=q3,
                         latency_iqr_seconds=q3-q1 if q1 is not None else None,
                         total_elapsed_seconds=sum(r["elapsed_seconds"] for r in all_records),
                         generated_tokens=sum(r.get("generated_tokens",0) for r in successful),
                         prompt_tokens=sum(r.get("prompt_tokens",0) for r in successful)))
    return rows


def answer_audit(questions, answers, ratings):
    rows=[]
    for condition in CONDITIONS:
        for qid,q in questions.items():
            raw,rating=answers[condition,qid],ratings[condition,qid]
            rows.append(dict(question_id=qid,condition=condition,seed=rating["seed"],group=q["group"],
                             ecosystem=q["ecosystem"],pair_id=q["pair_id"],raw_status=raw["status"],
                             checkpoint_1=rating["checkpoint_points"][0],checkpoint_2=rating["checkpoint_points"][1],
                             checkpoint_3=rating["checkpoint_points"][2],points=rating["points"],
                             material_additional_error=rating["material_additional_error"],category=rating["category"],
                             reason=rating["reason"],error_type=rating.get("error_type",rating.get("code","")),
                             elapsed_seconds=raw["elapsed_seconds"]))
    return rows


def retrieval_coverage(questions, answers):
    archive=json.loads((ROOT/"data/Assignment3_Main_Experiment_Data.json").read_text())
    reference_ids={q["display_id"]:set(q["source_ids"]) for q in archive["questions"]}
    rows=[]
    for condition in ("simple","rag"):
        for group in GROUPS:
            ids=[qid for qid,q in questions.items() if group=="overall" or q["group"]==group]
            retrieved=[{chunk["source_id"] for chunk in answers[condition,qid].get("retrieval",[])} for qid in ids]
            hits=sum(bool(source_ids & reference_ids[qid]) for qid,source_ids in zip(ids,retrieved))
            rows.append(dict(condition=condition,group=group,n=len(ids),any_reference_source_retrieved=hits,
                             reference_source_hit_percent=percent(hits,len(ids)),
                             mean_distinct_retrieved_sources=statistics.mean(len(s) for s in retrieved)))
    return rows


def write_csv(path,rows):
    require(rows,"Cannot write a CSV without schema/data")
    with path.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
        writer.writeheader();writer.writerows(rows)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--answers",type=Path,default=SUP/"raw/answers.jsonl")
    p.add_argument("--ratings",type=Path,default=SUP/"raw/ratings.jsonl")
    p.add_argument("--out",type=Path,default=SUP/"results")
    args=p.parse_args()
    questions,answers,ratings,pairs=read_inputs(args.answers,args.ratings)
    main_rows,sensitivity=main_metrics(questions,ratings)
    audit=answer_audit(questions,answers,ratings)
    outputs={"main_results.csv":main_rows,"sensitivity.csv":sensitivity,
             "paired_comparisons.csv":paired_metrics(questions,ratings,pairs),
             "efficiency.csv":efficiency_metrics(answers),"answer_audit.csv":audit,
             "retrieval_coverage.csv":retrieval_coverage(questions,answers)}
    failures=[r for r in audit if r["category"]!="correct"]
    args.out.mkdir(parents=True,exist_ok=True)
    for filename,rows in outputs.items():write_csv(args.out/filename,rows)
    with (args.out/"error_cases.csv").open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(audit[0]),lineterminator="\n")
        writer.writeheader();writer.writerows(failures)
    print("Verified complete grid: 40 questions × 3 conditions; 120 explicit ratings.")
    for row in main_rows:
        if row["group"]=="overall":
            print(f"{row['condition']}: {row['fully_correct']}/{row['n']} fully correct; "
                  f"{row['checkpoint_points']}/{row['checkpoint_max']} checkpoints; "
                  f"{row['missing']} missing")
    print(f"Wrote {len(outputs)+1} CSVs to {args.out}. All five supplementary tests share one Holm family.")


if __name__=="__main__":main()
