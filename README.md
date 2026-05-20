# 🏭 Personal Branding Factory# Lior Pozin's Personal Branding Factory



An AI-powered system that generates personalized social media content for **any** CEO, founder, or thought leader. Set up your profile once, and the system scouts trends, generates ideas, writes posts in your voice, validates quality, and creates images — all automatically.An agentic AI system that generates personalized social media content for **Lior Pozin** — CEO of AutoDS (acquired by Fiverr), BuildYourStore.ai, CreateUGC.AI.



---Built by Tal. Operated by Reut.



## ⚡ Quick Start (5 minutes)---



### 1. Clone the repo## Quick Start



```bash### 1. Install dependencies

git clone https://github.com/reut-amariyo/social-media-ceo-factory.git

cd social-media-ceo-factory```bash

```pip install -r requirements.txt

```

### 2. Install dependencies

### 2. Set up your `.env` file

```bash

pip install -r requirements.txtCreate a `.env` file in the project root (copy from `.env.example`):

```

```

**Also install Ollama** (free local AI — required as fallback):SERPAPI_API_KEY=your_serpapi_key_here

- macOS/Linux: https://ollama.com/downloadXAI_API_KEY=your_grok_xai_key_here

- Windows: https://ollama.com/download/windowsOBSIDIAN_VAULT_PATH=/Users/reut/Documents/MyObsidianVault

OBSIDIAN_SYSTEM_DIR=the-system-v5

Then pull the model:```

```bash

ollama pull llama3### 3. Make sure Ollama is running

```

Open the Ollama app, then:

### 3. Run the setup wizard

```bash

```bashollama pull llama3

python setup_profile.py```

```

### 4. Run the factory

This asks for your name, company, topics, tone, stories, and expertise. Takes ~2 minutes. Creates `profile.yaml` (gitignored — your data stays private).

```bash

### 4. Run the factorypython main.py

```

```bash

python main.py---

```

## How It Works

Or use the desktop app:

```bashThe system runs 6 agents in sequence:

python app.py

``````

Load Context → Scout → Ideator → [Reut picks] → Creator → Validator → Graphic Artist → Save

---```



## 🔑 API Keys (Optional but Recommended)| Agent | What it does |

|-------|-------------|

The system works with **zero API keys** (uses Ollama locally), but it's faster with:| **Scout** | Searches Google + X for trending topics in Lior's focus areas |

| **Ideator** | Filters trends through Voice DNA, proposes 3 content angles |

| Key | What it does | Cost | How to get || **Human Checkpoint** | Reut picks her favorite idea |

|-----|-------------|------|-----------|| **Creator** | Writes drafts for X, LinkedIn, Instagram in Lior's exact voice |

| `XAI_API_KEY` | Grok-3 for fast LLM generation | Pay-per-use | https://console.x.ai || **Validator** | Gatekeeper — checks tone, vocabulary, punctuation, brand alignment |

| `SERPAPI_API_KEY` | Google search for trend scouting | 100 free/month | https://serpapi.com || **Graphic Artist** | Generates a branded image with Stable Diffusion XL (optional) |



Add them to your `.env` file (created during setup) or set as environment variables.---



---## Obsidian Vault Integration (ABC-TOM v5)



## 🧠 How It WorksThe system reads from and writes to your Obsidian vault:



```### What the system READS (your files — you control these)

Setup Profile → Scout → Ideator → [You pick] → Creator → Validator → Graphic Artist → Save

```| File | What it contains |

|------|-----------------|

| Agent | What it does || `C-core/voice-dna.md` | How Lior speaks — writing patterns, tone, vocabulary |

|-------|-------------|| `C-core/project-brief.md` | CEO identity, business context, focus areas |

| **Scout** | Scans 20+ tech news sources, Hacker News, X for trending topics || `C-core/icp-profile.md` | 3 audience segments (Investors, Entrepreneurs, Growth-Seekers) |

| **Ideator** | Filters trends through YOUR brand, proposes 5-7 content angles || `M-memory/learning-log.md` | What worked, what didn't, golden rules |

| **Human Checkpoint** | You pick your favorite idea || `M-memory/feedback.md` | Audience signals |

| **Creator** | Writes drafts for X, LinkedIn, Instagram in YOUR voice || `B-brain/content-samples/` | Past successful posts (used for style mimicking) |

| **Validator** | Quality control — checks tone, banned words, brand alignment |

| **Graphic Artist** | Generates a branded image with Stable Diffusion XL (local, free) |> **The system never edits these files.** You can update them anytime via Claude Desktop.

| **Analyst** | Learns from each run to improve future content |

### What the system WRITES (agent files — review and merge)

---

| File | What it contains |

## 💻 Platform Support|------|-----------------|

| `M-memory/learning-log-agent.md` | Agent-generated insights from post analysis |

| Platform | GUI App (`app.py`) | Terminal (`main.py`) || `O-output/[NN]-[slug]/copywriter-draft.md` | Generated drafts ready for your review |

|----------|-------------------|---------------------|

| **macOS** | ✅ Full support (Tkinter) | ✅ |---

| **Windows** | ✅ Works (Tkinter is built-in) | ✅ |

| **Linux** | ✅ Works (install `python3-tk`) | ✅ |## Reut's Daily Workflow



