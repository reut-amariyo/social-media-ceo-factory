"""
Obsidian I/O — ABC-TOM v5 Vault Integration
=============================================
Maps to Reut's actual Obsidian vault structure:

    the-system-v5/
    ├── A-agents/           Agent definitions (strategist-scout.md, copywriter-agent-social.md, etc.)
    ├── B-brain/            Content samples, communication samples, research samples
    │   ├── content-samples/
    │   ├── communication-samples/
    │   ├── research-samples/
    │   └── INBOX/
    ├── C-core/             Brand foundation files
    │   ├── project-brief.md    → CEO profile + business context
    │   ├── voice-dna.md        → Brand DNA + deep writing patterns
    │   └── icp-profile.md      → Target audience profiles
    ├── M-memory/           System memory
    │   ├── learning-log.md     → What worked / what didn't
    │   ├── feedback.md         → Audience signals
    │   └── decisions.md        → Strategic choices
    ├── O-output/           Generated content (drafts, final posts)
    └── T-tools/            Skills, prompts, workflows
"""

import os
import yaml
from datetime import datetime

# ============================================================
# Vault paths — mapped to ABC-TOM v5 structure
# ============================================================
VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", "/Users/reut/Documents/MyObsidianVault")
SYSTEM_DIR = os.getenv("OBSIDIAN_SYSTEM_DIR", "the-system-v5")  # root of the ABC-TOM system

# C-core: Brand foundation
PROJECT_BRIEF = os.path.join("C-core", "project-brief.md")
VOICE_DNA = os.path.join("C-core", "voice-dna.md")
ICP_PROFILE = os.path.join("C-core", "icp-profile.md")

# M-memory: System memory
LEARNING_LOG = os.path.join("M-memory", "learning-log.md")
FEEDBACK_LOG = os.path.join("M-memory", "feedback.md")
DECISIONS_LOG = os.path.join("M-memory", "decisions.md")

# M-memory: Agent-written files (safe — never touches Reut's files)
# Reut can review these and merge into the main files when ready.
AGENT_LEARNING_LOG = os.path.join("M-memory", "learning-log-agent.md")
AGENT_FEEDBACK_LOG = os.path.join("M-memory", "feedback-agent.md")

# B-brain: Content samples (past posts for few-shot)
CONTENT_SAMPLES = os.path.join("B-brain", "content-samples")
COMMUNICATION_SAMPLES = os.path.join("B-brain", "communication-samples")
RESEARCH_SAMPLES = os.path.join("B-brain", "research-samples")

# A-agents: Agent definitions
AGENTS_DIR = "A-agents"

# O-output: Generated content
OUTPUT_DIR = "O-output"

# T-tools: Skills and workflows
TOOLS_DIR = "T-tools"


def _vault_path(*parts: str) -> str:
    """Build a full path inside the vault's system directory."""
    return os.path.join(VAULT_PATH, SYSTEM_DIR, *parts)


def test_connection() -> bool:
    """Test if the Obsidian vault and ABC-TOM system directory are accessible."""
    if not os.path.isdir(VAULT_PATH):
        print(f"   ❌ Obsidian vault NOT found at: {VAULT_PATH}")
        print(f"   💡 Set OBSIDIAN_VAULT_PATH in .env")
        return False

    system_path = _vault_path()
    if os.path.isdir(system_path):
        # Check for the key C-core files
        found = []
        for f in [PROJECT_BRIEF, VOICE_DNA, ICP_PROFILE, LEARNING_LOG]:
            if os.path.exists(_vault_path(f)):
                found.append(os.path.basename(f))
        print(f"   ✅ ABC-TOM v5 system found at: {system_path}")
        print(f"   📂 Core files found: {', '.join(found) if found else 'none yet'}")
        return True
    else:
        # Fallback: maybe the vault IS the system dir (flat structure)
        if os.path.exists(os.path.join(VAULT_PATH, "C-core")):
            print(f"   ✅ Obsidian vault found (flat structure): {VAULT_PATH}")
            return True
        print(f"   ⚠️  Vault found but ABC-TOM v5 system dir missing at: {system_path}")
        print(f"   💡 Set OBSIDIAN_SYSTEM_DIR in .env if the folder has a different name")
        return True  # vault exists, system dir might be different


