import { actorAt, ease, clamp, mix, add, rotateY, localPoint } from '../../../src/motion.mjs';

const ROOMATE_ACTIONS = new Set(['roommate_arrive','almost_excuse','faucet_off','honest','roommate_question','snack_grab']);
export const move = (a,b,u) => mix(a,b,clamp(u));
function stand(x=0,z=.5,yaw=0){return {position:[x,1.18,z],yaw,lean:0,sitting:0,squat:0,left:{position:add([x,.12,z],rotateY([-.18,0,0],yaw)),moving:false},right:{position:add([x,.12,z],rotateY([.18,0,0],yaw)),moving:false},shoeYaw:yaw};}
function seated(x=0,z=-.25,height=.83){const a=stand(x,z);a.position[1]=height;a.sitting=1;a.left.position=[x-.20,.12,z+.70];a.right.position=[x+.20,.12,z+.70];return a;}
function walk(from,to,u){
  const raw=actorAt(.60+clamp(u)*3.25), dx=to[0]-from[0],dz=to[1]-from[1],distance=Math.hypot(dx,dz),yaw=Math.atan2(dx,dz);
  const along=[Math.sin(yaw),0,Math.cos(yaw)],side=[Math.cos(yaw),0,-Math.sin(yaw)];
  const foot=f=>{const q=(f.position[0]+2.7)/2.825;return {position:[from[0]+along[0]*q*distance+side[0]*(f.position[2]-.71),f.position[1],from[1]+along[2]*q*distance+side[2]*(f.position[2]-.71)],moving:f.moving,phase:f.phase};};
  const left=foot(raw.left),right=foot(raw.right);const span=Math.hypot(left.position[0]-right.position[0],left.position[2]-right.position[2]);
  return {position:[(left.position[0]+right.position[0])/2,1.18-.13*(span/1.15)**2,(left.position[2]+right.position[2])/2],yaw,lean:.065,sitting:0,squat:0,left,right,shoeYaw:yaw};
}
function sitMotion(u){const a=seated(2.3,-.05,.84);const q=ease(u,.08,.83);a.position=move([2.3,1.18,.45],[2.3,.84,-.05],q);a.sitting=q;a.lean=.28*Math.sin(Math.PI*q)-.07*q;return a;}
function pose(actor,t,smile=0){const swing=Math.sin(t*13);return {time:t,t,actor,ball:{position:localPoint(actor,[0,.65,3])},leftHand:localPoint(actor,[-.38,actor.sitting?.18:.04,.20-(actor.left.moving?.20*swing:0)]),rightHand:localPoint(actor,[.38,actor.sitting?.18:.04,.20+(actor.right.moving?.20*swing:0)]),blink:Math.max(0,1-Math.abs((t+1.1)%4.7-2.1)/.10),smile,shot:'wide'};}

