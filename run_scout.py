from dotenv import load_dotenv
from branding_factory.agents.scout import run_scout_agent
from core.state import AgentState
from utils.obsidian_io import test_connection, get_ceo_profile

load_dotenv()

if __name__ == "__main__":
    # 1. Test Obsidian connection
    print("🔌 Checking Obsidian Vault Connection...")
    connected = test_connection()

    # 2. Load CEO profile from Obsidian (or use fallback)
    if connected:
        ceo_profile = get_ceo_profile()
    else:
        ceo_profile = {}

    if not ceo_profile:
        print("   ⚠️  No CEO profile found — using fallback demo profile")
        ceo_profile = {
            "name": "Lior Pozin",
            "company": "AutoDS",
            "role": "CEO & Serial Entrepreneur",
            "industry": "E-commerce, SaaS, AI",
            "topics": ["Scaling", "Pricing Strategy", "Growth Hacking", "AI in Business"],
            "tone": "Direct, bold, eye-level, no-BS, action-oriented",
        }

    # 3. Build state with CEO profile
    state = AgentState(
        ceo_profile=ceo_profile,
        voice_dna="",
        icp_profile="",
        trend_report="",
        ideas=[],
        selected_idea="",
        post_drafts={},
        image_path="",
        validation_results="",
        iteration_count=0,
        learning_context=""
    )
    result = run_scout_agent(state)

    print("\n" + "=" * 60)
    print("📊 TREND REPORT (AI Summary)")
    print("=" * 60)
    print(result.get("trend_report"))

    print("\n" + "=" * 60)
    print("🔗 GOOGLE SOURCES (Top 5 URLs)")
    print("=" * 60)
    for i, src in enumerate(result.get("google_sources", []), 1):
        print(f"\n{i}. {src['title']}")
        print(f"   🌐 URL:     {src['url']}")
        print(f"   📰 Source:  {src['source']}")
        print(f"   📝 Snippet: {src['snippet']}")

    print("\n" + "=" * 60)
    print("🐦 GROK / X TRENDING TOPICS")
    print("=" * 60)
    print(result.get("grok_trends", ""))
