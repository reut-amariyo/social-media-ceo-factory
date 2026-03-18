"""
Analyst Agent — Post-Performance Analysis
============================================
Analyzes engagement data and extracts Golden Rules.
Writes to learning-log-agent.md (safe — never touches Reut's learning-log.md).
"""

import ollama
from utils.obsidian_io import update_learning_log
from datetime import datetime


def run_analyst_agent(state: dict):
    """
    Agent 6: The Analyst
    - Analyzes engagement data from past posts
    - Extracts 'Golden Rules' for what works
    - Saves insights to learning-log-agent.md (safe — Reut merges when ready)
    """
    print("--- 📊 AGENT: ANALYST (Learning from Performance Data) ---")

    ceo = state.get("ceo_profile", {})
    ceo_name = ceo.get("name", "Lior Pozin")

    # In a full system, this would come from social media APIs
    # For now, it can be passed as engagement_data in state
    engagement_data = state.get("engagement_data", "")

    if not engagement_data:
        print("   ⚠️  No engagement data provided. Skipping analysis.")
        return {"learning_context": state.get("learning_context", "")}

    prompt = f"""You are a social media analytics expert for {ceo_name}, CEO of AutoDS.

Analyze this engagement data from their recent posts:
{engagement_data}

Extract actionable 'Golden Rules' — patterns that drive the most engagement.
Focus on:
- What type of hooks get the most clicks/impressions
- What topics get the most comments
- What posting style (length, tone, format) performs best
- What to AVOID based on poor performance
- Did the content pass the "Lior Test" (could only Lior say this)?

Format as a bullet list:
- [Insight]: <Specific actionable instruction>

Keep it concise. Max 5 insights."""

    print("   🧠 Analyzing with Ollama (llama3)...")
    response = ollama.generate(model="llama3", prompt=prompt)
    insights = response["response"]

    # Write to learning-log-agent.md (safe — never touches Reut's file)
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    log_entry = f"\n## Analyst Insights ({today})\n{insights}\n"

    update_learning_log(log_entry)

    return {"learning_context": insights}