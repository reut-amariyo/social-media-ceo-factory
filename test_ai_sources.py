"""
Quick test to verify AI company sources are working
"""
import sys
sys.path.append('branding_factory/agents')

from scout import AI_COMPANY_SOURCES, _fetch_rss_feed, _scrape_company_news

print("🧪 TESTING AI COMPANY NEWS SOURCES")
print("=" * 60)

# Test RSS feeds
print("\n📡 Testing RSS Feeds:")
rss_tests = [
    ("OpenAI Blog", AI_COMPANY_SOURCES["openai_blog"]),
    ("Google AI Blog", AI_COMPANY_SOURCES["google_ai_blog"]),
    ("Microsoft AI", AI_COMPANY_SOURCES["microsoft_ai"]),
]

for name, url in rss_tests:
    print(f"\n   Testing: {name}")
    items = _fetch_rss_feed(name, url, 2)
    if items:
        print(f"   ✅ Success: {len(items)} items")
        for item in items:
            print(f"      • {item['title'][:80]}")
    else:
        print(f"   ⚠️  No items (might be network issue)")

# Test scraping
print("\n\n🕷️  Testing Web Scraping:")
scrape_tests = [
    ("Anthropic", AI_COMPANY_SOURCES["anthropic_news"]),
    ("Apple ML", AI_COMPANY_SOURCES["apple_ml"]),
]

for name, url in scrape_tests:
    print(f"\n   Testing: {name}")
    items = _scrape_company_news(name, url, 2)
    if items:
        print(f"   ✅ Success: {len(items)} items")
        for item in items:
            print(f"      • {item['title'][:80]}")
    else:
        print(f"   ⚠️  No items (might be network issue or structure changed)")

print("\n" + "=" * 60)
print("✅ Test complete!")
print(f"\n📊 Total AI company sources configured: {len(AI_COMPANY_SOURCES)}")
print("\nSources:")
for name in AI_COMPANY_SOURCES.keys():
    print(f"   • {name}")