def _read_md_file(relative_path: str, strip_frontmatter: bool = True) -> str:
    """Read a markdown file from the vault. Optionally strip YAML frontmatter."""
    # Try system path first, then vault root (flat layout)
    for base in [_vault_path(), VAULT_PATH]:
        filepath = os.path.join(base, relative_path)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                content = f.read()
            if strip_frontmatter and content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    return parts[2].strip()
            return content
    return ""


def _read_yaml_frontmatter(relative_path: str) -> dict:
    """Read YAML frontmatter from a markdown file."""
    for base in [_vault_path(), VAULT_PATH]:
        filepath = os.path.join(base, relative_path)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                content = f.read()
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    try:
                        return yaml.safe_load(parts[1]) or {}
                    except yaml.YAMLError:
                        pass
    return {}


# ============================================================
# CEO Profile — from C-core/project-brief.md
# ============================================================
def get_ceo_profile() -> dict:
    """
    Load the CEO profile from C-core/project-brief.md.
    Parses the project brief to extract CEO identity, business, and focus areas.
    """
    # Try YAML frontmatter first
    frontmatter = _read_yaml_frontmatter(PROJECT_BRIEF)
    if frontmatter and frontmatter.get("name"):
        print(f"   ✅ Loaded CEO profile from frontmatter: {frontmatter.get('name')}")
        return frontmatter

    # Parse the markdown content for key info
    content = _read_md_file(PROJECT_BRIEF)
    if not content:
        print(f"   ⚠️  project-brief.md not found in vault")
        return {}

    # Extract structured data from the project brief
    profile = {"_raw_brief": content}

    # Look for common patterns in the project brief
    for line in content.split("\n"):
        lower = line.lower().strip()
        if "lior pozin" in lower:
            profile["name"] = "Lior Pozin"
        if "autods" in lower and "company" not in profile:
            profile["company"] = "AutoDS"
        if "ceo" in lower and "role" not in profile:
            profile["role"] = "CEO & Serial Entrepreneur"

    # Set defaults if parsing didn't find everything
    profile.setdefault("name", "Lior Pozin")
    profile.setdefault("company", "AutoDS")
    profile.setdefault("role", "CEO & Serial Entrepreneur")
    profile.setdefault("industry", "E-commerce, SaaS, AI")
    profile.setdefault("topics", [
        "Scaling", "Pricing Strategy", "Revenue Upselling",
        "Growth Hacking", "Branding", "AI in Business",
    ])
    profile.setdefault("tone", "Direct, bold, eye-level, no-BS, action-oriented")

    print(f"   ✅ Loaded CEO profile: {profile.get('name')} ({profile.get('company')})")
    return profile


# ============================================================
# Voice DNA — from C-core/voice-dna.md
# ============================================================
def get_voice_dna() -> str:
    """
    Load the Voice DNA from C-core/voice-dna.md.
    Contains: brand personality, writing patterns, hook types, sentence DNA,
    vocabulary fingerprint, owner editing rules, tone rules.
    """
    content = _read_md_file(VOICE_DNA)
    if content:
        print(f"   ✅ Loaded Voice DNA ({len(content)} chars)")
        return content
    print("   ⚠️  voice-dna.md not found — using embedded defaults")
    return _default_voice_dna()


