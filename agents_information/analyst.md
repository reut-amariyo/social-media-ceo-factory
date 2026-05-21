# 📊 Analyst Agent — Post-Run Learning

## What it does

The Analyst runs **after** the full pipeline completes. It analyzes what happened during the run and extracts actionable insights for future content generation.

## What it analyzes

- Which idea was selected and why
- Validation scores (what scored high/low)
- How many retries were needed
- What feedback the Validator gave
- Patterns in successful vs rejected drafts

## Output

Writes insights to `learning-log-agent.md` (if Obsidian vault configured) with:
- **Golden Rules** — patterns that work for your brand
- **Anti-patterns** — things to avoid next time
- **Content signals** — what topics/hooks performed best

## How it improves future runs

The Ideator and Creator read the learning log on subsequent runs. Over time:
- Ideas get more aligned with what works
- Drafts avoid past mistakes
- Voice accuracy improves with each iteration

## Safety

The Analyst **never** edits your personal files. It writes to a separate agent file that you can review and merge when ready.

## LLM used

- **Primary:** Grok-3 (fast, remote)
- **Fallback:** Ollama Llama 3 (local)
