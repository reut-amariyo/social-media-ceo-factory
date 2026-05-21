"""
Creator Agent — Copywriter (Social Media)
===========================================
Generates multi-platform drafts in the CEO's exact voice.
Loads platform-specific writing skills from agents_information/skills/creator_platform_guide.md

The Creator MUST read and follow the platform guide before writing any content.
"""

import os
import ollama
from openai import OpenAI
from utils.obsidian_io import get_learning_log, get_past_posts

XAI_API_KEY = os.getenv("XAI_API_KEY")

# Load skills at import time
def _load_skill(filename: str) -> str:
    """Load a skill file from agents_information/skills/."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "agents_information", "skills", filename)
    if os.path.exists(path):
        with open(path) as f:
            return f.read()
    # Try alternate path (running from project root)
    alt_path = os.path.join("agents_information", "skills", filename)
    if os.path.exists(alt_path):
        with open(alt_path) as f:
            return f.read()
    return ""

PLATFORM_SKILL = _load_skill("creator_platform_guide.md")
HOOK_WRITING_SKILL = _load_skill("hook_writing.md")
STORYTELLING_SKILL = _load_skill("storytelling.md")


def _generate_with_best_llm(prompt: str, agent_name: str = "Creator") -> str:
    """Use Grok (fast, remote) if available, otherwise fall back to Ollama (local)."""
    if XAI_API_KEY:
        print(f"   🧠 {agent_name}: Generating with Grok-3 (remote — fast)...")
        try:
            client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
            response = client.chat.completions.create(
                model="grok-3",
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"   ⚠️  Grok failed ({e}), falling back to Ollama...")

    print(f"   🧠 {agent_name}: Generating with Ollama llama3 (local — slower)...")
    response = ollama.generate(model="llama3", prompt=prompt)
    return response["response"]


# Vocabulary rules — loaded from profile or defaults
VOCAB_NEVER_DEFAULT = '"leverage," "optimize," "synergize," "innovative," "hustle," "grind," "journey," "passionate about," "excited to announce"'


def run_creator_agent(state: dict):
    """
    Agent 3: The Creative Director / Copywriter
    - Takes the selected idea and generates multi-platform drafts
    - Uses Voice DNA + past posts for exact style mimicking
    - Generates: X post, LinkedIn post, Instagram carousel
    """
    print("--- ✍️ AGENT: CREATOR (Copywriter — Writing in Your Voice) ---")

    ceo = state.get("ceo_profile", {})
    ceo_name = ceo.get("name", "Unknown")
    tone = ceo.get("tone", "Direct, bold, eye-level, no-BS")
    banned_words = ceo.get("banned_words", [])
    preferred_words = ceo.get("preferred_words", [])

    selected_idea = state.get("selected_idea", "")
    trend_report = state.get("trend_report", "")
    validation_feedback = state.get("validation_results", "")

    # Load Voice DNA from state (the primary style guide)
    voice_dna = state.get("voice_dna", "")
    icp_profile = state.get("icp_profile", "")

    # Load past posts for few-shot style mimicking
    past_posts = get_past_posts(limit=5)
    learning_log = state.get("learning_context", "") or get_learning_log()
    past_posts_text = "\n---\n".join(past_posts[:3]) if past_posts else "No past posts available."

    # If retrying after validation failure, include feedback
    retry_instructions = ""
    if validation_feedback and "FAIL" in validation_feedback:
        # Extract specific banned words mentioned in feedback
        banned_words_found = []
        for word in ["leverage", "optimize", "synergize", "utilize", "implement",
                     "innovative", "cutting-edge", "best-in-class", "game-changer",
                     "very", "quite", "somewhat", "journey", "passionate about",
                     "excited to announce", "hustle", "grind"]:
            if word.lower() in (validation_feedback.lower() + " " + 
                               str(state.get("post_drafts", {}))).lower():
                banned_words_found.append(word)
        
        banned_warning = ""
        if banned_words_found:
            banned_warning = f"""