export function frameState(shot,time){
  const local=time-shot.start,duration=shot.end-shot.start,u=clamp(local/duration),a=shot.action,p=shot.paragraph;
  const out={set:shot.set,action:a,camera:shot.camera,heroVisible:true,buddyVisible:false,role:'roommate',mood:'neutral',props:{},water:false,typing:0,progress:u,shotId:shot.id};
  let hero=pose(shot.set==='living'?seated(2.3,-.05,.84):shot.set==='work'?seated(0,-.25,.83):stand(-.2,.5),time);
  let buddy=pose(stand(1.9,.1),time,.45);
  const own=(name,who,hand,offset=[0,0,0],rotation=[0,0,0])=>{out.props[name]={position:add((who==='hero'?hero:buddy)[`${hand}Hand`],offset),rotation,owner:`${who}.${hand}`,offset};};
  const fixed=(name,position,rotation=[0,0,0])=>{out.props[name]={position,rotation,owner:null};};
  const gaze=(point,who=hero)=>{who.ball.position=point;};
  const kitchenBowl=[-1.35,1.20,1.12],tableBowl=[1.0,.90,.82],tableRemote=[1.62,.84,.70],rackPlate=[-.85,1.28,1.19],heldPlate=[-.12,1.22,1.12],restPlate=[-.40,1.06,1.12];
  if(shot.set==='living'){fixed('bowl',p>=11?tableBowl:[1.0,.90,.82]);fixed('remote',tableRemote);if(p<11&&a!=='uneasy_movie')out.props.bowl.visible=false;}
  if(shot.set==='kitchen'){fixed('bowl',kitchenBowl);out.props.bowl.visible=p>=2&&p<=11;fixed('plate',p>=13?restPlate:rackPlate,p>=13?[0,0,0]:[Math.PI/2,0,0]);}
  out.chairZ=-.25;out.lidAngle=p>=12?-Math.PI/2:.12;

  if(['couch_guilt','couch_movie','uneasy_movie','still_guilty','stay','watch','rest_end'].includes(a)){
    hero=pose(seated(2.3,-.05,.84),time,a==='rest_end'?.72:a==='watch'?.6:0.1);
    hero.leftHand=localPoint(hero.actor,[-.28,.20,.35]);own('remote','hero','left',[0,.01,.02]);
    if(a==='couch_guilt'||a==='still_guilty'||a==='uneasy_movie'){hero.actor.lean=.06+.08*Math.sin(Math.PI*u);hero.rightHand=localPoint(hero.actor,[.34,.25+.12*Math.sin(Math.PI*u),.31]);out.mood='guilty';gaze([-.6,2.0,1.2]);}
    else {hero.actor.lean=-.04*ease(u,.2,.8);hero.rightHand=localPoint(hero.actor,[.34,.16,.26]);gaze([1.6,1.7,3.5]);}
  }
  if(a==='keys'){
    out.heroVisible=false;fixed('key',[.50,1.20,-1.28],[0,0,.4*Math.sin(Math.PI*u)]);out.keyHand=true;
  }
  if(['dinner_done','prepare_snack','set_snack','pickup_snack'].includes(a)){
    hero=pose(stand(-1.2,.5),time,.15);hero.actor.lean=.23;
    const contact=[-1.35,1.04,1.12],carry=localPoint(hero.actor,[-.30,.25,.38]);
    if(a==='dinner_done'){hero.leftHand=move(localPoint(hero.actor,[-.35,.10,.3]),[-1.35,1.09,1.08],ease(u,.05,.55));hero.rightHand=localPoint(hero.actor,[.31,.12,.37]);fixed('plate',[-1.2,1.06,1.30]);}
    else if(a==='set_snack'){
      hero.leftHand=move(carry,contact,ease(u,.04,.70));if(u<.72)own('bowl','hero','left',[0,.16,0]);else fixed('bowl',kitchenBowl);
    }else{
      hero.leftHand=move(localPoint(hero.actor,[-.35,.1,.3]),contact,ease(u,.02,.35));
      if(u>.36){hero.leftHand=move(contact,carry,ease(u,.38,.95));own('bowl','hero','left',[0,.16,0]);}else fixed('bowl',kitchenBowl);
      hero.rightHand=localPoint(hero.actor,[.25,.17,.35]);
    }
    gaze(kitchenBowl);
  }
  if(a==='walk_pull'){
    if(u<.67)hero=pose(walk([1.65,-.3],[0,-.75],u/.67),time);
    else{hero=pose(stand(0,-.75),time);out.chairZ=.05-.30*ease(u,.67,.95);hero.leftHand=[-.27,1.37,out.chairZ-.33];}
    gaze([0,1.3,.8]);
  }
  if(['typing_reply','file_check','inbox_overflow','reach_work','alarm_off','missed_break','hesitate','realize','leave_desk','useful_pause','hover_couch','urgent_done','close_laptop','write_note','phone_reply'].includes(a)){
    hero=pose(seated(0,-.25,.83),time);hero.actor.lean=.24;gaze([0,1.35,.92]);
    hero.leftHand=[-.20,1.075,.71];hero.rightHand=[.22,1.075,.71];
    if(['typing_reply','inbox_overflow','file_check','reach_work'].includes(a)){
      hero.leftHand[1]+=.012*Math.sin(local*14+.5);hero.rightHand[1]+=.012*Math.sin(local*17);out.typing=u;
      if(a==='file_check')hero.rightHand=[.50,1.07,.63];
    }
    if(['missed_break','hesitate','realize','useful_pause','urgent_done'].includes(a)){
      hero.actor.lean=.08;hero.leftHand=localPoint(hero.actor,[-.34,.16,.30]);hero.rightHand=move([.20,1.04,.50],localPoint(hero.actor,[.25,.77,-.04]),ease(u,.15,.7));out.mood=a==='realize'?'recognition':'guilty';
      if(a==='realize')hero.rightHand=localPoint(hero.actor,[.30,.35,.40]);
    }
    if(a==='useful_pause'){
      hero.actor.lean=.24-.20*ease(u,.40,.90);hero.rightHand=move([.22,1.12,.58],[.20,1.12,.60],ease(u,.05,.32));
      if(u>.38)hero.rightHand=move([.20,1.12,.60],localPoint(hero.actor,[.34,.16,.30]),ease(u,.42,.88));
      gaze(move([0,1.35,.92],[2.3,1.6,1.2],ease(u,.50,.90)));
    }
    if(a==='leave_desk'){
      hero=pose(stand(.20,-.35),time);hero.actor.yaw=-.5*ease(u,.1,.8);hero.leftHand=[-.27,1.37,-.58];gaze([1.5,1.3,1.0]);
    }
    if(a==='hover_couch'){
      hero=pose(stand(.1,-.4),time);hero.actor.position[1]-=.16*Math.sin(Math.PI*u);hero.leftHand=[-.27,1.34,-.58];hero.rightHand=localPoint(hero.actor,[.38,.10,.25]);gaze([0,1.4,.8]);
    }
    if(a==='alarm_off'){
      hero.rightHand=move([.22,1.075,.71],[.70,1.025,.55],ease(u,.1,.5));fixed('phone',[.70,.99,.55],[-Math.PI/2,0,0]);out.phoneMode='timer';out.message='00:00';
    }
    if(a==='close_laptop'){
      hero=pose(stand(0,-.10),time);hero.actor.position[1]=1.10;hero.actor.lean=.64;gaze([0,1.3,.8]);
      const q=ease(u,.15,.80);out.lidAngle=.12+(-Math.PI/2-.12)*q;
      const angle=out.lidAngle;hero.leftHand=[-.20,.97+.64*Math.cos(angle),1.02+.64*Math.sin(angle)];hero.rightHand=localPoint(hero.actor,[.35,.12,.30]);
    }
    if(a==='write_note'){
      fixed('paper',[.92,.925,.57]);out.props.paper.scale=.75;const q=clamp((u-.06)/.58);hero.actor.position[0]=.25;hero.actor.lean=.34;
      hero.rightHand=[.72+.22*((q*3)%1),1.08,.46+Math.floor(Math.min(.999,q)*3)*.085];hero.leftHand=localPoint(hero.actor,[-.34,.14,.30]);if(u>.72)hero.rightHand=move(hero.rightHand,localPoint(hero.actor,[.34,.23,.30]),ease(u,.72,.92));own('pen','hero','right',[0,-.02,0]);out.noteProgress=q;
    }
    if(a==='phone_reply'||a==='realize'){
      hero.actor.lean=.10;hero.rightHand=localPoint(hero.actor,[.30,.35,.40]);hero.leftHand=localPoint(hero.actor,[-.03,.28,.46]);own('phone','hero','right',[0,.10,0],[0,Math.PI,0]);gaze(out.props.phone.position);
      out.message='I did nothing all afternoon. I feel awful.';out.draft='You were exhausted. You needed a break.';
    }
  }
  if(['phone_movie','phone_question','unsent_insert','thumb_stop','timer_insert','email_insert','document_insert','remote_insert','empty_movie'].includes(a)){
    out.heroVisible=false;
    if(['phone_movie','phone_question','unsent_insert','thumb_stop','timer_insert'].includes(a)){
      fixed('phone',[0,1.5,.5]);out.insertHands=true;out.message=a==='phone_movie'?'Finally, movie time.':a==='timer_insert'?'00:00':"How's the movie?";
      out.draft=['unsent_insert','thumb_stop'].includes(a)?"Haven't earned it yet.":'';out.phoneMode=a==='timer_insert'?'timer':out.draft?'unsent':'message';out.phoneProgress=a==='thumb_stop'?1:clamp(u*1.6);
    }
    if(a==='remote_insert'||a==='empty_movie'){fixed('remote',tableRemote);if(p<11)out.props.bowl={position:kitchenBowl,visible:false};}
    if(a==='timer_insert'){fixed('phone',[.70,.99,.55],[-Math.PI/2,0,0]);out.insertHands=false;}
  }
  if(a==='snack_cooling'){out.heroVisible=false;fixed('bowl',kitchenBowl);}
  if(['friend_rest','friend_kindness','leisure','boss'].includes(a)){
    out.heroVisible=false;out.buddyVisible=true;out.role='friend';
    buddy=pose(seated(0,-.05,.84),time,a==='friend_kindness'?.55:.08);buddy.actor.lean=a==='friend_rest'?-.11:.1;
    if(a==='boss')buddy=pose(seated(0,-.25,.83),time,.02);
    buddy.rightHand=localPoint(buddy.actor,[.30,.36,.42]);buddy.leftHand=localPoint(buddy.actor,[-.10,.28,.42]);own('phone','buddy','right',[0,.10,0],[0,Math.PI,0]);gaze(out.props.phone.position,buddy);
    out.message=a==='boss'?'Please reply tonight.':a==='friend_kindness'?'You needed a break.':'I feel bad about doing nothing.';
  }
  if(['inspection','receipt'].includes(a)){
    hero=pose(stand(-1.05,.65),time,.05);buddy=pose(seated(.95,0,.84),time,.1);out.buddyVisible=true;out.role='clerk';
    hero.rightHand=[-.26,1.32,.85];buddy.leftHand=[.36,1.32,.85];buddy.rightHand=localPoint(buddy.actor,[.40,.2,.4]);
    fixed('receipt',[.05,1.32,.87],[0,-.06,0]);hero.leftHand=localPoint(hero.actor,[-.32,.25,.30]);own('remote','hero','left');gaze([.95,1.8,.4]);gaze([-1,2,.65],buddy);
  }
  if(a==='laundry'){
    out.heroVisible=false;out.buddyVisible=true;out.role='friend';buddy=pose(walk([-.9,.5],[.5,.5],clamp(u*1.25)),time,.05);buddy.leftHand=localPoint(buddy.actor,[-.29,.23,.43]);buddy.rightHand=localPoint(buddy.actor,[.29,.23,.43]);fixed('basket',localPoint(buddy.actor,[0,.24,.46]));
  }
  if(a==='care'){
    out.buddyVisible=true;out.role='friend';hero=pose(seated(.65,-.05,.84),time,.25);buddy=pose(stand(-.65,.5),time,.3);
    hero.leftHand=[.18,1.20,.75];buddy.rightHand=move(localPoint(buddy.actor,[.3,.08,.3]),[-.02,1.15,.75],ease(u,.1,.65));own('cup','buddy','right',[0,.10,0]);gaze(out.props.cup.position);gaze([.65,1.8,.3],buddy);
  }
  if(a==='walk_snack'){
    hero=pose(walk([-.10,.50],[1.25,.35],clamp(u*1.08)),time,.12);hero.leftHand=localPoint(hero.actor,[-.30,.22,.36]);own('bowl','hero','left',[0,.16,0]);gaze([2.3,1.2,.0]);
  }
  if(a==='sit_play'){
    if(u<.25){hero=pose(stand(1.25,.35),time,.1);hero.actor.position[1]=.98;hero.actor.lean=.3;hero.leftHand=move(localPoint(hero.actor,[-.30,.22,.36]),[1,.74,.82],ease(u,0,.22));if(u<.22)own('bowl','hero','left',[0,.16,0]);else fixed('bowl',tableBowl);}
    else if(u<.50){hero=pose(walk([1.25,.35],[2.3,.45],(u-.25)/.25),time,.1);fixed('bowl',tableBowl);}
    else{hero=pose(sitMotion((u-.50)/.50),time,.2);fixed('bowl',tableBowl);hero.actor.lean+=.43*ease(u,.76,.90);hero.leftHand=move(localPoint(hero.actor,[-.28,.2,.35]),[1.62,.82,.70],ease(u,.76,.91));if(u>.91){hero.leftHand=move([1.62,.82,.70],localPoint(hero.actor,[-.28,.20,.35]),ease(u,.91,1));own('remote','hero','left',[0,.01,.02]);}}
  }
  if(a==='startle'){
    const q=ease(u,.26,.90);hero=pose(sitMotion(1-q),time,0);hero.actor.lean+=.40*(1-q);out.mood='guilty';
    hero.leftHand=move(localPoint(hero.actor,[-.28,.2,.35]),[1.62,.82,.70],ease(u,0,.22));if(u<.22)own('remote','hero','left',[0,.01,.02]);
    if(u>.25)hero.leftHand=localPoint(hero.actor,[-.39,.06,.16]);gaze([-.3,2,1.5]);
  }
  if(a==='hurry'){
    if(u<.40)hero=pose(walk([1.85,.5],[-.2,.5],u/.40),time,0);
    else{
      hero=pose(stand(-.2,.5),time,0);const end=walk([1.85,.5],[-.2,.5],1);hero.actor.left=end.left;hero.actor.right=end.right;hero.actor.lean=.20;
      const handAtRack=[-1.0,1.28,1.19],holding=[-.28,1.20,1.12];hero.leftHand=move(localPoint(hero.actor,[-.35,.12,.35]),handAtRack,ease(u,.40,.62));
      if(u>.64){hero.leftHand=move(handAtRack,holding,ease(u,.64,.96));own('plate','hero','left',[.16,.02,0],[Math.PI/3,0,.10]);}else fixed('plate',rackPlate,[Math.PI/2,0,0]);
    }
    gaze([-.6,1.2,1.16]);
  }
  if(['wash','roommate_arrive','almost_excuse','faucet_off','honest','roommate_question'].includes(a)){
    hero=pose(stand(-.2,.5),time,a==='honest'?.35:0);hero.actor.lean=.20;out.water=true;
    hero.leftHand=[-.28,1.20,1.12];hero.rightHand=[-.03+.045*Math.sin(local*7),1.245,1.205];own('plate','hero','left',[.16,.02,0],[Math.PI/3,0,.10]);gaze(heldPlate);out.mood=a==='almost_excuse'?'guilty':'neutral';
    if(ROOMATE_ACTIONS.has(a)){out.buddyVisible=true;buddy=pose(a==='roommate_arrive'?walk([2.8,.30],[1.75,.35],clamp(u*1.3)):stand(1.75,.35),time,.3);gaze([-.2,2.0,.5],buddy);}
    if(a==='faucet_off'){
      hero.rightHand=move([-.02,1.245,1.205],[.55,1.13,1.05],ease(u,.02,.28));out.water=u<.36;
      if(u>.40){hero.leftHand=move([-.28,1.20,1.12],[-.56,1.07,1.12],ease(u,.40,.72));if(u<.74)own('plate','hero','left',[.16,.02,0],[Math.PI/3*(1-ease(u,.4,.72)),0,0]);else fixed('plate',restPlate);}
    }
    if(a==='honest'||a==='roommate_question'){
      out.water=false;fixed('plate',restPlate);hero.actor.lean=.02;hero.leftHand=localPoint(hero.actor,[-.38,.05,.18]);hero.rightHand=localPoint(hero.actor,[.38,.05,.18]);gaze([1.75,2.0,.35]);out.mood='relief';
    }
    if(a==='roommate_question')buddy.rightHand=localPoint(buddy.actor,[.45,.28,.38]);
  }
  if(a==='sit_back')hero=pose(sitMotion(u),time,.4);
  if(a==='snack_grab'){
    hero=pose(seated(2.3,-.05,.84),time,.45);out.buddyVisible=true;buddy=pose(stand(.55,.55),time,.5);buddy.actor.position[1]-=.13*Math.sin(Math.PI*clamp(u*1.6));buddy.actor.lean=.17;
    const table=[1.05,.98,.82],mouth=localPoint(buddy.actor,[.17,.79,.27]);buddy.rightHand=move(localPoint(buddy.actor,[.38,.1,.2]),table,ease(u,.02,.30));
    if(u>.34){buddy.rightHand=move(table,mouth,ease(u,.35,.78));own('snack','buddy','right',[0,.02,.02]);if(u>.85)out.props.snack.scale=1-ease(u,.85,1);}
    if(u>.62){buddy=pose(walk([.55,.55],[-1.65,-.5],(u-.62)/.38),time,.4);out.props.snack.visible=false;}
    fixed('bowl',tableBowl);gaze([2.3,1.8,.4],buddy);
  }
  if(a==='find_place'){
    hero=pose(seated(2.3,-.05,.84),time,.5);hero.actor.lean=.43;
    hero.leftHand=move([1.62,.82,.70],localPoint(hero.actor,[-.28,.2,.35]),ease(u,.1,.7));own('remote','hero','left',[0,.01,.02]);gaze([1.6,1.7,3.5]);
  }
  out.hero=hero;out.buddy=buddy;
  if(a==='inbox_overflow')out.laptopMode='overflow';else if(['file_check','document_insert','write_note','close_laptop','urgent_done'].includes(a))out.laptopMode='document';else out.laptopMode=a==='typing_reply'?'reply':'email';
  return out;
}
