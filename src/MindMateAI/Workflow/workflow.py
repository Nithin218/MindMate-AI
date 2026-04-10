"""
MindMate AI Workflow
Pipeline: user_query -> emotion -> cbt -> ethical_check -> writer -> final_output

Removed: rewrite_agent (no longer in pipeline)
Simplified: emotion returns one word, ethical_check returns true/false only
"""
from langgraph.graph import StateGraph, END
from MindMateAI.Agents.mental_health_state import MentalHealthState
from MindMateAI.Agents.emotion_analysis_agent import create_emotion_analysis_agent
from MindMateAI.Agents.cbt_agent import create_cbt_agent
from MindMateAI.Agents.ethical_guardian_agent import create_ethical_guardian_agent
from MindMateAI.Agents.writer_agent import create_writer_agent
from MindMateAI.logger import logger


# ── Helper: extract last AI message text ────────────────────────────────────
def _last_ai_text(state: MentalHealthState) -> str:
    """Pull the last AIMessage content from state['messages']."""
    messages = state.get("messages", [])
    for msg in reversed(messages):
        role = getattr(msg, "type", None) or msg.get("role", "")
        if role in ("ai", "assistant"):
            content = getattr(msg, "content", None) or msg.get("content", "")
            if isinstance(content, list):
                # Handle multi-part content blocks
                return " ".join(
                    block.get("text", "") if isinstance(block, dict) else str(block)
                    for block in content
                ).strip()
            return str(content).strip()
    return ""


# ── Node: Emotion Analysis ───────────────────────────────────────────────────
def emotion_node(state: MentalHealthState) -> dict:
    logger.info("Emotion Analysis Agent running...")
    agent = create_emotion_analysis_agent(state)
    result = agent.invoke(state)

    raw = _last_ai_text(result).strip().lower()

    # Clean: take only the first word in case model adds punctuation
    emotion = raw.split()[0].rstrip(".,!?;:") if raw else "stress"

    # Validate against known labels, default to "stress" if unknown
    valid_emotions = {
        "stress", "anxiety", "burnout", "overwhelm", "depression",
        "sadness", "loneliness", "grief", "anger", "frustration",
        "guilt", "shame", "fear", "confusion", "productivity"
    }
    if emotion not in valid_emotions:
        logger.info(f"Unknown emotion '{emotion}', defaulting to 'stress'")
        emotion = "stress"

    logger.info(f"Emotion detected: {emotion}")
    return {"emotion": emotion, "messages": result.get("messages", [])}


# ── Node: CBT Agent ──────────────────────────────────────────────────────────
def cbt_node(state: MentalHealthState) -> dict:
    logger.info("CBT Agent running...")
    agent = create_cbt_agent(state)
    result = agent.invoke(state)

    cbt_response = _last_ai_text(result).strip()
    logger.info("CBT response generated.")
    return {"cbt_response": cbt_response, "messages": result.get("messages", [])}


# ── Node: Ethical Guardian ───────────────────────────────────────────────────
def ethical_node(state: MentalHealthState) -> dict:
    logger.info("Ethical Guardian running...")
    agent = create_ethical_guardian_agent(state)
    result = agent.invoke(state)

    raw = _last_ai_text(result).strip().lower()
    # Extract true/false from the first word
    first_word = raw.split()[0].rstrip(".,!?;:") if raw else "false"
    ethical = first_word == "true"

    logger.info(f"Ethical check: {ethical}")
    return {"ethical_check": ethical, "messages": result.get("messages", [])}


# ── Node: Writer Agent ───────────────────────────────────────────────────────
def writer_node(state: MentalHealthState) -> dict:
    logger.info("Writer Agent running...")
    agent = create_writer_agent(state)
    result = agent.invoke(state)

    final_output = _last_ai_text(result).strip()
    logger.info("Final output generated.")
    return {"final_output": final_output, "messages": result.get("messages", [])}


# ── Routing: after ethical check ────────────────────────────────────────────
def ethical_routing(state: MentalHealthState) -> str:
    retry_count = state.get("retry_count", 0)

    if state.get("ethical_check"):
        logger.info("Ethical check passed -> writer")
        return "writer"

    if retry_count >= 2:
        logger.info("Max retries reached -> writer anyway")
        return "writer"

    logger.info(f"Ethical check failed (retry {retry_count + 1}) -> cbt retry")
    return "cbt_retry"


# ── Node: CBT Retry (increments counter) ────────────────────────────────────
def cbt_retry_node(state: MentalHealthState) -> dict:
    retry_count = state.get("retry_count", 0) + 1
    logger.info(f"CBT retry attempt {retry_count}...")
    agent = create_cbt_agent(state)
    result = agent.invoke(state)

    cbt_response = _last_ai_text(result).strip()
    return {
        "cbt_response": cbt_response,
        "retry_count": retry_count,
        "messages": result.get("messages", [])
    }


# ── Build Graph ──────────────────────────────────────────────────────────────
def build_workflow() -> StateGraph:
    graph = StateGraph(MentalHealthState)

    # Add nodes
    graph.add_node("emotion",     emotion_node)
    graph.add_node("cbt",         cbt_node)
    graph.add_node("cbt_retry",   cbt_retry_node)
    graph.add_node("ethical",     ethical_node)
    graph.add_node("writer",      writer_node)

    # Entry point
    graph.set_entry_point("emotion")

    # Edges
    graph.add_edge("emotion",   "cbt")
    graph.add_edge("cbt",       "ethical")
    graph.add_edge("cbt_retry", "ethical")
    graph.add_edge("writer",    END)

    # Conditional routing after ethical check
    graph.add_conditional_edges(
        "ethical",
        ethical_routing,
        {
            "writer":    "writer",
            "cbt_retry": "cbt_retry",
        }
    )

    return graph.compile()


# ── Backward-compatible alias ────────────────────────────────────────────────
# main.py imports GraphBuilder — this class keeps that import working as-is.
class GraphBuilder:
    """
    Compatibility wrapper so existing main.py code needs zero changes.

    Supports all calling styles:
        GraphBuilder().build()   -> compiled graph
        GraphBuilder()()         -> compiled graph  (instance called directly)
        graph_builder = GraphBuilder(); graph_builder() -> compiled graph
    """
    def build(self):
        return build_workflow()

    def __call__(self):
        return build_workflow()