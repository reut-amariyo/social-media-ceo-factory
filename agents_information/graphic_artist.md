# 🎨 Graphic Artist Agent — Image Generator

## What it does

Generates a branded image for your social media post using **Stable Diffusion XL** running locally on your machine. No API needed — it's 100% free and private.

## How it works

1. Takes the context from your selected idea + generated drafts
2. Builds an image prompt (professional, modern, tech aesthetic)
3. Generates a 1024x1024 image with SDXL
4. Saves to the run's output folder

## Auto-detected GPU

| Platform | GPU Backend | Performance |
|----------|-------------|-------------|
| macOS (M1/M2/M3/M4) | Apple MPS | ~2 min per image |
| Windows/Linux (NVIDIA) | CUDA | ~30 sec per image |
| No GPU | CPU | ~10 min (slow) |

The agent auto-detects your hardware — no configuration needed.

## Installation (optional)

Image generation is **optional**. If not installed, the agent skips gracefully.

To enable:
```bash
pip install torch diffusers transformers accelerate
```

> ⚠️ First run downloads the SDXL model (~7GB). After that it's cached locally.

## Image style

- Professional, modern 3D render style
- Clean, futuristic, corporate tech aesthetic
- Colors: Deep blue, white, subtle gold accents
- No text in the image (you add text in your social media tool)

## Output

Saves to: `outputs/YYYY-MM-DD_HH-MM/post_image_XXXX.png`
