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
    ceo_name = ceo.get("name", "Unknown")
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

CRITICAL INSTRUCTION: Every idea MUST be directly based on the Scout findings above.
- Use the AI company news (Section 1)
- Use the trending X posts (Section 2)
- Connect {ceo_name}'s {company} experience to what's happening NOW

Propose 5-7 content ideas. Keep it ULTRA SIMPLE - just 2 fields per idea.

Format for each idea:

IDEA [N]:
The idea: [One punchy sentence connecting Scout finding to {ceo_name}'s experience]

Hook: [The scroll-stopping opening line - make it provocative]

---

RULES:
1. Every idea MUST reference a specific Scout finding
2. Keep it SHORT and PUNCHY
3. Make it CONTROVERSIAL or surprising
4. Only {ceo_name} can say this (their unique experience at {company})
5. Generate 5-7 ideas (at least 5, up to 7)

Example of GOOD format:
IDEA 1:
The idea: [A specific news item] - I've been applying this at {company} with real results.

Hook: "I just [specific bold claim with numbers]. [Surprising outcome]."

---

IDEA 2:
The idea: Everyone's doing X - but at {company} we did the opposite and it worked.

Hook: "Hot take: [Contrarian statement]. We [specific action] and [specific result]."

Return 5-7 ideas. Each must connect to a Scout finding."""

    print("   🧠 Generating ideas...")
    ideas_text = _generate_with_best_llm(prompt, agent_name="Ideator")

    # --- Self-reflection: rank ideas against past performance ---
    print("   🔍 Ideator: Self-reflecting on idea quality...")
    if learning_log or past_posts:
        ranking_prompt = f"""You just generated these 5-7 content ideas:

{ideas_text}

PAST PERFORMANCE DATA:
{learning_log[:1500]}

Rank all ideas from strongest to weakest based on:
1. Friction potential (will it generate comments/debate?)
2. Uniqueness (could only Lior say this?)
3. Clarity (is it immediately clear what the post is about?)

Return them ranked as:
RANKED IDEA 1: 
[paste the full idea text exactly as written]

RANKED IDEA 2: 
[paste the full idea text exactly as written]

RANKED IDEA 3: 
[paste the full idea text exactly as written]

RANKED IDEA 4: 
[paste the full idea text exactly as written]

RANKED IDEA 5: 
[paste the full idea text exactly as written]

(Continue for ideas 6-7 if generated)

Add one sentence explaining why each is ranked there."""

        ranked_text = _generate_with_best_llm(ranking_prompt, agent_name="Ideator (ranking)")
        # Try to parse ranked ideas
        ranked_ideas = _parse_ranked_ideas(ranked_text)
        if ranked_ideas and len(ranked_ideas) >= 2:
            ideas = ranked_ideas
            print(f"   ✅ Ideas ranked by predicted performance ({len(ideas)} ideas)")
        else:
            # Fall back to original parsing
            ideas = _parse_ideas(ideas_text)
            print(f"   ⏭️ Ranking parse failed — using original order")
    else:
        ideas = _parse_ideas(ideas_text)

    if not ideas:
        ideas = [ideas_text]

    print(f"   ✅ Generated {len(ideas)} content ideas")

    return {
        "ideas": ideas,
    }


def _parse_ideas(ideas_text: str) -> list[str]:
    """Parse numbered ideas from LLM output (supports 1-7 ideas)."""
    ideas = []
    for i in range(1, 8):  # Parse up to 7 ideas
        start = ideas_text.find(f"{i}.")
        if start == -1:
            start = ideas_text.find(f"IDEA {i}")
        end = ideas_text.find(f"{i + 1}.") if i < 7 else len(ideas_text)
        if end == -1 and i < 7:
            end = ideas_text.find(f"IDEA {i + 1}")
        if start != -1:
            ideas.append(ideas_text[start:end if end != -1 else len(ideas_text)].strip())
    return ideas


def _parse_ranked_ideas(ranked_text: str) -> list[str]:
    """Parse ranked ideas from the self-reflection output (supports 1-7 ideas)."""
    import re
    # Find all RANKED IDEA N: positions
    markers = list(re.finditer(r'RANKED IDEA \d+:', ranked_text))
    if not markers:
        return []
    
    ideas = []
    for idx, match in enumerate(markers):
        start = match.end()
        end = markers[idx + 1].start() if idx + 1 < len(markers) else len(ranked_text)
        idea_text = ranked_text[start:end].strip()
        # Extract just the idea + hook, stop before any "This ranks" explanation
        # Keep the core content but trim ranking explanation for cleaner display
        lines = idea_text.split('\n')
        clean_lines = []
        for line in lines:
            # Stop if we hit a ranking explanation for a DIFFERENT idea
            if re.match(r'RANKED IDEA \d+:', line):
                break
            clean_lines.append(line)
        idea_text = '\n'.join(clean_lines).strip()
        if idea_text:
            ideas.append(idea_text)
    return ideas