"""
Scout Agent — Tech Pulse Radar (Upgraded)
==========================================
Multi-source intelligence gathering for trend hijacking.

Sources:
1. Tech News Sites: The Verge AI, TechCrunch AI, Wired, MIT Tech Review
2. AI Company Blogs: OpenAI, Anthropic, Google AI, Microsoft, Meta, Apple ML, AWS, Hugging Face, Stability AI, Mistral, Cohere
3. Hacker News: Top stories with high engagement
4. X Account Monitoring: Tech influencers + Content inspiration accounts via Grok
5. Inspiration List: 16 content creators to learn format/style from
6. Friction Extraction: What people are arguing about in comments
7. Lior Mapping: How to connect trends to his AutoDS experience

Output: 3 Trend + Friction + Lior Angle + Format Inspiration combos with eye-level hooks
"""

import os
import sys
import requests
import feedparser
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI
from dotenv import load_dotenv

# Add parent directory to path to import inspiration_list
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from inspiration_list import get_x_inspiration_handles, get_inspiration_summary

load_dotenv()

XAI_API_KEY = os.getenv("XAI_API_KEY")

# Tech influencers to monitor via X (AI/Tech specific)
TECH_X_ACCOUNTS = [
    "alliekmiller",      # AI in business (1.2M followers)
    "bentossell",        # Ben's Bites, practical AI tools
    "Saj_Adib",          # AI Tool Radar
    "rowancheung",       # The Rundown AI, daily news
    "mattshumer_",       # OthersideAI CEO
    "OfficialLoganK",    # Google/OpenAI, big tech moves
    "emollick",          # Wharton prof, experimental AI use
    "shl",               # Sahil Lavingia (Gumroad)
    "patio11",           # Patrick McKenzie, SaaS insights
    "swyx",              # AI Engineer Summit, dev tools
    "sama",              # Sam Altman, OpenAI CEO
]

# Inspiration list (content creators to learn from)
INSPIRATION_X_ACCOUNTS = get_x_inspiration_handles()

# Combined list: Tech + Inspiration
KEY_X_ACCOUNTS = TECH_X_ACCOUNTS + INSPIRATION_X_ACCOUNTS

# Tech news sources (RSS/scraping)
TECH_SOURCES = {
    "verge_ai": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
    "techcrunch_ai": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "wired": "https://www.wired.com/feed/tag/ai/latest/rss",
    "mit_tech": "https://www.technologyreview.com/feed/",
}

