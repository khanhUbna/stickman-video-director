import * as THREE from 'three';
import { makeScene } from '../../../src/scene.mjs';
import { createWorld } from './sets.mjs';
import { frameState } from './acting.mjs';
import timeline from '../assets/timeline.json';
import captions from '../assets/captions.json';

const canvas=document.getElementById('film-canvas');
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,preserveDrawingBuffer:true,powerPreference:'low-power'});
renderer.setPixelRatio(1);renderer.setSize(1920,1080,false);renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.02;
renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFShadowMap;
let stage,buddy,world,lastTime=-1,debug={};
const gl=renderer.getContext(),pixel=new Uint8Array(4);
const captionElements=[...document.querySelectorAll('.caption-body')];
const V=p=>new THREE.Vector3(...p);
function chooseShot(t){return timeline.shots.find(s=>t>=s.start&&t<s.end)||timeline.shots.at(-1);}
function cameraFor(state,shot){
  const camera=stage.camera;let position,target,width;
  const root=state.hero.actor.position;
  const settings={
    living:[[6.3,4.4,9.4],[0,1.10,0],9.6],
    work:[[4.6,3.5,5.5],[0,1.05,.4],6.5],
    work_ots:[[2.6,3.1,-3.6],[0,1.18,.55],4.4],
    kitchen:[[5.4,3.8,7.2],[.10,1.12,.8],7.4],
    sink:[[-3.0,3.1,4.8],[-.15,1.30,1.02],4.9],
    plate:[[.9,2.4,3.7],[-.12,1.22,1.12],2.0],
    friend:[[4.0,3.2,5.8],[0,1.08,.1],6.1],
    inspection:[[4.5,3.1,6.4],[0,1.16,.70],6.7],
    receipt:[[1.0,2.1,4.0],[.05,1.32,.87],2.25],
    key:[[1.4,1.7,1.3],[.50,1.2,-1.3],1.5],
    phone:[[0,1.5,5.1],[0,1.50,2.5],1.10],
    timer:[[1.6,2.7,1.3],[.70,1.0,.55],1.10],
    snack:[[-.2,2.1,3.2],[-1.35,1.20,1.12],1.70],
    laptop:[[1.0,2.05,-2.8],[0,1.27,.95],2.30],
    note:[[.92,3.0,.90],[.92,.93,.57],1.30],
    empty:[[5.0,3.5,6.6],[2.1,1.05,.2],6.0],
    remote:[[2.2,1.8,2.8],[1.62,.84,.70],1.20],
  };
  if(shot.camera==='face'){
    const y=state.set==='living'?.84:state.set==='work'&&['leave_desk','hover_couch'].includes(state.action)?1.18:state.set==='work'?.83:1.18;
    target=[root[0],y+.72,root[2]+.08];position=[root[0]+2.6,y+1.75,root[2]+4.7];width=3.35;
  }else if(shot.camera==='buddy_face'){
    const b=state.buddy.actor.position;target=[b[0],b[1]+.76,b[2]];position=[b[0]-2.1,b[1]+1.6,b[2]+4.7];width=3.35;
  }else [position,target,width]=settings[shot.camera]||settings[state.set]||settings.living;
  camera.left=-width/2;camera.right=width/2;camera.top=width*9/32;camera.bottom=-width*9/32;camera.position.set(...position);camera.lookAt(...target);camera.updateProjectionMatrix();camera.updateMatrixWorld(true);
  // These are open diorama sets: remove the wall on the camera side, keep the opposite backdrop.
  world.prop.workFrontWall.visible=position[2]<1.85;
  world.prop.workBackWall.visible=position[2]>-1.85;
}
function applyProps(state){
  world.prop.chair.position.z=state.chairZ;world.prop.lid.rotation.x=state.lidAngle;
  for(const [name,config]of Object.entries(state.props)){
    const object=world.prop[name];if(!object)continue;
    object.visible=config.visible!==false;object.position.set(...config.position);object.rotation.set(...(config.rotation||[0,0,0]));object.scale.setScalar(config.scale??1);
  }
  world.prop.water.visible=state.water;world.prop.valve.rotation.y=state.water?0:-.8;
  world.prop.insertHands.visible=!!state.insertHands;
  if(state.insertHands){world.prop.phone.position.set(0,1.54,2.5);state.props.phone.position=[0,1.54,2.5];world.prop.insertHands.position.copy(world.prop.phone.position);world.prop.insertFinger.position.x=.105+.009*Math.sin(state.progress*12);}
  world.prop.keyHand.visible=!!state.keyHand;
  if(state.keyHand){world.prop.keyHand.rotation.z=.4*Math.sin(Math.PI*state.progress);}
  const a=state.action;
  if(state.props.phone)world.phoneText(state.message||"How's the movie?",state.draft||'',state.phoneMode||'message',state.phoneProgress??state.progress);
  world.laptopText(state.laptopMode||(['document_insert','write_note','close_laptop'].includes(a)?'document':'email'),state.progress);
  if(a==='write_note')world.noteText(state.noteProgress);else world.noteText(1);
  const mood=state.mood;
  stage.objects.mouth.scale.y=1;stage.objects.mouth.position.y=0;
  if(mood==='guilty'){stage.objects.brows[0].rotation.z=.22;stage.objects.brows[1].rotation.z=-.22;stage.objects.head.rotation.z=.04;stage.objects.mouth.scale.y=-1;stage.objects.mouth.position.y=-.26;stage.objects.mouth.material.opacity=1;stage.objects.smile.material.opacity=0;}
  if(mood==='recognition'){stage.objects.brows[0].rotation.z=-.12;stage.objects.brows[1].rotation.z=.08;}
  for(const [rig,pose]of [[stage,state.hero],[buddy,state.buddy]]){
    const [x,,z]=pose.actor.position,focus=pose.ball.position;
    let angle=Math.atan2(focus[0]-x,focus[2]-z)-pose.actor.yaw;
    while(angle>Math.PI)angle-=Math.PI*2;while(angle< -Math.PI)angle+=Math.PI*2;
    rig.objects.head.rotation.y=Math.max(-.55,Math.min(.55,angle));
  }
  if(state.action==='roommate_question')stage.objects.head.rotation.y+=.10*Math.sin(state.progress*Math.PI*4);
}

