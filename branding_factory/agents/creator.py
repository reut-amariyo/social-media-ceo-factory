"""
Creator Agent — Copywriter (Social Media)
===========================================
Generates multi-platform drafts in Lior Pozin's exact voice.
Based on A-agents/copywriter-agent-social.md from the ABC-TOM v5 system.

Follows the 12-section style guide:
1. Hook Types  2. Sentence Architecture  3. Paragraph Rules  4. Structural Rules
5. Transitions  6. Vocabulary  7. Punctuation  8. Pronouns  9. Emotional Texture
10. Ending Patterns  11. Eye-Level Tone  12. Owner Editing Rules
"""

import os
import ollama
from openai import OpenAI
from utils.obsidian_io import get_learning_log, get_past_posts

XAI_API_KEY = os.getenv("XAI_API_KEY")


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


# Lior's vocabulary rules — embedded from voice-dna.md
VOCAB_USE = '"real," "just," "precisely," "A LOT" (caps), "gold," "ruthlessly," "noise," "infrastructure"'
VOCAB_NEVER = '"leverage," "optimize," "synergize," "innovative," "hustle," "grind," "journey," "passionate about," "excited to announce"'


def run_creator_agent(state: dict):
    """
    Agent 3: The Creative Director / Copywriter
    - Takes the selected idea and generates multi-platform drafts
    - Uses Voice DNA + past posts for exact style mimicking
    - Generates: X post, LinkedIn post, Instagram carousel
    """
    print("--- ✍️ AGENT: CREATOR (Copywriter — Writing in Lior's Voice) ---")

    ceo = state.get("ceo_profile", {})
    ceo_name = ceo.get("name", "Lior Pozin")
    tone = ceo.get("tone", "Direct, bold, eye-level, no-BS")

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
        retry_instructions = f"""
⚠️ IMPORTANT: The previous draft was REJECTED by the Gatekeeper. Fix these issues:
{validation_feedback}
"""
        print(f"   🔄 Retrying with feedback: {validation_feedback[:100]}...")

    # Voice DNA excerpt (truncate to fit context window)
    voice_section = voice_dna[:3000] if voice_dna else ""

    prompt = f"""You are {ceo_name}'s personal copywriter. Write in his EXACT voice.

=== VOICE DNA (follow these rules EXACTLY) ===
{voice_section}

=== CRITICAL WRITING RULES ===

TONE: {tone}. Eye-level, NEVER condescending.
- Every sentence must pass: "Could this be read as 'I'm better than you'?" If yes, rewrite.
- Absorb punch lines into paragraph flow (shared observation, NOT guru pronouncement)
- Use "but because" for humble framing

VOCABULARY:
- USE: {VOCAB_USE}
- NEVER USE: {VOCAB_NEVER}

PUNCTUATION:
- Single dash with space ( - ) for parenthetical. NEVER em dash. NEVER double dash (--)
- NEVER curly/smart quotes. Always straight quotes.
- Colon as reveal device: "My response was simple:"

STRUCTURE:
- The Rule of 3: Numbered frameworks ALWAYS use exactly 3 steps
- Hook is always ONE line. Never a paragraph.
- 1-3 lines per paragraph. Never more.
- Time anchoring: Include specific time reference ("9 years ago" not "years ago")
- Proof-Through-Specifics: Never claim ("I'm productive"). List evidence.

SENTENCE PATTERNS (use 2-3 per post):
1. The Reframe: "Doing it all isn't saving money. It's just choosing to pay with your time."
2. The Punch Line: Ultra-short after build-up. "Zero." / "No doubt."
3. The Direct Command: "Don't write a single line of code."
4. The Conditional Conviction: "If [condition], [bold command]."
5. The "I stopped..." Confession: Lists specific things given up.

ENDING PATTERNS:
- If the last line delivers clear insight, STOP. Don't force a reframe.
- Closing questions should be specific and either/or. Never generic "What do you think?"
- Glue closing question to final paragraph, not staged on its own line.

=== PAST SUCCESSFUL POSTS (mimic this style closely) ===
{past_posts_text}

=== GOLDEN RULES FROM PAST PERFORMANCE ===
{learning_log[:1500]}

=== SELECTED CONTENT IDEA ===
{selected_idea}

=== TREND CONTEXT ===
{trend_report[:1000]}
{retry_instructions}

Now write drafts for ALL THREE platforms:

=== X (TWITTER) ===
- MAX 280 characters. Hook-heavy. End with engagement question.
- 1-2 hashtags max.

=== LINKEDIN ===
- Start with a 1-line hook that makes people click "See More"
- Then a blank line (creates the fold)
- 3-5 dense paragraphs (Sample 09 style: tight, no excess white space)
- End with an engagement CTA (comments)
- Professional but personal. CEO sharing from the arena.
- NO bold headers on list items. Inline flow.
- NO signposting unless the content doesn't demonstrate authority on its own.

=== INSTAGRAM ===
- 5-slide carousel script (Slide 1: bold hook, Slides 2-4: insights, Slide 5: CTA)
- Then write the caption

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

    return {
        "post_drafts": drafts,
        "iteration_count": state.get("iteration_count", 0) + 1,
    }


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