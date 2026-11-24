import { build } from 'esbuild';
import { readFile,writeFile,mkdir,copyFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const root=path.resolve(fileURLToPath(new URL('../',import.meta.url)));
const engine=path.resolve(root,'../..');
const timeline=JSON.parse(await readFile(path.join(root,'assets/timeline.json'),'utf8'));
const captions=JSON.parse(await readFile(path.join(root,'assets/captions.json'),'utf8'));
await mkdir(path.join(root,'assets/vendor'),{recursive:true});
for(const name of ['three.min.js','three.min.js.LEGAL.txt','LICENSE-three.txt'])await copyFile(path.join(engine,'assets/vendor',name),path.join(root,'assets/vendor',name));
await build({entryPoints:[path.join(root,'src/main.mjs')],bundle:true,plugins:[{name:'local-three',setup(b){b.onResolve({filter:/^three$/},()=>({path:'./vendor/three.min.js',external:true}));}}],format:'esm',target:'chrome140',outfile:path.join(root,'assets/film.js'),minify:false,legalComments:'linked'});
const escape=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const subtitleMarkup=captions.map(c=>`<div id="caption-${c.id}" class="clip caption" data-start="${c.start}" data-duration="${c.end-c.start}" data-track-index="2" data-track-kind="captions" data-layout-allow-overlap><span class="caption-body">${escape(c.text)}</span></div>`).join('\n');
const html=`<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=1920,height=1080"><title>Why You Feel Guilty When You Rest</title><style>
@font-face{font-family:Nunito;src:url('assets/fonts/Nunito.ttf');font-weight:100 900;font-style:normal;font-display:block;}
*{box-sizing:border-box;margin:0;padding:0}html,body,#rest-film{width:1920px;height:1080px;overflow:hidden;background:#e9dccc}#rest-film{position:relative}#film-canvas{position:absolute;inset:0;width:1920px;height:1080px;display:block}.caption{position:absolute;left:192px;right:192px;bottom:105px;text-align:center;z-index:20;pointer-events:none}.caption-body{display:inline-block;opacity:0;white-space:nowrap;font:800 50px/1.24 Nunito,sans-serif;letter-spacing:.2px;color:#fffdf4;background:rgba(26,39,38,.88);padding:10px 22px 12px;border-radius:14px;text-shadow:0 2px 2px #172725}#flashback-tag{position:absolute;left:126px;top:82px;z-index:15;color:#29483e;background:#fff0cf;padding:13px 21px;border-radius:9px;font:800 38px Nunito,sans-serif;opacity:0}
</style></head><body><div id="rest-film" data-composition-id="rest-film" data-start="0" data-duration="${timeline.duration}" data-width="1920" data-height="1080" data-fps="12" data-no-timeline data-layout-allow-overlap>
<canvas id="film-canvas" class="clip" data-start="0" data-duration="${timeline.duration}" data-track-index="1" data-track-kind="graphics" data-layout-allow-overflow data-layout-allow-overlap></canvas>
<div id="flashback-tag">ONE HOUR EARLIER</div>
${subtitleMarkup}
<audio id="film-mix" class="clip" data-start="0" data-duration="${timeline.duration}" data-track-index="3" src="assets/mix.flac"></audio>
</div><script type="module" src="assets/film.js"></script></body></html>`;
await writeFile(path.join(root,'index.html'),html);
console.log(JSON.stringify({duration:timeline.duration,shots:timeline.shots.length,captions:captions.length,localOnly:true}));
