# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy", "soundfile", "pyloudnorm", "jsonschema"]
# ///
"""Native kinetic source adapter; required content is always explicit."""
from pathlib import Path
import argparse,json,hashlib,math,re,shutil,subprocess,sys
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parent;CORE=ROOT/'core'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def save(p,o):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):
 with Path(p).open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()
def digest():
 # This candidate identity is explicitly separate from the platform's signed manifest digest.
 rows={n:sha(ROOT/n)for n in sorted(read(ROOT/'integrity.json')['files'])if n!='content-boundary.json'}
 rows['integrity.json']=sha(ROOT/'integrity.json')
 return hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def media_path(root,value):
 if not isinstance(value,str)or not value:raise ValueError('needs-binding: media file')
 q=Path(value);raw=q if q.is_absolute()else root/q;p=raw.resolve()
 if raw.is_symlink()or not p.is_file():raise ValueError('Missing media or symlink: '+value)
 if not q.is_absolute()and not p.is_relative_to(root):raise ValueError('Relative media escapes the input directory')
 return p
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
def spec(p):
 data=probe(p);s=next((s for s in data['streams']if s['codec_type']=='video'),None)
 if not s:raise ValueError('Visual input has no video/image stream')
 if s.get('color_transfer')in['smpte2084','arib-std-b67']or any('DOVI'in str(v)for v in s.get('side_data_list',[])):raise ValueError('HDR input requires an explicit color-converted source')
 if s.get('sample_aspect_ratio','1:1')not in['1:1','0:1','N/A']:raise ValueError('Non-square pixels require explicit preprocessing')
 w,h=s['width'],s['height'];rotation=next((v.get('rotation',0)for v in s.get('side_data_list',[])if'rotation'in v),0)
 if abs(rotation)%180==90:w,h=h,w
 return w,h,float(data['format'].get('duration',0))
