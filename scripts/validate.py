#!/usr/bin/env python3
"""Offline structure checks; native HMY syntax is delegated to verify-hmy.mts."""
import json, re, sys, unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
SKIP={'.git','.local','__pycache__','node_modules','HANDOFF.md'}
ERRORS=[]
def fail(s): ERRORS.append(s)
def walk(d):
    for p in d.iterdir():
        if p.name in SKIP: continue
        if p.is_symlink(): fail('Symlink: '+str(p.relative_to(ROOT)))
        elif p.is_dir(): yield from walk(p)
        else: yield p
def prose(text,label):
    out,fence=[],None
    for line in text.splitlines():
        m=re.match(r'^\s{0,3}(\x60{3,}|~{3,})(.*)$',line)
        if m:
            mark,tail=m.groups()
            if fence is None: fence=mark; continue
            if mark[0]==fence[0] and len(mark)>=len(fence) and not tail.strip(): fence=None; continue
        if fence is None: out.append(line)
    if fence: fail('Unclosed fence: '+label)
    return '\n'.join(out)
def anchors(text):
    result,counts=set(),{}
    for h in re.findall(r'^#{1,6}\s+(.+?)\s*#*$',text,re.M):
        h=re.sub(r'<[^>]+>','',h).lower()
        slug=''.join(c for c in h if c in '-_ ' or unicodedata.category(c)[0] not in 'PS').replace(' ','-')
        i=counts.get(slug,0); counts[slug]=i+1
        result.add(slug+(f'-{i}' if i else ''))
    return result
def fm(t):
    m=re.match(r'\A---\n(.*?)\n---(?:\n|$)',t,re.S)
    return m[1] if m else None
def refs(t): return set(re.findall(r'!?\[\[[^\]]+\]\]|\]\([^)]+\)|\[\^[^\]]+\](?::[^\n]*)?',t))
def links(text,p,label):
    for target in re.findall(r'\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)',text):
        target=target.strip('<>')
        if re.match(r'[a-z][a-z0-9+.-]*:',target,re.I): continue
        raw,_,frag=target.partition('#')
        dest=(p.parent/unquote(raw)).resolve() if raw else p
        if not dest.is_relative_to(ROOT) or not dest.is_file(): fail(f'Broken relative link: {label} -> {target}')
        elif frag and dest.suffix=='.md' and unquote(frag) not in anchors(prose(dest.read_text(encoding='utf-8'),str(dest))):
            fail(f'Broken anchor: {label} -> {target}')