# AI Company Official Blogs & News (Product launches, features, research)
AI_COMPANY_SOURCES = {
    # OpenAI
    "openai_blog": "https://openai.com/blog/rss",
    "openai_research": "https://openai.com/research/rss",
    
    # Anthropic
    "anthropic_news": "https://www.anthropic.com/news",  # Will scrape
    
    # Google AI
    "google_ai_blog": "https://ai.googleblog.com/feeds/posts/default",
    "google_deepmind": "https://deepmind.google/discover/blog/rss.xml",
    
    # Microsoft AI
    "microsoft_ai": "https://blogs.microsoft.com/ai/feed/",
    
    # Meta AI
    "meta_ai": "https://ai.meta.com/blog/rss/",
    
    # Apple ML Research (no RSS, will scrape)
    "apple_ml": "https://machinelearning.apple.com",
    
    # Amazon/AWS AI
    "aws_ai": "https://aws.amazon.com/blogs/machine-learning/feed/",
    
    # Hugging Face
    "huggingface_blog": "https://huggingface.co/blog/feed.xml",
    
    # Stability AI
    "stability_ai": "https://stability.ai/news",  # Will scrape
    
    # Mistral AI
    "mistral_blog": "https://mistral.ai/news/",  # Will scrape
    
    # Cohere
    "cohere_blog": "https://cohere.com/blog",  # Will scrape
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


def _scrape_company_news(name: str, url: str, max_items: int = 3) -> list[dict]:
    """Scrape AI company news pages (for those without RSS feeds)."""
    try:
        response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')
        
        items = []
        # Try to find article titles and links (common patterns)
        for tag in soup.find_all(['h2', 'h3', 'h4'], limit=max_items * 2):
            link = tag.find_parent('a') or tag.find('a')
            if link and link.get('href'):
                title = tag.get_text(strip=True)
                href = link.get('href')
                
                # Make absolute URL if relative
                if href.startswith('/'):
                    from urllib.parse import urljoin
                    href = urljoin(url, href)
                
                if title and len(title) > 10:  # Filter out noise
                    items.append({
                        "source": name,
                        "title": title,
                        "link": href,
                    })
                    if len(items) >= max_items:
                        break
        
        return items
    except Exception as e:
        print(f"   ⚠️ Scrape failed for {name}: {e}")
        return []


def _get_top_x_posts_about_ai_saas() -> str:
    """Use Grok to get the top 5-7 X posts about AI in SaaS with highest engagement."""
    if not XAI_API_KEY:
        return ""
    
    prompt = """You are Grok with real-time X (Twitter) access.

Find the TOP 5-7 POSTS from the LAST 24-48 HOURS about AI in SaaS.

CRITICAL FILTERS:
- Focus: AI in SaaS (AI features in SaaS products, AI tools for SaaS companies, AI-powered SaaS)
- Sort by: Highest engagement (likes + retweets + replies combined)
- Only posts with 1000+ total engagement
- Skip: Generic AI hype, consumer AI apps, AI research papers

For each post, return:
1. @username
2. When posted (e.g., "2 hours ago", "yesterday", "today")
3. Exact post text (first 200 chars)
4. Engagement count (likes + retweets + replies)
5. Why it's trending (1 sentence)

Format:
---
@username · 2 hours ago · (15.2K engagement)
"Post text here..."
Why trending: Product Hunt launch of AI copilot for SaaS got massive traction

---
@username2 · yesterday · (12.8K engagement)
"Post text..."
Why trending: CEO shared revenue numbers from AI features

Keep it CONCISE. Return exactly 5-7 posts. ALWAYS include the timestamp (when posted)."""

    try:
        print(f"   🔍 Fetching top AI in SaaS posts from X...")
        client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
        response = client.chat.completions.create(
            model="grok-3",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"   ❌ Grok error: {e}")
        return ""


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
    print("      📰 Tech News: The Verge AI, TechCrunch AI, Wired, MIT Tech Review")
    print("      🏢 AI Companies: OpenAI, Anthropic, Google, Microsoft, Meta, Apple, AWS")
    print("      🔥 Hacker News: Top stories with >50 comments")
    print("      📄 Hugging Face: Daily upvoted papers")
    all_sources = []
    
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = {}
        
        # Tech news RSS feeds
        for name, url in TECH_SOURCES.items():
            futures[executor.submit(_fetch_rss_feed, name, url, 5)] = name
        
        # AI Company sources (RSS + scraping)
        rss_sources = [
            ("openai_blog", AI_COMPANY_SOURCES["openai_blog"]),
            ("openai_research", AI_COMPANY_SOURCES["openai_research"]),
            ("google_ai_blog", AI_COMPANY_SOURCES["google_ai_blog"]),
            ("google_deepmind", AI_COMPANY_SOURCES["google_deepmind"]),
            ("microsoft_ai", AI_COMPANY_SOURCES["microsoft_ai"]),
            ("meta_ai", AI_COMPANY_SOURCES["meta_ai"]),
            ("aws_ai", AI_COMPANY_SOURCES["aws_ai"]),
            ("huggingface_blog", AI_COMPANY_SOURCES["huggingface_blog"]),
        ]
        for name, url in rss_sources:
            futures[executor.submit(_fetch_rss_feed, name, url, 3)] = name
        
        # Scrape-only AI companies
        scrape_sources = [
            ("anthropic", AI_COMPANY_SOURCES["anthropic_news"]),
            ("apple_ml", AI_COMPANY_SOURCES["apple_ml"]),
            ("stability_ai", AI_COMPANY_SOURCES["stability_ai"]),
            ("mistral_blog", AI_COMPANY_SOURCES["mistral_blog"]),
            ("cohere_blog", AI_COMPANY_SOURCES["cohere_blog"]),
        ]
        for name, url in scrape_sources:
            futures[executor.submit(_scrape_company_news, name, url, 3)] = name
        
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
    
    # === PHASE 2: Top X Posts About AI in SaaS ===
    print("\n   🐦 PHASE 2: Finding top X posts about AI in SaaS...")
    print("      🔥 Filtering by highest engagement (1000+ interactions)")
    print("      🎯 Focus: AI features, AI-powered SaaS, AI in SaaS companies")
    
    top_x_posts = _get_top_x_posts_about_ai_saas()
    if top_x_posts:
        print("      ✅ Found top 5-7 posts")
    else:
        print("      ⏭️ Skipped (no XAI key)")
    
    # === PHASE 3: Generate Two Separate Sections ===
    print("\n   📝 PHASE 3: Generating structured trend report...")
    
    # Filter for AI in SaaS news with timestamps
    ai_saas_news = [item for item in all_sources if any(
        keyword in item.get('title', '').lower() or keyword in item.get('source', '').lower()
        for keyword in ['ai', 'openai', 'anthropic', 'microsoft', 'google', 'saas']
    )]
    
    # Include timestamps and sources in the summary
    ai_news_summary = "\n".join(
        f"• [{item.get('source', '')}] {item.get('title', '')} "
        f"(Published: {item.get('published', 'recently')})"
        for item in ai_saas_news[:15]
    )
    
    final_brief_prompt = f"""You are a trend analyst for Lior Pozin, CEO of AutoDS (acquired by Fiverr).

FOCUS: AI in SaaS (AI features in SaaS products, AI-powered SaaS tools, AI transforming SaaS companies)

AI COMPANY NEWS & RESEARCH (WITH TIMESTAMPS):
{ai_news_summary[:2500]}

TOP X POSTS ABOUT AI IN SAAS (HIGHEST ENGAGEMENT):
{top_x_posts[:2500]}

Lior's Background:
- Built AutoDS (dropshipping SaaS with AI automation) from $0 → $20M ARR → Acquired by Fiverr
- Used AI for product research automation, pricing optimization
- Bootstrapped, then acquired 4 competitors
- E-commerce operations at $150M+ GMV

TASK: Create a structured trend report with TWO sections:

=== SECTION 1: AI COMPANY NEWS (3-6 items) ===

Pick 3-6 news items from AI companies (Anthropic, OpenAI, Microsoft, Google, Meta, AWS, etc.)

Format each as 1 sentence (25-35 words):
- [Company] [timing] [what happened] + [why SaaS companies should care]

Example:
1. Anthropic yesterday released Claude with 200K context windows, letting SaaS companies build AI on entire customer histories instead of snippets.
2. Microsoft this week announced $50/month Copilot pricing, proving customers will pay premium for AI features.
3. OpenAI today launched Realtime API, enabling SaaS companies to add voice AI in hours, not months.

=== SECTION 2: TOP X POSTS (3-6 items) ===

Pick 3-6 posts from the X monitoring data provided above.

Format each as:
@username · [timing] · ([engagement] interactions)
"[First 100-150 chars of post]"
Intent: [Why this is trending - what's the emotional driver or business angle]

Example:
@rauchg · 3 hours ago · (18.5K interactions)
"Vercel just shipped AI SDK 4.0 with streaming and function calling built in. This changes everything for SaaS companies building AI features..."
Intent: Product launch excitement + FOMO (fear of being left behind in AI race)

CRITICAL RULES:
- Section 1: Company news ONLY (not X posts)
- Section 2: X posts ONLY (not company news)
- MUST include timing in both sections
- MUST include "Intent" for X posts (emotional/business driver)
- Keep it concise and actionable

Return in this exact format:

=== AI COMPANY NEWS ===
1. [sentence]
2. [sentence]
3. [sentence]
(continue for 3-6 items)

=== TOP X POSTS ===
@username · timing · (engagement)
"post text..."
Intent: [intent]

@username · timing · (engagement)
"post text..."
Intent: [intent]

(continue for 3-6 items)"""

    final_brief = _generate_with_grok(final_brief_prompt, agent_name="Scout (Final Brief)")
    
    # Summary of sources used
    print("\n   ✅ SCOUT COMPLETE — Structured report generated")
    print("   📰 AI Company News: 3-6 items")
    print("   🐦 Top X Posts: 3-6 items with intent analysis")
    print(f"   📊 AI in SaaS sources used: {len(ai_saas_news)} items")
    print(f"   🐦 Top X posts: {len(top_x_posts) if top_x_posts else 0} chars")
    print()
    
    return {
        "trend_report": final_brief,
        "raw_sources": ai_saas_news[:15],  # Keep top 15 AI/SaaS sources
        "top_x_posts": top_x_posts,
    }

