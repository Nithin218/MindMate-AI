from typing import TypedDict, List, Dict, Any
from langgraph.graph import MessagesState

class MentalHealthState(MessagesState):
    user_query: str
    rewritten_query: str
    emotion: str
    cbt_response: str
    schedule_recommendation: str
    ethical_check: bool
    ethical_feedback: str
    final_output: str
    messages: List[Dict[str, Any]]
    retry_count: int
    remaining_steps: int