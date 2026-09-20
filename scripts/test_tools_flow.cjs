// Local browser regression for the independent learning tools page.
// node scripts/test_tools_flow.cjs [/path/to/node_modules/playwright] [chromium]
const fs=require('node:fs');
const path=require('node:path');
const os=require('node:os');
const assert=require('node:assert/strict');
const {chromium}=require(process.argv[2]||'playwright');
const root=path.resolve(__dirname,'..');
const output=fs.mkdtempSync(path.join(os.tmpdir(),'epgo-tools-'));
let browser;
const errors=[];
async function setup(width){
  const context=await browser.newContext({viewport:{width,height:850}});
  const calls=[];
  await context.route('**/*',async route=>{
    const url=new URL(route.request().url());
    if(url.pathname.endsWith('/epgo/media-api.php')){
      calls.push({url:url.pathname,method:route.request().method()});
      return route.fulfill({status:503,json:{status:'error',message:'媒体服务测试占位'}});
    }
    if(url.hostname==='epgo.test'&&url.pathname.startsWith('/epgo/')){
      const rel=decodeURIComponent(url.pathname)+(url.pathname.endsWith('/')?'index.html':'');
      const file=path.resolve(root,'.'+rel);
      if(file.startsWith(root+path.sep)&&fs.existsSync(file))return route.fulfill({path:file});
      return route.fulfill({status:404,body:'missing local fixture'});
    }
    if(url.pathname.includes('/api/')){calls.push({url:url.pathname,method:route.request().method()});return route.fulfill({json:{code:0}})}
    if(route.request().resourceType()==='image')return route.fulfill({path:path.join(root,'epgo/share.jpg')});
    return route.fulfill({status:200,body:'',contentType:'text/plain'});
  });
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));return{page,context,calls};
}
async function noOverflow(page,label){const s=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));assert(s.scroll<=s.width+1,`${label}: ${JSON.stringify(s)}`)}
(async()=>{
  browser=await chromium.launch({...(process.argv[3]?{executablePath:process.argv[3]}:{channel:'chrome'}),headless:true,timeout:20000});
  const s=await setup(390),page=s.page;
  await page.goto('http://epgo.test/epgo/');
  await page.locator('a[href="/epgo/tools.html#calendar"]').click();
  assert.equal(new URL(page.url()).pathname,'/epgo/tools.html');
  assert.equal(new URL(page.url()).hash,'#calendar');
  await page.goto('http://epgo.test/epgo/tools.html#today');
  await page.evaluate(()=>localStorage.clear());
  await page.reload();
  assert.equal(await page.locator('#today-total').innerText(),'0');
  await page.locator('[data-action="quick-task"]').click();
  await page.locator('#cal-title').fill('完成 KET 阅读');
  await page.locator('#calendar-form button[type="submit"]').click();
  assert.equal(await page.locator('#today-total').innerText(),'1');
  assert.equal(await page.locator('#today-done').innerText(),'0');
  await page.locator('#calendar-list [data-cal-done]').click();
  assert.equal(await page.locator('#today-done').innerText(),'1');
  await page.reload();await page.locator('[data-panel="today"]').click();
  assert.equal(await page.locator('#today-done').innerText(),'1');
  await page.locator('[data-panel="calendar"]').click();
  assert.equal(await page.locator('#calendar-list .item').count(),1);
  await page.locator('#calendar-list [data-cal-delete]').click();
  assert.equal(await page.locator('#calendar-list .item').count(),0);

  await page.locator('[data-panel="memo"]').click();
  await page.locator('#memo-text').fill('第三人称单数要加 s');
  await page.locator('#memo-example').fill('She likes reading.');
  await page.locator('#memo-form button[type="submit"]').click();
  assert.equal(await page.locator('#memo-list .item').count(),1);
  await page.locator('#memo-search').fill('reading');
  assert.equal(await page.locator('#memo-list .item').count(),1);
  await page.locator('[data-memo-delete]').click();
  assert.equal(await page.locator('#memo-list .item').count(),0);

  await page.locator('[data-panel="vocab"]').click();
  await page.locator('#vocab-word').fill('improve');
  await page.locator('#vocab-meaning').fill('提高');
  await page.locator('#vocab-form button[type="submit"]').click();
  assert.equal(await page.locator('#vocab-list .item').count(),1);
  await page.locator('[data-vocab-done]').click();
  assert.match(await page.locator('#vocab-list .item').first().getAttribute('class'),/done/);
  await page.locator('[data-vocab-delete]').click();
  assert.equal(await page.locator('#vocab-list .item').count(),0);

  await page.locator('[data-panel="plan"]').click();
  await page.locator('#plan-minutes').selectOption('30');
  await page.locator('#plan-form button[type="submit"]').click();
  assert.equal(await page.locator('#plan-list .item').count(),7);
  await page.evaluate(()=>localStorage.setItem('epgo_tool_vocab_v1',JSON.stringify([{id:'test-word',word:'improve',meaning:'提高',example:'I improve every day.',mastered:false,createdAt:Date.now()}])));
  await page.reload();
  await page.locator('[data-panel="wordcards"]').click();
  assert.equal(await page.locator('#wordcard').isVisible(),true);
  assert.equal(await page.locator('#wordcard-word').innerText(),'improve');
  await page.locator('#wordcard-show').click();
  assert.match(await page.locator('#wordcard-answer').innerText(),/提高/);

  await page.locator('[data-panel="timer"]').click();
  await page.locator('[data-min="15"]').click();
  assert.equal(await page.locator('#clock').innerText(),'15:00');
  await page.locator('#timer-start').click();
  assert.equal(await page.locator('#timer-start').innerText(),'暂停');
  await page.locator('#timer-start').click();
  assert.equal(await page.locator('#timer-start').innerText(),'开始');
  await page.screenshot({path:path.join(output,'tools-mobile.png'),fullPage:true});

  await page.evaluate(()=>localStorage.setItem('epgo_assessment_result_v3',JSON.stringify({version:3,score:24,total:29,level:'ket',profile:{name:'测试同学'},createdAt:'2026-09-19T10:00:00.000Z',partScores:[{name:'阅读',score:5,total:5},{name:'词汇',score:5,total:6},{name:'完形',score:5,total:6}]})));
  await page.locator('[data-panel="report"]').click();
  assert.match(await page.locator('#report-content').innerText(),/24/);
  assert.equal(await page.locator('#report-content .part-score').count(),3);

  const png=Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=','base64');
  await page.locator('[data-panel="idphoto"]').click();
  await page.locator('#photo-file').setInputFiles({name:'sample.png',mimeType:'image/png',buffer:png});
  await page.waitForFunction(()=>!document.querySelector('#photo-canvas').hidden);
  assert.equal(await page.locator('#photo-canvas').getAttribute('width'),'295');
  assert.equal(await page.locator('#photo-download').isEnabled(),true);
  await page.locator('#photo-scale').fill('1.25');
  await page.locator('[data-panel="imagecompress"]').click();
  await page.locator('#compress-file').setInputFiles({name:'sample.png',mimeType:'image/png',buffer:png});
  await page.waitForFunction(()=>!document.querySelector('#compress-canvas').hidden);
  assert.equal(await page.locator('#compress-download').isEnabled(),true);
  assert.match(await page.locator('#compress-meta').innerText(),/压缩后/);
  await page.locator('[data-panel="platform"]').click();
  await page.locator('#platform-url').fill('https://example.com/video/1');
  assert.match(await page.locator('#platform-result').innerText(),/无法识别/);
  await page.locator('#platform-url').fill('https://v.douyin.com/test');
  assert.match(await page.locator('#platform-result').innerText(),/待适配/);
  await page.locator('#platform-url').fill('https://www.bilibili.com/video/BV1test');
  await page.locator('#platform-consent').check();
  await page.locator('#platform-form button[type="submit"]').click();
  await page.waitForFunction(()=>document.querySelector('#platform-result').classList.contains('error'));
  assert.match(await page.locator('#platform-result').innerText(),/媒体服务测试占位/);
  assert.equal(s.calls.filter(x=>x.url.endsWith('/epgo/media-api.php')).length,1);
  await page.goto('http://epgo.test/epgo/');
  assert.equal(await page.locator('footer').innerText().then(t=>t.includes('授权推广页')),false);
  await page.context().close();

  for(const width of [320,390,768,1024,1440]){const x=await setup(width);await x.page.goto('http://epgo.test/epgo/tools.html');await noOverflow(x.page,`tools ${width}`);await x.context.close()}
  assert.deepEqual(errors,[],'no browser runtime errors');
  console.log(JSON.stringify({status:'PASS',screenshots:output,viewports:[320,390,768,1024,1440],features:['calendar add/complete/delete/persist','memo add/search/delete','vocabulary add/master/delete','timer start/pause/reset','assessment report read-only','id photo crop','image compression','footer label removed'],network:'no payment/API calls'},null,2));
})().catch(e=>{console.error(e);process.exitCode=1}).finally(async()=>{if(browser)await browser.close()});
