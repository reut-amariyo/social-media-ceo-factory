"""
Validator Agent — Gatekeeper
==============================
Quality control gate before publishing. Based on A-agents/gatekeeper-agent.md.

Checks:
1. Platform specs (X 280 chars, LinkedIn "See More" hook, Instagram 5 slides)
2. Voice DNA alignment (banned words, punctuation, tone)
3. The Lior Test: "Could only Lior say this?"
4. Eye-level tone check (no condescension, no guru energy)
5. Brand alignment (banned topics, off-ICP detection)
6. CTA / engagement hook presence
"""

import re


# Lior's banned vocabulary — from voice-dna.md
BANNED_WORDS = [
    "leverage", "optimize", "synergize", "utilize", "implement",
    "innovative", "cutting-edge", "best-in-class", "game-changer", "game-changers",
    "very", "quite", "somewhat",
    "journey", "passionate about", "excited to announce",
    "hustle", "grind", "rise and grind",
]

# Condescending patterns to flag
CONDESCENDING_PATTERNS = [
    "not because i have more time than you",
    "here's what most people miss",
    "here's what most founders get wrong",
    "i want to talk about",  # Never announce intent
    "let me explain",
    "you need to understand",
    "the truth is",
    "wake up",
]

# Punctuation violations
PUNCTUATION_VIOLATIONS = [
    ("—", "em dash (use single dash with space: ' - ')"),
    ("--", "double dash (use single dash with space: ' - ')"),
    ("\u201c", "curly left quote (use straight quotes)"),
    ("\u201d", "curly right quote (use straight quotes)"),
    ("\u2018", "curly left single quote (use straight quotes)"),
    ("\u2019", "curly right single quote (use straight quotes)"),
]


def run_validator_agent(state: dict):
    """
    Agent 5: The Gatekeeper / Validator
    Quality control gate — checks platform specs, voice DNA alignment, and brand fit.
    """
    print("--- ✅ AGENT: VALIDATOR (Gatekeeper — Quality Control) ---")
    drafts = state.get("post_drafts", {})
    voice_dna = state.get("voice_dna", "")
    errors = []

    # === 1. X (Twitter) Checks ===
    x_post = drafts.get("x", "")
    if x_post:
        if len(x_post) > 280:
            errors.append(f"❌ X post too long ({len(x_post)}/280 chars). Shorten it.")
        if len(x_post) < 50:
            errors.append("❌ X post too short. Needs more substance.")
        print(f"   🐦 X post: {len(x_post)}/280 chars")
    else:
        errors.append("❌ X post is missing.")

    # === 2. LinkedIn Checks ===
    li_post = drafts.get("linkedin", "")
    if li_post:
        # Check for "See More" hook (needs a line break in first 150 chars)
        if "\n\n" not in li_post[:150] and "\n" not in li_post[:150]:
            errors.append("❌ LinkedIn: Needs a 'See More' hook — add a line break in the first 2 lines.")
        if len(li_post) < 100:
            errors.append("❌ LinkedIn post too short. Needs more depth.")
        # Check hook is ONE line (not a paragraph)
        first_line = li_post.split("\n")[0]
        if len(first_line) > 200:
            errors.append("❌ LinkedIn: Hook must be ONE line (max ~150 chars). Currently too long.")
        print(f"   💼 LinkedIn post: {len(li_post)} chars")
    else:
        errors.append("❌ LinkedIn post is missing.")

    # === 3. Instagram Checks ===
    ig_slides = drafts.get("instagram_slides", "")
    ig_caption = drafts.get("instagram_caption", "")
    if ig_slides:
        slide_count = ig_slides.lower().count("slide")
        if slide_count < 4:
            errors.append(f"❌ Instagram carousel: Only {slide_count} slides found, need at least 5.")
        print(f"   📸 Instagram: {slide_count} slides detected")
    else:
        errors.append("❌ Instagram carousel slides are missing.")

    if not ig_caption:
        errors.append("❌ Instagram caption is missing.")

    # === 4. Voice DNA Checks ===
    combined_text = " ".join(drafts.values())
    combined_lower = combined_text.lower()

    # 4a. Banned vocabulary
    for word in BANNED_WORDS:
        if word in combined_lower:
            errors.append(f"❌ Voice violation: '{word}' is banned. Lior never uses this word.")

    # 4b. Punctuation violations
    for char, desc in PUNCTUATION_VIOLATIONS:
        if char in combined_text:
            errors.append(f"❌ Punctuation violation: Found {desc}.")

    # 4c. Condescension / guru energy check
    for pattern in CONDESCENDING_PATTERNS:
        if pattern in combined_lower:
            errors.append(f"❌ Eye-level violation: '{pattern}' sounds condescending. Rewrite at eye-level.")

    # 4d. Rule of 3 check (if numbered steps exist, must be exactly 3)
    numbered_steps = re.findall(r"^\s*\d+[\.\)]\s", combined_text, re.MULTILINE)
    if len(numbered_steps) > 3:
        # Check if they're framework steps (not just any numbered list)
        step_numbers = [int(re.match(r"\s*(\d+)", s).group(1)) for s in numbered_steps if re.match(r"\s*(\d+)", s)]
        if max(step_numbers, default=0) > 3:
            errors.append(f"❌ Rule of 3 violation: Found {max(step_numbers)} numbered steps. Lior's frameworks always use exactly 3.")

    # === 5. CTA / Engagement Hook Check ===
    cta_keywords = [
        "comment", "thoughts", "agree", "what do you think",
        "share your", "tell me", "let me know", "drop a",
        "do you", "have you", "would you", "what did i miss",
        "which one", "how do you",
    ]
    if not any(word in combined_lower for word in cta_keywords):
        errors.append("❌ Missing Engagement CTA: Posts should invite comments/discussion.")

    # === 6. The Lior Test ===
    # Check for generic advice that any competitor could write
    generic_signals = [
        "in today's fast-paced world",
        "in this day and age",
        "the future is",
        "it's no secret that",
        "we all know that",
        "it goes without saying",
    ]
    for signal in generic_signals:
        if signal in combined_lower:
            errors.append(f"❌ Lior Test FAIL: '{signal}' is generic. Could come from any LinkedIn account.")

    # === 7. Brand Alignment (from Voice DNA banned topics) ===
    if voice_dna:
        brand_errors = _check_brand_alignment(combined_lower, voice_dna)
        errors.extend(brand_errors)

    # === Result ===
    if errors:
        error_report = " | ".join(errors)
        print(f"   🚫 FAILED — {len(errors)} issues found")
        for e in errors:
            print(f"      {e}")
        return {
            "validation_results": f"FAIL: {error_report}",
            "iteration_count": state.get("iteration_count", 0),
        }

    print("   ✅ PASSED — All checks cleared! Ready for Reut's review.")
    return {"validation_results": "PASS"}


def _check_brand_alignment(text: str, voice_dna: str) -> list[str]:
    """Check if content conflicts with Voice DNA rules."""
    errors = []
    # Extract "What We're NOT" rules from voice DNA
    for line in voice_dna.split("\n"):
        lower = line.lower().strip()
        if any(kw in lower for kw in ["never", "avoid", "don't", "banned", "not talk", "what we're not"]):
            # Check for key concept words (longer than 4 chars)
            words = [w for w in lower.split() if len(w) > 5 and w not in ("never", "avoid", "don't", "should", "always")]
            for word in words[:2]:  # max 2 keywords per rule
                if word in text:
                    errors.append(f"❌ Brand alignment: Content mentions '{word}' — conflicts with Voice DNA rule")
                    break
    return errors