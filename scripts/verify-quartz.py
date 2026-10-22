#!/usr/bin/env python3
# Exercise the independent fixtures in a built Quartz site. Requires optional Python Playwright.
import argparse
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
from threading import Thread
from urllib.parse import quote, urlsplit

@contextmanager
def serve(public):
    class Handler(SimpleHTTPRequestHandler):
        def log_message(self, *_): pass
        def do_GET(self):
            target=Path(self.translate_path(self.path))
            if not target.exists() and Path(str(target)+'.html').is_file():
                parts=urlsplit(self.path)
                self.path=parts.path+'.html'+('?' + parts.query if parts.query else '')
            super().do_GET()
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(public)))
    thread=Thread(target=server.serve_forever,daemon=True);thread.start()
    try: yield 'http://127.0.0.1:'+str(server.server_address[1])
    finally:server.shutdown();server.server_close();thread.join()

def required_pages(public, index, fixtures):
    titles=[]
    for document in sorted(fixtures.rglob('*.md')):
        match=re.search(r'^title:\s*(.+)$',document.read_text(encoding='utf-8'),re.M)
        if not match: raise ValueError('Fixture title missing: '+document.name)
        titles.append(match[1].strip().strip("'\""))
    if not titles: raise ValueError('No source fixtures found')
    titles.append('블록 표본')
    if len(titles)!=len(set(titles)): raise ValueError('Duplicate source fixture title')
    pages={}
    for title in titles:
        matches=[slug for slug,value in index.items() if value.get('title')==title]
        if len(matches)!=1: raise ValueError('Expected one index record for fixture: '+title)
        target=(public/(matches[0]+'.html')).resolve()
        if not target.is_relative_to(public.resolve()) or not target.is_file():
            raise FileNotFoundError('Missing rendered fixture: '+title)
        pages[title]=matches[0]
    return pages

