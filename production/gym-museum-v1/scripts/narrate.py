"""Character-priced OpenAI speech, gated by this film's explicit budget authorization.
Use --plan for free planning. No retry, fallback model, telemetry or hidden paid calls.
"""
from pathlib import Path
import json,hashlib,os,sys,urllib.request,urllib.error,subprocess
P=Path(__file__).resolve().parents[1]
auth=json.loads((P/'authorization.json').read_text());scenes=json.loads((P/'performance.json').read_text())
requests=[]
for role,voice in auth['voices'].items():
 groups=[];group=''
 for scene in scenes:
  for row in scene['lines']:
   if row['speaker']!=role:continue
   candidate=(group+'\n\n'+row['text']).strip()
   if len(candidate)>3500:
    assert group;groups.append(group);group=row['text']
   else:group=candidate
 if group:groups.append(group)
 for i,text in enumerate(groups):
  assert len(text)<=3500
  requests.append({'id':role.lower()+f'-{i+1:02d}','role':role,'voice':voice,'text':text,'characters':len(text),'estimated_usd':len(text)*30/1e6,'text_sha256':hashlib.sha256(text.encode()).hexdigest()})
plan={'model':auth['model'],'price_usd_per_million_characters':30,'pricing_source':'https://developers.openai.com/api/docs/models/tts-1-hd','requests':requests,'estimated_usd':sum(r['estimated_usd'] for r in requests),'proposed_cap_usd':auth['maximum_usd_proposed'],'authorized':auth['paid_tts_authorized'],'no_automatic_retry':True}
(P/'audio/voice-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
print('Planned requests:',len(requests),'characters:',sum(r['characters'] for r in requests),'estimated USD:',round(plan['estimated_usd'],5),flush=True)
if '--plan' in sys.argv:sys.exit(0)
assert auth['paid_tts_authorized'] is True,'STOP: this film has no explicit paid TTS authorization'
assert plan['estimated_usd']<=auth['maximum_usd'],'Budget exceeded'
assert os.environ.get('OPENAI_API_KEY'),'No OpenAI key configured; no request made'
ledger=P/'audio/tts-ledger.json';rows=json.loads(ledger.read_text()) if ledger.exists() else []
for r in requests:
 out=P/'audio'/(r['id']+'-native.wav');old=next((x for x in rows if x['id']==r['id']),None)
 if old:
  assert old['state']=='saved' and out.exists() and old['text_sha256']==r['text_sha256'],'Prior attempt exists: stop, no automatic retry'
  continue
 row={k:v for k,v in r.items() if k!='text'};row.update(state='attempted',model=auth['model'],invoice_accessed=False);rows.append(row);ledger.write_text(json.dumps(rows,indent=2)+'\n')
 req=urllib.request.Request('https://api.openai.com/v1/audio/speech',data=json.dumps({'model':auth['model'],'voice':r['voice'],'input':r['text'],'speed':1,'response_format':'wav'}).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+os.environ['OPENAI_API_KEY']})
 try:
  with urllib.request.urlopen(req,timeout=240) as res:data=res.read()
 except urllib.error.HTTPError as e:raise SystemExit(f'TTS HTTP {e.code}; no retry; no secret or response body printed')
 assert data[:4]==b'RIFF','Non-WAV response; no retry'
 out.write_bytes(data);row.update(state='saved',sha256=hashlib.sha256(data).hexdigest());ledger.write_text(json.dumps(rows,indent=2)+'\n');print(r['id'],'saved',len(data),flush=True)
# Concatenate only the already purchased native chunks. No speech rate changes.
for role in auth['voices']:
 chunk=[P/'audio'/(r['id']+'-native.wav') for r in requests if r['role']==role]
 listing=P/'.cache'/(role.lower()+'-native-list.txt');listing.write_text(''.join("file '"+str(x)+"'\n" for x in chunk))
 subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(listing),'-c:a','pcm_s16le',str(P/'audio'/(role.lower()+'-native.wav'))],check=True)
print('All native voices saved. Rendering must reuse these files.',flush=True)
