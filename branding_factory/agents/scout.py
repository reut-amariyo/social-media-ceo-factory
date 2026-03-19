"""
Scout Agent — Tech Pulse Radar (Upgraded)
==========================================
Multi-source intelligence gathering for trend hijacking.

Sources:
1. Tech Sites: The Verge AI, TechCrunch AI, Wired, MIT Tech Review, Hacker News, Hugging Face
2. X Account Monitoring: 12 key influencer accounts via Grok
3. Conversation Heat Detection: Which topics have the most engagement
4. Friction Extraction: What people are arguing about in comments
5. Lior Mapping: How to connect trends to his AutoDS experience

Output: 3 Trend + Friction + Lior Angle combos with eye-level hooks
"""

import os
import requests
import feedparser
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

XAI_API_KEY = os.getenv("XAI_API_KEY")

# Tech influencers to monitor via X
KEY_X_ACCOUNTS = [
    "alliekmiller",      # AI in business (1.2M followers)
    "bentossell",        # Ben's Bites, practical AI tools
    "Saj_Adib",          # AI Tool Radar
    "rowancheung",       # The Rundown AI, daily news
    "mattshumer_",       # OthersideAI CEO
    "OfficialLoganK",    # Google/OpenAI, big tech moves
    "emollick",          # Wharton prof, experimental AI use
    "levelsio",          # Indie hacker, bootstrapping
    "shl",               # Sahil Lavingia (Gumroad)
    "patio11",           # Patrick McKenzie, SaaS insights
    "swyx",              # AI Engineer Summit, dev tools
    "sama",              # Sam Altman, OpenAI CEO
]

# Tech news sources (RSS/scraping)
TECH_SOURCES = {
    "verge_ai": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
    "techcrunch_ai": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "wired": "https://www.wired.com/feed/tag/ai/latest/rss",
    "mit_tech": "https://www.technologyreview.com/feed/",
}

# Lior's expertise areas (for mapping trends)
LIOR_EXPERTISE = {
    "saas_pricing": "Scaled AutoDS using outcome-based pricing, not cost-plus",
    "ai_automation": "Built AI-powered product research that processed millions of listings",
    "growth_hacking": "Grew from $0 to 8 figures using viral loops and upselling",
    "competitor_acquisition": "Acquired 4 competitors (DSM-Tool, ViralVault, Salefreaks, Yaballe)",
    "bootstrapping": "Bootstrapped to $20M ARR before acquisition",
    "ecommerce_ops": "Ran dropshipping operations at $150M+ GMV",
}

# Lior's story moments (for connecting to trends)
LIOR_STORIES = [
    "Age 14: Found TinyDeal-eBay arbitrage, made first $40 profit",
    "Age 21: eBay blocked account, built automation → became AutoDS",
    "VAT Crisis: Took a loan, created $30K/month mentorship program",
    "Rejected PE Deal: Walked away 1 day before closing (cultural misalignment)",
    "Fiverr Acquisition: First dropshipping software acquired by public company",
]


def _generate_with_grok(prompt: str, agent_name: str = "Scout") -> str:
    """Use Grok-3 for all generation (fast, remote)."""
    if not XAI_API_KEY:
        return "⚠️ XAI_API_KEY not set — cannot generate content"
    
    print(f"   🧠 {agent_name}: Generating with Grok-3...")
    try:
        client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
        response = client.chat.completions.create(
            model="grok-3",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"   ❌ Grok error: {e}")
        return f"Error: {e}"


def _fetch_rss_feed(name: str, url: str, max_items: int = 5) -> list[dict]:
    """Fetch RSS feed and return top N items."""
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries[:max_items]:
            items.append({
                "source": name,
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", "")[:200],
                "published": entry.get("published", ""),
            })
        return items
    except Exception as e:
        print(f"   ⚠️ RSS fetch failed for {name}: {e}")
        return []


def _fetch_hacker_news_top(max_items: int = 10) -> list[dict]:
    """Fetch top stories from Hacker News (stories with >50 comments)."""
    try:
        # Get top story IDs
        top_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(top_url, timeout=5)
        story_ids = response.json()[:30]  # Get top 30

        stories = []
        for story_id in story_ids[:max_items]:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_data = requests.get(story_url, timeout=3).json()
            
            # Only include if it has comments (indicates engagement)
            if story_data.get("descendants", 0) > 50:
                stories.append({
                    "source": "Hacker News",
                    "title": story_data.get("title", ""),
                    "link": story_data.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                    "comments": story_data.get("descendants", 0),
                    "score": story_data.get("score", 0),
                })
        
        return sorted(stories, key=lambda x: x["comments"], reverse=True)[:max_items]
    except Exception as e:
        print(f"   ⚠️ HN fetch failed: {e}")
        return []


def _fetch_huggingface_papers(max_items: int = 5) -> list[dict]:
    """Fetch top upvoted papers from Hugging Face daily papers."""
    try:
        url = "https://huggingface.co/papers"
        response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')
        
        papers = []
        # This is a simplified scraper — HF's structure may change
        for article in soup.find_all("article", limit=max_items):
            title_elem = article.find("h3")
            if title_elem:
                papers.append({
                    "source": "Hugging Face Papers",
                    "title": title_elem.get_text(strip=True),
                    "link": "https://huggingface.co/papers",
                })
        
        return papers[:max_items]
    except Exception as e:
        print(f"   ⚠️ HuggingFace fetch failed: {e}")
        return []


