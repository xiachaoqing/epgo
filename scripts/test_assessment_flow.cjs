// Local browser regression. All HTTP requests are intercepted: no live orders or messages.
// node scripts/test_assessment_flow.cjs [/path/to/node_modules/playwright]
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const assert = require('node:assert/strict');
const {execFileSync} = require('node:child_process');
const {chromium} = require(process.argv[2] || 'playwright');
const root = path.resolve(__dirname, '..');
const output = fs.mkdtempSync(path.join(os.tmpdir(), 'epgo-ui-'));
const index = fs.readFileSync(path.join(root,'epgo/index.html'),'utf8');
const baseline = execFileSync('git',['show','d66a545:epgo/index.html'],{cwd:root,encoding:'utf8'});
const scripts = html => [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)].map(m=>m[1]);
assert.deepEqual(scripts(index),scripts(baseline),'all purchase inline scripts must remain byte-identical');
const answerRows = [
 ['a balcony','a panda','a helmet','stairs','a dolphin'],
 ['2','2','0','1','2','1'],
 ['hospital','cook','hungry','vegetables','bowl'],
 ['1','0','2','0','1'],
 ['take a coat','hot and sunny','black clouds','his camera','big leaves','home','surprised']
];
let browser;
const errors = [];
async function setup(width=390,wx=false) {
 const context = await browser.newContext({viewport:{width,height:844}, ...(wx?{userAgent:'Mozilla/5.0 MicroMessenger/8.0'}:{})});
 if(wx) await context.addInitScript(()=>{
   sessionStorage.setItem('jzt_openid','TEST_OPENID');
   window.wx={config(){},ready(fn){fn()},error(){},onMenuShareAppMessage(){},onMenuShareTimeline(){},chooseWXPay(p){window.__pay=p;}};
 });
 const calls=[];
 await context.route('**/*',async route=>{
   const url=new URL(route.request().url());
   if(url.hostname==='epgo.test' && url.pathname.startsWith('/epgo/')) {
     const rel=decodeURIComponent(url.pathname)+(url.pathname.endsWith('/')?'index.html':'');
     const file=path.resolve(root,'.'+rel);
     if(file.startsWith(root+path.sep) && fs.existsSync(file)) return route.fulfill({path:file});
     return route.fulfill({status:404,body:'missing local fixture'});
   }
   if(url.pathname.includes('/api/jzt/')) {
     calls.push({url:url.pathname,method:route.request().method(),data:route.request().postDataJSON()});
     let body={signature:'test',appId:'test',timestamp:1,nonceStr:'test',followed:true,status:'pending'};
     if(url.pathname.endsWith('/order/create')) body={code:0,order_no:'TEST_ORDER',pay_params:{appId:'test',timeStamp:'1',nonceStr:'test',package:'test',signType:'RSA',paySign:'test'}};
     return route.fulfill({json:body});
   }
   if(route.request().resourceType()==='image') {
     const name=decodeURIComponent(path.basename(url.pathname));
     if(name==='logo.png') return route.fulfill({path:path.join(root,'epgo/favicon.ico')});
     const local=['epgo/'+name,'epgo/thumbs/thumb_'+name.replace(/\.png$/,'.jpg'),'epgo/cropped/'+name.replace(/\.png$/,'_crop.png')].map(f=>path.join(root,f)).find(f=>fs.existsSync(f));
     return route.fulfill({path:local||path.join(root,'epgo/share.jpg')});
   }
   return route.fulfill({status:200,body:'',contentType:'text/plain'});
 });
 const page=await context.newPage(); page.on('pageerror',e=>errors.push(e.message));
 return {page,context,calls};
}
async function begin(page) {
 await page.goto('http://epgo.test/epgo/assessment.html');
 await page.locator('.level-card.recommended').click();
 await page.locator('#studentName').fill('测试同学');
 await page.locator('#studentGrade').selectOption({label:'小学四年级'});
 await page.getByRole('button',{name:'开始答题',exact:true}).click();
}
async function fill(page,wrong=false) {
 for(let pi=0;pi<answerRows.length;pi++) {
   await page.locator(`[data-part-target="${pi}"]`).click();
   for(let qi=0;qi<answerRows[pi].length;qi++) {
     const id=`p${pi}_q${qi}`, expected=answerRows[pi][qi];
     const inputs=page.locator(`input[data-id="${id}"]`);
     if(await inputs.first().getAttribute('type')==='radio') {
       const options=await inputs.evaluateAll(nodes=>nodes.map(n=>n.value));
       const value=wrong?options.find(v=>v!==expected):expected;
       await page.locator(`input[data-id="${id}"][value="${value}"]`).check();
     } else await inputs.fill(wrong?'incorrect':expected);
   }
   if(pi===2) await page.locator(`input[data-id="p2_title"][value="${wrong?'0':'1'}"]`).check();
 }
}
async function noOverflow(page,label) {
 const sizes=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));
 assert(sizes.scroll<=sizes.width+1,`${label}: ${JSON.stringify(sizes)}`);
}
(async()=>{
 browser=await chromium.launch({...(process.argv[3]?{executablePath:process.argv[3]}:{channel:'chrome'}),headless:true,timeout:20000});
 const {page,context,calls}=await setup();
 await page.goto('http://epgo.test/epgo/assessment.html');
 await page.screenshot({path:path.join(output,'assessment-mobile.png'),fullPage:true});
 assert.equal(await page.locator('.level-card[aria-disabled="true"]').count(),2);
 await page.locator('.level-card.recommended').click();
 await page.getByRole('button',{name:'开始答题',exact:true}).click();
 assert.equal(await page.locator('#profileError').isVisible(),true);
 await page.locator('#studentName').fill('测试同学');
 await page.locator('#studentPhone').fill('123');
 await page.getByRole('button',{name:'开始答题',exact:true}).click();
 assert.match(await page.locator('#profileError').innerText(),/11位/);
 await page.locator('#studentPhone').fill('');
 await page.getByRole('button',{name:'开始答题',exact:true}).click();
 await fill(page);
 await page.locator('[data-id="p4_q0"]').fill('');
 assert.equal(await page.locator('#progText').innerText(),'28/29');
 page.once('dialog',d=>d.dismiss()); await page.locator('#btnSubmit').click();
 assert.equal(await page.locator('#quizPanel').isVisible(),true);
 await page.reload(); await page.locator('#resumeDraft').click();
 assert.equal(await page.locator('#progText').innerText(),'28/29');
 await page.locator('[data-id="p4_q0"]').fill('  TAKE   A COAT  ');
 await page.locator('#btnSubmit').click();
 assert.equal(await page.locator('#rScore').innerText(),'29/29');
 assert.equal(await page.locator('#rParts .ps-item').count(),5);
 await page.screenshot({path:path.join(output,'result-mobile.png'),fullPage:true});
 await page.reload(); await page.locator('#viewSaved').click();
 assert.equal(await page.locator('#rScore').innerText(),'29/29');
 await page.goto('http://epgo.test/epgo/assessment.html#result');
 assert.equal(await page.locator('#rScore').innerText(),'29/29');
 await page.locator('#buyLink').click();
 assert.equal(new URL(page.url()).hash,'#pricing');
 assert.equal(new URL(page.url()).search,'?source=assessment');
 await page.locator('.price-card .btn-price').first().click();
 assert.equal(await page.locator('#buyModal').isVisible(),true);
 await page.locator('#mPhone').fill('13800000000');
 let normalWarning=''; page.once('dialog',async d=>{normalWarning=d.message();await d.accept();});
 await page.locator('#payBtn').click(); assert.match(normalWarning,/微信/);
 assert.equal(calls.filter(c=>c.url.endsWith('/order/create')).length,0);
 await page.locator('#buyModal .modal-x').click();
 await page.goto('http://epgo.test/epgo/#follow');
 assert.equal(await page.locator('#followModal').isVisible(),true);
 await context.close();

 const negative=await setup(1440); await begin(negative.page); await fill(negative.page,true);
 await negative.page.locator('[data-part-target="2"]').click();
 await negative.page.screenshot({path:path.join(output,'quiz-desktop.png'),fullPage:true});
 await negative.page.locator('#btnSubmit').click(); assert.equal(await negative.page.locator('#rScore').innerText(),'0/29');
 const guards=await negative.page.evaluate(()=>({
   substring:isCorrect({type:'fill'},{key:['a']},'banana'),
   stem:isCorrect({type:'fill'},{key:['surprised']},'surpris'),
   hotOnly:isCorrect(QUIZZES.ket.parts[4],QUIZZES.ket.parts[4].questions[1],'hot'),
   clozeWrong:isCorrect(QUIZZES.ket.parts[2],QUIZZES.ket.parts[2].questions[0],'hospitalxxx'),
   full:isCorrect(QUIZZES.ket.parts[4],QUIZZES.ket.parts[4].questions[1],'sunny and hot')
 })); assert.deepEqual(guards,{substring:false,stem:false,hotOnly:false,clozeWrong:false,full:true});
 await negative.context.close();
 const empty=await setup(); await begin(empty.page);
 empty.page.once('dialog',d=>d.accept()); await empty.page.locator('#btnSubmit').click();
 assert.equal(await empty.page.locator('#rScore').innerText(),'0/29');
 assert.match(await empty.page.locator('#rAdvice').innerText(),/没有作答/); await empty.context.close();

 const unavailable=await setup();
 await unavailable.context.addInitScript(()=>{
   Storage.prototype.getItem=()=>{throw new Error('storage disabled')};
   Storage.prototype.setItem=()=>{throw new Error('storage disabled')};
 });
 await begin(unavailable.page); unavailable.page.once('dialog',d=>d.accept());
 await unavailable.page.locator('#btnSubmit').click();
 assert.match(await unavailable.page.locator('#storageStatus').innerText(),/未能保存/);
 assert.equal(await unavailable.page.locator('#rScore').innerText(),'0/29');
 await unavailable.page.getByRole('button',{name:'复制报告发给老师'}).click();
 assert.match(await unavailable.page.locator('#storageStatus').innerText(),/已复制|不支持复制/);
 await unavailable.context.close();

 for(const width of [320,390,768,1024,1440]) {
   const s=await setup(width);
   for(const route of ['assessment.html','']) {
     await s.page.goto('http://epgo.test/epgo/'+route); await noOverflow(s.page,`${route||'purchase'} ${width}`);
     if(route && width===1440) await s.page.screenshot({path:path.join(output,'assessment-desktop.png'),fullPage:true});
   }
   const columns=await s.page.locator('.price-grid').evaluate(n=>getComputedStyle(n).gridTemplateColumns.split(' ').length);
   assert.equal(columns,width<=600?1:width<=960?2:4);
   for(let i=0;i<4;i++) {
     await s.page.locator('.price-card .btn-price').nth(i).click();
     const modal=await s.page.locator('#buyModal .modal').boundingBox();
     assert(modal.x>=0 && modal.x+modal.width<=width+1);
     assert.equal(await s.page.locator('#mAmount').innerText(),['¥9.9','¥39','¥99','¥298'][i]);
     if(i===0 && [390,1440].includes(width)) await s.page.screenshot({path:path.join(output,`purchase-modal-${width}.png`)});
     await s.page.locator('#buyModal .modal-x').click();
   }
   if(width===1440) await s.page.screenshot({path:path.join(output,'purchase-desktop.png'),fullPage:true});
   await begin(s.page); await noOverflow(s.page,`quiz ${width}`);
   if(width===390) await s.page.screenshot({path:path.join(output,'quiz-mobile.png'),fullPage:true});
   await s.context.close();
 }
 // Exercise the unchanged payment flow against intercepted API and SDK responses only.
 const wx=await setup(390,true);
 await wx.page.goto('http://epgo.test/epgo/');
 await wx.page.locator('.price-card .btn-price').first().click();
 await wx.page.locator('#mPhone').fill('13800000000'); await wx.page.locator('#payBtn').click();
 await wx.page.waitForFunction(()=>!!window.__pay);
 const order=wx.calls.find(c=>c.url.endsWith('/order/create'));
 assert.deepEqual(order.data,{plan_id:'trial',phone:'13800000000',grade:'',openid:'TEST_OPENID',trade_type:'JSAPI'});
 wx.page.once('dialog',d=>d.accept()); await wx.page.evaluate(()=>window.__pay.cancel());
 assert.equal(await wx.page.locator('#payBtn').isEnabled(),true);
 await wx.page.evaluate(()=>window.__pay.success());
 await wx.page.waitForURL('**/result.html?order=TEST_ORDER'); await wx.context.close();
 assert.deepEqual(errors,[],'no browser runtime errors');
 console.log(JSON.stringify({status:'PASS',screenshots:output,viewports:[320,390,768,1024,1440],ket:['29/29','0/29','blank 0/29','draft resume','saved result'],payment:'unchanged scripts + intercepted SDK/API only'},null,2));
})().catch(e=>{console.error(e);process.exitCode=1}).finally(async()=>{if(browser) await browser.close()});
