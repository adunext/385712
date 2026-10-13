/* Explicit consumer inputs. No author media, narration, or implicit demo mode. */
const USER_INPUT=window.KINETIC_INPUT;
const TEXT_GLOBAL=s=>String(s??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const RAW_TEXT=id=>{const v=USER_INPUT.content[id];if(v===undefined)throw Error('needs-binding: '+id);return v;};
const TEXT=id=>TEXT_GLOBAL(RAW_TEXT(id));
window.USER_OUTPUT_TIME=0;
window.userPresenter=t=>{const p=USER_INPUT.presenter;if(p.mode==='none')return USER_INPUT.blank;if(p.mode==='image')return p.file;return p.directory+'/'+String(Math.min(p.frames-1,Math.max(0,Math.floor(t*60+1e-6)))).padStart(5,'0')+'.jpg';};
window.userFace=t=>{
 const p=USER_INPUT.presenter,rows=p.tracking;
 if(!rows?.length)return p.face||{cx:.5,cy:.4,h:.3};
 let i=0;while(i<rows.length-1&&rows[i+1].time<=t)i++;
 const a=rows[i],b=rows[Math.min(i+1,rows.length-1)],k=b.time>a.time?Math.min(1,Math.max(0,(t-a.time)/(b.time-a.time))):0;
 return Object.fromEntries(['cx','cy','h'].map(n=>[n,a[n]+(b[n]-a[n])*k]));
};
window.mediaPoster=id=>USER_INPUT.media.thumbnail?.file||USER_INPUT.blank;
window.resolveMedia=src=>{
 if(src.startsWith('brand/')||src==='assets/grain.png')return src;
 if(src.startsWith('talk/'))return window.userPresenter(window.USER_OUTPUT_TIME);
 let role,frame=0,m;
 if((m=src.match(/^assets\/cmt\/c(\d+)/))){const p=USER_INPUT.media.feedback?.[+m[1]];if(!p)throw Error('needs-binding: feedback '+m[1]);return p.file;}
 if((m=src.match(/^sc\/wall2\/(\d+)\/f_(\d+)/))){role='wall';frame=+m[2]-1;const p=USER_INPUT.media.wall?.[+m[1]];if(!p)throw Error('needs-binding: gallery wall '+m[1]);return p.mode==='image'?p.file:p.directory+'/'+String(frame).padStart(5,'0')+'.jpg';}
 if(src.startsWith('sc/thumb/'))role='thumbnail';
 else if((m=src.match(/^sc\/([^/]+)\/f_(\d+)/))){role=m[1];frame=+m[2]-1;}
 if(role){const p=USER_INPUT.media[role];if(!p)throw Error('needs-binding: '+role);return p.mode==='image'?p.file:p.directory+'/'+String(frame).padStart(5,'0')+'.jpg';}
 if(src===USER_INPUT.blank||Object.values(USER_INPUT.media).some(p=>p?.file===src)||src.startsWith('user-assets/'))return src;
 throw Error('Undeclared media path: '+src);
};
window.kineticInitialize=async()=>{
 await READY;
 window.imgWait=async()=>{const rows=[..._pending].map(im=>({im,src:im.src}));_pending.clear();await Promise.all(rows.map(async({im,src})=>{await im.decode();if(im.src!==src||!im.naturalWidth)throw Error('Current media frame did not decode: '+src);}));};
 const native=window.renderAt;
 const box=document.createElement('div');box.id='user-captions';
 box.style.cssText='position:absolute;left:150px;right:150px;top:930px;text-align:center;font:650 48px/1.24 PuHuiTi,Geist,sans-serif;letter-spacing:.6px;color:white;-webkit-text-stroke:5px rgba(5,6,8,.95);paint-order:stroke fill;pointer-events:none';$('ov').append(box);
 const top=document.createElement('div'),clock=document.createElement('div'),mark=document.createElement('img');
 top.style.cssText='position:absolute;left:72px;top:40px;height:40px;display:flex;align-items:center;font:500 24px "Geist Mono",PuHuiTi,sans-serif;letter-spacing:3px';
 clock.style.cssText='position:absolute;right:72px;top:40px;height:40px;display:flex;align-items:center;font:500 24px "Geist Mono",monospace;letter-spacing:3px';
 mark.style.cssText='position:absolute;right:77px;top:27px;width:66px;height:66px;object-fit:contain;pointer-events:none';$('ov').append(top,clock,mark);
 const marks={};for(const tone of['lighter','path']){marks[tone]=[];for(let i=0;i<132;i++){const im=new Image();im.src=`brand/frames-${tone}/${String(i).padStart(3,'0')}.png`;await im.decode();marks[tone].push(im);}}
 const nativeTKState=tkState;
 tkState=t=>{const s=nativeTKState(t);if(t>=173.25&&t<180.6){const p=EZ.inout(pr(t,173.25,173.8))*(1-EZ.inout(pr(t,179.9,180.6)));for(const[k,n]of Object.entries({x:1700,y:240,w:230,h:230,r:115}))s[k]=lerp(s[k],n,p);}return s;};
 const nativeExtra=window.TK_EXTRA;window.TK_EXTRA=t=>({...nativeExtra?.(t),...(USER_INPUT.presenter.mode==='none'?{o:0}:{})});
 function toneAt(s){const scene=SCENES.filter(g=>s>=g.s&&s<g.e).at(-1);if(scene?.inkHud)return'path';const full=[...$('top').querySelectorAll('.e')].filter(e=>{const r=e.getBoundingClientRect(),st=getComputedStyle(e);return r.width>1900&&r.height>1070&&+st.opacity>.8&&st.visibility==='visible'&&getComputedStyle(e.parentElement).display!=='none';});for(const e of full){const rgb=getComputedStyle(e.firstElementChild).backgroundColor.match(/[\d.]+/g);if(rgb&&(rgb.length<4?1:+rgb[3])>.9&&(.2126*+rgb[0]+.7152*+rgb[1]+.0722*+rgb[2])>155)return'path';}return'lighter';}
 let current=-1,us=[];
 function captionAt(t){const i=USER_INPUT.captions.findIndex(c=>t>=c.start&&t<c.end);if(i<0){box.style.opacity=0;current=-1;return;}const c=USER_INPUT.captions[i];if(i!==current){current=i;box.replaceChildren();us=[];let line=document.createElement('div');line.style.whiteSpace='nowrap';box.append(line);const values=c.units?.length?c.units:[{text:c.text}];for(let j=0;j<values.length;j++){if(c.breakAfter?.includes(j-1)){line=document.createElement('div');line.style.whiteSpace='nowrap';box.append(line);}const u=values[j],e=document.createElement('span');e.textContent=u.text;e.style.cssText='position:relative;display:inline-block;white-space:pre';if(u.start!==undefined){const fill=document.createElement('span');fill.textContent=u.text;fill.style.cssText='position:absolute;inset:0;color:#7db2ff;white-space:pre';e.append(fill);us.push({u,fill});}line.append(e);}}
  for(const{u,fill}of us)fill.style.clipPath=`inset(0 ${100*(1-clamp((t-u.start)/Math.max(.02,u.end-u.start)))}% 0 0)`;
  box.style.opacity=Math.min(pr(t,c.start,c.start+.08),1-pr(t,c.end-.08,c.end));
 }
 window.renderAt=async t=>{
  if(!Number.isFinite(t)||t<0||t>=USER_INPUT.duration)throw Error('Output time outside plan');
  const p=USER_INPUT.plan.find(p=>t>=p.outputStart&&t<p.outputEnd)||USER_INPUT.plan.at(-1),u=t-p.outputStart,extra=p.outputEnd-p.outputStart-(p.sourceEnd-p.sourceStart),hold=p.holdAt===undefined?Infinity:p.holdAt-p.sourceStart,s=p.sourceStart+(u<hold?u:u<hold+extra?hold:u-extra);
  window.USER_OUTPUT_TIME=t;native(s);$('fade').style.opacity=clamp((t-(USER_INPUT.duration-.5))/.45);HUD.tl.style.opacity=HUD.tr.style.opacity=0;captionAt(t);
  const tone=toneAt(s),ink=tone==='path'?'#171d21':'#a5b2c0',w=USER_INPUT.markWindows.find(w=>t>=w.start&&t<w.end),a=w?Math.min(pr(t,w.start,w.start+.4),1-pr(t,w.end-.4,w.end))*.52:0;
  top.textContent=p.title;clock.textContent=tcode(t);top.style.color=clock.style.color=ink;clock.style.opacity=1-a/.52;mark.style.opacity=a;
  if(w)mark.src=marks[tone][Math.min(131,Math.floor((t-w.start)*24))].src;
  window.USER_STATE={outputTime:t,sourceTime:s,unit:p.id,presenter:tkState(s),mark:{tone,opacity:a},captions:[...box.children].map(e=>({text:e.textContent,width:e.getBoundingClientRect().width}))};
  await imgWait();
 };
 window.USER_READY=true;
};
