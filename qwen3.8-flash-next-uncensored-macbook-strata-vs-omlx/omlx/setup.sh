#!/bin/bash
# One-command setup: Qwen3.8-Flash-Next-Uncensored on oMLX, exactly as we run it (KV 4-bit affine4, MTP on, YaRN x2 to 524,288 tokens, model pinned).
# usage: ./setup.sh [2|3]      2 = oQ2e-mtp (72 GB, default), 3 = oQ3e-mtp (86 GB)
# needs: Apple Silicon, 128 GB RAM, oMLX 0.8.2 in /Applications (https://github.com/jundot/omlx/releases), `pip install -U huggingface_hub`
set -e; V=${1:-2}; ID=Qwen3.8-Flash-Next-Uncensored-oQ${V}e-mtp; REPO=damianpy/$ID-MLX; DIR=~/.omlx/models/$ID; HERE=$(cd "$(dirname "$0")" && pwd)
[ "$(uname -m)" = arm64 ] || { echo "Apple Silicon only"; exit 1; }
RAM=$(( $(sysctl -n hw.memsize) / 1073741824 )); [ $RAM -ge 120 ] || echo "WARNING: ${RAM} GB RAM; this build is sized for 128 GB"
[ -d /Applications/oMLX.app ] || { echo "Install oMLX 0.8.2 first: https://github.com/jundot/omlx/releases"; exit 1; }
FREE=$(df -g ~ | awk 'NR==2{print $4}'); [ $FREE -ge 100 ] || { echo "Need ~100 GB free disk, have ${FREE} GB"; exit 1; }
echo "1/4 weights -> $DIR"; hf download $REPO --local-dir $DIR
echo "2/4 oMLX model settings (KV affine4 4-bit, MTP, 524k context, pinned + default)"
python3 - "$HERE/model-settings-entry.json" "$ID" <<'PY'
import json, os, sys, shutil, time
S = os.path.expanduser("~/.omlx/model_settings.json"); e = json.load(open(sys.argv[1])); mid = sys.argv[2]
d = json.load(open(S)) if os.path.exists(S) else {"version": 1, "models": {}}
if os.path.exists(S): shutil.copy(S, S + time.strftime(".bak-%Y%m%d-%H%M%S"))
for v in d["models"].values(): v["is_default"] = False
d["models"][mid] = e; open(S, "w").write(json.dumps(d, indent=2) + "\n"); print("  written", S)
PY
echo "3/4 memory: oMLX ceiling 108 GB, hot cache 2 GB (Settings > Memory in the oMLX app), and cap GPU wired memory so a too-long prompt fails instead of freezing the Mac:"
echo "    sudo sysctl iogpu.wired_limit_mb=110592"
echo "4/4 restart oMLX, then:  python3 $HERE/speed.py $ID 4096:1:256 131072:1:256   (export OMLX_API_KEY=<your oMLX API key> if you set one)"