def plan(input_file):
 source=input_file.resolve();d=read(source);root=source.parent;catalog=read(CORE/'catalog.json');groups={g['id']:g for g in catalog['groups']};schema=read(CORE/'content.schema.json')['fields']
 errors=sorted(Draft202012Validator(read(ROOT/'params.schema.json')).iter_errors(d),key=lambda e:str(list(e.path)))
 if errors:raise ValueError('Invalid input: '+str(list(errors[0].path))+' '+errors[0].message)
 if d.get('mode')!='user-media':raise ValueError('Use user-media; no demo fallback exists')
 if d.get('language')not in['zh','en']:raise ValueError('Choose zh or en')
 if d.get('layout')!='landscape':raise ValueError('Portrait adaptation is not yet declared supported by this candidate')
 selected=d.get('scenes');content=d.get('content',{})
 if not isinstance(selected,list)or not 1<=len(selected)<=30:raise ValueError('needs-binding: select 1–30 native units')
 cursor=0;spans=[];active=set();required=set();roles=set()
 for item in selected:
  if not isinstance(item,dict)or item.get('id')not in groups:raise ValueError('Unknown scene')
  g=groups[item['id']];first_frame=round(g['start']*60);last_frame=round(g['end']*60);dur=(last_frame-first_frame)/60
  if g.get('maxReadingHold'):
   chosen=item.get('duration',dur)
   if not dur<=chosen<=dur+g['maxReadingHold']:raise ValueError('Basic reading hold exceeds its bounded range')
   extra=chosen-dur
  else:
   if 'duration'in item and abs(item['duration']-dur)>1e-6:raise ValueError('Native actions keep their source duration')
   extra=0
  if not isinstance(item.get('title'),str)or not item['title'].strip()or len(item['title'])>45:raise ValueError('needs-binding: short user chapter label')
  overlapping={n['id']for n in groups.values()if n['start']<g['end']-1e-4 and n['end']>g['start']+1e-4};active.update(overlapping)
  for ident in overlapping:required.update(groups[ident]['fields']);roles.update(groups[ident]['media'])
  span={'id':g['id'],'title':item['title'],'activeUnits':sorted(overlapping),'sourceStart':first_frame/60,'sourceEnd':last_frame/60,'sourceWindow':[g['start'],g['end']],'sourceFrames':[first_frame,last_frame],'outputStart':cursor,'outputEnd':cursor+dur+extra}
  if extra:span['holdAt']=g['holdAt']
  spans.append(span);cursor+=dur+extra
 if cursor>600:raise ValueError('Candidate supports at most 10 minutes')
 if d.get('duration')is not None and abs(d['duration']-cursor)>1/120:raise ValueError('Declared duration does not match the selected native windows')
 for f in schema:
  v=content.get(f['id'],'');limit=f['maxChars']if d['language']=='zh'else f['maxChars']*3+12
  if not isinstance(v,str)or len(v)>limit:raise ValueError('Text exceeds provisional capacity: '+f['id'])
  if f['id']in required and not v.strip():raise ValueError('needs-binding: '+f['id'])
 basic=d.get('basic',{});requirements={'B1':['keyword','explanation'],'B2':['heading','points'],'B3':['heading','left','right','conclusion'],'B4':['summary','action']};limits={'keyword':8,'heading':10,'left':8,'right':8,'explanation':42,'conclusion':48,'summary':10,'action':42,'label':32}
 for id in active:
  for key in requirements.get(id,[]):
   value=basic.get(key)
   if key=='points':
    if not isinstance(value,list)or not 1<=len(value)<=5 or any(not isinstance(v,str)or not v.strip()or len(v.split('\n'))>2 or any(len(line)>(18 if d['language']=='zh'else 44)for line in v.split('\n'))for v in value):raise ValueError('needs-binding: one to five neutral user points, each one or two explicit lines')
   elif not isinstance(value,str)or not value.strip():raise ValueError('needs-binding: basic.'+key)
 for key,value in basic.items():
  if key in limits and (not isinstance(value,str)or len(value)>(limits[key]if d['language']=='zh'else limits[key]*3+12)or len(value.split('\n'))>2):raise ValueError('Basic expression text exceeds capacity: '+key)
 for key in['title','presenterLabel']:
  if not isinstance(d.get(key),str)or len(d[key])>45:raise ValueError('needs-binding: '+key)
 media=d.get('media',{});assets={};consumed=[];ports=catalog['mediaPorts']
 def bind(role,value,port=None):
  if not isinstance(value,dict)or value.get('mode')not in['image','video']:raise ValueError('needs-binding: '+role+' image/video')
  p=media_path(root,value.get('file'));w,h,duration=spec(p);v={**value,'sourceWidth':w,'sourceHeight':h}
  if v['mode']=='video'and port:
   if duration<(port['frameCount']-1)/port['fps']-1/60:raise ValueError(role+' video is shorter than its required frame sequence')
   if port['kind']in['gallery','process']and v.get('cycle')!='explicit-allow':raise ValueError(role+' native carrier may cycle frames; supply an image or explicitly permit this illustrative cycle')
  if v['mode']=='image'and p.suffix.lower()not in['.png','.jpg','.jpeg','.webp']:raise ValueError('Still media must be PNG/JPEG/WebP')
  if role=='banner':
   focus=v.get('focus',{});highlights=focus.get('highlights',[])
   if not all(isinstance(focus.get(k),(float,int))and math.isfinite(focus[k])and 0<=focus[k]<=1 for k in['cx','cy'])or not 1<=len(highlights)<=5:raise ValueError('needs-binding: recording focus and 1–5 highlight rectangles')
   for box in highlights:
    if not all(isinstance(box.get(k),(float,int))and math.isfinite(box[k])and 0<=box[k]<=1 for k in['x','y','w','h'])or box['w']<=0 or box['h']<=0 or box['x']+box['w']>1 or box['y']+box['h']>1:raise ValueError('Invalid original-frame highlight rectangle')
  assets[role]=(p,v,port);consumed.append({'role':role,'sha256':sha(p),'path':str(p),'dimensions':[w,h],'duration':duration})
 presenter=media.get('presenter',{})
 if presenter.get('mode')=='none':pass
 else:
  bind('presenter',presenter)
  if presenter['mode']=='video'and spec(assets['presenter'][0])[2]<cursor-1/60:raise ValueError('Presenter video must cover the output clock continuously')
  face=presenter.get('face',{});tracking=presenter.get('tracking',[])
  if not all(isinstance(face.get(k),(float,int))and math.isfinite(face[k])and 0<face[k]<=1 for k in['cx','cy','h']):raise ValueError('needs-binding: face geometry in the original visual frame')
  for row in tracking:
   if not 0<=row.get('time',-1)<=cursor or not all(isinstance(row.get(k),(float,int))and 0<row[k]<=1 for k in['cx','cy','h']):raise ValueError('Invalid original-frame face tracking')
  if tracking!=sorted(tracking,key=lambda r:r['time']):raise ValueError('Tracking must be in output-time order')
 for role in roles:
  if role in['wall','feedback']:
   n=62 if role=='wall'else 10;arr=media.get(role)
   if not isinstance(arr,list)or len(arr)!=n:raise ValueError(f'needs-binding: {role} requires exactly {n} explicit entries for this native group')
   for i,v in enumerate(arr):bind(role+'/'+str(i),v,{'kind':'gallery','fps':12,'frameCount':30}if role=='wall'else None)
  else:
   port=ports.get(role);bind(role,media.get(role),port)
 for role in['voice','music']:
  v=media.get(role)
  if not isinstance(v,dict)or v.get('mode')not in['none','file']:raise ValueError('needs-binding: explicit '+role+' none/file')
  if v['mode']=='file':
   p=media_path(root,v.get('file'));metadata=probe(p)
   if not any(s['codec_type']=='audio'for s in metadata['streams'])or float(metadata['format'].get('duration',0))<cursor-1/60:raise ValueError(role+' must be a full output-clock audio track')
   if role=='music'and not v.get('license'):raise ValueError('Music source/license must be explicit')
   assets[role]=(p,v,None);consumed.append({'role':role,'sha256':sha(p),'path':str(p)})
 if d.get('soundEffects')not in['native','none']:raise ValueError('Choose native sound effects or explicit none')
 if 'markWindows'in d:
  windows=d['markWindows']
  if cursor>=7 and not windows:raise ValueError('A signature window is required for this duration')
  for i,w in enumerate(windows):
   if not all(math.isfinite(w[k])for k in['start','end'])or not 0<=w['start']<w['end']<=cursor-.5+1e-6 or abs(w['end']-w['start']-5.5)>1/60 or i and windows[i-1]['end']>w['start']:raise ValueError('Invalid circular signature window')
 for c in d.get('captions',[]):
  if not isinstance(c.get('text'),str)or not 0<=c['start']<c['end']<=cursor:raise ValueError('Invalid caption cue')
  if c.get('units'):
   if ''.join(u['text']for u in c['units'])!=c['text']:raise ValueError('Measured caption units must reconstruct the text')
   for u in c['units']:
    if not c['start']<=u['start']<u['end']<=c['end']:raise ValueError('Measured word interval outside its caption')
  if len(c.get('breakAfter',[]))>1:raise ValueError('Explicit captions support one or two lines')
 return {'profile':'kinetic-user-plan/1','inputSHA256':sha(source),'candidateContentDigest':digest(),'platformManifestDigest':'not yet established by official packer','layout':'landscape','language':d['language'],'duration_s':cursor,'frames':round(cursor*60),'width':1920,'height':1080,'fps':60,'spans':spans,'activeUnits':sorted(active),'requiredFields':sorted(required),'mediaRoles':sorted(roles),'inputs':consumed,'coverageComplete':False},d,assets
