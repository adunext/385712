/* New flexible expressions in the retained native engine. Source coverage is separate. */
(() => {
 const defs=[['B1',250,258],['B2',260,270],['B3',272,282],['B4',284,292]],B=USER_INPUT.basic||{};
 const txt=v=>TEXT_GLOBAL(v);
 const fontFamily=()=>USER_INPUT.language==='en'?'Anton':'PuHuiTi';
 function fit(e,value,maxWidth,maxSize,minSize=42){
  const c=document.createElement('canvas').getContext('2d');let fs=maxSize;
  for(;fs>=minSize;fs--){c.font=`${USER_INPUT.language==='en'?400:900} ${fs}px ${fontFamily()}`;if(c.measureText(value).width+[...value].length*2<=maxWidth)break;}
  if(fs<minSize)throw Error('Text cannot fit this native expression without changing meaning: '+value);
  e.style.fontSize=fs+'px';return fs;
 }
 const bodyFamily=()=>USER_INPUT.language==='en'?'Geist':'PuHuiTi';
 function body(parent,value,x,y,w,fs=42){return mk(parent,`<div style="width:${w}px;${GE(fs,SILVER,600)};font-family:${bodyFamily()},sans-serif;line-height:1.25;white-space:pre">${txt(value)}</div>`,x,y,{ax:0,ay:.5});}
 function fitBody(e,value,w,fs=42){const lines=value.split('\n');if(lines.length>2)throw Error('Use one or two explicit semantic lines');const c=document.createElement('canvas').getContext('2d');for(const line of lines){c.font=`${USER_INPUT.language==='en'?600:900} ${fs}px ${bodyFamily()}`;if(c.measureText(line).width>w)throw Error('Explicit text line exceeds its expression width: '+line);}}
 for(const[id,T0,T1]of defs){if(!USER_INPUT.selected.includes(id))continue;window.CURRENT_UNIT=id;
  const sc=SC(T0,T1,BG,'',{gridOpt:{a:.028}}),D=sc.el,items=[],dx=USER_INPUT.presenter.mode==='none'?(id==='B3'?175:300):0;TKF.push([T0,'R',0,true]);
  const base=mk(D,`<div style="width:1920px;height:1080px;background:radial-gradient(ellipse 65% 85% at ${dx?50:30}% 45%,rgba(32,47,73,.58),rgba(5,6,7,0) 75%)"></div>`,0,0);place(base,{o:1});
  const badge=TX(D,txt(B.label||''),190,180,MONO(22,BLUE2,4));
  let headline,detail,panels=[];
  if(id==='B1'){
   headline=chars(D,B.keyword,190,350,HV(118,SILVER,2),{cst:METAL});detail=body(D,B.explanation,190,570,900);
   const path=svgPath(D,'M0 0 L260 0 Q310 0 350 -30 L420 -80',470,100,BLUE2,4,{glow:BLUE2,blur:8,x:190,y:730});items.push(path);
   sc.update=t=>{const u=t-T0;if(!sc.fit){fit(headline.firstChild,B.keyword,940,118,80);fitBody(detail.firstChild,B.explanation,900);sc.fit=true;}show(badge,t,T0+.12,{k:'mask',d:.4,out:T1-.5});charsAt(headline,t,T0+.5,{k:'slam',d:.28,stag:.045,out:T1-.5,os:.012});show(detail,t,T0+1.1,{k:'up',d:.6,out:T1-.5});pathAt(path,EZ.inout(pr(t,T0+1.25,T0+2.45)),1-pr(t,T1-.5,T1));fxDraw(c=>{glow(c,640+dx,450,460,'60,105,180',.14);sparks(c,t,T0+.75,260+dx,350,{n:36,life:.8,dir:0,spread:5,speed:430,g:650,seed:8});stars(c,USER_OUTPUT_TIME,60,.28,4);});};
   SOURCE_S('B1.hit',T0+.58,'thud',.55);SOURCE_S('B1.line',T0+1.25,'write',.25,0,{d:1.2});SOURCE_S('B1.exit',T1-.4,'swoosh',.3);
  }
  if(id==='B2'){
   badge._y=110;headline=chars(D,B.heading,190,250,HV(88,SILVER,2),{cst:METAL});
   panels=B.points.map((point,i)=>mk(D,`<div class="glass" style="position:relative;width:910px;height:110px;border-radius:13px;padding:14px 25px;display:flex;align-items:center;gap:24px;border-left:3px solid ${i%2?GOLD:BLUE2}"><span style="${AN(40,i%2?GOLD:BLUE2)}">${String(i+1).padStart(2,'0')}</span><span class="point" style="${GE(36,SILVER,600)};font-family:${bodyFamily()},sans-serif;line-height:1.12;white-space:pre">${txt(point)}</span></div>`,190,370+i*120,{ax:0,ay:.5}));
   sc.update=t=>{if(!sc.fit){fit(headline.firstChild,B.heading,920,88,64);for(let i=0;i<panels.length;i++)fitBody(panels[i].querySelector('.point'),B.points[i],790,36);sc.fit=true;}show(badge,t,T0+.1,{k:'mask',d:.4,out:T1-.5});charsAt(headline,t,T0+.35,{k:'up',d:.3,stag:.04,out:T1-.5});panels.forEach((p,i)=>show(p,t,T0+.9+i*.16,{k:'right',dist:100,d:.55,out:T1-.5,ob:6}));fxDraw(c=>{stars(c,USER_OUTPUT_TIME,65,.22,11);glow(c,650+dx,610,520,'160,190,230',.06);});};
   B.points.forEach((_,i)=>SOURCE_S('B2.card',T0+.9+i*.16,'card',.3,i%2?.2:-.2));SOURCE_S('B2.exit',T1-.4,'swipe',.3);
  }
  if(id==='B3'){
   TKF.push([T0,'TR',0,true]);
   headline=chars(D,B.heading,190,250,HV(92,SILVER,2),{cst:METAL});
   panels=[B.left,B.right].map((v,i)=>mk(D,`<div class="glass" style="width:520px;height:320px;border-radius:22px;padding:38px 30px;border-top:3px solid ${i?GOLD:BLUE2}"><div style="${MONO(18,i?GOLD:BLUE2,4)}">${i?'B':'A'}</div><div class="label" style="${HV(62,SILVER,2)};${i?GOLDF:METAL};margin-top:45px;white-space:pre">${txt(v)}</div></div>`,470+i*630,530,{ax:.5,ay:.5}));
   detail=body(D,B.conclusion,190,820,1180,40);
   sc.update=t=>{if(!sc.fit){fit(headline.firstChild,B.heading,1170,92,60);panels.forEach((p,i)=>fit(p.querySelector('.label'),i?B.right:B.left,460,62,40));fitBody(detail.firstChild,B.conclusion,1180,40);sc.fit=true;}show(badge,t,T0+.08,{k:'mask',out:T1-.5});charsAt(headline,t,T0+.4,{k:'mask',d:.3,stag:.03,out:T1-.5});panels.forEach((p,i)=>show(p,t,T0+.9+i*.24,{k:i?'right':'left',dist:170,d:.6,out:T1-.5}));show(detail,t,T0+2.1,{k:'up',d:.5,out:T1-.5});fxDraw(c=>{const a=pr(t,T0+1.5,T0+2.1)*(1-pr(t,T1-.5,T1));c.strokeStyle=`rgba(233,236,239,${a*.3})`;c.setLineDash([5,9]);c.beginPath();c.moveTo(730+dx,530);c.lineTo(840+dx,530);c.stroke();c.setLineDash([]);stars(c,USER_OUTPUT_TIME,55,.2,12);});};
   SOURCE_S('B3.left',T0+.9,'swoosh',.35,-.3);SOURCE_S('B3.right',T0+1.14,'swoosh',.35,.3);SOURCE_S('B3.detail',T0+2.1,'shine',.28);SOURCE_S('B3.exit',T1-.4,'swipe',.3);
  }
  if(id==='B4'){
   headline=chars(D,B.summary,190,380,HV(106,SILVER,2),{cst:METAL});detail=body(D,B.action,190,600,900);
   const line=mk(D,`<div style="width:850px;height:3px;background:linear-gradient(90deg,${GOLD},${BLUE2});box-shadow:0 0 20px rgba(125,178,255,.3)"></div>`,190,500);
   sc.update=t=>{if(!sc.fit){fit(headline.firstChild,B.summary,930,106,64);fitBody(detail.firstChild,B.action,900);sc.fit=true;}show(badge,t,T0+.1,{k:'mask',out:T1-.5});charsAt(headline,t,T0+.5,{k:'slam',d:.32,stag:.04,out:T1-.5});show(detail,t,T0+1.5,{k:'up',d:.6,out:T1-.5});place(line,{o:pr(t,T0+1.15,T0+1.45)*(1-pr(t,T1-.5,T1)),sx:EZ.out(pr(t,T0+1.15,T0+1.7))});fxDraw(c=>{glow(c,640+dx,460,480,'90,145,235',.1+.025*Math.sin(USER_OUTPUT_TIME*1.4));stars(c,USER_OUTPUT_TIME,75,.25,21);sparks(c,t,T0+.75,600+dx,380,{n:50,life:.8,dir:0,spread:6.2,speed:500,g:300,seed:16});});};
   SOURCE_S('B4.hit',T0+.6,'hit',.5);SOURCE_S('B4.action',T0+1.5,'shine',.28);SOURCE_S('B4.exit',T1-.4,'swoosh',.3);
  }
  sc.cam=t=>({x:960,y:540,z:1+Math.max(0,Math.sin(Math.PI*pr(t,T0+.5,T0+.9)))*.008});
  if(dx)for(const e of D.children)if(e!==base&&e.classList.contains('e'))e._x+=dx;
 }
})();
