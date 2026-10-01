import { launch, arg } from './lib.mjs';
import fs from 'node:fs/promises';
const out=arg('--out','./out/lp-comparison');
const base=arg('--site','http://localhost:5173');
await fs.mkdir(out,{recursive:true});
const browser=await launch();
const results=[];
for(const width of [1440,390]){
 const context=await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce'});
 // Exclude analytics before navigation. Only synthetic/public marketing pages are loaded.
 await context.addInitScript(()=>{localStorage.setItem('sera_internal','1');window.__SERA_ANALYTICS_EXCLUDED__=true;});
 for(const [id,path] of [['desk','/real-estate/products/sumai-desk/'],['sketch','/real-estate/products/sumai-sketch/'],['miharu','/information-systems/products/ai-miharu/']]){
  const page=await context.newPage(); const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+path+'?sera_internal=1',{waitUntil:'networkidle'});
  await page.locator(width<768?'.mobile-page-brief h1':'.sumai-lp h1.font-semibold').waitFor({state:'visible',timeout:60000});
  const decline=page.getByRole('button',{name:'許可しない',exact:true});if(await decline.isVisible())await decline.click();
  await page.evaluate(()=>document.fonts.ready); await page.waitForTimeout(700);
  await page.screenshot({path:`${out}/${id}-${width}-hero.png`});
  if(width<768){await page.locator('.mobile-detail-toggle button').click();await page.waitForTimeout(300);}
  const sections=await page.locator('main section, .sumai-lp section').evaluateAll(nodes=>nodes.map(n=>({id:n.id,heading:n.querySelector('h2')?.textContent?.trim(),buttons:[...n.querySelectorAll('a,button')].map(e=>e.textContent?.trim()).slice(0,12)})));
  const overflow=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,width:innerWidth,excluded:document.documentElement.dataset.analyticsExcluded}));
  for(const n of await page.locator('section[id]').all()){if(await n.isVisible()){await n.scrollIntoViewIfNeeded();await page.waitForTimeout(70);}}
  await page.evaluate(()=>scrollTo(0,0));await page.waitForTimeout(200);
  await page.screenshot({path:`${out}/${id}-${width}-full.png`,fullPage:true});
  results.push({id,width,sections,overflow,errors});await page.close();
 }
 await context.close();
}
await fs.writeFile(`${out}/comparison.json`,JSON.stringify(results,null,2));
await browser.close();
console.log(JSON.stringify(results.map(({id,width,sections,overflow,errors})=>({id,width,sections:sections.map(s=>s.id),overflow,errors})),null,2));
