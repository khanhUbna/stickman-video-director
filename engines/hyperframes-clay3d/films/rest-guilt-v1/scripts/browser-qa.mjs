import puppeteer from 'puppeteer-core';
import {createServer}from'node:http';
import {readFile,writeFile,mkdir}from'node:fs/promises';
import {fileURLToPath}from'node:url';
import path from'node:path';
import {createHash}from'node:crypto';
const root=path.resolve(fileURLToPath(new URL('../',import.meta.url))),output=path.join(root,'output');await mkdir(output,{recursive:true});
const server=createServer(async(req,res)=>{const name=decodeURIComponent(new URL(req.url,'http://localhost').pathname).replace(/^\/+/, '')||'index.html';const file=path.resolve(root,name);if(!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}try{const body=await readFile(file);res.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':file.endsWith('.flac')?'audio/flac':file.endsWith('.ttf')?'font/ttf':'text/html');res.end(body);}catch{res.writeHead(404).end();}});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));let browser;
try{
 browser=await puppeteer.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-background-networking'],defaultViewport:{width:1920,height:1080,deviceScaleFactor:1}});
 const page=await browser.newPage(),errors=[],outside=[];
 page.on('pageerror',e=>{errors.push(e.message);console.error('Page error:',e.message);});await page.setRequestInterception(true);
 page.on('request',req=>{if(req.url().startsWith(`http://127.0.0.1:${server.address().port}/`)||/^(data:|blob:)/.test(req.url()))req.continue();else{outside.push(req.url());req.abort();}});
 const response=await page.goto(`http://127.0.0.1:${server.address().port}/`,{waitUntil:'load',timeout:60000});if(!response.ok()||errors.length)throw Error(`Load failed: ${errors.join('; ')}`);
 await page.waitForFunction(()=>!!window.__restFilm,{timeout:60000});await page.evaluate(()=>window.__restFilm.ready);
 const audit=await page.evaluate(()=>window.__restFilm.audit());await writeFile(path.join(output,'motion-audit.json'),JSON.stringify(audit,null,2)+'\n');
 console.log(JSON.stringify({motion_samples:audit.samples,contact_errors:audit.errors.length,first_errors:audit.errors.slice(0,8)}));
 const allShots=await page.evaluate(()=>window.__restFilm.timeline.shots);const selected=process.argv.slice(2);const shots=selected.length?allShots.filter(s=>selected.includes(s.id)):allShots;const frames=[];
 for(const shot of shots){const time=shot.start+shot.duration*.58;const frame=await page.evaluate(t=>window.__restFilm.seek(t),time);await page.screenshot({path:path.join(output,`${shot.id}.png`)});frames.push({shot:shot.id,time,action:shot.action,camera:shot.camera,reachable:frame.reachable,props:frame.props,projected:frame.projected});console.log(JSON.stringify({snapshot:shot.id,time:Math.round(time*10)/10}));}
 await page.evaluate(()=>window.__restFilm.seek(25));const first=await page.screenshot();await page.evaluate(()=>window.__restFilm.seek(210));await page.evaluate(()=>window.__restFilm.seek(25));const second=await page.screenshot();
 const hash=b=>createHash('sha256').update(b).digest('hex');
 const captionGeometry=await page.evaluate(()=>[...document.querySelectorAll('.caption-body')].map(n=>{const r=n.getBoundingClientRect();return {width:r.width,height:r.height,text:n.textContent};}));
 const overflow=captionGeometry.filter(x=>x.width>1536||x.height>100);const report={ok:!errors.length&&!outside.length&&!audit.errors.length&&!overflow.length&&hash(first)===hash(second),pageErrors:errors,externalRequests:outside,motion:audit,shots:frames.length,coverage:selected.length?'changed-shot follow-up; all motion samples still audited':'all shots',frames,captionOverflow:overflow,deterministicImage:hash(first)===hash(second),diagnostics:await page.evaluate(()=>window.__restFilm.diagnostics())};
 await writeFile(path.join(output,selected.length?'browser-qa-fixes.json':'browser-qa.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({ok:report.ok,shots:frames.length,errors:errors.length,contacts:audit.errors.length,captionOverflow:overflow.length,deterministic:report.deterministicImage}));if(!report.ok)process.exitCode=1;
}finally{await browser?.close();await new Promise(resolve=>server.close(resolve));}
