"""
Validator Agent — Gatekeeper (Agentic)
========================================
Two-phase quality control:

Phase 1 (Instant): Hard rule checks — regex/string for deterministic violations.
  → Platform specs, banned words, punctuation, missing sections

Phase 2 (LLM): Deep evaluation — intelligent judgment only an agent can make.
  → The Lior Test, eye-level tone, engagement quality, narrative hook strength,
    ICP fit, Voice DNA alignment, specific rewrite instructions

Returns PASS or FAIL with detailed, actionable feedback
that the Creator agent uses to improve the next draft in the retry loop.
"""

import os
import re
import ollama
from openai import OpenAI

XAI_API_KEY = os.getenv("XAI_API_KEY")


# ============================================================
# Hard rules — fast, deterministic checks
# ============================================================

BANNED_WORDS = [
    "leverage", "optimize", "synergize", "utilize", "implement",
    "innovative", "cutting-edge", "best-in-class", "game-changer", "game-changers",
    "very", "quite", "somewhat",
    "journey", "passionate about", "excited to announce",
    "hustle", "grind", "rise and grind",
]

CONDESCENDING_PATTERNS = [
    "not because i have more time than you",
    "here's what most people miss",
    "here's what most founders get wrong",
    "i want to talk about",
    "let me explain",
    "you need to understand",
    "the truth is",
    "wake up",
]

PUNCTUATION_VIOLATIONS = [
    ("\u2014", "em dash (use single dash with space: ' - ')"),
    ("--", "double dash (use single dash with space: ' - ')"),
    ("\u201c", "curly left quote (use straight quotes)"),
    ("\u201d", "curly right quote (use straight quotes)"),
    ("\u2018", "curly left single quote (use straight quotes)"),
    ("\u2019", "curly right single quote (use straight quotes)"),
]


def _phase1_hard_checks(drafts: dict) -> list[str]:
    """Phase 1: Instant deterministic checks. Returns list of errors."""
    errors = []

    # --- X (Twitter) ---
    x_post = drafts.get("x", "")
    if x_post:
        if len(x_post) > 280:
            errors.append(f"X post is {len(x_post)}/280 chars. Shorten it.")
        if len(x_post) < 50:
            errors.append("X post is too short. Needs more substance.")
    else:
        errors.append("X post is MISSING.")

    # --- LinkedIn ---
    li_post = drafts.get("linkedin", "")
    if li_post:
        if "\n\n" not in li_post[:200] and "\n" not in li_post[:200]:
            errors.append("LinkedIn: No line break in first 200 chars. Needs a 'See More' fold after the hook.")
        if len(li_post) < 100:
            errors.append("LinkedIn post is too short. Needs 3-5 dense paragraphs.")
        first_line = li_post.split("\n")[0]
        if len(first_line) > 200:
            errors.append(f"LinkedIn hook is {len(first_line)} chars. Must be ONE line (max ~150).")
    else:
        errors.append("LinkedIn post is MISSING.")

    # --- Instagram ---
    ig_slides = drafts.get("instagram_slides", "")
    if ig_slides:
        slide_count = ig_slides.lower().count("slide")
        if slide_count < 4:
            errors.append(f"Instagram carousel: Only {slide_count} slides detected. Need exactly 5.")
    else:
        errors.append("Instagram carousel slides are MISSING.")

    if not drafts.get("instagram_caption", ""):
        errors.append("Instagram caption is MISSING.")

    # --- Vocabulary ---
    combined_text = " ".join(drafts.values())
    combined_lower = combined_text.lower()

    for word in BANNED_WORDS:
        if word in combined_lower:
            errors.append(f"Banned word '{word}' detected. Lior NEVER uses this word. Remove or replace.")

    # --- Punctuation ---
    for char, desc in PUNCTUATION_VIOLATIONS:
        if char in combined_text:
            errors.append(f"Punctuation violation: {desc}. Replace all instances.")

    # --- Condescension patterns ---
    for pattern in CONDESCENDING_PATTERNS:
        if pattern in combined_lower:
            errors.append(f"Condescending pattern: '{pattern}'. Rewrite at eye-level, as a peer.")

    # --- Rule of 3 ---
    numbered_steps = re.findall(r"^\s*\d+[\.\)]\s", combined_text, re.MULTILINE)
    if len(numbered_steps) > 3:
        step_numbers = [
            int(re.match(r"\s*(\d+)", s).group(1))
            for s in numbered_steps
            if re.match(r"\s*(\d+)", s)
        ]
        if max(step_numbers, default=0) > 3:
            errors.append(
                f"Rule of 3 violation: Found {max(step_numbers)} numbered steps. "
                "Lior's frameworks ALWAYS use exactly 3."
            )

    return errors


