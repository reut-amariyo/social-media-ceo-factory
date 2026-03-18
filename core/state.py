from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    # CEO profile loaded from C-core/project-brief.md
    ceo_profile: dict
    # Voice DNA loaded from C-core/voice-dna.md (writing patterns, tone rules, vocabulary)
    voice_dna: str
    # ICP Profile loaded from C-core/icp-profile.md (3 audience segments)
    icp_profile: str
    # The current trend being discussed
    trend_report: str
    # The refined ideas for Reut to pick from
    ideas: List[str]
    # The final selection (Human-in-the-loop)
    selected_idea: str
    # The actual drafts for each platform
    post_drafts: dict # {'x': '...', 'linkedin': '...', 'instagram': '...'}
    # Path to the local M4 generated image
    image_path: str
    # Validation status
    validation_results: str
    # Iteration counter to prevent infinite loops
    iteration_count: int
    # The context from previous "Analyst" runs
    learning_context: str