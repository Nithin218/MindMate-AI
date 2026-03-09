from typing import TypedDict, List, Dict, Any, Annotated, Optional
import operator

class MentalHealthState(TypedDict):
    # Core user input
    user_query: str
    rewritten_query: str

    # Emotion classification (expanded for richer CBT technique selection)
    emotion: str                        # Primary emotion label (e.g., "anxiety", "grief")
    emotion_intensity: str              # "mild" | "moderate" | "severe"
    secondary_emotion: Optional[str]    # Secondary emotion if clearly present, else None
    emotion_rationale: Optional[str]    # Why this emotion was classified (for debugging)

    # Agent outputs
    cbt_response: str                   # Raw CBT therapist draft
    schedule_recommendation: str        # Optional schedule/plan (legacy field, kept for compatibility)
    final_output: str                   # Polished writer output shown to user

    # Ethical review
    ethical_check: bool                 # True = passed, False = failed
    ethical_feedback: str               # Specific feedback from ethical guardian
    ethical_concerns: List[str]         # List of specific concerns (empty if passed)
    specificity_score: int              # 1-10: how unique is the response to this user
    emotion_technique_match: bool       # Whether the technique matched the detected emotion

    # Pipeline control
    messages: Annotated[List[Dict[str, Any]], operator.add]
    retry_count: int                    # How many times CBT response has been regenerated
    remaining_steps: int                # LangGraph step budget