# ============================================================
# Phase 2: LLM deep evaluation
# ============================================================

def _phase2_llm_evaluation(drafts: dict, voice_dna: str, icp_profile: str, ceo_name: str) -> dict:
    """
    Phase 2: LLM reads the drafts and evaluates them as an intelligent gatekeeper.
    Returns: {"verdict", "scores", "avg_score", "feedback", "rewrite_instructions", "full_evaluation"}
    """
    combined_drafts = ""
    for platform, content in drafts.items():
        combined_drafts += f"\n=== {platform.upper()} ===\n{content}\n"

    prompt = f"""You are the Gatekeeper for {ceo_name}'s personal brand content.
Your job: evaluate these social media drafts RUTHLESSLY against {ceo_name}'s voice and brand rules.
You are NOT the writer. You are the quality gate. Be specific and actionable.

=== VOICE DNA (the rules these drafts MUST follow) ===
{voice_dna[:2500]}

=== TARGET AUDIENCE (ICP) ===
{icp_profile[:1000]}

=== DRAFTS TO EVALUATE ===
{combined_drafts}

Evaluate each draft on these 7 criteria. Score each 1-5:

1. THE LIOR TEST: Could ONLY {ceo_name} write this? (1=generic advice anyone could say, 5=unmistakably his)
2. EYE-LEVEL TONE: Is it peer-to-peer? (1=guru/condescending, 5=completely eye-level)
3. HOOK STRENGTH: Would this stop the scroll? (1=boring/generic, 5=can't-not-click)
4. VOICE ACCURACY: Does it match the Voice DNA patterns? (1=generic corporate, 5=nails his exact voice)
5. ICP FIT: Would the target audience engage? (1=wrong audience, 5=bullseye for their pain points)
6. ENGAGEMENT POTENTIAL: Will people comment/share/debate? (1=no friction, 5=debate-starter)
7. SPECIFICITY: Are there concrete details, numbers, time anchors, stories? (1=vague platitudes, 5=vivid and specific)

SCORING RULES:
- If ALL scores are 4+: PASS
- If ANY score is 1-2: FAIL
- If scores are mixed 3-4: Use your judgment but lean toward FAIL (quality bar is HIGH)

RESPOND IN EXACTLY THIS FORMAT:

SCORES:
- Lior Test: [1-5] — [one line explanation]
- Eye-Level Tone: [1-5] — [one line explanation]
- Hook Strength: [1-5] — [one line explanation]
- Voice Accuracy: [1-5] — [one line explanation]
- ICP Fit: [1-5] — [one line explanation]
- Engagement Potential: [1-5] — [one line explanation]
- Specificity: [1-5] — [one line explanation]

VERDICT: [PASS or FAIL]

FEEDBACK: [2-3 sentences on what's working well and what's not]

REWRITE_INSTRUCTIONS: [If FAIL: Give the writer SPECIFIC, ACTIONABLE instructions to fix each issue. Reference exact phrases or lines to change, and suggest alternatives. Be a tough editor, not vague. If PASS: Write "No changes needed — ready for Reut's final review."]"""

    print("   🧠 Gatekeeper: Deep evaluation with LLM...")
    result_text = _generate_with_llm(prompt)

    # Parse the LLM response
    verdict = "FAIL"  # default conservative
    upper = result_text.upper()
    if "VERDICT: PASS" in upper or "VERDICT:PASS" in upper:
        verdict = "PASS"

    # Extract scores
    scores = {}
    for line in result_text.split("\n"):
        line_stripped = line.strip()
        if line_stripped.startswith("- ") and ":" in line_stripped:
            parts = line_stripped[2:].split(":")
            if len(parts) >= 2:
                try:
                    name = parts[0].strip()
                    score_text = parts[1].strip()
                    score = int(score_text[0]) if score_text and score_text[0].isdigit() else 0
                    if 1 <= score <= 5:
                        scores[name] = score
                except (ValueError, IndexError):
                    pass

    avg_score = round(sum(scores.values()) / len(scores), 1) if scores else 0

    # Extract rewrite instructions
    rewrite_instructions = ""
    for marker in ["REWRITE_INSTRUCTIONS:", "REWRITE INSTRUCTIONS:"]:
        if marker in result_text:
            rewrite_instructions = result_text.split(marker)[-1].strip()
            break

    # Extract feedback
    feedback = ""
    if "FEEDBACK:" in result_text:
        feedback_section = result_text.split("FEEDBACK:")[-1]
        for stop_marker in ["REWRITE_INSTRUCTIONS:", "REWRITE INSTRUCTIONS:"]:
            if stop_marker in feedback_section:
                feedback_section = feedback_section.split(stop_marker)[0]
        feedback = feedback_section.strip()

    return {
        "verdict": verdict,
        "scores": scores,
        "avg_score": avg_score,
        "feedback": feedback,
        "rewrite_instructions": rewrite_instructions,
        "full_evaluation": result_text,
    }


