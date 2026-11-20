#!/usr/bin/env python3
"""Verify + measure the Mac FastFrames clips the way the V100 run was measured.

Per clip: ffmpeg frame count + dimensions + fps (ffprobe-equivalent via the imageio-ffmpeg
binary), then decoded-frame quality: brightness (mean gray 0-255), frame-diff (mean abs
difference between consecutive frames, 0-255), Laplacian-variance sharpness (mean over
frames). Extracts the same sample frames as the V100 out/frames set: 0.06 s, 2.5 s, 5.00 s
PNGs + a mid jpg.

Run: .venv/bin/python -I quality_mac.py out/corgi_mac.mp4 out/piano_mac.mp4 out/site_mac.mp4
Writes quality_mac.json next to this script.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import imageio.v2 as imageio
import imageio_ffmpeg


def probe(mp4):
    exe = imageio_ffmpeg.get_ffmpeg_exe()
    # frame count + fps + dimensions: copy-decode into null muxer
    r = subprocess.run([exe, "-loglevel", "info", "-i", mp4, "-map", "0:v", "-c", "copy",
                        "-f", "null", "-"], capture_output=True, text=True)
    err = r.stderr
    m = re.search(r"frame=\s*(\d+)", err)
    d = re.search(r"(\d{2,5})x(\d{2,5})[,.]", err)
    f = re.search(r"([\d.]+) fps", err) or re.search(r"fps=\s*([\d.]+)", err)
    return {"frames": int(m.group(1)) if m else None,
            "dims": f"{d.group(1)}x{d.group(2)}" if d else None,
            "fps": float(f.group(1)) if f else None}


def metrics(mp4):
    rd = imageio.get_reader(mp4)
    grays, lapvars = [], []
    prev = None
    frdiff = []
    for fr in rd:
        g = (0.299 * fr[..., 0] + 0.587 * fr[..., 1] + 0.114 * fr[..., 2]).astype(np.float32)
        grays.append(g.mean())
        lap = 4 * g[1:-1, 1:-1] - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:]
        lapvars.append(float(lap.var()))
        if prev is not None:
            frdiff.append(float(np.abs(g - prev).mean()))
        prev = g
    rd.close()
    return {
        "brightness_mean_of_255": round(float(np.mean(grays)), 1),
        "frame_diff_mean": round(float(np.mean(frdiff)), 1),
        "laplacian_variance_sharpness": round(float(np.mean(lapvars)), 2),
        "n_frames_decoded": len(grays),
    }


def samples(mp4, outdir: Path):
    stem = Path(mp4).stem.replace("_mac", "")
    if "v100ref" in str(mp4):
        stem = "v100_" + stem
    rd = imageio.get_reader(mp4)
    want = {"0.06s": 1, "2.5s": 40, "5.00s": 81}
    saved = []
    idx = 0
    for fr in rd:
        idx += 1
        for name, frame_no in want.items():
            if idx == frame_no:
                p = outdir / f"{stem}_{name}.png"
                imageio.imwrite(p, fr)
                saved.append(str(p))
        if idx == 41:
            from PIL import Image
            Image.fromarray(fr).convert("RGB").save(outdir / f"{stem}_mid.jpg", quality=92)
            saved.append(str(outdir / f"{stem}_mid.jpg"))
        if idx >= 81:
            break
    rd.close()
    return saved


def main():
    out = {}
    sample_dir = Path(__file__).parent / "out" / "frames_mac"
    sample_dir.mkdir(parents=True, exist_ok=True)
    for mp4 in sys.argv[1:]:
        p = Path(mp4)
        if not p.exists():
            out[p.name] = {"error": "missing"}
            continue
        rec = {"probe": probe(str(p))}
        rec.update(metrics(str(p)))
        rec["sample_frames"] = samples(str(p), sample_dir)
        rec["size_bytes"] = p.stat().st_size
        out[p.name] = rec
        print(json.dumps({p.name: rec}), flush=True)
    Path(__file__).with_name("quality_mac.json").write_text(json.dumps(out, indent=1))
    print("QUALITY_DONE")


if __name__ == "__main__":
    main()
