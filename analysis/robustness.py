"""Post hoc diagnostics preserving the five fixed ecosystem quotas."""
import csv
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from original_results import read_archive, fully_correct, paired_interval

ROOT=Path(__file__).resolve().parents[1]

def convolve(a,b):
    out=Counter()
    for x,w in a.items():
        for y,v in b.items():out[x+y]+=w*v
    return out

def write(name,records):
    (ROOT/'diagnostics').mkdir(exist_ok=True)
    with (ROOT/'diagnostics'/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n')
        w.writeheader();w.writerows(records)

def main():
    conditions,answers,pairs=read_archive()
    subgroup=[];leaveout=[];intervals=[]
    for condition,label in conditions.items():
        strata=defaultdict(list)
        for pair in pairs.values():
            a,b=[answers[condition,pair[g]] for g in ['established','recent']]
            assert a['ecosystem']==b['ecosystem']
            strata[a['ecosystem']].append((int(fully_correct(a)),int(fully_correct(b))))
        assert len(strata)==5 and all(len(v)==4 for v in strata.values())
        dist=Counter({0:1})
        for ecosystem,values in sorted(strata.items()):
            differences=[e-r for e,r in values]
            local=Counter({0:1})
            for _ in range(4):local=convolve(local,Counter(differences))
            dist=convolve(dist,local)
            subgroup.append(dict(condition=label,ecosystem=ecosystem,pairs=4,
                                 established_correct=sum(e for e,r in values),recent_correct=sum(r for e,r in values),
                                 gap_pp=f'{25*sum(differences):.1f}'))
            remaining=[v for k,vs in strata.items() if k!=ecosystem for v in vs]
            gap=100*sum(e-r for e,r in remaining)/len(remaining)
            leaveout.append(dict(condition=label,excluded_ecosystem=ecosystem,pairs=len(remaining),gap_pp=f'{gap:.2f}'))
        total=4**20
        assert sum(dist.values())==total
        endpoints=[]
        for q in [Fraction(1,40),Fraction(39,40)]:
            cumulative=0
            for difference,weight in sorted(dist.items()):
                cumulative+=weight
                if cumulative>=q*total:endpoints.append(5*difference);break
        gaps=[float(r['gap_pp']) for r in leaveout if r['condition']==label]
        intervals.append(dict(condition=label,stratified_ci_low_pp=endpoints[0],stratified_ci_high_pp=endpoints[1],
                              leave_one_out_min_pp=min(gaps),leave_one_out_max_pp=max(gaps)))
    write('ecosystem_results.csv',subgroup)
    write('leave_one_ecosystem_out.csv',leaveout)
    write('robustness_summary.csv',intervals)
    for r in intervals:print(r)
    print('Diagnostics are retrospective; preserve four pairs per ecosystem, not prompt-block dependence.')

if __name__=='__main__':main()
