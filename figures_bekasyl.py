"""Rebuild all three report charts from CSV results. Standard library only."""
import argparse
from pathlib import Path
from figures import read_rows, chart_svg, text, rect, errors_chart

def accuracy_chart(rows):
    colors=['#244e78','#057b72']
    labels=[r['condition'] for r in rows if r['group']=='established' and r['condition']!='All conditions']
    plot=[text(65,23,'Fully correct answers (%)',15)]
    for j,label in enumerate(['Established','Recent']):
        x=485+j*130
        plot += [rect(x,10,15,15,colors[j]),text(x+22,23,label,15)]
    for tick in range(0,101,20):
        y=205-1.5*tick
        plot += [f'<path d="M 65 {y} H 750" stroke="#d9e1e9"/>',text(55,y+4,tick,14,'end')]
    for i,label in enumerate(labels):
        center=180+225*i
        for j,group in enumerate(['established','recent']):
            row=next(r for r in rows if r['condition']==label and r['group']==group)
            value=float(row['strict_percent']);x=center-62+64*j;y=205-1.5*value
            plot += [rect(x,y,58,1.5*value,colors[j]),text(x+29,y-7,f'{value:g}%',15,'middle',True)]
        plot.append(text(center,233,label,16,'middle',True))
    return '\n'.join(['<svg xmlns="http://www.w3.org/2000/svg" width="780" height="250" viewBox="0 0 780 250"><title>Fully correct answers by topic group</title><rect width="780" height="250" fill="white"/><g font-family="Arial, sans-serif" fill="#192b40">',*plot,'</g></svg>',''])

def gap_chart(rows):
    plot = [text(32,68,'Established minus recent accuracy, percentage points',15)]
    x0, scale = 205, 8
    for tick in range(0,61,10):
        x = x0 + tick*scale
        plot += [f'<path d="M {x} 92 V 245" stroke="#d9e1e9"/>',text(x,268,tick,14,'middle')]
    plot += [f'<path d="M {x0} 92 V 245" stroke="#718096" stroke-dasharray="4 4"/>']
    for i,r in enumerate(rows):
        y=112+55*i
        lo,hi,gap=[float(r[k]) for k in ['ci_low_pp','ci_high_pp','gap_pp']]
        left,right,mid=[x0+scale*v for v in [lo,hi,gap]]
        plot += [text(32,y+5,r['condition'],16,bold=True),
                 f'<path d="M {left} {y} H {right} M {left} {y-7} V {y+7} M {right} {y-7} V {y+7}" stroke="#244e78" stroke-width="3"/>',
                 f'<circle cx="{mid}" cy="{y}" r="6" fill="#057b72"/>',
                 text(right+12,y+5,f'+{gap:g} [{lo:g}, {hi:g}]',14)]
    plot += [text(32,306,'Pointwise 95% paired percentile bootstrap intervals; 20 pairs per condition.',14),
             text(32,329,'Exploratory. Shared prompt-block dependence is not included.',14)]
    return chart_svg('Topic gaps and uncertainty',860,350,plot)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--results',type=Path,default=Path('results'))
    p.add_argument('--out',type=Path,default=Path('report_figures'))
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    charts={'accuracy_by_topic.svg':accuracy_chart(read_rows(a.results,'main_results')),
            'topic_gap_intervals.svg':gap_chart(read_rows(a.results,'paired_topic_comparisons')),
            'error_categories.svg':errors_chart(read_rows(a.results,'error_summary'))}
    for name,svg in charts.items(): (a.out/name).write_text(svg,encoding='utf-8')
    print('Three report SVG charts written to',a.out)

if __name__=='__main__': main()