def main():
    parser=argparse.ArgumentParser(description='Check built fixture pages in Chromium; no schema/parser copy.')
    parser.add_argument('--public-dir',type=Path,required=True)
    parser.add_argument('--report',type=Path)
    parser.add_argument('--screenshots',type=Path)
    args=parser.parse_args();public=args.public_dir.resolve()
    index=json.loads((public/'static/contentIndex.json').read_text(encoding='utf-8'))
    from playwright.sync_api import sync_playwright, expect
    checks=[];errors=[];pages={}
    def check(name,value,detail=None):
        checks.append({'name':name,'status':'Passed' if value else 'Failed',**({'detail':detail} if detail is not None else {})})
        assert value, name+': '+str(detail)
    def report():
        data={'status':'Failed' if errors or any(c['status']=='Failed' for c in checks) else 'Passed','checks':checks,'required_pages':len(pages),'page_errors':errors,'limits':'Chromium fixtures only; actual Obsidian app, other browsers, screen readers and physical touch devices are separate.'}
        if args.report:
            args.report.parent.mkdir(parents=True,exist_ok=True)
            args.report.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'status':data['status'],'checks':len(checks),'page_errors':len(errors)},ensure_ascii=False))
    try:
      pages=required_pages(public,index,Path(__file__).resolve().parents[1]/'examples/fixtures/vault')
      with serve(public) as base, sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        try:
          context=browser.new_context(viewport={'width':1440,'height':1000})
          page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
          def goto(title,pg=page):
              slug=pages[title]
              response=pg.goto(base+'/'+quote(slug,safe='/'),wait_until='networkidle')
              check('HTTP '+title,response.status==200)
              pg.locator('#hmy-main > article').wait_for();return pg.locator('#hmy-main > article')
          for title in pages:
              article=goto(title)
              check('rendered '+title,article.locator('pre[data-language^="hmy-"], pre[class*="language-hmy-"]').count()==0)
              check('images '+title,article.locator('img').evaluate_all('(els)=>els.every(e=>e.complete&&e.naturalWidth>0)'))
          for width in [360,768,1440]:
            for theme in ['light','dark']:
              page.set_viewport_size({'width':width,'height':1000})
              for title in ['메인보드 데이터 경로','CPU 캐시 계층','PCIe 대역폭 비교','DDR CAS 지연시간','SSD 인식 불량','블록 표본']:
                article=goto(title);page.evaluate('t=>document.documentElement.setAttribute("saved-theme",t)',theme)
                check(f'layout {title} {width} {theme}',page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
                check(f'content {title} {width} {theme}',len(article.inner_text())>100)
              check(f'theme {width} {theme}',page.evaluate('document.documentElement.getAttribute("saved-theme")')==theme)
          page.set_viewport_size({'width':1440,'height':1000})
          article=goto('DDR CAS 지연시간');ddr=article.locator('[data-hmy-explorer="ddr-cas"]')
          result=ddr.locator('.hmy-explorer-result');expect(result).to_contain_text('10.00 ns')
          ddr.locator('input[name=dataRate]').fill('5600');ddr.locator('input[name=cl]').fill('40')
          expect(result).to_contain_text('14.29 ns');check('CAS input changes result',True)
          check('CAS baseline remains labelled','6000 MT/s' in ddr.locator('.hmy-explorer-baseline').inner_text())
          for bad in ['', '0', '16001', '5600.5']:
              ddr.locator('input[name=dataRate]').fill(bad)
              expect(result).to_contain_text('계산 결과를 표시할 수 없습니다')
              expect(ddr.locator('input[name=dataRate]')).to_have_attribute('aria-invalid','true')
              check('CAS rejects input '+repr(bad),True)
          ddr.get_by_role('button',name='기준값으로 초기화',exact=True).click()
          expect(result).to_contain_text('10.00 ns');expect(ddr.locator('input[name=cl]')).to_have_value('30');check('CAS reset',True)
          if args.screenshots:
              args.screenshots.mkdir(parents=True,exist_ok=True);ddr.screenshot(path=str(args.screenshots/'ddr-desktop.png'))
          article.get_by_role('link',name='메모리 트레이닝',exact=True).first.click()
          page.wait_for_url(re.compile('memory-training'));page.go_back(wait_until='networkidle')
          expect(page.locator('[data-hmy-explorer] input[name=dataRate]')).to_have_count(1);check('SPA back has one control set',True)
          article=goto('메인보드 데이터 경로');diagram=article.locator('[data-hmy-diagram]')
          diagram.get_by_role('button',name='칩셋',exact=True).click()
          expect(diagram.locator('[data-map-node=chipset]')).to_have_class(re.compile('is-selected'))
          check('diagram related edges',diagram.locator('.hmy-map-edges .is-related').count()==2)
          crossings=diagram.locator('svg').evaluate('''svg=>{let bad=[];for(const edge of svg.querySelectorAll('[data-svg-from]')){const line=edge.querySelector('path');if(!line)continue;const length=line.getTotalLength();for(const node of svg.querySelectorAll('[data-svg-node]')){if([edge.dataset.svgFrom,edge.dataset.svgTo].includes(node.dataset.svgNode))continue;const b=node.querySelector('rect').getBBox();for(let i=1;i<100;i++){const p=line.getPointAtLength(length*i/100);if(p.x>b.x&&p.x<b.x+b.width&&p.y>b.y&&p.y<b.y+b.height){bad.push(node.dataset.svgNode);break;}}}}return bad}''')
          check('diagram avoids unintended intermediate nodes',not crossings,crossings)
          diagram.get_by_role('button',name='전체 연결 보기',exact=True).click();check('diagram reset',diagram.locator('[data-map-node].is-selected').count()==0)
          diagram.get_by_role('button',name='확대 보기',exact=True).focus();page.keyboard.press('Enter')
          expect(page.get_by_role('dialog')).to_be_visible();page.keyboard.press('Escape');expect(page.get_by_role('dialog')).to_have_count(0)
          check('diagram zoom keyboard and focus',page.evaluate('document.activeElement.textContent')=='확대 보기')
          if args.screenshots:diagram.screenshot(path=str(args.screenshots/'paths-desktop.png'))
          article=goto('SSD 인식 불량');flow=article.locator('[data-hmy-diagnosis]')
          flow.get_by_role('button',name='예',exact=True).click();flow.get_by_role('button',name='아니오',exact=True).click();flow.get_by_role('button',name='USB 브리지',exact=True).click()
          expect(flow.locator('[data-node=usb]')).to_be_visible()
          check('diagnosis choices and action','초기화·포맷' in flow.locator('[data-node=usb]').inner_text())
          check('diagnosis moves focus',page.evaluate('document.activeElement.closest("[data-node]")?.dataset.node')=='usb')
          page.emulate_media(media='print');check('selected diagnosis prints every node',flow.locator('[data-node]:visible').count()==9);page.emulate_media(media='screen')
          flow.get_by_role('button',name='이전 단계',exact=True).click();expect(flow.locator('[data-node=enumeration]')).to_be_visible();check('diagnosis previous',True)
          flow.get_by_role('button',name='전체 흐름 보기',exact=True).click();check('diagnosis full flow',flow.locator('[data-node]:visible').count()==9)
          page.emulate_media(media='print');check('diagnosis print actions',flow.locator('[data-node=usb]').is_visible());page.emulate_media(media='screen')
          article=goto('PCIe 대역폭 비교');plot=article.locator('.hmy-plot')
          check('plot values and conditions',all(s in plot.inner_text() for s in ['7.88','15.75','GB/s','편도','실측 아님']))
          article=goto('블록 표본')
          spec=article.locator('.hmy-spec--comparison')
          options=spec.locator('input[type=checkbox]')
          expect(options).to_have_count(3)
          options.nth(2).check();check('comparison differences',spec.locator('.is-different').count()>0)
          options.nth(0).uncheck();check('comparison selects visible groups',spec.locator('.hmy-spec-group:visible').count()==1)
          page.emulate_media(media='print');check('comparison prints all groups',spec.locator('.hmy-spec-group:visible').count()==2);page.emulate_media(media='screen')
          options.nth(0).check();check('comparison restores groups',spec.locator('.hmy-spec-group:visible').count()==2)
          pcie=article.locator('[data-hmy-explorer="pcie-bandwidth"]')
          expect(pcie.locator('.hmy-explorer-result')).to_contain_text('7.88 GB/s')
          pcie.locator('select[name=generation]').select_option('5');pcie.locator('select[name=lanes]').select_option('16')
          expect(pcie.locator('.hmy-explorer-result')).to_contain_text('63.02 GB/s')
          check('PCIe supported inputs',pcie.locator('select[name=generation] option').all_text_contents()==['1.0','2.0','3.0','4.0','5.0'])
          pcie.get_by_role('button',name='기준값으로 초기화',exact=True).click();expect(pcie.locator('.hmy-explorer-result')).to_contain_text('7.88 GB/s');check('PCIe reset',True)
          comparison=article.locator('[data-hmy-compare]');slider=comparison.get_by_role('slider')
          expect(slider).to_have_count(1);slider.focus();slider.press('End');expect(slider).to_have_value('100');slider.press('Home');expect(slider).to_have_value('0');check('image slider keyboard',True)
          comparison.locator('summary').click();check('image credits retained',comparison.inner_text().count('MIT')==2)
          check('signal semantic fallback','실측 파형 아님' in article.locator('.hmy-signal').inner_text() and article.locator('.hmy-signal table').count()==1)
          guide=article.locator('.hmy-guide');guide.get_by_role('button',name='다음 단계',exact=True).click()
          check('guide keeps safety visible',guide.locator('[aria-current=step]').count()==1 and '초기화·포맷' in guide.inner_text())
          nojs=browser.new_context(java_script_enabled=False,viewport={'width':360,'height':900});static=nojs.new_page()
          article=goto('DDR CAS 지연시간',static);check('no-JS CAS data',article.locator('table').count()==1 and '10.00 ns' in article.inner_text() and article.locator('input').count()==0)
          article=goto('SSD 인식 불량',static);check('no-JS complete diagnosis',article.locator('[data-node]:visible').count()==9)
          article=goto('블록 표본',static);check('no-JS image originals',article.locator('[data-hmy-compare] img').count()==2 and article.locator('input[type=range]').count()==0)
          nojs.close();context.close();check('page errors',not errors,errors)
        finally:browser.close()
    except Exception as exc:
        checks.append({'name':'execution','status':'Failed','detail':str(exc)});report();raise
    report()
if __name__=='__main__':main()
