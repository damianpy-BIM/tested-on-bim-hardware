#!/usr/bin/env python3
"""generate.py - text prompt -> Three.js page (+ GLB) with a local Qwen3.5-4B 3D coder, checked in a headless browser.

  python3 generate.py glb   "Create a low-poly delivery drone with four rotors" --out out/drone
  python3 generate.py scene "A modern glass house with a flat roof, a deck and trees" --out out/house

glb   = ccore/Qwen3.5-4B-GLB-3D-Coder: the page has an Export GLB button; success = a valid glTF 2.0 binary with >= 1 mesh.
scene = ccore/Qwen3.5-4B-3D-Coder: an architectural / landscape scene; success = a drawn canvas and no page error.
A failed page (no complete HTML, broken JavaScript, no GLB) is regenerated, up to --tries times.

Needs: llama.cpp `llama-server` (LLAMA_SERVER), the Q4_K_M GGUF (MODEL), Node.js >= 20 and `npm install` in this folder.
GPU: pick the card with CUDA_VISIBLE_DEVICES; one 4B Q4 model + 3 x 32k context fits in about 7 GB of VRAM.
"""
import argparse, json, os, re, signal, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.realpath(__file__))
PORT = int(os.environ.get("PORT", "8323"))
MODES = {
    "glb": {"system": ("Create game assets for the Godot editor, which uses GLB files. Create whatever the user requests as a good-quality "
                       "low-poly asset using only Three.js in one complete standalone HTML file. The HTML must show the asset and include "
                       "an Export GLB button that downloads a working GLB. If the requested asset needs animation, add it and include the "
                       "animation in the exported GLB; otherwise make it static."),
            "sampling": {"temperature": 0.8, "top_k": 40, "top_p": 0.95, "min_p": 0.0}, "max_tokens": 24000, "extra": {}},
    "scene": {"system": ("Use only the Three.js core ES module from https://cdnjs.cloudflare.com/ajax/libs/three.js/0.160.0/three.module.min.js. "
                         "Do not import addons or legacy examples/js paths; implement any camera controls directly inside the HTML. "
                         "Write one complete standalone HTML file that shows the requested scene, framed by the initial camera."),
              "sampling": {"temperature": 0.7, "top_k": 30, "top_p": 0.95, "min_p": 0.0}, "max_tokens": 16384,
              "extra": {"chat_template_kwargs": {"enable_thinking": False}}},
}


def extract_html(text):
    t = re.sub(r"<think>.*?</think>", "", text, flags=re.S)
    m = re.search(r"(<!DOCTYPE html|<html)", t, re.I)
    e = t.lower().rfind("</html>")
    return t[m.start():e + 7] if m and e >= 0 else None


def chat(mode, prompt, timeout=900):
    c = MODES[mode]
    body = {"model": "local", "messages": [{"role": "system", "content": c["system"]}, {"role": "user", "content": prompt}],
            "max_tokens": c["max_tokens"], "stream": False, **c["sampling"], **c["extra"]}
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=MODES)
    ap.add_argument("prompt")
    ap.add_argument("--out", default="out/asset")
    ap.add_argument("--tries", type=int, default=3)
    a = ap.parse_args()
    server, model = os.environ.get("LLAMA_SERVER", "llama-server"), os.environ.get("MODEL")
    if not model or not os.path.exists(model):
        sys.exit("set MODEL=/path/to/the Q4_K_M .gguf")
    out = os.path.abspath(a.out); os.makedirs(out, exist_ok=True)
    srv = subprocess.Popen([server, "-m", model, "-ngl", "99", "-c", "32768", "-fa", "on", "--host", "127.0.0.1",
                            "--port", str(PORT), "--no-webui"], stdout=open(os.path.join(out, "server.log"), "w"),
                           stderr=subprocess.STDOUT)
    try:
        for _ in range(180):
            try:
                if json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/health", timeout=3)).get("status") == "ok":
                    break
            except Exception:
                time.sleep(1)
        attempts = []
        for n in range(1, a.tries + 1):
            t0 = time.time()
            r = chat(a.mode, a.prompt)
            wall = time.time() - t0
            toks = r.get("usage", {}).get("completion_tokens")
            att = {"n": n, "tokens": toks, "seconds": round(wall, 1), "tok_s": round(toks / wall, 1) if toks else None}
            page = extract_html(r["choices"][0]["message"].get("content") or "")
            if not page:
                att["result"] = "no complete HTML"; attempts.append(att); continue
            hp = os.path.join(out, f"scene-{n}.html"); open(hp, "w").write(page)
            js = ["render.js", hp, os.path.join(out, "preview.png"), os.path.join(out, "asset.glb")] if a.mode == "glb" \
                else ["scene.js", hp, os.path.join(out, "preview.png")]
            p = subprocess.run(["node", *js], cwd=HERE, capture_output=True, text=True, timeout=240)
            res = json.loads((p.stdout.strip().splitlines() or ["{}"])[-1])
            att["result"] = "ok" if res.get("ok") else (res.get("why") or "render failed")
            att["check"] = res
            attempts.append(att)
            if res.get("ok"):
                os.replace(hp, os.path.join(out, "scene.html"))
                break
        json.dump({"mode": a.mode, "prompt": a.prompt, "attempts": attempts}, open(os.path.join(out, "meta.json"), "w"), indent=1)
        print(json.dumps(attempts[-1] if attempts else {"result": "no attempt"}))
    finally:
        srv.send_signal(signal.SIGTERM)
        srv.wait(30)


if __name__ == "__main__":
    main()
