#!/usr/bin/env python3
"""
🧑‍💼 Personal Branding Factory — Profile Setup
================================================
First-run wizard that creates your personal profile.
Run this once before using the system.

Usage:
    python setup_profile.py
"""

import os
import yaml
from pathlib import Path

PROFILE_PATH = Path("profile.yaml")
ENV_PATH = Path(".env")


def run_setup():
    print("=" * 60)
    print("🏭 PERSONAL BRANDING FACTORY — SETUP WIZARD")
    print("=" * 60)
    print()
    print("Let's set up your personal brand profile.")
    print("This takes about 2 minutes. You can update it later.\n")

    # --- Basic Info ---
    print("─" * 40)
    print("📋 BASIC INFO")
    print("─" * 40)
    name = input("Your full name: ").strip()
    company = input("Your company name: ").strip()
    role = input("Your role (e.g., CEO, Founder, CTO): ").strip()
    industry = input("Your industry (e.g., E-commerce, SaaS, FinTech): ").strip()

    # --- Topics ---
    print()
    print("─" * 40)
    print("🎯 CONTENT TOPICS (what you talk about)")
    print("─" * 40)
    print("Enter 3-6 topics you want to post about, comma-separated.")
    print("Example: Scaling, AI in Business, Pricing Strategy, Leadership")
    topics_raw = input("Your topics: ").strip()
    topics = [t.strip() for t in topics_raw.split(",") if t.strip()]

    # --- Tone ---
    print()
    print("─" * 40)
    print("🎤 YOUR VOICE / TONE")
    print("─" * 40)
    print("Describe how you write on social media (2-5 adjectives).")
    print("Example: Direct, bold, eye-level, no-BS, action-oriented")
    tone = input("Your tone: ").strip()

    # --- Background / Story ---
    print()
    print("─" * 40)
    print("📖 YOUR STORY (key milestones)")
    print("─" * 40)
    print("List 3-5 career milestones that make you unique.")
    print("Press Enter after each. Type 'done' when finished.")
    print("Example: Built company from $0 to $10M ARR in 3 years")
    stories = []
    while True:
        story = input(f"  Milestone {len(stories) + 1}: ").strip()
        if story.lower() == "done" or (not story and len(stories) >= 1):
            break
        if story:
            stories.append(story)

    # --- Expertise ---
    print()
    print("─" * 40)
    print("💡 YOUR EXPERTISE AREAS")
    print("─" * 40)
    print("List 3-5 things you're an expert at (one per line).")
    print("Format: area: what you did")
    print("Example: pricing_strategy: Grew revenue 3x by switching to outcome-based pricing")
    print("Type 'done' when finished.")
    expertise = {}
    while True:
        entry = input(f"  Expertise {len(expertise) + 1}: ").strip()
        if entry.lower() == "done" or (not entry and len(expertise) >= 1):
            break
        if ":" in entry:
            key, value = entry.split(":", 1)
            expertise[key.strip()] = value.strip()
        elif entry:
            expertise[entry.lower().replace(" ", "_")] = entry

    # --- Banned Words ---
    print()
    print("─" * 40)
    print("🚫 WORDS YOU NEVER USE (optional)")
    print("─" * 40)
    print("Any words/phrases that don't fit your brand? Comma-separated.")
    print("Example: leverage, synergize, hustle, grind")
    print("Press Enter to skip (we'll use sensible defaults).")
    banned_raw = input("Banned words: ").strip()
    banned_words = [w.strip() for w in banned_raw.split(",") if w.strip()] if banned_raw else []

    # --- Preferred Words ---
    print()
    print("Words you LOVE to use? Comma-separated (or Enter to skip).")
    preferred_raw = input("Preferred words: ").strip()
    preferred_words = [w.strip() for w in preferred_raw.split(",") if w.strip()] if preferred_raw else []

    # --- Content Focus ---
    print()
    print("─" * 40)
    print("🔎 CONTENT FOCUS (what should the Scout look for?)")
    print("─" * 40)
    print("Keywords the Scout uses to filter trending news for you.")
    print("Comma-separated. Press Enter to use your topics as focus.")
    print("Example: AI agents, developer tools, SaaS infrastructure")
    focus_raw = input("Content focus: ").strip()
    content_focus = [f.strip() for f in focus_raw.split(",") if f.strip()] if focus_raw else topics

    # --- X Accounts ---
    print()
    print("─" * 40)
    print("🐦 X ACCOUNTS TO MONITOR (optional)")
    print("─" * 40)
    print("Usernames (without @) of people in your space, comma-separated.")
    print("Example: swyx, sama, patio11")
    print("Press Enter to skip.")
    x_raw = input("X accounts: ").strip()
    x_accounts = [a.strip().lstrip("@") for a in x_raw.split(",") if a.strip()] if x_raw else []

    # --- Build profile ---
    profile = {
        "name": name,
        "company": company,
        "role": role,
        "industry": industry,
        "topics": topics,
        "tone": tone,
        "stories": stories,
        "expertise": expertise,
        "banned_words": banned_words,
        "preferred_words": preferred_words,
        "content_focus": content_focus,
        "x_accounts": x_accounts,
    }

    # Save
    with open(PROFILE_PATH, "w") as f:
        yaml.dump(profile, f, default_flow_style=False, allow_unicode=True)

    print()
    print("=" * 60)
    print(f"✅ Profile saved to: {PROFILE_PATH}")
    print("=" * 60)
    print()
    print("Next steps:")
    print(f"  1. Review/edit {PROFILE_PATH} anytime")
    print("  2. Set up your .env file (API keys)")
    print("  3. Run: python main.py")
    print()

    # --- Create .env if it doesn't exist ---
    if not ENV_PATH.exists():
        print("─" * 40)
        print("🔑 API KEYS SETUP")
        print("─" * 40)
        print()
        print("The system needs at least ONE of these:")
        print("  • XAI_API_KEY (Grok — fast, recommended)")
        print("  • Or just Ollama installed locally (free, slower)")
        print()
        print("Optional:")
        print("  • SERPAPI_API_KEY (Google search — 100 free/month)")
        print()
        
        xai_key = input("XAI_API_KEY (or Enter to skip): ").strip()
        serp_key = input("SERPAPI_API_KEY (or Enter to skip): ").strip()

        with open(ENV_PATH, "w") as f:
            f.write("# Personal Branding Factory — API Keys\n")
            f.write("# =====================================\n\n")
            f.write(f"XAI_API_KEY={xai_key}\n")
            f.write(f"SERPAPI_API_KEY={serp_key}\n")
            f.write("\n# Obsidian vault path (optional — for reading your writing style)\n")
            f.write("# OBSIDIAN_VAULT_PATH=/path/to/your/vault\n")
            f.write("# OBSIDIAN_SYSTEM_DIR=the-system-v5\n")

        print(f"\n✅ .env file created! Edit it anytime to add/change keys.")

    return profile


def load_profile() -> dict:
    """Load the user profile. Returns empty dict if not set up yet."""
    if not PROFILE_PATH.exists():
        return {}
    with open(PROFILE_PATH) as f:
        return yaml.safe_load(f) or {}


if __name__ == "__main__":
    run_setup()
