from langgraph.graph import StateGraph, END
from branding_factory.agents.scout import run_scout_agent
from branding_factory.agents.ideator import run_ideator_agent
from branding_factory.agents.creator import run_creator_agent
from branding_factory.agents.validator import run_validator_agent
from branding_factory.agents.graphic_artist import run_graphic_agent
from branding_factory.agents.analyst import run_analyst_agent
from utils.obsidian_io import (
    save_drafts_to_obsidian,
    get_learning_log,
    get_voice_dna,
    get_icp_profile,
)


# ============================================================
# Human-in-the-loop: Reut picks her favorite idea
# ============================================================
def human_approval_node(state: dict):
    """
    Pauses the flow and lets Reut choose which idea to develop.
    This is the Human Checkpoint from the PRD.
    """
    print("\n" + "=" * 60)
    print("🛑 HUMAN CHECKPOINT — Reut, pick your favorite idea!")
    print("=" * 60)

    ideas = state.get("ideas", [])
    if not ideas:
        print("   ⚠️  No ideas generated. Using trend report as fallback.")
        return {"selected_idea": state.get("trend_report", "Latest tech trends")}

    for i, idea in enumerate(ideas, 1):
        print(f"\n{'─' * 40}")
        print(f"💡 IDEA {i}:")
        print(f"{'─' * 40}")
        print(idea)

    print(f"\n{'─' * 40}")
    while True:
        try:
            choice = input(f"\n👉 Enter your choice (1-{len(ideas)}), or 'skip' to auto-pick: ").strip()
            if choice.lower() == "skip":
                selected = ideas[0]
                print(f"   ⏭️  Auto-selected Idea 1")
                break
            choice_num = int(choice)
            if 1 <= choice_num <= len(ideas):
                selected = ideas[choice_num - 1]
                print(f"   ✅ Selected Idea {choice_num}")
                break
            else:
                print(f"   ❌ Please enter a number between 1 and {len(ideas)}")
        except ValueError:
            print("   ❌ Please enter a valid number")

    return {"selected_idea": selected}


# ============================================================
# Save final output to Obsidian
# ============================================================
def save_to_obsidian_node(state: dict):
    """Save the validated drafts to Obsidian's Drafts folder."""
    print("--- 📂 SAVING TO OBSIDIAN ---")

    drafts = state.get("post_drafts", {})
    trend = state.get("selected_idea", "")
    image_path = state.get("image_path", "")

    filepath = save_drafts_to_obsidian(drafts, trend, image_path)

    if filepath:
        print(f"   ✅ All drafts saved! Open Obsidian to review and edit.")
    else:
        # Save locally as fallback
        print("   ⚠️  Could not save to Obsidian. Saving locally...")
        _save_local_fallback(drafts, trend, image_path)

    return state


def _save_local_fallback(drafts: dict, trend: str, image_path: str):
    """Save drafts locally if Obsidian isn't available."""
    import os
    from datetime import datetime

    os.makedirs("outputs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"outputs/draft_{timestamp}.md"

    with open(filepath, "w") as f:
        f.write(f"# Social Media Drafts\n\n")
        f.write(f"**Topic:** {trend}\n\n")
        for platform, content in drafts.items():
            f.write(f"## {platform.upper()}\n\n{content}\n\n")
        if image_path:
            f.write(f"## Image\n\n![image]({image_path})\n")

    print(f"   ✅ Saved locally to: {filepath}")


# ============================================================
# Load learning context at the start
# ============================================================
def load_context_node(state: dict):
    """Load learning log, Voice DNA, and ICP at the start of the flow."""
    print("--- 📚 LOADING CONTEXT ---")

    learning_context = get_learning_log()
    print(f"   📝 Learning log: {len(learning_context)} chars")

    voice_dna = get_voice_dna()
    print(f"   🎤 Voice DNA: {len(voice_dna)} chars")

    icp_profile = get_icp_profile()
    print(f"   🎯 ICP Profile: {len(icp_profile)} chars")

    return {
        "learning_context": learning_context,
        "voice_dna": voice_dna,
        "icp_profile": icp_profile,
    }


# ============================================================
# Routing Logic
# ============================================================
def validation_router(state: dict):
    """
    After validation:
    - FAIL + iterations < 3 → retry (back to Creator)
    - PASS → continue to Graphic Artist
    """
    validation = state.get("validation_results", "")
    iteration = state.get("iteration_count", 0)

    if "FAIL" in validation and iteration < 3:
        print(f"   🔄 Routing back to Creator (attempt {iteration + 1}/3)")
        return "retry"
    elif "FAIL" in validation:
        print(f"   ⚠️  Max retries reached. Proceeding with current drafts.")
        return "proceed"
    else:
        return "proceed"


# ============================================================
# Build the Full LangGraph Workflow
# ============================================================
def create_factory_graph():
    """
    The full agentic flow:
    Load Context → Scout → Ideator → [Human Approval] → Creator → Validator → (loop or pass)
    → Graphic Artist → Save to Obsidian
    """
    workflow = StateGraph(dict)

    # Define all nodes
    workflow.add_node("load_context", load_context_node)
    workflow.add_node("scout", run_scout_agent)
    workflow.add_node("ideator", run_ideator_agent)
    workflow.add_node("human_approval", human_approval_node)
    workflow.add_node("creator", run_creator_agent)
    workflow.add_node("validator", run_validator_agent)
    workflow.add_node("graphic_artist", run_graphic_agent)
    workflow.add_node("save_to_obsidian", save_to_obsidian_node)

    # Define the flow
    workflow.set_entry_point("load_context")
    workflow.add_edge("load_context", "scout")
    workflow.add_edge("scout", "ideator")
    workflow.add_edge("ideator", "human_approval")
    workflow.add_edge("human_approval", "creator")
    workflow.add_edge("creator", "validator")

    # Validation loop: retry or proceed
    workflow.add_conditional_edges(
        "validator",
        validation_router,
        {
            "retry": "creator",
            "proceed": "graphic_artist",
        },
    )

    workflow.add_edge("graphic_artist", "save_to_obsidian")
    workflow.add_edge("save_to_obsidian", END)

    return workflow.compile()