def _monitor_x_accounts_via_grok(accounts: list[str], topic_context: str) -> str:
    """Use Grok to check recent tweets from key accounts."""
    if not XAI_API_KEY:
        return ""
    
    accounts_str = ", ".join(f"@{acc}" for acc in accounts)
    prompt = f"""You are Grok with real-time X (Twitter) access.

Check the LAST 3 TWEETS from each of these accounts:
{accounts_str}

Context: We're looking for trending topics in: {topic_context}

For each account, report:
1. What they're talking about (topic)
2. The engagement (likes, retweets if notable)
3. Any friction/debate in replies

Focus on topics that appear across MULTIPLE accounts (cross-account trends).
Format as a brief summary (3-5 sentences per major trend detected)."""

    try:
        return _generate_with_grok(prompt, agent_name="Scout (X Monitor)")
    except Exception as e:
        print(f"   ⚠️ X monitoring failed: {e}")
        return ""


def run_scout_agent(state: dict):
    """
    Tech Pulse Radar — Multi-source intelligence gathering.
    
    Finds: Trending topics + Friction + Lior's unique angle + Eye-level hooks
    """
    print("--- 🔍 AGENT: SCOUT (Tech Pulse Radar) ---")
    
    ceo = state.get("ceo_profile", {})
    ceo_name = ceo.get("name", "Lior Pozin")
    company = ceo.get("company", "AutoDS")
    topics = ceo.get("topics", ["SaaS", "AI", "Scaling"])
    topic_context = ", ".join(topics) if isinstance(topics, list) else str(topics)
    
    print(f"   👤 CEO: {ceo_name} | Company: {company}")
    print(f"   🎯 Focus: {topic_context}")
    
    # === PHASE 1: Multi-Source Scan (Parallel) ===
    print("\n   🌐 PHASE 1: Scanning tech sources...")
    all_sources = []
    
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {}
        
        # Tech site RSS feeds
        for name, url in TECH_SOURCES.items():
            futures[executor.submit(_fetch_rss_feed, name, url, 5)] = name
        
        # Hacker News
        futures[executor.submit(_fetch_hacker_news_top, 10)] = "hacker_news"
        
        # Hugging Face papers
        futures[executor.submit(_fetch_huggingface_papers, 5)] = "huggingface"
        
        for future in as_completed(futures):
            source_name = futures[future]
            try:
                result = future.result()
                all_sources.extend(result)
                print(f"      ✅ {source_name}: {len(result)} items")
            except Exception as e:
                print(f"      ⚠️ {source_name} failed: {e}")
    
    print(f"   📊 Total sources collected: {len(all_sources)}")
    
    # === PHASE 2: X Account Monitoring ===
    print("\n   🐦 PHASE 2: Monitoring key X accounts via Grok...")
    x_monitoring = _monitor_x_accounts_via_grok(KEY_X_ACCOUNTS[:12], topic_context)
    if x_monitoring:
        print("      ✅ X monitoring complete")
    else:
        print("      ⏭️ Skipped (no XAI key)")
    
    # === PHASE 3: Final Brief Generation ===
    print("\n   📝 PHASE 3: Generating trend briefs...")
    
    # Build a summary of all sources for context
    sources_summary = "\n".join(
        f"[{item.get('source', 'Unknown')}] {item.get('title', '')} "
        f"({item.get('comments', 0)} comments, {item.get('score', 0)} upvotes)"
        for item in all_sources[:25]
    )
    
    final_brief_prompt = f"""You are the Tech Pulse Radar for Lior Pozin, CEO of AutoDS (acquired by Fiverr).

COLLECTED INTELLIGENCE:

Tech News Sources:
{sources_summary[:2500]}

X Account Monitoring:
{x_monitoring[:1500]}

Lior's Expertise:
- SaaS pricing (outcome-based, not cost-plus)
- AI automation (built product research AI at AutoDS)
- Bootstrapping ($0 to $20M ARR, then acquired by Fiverr)
- Competitor acquisition (4 companies: DSM-Tool, ViralVault, Salefreaks, Yaballe)
- E-commerce operations ($150M+ GMV)

Lior's Stories:
{chr(10).join(f"- {s}" for s in LIOR_STORIES)}

TARGET AUDIENCE:
- **Builders** (anyone building products, not just "founders")
- Entrepreneurs (aspiring and active)
- Growth-minded people who want to ship and win

CRITICAL RULES:
1. Use "builders" instead of "founders"
2. Make language ACCESSIBLE (no jargon)
3. Start with HUMAN EMOTION (fear, FOMO, confusion)
4. Connect to Lior's REAL EXPERIENCE at AutoDS
5. Focus on FRICTION (what people are arguing/struggling with)

TASK: Create 3 TREND BRIEFS in this exact format:

---
**TREND #1: [Title]**

**What's Happening (Raw Trend):**
[2-3 sentences: what's the tech news/event happening RIGHT NOW]

**The Friction (What People Are Arguing About):**
[2-3 sentences: what's the pain, debate, confusion, or fear]

**Lior's Lens (His Unique POV from AutoDS):**
[2-3 sentences: how his journey from eBay arbitrage → $150M GMV gives him a unique answer]

**Eye-Level Hook (Accessible to Everyone):**
[1-2 punchy sentences. Use "builders" not "founders". Make it relatable.]

---
**TREND #2: [Title]**
[same format]

---
**TREND #3: [Title]**
[same format]

---

Make hooks PUNCHY. Make language SIMPLE. Show Lior's BATTLE SCARS."""

    final_brief = _generate_with_grok(final_brief_prompt, agent_name="Scout (Final Brief)")
    
    print("\n   ✅ SCOUT COMPLETE — 3 trend briefs generated\n")
    
    return {
        "trend_report": final_brief,
        "raw_sources": all_sources[:20],  # Keep top 20 for reference
        "x_monitoring": x_monitoring,
    }