def main():
    manifest=json.loads((ROOT/'scripts/package-files.json').read_text(encoding='utf-8'))
    if len(manifest)!=len(set(manifest)): fail('Duplicate manifest path')
    actual={p.relative_to(ROOT).as_posix() for p in walk(ROOT)}
    expected=set(manifest)
    for p in sorted(expected-actual): fail('Missing package file: '+p)
    for p in sorted(actual-expected): fail('Unreviewed package file: '+p)
    texts={}
    for rel in sorted(actual & expected):
        p=ROOT/rel
        text=p.read_text(encoding='utf-8'); texts[rel]=text
        for label,pattern in {
            'absolute-local-path':r'\b[A-Za-z]:[\\/]|/(?:Users|home)/[A-Za-z0-9_-]+/',
            'credential':r'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{35,}|sk-[A-Za-z0-9]{30,})',
            'private-key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'
        }.items():
            if re.search(pattern,text): fail(label+': '+rel+' (inspect locally)')
        if p.suffix=='.md':
            cleaned=prose(text,rel)
            if not rel.startswith('examples/fixtures/before/'): links(cleaned,p,rel)
            if re.search(r'Internal Wiki|Confluence|Outline|ERP|접수 SOP',cleaned): fail('Removed audience material: '+rel)
        if p.suffix=='.json': json.loads(text)
    skill=texts.get('SKILL.md','')
    front=fm(skill)
    if front is None: fail('Missing skill frontmatter')
    else:
        fields=dict(re.findall(r'^(name|description|license): (.+)$',front,re.M))
        if fields.get('name')!='hmy-wiki-writing': fail('Wrong skill name')
        if not 1<=len(fields.get('description',''))<=1024: fail('Description length')
        if fields.get('license')!='MIT': fail('Missing MIT metadata')
    if len(skill.splitlines())>500: fail('Entrypoint too large')
    version=texts.get('VERSION','').strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+',version): fail('Invalid version')
    for p in ['README.md','CHANGELOG.md']:
        if version not in texts.get(p,''): fail('Version missing: '+p)
    if 'npx skills add HoMongYi/hmy-wiki-writing' not in texts.get('README.md',''): fail('Missing install command')
    if '$hmy-wiki-writing' not in texts.get('agents/openai.yaml',''): fail('Missing invocation prompt')
    vault=ROOT/'examples/fixtures/vault'
    docs={p.stem:p for p in vault.rglob('*.md')}
    if len(docs)!=len(list(vault.rglob('*.md'))): fail('Ambiguous fixture name')
    for p in docs.values():
        body=prose(p.read_text(encoding='utf-8'),p.name)
        for raw in re.findall(r'(?<!!)\[\[([^\]]+)\]\]',body):
            name,_,heading=raw.split('|')[0].partition('#')
            dest=docs.get(name) if name else p
            if dest is None: fail('Missing fixture Wikilink: '+raw)
            elif heading and not re.search(r'^#{1,6}\s+'+re.escape(heading)+r'\s*$',dest.read_text(encoding='utf-8'),re.M):
                fail('Missing fixture heading: '+raw)
        defs=set(re.findall(r'^\[\^([^\]]+)\]:',body,re.M))
        uses=set(re.findall(r'\[\^([^\]]+)\](?!:)',body))
        if defs!=uses: fail('Unpaired footnote: '+p.name)
        if re.search(r'^#{1,6}\s+(출처|Sources?|검토 필요)\s*$',body,re.M): fail('Public fixture heading: '+p.name)
    for name in ['NVMe.md','M.2 점검.md']:
        before=(ROOT/'examples/fixtures/before'/name).read_text(encoding='utf-8')
        after=(vault/'01_하드웨어'/name).read_text(encoding='utf-8')
        if fm(before)!=fm(after): fail('Frontmatter changed: '+name)
        if not refs(before)<=refs(after): fail('Lost reference: '+name)
    before=(ROOT/'examples/fixtures/before/M.2 점검.md').read_text(encoding='utf-8')
    after=(vault/'01_하드웨어/M.2 점검.md').read_text(encoding='utf-8')
    old='연결 방식의 확인을 위해서는 메인보드 매뉴얼에서 해당 슬롯의 사양을 조회하는 것이 필요하다.'
    new='연결 방식을 확인하려면 메인보드 매뉴얼에서 해당 슬롯의 사양을 살펴본다.'
    if before.count(old)!=1 or after!=before.replace(old,new): fail('Light Edit changed outside permitted sentence')
    for asset in vault.rglob('*.svg'):
        svg=ET.fromstring(asset.read_text(encoding='utf-8'))
        for n in svg.iter():
            if n.tag.rsplit('}',1)[-1] not in {'svg','title','desc','rect','g','path','text'}: fail('Unexpected SVG element: '+asset.name)
            if any(k.lower().startswith('on') or k.rsplit('}',1)[-1]=='href' for k in n.attrib): fail('Active/external SVG: '+asset.name)
    cases=json.loads(texts.get('evals/inputs.json','[]'))
    if {c['id'] for c in cases}!={f'H{i:02}' for i in range(1,13)}: fail('Incomplete behavior inputs')
    coverage=json.loads(texts.get('evals/coverage.json','{}'))
    if set(coverage)!={str(i) for i in range(1,21)}: fail('Incomplete 20-behavior coverage')
    print(json.dumps({'status':'Failed' if ERRORS else 'Passed','files':len(actual),'errors':ERRORS,
      'limits':'Offline structure only; native HMY syntax, factual accuracy and app rendering are separate.'},ensure_ascii=False,indent=2))
if __name__=='__main__':
    try: main()
    except (OSError,ValueError,KeyError,ET.ParseError) as e:
        fail(type(e).__name__+': '+str(e))
        print(json.dumps({'status':'Failed','errors':ERRORS},ensure_ascii=False,indent=2))
    sys.exit(bool(ERRORS))
