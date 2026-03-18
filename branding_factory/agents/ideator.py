"""
Ideator Agent — Brand Strategist
==================================
Filters scout's trends through Brand DNA, proposes 3 content angles.
Uses Voice DNA + ICP + learning log for brand-aligned ideation.
"""

import os
import ollama
from openai import OpenAI
from utils.obsidian_io import get_learning_log, get_brand_dna, get_past_posts

XAI_API_KEY = os.getenv("XAI_API_KEY")


def _generate_with_best_llm(prompt: str, agent_name: str = "Ideator") -> str:
    """Use Grok (fast, remote) if available, otherwise fall back to Ollama (local)."""
    if XAI_API_KEY:
        print(f"   🧠 {agent_name}: Generating with Grok-3 (remote — fast)...")
        try:
            client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
            response = client.chat.completions.create(
                model="grok-3",
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"   ⚠️  Grok failed ({e}), falling back to Ollama...")

    print(f"   🧠 {agent_name}: Generating with Ollama llama3 (local — slower)...")
    response = ollama.generate(model="llama3", prompt=prompt)
    return response["response"]


def run_ideator_agent(state: dict):
    """
    Agent 2: The Brand Strategist / Ideator
    - Reads Voice DNA + ICP + learning log from state/Obsidian
    - Filters trends to match the CEO's brand
    - Proposes 3 content angles with specific archetypes and hooks
    """
    print("--- 💡 AGENT: IDEATOR (Brainstorming Content Angles) ---")

    ceo = state.get("ceo_profile", {})
    ceo_name = ceo.get("name", "Lior Pozin")
    company = ceo.get("company", "AutoDS")
    industry = ceo.get("industry", "E-commerce, SaaS, AI")
    topics = ceo.get("topics", [])
    tone = ceo.get("tone", "Direct, bold, eye-level, no-BS")
    topics_str = ", ".join(topics) if isinstance(topics, list) else str(topics)

    trend_report = state.get("trend_report", "")

    # Load context — prefer from state (loaded by orchestrator), fallback to Obsidian
    voice_dna = state.get("voice_dna", "") or ""
    icp_profile = state.get("icp_profile", "") or ""
    learning_log = state.get("learning_context", "") or get_learning_log()

    # Load past posts for style reference
    brand_dna = get_brand_dna() if not voice_dna else voice_dna
    past_posts = get_past_posts(limit=5)

    print(f"   📖 Voice DNA: {len(voice_dna)} chars")
    print(f"   🎯 ICP Profile: {len(icp_profile)} chars")
    print(f"   📝 Learning Log: {len(learning_log)} chars")
    print(f"   📄 Past posts: {len(past_posts)} loaded")

    past_posts_text = "\n---\n".join(past_posts) if past_posts else "No past posts available."

    # Build voice DNA section (trimmed — ideator needs direction, not full DNA)
    voice_section = voice_dna[:1500] if voice_dna else brand_dna[:1000]
    icp_section = icp_profile[:800] if icp_profile else ""

    prompt = f"""You are a personal branding strategist for {ceo_name}, CEO of {company}.
Industry: {industry}
Focus topics: {topics_str}
Tone: {tone}

VOICE DNA (how {ceo_name} speaks — follow this exactly):
{voice_section}

TARGET AUDIENCE (ICP):
{icp_section}

KEY RULES FROM PAST PERFORMANCE:
{learning_log[:2000]}

EXAMPLES OF PAST SUCCESSFUL POSTS (mimic this style):
{past_posts_text[:3000]}

TODAY'S STRATEGIC BRIEF FROM SCOUT:
{trend_report}

Based on all of the above, propose exactly 3 content ideas that:
1. Are aligned with {ceo_name}'s Voice DNA and tone (eye-level, never condescending)
2. Connect a trending topic to their personal experience or expertise
3. Have FRICTION — something debatable, not just "everyone agrees this is great"
4. Would drive engagement (comments, shares) on LinkedIn (primary) + X + Instagram
5. Pass the "Lior Test": Could ONLY {ceo_name} say this? (not generic advice)

For each idea, provide:
- IDEA [N]: [catchy title]
- ARCHETYPE: [which content type — External Brand Story / Personal Confession / Scene-Based Lesson / Framework / Empathy-First / Stories + Takeaways]
- HOOK TYPE: [Provocative question / Personal confession / Scene-setting / Shocking stat / Empathy hook / Reader-mirror / Staccato fragments]
- THE HOOK: The actual opening line that would stop the scroll (ONE line only)
- ANGLE: How to connect the trend to {ceo_name}'s specific experience
- TARGET: Investors / Entrepreneurs / Growth-Seekers
- PLATFORMS: Which platforms this works best on

Return exactly 3 ideas numbered 1, 2, 3."""

    print("   🧠 Generating ideas...")
    ideas_text = _generate_with_best_llm(prompt, agent_name="Ideator")

    # Parse into a list of ideas
    ideas = []
    for i in range(1, 4):
        start = ideas_text.find(f"{i}.")
        if start == -1:
            start = ideas_text.find(f"IDEA {i}")
        end = ideas_text.find(f"{i + 1}.") if i < 3 else len(ideas_text)
        if end == -1 and i < 3:
            end = ideas_text.find(f"IDEA {i + 1}")
        if start != -1:
            ideas.append(ideas_text[start:end if end != -1 else len(ideas_text)].strip())

    if not ideas:
        ideas = [ideas_text]  # Fallback: return full text as single idea

    print(f"   ✅ Generated {len(ideas)} content ideas")

    return {
        "ideas": ideas,
    }
