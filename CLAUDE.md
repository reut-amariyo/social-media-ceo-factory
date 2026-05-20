# CLAUDE.md — AI Assistant Instructions

> Give this file to any AI (Claude, ChatGPT, Copilot) to help you install and use the system.

---

## What Is This?

This is a **Personal Branding Factory** — an AI system that generates social media content (X, LinkedIn, Instagram) tailored to YOUR personal brand. It scouts trending topics, generates ideas, writes posts in your voice, validates quality, and creates images.

---

## First-Time Setup

### Prerequisites

1. **Python 3.10+** installed
2. **Ollama** installed (https://ollama.com) — free local AI
3. **Git** installed

### Installation Steps

```bash
# 1. Clone the repo
git clone https://github.com/reut-amariyo/social-media-ceo-factory.git
cd social-media-ceo-factory

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# 3. Install Python packages
pip install -r requirements.txt

# 4. Install and start Ollama, then pull the model
ollama pull llama3

# 5. Run the profile setup wizard
python setup_profile.py
```

The setup wizard asks for:
- Your name, company, role, industry
- Topics you post about (3-6)
- Your writing tone (adjectives)
- Career milestones (3-5 stories)
- Expertise areas
- Words you never use / love to use

This creates `profile.yaml` — your personal brand config.

### Optional: API Keys for Better Performance

Create/edit `.env` in the project root:
```
XAI_API_KEY=your_key_here      # Grok-3 (fast cloud LLM) — https://console.x.ai
SERPAPI_API_KEY=your_key_here   # Google search (100 free/month) — https://serpapi.com
```

Without these, the system uses Ollama (slower but 100% free).

---

## Running the System

### Terminal mode (recommended for first run):
```bash
python main.py
```

### Desktop GUI:
```bash
python app.py
```

### What happens during a run:
1. **Scout** scans 20+ news sources + X for trends (2-3 min)
2. **Ideator** proposes 5-7 content ideas based on your brand
3. **You pick** your favorite idea
4. **Creator** writes drafts for X, LinkedIn, Instagram
5. **Validator** checks quality (retries up to 3x if needed)
6. **Graphic Artist** generates an image (if torch/diffusers installed)
7. **Output** saved to `outputs/` folder

---

## Optional: Obsidian Vault for Deep Personalization

If you want the AI to deeply learn your writing style, create these files in an Obsidian vault (or any folder):

| File | What to put in it |
|------|------------------|
| `voice-dna.md` | How you write — sentence patterns, words you use, tone rules |
| `project-brief.md` | Your business story, achievements, what makes you unique |
| `icp-profile.md` | Who your audience is (segments, pain points, what they want) |
| `learning-log.md` | Notes on what content worked/didn't work |
| `content-samples/` | Folder with 5-10 of your best past posts |

Then set in `.env`:
```
OBSIDIAN_VAULT_PATH=/path/to/your/vault
```

**This is optional.** The system works with just `profile.yaml`.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| "No profile found" | Run `python setup_profile.py` |
| Ollama connection error | Make sure Ollama app is running (`ollama serve`) |
| Very slow generation | Add `XAI_API_KEY` to `.env` for cloud LLM |
| Image generation fails | Install `pip install torch diffusers transformers accelerate` |
| Windows: tkinter missing | Reinstall Python with "tcl/tk" checkbox selected |
| Linux: tkinter missing | `sudo apt install python3-tk` |

---

## Editing Your Profile

Edit `profile.yaml` directly (YAML format) or re-run:
```bash
python setup_profile.py
```

---

## Architecture (for developers)

- **LangGraph** orchestrates the agent pipeline (state machine)
- **Ollama** (local) or **Grok-3** (cloud) for text generation
- **Stable Diffusion XL** for image generation (local GPU)
- **SerpAPI** for Google search (optional)
- **RSS + BeautifulSoup** for news scraping (free, no key needed)
- All personal data stays local (`.gitignore` protects everything)
