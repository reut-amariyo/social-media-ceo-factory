# 💡 Ideator Agent — Brand Strategist

## What it does

The Ideator takes the Scout's trend report and generates **5-7 content ideas** tailored to your personal brand. Each idea connects a trending topic to YOUR unique experience.

## How it works

1. Reads the trend report from Scout
2. Loads your Voice DNA, ICP profile, and learning log (if available)
3. Loads past successful posts (for style reference)
4. Generates 5-7 ideas with hooks
5. **Self-reflects** — ranks ideas by predicted performance
6. Returns the ranked list for you to choose from

## How it uses your profile

From `profile.yaml`:
- **`name`** + **`company`** → Personalizes ideas ("Only YOU can say this")
- **`topics`** → Ensures ideas match your content pillars
- **`tone`** → Shapes the hook style
- **`stories`** + **`expertise`** → Connects trends to your lived experience

From Obsidian vault (optional):
- **`voice-dna.md`** → Deep writing patterns
- **`icp-profile.md`** → Audience targeting
- **`learning-log.md`** → What worked before
- **`content-samples/`** → Past posts for style mimicking

## Output format

Each idea has:
```
IDEA [N]:
The idea: [One sentence connecting a trend to your experience]
Hook: [The scroll-stopping opening line]
```

## Self-reflection

After generating ideas, the Ideator ranks them by:
1. **Friction potential** — will it generate comments/debate?
2. **Uniqueness** — could ONLY you say this?
3. **Clarity** — is it immediately clear what the post is about?

## LLM used

- **Primary:** Grok-3 (if `XAI_API_KEY` set) — fast, remote
- **Fallback:** Ollama Llama 3 (local, slower)
