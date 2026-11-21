# AI Watermark Remover

**What it is.** Detects and removes AI watermarks and provenance metadata from images and video

**Verdict: works.** Provenance identification works well on CPU (correct platform on 5/6 real AI images, C2PA/EXIF/XMP/TC260/visible marks, 1-3 s and 120 MB per image); the removal half was deliberately not run and should not be deployed from China, where supplying AI-label removal tools is restricted.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

