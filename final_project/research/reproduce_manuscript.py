"""Reproduce historical evidence and every manuscript table and vector figure."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / 'manuscript' / 'assets'

def read(relative):
    with (ROOT / relative).open(newline='') as stream:
        return list(csv.DictReader(stream))

def write(name, headers, rows):
    with (OUT / name).open('w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(headers)
        writer.writerows(rows)

def interval(correct, total):
    z = 1.959963984540054
    rate = correct / total
    denominator = 1 + z*z/total
    centre = (rate + z*z/(2*total))/denominator
    half = z*math.sqrt(rate*(1-rate)/total + z*z/(4*total*total))/denominator
    return f'{100*(centre-half):.1f}–{100*(centre+half):.1f}'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    subprocess.run([sys.executable, 'reproduce_all.py', '--verify'], cwd=ROOT, check=True)
    OUT.mkdir(parents=True, exist_ok=True)
    originals = read('results/main_results.csv')
    rows = []
    for r in originals:
        if r['group'] != 'overall' or r['condition'] == 'All conditions':
            continue
        groups = {x['group']: x for x in originals if x['condition'] == r['condition']}
        rows.append([r['condition'], f"{r['fully_correct']}/40 ({float(r['strict_percent']):.1f}%)", interval(int(r['fully_correct']),40), groups['established']['fully_correct']+'/20', groups['recent']['fully_correct']+'/20', r['checkpoint_points']+'/120'])
    write('Table_1_original_accuracy.csv', ['Condition','Overall correct','95% CI (%)','Established','Recent','Checkpoints'],rows)
    rows = [[r['condition'],r['gap_pp'],r['ci_low_pp']+'–'+r['ci_high_pp'],r['established_only']+'/'+r['recent_only'],r['raw_p'],r['holm_p']] for r in read('results/paired_topic_comparisons.csv')]
    write('Table_2_original_tests.csv',['Condition','Gap (pp)','95% CI (pp)','E only/R only','Raw p','Holm p'],rows)
    labels={'simple':'Keyword search','model':'Qwen','rag':'Qwen + BM25'}
    rows=[]
    for r in read('supplement/results/main_results.csv'):
        if r['group']=='overall':
            rows.append([labels[r['condition']],r['fully_correct']+'/40',f"{float(r['strict_percent']):.1f}", f"{float(r['ci_low_percent']):.1f}–{float(r['ci_high_percent']):.1f}",r['checkpoint_points']+'/120',r['partial']+'/'+r['incorrect']])
    write('Table_3_supplement_accuracy.csv',['Condition','Correct','Accuracy (%)','95% CI (%)','Checkpoints','Partial/incorrect'],rows)
    names=['Qwen − search','RAG − search','RAG − Qwen','Qwen E − R','RAG E − R']
    rows=[]
    for name,r in zip(names,read('supplement/results/paired_comparisons.csv')):
        rows.append([name,f"{float(r['gap_pp']):.1f}",f"{float(r['ci_low_pp']):.1f}–{float(r['ci_high_pp']):.1f}",r['first_only']+'/'+r['second_only'],f"{float(r['raw_p']):.4f}",f"{float(r['holm_p']):.4f}"])
    write('Table_4_supplement_tests.csv',['Comparison','Gap (pp)','95% CI (pp)','First/second only','Raw p','Holm p'],rows)
    rows=[]
    for path in ['results/sensitivity.csv','supplement/results/sensitivity.csv']:
        for r in read(path):
            if r['group']=='overall' and r['condition']!='All conditions':
                rows.append([labels.get(r['condition'],r['condition']),r['strict_correct']+'/40',r['checkpoint_only_correct']+'/40',f"{float(r['strict_percent']):.1f}",f"{float(r['checkpoint_only_percent']):.1f}"])
    write('Table_5_scoring_sensitivity.csv',['Condition','Strict count','Checkpoint-only count','Strict (%)','Checkpoint-only (%)'],rows)
    coverage={r['condition']:r for r in read('supplement/results/retrieval_coverage.csv') if r['group']=='overall'}
    rows=[]
    for r in read('supplement/results/efficiency.csv'):
        c=r['condition']
        rows.append([labels[c],f"{float(r['latency_median_seconds']):.4f}",f"{float(r['latency_q1_seconds']):.4f}–{float(r['latency_q3_seconds']):.4f}",f"{float(r['latency_iqr_seconds']):.4f}",coverage[c]['any_reference_source_retrieved']+'/40' if c in coverage else 'N/A'])
    write('Table_6_efficiency.csv',['Condition','Median (s)','Q1–Q3 (s)','IQR (s)','Reference-source hit'],rows)
    sources = ['report_figures/accuracy_by_topic.svg','report_figures/topic_gap_intervals.svg','supplement/figures/supplement_accuracy_by_topic.svg']
    for number,source in enumerate(sources,1):
        shutil.copyfile(ROOT/source,OUT/f'Figure_{number}.svg')
    manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir()) if p.suffix in {'.csv','.svg'}}
    manifest_path=ROOT/'manuscript_reference_outputs.json'
    if args.verify:
        expected=json.loads(manifest_path.read_text())
        if manifest!=expected:
            raise RuntimeError('Manuscript export hashes differ from the handoff references')
    else:
        manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    print('PASS: 6 manuscript tables and 3 vector figures reproduced from checked evidence.')

if __name__=='__main__':
    main()
