"""Verified, model-specific Anima content. Private generation state is never exported."""
from __future__ import annotations
import copy
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile
from PIL import Image

MODEL='anima-turbo'
REPOSITORY='akiba-tokyo-jp/manga-style'
CATEGORIES={'shonen','shojo','seinen','josei','kodomo','yonkoma','gag','horror','essay','gekiga','other'}
EXTRA_CATEGORIES={'other':{'ja':'その他・成人向け参考','en':'Other / adult-manga references'}}
FACETS={'expression':{'mono','color'},'line':{'thin','thick','rough'},'proportion':{'chibi','standard','realistic'},'finish':{'solid','tone','lineonly'}}
ID=re.compile(r'anima-[a-z0-9]+(?:-[a-z0-9]+)*\Z')
SHA=re.compile(r'[0-9a-f]{64}\Z')


def require(condition,message):
    if not condition:raise ValueError(message)


def read_manifest(path):
    value=json.loads(Path(path).read_text(encoding='utf-8'))
    require(isinstance(value,dict) and value.get('schema')==1 and value.get('repository')==REPOSITORY,'Invalid Anima manifest')
    require(isinstance(value.get('bundles'),list) and isinstance(value.get('entries'),list),'Invalid Anima lists')
    return value


def load_catalog(path,archive_dir):
    manifest=read_manifest(path)
    members={}
    for bundle in manifest['bundles']:
        name=bundle.get('asset','')
        require(isinstance(name,str) and re.fullmatch(r'[a-z0-9][a-z0-9.-]*\.zip',name),'Unsafe Anima archive')
        require(isinstance(bundle.get('sha256'),str) and SHA.fullmatch(bundle['sha256']),'Invalid archive SHA')
        archive=Path(archive_dir)/name
        require(not archive.is_symlink() and archive.stat().st_size<=64*1024*1024,'Unsafe Anima archive file')
        raw=archive.read_bytes()
        require(hashlib.sha256(raw).hexdigest()==bundle['sha256'],'Anima archive SHA mismatch')
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            require(sum(i.file_size for i in z.infolist())<=128*1024*1024,'Anima archive expands too far')
            for info in z.infolist():
                require(re.fullmatch(r'anima-[a-z0-9]+(?:-[a-z0-9]+)*/[0-9a-f]{64}\.(?:png|jpg)',info.filename) and info.filename not in members,'Unsafe or duplicate Anima member')
                require(info.file_size<=25*1024*1024 and (info.external_attr>>16)&0o170000!=0o120000,'Unsafe Anima member type/size')
                members[info.filename]=z.read(info)
    rows=[];seen=set();used=set()
    for source in manifest['entries']:
        require(isinstance(source,dict),'Invalid Anima entry')
        entry=copy.deepcopy(source);sid=entry.get('id','')
        require(isinstance(sid,str) and ID.fullmatch(sid) and sid not in seen,'Invalid or duplicate Anima id');seen.add(sid)
        require(entry.get('category') in CATEGORIES,'Unknown Anima category')
        if entry['category']=='other':
            require(entry.get('reference_context')=='adult-manga' and entry.get('sample_content')=='non-explicit-fully-clothed-adult','Other entries require explicit adult-reference/nonsexual-sample classification')
        require(entry.get('model_version')=='anima-turbo-v1.1','Unverified Anima model')
        for field in ('title','summary','limitations'):
            require(isinstance(entry.get(field),dict) and all(isinstance(entry[field].get(lang),str) and entry[field][lang] for lang in ('ja','en')),'Missing bilingual Anima description')
        from urllib.parse import urlsplit
        references=entry.get('references',[])
        require(isinstance(references,list),'Invalid Anima reference list')
        for reference in references:
            require(isinstance(reference,dict) and isinstance(reference.get('title'),str) and isinstance(reference.get('url'),str),'Invalid Anima reference')
            url=urlsplit(reference['url'])
            require(url.scheme=='https' and url.hostname and not url.username and not url.password,'Unsafe Anima reference URL')
        for prompt in (entry.get('prompt'),entry.get('sample',{}).get('prompt')):
            require(isinstance(prompt,dict) and set(prompt)=={'en'} and isinstance(prompt['en'],str) and prompt['en'].strip(),'Anima requires exact English-only prompts')
        require(isinstance(entry.get('features'),dict) and set(entry['features'])==set(FACETS),'Invalid Anima facets')
        for key,values in entry['features'].items():
            require(isinstance(values,list) and all(v in FACETS[key] for v in values),'Unknown Anima facet value')
        sample=entry['sample'];reported=sample.get('reported_settings',{});requested=sample.get('requested_settings',{})
        require(reported.get('model')==entry['model_version'] and requested.get('model')==entry['model_version'] and reported.get('provider')=='ps5-anima','Anima provenance model mismatch')
        require(isinstance(sample.get('native_job_id'),str) and re.fullmatch(r'[0-9a-f]{32}',sample['native_job_id']) and reported.get('native_job_id')==sample['native_job_id'],'Missing native generation job')
        for file_key,sha_key,kind in (('file','sha256','PNG'),('thumb','thumb_sha256','JPEG')):
            digest=sample.get(sha_key,'');name=sample.get(file_key,'');ext='.png' if kind=='PNG' else '.jpg'
            require(isinstance(digest,str) and SHA.fullmatch(digest) and name==digest+ext,'Unsafe or unpinned Anima image')
            member=sid+'/'+name;require(member in members,'Missing Anima image');used.add(member)
            data=members[member];require(hashlib.sha256(data).hexdigest()==digest,'Anima image SHA mismatch')
            try:
                with Image.open(io.BytesIO(data)) as image:
                    expected=(sample.get('width'),sample.get('height')) if kind=='PNG' else (384,512)
                    require(image.format==kind and image.size==expected,'Unexpected Anima image format/size')
                    image.verify()
            except (OSError,SyntaxError) as exc:raise ValueError('Invalid Anima image') from exc
            entry['image_bytes' if kind=='PNG' else 'thumb_bytes']=data
        rows.append(entry)
    require(set(members)==used,'Unreferenced Anima assets are not publishable')
    return rows


