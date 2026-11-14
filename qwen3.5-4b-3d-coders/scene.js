// node scene.js <scene.html> <out.png>   (14/11/2026, glb3d scene mode: Qwen3.5-4B-3D-Coder pages have no Export GLB button)
// Opens a model-written Three.js page, waits for it to draw, screenshots it. ok = a sized <canvas> and no page error.
const path = require('path');
const { ORIGIN, launch, openPage } = require('./browser');

(async () => {
  const [html, png] = process.argv.slice(2).map(p => path.resolve(p));
  const errors = [];
  const browser = await launch();
  let res = { ok: false };
  try {
    const page = await openPage(browser, { width: 1280, height: 800, log: errors });
    try { await page.goto(ORIGIN + html.slice(1), { waitUntil: 'load', timeout: 45000 }); }
    catch (e) { errors.push(`[nav] ${e.message}`); }
    await new Promise(r => setTimeout(r, 4000));
    await page.screenshot({ path: png });
    const canvas = await page.evaluate(() => {
      const c = Array.from(document.querySelectorAll('canvas')).find(c => c.width > 100 && c.height > 100);
      return c ? [c.width, c.height] : null;
    });
    const fatal = errors.filter(e => e.startsWith('[pageerror]'));
    res = { ok: !!canvas && fatal.length === 0, canvas, why: !canvas ? 'no canvas drawn' : fatal.length ? 'page error' : '' };
  } catch (e) { errors.push(`[render] ${e.message}`); }
  await browser.close();
  res.errors = errors.slice(0, 20);
  console.log(JSON.stringify(res));
  process.exit(res.ok ? 0 : 1);
})();
