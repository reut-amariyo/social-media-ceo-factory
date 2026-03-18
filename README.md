# Lior Pozin's Personal Branding Factory

An agentic AI system that generates personalized social media content for **Lior Pozin** — CEO of AutoDS (acquired by Fiverr), BuildYourStore.ai, CreateUGC.AI.

Built by Tal. Operated by Reut.

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up your `.env` file

Create a `.env` file in the project root (copy from `.env.example`):

```
SERPAPI_API_KEY=your_serpapi_key_here
XAI_API_KEY=your_grok_xai_key_here
OBSIDIAN_VAULT_PATH=/Users/reut/Documents/MyObsidianVault
OBSIDIAN_SYSTEM_DIR=the-system-v5
```

### 3. Make sure Ollama is running

Open the Ollama app, then:

```bash
ollama pull llama3
```

### 4. Run the factory

```bash
python main.py
```

---

## How It Works

The system runs 6 agents in sequence:

```
Load Context → Scout → Ideator → [Reut picks] → Creator → Validator → Graphic Artist → Save
```

| Agent | What it does |
|-------|-------------|
| **Scout** | Searches Google + X for trending topics in Lior's focus areas |
| **Ideator** | Filters trends through Voice DNA, proposes 3 content angles |
| **Human Checkpoint** | Reut picks her favorite idea |
| **Creator** | Writes drafts for X, LinkedIn, Instagram in Lior's exact voice |
| **Validator** | Gatekeeper — checks tone, vocabulary, punctuation, brand alignment |
| **Graphic Artist** | Generates a branded image with Stable Diffusion XL (optional) |

---

## Obsidian Vault Integration (ABC-TOM v5)

The system reads from and writes to your Obsidian vault:

### What the system READS (your files — you control these)

| File | What it contains |
|------|-----------------|
| `C-core/voice-dna.md` | How Lior speaks — writing patterns, tone, vocabulary |
| `C-core/project-brief.md` | CEO identity, business context, focus areas |
| `C-core/icp-profile.md` | 3 audience segments (Investors, Entrepreneurs, Growth-Seekers) |
| `M-memory/learning-log.md` | What worked, what didn't, golden rules |
| `M-memory/feedback.md` | Audience signals |
| `B-brain/content-samples/` | Past successful posts (used for style mimicking) |

> **The system never edits these files.** You can update them anytime via Claude Desktop.

### What the system WRITES (agent files — review and merge)

| File | What it contains |
|------|-----------------|
| `M-memory/learning-log-agent.md` | Agent-generated insights from post analysis |
| `O-output/[NN]-[slug]/copywriter-draft.md` | Generated drafts ready for your review |

---

## Reut's Daily Workflow

### Morning — Generate content

```bash
python main.py
```

1. The system reads your latest vault files (voice-dna, learning-log, past posts)
2. Scouts trending topics on Google + X
3. Proposes 3 content ideas — **you pick your favorite**
4. Generates multi-platform drafts in Lior's voice
5. Validates against Gatekeeper rules
6. Saves to `O-output/` in your vault

### During the day — Work in Claude Desktop as usual

Edit `voice-dna.md`, update `learning-log.md`, create posts — whatever you normally do. The agents never touch your files.

### Review agent insights

Open `M-memory/learning-log-agent.md` in Obsidian. It contains insights the Analyst agent extracted from post performance data.

To merge the good ones into your main learning log, tell Claude Desktop:

> "Read learning-log-agent.md. Promote the good insights to learning-log.md following The Loop protocol. Then clear the agent file."

### Review generated drafts

1. Open `O-output/` in Obsidian
2. Find the latest numbered folder (e.g. `12-scaling-ai-pricing/`)
3. Open `copywriter-draft.md`
4. Edit it, apply your instincts
5. Save the final version as `final-post.md` in the same folder

---

## Project Structure

```
social-media-ceo-factory/
├── main.py                          # Entry point — run this
├── run_scout.py                     # Standalone scout runner (for testing)
├── requirements.txt                 # Python dependencies
├── .env                             # API keys + vault path (not in git)
├── .gitignore
│
├── core/
│   ├── state.py                     # AgentState definition (shared memory)
│   └── orchestrator.py              # LangGraph workflow (agent flow)
│
├── branding_factory/
│   └── agents/
│       ├── scout.py                 # Agent 1: Trend Scout (Google + Grok)
│       ├── ideator.py               # Agent 2: Brand Strategist
│       ├── creator.py               # Agent 3: Copywriter
│       ├── validator.py             # Agent 4: Gatekeeper
│       ├── graphic_artist.py        # Agent 5: Image Generator (SDXL)
│       └── analyst.py               # Agent 6: Performance Analyst
│
├── utils/
│   └── obsidian_io.py               # Obsidian vault reader/writer (ABC-TOM v5)
│
└── outputs/                         # Local fallback for generated content
```

---

## API Keys

| Service | What it does | Get yours at |
|---------|-------------|-------------|
| **SerpAPI** | Google Search results | https://serpapi.com |
| **Grok (X API)** | Real-time X/Twitter trends | https://console.x.ai |
| **Ollama** | Local LLM (llama3) — free | https://ollama.com |

---

## The Safety Rule

```
READ  → Reut's files (C-core, M-memory, B-brain)     ← Reut owns these
WRITE → Agent files (learning-log-agent.md, O-output/) ← Agents own these
```

The agents **never modify** Reut's working files. All agent output goes to separate files that Reut reviews and merges when she's ready. This follows the ABC-TOM "Loop" philosophy: agents propose, the human decides.
