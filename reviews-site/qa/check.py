from pathlib import Path
import os, tempfile, json
from playwright.sync_api import sync_playwright
BASE=Path(__file__).resolve().parents[1]
QA=BASE/'qa'
(QA/'tmp').mkdir(exist_ok=True)
tempfile.tempdir=str(QA/'tmp')
os.environ['TMPDIR']=str(QA/'tmp')
results=[]
def check(label, condition):
 results.append({'check':label,'passed':bool(condition)})
 assert condition,label
with sync_playwright() as p:
 context=p.chromium.launch_persistent_context(str(QA/'tmp'/'browser-profile'),headless=True,downloads_path=str(QA/'tmp'),env={**os.environ,'TMPDIR':str(QA/'tmp')},args=['--disable-crash-reporter'])
 page=context.pages[0]
 errors=[]; external=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('request',lambda r:external.append(r.url) if r.url.startswith(('https://','http://')) else None)
 page.goto((BASE/'index.html').as_uri())
 check('Exact SEO title',page.title()=='Motor Inn Auto Group Reviews | Real Customer Reviews in Carroll, IA')
 check('All five platform rows',page.locator('.platform').count()==5)
 check('Missing ratings stay unknown',page.get_by_text('Rating not yet verified',exact=True).count()==5)
 check('Unavailable Google/Cars review actions disabled',page.locator('button:disabled').count()==2)
 graph=json.loads(page.locator('#organization-schema').text_content())
 check('Default Organization schema only',graph['@type']=='Organization' and 'aggregateRating' not in graph and 'review' not in graph)
 check('No preview aggregate or quoted reviews',not page.locator('#first-party').is_visible() and not page.locator('#quotes-section').is_visible())
 for width in [320,390,768,1440]:
  page.set_viewport_size({'width':width,'height':1000})
  check(f'No horizontal overflow at {width}px',page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
  if width in [390,1440]:page.screenshot(path=str(QA/f'preview-{width}.png'),full_page=True)
 page.keyboard.press('Tab')
 check('Keyboard skip link focus',page.locator('.skip').evaluate('(el)=>el===document.activeElement'))
 # Measure actual browser-converted foreground/background contrast.
 colors=page.evaluate('''() => {const c=document.createElement('canvas');c.width=c.height=1;const x=c.getContext('2d');const rgb=color=>{x.clearRect(0,0,1,1);x.fillStyle=color;x.fillRect(0,0,1,1);return Array.from(x.getImageData(0,0,1,1).data).slice(0,3)};const style=getComputedStyle(document.documentElement);return Object.fromEntries(['bg','ink','primary','surface','muted','accent','white'].map(k=>[k,rgb(style.getPropertyValue('--'+k).trim())]));}''')
 def lum(rgb):
  vals=[v/255 for v in rgb];linear=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in vals]
  return sum(a*b for a,b in zip(linear,[.2126,.7152,.0722]))
 for fg,bg in [('ink','bg'),('muted','bg'),('muted','surface'),('white','primary'),('primary','bg'),('ink','accent')]:
  a,b=sorted([lum(colors[fg]),lum(colors[bg])]);ratio=(b+.05)/(a+.05)
  check(f'Contrast {fg}/{bg}: {ratio:.2f}:1',ratio>=4.5)
 # Real data behavior: synthetic fixtures remain in browser memory only, never config.
 page.add_init_script("""window.__TEST_FIXTURE__=true;""")
 script=page.locator('script').last.text_content()
 page.evaluate("""() => {const d=window.REVIEWS_DATA;d.platforms[0]={...d.platforms[0],verified:true,checkedAt:'2026-09-15',rating:4.5,count:10,profileUrl:'https://example.com/reviews'};d.reviews=[{author:'QA fixture',text:'<img src=x onerror=alert(1)>',date:'2026-09-15',rating:4,scale:5,sourceUrl:'https://example.com/review',verified:true,permissionConfirmed:true,platformId:'google',origin:'third-party'}];} """)
 page.evaluate(script)
 check('Verified summary displays supplied values',page.locator('.rating').first.text_content()=='4.5 / 5')
 check('Untrusted review text stays text',page.locator('#quotes img').count()==0 and '<img' in page.locator('#quotes').text_content())
 graph=json.loads(page.locator('#organization-schema').text_content())
 check('Third-party values excluded from schema', 'aggregateRating' not in graph and 'review' not in graph)
 page.evaluate("""() => {const d=window.REVIEWS_DATA;d.structuredReviews={enabled:true,aggregate:{verified:true,origin:'first-party',rating:4.6,count:10,scale:5,checkedAt:'2026-09-15',sourceUrl:'https://example.com/first-party'}};d.reviews[0].origin='first-party';d.reviews[0].platformId='first-party';}""")
 page.evaluate(script)
 graph=json.loads(page.locator('#organization-schema').text_content())
 check('Verified first-party AggregateRating supported',graph['aggregateRating']['@type']=='AggregateRating' and graph['aggregateRating']['ratingValue']==4.6)
 check('Verified first-party Review supported',graph['review'][0]['@type']=='Review')
 check('Schema aggregate visible to readers',page.locator('#first-party').is_visible() and '4.6 / 5 from 10 reviews' in page.locator('#first-party').text_content())
 page.evaluate("""() => {window.REVIEWS_DATA.platforms[0].rating=99;window.REVIEWS_DATA.structuredReviews.aggregate.origin='third-party';window.REVIEWS_DATA.reviews=[];}""")
 page.evaluate(script)
 graph=json.loads(page.locator('#organization-schema').text_content())
 check('Out-of-range platform score rejected',page.locator('.rating').first.text_content()=='Rating not yet verified')
 check('Third-party aggregate rejected even when enabled','aggregateRating' not in graph)
 check('Rejected aggregate removed visibly',not page.locator('#first-party').is_visible())
 check('No JavaScript errors',not errors)
 check('Zero external requests on load and render',not external)
 # Reload pristine preview before final browser close.
 page.reload()
 check('Preview remains noindex',page.locator('meta[name=robots]').get_attribute('content')=='noindex, nofollow')
 context.close()
 with p.chromium.launch_persistent_context(str(QA/'tmp'/'nojs-profile'),headless=True,java_script_enabled=False,env={**os.environ,'TMPDIR':str(QA/'tmp')}) as nojs:
  tab=nojs.pages[0];tab.goto((BASE/'index.html').as_uri())
  check('No-JavaScript fallback is usable',tab.locator('noscript').is_visible() and tab.get_by_role('link',name='official Motor Inn review page').is_visible())
(QA/'results.json').write_text(json.dumps({'checks':results,'passed':len(results),'errors':errors,'external_requests':external},indent=2)+'\n')
import shutil
shutil.rmtree(QA/'tmp')
print(json.dumps({'passed':len(results),'errors':errors,'external_requests':external}))