def _default_voice_dna() -> str:
    """Embedded Voice DNA defaults for Lior Pozin (from the actual file)."""
    return """## Brand Personality
- Competitive, action-oriented, self-development focus
- Macro-manager, no ego, direct & bold
- Never: Arrogant, fluffy, corporate, overly polished, wishy-washy
- Style: CEO sharing from the arena, not a coach from the sidelines

## Tone Rule: Eye-Level, Never Condescending
Every sentence must pass: "Could this be read as 'I'm better than you'?" If yes, rewrite.
- Use "but because" connector for humble framing
- Absorb punch lines into paragraphs (shared observation, not guru pronouncement)
- "most people I know" includes self in the group

## What We're NOT
- Product advocacy (if it could appear on the product's LinkedIn, it's marketing)
- No friction + no personal stake = skip
- Generic claims any competitor could make

## Vocabulary Fingerprint
USE: "real," "just," "precisely," "A LOT" (caps), "gold," "ruthlessly," "noise," "infrastructure"
NEVER: "leverage," "optimize," "synergize," "innovative," "hustle," "grind," "journey," "passionate about"

## Punctuation Rules
- Single dash with space ( - ) for parenthetical
- NEVER em dash, NEVER double dash (--)
- NEVER curly/smart quotes
- Colon as reveal device: "My response was simple:"

## The Rule of 3
Numbered frameworks always use exactly 3 steps. Not 5, not 7.

## Hook Rules
Always ONE line. Never a paragraph.
9 proven types: Provocative question, Personal confession, Scene-setting, Shocking stat,
External case study, Milestone announcement, Empathy hook, Direct quote, Reader-mirror.
"""


# ============================================================
# ICP Profile — from C-core/icp-profile.md
# ============================================================
def get_icp_profile() -> str:
    """
    Load the ICP (Ideal Customer Profile) from C-core/icp-profile.md.
    Contains: 3 audience segments, their pain points, how to speak to each.
    """
    content = _read_md_file(ICP_PROFILE)
    if content:
        print(f"   ✅ Loaded ICP Profile ({len(content)} chars)")
        return content
    print("   ⚠️  icp-profile.md not found — using embedded defaults")
    return _default_icp()


def _default_icp() -> str:
    """Embedded ICP defaults for Lior Pozin."""
    return """## 3 Audience Segments

### 1. Investors
Want: Proven operators, frameworks, track record, data-driven thinking
Hook with: Milestones, exits, financial specifics

### 2. Entrepreneurs (age 25-35, bootstrapped)
Want: 0-to-millions roadmaps, personal stories, confessions
Hook with: "I stopped..." patterns, real numbers, delegation frameworks

### 3. Growth-Seekers (scaling, need systems)
Want: Frameworks, case studies, industry analysis
Hook with: External brand stories, industry moves, reframes

## Language Style
Direct, bold, no-BS, action-oriented, results-focused.
Speak as CEO > Coach. Zero fluff. ROI focused. Real stories.

## Platforms
LinkedIn (primary), Instagram, X/Twitter, TikTok
"""


# ============================================================
# Brand DNA — combined Voice DNA + ICP (convenience function)
# ============================================================
def get_brand_dna() -> str:
    """
    Load the full Brand DNA: Voice DNA + ICP Profile combined.
    This is the comprehensive brand context for agents.
    """
    voice_dna = get_voice_dna()
    icp = get_icp_profile()
    return f"# VOICE DNA\n{voice_dna}\n\n# ICP PROFILE\n{icp}"


