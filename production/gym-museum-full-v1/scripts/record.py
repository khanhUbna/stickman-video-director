"""Record only missing speech. Approved49-word sample is reused, never revoiced."""
from pathlib import Path
import json,hashlib,os,sys,urllib.request,urllib.error
P=Path(__file__).resolve().parents[1];V=P.parent/'gym-museum-preview-v2';auth=json.loads((P/'authorization.json').read_text());scenes=json.loads((P/'performance.json').read_text());old=json.loads((V/'turns20.json').read_text())
if auth.get('generation_complete') and '--plan' not in sys.argv:
 print('Speech is complete. Reuse saved audio; no paid requests made.');raise SystemExit(0)
reuse={};missing=[]
for si,s in enumerate(scenes):
 for li,r in enumerate(s['lines']):
  x=dict(r,scene=si,line=li,id=f's{si+1:02d}-l{li+1:02d}');match=next((o for o in old if o['speaker']==x['speaker'] and o['text']==x['text']),None)
  if match:reuse[x['id']]=dict(source_project=str(V),source_turn=match)
  else:missing.append(x)
assert len(reuse)==6,'All six approved utterances must be reused'
(P/'audio/reuse-map.json').write_text(json.dumps(reuse,indent=2)+'\n')
requests=[]
for role,voice in auth['voices'].items():
 group=[]
 def finish(group):
  if not group:return
  text='\n\n'.join(x['text'] for x in group);idx=sum(r['role']==role for r in requests)+1;requests.append({'id':f'{role.lower()}-missing-{idx:02d}','role':role,'voice':voice,'turn_ids':[x['id'] for x in group],'input':text,'characters':len(text),'estimated_usd':len(text)*30/1e6,'input_sha256':hashlib.sha256(text.encode()).hexdigest()})
 for r in [x for x in missing if x['speaker']==role]:
  if group and len('\n\n'.join(x['text'] for x in group+[r]))>3500:finish(group);group=[]
  group.append(r)
 finish(group)
plan={'model':auth['model'],'reuse_turns':list(reuse),'missing_requests':requests,'new_estimated_usd':sum(x['estimated_usd'] for x in requests),'previous_sample_estimated_usd':auth['previous_sample_estimated_usd']};plan['estimated_project_total_usd']=plan['new_estimated_usd']+plan['previous_sample_estimated_usd'];assert plan['estimated_project_total_usd']<=auth['maximum_usd']
(P/'audio/record-plan.json').write_text(json.dumps(plan,indent=2)+'\n');print('New requests:',len(requests),'reuse turns:',len(reuse),'new USD:',round(plan['new_estimated_usd'],5),'total with sample:',round(plan['estimated_project_total_usd'],5),flush=True)
if '--plan' in sys.argv:sys.exit(0)
assert auth['paid_tts_authorized'] and auth['full_film_authorized'];assert os.environ.get('OPENAI_API_KEY'),'No key; no request made'
ledger=P/'audio/tts-ledger.json';rows=json.loads(ledger.read_text()) if ledger.exists() else []
for r in requests:
 out=P/'audio'/(r['id']+'.wav');old=next((x for x in rows if x['id']==r['id']),None)
 if old:
  assert old['state']=='saved' and out.exists() and old['input_sha256']==r['input_sha256'],'Prior attempt exists; no automatic retry'
  continue
 row={k:v for k,v in r.items() if k!='input'};row.update(state='attempted',model=auth['model'],invoice_accessed=False);rows.append(row);ledger.write_text(json.dumps(rows,indent=2)+'\n')
 req=urllib.request.Request('https://api.openai.com/v1/audio/speech',data=json.dumps({'model':auth['model'],'voice':r['voice'],'input':r['input'],'response_format':'wav','speed':1}).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+os.environ['OPENAI_API_KEY']})
 try:
  with urllib.request.urlopen(req,timeout=240) as response:data=response.read()
 except urllib.error.HTTPError as e:raise SystemExit(f'HTTP {e.code}; no automatic retry, no secret or response body logged')
 assert data[:4]==b'RIFF','Unexpected non-WAV response; no retry'
 out.write_bytes(data);row.update(state='saved',sha256=hashlib.sha256(data).hexdigest());ledger.write_text(json.dumps(rows,indent=2)+'\n');print(r['id'],'saved',len(data),flush=True)
print('All missing speech saved. Reuse on every render.',flush=True)
