"""Independent arithmetic audit; uses the archived ratings without changing them."""
import csv
import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction
from math import comb, factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def rows(name):
    with (ROOT / 'results' / name).open(newline='') as f:
        return list(csv.DictReader(f))

def save(name, records):
    with (ROOT / 'audit' / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(records[0]), lineterminator='\n')
        w.writeheader(); w.writerows(records)

def main():
    (ROOT / 'audit').mkdir(exist_ok=True)
    raw = (ROOT / 'data/Assignment3_Main_Experiment_Data.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '7ff20f027235b6d4c840b2ee82b0add6bb620b9374ada004779035bd2e34fe1d'
    d = json.loads(raw)
    labels = {x['condition_id']: x['model_label'] for x in d['model_conditions']}
    q = {x['display_id']: x for x in d['questions']}
    assert len(q) == 40
    assert Counter(x['group'] for x in q.values()) == {'established': 20, 'recent': 20}
    assert len(Counter((x['ecosystem'], x['group']) for x in q.values())) == 10
    assert set(Counter((x['ecosystem'], x['group']) for x in q.values()).values()) == {4}
    assert set(Counter((x['block'], x['group']) for x in q.values()).values()) == {5}
    assert set(Counter((x['block'], x['ecosystem']) for x in q.values()).values()) == {2}
    index = {}
    flat = []
    for a in d['responses']:
        key = (a['condition_id'], a['question_id'])
        assert key not in index
        assert all(a[k] == q[key[1]][k] for k in ['group', 'pair_id', 'block', 'ecosystem'])
        assert len(a['checkpoint_points']) == 3 and set(a['checkpoint_points']) <= {0, 1}
        assert a['points'] == sum(a['checkpoint_points'])
        strict = int(all(a['checkpoint_points']) and not a['material_additional_error'])
        assert a['category'] == ('correct' if strict else 'partial')
        index[key] = strict
        flat.append(dict(condition=labels[key[0]], question_id=key[1], pair=a['pair_id'],
                         group=a['group'], block=a['block'], ecosystem=a['ecosystem'],
                         checkpoint_1=a['checkpoint_points'][0], checkpoint_2=a['checkpoint_points'][1],
                         checkpoint_3=a['checkpoint_points'][2], points=a['points'],
                         added_error=int(a['material_additional_error']), fully_correct=strict,
                         checkpoint_only=int(a['points'] == 3)))
    assert set(index) == {(c, i) for c in labels for i in q}
    assert len(flat) == 120
    for r in rows('main_results.csv'):
        s = [x for x in flat if (r['condition'] == 'All conditions' or x['condition'] == r['condition'])
             and (r['group'] == 'overall' or x['group'] == r['group'])]
        assert len(s) == int(r['n'])
        assert sum(x['fully_correct'] for x in s) == int(r['fully_correct'])
        assert len(s) - int(r['fully_correct']) == int(r['partial'])
        assert all(int(r[k]) == 0 for k in ['incorrect', 'abstain', 'missing'])
        assert sum(x['points'] for x in s) == int(r['checkpoint_points'])
        assert int(r['checkpoint_max']) == 3 * len(s)
        assert r['strict_percent'] == f"{100*sum(x['fully_correct'] for x in s)/len(s):.1f}"
        assert r['checkpoint_percent'] == f"{100*sum(x['points'] for x in s)/(3*len(s)):.1f}"
    for r in rows('sensitivity.csv'):
        selected = [x for x in flat if r['condition'] == 'All conditions' or x['condition'] == r['condition']]
        if r['group'].startswith('established-minus'):
            for field, key in [('strict_percent', 'fully_correct'), ('checkpoint_only_percent', 'checkpoint_only')]:
                scores = [Fraction(sum(x[key] for x in selected if x['group'] == g),
                                   sum(x['group'] == g for x in selected)) for g in ['established', 'recent']]
                assert r[field] == f'{float(100*(scores[0]-scores[1])):.1f}'
        else:
            selected = [x for x in selected if r['group'] == 'overall' or x['group'] == r['group']]
            assert int(r['n']) == len(selected)
            for field, key, pct in [('strict_correct', 'fully_correct', 'strict_percent'),
                                    ('checkpoint_only_correct', 'checkpoint_only', 'checkpoint_only_percent')]:
                count = sum(x[key] for x in selected)
                assert int(r[field]) == count and r[pct] == f'{100*count/len(selected):.1f}'
    paired = []
    stats = []
    for c, label in labels.items():
        by_pair = defaultdict(dict)
        for i, question in q.items():
            by_pair[question['pair_id']][question['group']] = i
        differences = []
        for pid, p in sorted(by_pair.items()):
            assert set(p) == {'established', 'recent'}
            assert q[p['established']]['block'] != q[p['recent']]['block']
            e, r = index[c, p['established']], index[c, p['recent']]
            differences.append(e-r)
            paired.append(dict(condition=label, pair=pid, established_id=p['established'],
                               recent_id=p['recent'], established_correct=e, recent_correct=r, difference=e-r))
        n = len(differences); b = differences.count(1); cminus = differences.count(-1)
        assert n == 20
        # Exact binomial survival probability for the one-sided McNemar test.
        pval = Fraction(sum(comb(b+cminus, k) for k in range(b, b+cminus+1)), 2**(b+cminus))
        # Independent multinomial enumeration of the empirical paired bootstrap.
        # This differs from the convolution implementation in reproduce.py.
        mass = Counter()
        probs = [Fraction(b,n), Fraction(cminus,n), Fraction(n-b-cminus,n)]
        for plus in range(n+1):
            for minus in range(n-plus+1):
                zero = n-plus-minus
                ways = factorial(n)//(factorial(plus)*factorial(minus)*factorial(zero))
                mass[plus-minus] += ways*probs[0]**plus*probs[1]**minus*probs[2]**zero
        assert sum(mass.values()) == 1
        endpoints = []
        for alpha in [Fraction(1,40), Fraction(39,40)]:
            cumulative = Fraction(0)
            for value, weight in sorted(mass.items()):
                cumulative += weight
                if cumulative >= alpha:
                    endpoints.append(100*value/n); break
        stats.append(dict(condition=label, b=b, c=cminus, gap=100*sum(differences)/n,
                          low=endpoints[0], high=endpoints[1], p=pval))
    highest = Fraction(0)
    for rank, r in enumerate(sorted(stats,key=lambda x:x['p'])):
        highest = max(highest, min(1, (3-rank)*r['p'])); r['holm'] = highest
    for ref in rows('paired_topic_comparisons.csv'):
        r = next(x for x in stats if x['condition'] == ref['condition'])
        for key, source in [('established_only','b'),('recent_only','c'),('gap_pp','gap'),('ci_low_pp','low'),('ci_high_pp','high')]:
            assert float(ref[key]) == r[source]
        assert ref['raw_p'] == f"{float(r['p']):.4f}"
        assert ref['holm_p'] == f"{float(r['holm']):.4f}"
    errors = rows('error_audit.csv')
    assert len(errors) == 19
    failed = {(x['condition'],x['question_id']) for x in flat if not x['fully_correct']}
    assert {(x['condition'],x['question_id']) for x in errors} == failed
    counts = Counter(x['code'] for x in errors)
    for r in rows('error_summary.csv'):
        assert int(r['count']) == counts[r['code']]
        assert r['percent'] == f"{100*counts[r['code']]/19:.1f}"
    save('answer_level.csv',flat); save('matched_pairs.csv',paired)
    detailed = [{k:(str(v) if isinstance(v,Fraction) else v) for k,v in r.items()} for r in stats]
    (ROOT/'audit/statistics_exact.json').write_text(json.dumps(detailed,indent=2)+'\n')
    print('PASS: archive checksum, 120 unique answers, 40 questions, 20 pairs, ecosystem/block quotas.')
    print('PASS: every cell of main results and sensitivity tables; error counts and coverage.')
    print('PASS: exact McNemar probabilities, Holm correction, independently enumerated bootstrap intervals.')
    print('PASS: 101/120 fully correct; 344/360 points; 19 partial; checkpoint-only 106/120.')
    print('Scope: audit of archived judgments and calculations; no new generations or human rating agreement.')

if __name__ == '__main__':
    main()
