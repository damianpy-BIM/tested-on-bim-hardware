// node render.js <scene.html> <out.png> <out.glb>
// Opens a model-written Three.js page, screenshots it, presses its "Export GLB" button and saves the GLB it produces.
// Prints one JSON line: {ok, glb:{...}, errors:[...]}. Exit 0 only when a valid GLB with >= 1 mesh was saved.
const fs = require('fs');
const path = require('path');
const { ORIGIN, launch, openPage, checkGlb } = require('./browser');

// Runs in the page before its own scripts: keep every Blob handed to URL.createObjectURL and every download click.
const HOOK = () => {
  window.__glb3d = { blobs: [], clicks: [] };
  const orig = URL.createObjectURL.bind(URL);
  URL.createObjectURL = (o) => { const u = orig(o); if (o instanceof Blob) window.__glb3d.blobs.push({ u, o }); return u; };
  const ac = HTMLAnchorElement.prototype.click;
  HTMLAnchorElement.prototype.click = function () { window.__glb3d.clicks.push({ href: this.href, name: this.download }); };
  const de = EventTarget.prototype.dispatchEvent;
  EventTarget.prototype.dispatchEvent = function (ev) {
    if (this instanceof HTMLAnchorElement && ev && ev.type === 'click' && this.download) {
      window.__glb3d.clicks.push({ href: this.href, name: this.download }); return true;
    }
    return de.call(this, ev);
  };
};

(async () => {
  const [html, png, glbOut] = process.argv.slice(2).map(p => path.resolve(p));
  const errors = [];
  const browser = await launch();
  let res = { ok: false };
  try {
    const page = await openPage(browser, { width: 1000, height: 800, log: errors });
    await page.evaluateOnNewDocument(HOOK);
    try { await page.goto(ORIGIN + html.slice(1), { waitUntil: 'load', timeout: 45000 }); }
    catch (e) { errors.push(`[nav] ${e.message}`); }
    await new Promise(r => setTimeout(r, 3500));
    await page.screenshot({ path: png });
    const clicked = await page.evaluate(() => {
      const els = Array.from(document.querySelectorAll('button, a, input[type=button], [role=button]'));
      const b = els.find(e => /export|glb|download/i.test((e.textContent || e.value || '') + (e.id || '')));
      if (!b) return false; b.disabled = false; b.click(); return true;
    });
    let b64 = null;
    for (let i = 0; i < 40 && !b64; i++) {
      await new Promise(r => setTimeout(r, 500));
      b64 = await page.evaluate(async () => {
        const H = window.__glb3d; if (!H) return null;
        const cands = H.clicks.map(c => (H.blobs.find(b => b.u === c.href) || {}).o).filter(Boolean).concat(H.blobs.map(b => b.o));
        for (const blob of cands.reverse()) {
          const buf = new Uint8Array(await blob.arrayBuffer());
          if (buf.length > 20 && String.fromCharCode(...buf.slice(0, 4)) === 'glTF') {
            let s = ''; for (let k = 0; k < buf.length; k += 0x8000) s += String.fromCharCode(...buf.slice(k, k + 0x8000));
            return btoa(s);
          }
        }
        return null;
      });
    }
    if (!clicked) errors.push('no export button');
    if (b64) {
      const buf = Buffer.from(b64, 'base64');
      const g = checkGlb(buf);
      if (g.ok) fs.writeFileSync(glbOut, buf);
      res = { ok: g.ok, glb: g, clicked };
    } else res = { ok: false, clicked, why: 'no GLB produced' };
  } catch (e) { errors.push(`[render] ${e.message}`); }
  await browser.close();
  res.errors = errors.slice(0, 20);
  console.log(JSON.stringify(res));
  process.exit(res.ok ? 0 : 1);
})();