# ============================================================
# Content Samples — from B-brain/content-samples/
# ============================================================
def get_past_posts(limit: int = 5) -> list[str]:
    """
    Load past successful posts from B-brain/content-samples/.
    Also checks O-output/ subdirectories for final-post.md files.
    """
    posts = []

    # Source 1: B-brain/content-samples/
    for base in [_vault_path(), VAULT_PATH]:
        samples_dir = os.path.join(base, CONTENT_SAMPLES)
        if os.path.isdir(samples_dir):
            files = sorted(
                [f for f in os.listdir(samples_dir) if f.endswith(".md")],
                reverse=True,
            )
            for filename in files[:limit]:
                filepath = os.path.join(samples_dir, filename)
                with open(filepath, "r") as f:
                    content = f.read()
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        content = parts[2].strip()
                posts.append(content)
            break  # found the directory, stop looking

    # Source 2: O-output/*/final-post.md (published posts)
    if len(posts) < limit:
        for base in [_vault_path(), VAULT_PATH]:
            output_dir = os.path.join(base, OUTPUT_DIR)
            if os.path.isdir(output_dir):
                folders = sorted(os.listdir(output_dir), reverse=True)
                for folder in folders:
                    if len(posts) >= limit:
                        break
                    final = os.path.join(output_dir, folder, "final-post.md")
                    if os.path.exists(final):
                        with open(final, "r") as f:
                            content = f.read()
                        if content.startswith("---"):
                            parts = content.split("---", 2)
                            if len(parts) >= 3:
                                content = parts[2].strip()
                        posts.append(content)
                break

    if posts:
        print(f"   ✅ Loaded {len(posts)} past posts from Obsidian")
    else:
        print(f"   ⚠️  No past posts found in vault")
    return posts


# ============================================================
# Agent Definitions — from A-agents/
# ============================================================
def get_agent_definition(agent_name: str) -> str:
    """
    Load an agent definition file from A-agents/.
    agent_name: e.g. 'strategist-scout', 'copywriter-agent-social', 'gatekeeper-agent'
    """
    filename = f"{agent_name}.md"
    content = _read_md_file(os.path.join(AGENTS_DIR, filename))
    if content:
        print(f"   ✅ Loaded agent definition: {agent_name}")
    return content


