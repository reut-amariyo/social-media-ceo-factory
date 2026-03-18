"""
Scout Agent — Strategist & Narrative Scout
===========================================
Finds trending topics and identifies the "Lior Angle" + friction.
Based on A-agents/strategist-scout.md from the ABC-TOM v5 system.

Focus Areas: Scaling, Pricing Strategy, Revenue Upselling, Growth Hacking, Branding, AI in Business
Output: Trend report with narrative hook, recommended archetype, and Copywriter instructions.
"""

import os
import ollama
from serpapi import GoogleSearch
from openai import OpenAI
from dotenv import load_dotenv
from core.state import AgentState

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")

# Lior's focus areas — what to scout for
FOCUS_AREAS = [
    "Scaling businesses and frameworks",
    "Pricing strategy and revenue optimization",
    "Growth hacking and viral mechanics",
    "E-commerce operations and dropshipping",
    "AI in business (Agentic AI, automation)",
    "Personal branding for founders and CEOs",
    "Startup operations and founder challenges",
]

# Lior's story assets — for connecting trends to personal experience
STORY_ASSETS = [
    "Age 14: Found TinyDeal-eBay arbitrage, made first $40 profit",
    "Age 21: eBay blocked account, built automation software → became AutoDS",
    "VAT Crisis: Took a loan, created mentorship program (150 people x $200/month)",
    "DSM-Tool: Feared market leader, overtook in 5 years, then acquired them",
    "Rejected PE Deal: Walked away one day before closing (cultural misalignment)",
    "Fiverr Acquisition: First dropshipping software acquired by a public company",
    "4 competitor acquisitions: DSM-Tool, ViralVault, Salefreaks, Yaballe",
    "$150M+ GMV, $20M+ ARR, 250+ employees",
]


def _search_google_trends(query: str, num_results: int = 5) -> list[dict]:
    """Search Google via SerpAPI and return top N results with title, URL, snippet."""
    print("   📡 Searching Google via SerpAPI...")
    params = {
        "engine": "google",
        "q": query,
        "num": num_results,
        "api_key": SERPAPI_API_KEY,
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    organic = results.get("organic_results", [])

    sources = []
    for item in organic[:num_results]:
        sources.append({
            "title": item.get("title", ""),
            "url": item.get("link", ""),
            "snippet": item.get("snippet", ""),
            "source": item.get("source", ""),
        })
    return sources


def _search_grok_trending(topic: str) -> str | None:
    """Use Grok (X API) to get real-time trending topics and conversations."""
    if not XAI_API_KEY:
        print("   ⚠️  Skipping Grok — XAI_API_KEY not set")
        return None
    print("   🐦 Querying Grok for trending X conversations...")
    try:
        client = OpenAI(
            api_key=XAI_API_KEY,
            base_url="https://api.x.ai/v1",
        )
        response = client.chat.completions.create(
            model="grok-3",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Grok, an AI with access to real-time X (Twitter) data. "
                        "Provide the top 5 trending conversations and hashtags on X right now "
                        "related to the given topic. Include key influencers and viral posts. "
                        "Focus on topics with FRICTION — where people disagree or debate."
                    ),
                },
                {
                    "role": "user",
                    "content": f"What are the top trending conversations on X about: {topic}? "
                               f"List the top 5 with hashtags, key voices, and what the FRICTION is.",
                },
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"   ⚠️  Grok API error (will continue without it): {e}")
        return None


