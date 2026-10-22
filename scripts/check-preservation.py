#!/usr/bin/env python3
"""Conservative preservation gate; does not judge technical meaning or duplicate HMY schema."""
import argparse, collections, json, re, sys
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
def protected(text):
    return collections.Counter(re.findall(r'!?\[\[[^\]]+\]\]|!?\[[^\]\n]*\]\([^\n)]*\)|^\[\^[^\]]+\]:[^\n]*|\[\^[^\]]+\](?!:)', text, re.M))
def check(before,after,mode='deep',old=None,new=None):
    errors=[]
    if (old is None) != (new is None): errors.append('Provide both allowed-old and allowed-new')
    if mode=='light' and before!=after and (old is None or new is None):
        errors.append('Light Edit changes require a declared replacement')
    front=lambda s: (re.match(r'\A---\r?\n[\s\S]*?\r?\n---(?:\r?\n|$)',s) or [''])[0]
    if front(before)!=front(after): errors.append('Frontmatter changed; inspect explicitly')
    lost=protected(before)-protected(after)
    if lost: errors.append('Lost or changed reference: '+json.dumps(dict(lost),ensure_ascii=False))
    # A zero-change result is valid for deliberately preserved text.
    if mode=='light':
        headings=lambda s:re.findall(r'^#{1,6}\s+.*$',s,re.M)
        if headings(before)!=headings(after): errors.append('Light Edit changed headings')
        fences=lambda s:re.findall(r'^\x60{3,}[^\n]*\n[\s\S]*?^\x60{3,}\s*$',s,re.M)
        if fences(before)!=fences(after): errors.append('Light Edit changed fenced blocks')
    if old is not None:
        if new is None or before.count(old)!=1 or after!=before.replace(old,new,1):
            errors.append('Changed outside the declared replacement')
    return {'status':'Failed' if errors else 'Passed','errors':errors,'limits':'Text preservation only; meaning, destination validity and rendering need separate checks.'}
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('before',type=Path);p.add_argument('after',type=Path)
    p.add_argument('--mode',choices=['light','deep'],default='deep')
    p.add_argument('--allowed-old');p.add_argument('--allowed-new')
    a=p.parse_args()
    result=check(a.before.read_text(encoding='utf-8'),a.after.read_text(encoding='utf-8'),a.mode,a.allowed_old,a.allowed_new)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return result['status']!='Passed'
if __name__=='__main__':
    sys.exit(main())