# ============================================================
# Save Drafts — to O-output/ (ABC-TOM naming convention)
# ============================================================
def save_drafts_to_obsidian(drafts: dict, trend_topic: str = "", image_path: str = "") -> str:
    """
    Save generated drafts to O-output/ following ABC-TOM naming:
    O-output/[number]-[slug]/copywriter-draft.md
    """
    # Find next output number
    output_base = None
    for base in [_vault_path(), VAULT_PATH]:
        candidate = os.path.join(base, OUTPUT_DIR)
        if os.path.isdir(candidate):
            output_base = candidate
            break
    if not output_base:
        output_base = _vault_path(OUTPUT_DIR)

    os.makedirs(output_base, exist_ok=True)

    # Determine next folder number
    existing = [d for d in os.listdir(output_base) if os.path.isdir(os.path.join(output_base, d))]
    numbers = []
    for d in existing:
        try:
            numbers.append(int(d.split("-")[0]))
        except (ValueError, IndexError):
            pass
    next_num = max(numbers, default=0) + 1

    # Create slug from topic
    slug = "".join(c if c.isalnum() or c in "-_ " else "" for c in trend_topic[:50])
    slug = slug.strip().replace(" ", "-").lower()[:40] or "social-post"
    folder_name = f"{next_num:02d}-{slug}"
    folder_path = os.path.join(output_base, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")

    # Build YAML frontmatter
    frontmatter = {
        "date": today,
        "status": "draft",
        "topic": trend_topic[:100] if trend_topic else "Untitled",
        "platforms": list(drafts.keys()),
        "tags": ["social-media", "draft", "auto-generated"],
    }
    if image_path:
        frontmatter["image"] = image_path

    # Build the Markdown content
    content = "---\n"
    content += yaml.dump(frontmatter, default_flow_style=False)
    content += "---\n\n"
    content += f"# Social Media Drafts - {today}\n\n"
    content += f"**Topic:** {trend_topic}\n\n"

    if "x" in drafts:
        content += "## X (Twitter)\n\n"
        content += f"{drafts['x']}\n\n"

    if "linkedin" in drafts:
        content += "## LinkedIn\n\n"
        content += f"{drafts['linkedin']}\n\n"

    if "instagram_slides" in drafts:
        content += "## Instagram Carousel\n\n"
        content += f"{drafts['instagram_slides']}\n\n"

    if "instagram_caption" in drafts:
        content += "### Caption\n\n"
        content += f"{drafts['instagram_caption']}\n\n"

    if image_path:
        content += f"## Generated Image\n\n![[{os.path.basename(image_path)}]]\n\n"

    content += "---\n*Generated by Lior Pozin's Branding Factory*\n"

    filepath = os.path.join(folder_path, "copywriter-draft.md")
    try:
        with open(filepath, "w") as f:
            f.write(content)
        print(f"   ✅ Drafts saved to: {folder_path}/")
        return filepath
    except Exception as e:
        print(f"   ❌ Failed to save to Obsidian: {e}")
        return ""


# ============================================================
# Learning Log — READ from M-memory/learning-log.md
#                WRITE to M-memory/learning-log-agent.md (safe)
# ============================================================
def update_learning_log(content: str):
    """
    Append agent insights to M-memory/learning-log-agent.md (SAFE).

    Why a separate file?
    - Reut edits learning-log.md daily via Claude Desktop
    - Writing to the same file risks corruption if both write at the same time
    - Agent writes go to learning-log-agent.md instead
    - Reut can review and merge into the main log when ready (The Loop)
    """
    for base in [_vault_path(), VAULT_PATH]:
        memory_dir = os.path.join(base, "M-memory")
        if os.path.isdir(memory_dir):
            agent_log = os.path.join(base, AGENT_LEARNING_LOG)
            try:
                # Create the file with a header if it doesn't exist yet
                if not os.path.exists(agent_log):
                    with open(agent_log, "w") as f:
                        f.write("# Agent Learning Log\n\n")
                        f.write("> Auto-generated by the Branding Factory agents.\n")
                        f.write("> Review these insights and promote to learning-log.md when ready.\n\n")
                        f.write("---\n\n")

                with open(agent_log, "a") as f:
                    f.write(f"\n{content}")
                print(f"   ✅ Insights saved to learning-log-agent.md (safe — won't touch Reut's file)")
                return
            except Exception as e:
                print(f"   ⚠️  Could not write to agent learning log: {e}")
                return

    # Fallback: write locally
    local_fallback = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "outputs", "learning-log-agent.md"
    )
    os.makedirs(os.path.dirname(local_fallback), exist_ok=True)
    try:
        with open(local_fallback, "a") as f:
            f.write(f"\n{content}")
        print(f"   ✅ Insights saved locally to outputs/learning-log-agent.md")
    except Exception as e:
        print(f"   ⚠️  Could not save insights: {e}")


def get_learning_log() -> str:
    """Read M-memory/learning-log.md from the vault."""
    content = _read_md_file(LEARNING_LOG, strip_frontmatter=False)
    if content:
        return content

    # Fallback: check local learning log
    local_log = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "branding_factory", "learning_log.md"
    )
    if os.path.exists(local_log):
        with open(local_log, "r") as f:
            return f.read()

    return "Write engaging, high-value tech content."


if __name__ == "__main__":
    print("🔌 Testing Obsidian Vault Connection...\n")
    connected = test_connection()
    if connected:
        profile = get_ceo_profile()
        if profile:
            print(f"\n📋 CEO Profile:")
            for k, v in profile.items():
                print(f"   {k}: {v}")

        brand_dna = get_brand_dna()
        print(f"\n📖 Brand DNA Preview:\n{brand_dna[:300]}...")

        posts = get_past_posts(limit=3)
        print(f"\n📄 Past Posts: {len(posts)} loaded")
        for i, p in enumerate(posts, 1):
            print(f"   Post {i}: {p[:100]}...")

        log = get_learning_log()
        print(f"\n📝 Learning Log Preview:\n{log[:200]}...")
    else:
        print("\n💡 To fix: Set OBSIDIAN_VAULT_PATH in .env to your Obsidian vault directory.")