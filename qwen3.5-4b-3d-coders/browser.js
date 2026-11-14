// Headless Chromium (swiftshader WebGL) with every page served from disk under http://glb3d.local/
// and every three.js CDN URL (jsdelivr / unpkg / esm.sh, any version) answered from the local three@0.160.0.
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const ROOT = __dirname;
const THREE_DIR = path.join(ROOT, 'node_modules', 'three');
const ORIGIN = 'http://glb3d.local/';
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json',
  '.glb': 'model/gltf-binary', '.svg': 'image/svg+xml', '.png': 'image/png', '.css': 'text/css' };

function localFor(url) {
  if (url.startsWith(ORIGIN)) return '/' + decodeURIComponent(url.slice(ORIGIN.length).split('?')[0]);
  const m = url.match(/^https?:\/\/(?:cdn\.jsdelivr\.net\/npm|unpkg\.com|esm\.sh|cdn\.skypack\.dev)\/three(?:@[^/]+)?\/(.+?)(?:\?.*)?$/);
  if (m) return path.join(THREE_DIR, m[1].replace(/^examples\/js\//, 'examples/jsm/'));
  // 14/11/2026: the 3D Coder imports three from cdnjs (ajax/libs/three.js/<v>/three.module[.min].js)
  if (/^https?:\/\/cdnjs\.cloudflare\.com\/ajax\/libs\/three\.js\/[^/]+\/three\.module(?:\.min)?\.js(?:\?.*)?$/.test(url))
    return path.join(THREE_DIR, 'build', 'three.module.js');
  if (/^https?:\/\/(?:cdn\.jsdelivr\.net\/npm|unpkg\.com|esm\.sh)\/three(?:@[^/]+)?\/?$/.test(url))
    return path.join(THREE_DIR, 'build', 'three.module.js');
  return null;
}

async function launch() {
  return puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--use-gl=angle', '--use-angle=swiftshader',
      '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl'],
  });
}

async function openPage(browser, { width = 1000, height = 800, log = [] } = {}) {
  const page = await browser.newPage();
  await page.setViewport({ width, height });
  await page.setRequestInterception(true);
  page.on('request', req => {
    if (req.url().endsWith('/favicon.ico')) return req.respond({ status: 204, body: '' });
    const f = localFor(req.url());
    if (f === null) return req.continue();
    try {
      const body = fs.readFileSync(f);
      req.respond({ status: 200, contentType: MIME[path.extname(f)] || 'application/octet-stream', body,
        headers: { 'Access-Control-Allow-Origin': '*' } });
    } catch (e) {
      log.push(`[404] ${req.url()}`);
      req.respond({ status: 404, body: 'not found' });
    }
  });
  page.on('console', m => { if (m.type() === 'error' && !/status of 40[34]/.test(m.text())) log.push(`[console] ${m.text()}`); });
  page.on('pageerror', e => log.push(`[pageerror] ${e.message}`));
  return page;
}

// GLB sanity: magic, version 2, declared length, JSON chunk with >= 1 mesh.
function checkGlb(buf) {
  if (buf.length < 20 || buf.toString('ascii', 0, 4) !== 'glTF') return { ok: false, why: 'no glTF magic' };
  if (buf.readUInt32LE(4) !== 2) return { ok: false, why: 'not glTF 2' };
  if (buf.readUInt32LE(8) !== buf.length) return { ok: false, why: 'length mismatch' };
  const jl = buf.readUInt32LE(12);
  if (buf.toString('ascii', 16, 20) !== 'JSON') return { ok: false, why: 'first chunk not JSON' };
  const j = JSON.parse(buf.toString('utf8', 20, 20 + jl));
  const meshes = (j.meshes || []).length;
  let prims = 0; for (const m of j.meshes || []) prims += (m.primitives || []).length;
  return { ok: meshes > 0, why: meshes ? '' : 'no mesh', meshes, primitives: prims, nodes: (j.nodes || []).length,
    animations: (j.animations || []).length, materials: (j.materials || []).length, bytes: buf.length };
}

module.exports = { ROOT, ORIGIN, launch, openPage, checkGlb };
