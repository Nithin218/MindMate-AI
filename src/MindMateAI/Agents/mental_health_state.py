from typing import TypedDict, List, Dict, Any

class MentalHealthState(TypedDict):
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