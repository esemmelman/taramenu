const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || 'C:/Users/esemm/AppData/Local/ms-playwright/chromium-1243/chrome-win64/chrome.exe', headless: true });
  const page = await browser.newPage({viewport: {width: 1440, height: 1000}});
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  const base = process.env.TEST_URL || 'http://127.0.0.1:8765/';
  await page.goto(base);
  const torah = page.frameLocator('#page-frame');
  await torah.locator('.aliyah-heading').last().waitFor();
  assert.equal(await torah.locator('.aliyah-heading').count(), 6);
  assert.equal(await torah.locator('.verse-row').count(), 15);
  assert.deepEqual(await torah.locator('.verse-row .verse-number').allTextContents(), Array.from({length:15},(_,i)=>String(i+1)));
  await torah.locator('#script-toggle').click();
  assert(await torah.locator('body').evaluate(el=>el.classList.contains('script-mode')));
  await torah.locator('#script-toggle').click();
  await page.screenshot({path:'tmp/torah.png',fullPage:true});

  await page.selectOption('#page-list','service');
  assert.equal(await page.locator('.slide-button').count(),13);
  for (let i=1;i<=13;i++) {
    await page.getByRole('button',{name:`Page ${i}`,exact:true}).click();
    await page.waitForFunction(n=>{const img=document.querySelector('#service-image');return img.complete && img.naturalWidth>0 && img.src.includes(`page-${n}.png`);},i);
  }
  await page.getByRole('button',{name:'Page 1',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('#service-image').complete && document.querySelector('#service-image').src.includes('page-1.png'));
  await page.locator('#service-record-button').waitFor({state:'visible'});
  await page.screenshot({path:'tmp/service.png',fullPage:true});

  await page.selectOption('#page-list','torah-portion');
  await page.locator('.torah-verse.highlighted').last().waitFor();
  assert.equal(await page.locator('.torah-verse.highlighted').count(),15);
  assert.deepEqual(await page.locator('.torah-verse.highlighted').evaluateAll(els=>els.map(el=>[Number(el.dataset.chapter),Number(el.dataset.verse)])),Array.from({length:15},(_,i)=>[8,i+1]));
  assert.equal(await page.locator('.torah-chapter').count(),4);
  assert.equal(await page.locator('.torah-verse').count(),121);
  await page.locator('[data-chapter="8"][data-verse="1"]').scrollIntoViewIfNeeded();
  await page.screenshot({path:'tmp/english.png',fullPage:false});

  await page.selectOption('#page-list','timeline/');
  const timeline = page.frameLocator('#page-frame');
  await timeline.locator('.date-heading').last().waitFor();
  assert.equal(await timeline.locator('.date-heading').count(),12);
  assert.equal(await timeline.locator('.date-heading').first().textContent(),'10/26');
  assert.equal(await timeline.locator('.date-heading').last().textContent(),'1/5');
  assert.equal(await timeline.locator('tbody tr').count(),45);
  assert(await timeline.locator('.cell').first().isDisabled());
  await page.screenshot({path:'tmp/timeline.png',fullPage:true});

  await page.selectOption('#page-list','homework');
  await page.waitForFunction(()=>document.querySelector('#sync-status').textContent==='Synced');
  const original = await page.locator('#homework-editor').innerHTML();
  await page.locator('#homework-editor').fill('Tara verification — temporary');
  await page.waitForFunction(()=>document.querySelector('#sync-status').textContent==='Saved and synced');
  await page.reload();
  await page.selectOption('#page-list','homework');
  await page.waitForFunction(()=>document.querySelector('#sync-status').textContent==='Synced');
  assert.equal(await page.locator('#homework-editor').textContent(),'Tara verification — temporary');
  await page.locator('#homework-editor').evaluate((el, original)=>{el.innerHTML=original;el.dispatchEvent(new Event('input'));},original);
  await page.waitForFunction(()=>document.querySelector('#sync-status').textContent==='Saved and synced');
  assert.deepEqual(errors,[]);
  console.log('PASS: 6 aliyot, 15 Hebrew verses, 13 service pages, 121 English verses, 15 yellow highlights, timeline boundaries and view-only cells, homework save/reload/restore; no JavaScript errors.');
  await browser.close();
})().catch(error=>{console.error(error);process.exit(1);});