def prepare(input_file,out):
 report,d,assets=plan(input_file)
 if out.exists()or out.resolve().is_relative_to(ROOT):raise ValueError('Preserve existing directories and keep the core read-only')
 shutil.copytree(CORE,out);(out/'user-assets').mkdir();bound={};reports=[]
 for role,(p,v,port)in assets.items():
  key=role.replace('/','-');dest=out/'user-assets'/key
  if role in['voice','music']:
   dest=dest.with_suffix(p.suffix.lower());shutil.copy2(p,dest);bound[role]={**v,'file':str(dest.relative_to(out))};continue
  if role=='presenter':
   w,h=v['sourceWidth'],v['sourceHeight'];scale=max(720/w,1280/h);dx=(w*scale-720)/2;dy=(h*scale-1280)/2
   def crop(face):return{'cx':(face['cx']*w*scale-dx)/720,'cy':(face['cy']*h*scale-dy)/1280,'h':face['h']*h*scale/1280}
   face=crop(v['face']);tracking=[{'time':a['time'],**crop(a)}for a in v.get('tracking',[])]
   if not all(0<x<1 for x in face.values()):raise ValueError('Face falls outside the prepared crop; choose a fitting original frame')
   port={'fps':60,'frameCount':report['frames']};filt='scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280';geometry={'face':face,'tracking':tracking}
  elif role=='banner':
   w,h=v['sourceWidth'],v['sourceHeight'];scale=min(1600/w,1028/h);dx=(1600-w*scale)/2;dy=(1028-h*scale)/2;f=v['focus'];geometry={'focus':{'cx':(f['cx']*w*scale+dx)/1600,'cy':(f['cy']*h*scale+dy)/1028,'highlights':[{'x':(b['x']*w*scale+dx)/1600,'y':(b['y']*h*scale+dy)/1028,'w':b['w']*w*scale/1600,'h':b['h']*h*scale/1028}for b in f['highlights']]}};filt='scale=1600:1028:force_original_aspect_ratio=decrease,pad=1600:1028:(ow-iw)/2:(oh-ih)/2'
  else:filt='scale=1280:1280:force_original_aspect_ratio=decrease';geometry={}
  if v['mode']=='image':
   dest=dest.with_suffix('.png');subprocess.run(['ffmpeg','-v','error','-n','-i',str(p),'-vf',filt,'-frames:v','1',str(dest)],check=True);b={'mode':'image','file':str(dest.relative_to(out)),**geometry}
  else:
   dest.mkdir();subprocess.run(['ffmpeg','-v','error','-n','-i',str(p),'-vf',f"fps={port['fps']},"+filt,'-frames:v',str(port['frameCount']),'-start_number','0','-q:v','2',str(dest/'%05d.jpg')],check=True)
   actual=len(list(dest.glob('*.jpg')))
   if actual!=port['frameCount']:raise ValueError('Prepared video sequence is incomplete: '+role)
   b={'mode':'video','directory':str(dest.relative_to(out)),'frames':actual,'fps':port['fps'],**geometry}
  bound[role]=b;reports.append({'role':role,'inputSHA256':sha(p),'prepared':b,'originalDimensions':[v['sourceWidth'],v['sourceHeight']]})
 media={k:v for k,v in bound.items()if'/'not in k}
 for role in['wall','feedback']:
  if role in report['mediaRoles']:media[role]=[bound[role+'/'+str(i)]for i in range(62 if role=='wall'else 10)]
 for role in['voice','music']:media.setdefault(role,{'mode':'none'})
 (out/'user-assets/blank.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="720" height="1280"/>',encoding='utf-8')
 content={f['id']:d.get('content',{}).get(f['id'],'')for f in read(CORE/'content.schema.json')['fields']}
 captions=[]
 for c in d.get('captions',[]):
  c=json.loads(json.dumps(c));c['text']=re.sub(r'[,，.。]+\s*$','',c['text'])
  if c.get('units'):c['units'][-1]['text']=re.sub(r'[,，.。]+\s*$','',c['units'][-1]['text'])
  captions.append(c)
 markWindows=[];at=8 if report['duration_s']>=14 else max(0,report['duration_s']-6)
 while report['duration_s']>=7 and at+5.5<=report['duration_s']-.5+1e-6:markWindows.append({'start':at,'end':at+5.5});at+=30
 if 'markWindows'in d:markWindows=d['markWindows']
 settings={'selected':report['activeUnits'],'content':content,'basic':d.get('basic',{}),'titles':{g['id']:next((p['title']for p in report['spans']if p['id']==g['id']),d['title'])for g in read(CORE/'catalog.json')['groups']},'title':d['title'],'presenterLabel':d['presenterLabel'],'presenter':media.get('presenter',{'mode':'none'}),'media':media,'plan':report['spans'],'duration':report['duration_s'],'language':d['language'],'layout':'landscape','captions':captions,'markWindows':markWindows,'blank':'user-assets/blank.svg','soundEffects':d['soundEffects']}
 save(out/'settings.json',settings);(out/'user-input.js').write_text('window.KINETIC_INPUT='+json.dumps(settings,ensure_ascii=False)+';\n',encoding='utf-8');(out/'config.js').write_text('window.CONFIG='+json.dumps({'brand':'MotionGit','account':d['presenterLabel'],'demo':False,'fps':60,'width':1920,'height':1080,'end':223.85,'subtitles':False,'race':{'labels':['a','b'],'keys':[0,223.85]}})+';\n',encoding='utf-8')
 save(out/'user-plan.json',report);save(out/'binding-report.json',{'inputSHA256':report['inputSHA256'],'candidateContentDigest':report['candidateContentDigest'],'boundFiles':{n:sha(out/n)for n in['settings.json','user-input.js','config.js']},'media':reports,'credentialsIncluded':False});return report