def add_to_export(stage,rows,store,main,write,image_records):
    """Add independent Anima projections inside the exporter's atomic staging tree."""
    if not rows:return
    from urllib.parse import quote
    from app.catalogue import FACETS as UI_FACETS,MODELS,TEXT,model_url
    from app.ui import UI
    stage=Path(stage)
    index=json.loads((stage/'_public/catalogue.json').read_text(encoding='utf-8'))
    routes=json.loads((stage/'_data/routes.json').read_text(encoding='utf-8'))
    require(not any(row['id'] in routes['visible'] for row in rows),'Anima/GPT identifier collision')
    old_visible=list(routes['visible'])
    anima_roots=list(routes['roots'])
    anima_roots.extend(sid for sid in EXTRA_CATEGORIES if any(row['category']==sid for row in rows))
    routes['model_roots']={'gpt-image':list(routes['roots']),MODEL:anima_roots}
    index['model_roots']=copy.deepcopy(routes['model_roots'])
    index['category_labels']={MODEL:{sid:EXTRA_CATEGORIES[sid] for sid in anima_roots if sid in EXTRA_CATEGORIES}}
    def category_title(sid,lang):return EXTRA_CATEGORIES[sid][lang] if sid in EXTRA_CATEGORIES else store.title(sid,lang)
    def image_url(row,key):return main.SITE_ORIGIN+'/files/'+MODEL+'/'+row['id']+'/'+row['sample'][key]
    def context(lang,path,title):
        other='en' if lang=='ja' else 'ja'
        ctx=main.base_ctx(lang,False,model_url(path,other,False,MODEL),title,[])
        ctx.update(newui=TEXT[lang],active_model=MODEL,model_info={**MODELS[MODEL],'status':'available'},
                   home_url=model_url('/',lang,False,MODEL),search_url=model_url('/search',lang,False,MODEL),
                   api_guide_url=model_url('/api',lang,False,MODEL),
                   model_tabs=[{**model,'active':model['id']==MODEL,'url':model_url('/search',lang,False,model['id'])} for model in MODELS.values()])
        return ctx
    for row in rows:
        sid=row['id'];sample=row['sample'];root=row['category']
        require(root in anima_roots,'Anima category is not publicly visible')
        for key,body in (('file',row['image_bytes']),('thumb',row['thumb_bytes'])):
            path='files/'+MODEL+'/'+sid+'/'+sample[key]
            target=stage/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(body)
            image_records['/'+path]={'sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body)}
        payloads={};pages={};labels={}
        for lang in UI:
            title=row['title'][lang];summary=row['summary'][lang]
            payload={'id':sid,'path':[],'level':1,'category':root,'title':title,'summary':summary,
                     'expression':row['features']['expression'][0],
                     'model':{'id':MODEL,'version':row['model_version']},'prompt':row['prompt'],'avoid':[],
                     'samples':[{'subject':'example','url':image_url(row,'file'),'prompt':sample['prompt'],
                                 'settings':sample['requested_settings'],'reported_settings':sample['reported_settings'],
                                 'sha256':sample['sha256'],'native_job_id':sample['native_job_id']}],
                     'reference':0,'children':[],'comparisons':[],'version':row.get('version',1),'updated_at':row.get('updated_at'),
                     'license':{'generated':True,'artist_names':False,'terms':main.LICENSE_TERMS},
                     'limitations':row['limitations'][lang],'references':row.get('references',[])}
            payloads[lang]=payload
            if root=='other':payload.update(reference_context=row['reference_context'],sample_content=row['sample_content'])
            ctx=context(lang,'/styles/'+sid,title)
            ctx.update(entry=row,title=title,summary=summary,limitation=row['limitations'][lang],
                       image_url=image_url(row,'file'),sample=sample,style_text=row['prompt']['en'],
                       full_prompt=sample['prompt']['en'],api_url=main.SITE_ORIGIN+'/v1/styles/'+sid+'?model='+MODEL,
                       copy_prefix='Anima Turbo / '+category_title(root,lang)+' / '+sid,
                       category_notice=(('成人向け漫画の描法を参考にした別枠です。見本は成人の着衣・非露骨な表現です。' if lang=='ja' else 'A separate adult-manga drawing-reference category. Samples show fully clothed adults in non-explicit scenes.') if root=='other' else None))
            rendered=main.env.get_template('anima_style.html').render(**ctx)
            pages[lang]={MODEL:{'en':rendered,'ja':rendered}}
            labels[lang]={'id':sid,'level':3,'title':title,'summary':summary,'path':category_title(root,lang),
                          'model_name':'Anima Turbo','thumb_url':'/files/'+MODEL+'/'+sid+'/'+sample['thumb'],
                          'url':model_url('/styles/'+sid,lang,False,MODEL),
                          'hay':' '.join([sid,*row['title'].values(),*row['summary'].values(),row['prompt']['en']]).casefold()}
        write('_data/styles/'+MODEL+'/'+sid+'.json',payloads)
        write('_data/pages/'+sid+'.json',pages)
        index['records'].append({'id':sid,'model':MODEL,'level':3,'chain':[root,sid],'look_group':False,'features':row['features'],'labels':labels})
    write('_public/catalogue.json',index)
    routes['visible']+= [r['id'] for r in rows]
    routes['model_visible']={'gpt-image':old_visible,MODEL:[r['id'] for r in rows]}
    routes['health']['anima_styles']=len(rows)
    routes['empty']={'ja':'<section class="model-empty"><h2>この絵柄の Anima 見本は未登録です</h2></section>',
                     'en':'<section class="model-empty"><h2>No Anima example is registered for this style.</h2></section>'}
    write('_data/routes.json',routes)
    models=json.loads((stage/'_data/models.json').read_text(encoding='utf-8'))
    for model in models['models']:
        if model['id']==MODEL:model.update(status='available',style_count=len(rows))
    write('_data/models.json',models)
    for lang in UI:
        tree={'version':1,'model':{'id':MODEL,'name':'Anima Turbo','status':'available'},'nodes':[
            {'id':r['id'],'parent':None,'level':1,'category':r['category'],'title':r['title'][lang],
             'summary':r['summary'][lang],'thumbnail_url':image_url(r,'thumb'),'path':[r['title'][lang]]} for r in rows]}
        write('_data/tree/'+lang+'-'+MODEL+'.json',tree)
        ctx=context(lang,'/search',TEXT[lang]['heading'])
        roots=[{'id':sid,'title':category_title(sid,lang),'url':model_url('/n/'+sid,lang,False,MODEL)} for sid in anima_roots]
        selected={k:'' for k in ('root','topic','q',*UI_FACETS)}
        cards=[record['labels'][lang] for record in index['records'] if record.get('model')==MODEL]
        ctx.update(gallery_title=TEXT[lang]['heading'],registered_count=len(rows),model_ready=True,q='',selected=selected,
                   roots=roots,topics=[],cards=cards,total=len(rows),page=1,pages=1,previous_url=None,next_url=None,
                   clear_url=model_url('/search',lang,False,MODEL),topic_basic_url=None,category_basic_genko=None,
                   facet_options={k:[{'value':v,'label':ja if lang=='ja' else en} for v,ja,en in options] for k,options in UI_FACETS.items()})
        gallery=main.env.get_template('gallery.html').render(**ctx)
        gallery=gallery.replace('</head>','<script type="module" src="/static/gallery.mjs"></script></head>')
        write('_data/gallery/'+lang+'-'+MODEL+'.html',gallery)
        guide_ctx=context(lang,'/api','Anima Turbo API')
        guide_ctx['example_id']=rows[0]['id']
        write('_data/guide/'+lang+'-'+MODEL+'.html',main.env.get_template('anima_api.html').render(**guide_ctx))
