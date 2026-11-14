# Qwen3.5-4B 3D coders on one NVIDIA V100 32 GB

Two 4B fine-tunes by [ccore](https://huggingface.co/ccore) (Apache-2.0) that write a complete Three.js page from one sentence:

| Model | What it writes | Our verdict |
|---|---|---|
| [ccore/Qwen3.5-4B-GLB-3D-Coder](https://huggingface.co/ccore/Qwen3.5-4B-GLB-3D-Coder) | a low-poly game asset with an **Export GLB** button (Godot, Blender, web) | works |
| [ccore/Qwen3.5-4B-3D-Coder](https://huggingface.co/ccore/Qwen3.5-4B-3D-Coder) | an architectural or landscape scene with its own camera controls | partly |

`generate.py` runs either model through llama.cpp, opens the page in headless Chromium, checks it (a valid glTF 2.0 binary
for `glb`, a drawn canvas with no page error for `scene`) and regenerates a failed page, up to 3 tries.

## Hardware and software
| | |
|---|---|
| GPU | 1 x NVIDIA Tesla V100 32 GB (sm_70), full offload (`-ngl 99`), flash attention on |
| Weights | Q4_K_M GGUF, 2.7 GB each |
| Engine | llama.cpp `llama-server`, 32k context |
| Browser check | Puppeteer 25.16 + chrome-headless-shell, SwiftShader WebGL, three 0.160.0 served locally |

## Measured
| Run | Prompt | Result | Tokens | Time | Decode speed |
|---|---|---|---|---|---|
| GLB coder, 14/11/2026 | "Create a low-poly delivery drone with four rotors" | GLB ok on try 1 (87 meshes, 170 KB) | 11 033 | 93.0 s | 118.6 tok/s |
| 3D Coder, 14/11/2026 | "A modern glass house with a flat roof, a deck and trees" | scene ok on try 1 | 7 720 | 66.2 s | 116.6 tok/s |
| GLB coder, `generate.py`, 14/11/2026 | "Create a mana potion" | GLB ok on try 1 (15 meshes, 53 KB) | 7 686 | 64.4 s | 119.3 tok/s |
| 3D Coder, `generate.py`, 14/11/2026 | "A small harbour with a lighthouse and wooden boats" | failed 3 of 3 tries (page errors, e.g. `Identifier 'door' has already been declared`) | 8 646-10 295 | 72.0-86.4 s | 117.6-120.1 tok/s |
| 3D Coder, 13/11/2026 | 3 prompts x 2 seeds x 2 settings, one shot, no retry | 2 of 8 pages ran without a code fix | 5-10k each | 56-135 s | 116-123 tok/s |

Speeds: 1 x V100 32 GB, Q4_K_M, llama.cpp, 32k context, batch 1, decode tokens per second.
VRAM for the 3D Coder: about 2.6 GiB at 24.5k context. The one-shot failures were small JavaScript errors (an addon class used
from the core module, a variable declared twice), which is why `generate.py` checks every page and tries again.

## Run it
```bash
npm install                                   # puppeteer + three, in this folder
export LLAMA_SERVER=/path/to/llama-server CUDA_VISIBLE_DEVICES=0
MODEL=/path/to/Qwen3.5-4B-GLB-3D-Coder-Q4_K_M.gguf python3 generate.py glb "Create a mana potion" --out out/potion
MODEL=/path/to/Qwen3.5-4B-3D-Coder-Q4_K_M.gguf    python3 generate.py scene "A small harbour with a lighthouse" --out out/harbour
```
Output: `scene.html` (open it in a browser), `preview.png`, `asset.glb` (glb mode), `meta.json` (tokens, time, checks).
Weights are not stored here: download the GGUF files from the Hugging Face pages above (Apache-2.0).
