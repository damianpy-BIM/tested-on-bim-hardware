#!/usr/bin/env python3
"""Does the umT5-XXL TextEncoder return a fresh tensor per call, or a reused buffer?

Run3 anomaly: with all 3 prompts batch-encoded up front, the SECOND clip came out with the
THIRD prompt's content while the first and third were right. If the encoder returns a view of
one shared output buffer, embeds[0..2] all alias the last-written content — which would need a
second mechanism to explain prompt 1 being right, so this test checks the buffer hypothesis
directly: data_ptr equality + content drift after encoding a later prompt.
"""
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTORCH_MPS_HIGH_WATERMARK_RATIO", "0.0")
sys.path.insert(0, str(Path(__file__).resolve().parent / "repo"))

import torch
from fastframes.wan.text_encoder import TextEncoder

root = Path(os.path.expanduser("~/Downloads/fastframes-mac/checkpoints"))
wan_dir = root / "Wan2.1-T2V-14B"
te = TextEncoder(str(wan_dir), 512).to(torch.device("mps"))
prompts = ["corgi skateboard tokyo neon", "woman piano jazz club rain warm zoom",
           "aerial drone glass tower cranes sky"]
emb = [te([p])["prompt_embeds"] for p in prompts]
print("ptrs:", [hex(e.data_ptr()) for e in emb])
print("shared storage 0-2:", emb[0].untyped_storage().data_ptr() == emb[2].untyped_storage().data_ptr())
print("shared storage 1-2:", emb[1].untyped_storage().data_ptr() == emb[2].untyped_storage().data_ptr())
d12 = (emb[1].float() - emb[2].float()).abs().mean().item()
print("mean|embed1-embed2| after all encodes:", round(d12, 6))
# re-encode prompt 1 alone and compare to the stored embeds[1]
e1b = te([prompts[1]])["prompt_embeds"]
print("mean|embed1_stored - embed1_fresh|:", round((emb[1].float() - e1b.float()).abs().mean().item(), 6))
print("ALIAS_TEST_DONE")
