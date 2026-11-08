"""Snapshot the pre-existing official-source list, without reading reference answers."""
import hashlib,json,re,time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
from pathlib import Path
from urllib.request import Request,urlopen
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'supplement/corpus'

def sha(data):return hashlib.sha256(data).hexdigest()
class PageText(HTMLParser):
    def __init__(self):super().__init__();self.skip=0;self.inmain=0;self.body=[];self.main=[]
    def handle_starttag(self,tag,attrs):
        if tag in ['script','style','nav','header','footer','head']:self.skip+=1
        if tag=='main':self.inmain+=1
    def handle_endtag(self,tag):
        if tag in ['script','style','nav','header','footer','head']:self.skip=max(0,self.skip-1)
        if tag=='main':self.inmain=max(0,self.inmain-1)
    def handle_data(self,data):
        if not self.skip:
            self.body.append(data)
            if self.inmain:self.main.append(data)
def fetch(source):
    url=source['url']
    # Fixed transport transformation: raw Git content instead of GitHub UI.
    url=url.replace('https://github.com/git/git/blob/','https://raw.githubusercontent.com/git/git/')
    result=dict(source)
    for attempt in range(2):
        try:
            r=urlopen(Request(url,headers={'User-Agent':'RMT-course-reproducibility/1.0'}),timeout=45);raw=r.read()
            (OUT/'snapshots'/f"{source['source_id']}.bin").write_bytes(raw)
            if 'html' in r.headers.get('content-type',''):
                parser=PageText();parser.feed(raw.decode('utf-8',errors='replace'));txt=' '.join(parser.main or parser.body)
            else:txt=raw.decode('utf-8',errors='replace')
            txt=re.sub(r'\s+',' ',txt).strip()
            assert len(txt)>100,'Insufficient source text'
            result.update(status='ok',final_url=r.url,http_status=r.status,raw_sha256=sha(raw),text_sha256=sha(txt.encode()),text=txt)
            return result
        except Exception as e:result.update(status='failed',error=str(e),attempts=attempt+1)
    return result

def main():
    OUT.mkdir(exist_ok=True);(OUT/'snapshots').mkdir(exist_ok=True)
    archive=json.loads((ROOT/'data/Assignment3_Main_Experiment_Data.json').read_text())
    sources=archive['sources']
    results=list(ThreadPoolExecutor(max_workers=6).map(fetch,sources))
    chunks=[]
    for source in results:
        if source['status']!='ok':continue
        words=source['text'].split()
        for start in range(0,len(words),140):
            text=' '.join(words[start:start+180])
            if len(text)<50:continue
            chunks.append(dict(chunk_id=f"{source['source_id']}:{start:06d}",source_id=source['source_id'],
                               url=source['url'],title=source['title'],version=source.get('version',''),text=text))
    (OUT/'chunks.json').write_text(json.dumps(chunks,ensure_ascii=False,indent=2)+'\n')
    manifest={'snapshot_utc':datetime.now(timezone.utc).isoformat(),'chunk_words':180,'stride_words':140,
              'sources':[{k:v for k,v in s.items() if k!='text'} for s in results],
              'chunks_sha256':sha((OUT/'chunks.json').read_bytes()),'chunk_count':len(chunks)}
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print('Sources',len(sources),'available',sum(s['status']=='ok' for s in results),'chunks',len(chunks))
    for s in results:
        if s['status']!='ok':print('FAILED',s['source_id'],s['url'],s['error'])

if __name__=='__main__':main()
