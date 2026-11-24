"""Build the shot ledger from the recorded narration's actual aligned anchor words."""
from pathlib import Path
import json,re,math
ROOT=Path(__file__).resolve().parents[1]
speech=json.loads((ROOT/'assets/speech.json').read_text()); words=json.loads((ROOT/'assets/words.json').read_text())
# Each row: exact narration anchor, action, set, camera. No reused trial footage.
plan=[
 [('Why does','couch_guilt','living','face'),('Picture this.','keys','entry','key'),('A second ago,','couch_movie','living','living'),("Now you're washing",'wash','kitchen','sink')],
 [('An hour earlier,','dinner_done','kitchen','kitchen'),('You texted','phone_movie','living','phone'),('You made a snack,','prepare_snack','kitchen','kitchen'),('Then you noticed','email_insert','work','laptop')],
 [('One unanswered email.','email_insert','work','laptop'),('But answering','hesitate','work','face'),('You put the snack down,','set_snack','kitchen','kitchen'),('crossed the room,','walk_pull','work','work')],
 [('You sent the reply.','typing_reply','work','work'),('Apparently','inbox_overflow','work','laptop'),('Now you needed','file_check','work','work_ots'),('Your movie','empty_movie','living','empty'),('The snack','snack_cooling','kitchen','snack')],
 [('Your phone rang.','timer_insert','work','timer'),('You had successfully','missed_break','work','face'),('You silenced','alarm_off','work','work_ots'),('Just finish this.','reach_work','work','work')],
 [('Then your friend','friend_rest','friend','friend'),('Your reply','phone_reply','work','face'),('A moment later,','phone_question','work','phone'),('You looked','remote_insert','living','remote')],
 [('You started typing:','unsent_insert','work','phone'),('Then stopped.','thumb_stop','work','phone'),('But looking','realize','work','face'),('Your friend could rest','friend_kindness','friend','friend')],
 [("Maybe that's",'leave_desk','work','work'),('If being useful','useful_pause','work','face'),('The document','document_insert','work','laptop'),('But can you','hover_couch','work','work')],
 [('Research has linked','leisure','friend','friend'),("That doesn't explain",'uneasy_movie','living','face'),('In this story,','inspection','inspection','inspection'),('Imagine watching','receipt','inspection','receipt')],
 [('Sometimes the pressure','boss','work','work_ots'),("Housework isn't",'laundry','living','living'),('Someone depends','care','friend','friend'),('But tonight,','urgent_done','work','work')],
 [('You look','document_insert','work','laptop'),('You write yourself','write_note','work','note'),('Then you close','close_laptop','work','work_ots'),('You take the snack','pickup_snack','kitchen','kitchen'),('back to the couch.','walk_snack','living','living'),('This time,','sit_play','living','living')],
 [('And right then,','keys','entry','key'),('The familiar thought','startle','living','living'),('You hurry','hurry','kitchen','kitchen'),('Under the running water,','wash','kitchen','plate')],
 [('Your roommate walks in.','roommate_arrive','kitchen','kitchen'),('You almost say','almost_excuse','kitchen','face'),('Instead,','faucet_off','kitchen','sink'),('Your mouth','honest','kitchen','face')],
 [('Any good?','roommate_question','kitchen','buddy_face'),('You sit back down.','sit_back','living','living'),('Your roommate takes','snack_grab','living','living'),("That's it.",'find_place','living','remote')],
 [("The guilt hasn't",'still_guilty','living','face'),('But this time,','stay','living','living'),('You let the movie','watch','living','face'),('And you let someone','rest_end','living','living')]
]
norm=lambda s:re.sub(r'[^a-z0-9]','',s.lower())
shots=[]
for p,rows in zip(speech['paragraphs'],plan):
    pw=[w for w in words if w['paragraph']==p['id']]; normalized=[norm(w['text']) for w in pw]
    for j,(anchor,action,set_name,camera) in enumerate(rows):
        needle=[norm(w) for w in anchor.split()]
        candidates=[i for i in range(len(pw)-len(needle)+1) if normalized[i:i+len(needle)]==needle]
        if not candidates: raise ValueError(f'Missing P{p["id"]} anchor: {anchor}')
        at=candidates[0];start=max(0,pw[at]['start']-0.04)
        if p['id']==1 and j==0:start=0
        shots.append({'id':f'p{p["id"]:02d}-s{j+1:02d}','paragraph':p['id'],'anchor':anchor,'action':action,'set':set_name,'camera':camera,'start':round(start,6),'source_word':pw[at]['index']})
duration=math.ceil(speech['duration']*6)/6
for i,s in enumerate(shots): s['end']=shots[i+1]['start'] if i+1<len(shots) else duration; s['duration']=round(s['end']-s['start'],6);assert s['duration']>0
timeline={'title':'Why You Feel Guilty When You Rest','duration':duration,'pose_hz':12,'capture_fps':12,'delivery_fps':30,'script_sha256':speech['script_sha256'],'shots':shots}
(ROOT/'assets/timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2)+'\n')
lines=['# Recorded-narration storyboard','','Every shot is anchored to the actual local recording. Times are measured, not a proposed SRT.','', '| Start | End | Narration anchor | Set | Action | Camera |','| --- | --- | --- | --- | --- | --- |']
for s in shots:lines.append(f'| {s["start"]:.2f}s | {s["end"]:.2f}s | {s["anchor"]} | {s["set"]} | {s["action"]} | {s["camera"]} |')
lines+=['','The plate is a clean dish from the drying rack, not the snack bowl. The bowl stays on the kitchen counter until it is carried to the living-room side table. The remote is placed before the startled rise and recovered at the ending. All messages and screen designs are fictional illustrations of the approved narration.','', 'The inspection desk is an imagined metaphor, not an observed experiment. The external-pressure montage is contextual illustration; it is not presented as this protagonist’s actual roommate judging them.']
(ROOT/'STORYBOARD.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'shots':len(shots),'duration':duration,'shortest':min(s['duration'] for s in shots),'longest':max(s['duration'] for s in shots)}))
