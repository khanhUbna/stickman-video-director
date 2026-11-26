"""Two new approved-script lines for the 20s sample's payoff, not retries/revoices."""
from pathlib import Path
import json,os,hashlib,urllib.request,urllib.error,subprocess
P=Path(__file__).resolve().parents[1];a=json.loads((P/'authorization.json').read_text());assert a['paid_tts_authorized'];
if a.get('generation_complete'):
 print('Payoff voices already saved; no requests made.');raise SystemExit(0)
ledger=P/'audio/tts-ledger.json';rows=json.loads(ledger.read_text());new=[('VALE','When does the torture begin?'),('MINA',"It doesn't have to.")]
assert sum(x['estimated_usd'] for x in rows)+sum(len(t)*30/1e6 for r,t in new)<=a['maximum_usd']
for role,text in new:
 ident=role.lower()+'-payoff-01';f=P/'audio'/(ident+'-native.wav');old=next((x for x in rows if x['id']==ident),None)
 if old:
  assert old['state']=='saved' and f.exists(),'Prior attempt exists; no retry';continue
 row={'id':ident,'role':role,'voice':a['voices'][role],'characters':len(text),'estimated_usd':len(text)*30/1e6,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'model':a['model'],'state':'attempted','purpose':'Additional original-script payoff line for 20s preview only, not a retry','invoice_accessed':False};rows.append(row);ledger.write_text(json.dumps(rows,indent=2)+'\n')
 req=urllib.request.Request('https://api.openai.com/v1/audio/speech',data=json.dumps({'model':a['model'],'voice':row['voice'],'input':text,'response_format':'wav','speed':1}).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+os.environ['OPENAI_API_KEY']})
 try:
  with urllib.request.urlopen(req,timeout=240) as r:data=r.read()
 except urllib.error.HTTPError as e:raise SystemExit(f'HTTP {e.code}; no automatic retry; no key logged')
 assert data[:4]==b'RIFF';f.write_bytes(data);row.update(state='saved',sha256=hashlib.sha256(data).hexdigest());ledger.write_text(json.dumps(rows,indent=2)+'\n');print(ident,'saved',flush=True)
for role,_ in new:
 sources=[P/'audio'/(role.lower()+'-01-native.wav'),P/'audio'/(role.lower()+'-payoff-01-native.wav')];ls=P/'.cache'/(role.lower()+'-complete-list.txt');ls.write_text(''.join("file '"+str(f.resolve())+"'\n" for f in sources));subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(ls),'-c:a','pcm_s16le',str(P/'audio'/(role.lower()+'-native.wav'))],check=True)
base=json.loads((P.parent/'gym-museum-v1/performance.json').read_text())[6]['lines'];vi=json.loads((P.parent/'gym-museum-v1/performance-vi.json').read_text())[6]['lines'];selected=[0,1,2,3,5,6]
for filename,source in [('performance.json',base),('performance-vi.json',vi)]:
 (P/filename).write_text(json.dumps([{'scene':'Live demonstration excerpt with payoff','lines':[source[i] for i in selected]}],ensure_ascii=False,indent=2)+'\n')
for filename,source in [('script-en.txt',base),('script-vi.txt',vi)]: (P/filename).write_text('\n\n'.join(source[i]['text'] for i in selected)+'\n')
print('Total estimated USD',sum(r['estimated_usd'] for r in rows),flush=True)