function updateScene(seconds,{draw=true}={}){
  const t=Math.min(timeline.duration-1/240,Math.max(0,Math.floor((seconds+1e-7)*12)/12));
  const shot=chooseShot(t),state=frameState(shot,t);
  world.show(state.set);stage.actorObjects.forEach(o=>{o.visible=state.heroVisible;});buddy.actorObjects.forEach(o=>{o.visible=state.buddyVisible;});
  buddy.materials.vest.color.set(state.role==='friend'?'#5b7e94':state.role==='clerk'?'#686a7d':'#526d92');buddy.materials.hair.color.set(state.role==='friend'?'#795342':'#453e39');
  stage.update(state.hero);buddy.update(state.buddy);stage.objects.ball.visible=false;buddy.objects.ball.visible=false;
  applyProps(state);cameraFor(state,shot);stage.scene.updateMatrixWorld(true);
  const active=state.set==='friend'||state.action==='boss'||state.action==='laundry'?buddy:stage;
  const relevant=shot.camera==='face'||shot.camera==='buddy_face'?['head','leftShoulder','rightShoulder']:['leftHand','rightHand','head'];
  const joints={hero:stage.debug.joints,buddy:buddy.debug.joints};
  const reachable=[];
  if(state.heroVisible)reachable.push(...stage.debug.reaches.map(r=>({...r,who:'hero'})));
  if(state.buddyVisible)reachable.push(...buddy.debug.reaches.map(r=>({...r,who:'buddy'})));
  const captionsActive=[];
  captions.forEach((cue,i)=>{const visible=t>=cue.start&&t<cue.end;captionElements[i].style.opacity=visible?'1':'0';if(visible)captionsActive.push(cue.id);});
  const tag=document.getElementById('flashback-tag');tag.style.opacity=shot.paragraph===2&&shot.action==='dinner_done'?'1':'0';
  const projected=Object.fromEntries(relevant.filter(k=>active.debug.joints[k]).map(k=>[k,V(active.debug.joints[k]).project(stage.camera).toArray()]));
  debug={t,shot:shot.id,paragraph:shot.paragraph,action:state.action,set:state.set,camera:shot.camera,heroVisible:state.heroVisible,buddyVisible:state.buddyVisible,reachable,joints,projected,props:state.props,water:state.water,captionsActive,feet:{hero:state.hero.actor,buddy:state.buddy.actor}};
  if(draw){renderer.render(stage.scene,stage.camera);gl.readPixels(0,0,1,1,gl.RGBA,gl.UNSIGNED_BYTE,pixel);lastTime=t;}
  return debug;
}
const ready=(async()=>{
  await document.fonts.load('700 50px Nunito');
  stage=makeScene(renderer);buddy=makeScene(renderer);
  for(const object of buddy.actorObjects)stage.scene.add(object);
  world=createWorld(stage);
  const keyHand=new THREE.Group();world.groups.entry.add(keyHand);world.prop.keyHand=keyHand;keyHand.position.set(.595,1.135,-1.10);
  stage.helpers.ellipsoid(keyHand,stage.materials.skin,[0,0,0],[.06,.065,.055]);stage.helpers.box(keyHand,stage.materials.cream,[.18,-.04,0],[.28,.11,.11],.04);
  stage.scene.traverse(o=>{if(o.isDirectionalLight&&o.castShadow)o.shadow.mapSize.set(768,768);});
  updateScene(0,{draw:false});
  renderer.compile(stage.scene,stage.camera);updateScene(0);
})();
window.__hf=window.__hf||{};window.__hf.buildReady=window.__hf.buildReady||{};window.__hf.buildReady['rest-film']=ready;
window.addEventListener('hf-seek',event=>{const work=ready.then(()=>updateScene(event.detail.time));event.detail.waitUntil?.(work);});
window.__restFilm={
  ready,timeline,
  seek:async t=>{await ready;return JSON.parse(JSON.stringify(updateScene(t)));},
  audit:async()=>{await ready;const prior=lastTime;const errors=[],landings=[];let samples=0,previous=null;for(let frame=0;frame<Math.round(timeline.duration*12);frame++){const d=updateScene(frame/12,{draw:false});samples++;for(const r of d.reachable)if(r.armError>.015||r.footError>.015)errors.push({t:d.t,shot:d.shot,action:d.action,...r});if(previous&&previous.shot===d.shot)for(const who of ['hero','buddy'])if(d[who+'Visible'])for(const side of ['left','right'])if(previous.feet[who][side].moving&&!d.feet[who][side].moving)landings.push({time:d.t+1/30,who,side,shot:d.shot});previous=d;}updateScene(prior);return {samples,errors,landings};},
  diagnostics:()=>({webgl:gl.getParameter(gl.VERSION),width:1920,height:1080,calls:renderer.info.render.calls}),
};
