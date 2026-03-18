"""
Analyst Agent — Post-Run Learning
====================================
After Reut approves drafts, the Analyst logs what worked for future runs.
Writes to learning-log-agent.md (safe — never touches Reut's learning-log.md).
"""

import os
import ollama
from openai import OpenAI
from utils.obsidian_io import update_learning_log
from datetime import datetime

XAI_API_KEY = os.getenv("XAI_API_KEY")


def _generate_with_best_llm(prompt: str) -> str:
    """Use Grok (fast, remote) if available, otherwise fall back to Ollama."""
    if XAI_API_KEY:
        print("   🧠 Analyst: Analyzing with Grok-3 (remote)...")
        try:
            client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
            response = client.chat.completions.create(
                model="grok-3",
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"   ⚠️  Grok failed ({e}), falling back to Ollama...")

    print("   🧠 Analyst: Analyzing with Ollama llama3 (local)...")
    response = ollama.generate(model="llama3", prompt=prompt)
    return response["response"]


def run_analyst_agent(state: dict):
    """
    Agent 6: The Analyst — learns from each run.
    - Analyzes what happened in this run (scores, iterations, idea chosen)
    - Extracts actionable 'Golden Rules' for future runs
    - Saves to learning-log-agent.md (safe — Reut merges when ready)
    """
    print("--- 📊 AGENT: ANALYST (Learning from This Run) ---")

    ceo = state.get("ceo_profile", {})
    ceo_name = ceo.get("name", "Lior Pozin")
    engagement_data = state.get("engagement_data", "")
    selected_idea = state.get("selected_idea", "")
    drafts = state.get("post_drafts", {})
    scores = state.get("validation_scores", {})
    iterations = state.get("iteration_count", 0)
    validation = state.get("validation_results", "")

    # Build a summary of what happened
    drafts_preview = ""
    for platform, content in drafts.items():
        drafts_preview += f"\n[{platform.upper()}]: {content[:200]}...\n"

    scores_text = "\n".join(f"- {k}: {v}/5" for k, v in scores.items()) if scores else "No scores available"

    prompt = f"""You are a social media analytics expert for {ceo_name}'s brand.

A content run just completed. Analyze what happened and extract lessons for next time.

=== RUN SUMMARY ===
{engagement_data}

=== IDEA CHOSEN ===
{selected_idea[:300]}

=== GATEKEEPER SCORES ===
{scores_text}

=== ITERATIONS NEEDED ===
{iterations} (lower is better — means Creator nailed it faster)

=== FINAL DRAFTS (preview) ===
{drafts_preview}

=== VALIDATION NOTES ===
{validation[:500]}

Based on all of this, extract 3-5 actionable 'Golden Rules' for the NEXT run:
- What worked well that we should KEEP doing?
- What caused issues (failed validation, needed retries) that we should AVOID?
- What specific patterns in hooks/tone/structure led to higher scores?
- Any recommendation for the Ideator on what types of ideas to prioritize?

Format as bullet points. Be specific — reference actual scores and patterns, not vague advice."""

    insights = _generate_with_best_llm(prompt)

    # Write to learning-log-agent.md
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    avg_score = sum(scores.values()) / len(scores) if scores else 0
    log_entry = (
        f"\n## Run Analysis ({today})\n"
        f"**Idea:** {selected_idea[:100]}...\n"
        f"**Score:** {avg_score:.1f}/5 | **Iterations:** {iterations}\n"
        f"**Result:** Approved by Reut\n\n"
        f"### Insights\n{insights}\n"
        f"\n---\n"
    )

    update_learning_log(log_entry)
    print(f"   ✅ Logged {len(insights)} chars of insights to learning-log-agent.md")

    return {"learning_context": insights}