> **Windows/Linux users**: Image generation uses CUDA instead of Apple MPS. If you don't have a GPU, images are skipped gracefully.### Morning — Generate content



---```bash

python main.py

## 📁 Your Personal Brand "Brain" (Optional)```



For deeper personalization, create an Obsidian vault with:1. The system reads your latest vault files (voice-dna, learning-log, past posts)

2. Scouts trending topics on Google + X

```3. Proposes 3 content ideas — **you pick your favorite**

your-vault/4. Generates multi-platform drafts in Lior's voice

├── voice-dna.md          # How you write — patterns, tone, vocabulary5. Validates against Gatekeeper rules

├── project-brief.md      # Your business context6. Saves to `O-output/` in your vault

├── icp-profile.md        # Your target audience segments

├── learning-log.md       # What content worked/didn't### During the day — Work in Claude Desktop as usual

└── content-samples/      # Past successful posts (for style mimicking)

```Edit `voice-dna.md`, update `learning-log.md`, create posts — whatever you normally do. The agents never touch your files.



Set the path in `.env`:### Review agent insights

```

OBSIDIAN_VAULT_PATH=/path/to/your/vaultOpen `M-memory/learning-log-agent.md` in Obsidian. It contains insights the Analyst agent extracted from post performance data.

```

To merge the good ones into your main learning log, tell Claude Desktop:

**Don't have an Obsidian vault?** No problem — the system works fine with just `profile.yaml`. The vault is an optional power-up for voice accuracy.

> "Read learning-log-agent.md. Promote the good insights to learning-log.md following The Loop protocol. Then clear the agent file."

---

### Review generated drafts

## 🔒 Privacy

1. Open `O-output/` in Obsidian

Your personal data **never** leaves your machine and is **never** committed to git:2. Find the latest numbered folder (e.g. `12-scaling-ai-pricing/`)

- `profile.yaml` — gitignored3. Open `copywriter-draft.md`

- `.env` — gitignored4. Edit it, apply your instincts

- `outputs/` — gitignored5. Save the final version as `final-post.md` in the same folder

- Obsidian vault contents — gitignored

---

---

## Project Structure

## 🛠️ Troubleshooting

```

| Issue | Fix |social-media-ceo-factory/

|-------|-----|├── main.py                          # Entry point — run this

| "No profile found" | Run `python setup_profile.py` |├── run_scout.py                     # Standalone scout runner (for testing)

| Ollama not found | Install from https://ollama.com and run `ollama pull llama3` |├── requirements.txt                 # Python dependencies

| Image generation skipped | Install: `pip install torch diffusers transformers accelerate` |├── .env                             # API keys + vault path (not in git)

| Slow generation | Set `XAI_API_KEY` in `.env` for fast cloud LLM |├── .gitignore

| X posts over 280 chars | Known issue — validator catches it and retries |│

├── core/

---│   ├── state.py                     # AgentState definition (shared memory)

│   └── orchestrator.py              # LangGraph workflow (agent flow)

## 📦 Project Structure│

├── branding_factory/

```│   └── agents/

├── setup_profile.py          # First-run wizard → creates profile.yaml│       ├── scout.py                 # Agent 1: Trend Scout (Google + Grok)

├── main.py                   # Terminal-based factory runner│       ├── ideator.py               # Agent 2: Brand Strategist

├── app.py                    # Desktop GUI (cross-platform Tkinter)│       ├── creator.py               # Agent 3: Copywriter

├── profile.yaml              # YOUR profile (gitignored)│       ├── validator.py             # Agent 4: Gatekeeper

├── .env                      # YOUR API keys (gitignored)│       ├── graphic_artist.py        # Agent 5: Image Generator (SDXL)

├── requirements.txt          # Python dependencies│       └── analyst.py               # Agent 6: Performance Analyst

├── branding_factory/│

│   └── agents/├── utils/

│       ├── scout.py          # Trend scouting (RSS + X + Hacker News)│   └── obsidian_io.py               # Obsidian vault reader/writer (ABC-TOM v5)

│       ├── ideator.py        # Idea generation + ranking│

│       ├── creator.py        # Multi-platform copywriting└── outputs/                         # Local fallback for generated content

│       ├── validator.py      # Quality gatekeeper```

│       ├── graphic_artist.py # Image generation (SDXL)

│       └── analyst.py        # Post-run learning---

├── core/

│   └── orchestrator.py       # LangGraph workflow engine## API Keys

└── utils/

    └── obsidian_io.py        # Obsidian vault integration| Service | What it does | Get yours at |

```|---------|-------------|-------------|

| **SerpAPI** | Google Search results | https://serpapi.com |

---| **Grok (X API)** | Real-time X/Twitter trends | https://console.x.ai |

| **Ollama** | Local LLM (llama3) — free | https://ollama.com |

## 🤝 Built By

---

Built by **Tal** & **Reut** — powered by LangGraph, Ollama, Grok, and Stable Diffusion XL.

## The Safety Rule

```
READ  → Reut's files (C-core, M-memory, B-brain)     ← Reut owns these
WRITE → Agent files (learning-log-agent.md, O-output/) ← Agents own these
```

The agents **never modify** Reut's working files. All agent output goes to separate files that Reut reviews and merges when she's ready. This follows the ABC-TOM "Loop" philosophy: agents propose, the human decides.
