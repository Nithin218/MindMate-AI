from typing import TypedDict, List, Dict, Any, Annotated, Optional
import operator


class MentalHealthState(TypedDict):
    # Core user input
    user_query: str

    # Emotion classification — just the label, nothing more
    emotion: str                        # Primary emotion label e.g. "anxiety", "stress"

    # Agent outputs
    cbt_response: str                   # Raw CBT therapist draft
    final_output: str                   # Polished writer output shown to user

    # Ethical review — just pass/fail
    ethical_check: bool                 # True = passed, False = failed

    # Pipeline control
    messages: Annotated[List[Dict[str, Any]], operator.add]
    retry_count: int                    # How many times CBT response has been regenerated
    remaining_steps: int                # LangGraph step budget