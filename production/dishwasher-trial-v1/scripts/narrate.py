from pathlib import Path
import json,os,urllib.request,urllib.error,hashlib
P=Path(__file__).resolve().parents[1];auth=json.loads((P/'authorization.json').read_text());scenes=json.loads((P/'performance.json').read_text())
roles={r:'\n\n'.join(x['text'] for s in scenes for x in s['lines'] if x['speaker']==r) for r in auth['voices']}
planned=sum(len(t) for t in roles.values())*30/1e6;assert auth['authorized'] and planned<=auth['maximum_usd'];print('Estimated total USD',planned,flush=True)
ledger=P/'audio/tts-ledger.json';rows=json.loads(ledger.read_text()) if ledger.exists() else []
for role,txt in roles.items():
 path=P/'audio'/f'{role.lower()}-native.wav';record=next((x for x in rows if x['role']==role),None)
 if record:
  assert record['state']=='saved' and path.exists(),'Previous attempt exists: no automatic retry';continue
 row={'role':role,'voice':auth['voices'][role],'model':auth['model'],'characters':len(txt),'estimated_usd':len(txt)*30/1e6,'state':'attempted','invoice_accessed':False};rows.append(row);ledger.write_text(json.dumps(rows,indent=2)+'\n')
 req=urllib.request.Request('https://api.openai.com/v1/audio/speech',data=json.dumps({'model':auth['model'],'voice':row['voice'],'input':txt,'speed':1,'response_format':'wav'}).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+os.environ['OPENAI_API_KEY']})
 try:
  with urllib.request.urlopen(req,timeout=240) as response:data=response.read()
 except urllib.error.HTTPError as e:raise SystemExit(f'TTS HTTP{e.code}; no retry; no key logged')
 path.write_bytes(data);row.update(state='saved',sha256=hashlib.sha256(data).hexdigest());ledger.write_text(json.dumps(rows,indent=2)+'\n');print(role,'saved',len(data),flush=True)
print('All roles saved. No additional paid requests needed.',flush=True)
