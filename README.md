# 🏭 Personal Branding Factory# 🏭 Personal Branding Factory# Lior Pozin's Personal Branding Factory



An AI-powered system that generates personalized social media content for **you** — whether you're a CEO, founder, creator, or thought leader. Set up your profile once, and the system scouts trends, generates ideas, writes posts in your voice, validates quality, and creates images — all automatically.



---An AI-powered system that generates personalized social media content for **any** CEO, founder, or thought leader. Set up your profile once, and the system scouts trends, generates ideas, writes posts in your voice, validates quality, and creates images — all automatically.An agentic AI system that generates personalized social media content for **Lior Pozin** — CEO of AutoDS (acquired by Fiverr), BuildYourStore.ai, CreateUGC.AI.



## ⚡ Quick Start (5 minutes)



### 1. Clone the repo---Built by Tal. Operated by Reut.



```bash

git clone https://github.com/reut-amariyo/social-media-ceo-factory.git

cd social-media-ceo-factory## ⚡ Quick Start (5 minutes)---

```



### 2. Install dependencies

### 1. Clone the repo## Quick Start

```bash

pip install -r requirements.txt

```

```bash### 1. Install dependencies

### 3. Install Ollama (free local AI)

git clone https://github.com/reut-amariyo/social-media-ceo-factory.git

- **macOS / Linux:** https://ollama.com/download

- **Windows:** https://ollama.com/download/windowscd social-media-ceo-factory```bash



Then pull the model:```pip install -r requirements.txt

```bash

ollama pull llama3```

```

### 2. Install dependencies

### 4. Run the setup wizard

### 2. Set up your `.env` file

```bash

python setup_profile.py```bash

```

pip install -r requirements.txtCreate a `.env` file in the project root (copy from `.env.example`):

This creates your `profile.yaml` with:

- Your name, company, role, industry```

- Topics you post about

- Your writing tone```

- Your career stories & expertise

- Content focus keywords (what the Scout looks for)**Also install Ollama** (free local AI — required as fallback):SERPAPI_API_KEY=your_serpapi_key_here

- X accounts to monitor

- Words you never/always use- macOS/Linux: https://ollama.com/downloadXAI_API_KEY=your_grok_xai_key_here



Takes ~2 minutes. Your data stays private (gitignored).- Windows: https://ollama.com/download/windowsOBSIDIAN_VAULT_PATH=/Users/reut/Documents/MyObsidianVault



### 5. (Optional) Set up API keysOBSIDIAN_SYSTEM_DIR=the-system-v5



Copy the example and add your keys:Then pull the model:```

```bash

cp .env.example .env```bash

```

ollama pull llama3### 3. Make sure Ollama is running

Edit `.env`:

``````

XAI_API_KEY=your_key_here       # Grok-3 (fast cloud LLM) — https://console.x.ai

SERPAPI_API_KEY=your_key_here    # Google Search (100 free/month) — https://serpapi.comOpen the Ollama app, then:

```

### 3. Run the setup wizard

> **No keys?** The system works without them — uses Ollama locally (slower but free).

```bash

### 6. Run the factory

```bashollama pull llama3

**Terminal:**

```bashpython setup_profile.py```

python main.py

``````



**Desktop App (GUI):**### 4. Run the factory

- macOS: Double-click `BrandingFactory.app` or run `bash launch_app.sh`

- Windows: Double-click `BrandingFactory.bat`This asks for your name, company, topics, tone, stories, and expertise. Takes ~2 minutes. Creates `profile.yaml` (gitignored — your data stays private).

- Any: `python app.py`

```bash

---

### 4. Run the factorypython main.py

## 🧠 How It Works

```

```

Your Profile → Scout → Ideator → [You pick] → Creator → Validator → Graphic Artist → Save```bash

```

python main.py---

| Agent | What it does |

|-------|-------------|```

| **Scout** | Scans 20+ news sources, Hacker News, and X for trending topics in YOUR focus areas |

| **Ideator** | Filters trends through your brand, proposes 5-7 content angles with hooks |## How It Works

| **Human Checkpoint** | You pick your favorite idea |