def main():
 p=argparse.ArgumentParser();p.add_argument('command',choices=['plan','prepare','preview','events','render']);p.add_argument('--input',type=Path);p.add_argument('--instance',type=Path);p.add_argument('--out',type=Path);p.add_argument('--time',type=float,default=1);a=p.parse_args()
 if a.command in['plan','prepare']:
  if not a.input or(a.command=='prepare'and not a.out):raise ValueError('Input and preparation output are required')
  if a.out and a.out.exists():raise ValueError('Preserve previous plans/instances; choose a new output')
  r=prepare(a.input,a.out)if a.command=='prepare'else plan(a.input)[0]
  if a.command=='plan'and a.out:save(a.out,r)
  print(json.dumps(r,ensure_ascii=False));return
 if not a.instance or not a.out or a.out.exists():raise ValueError('Choose an existing instance and a new output path')
 b=read(a.instance/'binding-report.json')
 if b['candidateContentDigest']!=digest():raise ValueError('Candidate identity changed; derive a new instance')
 if any(sha(a.instance/n)!=v for n,v in b['boundFiles'].items()):raise ValueError('Prepared binding changed; derive a new instance')
 cmd=['node',str(ROOT/'render.mjs'),'--root',str(a.instance),'--out',str(a.out)]
 if a.command=='preview':cmd+=['--preview','--time',str(a.time)]
 if a.command=='events':cmd+=['--events']
 subprocess.run(cmd,check=True)
 if a.command=='render':subprocess.run([sys.executable,str(ROOT/'mix.py'),'--instance',str(a.instance),'--silent-video',str(a.out)],check=True)
if __name__=='__main__':main()
