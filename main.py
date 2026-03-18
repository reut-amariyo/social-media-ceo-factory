#!/usr/bin/env python3
"""
🏭 Lior Pozin's Personal Branding Factory
==========================================
Agentic system that generates personalized social media content.
Built for Lior Pozin — CEO of AutoDS (acquired by Fiverr), BuildYourStore.ai, CreateUGC.AI.
Operated by Reut on her Mac.

Usage:
    python main.py

Flow:
    1. Load Context (Obsidian vault: Voice DNA + ICP + learning log)
    2. Scout (Google + Grok → trending topics, filtered for Lior's focus areas)
    3. Ideator (filter trends → 3 content angles with narrative hooks)
    4. Human Checkpoint (Reut picks her favorite)
    5. Creator (multi-platform drafts: X, LinkedIn, Instagram — in Lior's voice)
    6. Validator (quality control: eye-level tone, vocabulary, brand alignment)
    7. Graphic Artist (generate image with SDXL on M4)
    8. Save to Obsidian (O-output/ with ABC-TOM naming convention)
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


def main():
    print("=" * 60)
    print("🏭 LIOR POZIN'S BRANDING FACTORY")
    print("=" * 60)
    print()

    # Step 1: Test Obsidian Connection
    print("🔌 Checking Obsidian Vault...")
    vault_connected = test_connection()
    print()

    # Step 2: Load CEO Profile
    print("👤 Loading CEO Profile...")
    if vault_connected:
        ceo_profile = get_ceo_profile()
    else:
        ceo_profile = {}

    if not ceo_profile:
        print("   ⚠️  Using fallback CEO profile (update Obsidian vault for personalization)")
        ceo_profile = {
            "name": "Lior Pozin",
            "company": "AutoDS",
            "role": "CEO & Serial Entrepreneur",
            "industry": "E-commerce, SaaS, AI",
            "topics": [
                "Scaling",
                "Pricing Strategy",
                "Revenue Upselling",
                "Growth Hacking",
                "Branding",
                "AI in Business",
            ],
            "tone": "Direct, bold, eye-level, no-BS, action-oriented",
        }

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
