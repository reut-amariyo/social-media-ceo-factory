# 🔍 Scout Agent — Tech Pulse Radar

## What it does

The Scout is the first agent in the pipeline. It scans multiple news sources in parallel to find **trending topics** relevant to your content focus areas.

## Sources it scans

| Source | Type | What it finds |
|--------|------|--------------|
| The Verge AI | RSS | Breaking AI news |
| TechCrunch AI | RSS | Startup/VC AI coverage |
| Wired AI | RSS | Long-form AI analysis |
| MIT Technology Review | RSS | Research-level insights |
| OpenAI Blog | RSS | Product launches, research |
| Anthropic News | Scrape | Claude updates, safety research |
| Google AI / DeepMind | RSS | Model releases, research |
| Microsoft AI | RSS | Enterprise AI features |
| Meta AI | RSS | Open-source models |
| AWS AI | RSS | Cloud AI services |
| Hugging Face | RSS + API | Papers, model releases |
| Hacker News | API | Top stories with high engagement |
| X (Twitter) via Grok | LLM | Real-time trending posts |
| **Your custom sources** | RSS | Whatever you add in `profile.yaml` |

## How it uses your profile

From `profile.yaml`:
- **`topics`** → General filter for relevance
- **`content_focus`** → Specific keywords to filter news items
- **`custom_sources`** → Extra RSS feeds you add (your industry)
- **`x_accounts`** → People the Scout monitors on X

## Output

A structured trend report with:
1. **AI Company News** (3-6 items) — what big companies just launched/announced
2. **Top X Posts** (3-6 items) — highest engagement posts with intent analysis

## Configuration

Add custom sources in `profile.yaml`:
```yaml
content_focus:
  - AI agents
  - developer tools
  - your keywords here

custom_sources:
  - name: my_industry_feed
    url: https://example.com/feed.xml
    type: rss

x_accounts:
  - username1
  - username2
```

## Dependencies

- `feedparser` — RSS parsing
- `beautifulsoup4` — Web scraping
- `requests` — HTTP
- `openai` — Grok API (for X monitoring, optional)