| **Creator** | Writes drafts for X, LinkedIn, Instagram in YOUR voice |Or use the desktop app:

| **Validator** | Quality gatekeeper — checks tone, banned words, brand alignment. Retries up to 3x |

| **Graphic Artist** | Generates a branded image with Stable Diffusion XL (local, free) |```bashThe system runs 6 agents in sequence:

| **Analyst** | Learns from each run to improve future content |

python app.py

> For detailed documentation on each agent, see the [`agents_information/`](agents_information/) folder.

``````

---

Load Context → Scout → Ideator → [Reut picks] → Creator → Validator → Graphic Artist → Save

## 🎯 How the System Learns Your Voice

---```

The system knows who you are and how to write for you from **two sources** (use one or both):



### Option A: `profile.yaml` (Quick — Required)

## 🔑 API Keys (Optional but Recommended)| Agent | What it does |

Created by `python setup_profile.py`. Contains your basic brand DNA:

- Name, company, role, industry|-------|-------------|

- Topics, tone, stories, expertise

- Banned/preferred vocabularyThe system works with **zero API keys** (uses Ollama locally), but it's faster with:| **Scout** | Searches Google + X for trending topics in Lior's focus areas |



**This is enough to get started.** The AI uses your profile to generate content that only YOU could write.| **Ideator** | Filters trends through Voice DNA, proposes 3 content angles |



### Option B: Obsidian Vault (Deep — Optional Power-Up)| Key | What it does | Cost | How to get || **Human Checkpoint** | Reut picks her favorite idea |



For deeper voice accuracy, you can create a "brand brain" folder. This gives the AI examples of your actual writing style, audience info, and performance history.|-----|-------------|------|-----------|| **Creator** | Writes drafts for X, LinkedIn, Instagram in Lior's exact voice |



#### How to set up your brand brain:| `XAI_API_KEY` | Grok-3 for fast LLM generation | Pay-per-use | https://console.x.ai || **Validator** | Gatekeeper — checks tone, vocabulary, punctuation, brand alignment |



1. Create a folder anywhere on your computer (or use Obsidian):| `SERPAPI_API_KEY` | Google search for trend scouting | 100 free/month | https://serpapi.com || **Graphic Artist** | Generates a branded image with Stable Diffusion XL (optional) |

```

my-brand-brain/

├── C-core/

│   ├── voice-dna.mdAdd them to your `.env` file (created during setup) or set as environment variables.---

│   ├── project-brief.md

│   └── icp-profile.md

├── M-memory/

│   └── learning-log.md---## Obsidian Vault Integration (ABC-TOM v5)

└── B-brain/

    └── content-samples/

```

## 🧠 How It WorksThe system reads from and writes to your Obsidian vault:

2. Add the path to your `.env`:

```

OBSIDIAN_VAULT_PATH=/path/to/my-brand-brain

OBSIDIAN_SYSTEM_DIR=.```### What the system READS (your files — you control these)

```

Setup Profile → Scout → Ideator → [You pick] → Creator → Validator → Graphic Artist → Save

#### What to put in each file:

```| File | What it contains |

| File | What to write | Example |

|------|--------------|---------||------|-----------------|

| **`voice-dna.md`** | How you write. Sentence patterns, tone rules, vocabulary. | "I write short sentences. Max 2 lines per paragraph. I use 'real', 'build', 'ship'. I never say 'leverage' or 'innovative'." |

| **`project-brief.md`** | Your business context. What you do, what makes you unique. | "I'm the CEO of X. We do Y. I built it from $0 to $Z. My unique angle is..." || Agent | What it does || `C-core/voice-dna.md` | How Lior speaks — writing patterns, tone, vocabulary |

| **`icp-profile.md`** | Your target audience. Who reads your posts? | "Segment 1: Early-stage founders (pain: hiring). Segment 2: Tech leaders (pain: scaling)." |

| **`learning-log.md`** | What content worked/didn't. Rules you've learned. | "Posts with specific numbers get 3x engagement. Questions in hooks work better than statements." ||-------|-------------|| `C-core/project-brief.md` | CEO identity, business context, focus areas |

