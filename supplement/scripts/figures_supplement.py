"""Generate supplementary SVG plots exclusively from the actual main-results CSV."""
import argparse
import csv
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
SUP=ROOT/'supplement'
sys.path.insert(0,str(ROOT/"analysis"))
from plot_original import chart_svg,rect,text

CONDITIONS=('simple','model','rag')
LABELS={'simple':'Keyword search','model':'Qwen code model','rag':'Qwen + BM25 RAG'}
COLORS=('#244e78','#057b72')


def read_results(folder):
    with (folder/'main_results.csv').open(encoding='utf-8',newline='') as f:
        rows=list(csv.DictReader(f))
    result={(r['condition'],r['group']):r for r in rows}
    expected={(c,g) for c in CONDITIONS for g in ['overall','established','recent']}
    if set(result)!=expected or len(rows)!=len(expected):
        raise ValueError('Expected exactly three conditions × overall/established/recent in main_results.csv')
    for (condition,group),r in result.items():
        if int(r['n'])!=(40 if group=='overall' else 20):raise ValueError('Unexpected planned denominator')
        for key in ['strict_percent','checkpoint_percent','ci_low_percent','ci_high_percent']:
            if not 0<=float(r[key])<=100:raise ValueError(f'Invalid {key}: {r[key]}')
        if not float(r['ci_low_percent'])<=float(r['strict_percent'])<=float(r['ci_high_percent']):
            raise ValueError('Rate lies outside its reported interval')
    return result


def topic_accuracy(rows):
    content=[text(32,68,'Twenty planned questions per topic and condition. Whiskers: 95% Wilson intervals.',15)]
    for i,label in enumerate(['Established','Recent']):
        x=550+135*i
        content += [rect(x,83,16,16,COLORS[i]),text(x+23,96,label,14)]
    bottom,scale=333,2.1
    for tick in range(0,101,20):
        y=bottom-scale*tick
        content += [f'<path d="M 75 {y} H 815" stroke="#d9e1e9"/>',text(64,y+4,f'{tick}%',14,'end')]
    for i,condition in enumerate(CONDITIONS):
        center=195+245*i
        for j,group in enumerate(['established','recent']):
            r=rows[condition,group]
            value,low,high=[float(r[k]) for k in ['strict_percent','ci_low_percent','ci_high_percent']]
            x=center-58+j*64
            content.append(rect(x,bottom-scale*value,52,scale*value,COLORS[j]))
            mid=x+26;top=bottom-scale*high;lower=bottom-scale*low
            content.append(f'<path d="M {mid} {top} V {lower} M {mid-7} {top} H {mid+7} M {mid-7} {lower} H {mid+7}" stroke="#111827" stroke-width="1.8"/>')
            content.append(text(mid,bottom+22,f"{value:g}%",14,'middle',True))
            content.append(text(mid,bottom+40,f"{r['fully_correct']}/{r['n']}",13,'middle'))
        content.append(text(center,bottom+66,LABELS[condition],16,'middle',True))
    content.append(text(32,433,'Single deterministic run. Pointwise intervals do not model ecosystem or shared-block dependence.',14))
    return chart_svg('Supplementary full-correct accuracy',860,457,content)


def strict_vs_checkpoints(rows):
    content=[text(32,68,'Overall saved responses. Both measures use all planned items; their denominators differ.',15)]
    for j,label in enumerate(['Fully correct answers','Checkpoint points']):
        x=440+j*205
        content += [rect(x,83,16,16,COLORS[j]),text(x+23,96,label,14)]
    x0,scale=195,5.8
    for tick in range(0,101,20):
        x=x0+scale*tick
        content += [f'<path d="M {x} 115 V 341" stroke="#d9e1e9"/>',text(x,365,f'{tick}%',14,'middle')]
    for i,condition in enumerate(CONDITIONS):
        r=rows[condition,'overall'];center=145+i*80
        content.append(text(32,center+10,LABELS[condition],16,bold=True))
        for j,key in enumerate(['strict_percent','checkpoint_percent']):
            value=float(r[key]);y=center-15+j*27
            content.append(rect(x0,y,scale*value,20,COLORS[j]))
            ratio=f"{r['fully_correct']}/{r['n']}" if j==0 else f"{r['checkpoint_points']}/{r['checkpoint_max']}"
            content.append(text(x0+scale*value+8,y+15,f'{value:.1f}% ({ratio})',14,bold=True))
    content += [text(32,391,'Full correctness requires 3/3 checkpoints and no material added factual error.',14),
                text(32,414,'Checkpoint percentage retains credit for correctly supplied facts in partial answers.',14)]
    return chart_svg('Complete-answer reliability and checkpoint coverage',960,440,content)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results',type=Path,default=SUP/'results')
    parser.add_argument('--out',type=Path,default=SUP/'figures')
    args=parser.parse_args()
    rows=read_results(args.results)
    charts={'supplement_accuracy_by_topic.svg':topic_accuracy(rows),
            'supplement_strict_vs_checkpoints.svg':strict_vs_checkpoints(rows)}
    args.out.mkdir(parents=True,exist_ok=True)
    for name,svg in charts.items():(args.out/name).write_text(svg,encoding='utf-8')
    print('Wrote two plots from actual main_results.csv to',args.out)


if __name__=='__main__':main()
