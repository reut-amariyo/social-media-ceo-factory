# ✍️ Creator Agent — Copywriter

## What it does

The Creator takes your selected idea and writes **multi-platform drafts** in your exact voice. It generates content for X (Twitter), LinkedIn, and Instagram simultaneously.

## Platforms it writes for

| Platform | Format | Constraints |
|----------|--------|------------|
| **X (Twitter)** | Short hook + insight | Max 280 characters |
| **LinkedIn** | Long-form with fold | 1-line hook → blank line → 3-5 paragraphs |
| **Instagram** | 5-slide carousel + caption | Slide 1: hook, Slides 2-4: insights, Slide 5: CTA |

## How it uses your profile

- **`tone`** → Overall voice (e.g., "Direct, sharp, builder-mindset")
- **`banned_words`** → Words it will NEVER use (auto-stripped after generation)
- **`preferred_words`** → Words it favors in output
- **`stories`** / **`expertise`** → Specific details to weave in

From Obsidian (optional):
- **`voice-dna.md`** → Detailed sentence patterns, punctuation rules, paragraph structure
- **Past posts** → Few-shot style mimicking

## Writing rules it follows

- Hook is always ONE line (never a paragraph)
- 1-3 lines per paragraph max
- Time anchoring: specific time references ("In 2015" not "years ago")
- Proof-through-specifics: never claims, always evidence
- The Rule of 3: numbered lists always use exactly 3 items
- Eye-level tone: never condescending, never guru energy

## Self-check loop

After generating drafts, the Creator **evaluates its own work**:
1. Checks for banned words
2. Checks punctuation (no em dashes, no smart quotes)
3. Checks hook length
4. Checks for condescending tone
5. If issues found → rewrites automatically

## Banned word auto-removal

Even if the LLM ignores instructions, a **deterministic post-processing step** replaces banned words:
- "very" → "really"
- "leverage" → "use"
- "optimize" → "improve"
- "innovative" → "new"
- etc.

## LLM used

- **Primary:** Grok-3 (fast, remote)
- **Fallback:** Ollama Llama 3 (local)
