"""Recompute the original and supplementary evidence without loading any model."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def run(*args):
    subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,check=True)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');a=p.parse_args()
    manifest_path=ROOT/'reference_outputs.json'
    before=json.loads(manifest_path.read_text()) if manifest_path.exists() else None
    inputs=ROOT/'input_manifest.json'
    if inputs.exists():
        for path,digest in json.loads(inputs.read_text()).items():
            if sha(ROOT/path)!=digest:raise RuntimeError('Saved input differs: '+path)
    if a.verify and before is None:raise RuntimeError('Missing reference_outputs.json')
    run('reproduce.py','--verify')
    run('audit_bekasyl.py')
    run('robustness.py')
    run('figures.py','--results','reproduced','--out','reproduced/figures')
    run('figures_bekasyl.py','--results','reproduced','--out','reproduced/report_figures')
    run('supplement/scripts/analyze_supplement.py','--out','reproduced/supplement_results')
    run('supplement/scripts/figures_supplement.py','--results','reproduced/supplement_results','--out','reproduced/supplement_figures')
    mapping={}
    for folder in ['results','diagnostics','figures','report_figures','supplement/results','supplement/figures']:
        for f in sorted((ROOT/folder).glob('*')):
            if f.suffix not in ['.csv','.svg']:continue
            ref=str(f.relative_to(ROOT));mapping[ref]=sha(f)
            if folder=='results':generated=ROOT/'reproduced'/f.name
            elif folder=='diagnostics':generated=f
            elif folder=='supplement/results':generated=ROOT/'reproduced/supplement_results'/f.name
            elif folder=='supplement/figures':generated=ROOT/'reproduced/supplement_figures'/f.name
            else:generated=ROOT/'reproduced'/folder/f.name
            if sha(generated)!=mapping[ref]:raise RuntimeError('Regeneration differs: '+ref)
    if a.verify:
        if mapping!=before:raise RuntimeError('Reference output manifest differs')
    else:manifest_path.write_text(json.dumps(mapping,indent=2)+'\n')
    print(f'PASS: {len(mapping)} CSV/SVG files match saved evidence. No model or network needed.')
    print('Original: 120 answers; supplement: 120 outputs and 120 explicit ratings.')
    print('This is an automated software check, not a human teammate attestation.')

if __name__=='__main__':main()