def _generate_with_llm(prompt: str) -> str:
    """Use Grok (fast, remote) if available, otherwise fall back to Ollama."""
    if XAI_API_KEY:
        print("   🧠 Gatekeeper: Evaluating with Grok-3 (remote)...")
        try:
            client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
            response = client.chat.completions.create(
                model="grok-3",
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"   \u26a0\ufe0f  Grok failed ({e}), falling back to Ollama...")

    print("   🧠 Gatekeeper: Evaluating with Ollama llama3 (local)...")
    response = ollama.generate(model="llama3", prompt=prompt)
    return response["response"]


# ============================================================
# Main entry point
# ============================================================

def run_validator_agent(state: dict):
    """
    Gatekeeper Agent — Two-phase quality control.

    Phase 1 (instant): Hard-rule checks (banned words, platform specs, punctuation)
    Phase 2 (LLM): Deep evaluation (Lior Test, tone, engagement, voice accuracy)

    Returns actionable feedback that the Creator uses to improve drafts on retry.
    """
    print("--- \u2705 AGENT: VALIDATOR (Gatekeeper \u2014 Two-Phase Quality Control) ---")

    drafts = state.get("post_drafts", {})
    voice_dna = state.get("voice_dna", "")
    icp_profile = state.get("icp_profile", "")
    ceo = state.get("ceo_profile", {})
    ceo_name = ceo.get("name", "Lior Pozin")
    iteration = state.get("iteration_count", 0)

    if not drafts:
        print("   \u274c No drafts to validate!")
        return {
            "validation_results": "FAIL: No drafts provided. Creator must generate drafts first.",
            "iteration_count": iteration,
        }

    # == Phase 1: Hard rule checks (instant) ==
    print("   \u26a1 Phase 1: Hard rule checks...")
    hard_errors = _phase1_hard_checks(drafts)

    if hard_errors:
        print(f"   \U0001f6ab Phase 1: {len(hard_errors)} hard violations found")
        for e in hard_errors:
            print(f"      \u274c {e}")
    else:
        print("   \u2705 Phase 1: All hard rules passed")

    # == Phase 2: LLM deep evaluation ==
    print("   🧠 Phase 2: Deep LLM evaluation...")
    llm_eval = _phase2_llm_evaluation(drafts, voice_dna, icp_profile, ceo_name)

    verdict = llm_eval["verdict"]
    scores = llm_eval["scores"]
    avg_score = llm_eval["avg_score"]
    feedback = llm_eval["feedback"]
    rewrite_instructions = llm_eval["rewrite_instructions"]

    # Print scores
    print(f"\n   \U0001f4ca GATEKEEPER SCORES (avg: {avg_score}/5):")
    for name, score in scores.items():
        emoji = "\u2705" if score >= 4 else "\u26a0\ufe0f" if score == 3 else "\u274c"
        print(f"      {emoji} {name}: {score}/5")

    print(f"\n   \U0001f4ac Feedback: {feedback[:200]}")

    # == Final verdict ==
    if hard_errors or verdict == "FAIL":
        all_feedback_parts = []

        if hard_errors:
            all_feedback_parts.append(
                "HARD RULE VIOLATIONS:\n" + "\n".join(f"- {e}" for e in hard_errors)
            )

        if verdict == "FAIL" and rewrite_instructions:
            all_feedback_parts.append(
                f"GATEKEEPER EVALUATION (avg score: {avg_score}/5):\n{feedback}"
            )
            all_feedback_parts.append(
                f"SPECIFIC REWRITE INSTRUCTIONS:\n{rewrite_instructions}"
            )
        elif verdict == "FAIL":
            all_feedback_parts.append(
                f"GATEKEEPER EVALUATION (avg score: {avg_score}/5):\n{feedback}"
            )

        combined_feedback = "\n\n".join(all_feedback_parts)
        total_issues = len(hard_errors) + (1 if verdict == "FAIL" else 0)
        print(f"\n   \U0001f6ab VERDICT: FAIL \u2014 {total_issues} issue(s) (iteration {iteration})")

        return {
            "validation_results": f"FAIL:\n{combined_feedback}",
            "validation_scores": scores,
            "iteration_count": iteration,
        }

    # PASS
    print(f"\n   \u2705 VERDICT: PASS \u2014 All checks cleared! (avg score: {avg_score}/5)")
    print(f"   \U0001f4ac {feedback[:150]}")

    return {
        "validation_results": f"PASS (score: {avg_score}/5): {feedback}",
        "validation_scores": scores,
    }