| **`content-samples/`** | 5-10 of your best past posts (one per `.md` file). | Copy-paste your top LinkedIn/X posts here. The AI mimics this style. |

| **Scout** | Scans 20+ tech news sources, Hacker News, X for trending topics || `C-core/icp-profile.md` | 3 audience segments (Investors, Entrepreneurs, Growth-Seekers) |

> **Tip:** Ask any AI assistant: *"Read my CLAUDE.md file and help me fill in my brand brain files."*

| **Ideator** | Filters trends through YOUR brand, proposes 5-7 content angles || `M-memory/learning-log.md` | What worked, what didn't, golden rules |

---

| **Human Checkpoint** | You pick your favorite idea || `M-memory/feedback.md` | Audience signals |

## 📁 Output — Reviewing Your Results

| **Creator** | Writes drafts for X, LinkedIn, Instagram in YOUR voice || `B-brain/content-samples/` | Past successful posts (used for style mimicking) |

Every run saves a **complete folder** you can browse anytime:

| **Validator** | Quality control — checks tone, banned words, brand alignment |

```

outputs/| **Graphic Artist** | Generates a branded image with Stable Diffusion XL (local, free) |> **The system never edits these files.** You can update them anytime via Claude Desktop.

└── 2026-05-21_09-30/

    ├── run_summary.md      # Date, scores, selected idea, metadata| **Analyst** | Learns from each run to improve future content |

    ├── ideas.md            # All 5-7 ideas proposed (browse them later)

    ├── drafts.md           # Final X + LinkedIn + Instagram drafts### What the system WRITES (agent files — review and merge)

    ├── trends.md           # What the Scout found (full trend report)

    └── post_image_*.png    # Generated image (if any)---

```

| File | What it contains |

- Open `drafts.md` → copy your favorite draft → post it

- Open `ideas.md` → find ideas you didn't use → save for later## 💻 Platform Support|------|-----------------|

- Open `trends.md` → see what's trending in your space today

- Compare runs across days to see what topics keep appearing| `M-memory/learning-log-agent.md` | Agent-generated insights from post analysis |



---| Platform | GUI App (`app.py`) | Terminal (`main.py`) || `O-output/[NN]-[slug]/copywriter-draft.md` | Generated drafts ready for your review |



## 💻 Platform Support|----------|-------------------|---------------------|



| Platform | GUI App | Terminal | Image Generation || **macOS** | ✅ Full support (Tkinter) | ✅ |---

|----------|---------|---------|-----------------|

| **macOS** | ✅ Double-click `.app` | ✅ `python main.py` | ✅ Apple MPS (M1/M2/M3/M4) || **Windows** | ✅ Works (Tkinter is built-in) | ✅ |

| **Windows** | ✅ Double-click `.bat` | ✅ `python main.py` | ✅ NVIDIA CUDA |

| **Linux** | ✅ `python app.py` | ✅ `python main.py` | ✅ NVIDIA CUDA || **Linux** | ✅ Works (install `python3-tk`) | ✅ |## Reut's Daily Workflow



> No GPU? Image generation is skipped gracefully. Everything else works fine.



---> **Windows/Linux users**: Image generation uses CUDA instead of Apple MPS. If you don't have a GPU, images are skipped gracefully.### Morning — Generate content



## 🔑 API Keys



| Service | What it does | Cost | Required? |---```bash

|---------|-------------|------|-----------|

| **Ollama** | Local LLM (Llama 3) | Free | Yes (install from ollama.com) |python main.py

| **Grok (XAI_API_KEY)** | Fast cloud LLM for all agents | Pay-per-use | No — falls back to Ollama |

| **SerpAPI (SERPAPI_API_KEY)** | Google Search for trend scouting | 100 free/month | No — Scout uses RSS without it |## 📁 Your Personal Brand "Brain" (Optional)```



---



## 🔒 Privacy & SecurityFor deeper personalization, create an Obsidian vault with:1. The system reads your latest vault files (voice-dna, learning-log, past posts)



