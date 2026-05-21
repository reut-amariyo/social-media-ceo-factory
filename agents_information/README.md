# 📖 Agent Documentation

This folder contains detailed documentation for each agent in the Branding Factory pipeline.

## Agents (in execution order)

| # | Agent | File | Role |
|---|-------|------|------|
| 1 | [Scout](scout.md) | `branding_factory/agents/scout.py` | Trend intelligence gathering |
| 2 | [Ideator](ideator.md) | `branding_factory/agents/ideator.py` | Content idea generation |
| 3 | [Creator](creator.md) | `branding_factory/agents/creator.py` | Multi-platform copywriting |
| 4 | [Validator](validator.md) | `branding_factory/agents/validator.py` | Quality gatekeeper |
| 5 | [Graphic Artist](graphic_artist.md) | `branding_factory/agents/graphic_artist.py` | Image generation |
| 6 | [Analyst](analyst.md) | `branding_factory/agents/analyst.py` | Post-run learning |

## How they connect

```
Scout → feeds trends to → Ideator → you pick → Creator → Validator (loop up to 3x) → Graphic Artist → Save
```

Each agent receives the full pipeline state and adds its output to it. The orchestrator (`core/orchestrator.py`) manages the flow using LangGraph.