🚨 ABSOLUTE BAN — These words appeared in your last draft and MUST NOT appear again:
{', '.join(f'"{w}"' for w in banned_words_found)}
Do a final scan of your output. If ANY of these words appear, replace them immediately.
"""
        retry_instructions = f"""
⚠️ CRITICAL: The previous draft was REJECTED. You MUST fix these issues or the post cannot be published:
{validation_feedback}
{banned_warning}
"""
        print(f"   🔄 Retrying with feedback: {validation_feedback[:100]}...")

    # Voice DNA excerpt (truncate to fit context window)
    voice_section = voice_dna[:3000] if voice_dna else ""
    
    # Build vocabulary rules from profile
    vocab_never = ', '.join(f'"{w}"' for w in banned_words) if banned_words else VOCAB_NEVER_DEFAULT
    vocab_use = ', '.join(f'"{w}"' for w in preferred_words) if preferred_words else ""

    # Load the platform writing skill guide
    platform_guide = PLATFORM_SKILL if PLATFORM_SKILL else "Write platform-native posts for X (280 chars max), LinkedIn (3-8 paragraphs), and Instagram (5-slide carousel + caption)."

    # Load additional skills
    hook_skill = HOOK_WRITING_SKILL
    story_skill = STORYTELLING_SKILL

    prompt = f"""You are {ceo_name}'s personal copywriter. Write in their EXACT voice.

=== YOUR SKILL: PLATFORM WRITING GUIDE ===
Read this CAREFULLY. It defines how you write for each platform.
Follow these rules precisely — each platform must be DISTINCT, not cross-posted.

{platform_guide}

=== YOUR SKILL: HOOK WRITING ===
Use these techniques for opening lines. Every post MUST start with a strong hook.

{hook_skill}

=== YOUR SKILL: STORYTELLING ===
When the idea lends itself to narrative, apply this framework.

{story_skill}

=== CEO VOICE DNA ===
{voice_section}

=== VOICE CONSTRAINTS ===
TONE: {tone}. Eye-level, NEVER condescending.
- Every sentence must pass: "Could this be read as 'I'm better than you'?" If yes, rewrite.

VOCABULARY:
- PREFERRED: {vocab_use if vocab_use else "Use natural language"}
- NEVER USE: {vocab_never}

=== PAST SUCCESSFUL POSTS (mimic this style) ===
{past_posts_text}

=== GOLDEN RULES FROM PAST PERFORMANCE ===
{learning_log[:1500]}

=== SELECTED CONTENT IDEA ===
{selected_idea}

=== TREND CONTEXT ===
{trend_report[:1000]}
{retry_instructions}

Now execute. Write platform-native drafts following the Platform Writing Guide above.
Each platform MUST be distinct — different structure, different length, different energy.

Format EXACTLY like this:
X: [your X post]
LINKEDIN: [your LinkedIn post]
INSTAGRAM_SLIDES:
Slide 1: [text]
Slide 2: [text]
Slide 3: [text]
Slide 4: [text]
Slide 5: [text]
INSTAGRAM_CAPTION: [caption]"""

    print("   🧠 Generating drafts...")
    content = _generate_with_best_llm(prompt, agent_name="Creator")

    # Parse the response into platform-specific drafts
    drafts = _parse_drafts(content)

    print(f"   ✅ Generated drafts for {len(drafts)} platforms")
    for platform, text in drafts.items():
        preview = text[:80].replace("\n", " ")
        print(f"      📝 {platform}: {preview}...")

    # --- Self-evaluation: Creator checks its own work before sending to Validator ---
    print("   🔍 Creator self-check: evaluating own drafts...")
    self_check = _self_evaluate(drafts, ceo_name, voice_dna, selected_idea)
    if self_check:
        print(f"   🔄 Self-check found issues — rewriting...")
        print(f"      📝 {self_check[:150]}...")
        # Rewrite with self-feedback
        retry_prompt = prompt + f"""

⚠️ SELF-CHECK: Before submitting, I reviewed my own drafts and found these issues:
{self_check}