Your personal data **never** leaves your machine and is **never** committed to git:2. Scouts trending topics on Google + X



| What | Protected by |```3. Proposes 3 content ideas — **you pick your favorite**

|------|-------------|

| `profile.yaml` | `.gitignore` |your-vault/4. Generates multi-platform drafts in Lior's voice

| `.env` (API keys) | `.gitignore` |

| `outputs/` (all generated content) | `.gitignore` |├── voice-dna.md          # How you write — patterns, tone, vocabulary5. Validates against Gatekeeper rules

| Brand brain / Obsidian vault | `.gitignore` |

├── project-brief.md      # Your business context6. Saves to `O-output/` in your vault

---

├── icp-profile.md        # Your target audience segments

## 🛠️ Troubleshooting

├── learning-log.md       # What content worked/didn't### During the day — Work in Claude Desktop as usual

| Issue | Fix |

|-------|-----|└── content-samples/      # Past successful posts (for style mimicking)

| "No profile found" | Run `python setup_profile.py` |

| Ollama not found | Install from https://ollama.com, then `ollama pull llama3` |```Edit `voice-dna.md`, update `learning-log.md`, create posts — whatever you normally do. The agents never touch your files.

| Image generation skipped | `pip install torch diffusers transformers accelerate` |

| Slow generation | Add `XAI_API_KEY` to `.env` for fast cloud LLM |

| X posts over 280 chars | Validator catches this and retries automatically |

| Windows: tkinter error | Reinstall Python with "tcl/tk" checkbox |Set the path in `.env`:### Review agent insights

| Linux: tkinter missing | `sudo apt install python3-tk` |

```

---

OBSIDIAN_VAULT_PATH=/path/to/your/vaultOpen `M-memory/learning-log-agent.md` in Obsidian. It contains insights the Analyst agent extracted from post performance data.

## 📦 Project Structure

```

```

├── setup_profile.py              # First-run wizard → creates profile.yamlTo merge the good ones into your main learning log, tell Claude Desktop:

├── main.py                       # Terminal runner

├── app.py                        # Desktop GUI (cross-platform)**Don't have an Obsidian vault?** No problem — the system works fine with just `profile.yaml`. The vault is an optional power-up for voice accuracy.

├── BrandingFactory.app/          # macOS double-click launcher

├── BrandingFactory.bat           # Windows double-click launcher> "Read learning-log-agent.md. Promote the good insights to learning-log.md following The Loop protocol. Then clear the agent file."

├── launch_app.sh                 # macOS/Linux quick launch script

├── profile.yaml                  # YOUR profile (gitignored)---

├── .env                          # YOUR API keys (gitignored)

├── .env.example                  # Template for .env### Review generated drafts

├── requirements.txt              # Python dependencies

├── CLAUDE.md                     # AI-readable setup guide## 🔒 Privacy

├── agents_information/           # Detailed docs for each agent

├── branding_factory/1. Open `O-output/` in Obsidian

│   └── agents/

│       ├── scout.py              # Trend scouting (RSS + X + HN)Your personal data **never** leaves your machine and is **never** committed to git:2. Find the latest numbered folder (e.g. `12-scaling-ai-pricing/`)

│       ├── ideator.py            # Idea generation + ranking

│       ├── creator.py            # Multi-platform copywriting- `profile.yaml` — gitignored3. Open `copywriter-draft.md`

│       ├── validator.py          # Quality gatekeeper

│       ├── graphic_artist.py     # Image generation (SDXL)- `.env` — gitignored4. Edit it, apply your instincts

│       └── analyst.py            # Post-run learning

├── core/- `outputs/` — gitignored5. Save the final version as `final-post.md` in the same folder

│   └── orchestrator.py           # LangGraph workflow engine

├── utils/- Obsidian vault contents — gitignored

│   └── obsidian_io.py            # Vault integration (optional)

└── outputs/                      # Generated content (gitignored)---

```

---

---

## Project Structure

## 🤝 Credits

## 🛠️ Troubleshooting

Built by **Tal** — powered by LangGraph, Ollama, Grok, and Stable Diffusion XL.

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
