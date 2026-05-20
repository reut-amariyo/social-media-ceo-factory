#!/usr/bin/env python3
"""
🏭 Personal Branding Factory
==========================================
Agentic AI system that generates personalized social media content
for any CEO / founder / thought leader.

Usage:
    python setup_profile.py   (first time — sets up your profile)
    python main.py            (run the factory)

Flow:
    1. Load Context (profile.yaml + optional Obsidian vault)
    2. Scout (Google + Grok → trending topics, filtered for your focus areas)
    3. Ideator (filter trends → 3 content angles with narrative hooks)
    4. Human Checkpoint (you pick your favorite)
    5. Creator (multi-platform drafts: X, LinkedIn, Instagram — in your voice)
    6. Validator (quality control: tone, vocabulary, brand alignment)
    7. Graphic Artist (generate image with SDXL locally)
    8. Save output
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.orchestrator import create_factory_graph
from utils.obsidian_io import test_connection, get_ceo_profile
from setup_profile import load_profile


def main():
    # Load profile from profile.yaml
    profile = load_profile()
    
    if not profile:
        print("⚠️  No profile found! Run the setup wizard first:\n")
        print("    python setup_profile.py\n")
        sys.exit(1)

    ceo_name = profile.get("name", "Unknown")
    
    print("=" * 60)
    print(f"🏭 {ceo_name.upper()}'S BRANDING FACTORY")
    print("=" * 60)
    print()

    # Step 1: Test Obsidian Connection (optional enhancement)
    print("🔌 Checking Obsidian Vault...")
    vault_connected = test_connection()
    print()

    # Step 2: Build CEO Profile from profile.yaml (primary) + Obsidian (optional overlay)
    print("👤 Loading Profile...")
    ceo_profile = {
        "name": profile.get("name"),
        "company": profile.get("company"),
        "role": profile.get("role", "CEO"),
        "industry": profile.get("industry", ""),
        "topics": profile.get("topics", []),
        "tone": profile.get("tone", "Direct, bold, eye-level"),
        "stories": profile.get("stories", []),
        "expertise": profile.get("expertise", {}),
        "banned_words": profile.get("banned_words", []),
        "preferred_words": profile.get("preferred_words", []),
    }

    # Optionally overlay Obsidian data if connected
    if vault_connected:
        obsidian_profile = get_ceo_profile()
        if obsidian_profile:
            # Obsidian enriches but doesn't override profile.yaml
            for key, val in obsidian_profile.items():
                if val and not ceo_profile.get(key):
                    ceo_profile[key] = val

    print(f"   👤 CEO: {ceo_profile.get('name')}")
    print(f"   🏢 Company: {ceo_profile.get('company')}")
    print(f"   🎯 Topics: {', '.join(ceo_profile.get('topics', []))}")
    print()

    # Step 3: Build initial state
    initial_state = {
        "ceo_profile": ceo_profile,
        "voice_dna": "",  # loaded by load_context node
        "icp_profile": "",  # loaded by load_context node
        "trend_report": "",
        "ideas": [],
        "selected_idea": "",
        "post_drafts": {},
        "image_path": "",
        "validation_results": "",
        "iteration_count": 0,
        "learning_context": "",
    }

    # Step 4: Create and run the agentic graph
    print("🚀 Starting the Branding Factory...\n")
    graph = create_factory_graph()
    final_state = graph.invoke(initial_state)

    # Step 5: Print final summary
    print("\n" + "=" * 60)
    print("🎉 FACTORY RUN COMPLETE!")
    print("=" * 60)
    print(f"   📊 Validation: {final_state.get('validation_results', 'N/A')}")
    print(f"   🖼️  Image: {final_state.get('image_path', 'None')}")
    print(f"   🔄 Iterations: {final_state.get('iteration_count', 0)}")
    print()

    drafts = final_state.get("post_drafts", {})
    if drafts:
        print("📝 FINAL DRAFTS PREVIEW:")
        print("-" * 40)
        for platform, content in drafts.items():
            print(f"\n🔹 {platform.upper()}:")
            print(f"   {content[:150]}...")
    print()
    print("💡 Open Obsidian to review and edit your drafts!")
    print("=" * 60)


if __name__ == "__main__":
    main()