Rewrite ALL drafts fixing these issues. Return in the same format."""
        content2 = _generate_with_best_llm(retry_prompt, agent_name="Creator (self-fix)")
        drafts2 = _parse_drafts(content2)
        if drafts2 and len(drafts2) >= len(drafts):
            drafts = drafts2
            print("   ✅ Self-fix applied — improved drafts ready")
        else:
            print("   ⏭️ Self-fix parse failed — keeping original drafts")
    else:
        print("   ✅ Self-check passed — drafts look good")

    # Final deterministic scan: remove any remaining banned words
    drafts = _strip_banned_words(drafts)

    return {
        "post_drafts": drafts,
        "iteration_count": state.get("iteration_count", 0) + 1,
    }


def _strip_banned_words(drafts: dict) -> dict:
    """Deterministic post-processing: replace banned words with safe alternatives."""
    import re
    replacements = {
        r'\bvery\b': 'really',
        r'\bleverage\b': 'use',
        r'\boptimize\b': 'improve',
        r'\butilize\b': 'use',
        r'\bsynergize\b': 'combine',
        r'\bimplement\b': 'build',
        r'\binnovative\b': 'new',
        r'\bcutting-edge\b': 'sharp',
        r'\bgame-changer\b': 'shift',
        r'\bhustle\b': 'work',
        r'\bgrind\b': 'push',
        r'\bjourney\b': 'path',
    }
    cleaned = {}
    for platform, text in drafts.items():
        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        cleaned[platform] = text
    return cleaned


def _self_evaluate(drafts: dict, ceo_name: str, voice_dna: str, idea: str) -> str | None:
    """Creator self-evaluates its own drafts. Returns issues found, or None if clean."""
    combined = "\n\n".join(f"[{k.upper()}]: {v}" for k, v in drafts.items())

    prompt = f"""You just wrote these social media drafts for {ceo_name}. 
Now step back and evaluate your OWN work critically. Be honest.

VOICE DNA RULES:
{voice_dna[:1000]}

THE IDEA:
{idea[:500]}

YOUR DRAFTS:
{combined}

Check for these common mistakes:
1. Did I use any banned words (leverage, optimize, hustle, grind, journey, innovative)?
2. Did I use em dash (—) instead of single dash with space ( - )?
3. Did I use curly quotes instead of straight quotes?
4. Does the hook read as ONE line or did I make it a paragraph?
5. Is there any guru energy / condescending tone?
6. Did I use numbered steps? If so, are there exactly 3?
7. Is there a specific time anchor (not vague "years ago")?
8. Does the X post fit in 280 chars?

If you find ANY issues, list them briefly (max 5 bullet points).
If everything looks clean, respond with exactly: CLEAN"""

    result = _generate_with_best_llm(prompt, agent_name="Creator self-check")
    if result.strip().upper() == "CLEAN" or "clean" in result.strip().lower()[:20]:
        return None
    return result


def _parse_drafts(content: str) -> dict:
    """Parse the LLM response into a dict of platform drafts."""
    drafts = {}

    # Extract X post
    if "X:" in content:
        x_start = content.index("X:") + 2
        x_end = content.find("LINKEDIN:") if "LINKEDIN:" in content else len(content)
        drafts["x"] = content[x_start:x_end].strip()

    # Extract LinkedIn post
    if "LINKEDIN:" in content:
        li_start = content.index("LINKEDIN:") + 9
        li_end = content.find("INSTAGRAM_SLIDES:") if "INSTAGRAM_SLIDES:" in content else len(content)
        drafts["linkedin"] = content[li_start:li_end].strip()

    # Extract Instagram slides
    if "INSTAGRAM_SLIDES:" in content:
        ig_start = content.index("INSTAGRAM_SLIDES:") + 17
        ig_end = content.find("INSTAGRAM_CAPTION:") if "INSTAGRAM_CAPTION:" in content else len(content)
        drafts["instagram_slides"] = content[ig_start:ig_end].strip()

    # Extract Instagram caption
    if "INSTAGRAM_CAPTION:" in content:
        cap_start = content.index("INSTAGRAM_CAPTION:") + 18
        drafts["instagram_caption"] = content[cap_start:].strip()

    # Fallback if parsing fails
    if not drafts:
        drafts = {"x": content, "linkedin": content}

    return drafts