import os
import torch


def run_graphic_agent(state: dict):
    """
    Agent 4: The Graphic Artist
    - Generates a branded image for the social media post
    - Uses Stable Diffusion XL on Apple M4 MPS (local, free)
    """
    print("--- 🎨 AGENT: GRAPHIC ARTIST (Generating Image) ---")

    ceo = state.get("ceo_profile", {})
    ceo_name = ceo.get("name", "a CEO")
    company = ceo.get("company", "")

    # Use the selected idea + LinkedIn draft to describe the image
    selected_idea = state.get("selected_idea", "")
    drafts = state.get("post_drafts", {})
    li_post = drafts.get("linkedin", "")
    context = selected_idea[:150] if selected_idea else li_post[:150]

    image_prompt = (
        f"Professional, modern 3D render style illustration for a tech CEO's social media post. "
        f"Topic: {context}. "
        f"Style: Clean, futuristic, corporate tech aesthetic. "
        f"Colors: Deep blue, white, subtle gold accents. "
        f"No text in the image."
    )
    print(f"   🖼️  Prompt: {image_prompt[:100]}...")

    try:
        from diffusers import StableDiffusionXLPipeline

        device = "mps"  # Apple M4 Metal Performance Shaders
        model_id = "stabilityai/stable-diffusion-xl-base-1.0"

        print("   ⏳ Loading SDXL model (this may take a moment on first run)...")
        pipe = StableDiffusionXLPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            variant="fp16",
            use_safetensors=True,
        )
        pipe = pipe.to(device)

        print("   🎨 Generating image...")
        image = pipe(
            prompt=image_prompt,
            num_inference_steps=25,
            guidance_scale=7.5,
        ).images[0]

        # Save to outputs folder
        os.makedirs("outputs", exist_ok=True)
        filename = f"post_image_{os.urandom(4).hex()}.png"
        path = os.path.join("outputs", filename)
        image.save(path)

        print(f"   ✅ Image saved to: {path}")
        return {"image_path": path}

    except ImportError:
        print("   ⚠️  diffusers not installed. Skipping image generation.")
        print("   💡 Install with: pip install diffusers transformers accelerate")
        return {"image_path": ""}
    except Exception as e:
        print(f"   ⚠️  Image generation failed: {e}")
        print("   💡 Continuing without image — you can generate one manually.")
        return {"image_path": ""}