def run_scout_agent(state: AgentState):
    """
    Strategist & Narrative Scout Agent.
    Finds trending topics → identifies friction → recommends narrative hook + archetype.
    """
    print("--- 🔍 AGENT: SCOUT (Strategist & Narrative Scout) ---")

    ceo = state.get("ceo_profile", {})
    ceo_name = ceo.get("name", "Lior Pozin")
    company = ceo.get("company", "AutoDS")
    industry = ceo.get("industry", "E-commerce, SaaS, AI")
    topics = ceo.get("topics", FOCUS_AREAS[:3])
    topics_str = ", ".join(topics) if isinstance(topics, list) else str(topics)

    # Load voice DNA and ICP from state (loaded by orchestrator)
    voice_dna = state.get("voice_dna", "")
    icp_profile = state.get("icp_profile", "")

    print(f"   👤 CEO: {ceo_name} | Company: {company}")
    print(f"   🎯 Focus: {topics_str}")

    # Build personalized search queries
    google_query = f"{industry} trends {topics_str} 2025 2026"
    grok_topic = f"{industry} {topics_str} founders CEOs startups"

    # 1. Google Search via SerpAPI — top 5 URLs
    google_sources = _search_google_trends(google_query, num_results=5)
    google_text = "\n".join(
        f"- {s['title']} ({s['url']}): {s['snippet']}" for s in google_sources
    )
    print(f"   ✅ Found {len(google_sources)} Google sources")

    # 2. Grok (X/Twitter) — real-time trending topics with friction
    grok_trends = _search_grok_trending(grok_topic)
    if grok_trends:
        print("   ✅ Got Grok trending topics")
    else:
        print("   ⏭️  Continuing without Grok data")

    # 3. Ollama — synthesize into a strategic brief (strategist-scout format)
    print("   🧠 Generating strategic brief with Ollama (llama3)...")
    combined_data = f"GOOGLE SEARCH RESULTS:\n{google_text}"
    if grok_trends:
        combined_data += f"\n\nX (TWITTER) TRENDING TOPICS:\n{grok_trends}"

    # Build the strategist prompt with all context
    voice_dna_section = f"\nVOICE DNA (how {ceo_name} speaks):\n{voice_dna[:2000]}" if voice_dna else ""
    icp_section = f"\nTARGET AUDIENCE:\n{icp_profile[:1000]}" if icp_profile else ""
    story_assets_text = "\n".join(f"- {s}" for s in STORY_ASSETS)

    summary_prompt = f"""You are the Strategist & Narrative Scout for {ceo_name}, CEO of {company}.
Your job: turn current events into brand authority. Find the FRICTION in trends.

{ceo_name}'s FOCUS AREAS: {topics_str}
{ceo_name}'s EDGE: CEO sharing from the arena, not a coach from the sidelines. {company} (acquired by Fiverr), $150M+ GMV, 250+ employees, 4 competitor acquisitions.
{voice_dna_section}
{icp_section}

{ceo_name}'s STORY ASSETS (connect trends to these if possible):
{story_assets_text}

AVAILABLE CONTENT ARCHETYPES (recommend one for each topic):
1. External Brand Story (company move → lesson)
2. Personal Confession ("X years ago, I made...")
3. Scene-Based Lesson (visual story → insight)
4. Crisis Response (platform change → Lior's take)
5. Industry Analysis (big company case study → contrarian insight)
6. Framework/Milestone (teaching 3-step framework)
7. Empathy-First Framework (reader pain → Lior's system)
8. Stories + Takeaways (3 vivid moments → extracted tips)

RESEARCH DATA:
{combined_data}

Based on all of the above, create a STRATEGIC BRIEF with exactly 3 trending topics.
For EACH topic provide:

**TOPIC [N]: [title]**
- THE TREND: What's happening right now (1 sentence)
- THE FRICTION: Why people are struggling or debating this
- THE LIOR ANGLE: How {ceo_name}'s experience makes this uniquely his to talk about
- TARGET AUDIENCE: Investors / Entrepreneurs / Growth-Seekers
- RECOMMENDED ARCHETYPE: Which content archetype to use
- HOOK TYPE: Provocative question / Personal confession / Scene-setting / Shocking stat / Empathy hook / etc.
- THE "GOLD" DETAIL: A specific number, date, or fact from the research
- LIOR STORY ASSET: Which personal story connects (if any)
- NARRATIVE HOOK: A 1-line hook that would stop the scroll

Return exactly 3 topics in this format."""

    response = ollama.generate(model="llama3", prompt=summary_prompt)

    return {
        "trend_report": response["response"],
        "google_sources": google_sources,
        "grok_trends": grok_trends,
    }