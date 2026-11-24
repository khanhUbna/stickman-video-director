import * as THREE from 'three';

export function createWorld(stage) {
  const { scene, helpers: h, materials: m } = stage;
  const groups = {}; const prop = {}; const ui = {};
  const ink = '#283b3b';
  function group(name) { const g = new THREE.Group(); g.name = name; scene.add(g); groups[name] = g; return g; }
  function board(width = 1024, height = 640) {
    const canvas = document.createElement('canvas'); canvas.width = width; canvas.height = height;
    const context = canvas.getContext('2d'); const texture = new THREE.CanvasTexture(canvas); texture.colorSpace = THREE.SRGBColorSpace;
    const material = new THREE.MeshBasicMaterial({ map: texture, side: THREE.DoubleSide }); let signature = '';
    return { canvas, context, texture, material, paint(key, draw) { if (key === signature) return; signature = key; draw(context, width, height); texture.needsUpdate = true; } };
  }
  function words(ctx, text, x, y, maxWidth, line = 62) {
    let row = ''; let cy = y;
    for (const word of text.split(' ')) { const trial = row ? `${row} ${word}` : word; if (ctx.measureText(trial).width > maxWidth && row) { ctx.fillText(row, x, cy); row = word; cy += line; } else row = trial; }
    if (row) ctx.fillText(row, x, cy); return cy;
  }
  function room(name, wall = '#dfd2bc', openBack = false) {
    const g = group(name);
    h.box(g, m.floor, [0, -0.12, 0], [8.5, 0.24, 4.7], 0.08);
    if (!openBack) h.box(g, h.material(wall), [0, 1.9, -1.85], [8.5, 3.8, 0.14], 0.06);
    h.box(g, h.material(wall), [-4.2, 1.9, -0.4], [0.14, 3.8, 2.9], 0.06);
    return g;
  }
  const living = group('living');
  h.cylinder(living, m.shoe, [1.25, 0.36, 0.82], 0.065, 0.72);
  h.cylinder(living, m.trim, [1.25, 0.76, 0.82], 0.55, 0.09);
  const work = room('work', '#d6ddd1', true);
  prop.workFrontWall=h.box(work, h.material('#d6ddd1'), [0, 1.9, 1.85], [8.5, 3.8, 0.14], 0.06);
  prop.workBackWall=h.box(work, h.material('#d6ddd1'), [0, 1.9, -1.85], [8.5, 3.8, 0.14], 0.06);
  h.box(work, m.trim, [0, 0.86, 0.65], [2.7, 0.12, 1.1], 0.05);
  for (const x of [-1.1, 1.1]) for (const z of [0.24, 1.06]) h.cylinder(work, m.shoe, [x, 0.42, z], 0.06, 0.84);
  const chair = new THREE.Group(); work.add(chair); prop.chair = chair;
  h.box(chair, m.sage, [0, 0.55, 0], [0.78, 0.15, 0.72], 0.08);
  h.box(chair, m.sage, [0, 1.00, -0.33], [0.78, 0.85, 0.12], 0.08);
  for (const x of [-0.28, 0.28]) for (const z of [-0.24, 0.24]) h.cylinder(chair, m.shoe, [x, 0.25, z], 0.045, 0.50);
  const laptop = new THREE.Group(); laptop.position.set(0, 0.95, 0.70); work.add(laptop); prop.laptop = laptop;
  h.box(laptop, h.material('#70837f'), [0, 0, 0], [1.04, 0.035, 0.70], 0.025);
  for (let y = 0; y < 3; y++) for (let x = 0; x < 9; x++) h.box(laptop, m.cream, [-0.40 + x * 0.10, 0.025, -0.04 + y * 0.09], [0.075, 0.018, 0.06], 0.008);
  const lid = new THREE.Group(); lid.position.set(0, 0.02, 0.32); laptop.add(lid); prop.lid = lid;
  h.box(lid, h.material('#70837f'), [0, 0.34, 0], [1.04, 0.68, 0.045], 0.025);
  ui.laptop = board();
  const display = new THREE.Mesh(new THREE.PlaneGeometry(0.96, 0.59), ui.laptop.material); display.rotation.y = Math.PI; display.position.set(0, 0.34, -0.026); lid.add(display);
  h.cylinder(work, m.sage, [-1.0, 1.10, 0.95], 0.055, 0.42);
  const lampShade = new THREE.Mesh(new THREE.ConeGeometry(0.23, 0.28, 20), h.material('#d4b678')); lampShade.position.set(-1, 1.42, 0.95); work.add(lampShade);

  const kitchen = room('kitchen', '#cbd7c7');
  h.box(kitchen, m.sage, [0, 0.47, 1.30], [3.55, 0.94, 0.94], 0.07);
  h.box(kitchen, m.cream, [0, 0.99, 1.30], [3.72, 0.10, 1.06], 0.045);
  for (const x of [-1.15, 0, 1.15]) { h.box(kitchen, h.material('#9ab5a0'), [x, 0.47, 0.82], [1.05, 0.77, 0.04], 0.03); h.cylinder(kitchen, m.shoe, [x + 0.32, 0.55, 0.78], 0.025, 0.16).rotation.z = Math.PI / 2; }
  h.box(kitchen, h.material('#526d71'), [0.05, 1.05, 1.25], [0.92, 0.05, 0.63], 0.09);
  h.box(kitchen, h.material('#a2bab7'), [0.05, 1.078, 1.25], [0.74, 0.025, 0.49], 0.08);
  const faucetCurve = new THREE.CatmullRomCurve3([[0.40,1.04,1.58],[0.40,1.60,1.58],[0.22,1.65,1.32],[0.12,1.46,1.16]].map(p => new THREE.Vector3(...p)));
  kitchen.add(new THREE.Mesh(new THREE.TubeGeometry(faucetCurve, 20, 0.035, 10, false), h.material('#789995')));
  const valve = h.box(kitchen, m.shoe, [0.55, 1.10, 1.05], [0.16, 0.045, 0.045], 0.02); prop.valve = valve;
  h.box(kitchen, m.shoe, [-0.9, 1.06, 1.19], [0.75, 0.04, 0.52], 0.025);
  for (let i=0;i<5;i++) h.box(kitchen, m.trim, [-1.15+i*0.13, 1.13, 1.19], [0.02, 0.15, 0.47], 0.008);
  const water = h.cylinder(kitchen, h.material('#9bced1', {transparent:true,opacity:0.62,roughness:0.3}), [0.12, 1.27, 1.16], 0.018, 0.40); water.visible=false; prop.water=water;
  for (let i=0;i<3;i++) h.box(kitchen, m.cream, [-1.20+i*1.12, 2.40, -1.65], [0.92, 0.96, 0.18], 0.06);

  const entry = room('entry', '#d9c3a8');
  h.box(entry, m.shoe, [0, 1.30, -1.60], [1.65, 2.60, 0.15], 0.04);
  h.box(entry, h.material('#c89968'), [0, 1.30, -1.48], [1.42, 2.40, 0.075], 0.03);
  const knob=h.ellipsoid(entry,m.trim,[0.50,1.20,-1.40],[0.075,0.075,0.06]);prop.doorKnob=knob;
  const key = new THREE.Group(); scene.add(key); prop.key=key;
  const brass=h.material('#b67f21');const keyring=new THREE.Mesh(new THREE.TorusGeometry(0.065,0.014,8,32),brass);keyring.position.z=.16;key.add(keyring);h.box(key,brass,[0,0,.025],[.032,.032,.24],.005);for(const z of [-.055,-.015])h.box(key,brass,[.027,-.012,z],[.035,.035,.022],.003);h.ellipsoid(entry,m.ink,[.50,1.20,-1.332],[.017,.027,.004]);
  h.box(entry,m.trim,[-2.1,1.65,-1.57],[0.8,0.1,0.1],0.02);
  for(const x of [-2.35,-2.10,-1.85])h.ellipsoid(entry,m.shoe,[x,1.59,-1.47],[0.035,0.07,0.04]);

  const friend=room('friend','#b9cdd2');
  h.box(friend,m.sage,[0,0.34,0],[2.45,0.48,1.35],0.12);h.box(friend,h.material('#d0b7a3'),[0,0.64,0],[2.36,0.21,1.26],0.12);
  h.box(friend,m.cream,[0.70,0.88,-0.2],[0.64,0.23,0.7],0.10);h.box(friend,h.material('#84a6a6'),[-0.4,0.83,0.12],[1.4,0.18,1.15],0.10);
  h.box(friend,m.trim,[-2.3,0.6,-0.8],[0.75,1.2,0.55],0.05);
  for(let i=0;i<5;i++)h.box(friend,h.material(['#9d6652','#c6a872','#4f6c70'][i%3]),[-2.52+i*.11,1.37,-.8],[.08,.3,.3],.015);

  const inspection=room('inspection','#bfc7c3');
  h.box(inspection,h.material('#718b85'),[0.5,.65,.7],[2.8,1.3,.65],.07);
  const inspectionSign=board(800,400); ui.inspection=inspectionSign;
  const sign=new THREE.Mesh(new THREE.PlaneGeometry(1.5,.75),inspectionSign.material);sign.position.set(.5,1.25,1.04);inspection.add(sign);
  inspectionSign.paint('receipt',ctx=>{ctx.fillStyle='#f4e4c6';ctx.fillRect(0,0,800,400);ctx.fillStyle=ink;ctx.textAlign='center';ctx.font='800 80px Nunito';ctx.fillText('REST DESK',400,140);ctx.font='700 52px Nunito';ctx.fillText('Receipt required',400,260);});

  function loose(name) {const g=new THREE.Group();g.name=name;scene.add(g);prop[name]=g;return g;}
  const phone=loose('phone');h.box(phone,m.ink,[0,0,0],[.25,.45,.035],.025);ui.phone=board(500,900);
  const phoneScreen=new THREE.Mesh(new THREE.PlaneGeometry(.224,.404),ui.phone.material);phoneScreen.position.z=.019;phone.add(phoneScreen);prop.phoneScreen=phoneScreen;
  const remote=loose('remote');h.box(remote,m.ink,[0,0,0],[.085,.035,.23],.023);for(let i=0;i<3;i++)h.ellipsoid(remote,i?m.cream:m.sofa,[0,.021,-.06+i*.06],[.014,.008,.014]);
  const bowl=loose('bowl');const half=new THREE.Mesh(new THREE.SphereGeometry(1,24,12,0,Math.PI*2,Math.PI/2,Math.PI/2),h.material('#b0c7bd',{side:THREE.DoubleSide}));half.scale.set(.20,.14,.20);bowl.add(half);const rim=new THREE.Mesh(new THREE.TorusGeometry(.20,.018,6,32),m.cream);rim.rotation.x=Math.PI/2;bowl.add(rim);for(let i=0;i<12;i++){const a=i*2.4;h.ellipsoid(bowl,m.cream,[Math.sin(a)*.13,.015+Math.floor(i/5)*.025,Math.cos(a)*.11],[.038,.043,.038]);}
  const snack=loose('snack');h.ellipsoid(snack,h.material('#d3a56a'),[0,0,0],[.055,.025,.052]);
  const plate=loose('plate');h.cylinder(plate,m.white,[0,0,0],.235,.018);const edge=new THREE.Mesh(new THREE.TorusGeometry(.22,.018,8,32),m.white);edge.rotation.x=Math.PI/2;plate.add(edge);
  const pen=loose('pen');h.cylinder(pen,m.vest,[0,0,0],.014,.24);const tip=new THREE.Mesh(new THREE.ConeGeometry(.012,.045,8),m.ink);tip.rotation.x=Math.PI;tip.position.y=-.14;pen.add(tip);
  const paper=loose('paper');ui.paper=board(900,600);const page=new THREE.Mesh(new THREE.PlaneGeometry(.78,.52),ui.paper.material);page.rotation.x=-Math.PI/2;paper.add(page);
  const basket=loose('basket');h.box(basket,m.sage,[0,0,0],[.70,.36,.46],.07);for(let i=0;i<4;i++)h.ellipsoid(basket,h.material(['#d5b88f','#e4d5b4','#a9b9b4'][i%3]),[-.2+i*.13,.17,.0],[.16,.10,.15]);
  const cup=loose('cup');h.cylinder(cup,m.cream,[0,0,0],.09,.20);h.cylinder(cup,h.material('#9abcc0'),[0,.101,0],.075,.008);
  const receipt=loose('receipt');ui.receipt=board(700,700);const receiptFace=new THREE.Mesh(new THREE.PlaneGeometry(.62,.62),ui.receipt.material);receipt.add(receiptFace);ui.receipt.paint('receipt',ctx=>{ctx.fillStyle='#f5e4bf';ctx.fillRect(0,0,700,700);ctx.fillStyle=ink;ctx.textAlign='center';ctx.font='800 75px Nunito';ctx.fillText('YOUR RECEIPT?',350,180);ctx.font='600 53px Nunito';ctx.fillText('Permission to rest',350,360);ctx.fillText('Not found',350,500);});
  const insertHands=loose('insertHands');h.ellipsoid(insertHands,m.skin,[-.162,-.18,.015],[.045,.075,.050]);h.ellipsoid(insertHands,m.skin,[.162,-.18,.015],[.045,.075,.050]);prop.insertFinger=h.ellipsoid(insertHands,m.skin,[.105,-.205,.05],[.022,.03,.025]);

  function show(set) {for(const [name,g]of Object.entries(groups))g.visible=name===set;stage.environmentObjects.forEach(o=>{o.visible=set==='living';});for(const object of Object.values(prop))if(object.parent===scene)object.visible=false;}
  function phoneText(message,draft='',mode='message',progress=1) {
    const text=draft.slice(0,Math.round(draft.length*progress));ui.phone.paint(`${message}|${text}|${mode}`,ctx=>{
      ctx.fillStyle='#f4eddf';ctx.fillRect(0,0,500,900);ctx.fillStyle='#315f55';ctx.fillRect(0,0,500,120);ctx.font='800 52px Nunito';ctx.fillStyle='#fff9e9';ctx.fillText(mode==='timer'?'Timer':'Messages',30,80);
      if(mode==='timer'){ctx.fillStyle=ink;ctx.textAlign='center';ctx.font='800 104px Nunito';ctx.fillText(message,250,400);ctx.textAlign='left';ctx.font='600 44px Nunito';words(ctx,'Your break',70,530,360,56);return;}
      ctx.fillStyle='#dce5da';ctx.fillRect(25,170,450,300);ctx.fillStyle=ink;ctx.font='700 48px Nunito';words(ctx,message,45,235,410,64);
      if(draft){ctx.fillStyle='#fffdf5';ctx.fillRect(25,515,450,285);ctx.fillStyle=ink;ctx.font='700 47px Nunito';words(ctx,text,45,575,410,60);ctx.font='800 36px Nunito';ctx.fillStyle='#90664c';ctx.fillText(mode==='unsent'?'UNSENT':'Reply',45,845);}
    });
  }
  function laptopText(mode,progress=1) {ui.laptop.paint(`${mode}|${Math.floor(progress*40)}`,ctx=>{
    ctx.fillStyle='#f2ebd7';ctx.fillRect(0,0,1024,640);ctx.fillStyle='#315f55';ctx.fillRect(0,0,1024,95);ctx.fillStyle='#fff9eb';ctx.font='800 48px Nunito';ctx.fillText(mode==='document'?'Document':'Inbox',42,65);ctx.fillStyle=ink;
    if(mode==='document'){ctx.font='800 53px Nunito';ctx.fillText('A small correction',42,180);ctx.font='600 44px Nunito';words(ctx,'Fix this paragraph tomorrow. The urgent work is done.',42,275,910,70);ctx.fillStyle='#b95f4f';ctx.fillRect(42,360,650,10);return;}
    ctx.font='800 53px Nunito';ctx.fillText('One last email',42,185);ctx.font='600 44px Nunito';words(ctx,mode==='reply'?'Thanks, I will send the update tomorrow.'.slice(0,Math.round(progress*43)):'Quick question about the document.',42,280,910,65);
    if(mode==='overflow'){ctx.fillStyle='#d9e2d6';for(let i=0;i<3;i++){ctx.fillRect(40,245+i*112,940,88);ctx.fillStyle=ink;ctx.font='700 38px Nunito';ctx.fillText(['Another message','A document to check','One small change'][i],60,302+i*112);ctx.fillStyle='#d9e2d6';}}
    else{ctx.fillStyle='#315f55';ctx.fillRect(760,500,200,85);ctx.fillStyle='#fff9eb';ctx.font='800 42px Nunito';ctx.fillText(mode==='sent'?'Sent':'Send',795,557);}
  });}
  function noteText(progress=1){const text='FIX PARAGRAPH\nTomorrow\nAfter breakfast';ui.paper.paint(`note|${Math.floor(progress*text.length)}`,ctx=>{ctx.fillStyle='#f8ebca';ctx.fillRect(0,0,900,600);ctx.fillStyle=ink;ctx.font='800 66px Nunito';text.slice(0,Math.round(progress*text.length)).split('\n').forEach((line,i)=>ctx.fillText(line,60,140+i*140));});}
  return {groups,prop,ui,show,phoneText,laptopText,noteText};
}
