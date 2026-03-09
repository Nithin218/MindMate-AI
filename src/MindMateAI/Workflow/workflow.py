from langgraph.graph import StateGraph, START, END
from MindMateAI.Agents.mental_health_state import MentalHealthState
from MindMateAI.Agents.rewrite_agent import create_query_rewriting_agent
from MindMateAI.Agents.emotion_analysis_agent import create_emotion_analysis_agent
from MindMateAI.Agents.ethical_guardian_agent import create_ethical_guardian_agent
from MindMateAI.Agents.cbt_agent import create_cbt_agent
from MindMateAI.Agents.writer_agent import create_writer_agent
from MindMateAI.logger import logger
from typing import Literal
import json
import re


def _parse_json_safely(content: str) -> dict:
    """
    Robustly extract a JSON object from LLM output that may contain
    markdown fences, leading text, or trailing commentary.
    """
    # Strip markdown code fences
    content = content.strip()
    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)```", content)
    if fenced:
        content = fenced.group(1).strip()

    # Find the first {...} block in the content
    brace_match = re.search(r"\{[\s\S]*\}", content)
    if brace_match:
        content = brace_match.group(0)

    return json.loads(content)


class GraphBuilder:
    def __init__(self):
        self.graph = None

    # ──────────────────────────────────────────────
    # SUPERVISOR
    # ──────────────────────────────────────────────

    def supervisor_node(self, state: MentalHealthState):
        """Pass-through node — all routing logic lives in supervisor_routing."""
        return {}

    def supervisor_routing(
        self, state: MentalHealthState
    ) -> Literal[
        "rewrite", "emotion_analysis", "cbt_agent",
        "ethical_guardian", "writer", "increment_retry", "__end__"
    ]:
        logger.info("Supervisor deciding next step...")

        # Step 1 — Rewrite query
        if not state.get("rewritten_query"):
            logger.info("→ rewrite")
            return "rewrite"

        # Step 2 — Analyse emotion
        if not state.get("emotion"):
            logger.info("→ emotion_analysis")
            return "emotion_analysis"

        # Step 3 — Generate CBT response
        if not state.get("cbt_response"):
            logger.info("→ cbt_agent")
            return "cbt_agent"

        # Step 4 — Run ethical check (only if not yet checked)
        # ethical_check is None initially; True/False after the guardian runs
        if state.get("ethical_check") is None:
            logger.info("→ ethical_guardian")
            return "ethical_guardian"

        # Step 5 — Handle ethical failure → retry
        if state.get("ethical_check") is False:
            logger.info("→ increment_retry")
            return "increment_retry"

        # Step 6 — Polish and write final output
        if not state.get("final_output"):
            logger.info("→ writer")
            return "writer"

        logger.info("→ __end__")
        return "__end__"

    # ──────────────────────────────────────────────
    # NODE: REWRITE
    # ──────────────────────────────────────────────

    def rewrite_node(self, state: MentalHealthState) -> dict:
        agent = create_query_rewriting_agent(state)
        logger.info("Rewriting user query...")
        result = agent.invoke(state)
        rewritten_query = result["messages"][-1].content.strip()
        logger.info(f"Rewritten query: {rewritten_query[:120]}...")
        return {
            "rewritten_query": rewritten_query,
            "messages": [{"role": "rewrite", "content": rewritten_query}],
        }

    # ──────────────────────────────────────────────
    # NODE: EMOTION ANALYSIS
    # ──────────────────────────────────────────────

    def emotion_analysis_node(self, state: MentalHealthState) -> dict:
        agent = create_emotion_analysis_agent(state)
        logger.info("Analysing emotion...")
        result = agent.invoke(state)
        raw_content = result["messages"][-1].content

        emotion = "stress"
        intensity = "moderate"
        secondary_emotion = None
        rationale = ""

        try:
            analysis = _parse_json_safely(raw_content)
            emotion = analysis.get("emotion", "stress").strip().lower()
            intensity = analysis.get("intensity", "moderate").strip().lower()
            secondary_emotion = analysis.get("secondary_emotion")
            rationale = analysis.get("rationale", "")
            logger.info(f"Emotion classified: {emotion} ({intensity}) | secondary: {secondary_emotion}")
        except Exception as e:
            logger.warning(f"JSON parse failed for emotion analysis: {e}. Falling back to keyword match.")
            content_lower = raw_content.lower()
            # Ordered from most-specific to avoid early mismatches
            emotion_keywords = [
                ("burnout",     ["burnout", "burnt out", "burn out"]),
                ("overwhelm",   ["overwhelm"]),
                ("depression",  ["depress", "anhedonia", "hopeless"]),
                ("grief",       ["grief", "grieving", "lost someone", "passed away", "bereavement"]),
                ("loneliness",  ["lonel", "isolated", "disconnected", "invisible"]),
                ("anger",       ["anger", "furious", "rage", "livid", "betrayed"]),
                ("frustration", ["frustrat", "stuck", "blocked", "nothing works"]),
                ("guilt",       ["guilt", "shame", "ashamed", "my fault", "regret"]),
                ("fear",        ["terrified", "scared", "phobia", "avoidance"]),
                ("anxiety",     ["anxiety", "anxious", "panic", "what if", "dread"]),
                ("sadness",     ["sad", "down", "melanchol", "disappointed"]),
                ("confusion",   ["confus", "lost", "don't know what to do", "unclear"]),
                ("stress",      ["stress", "pressure", "deadline", "overload"]),
            ]
            for label, keywords in emotion_keywords:
                if any(kw in content_lower for kw in keywords):
                    emotion = label
                    break

        return {
            "emotion": emotion,
            "emotion_intensity": intensity,
            "secondary_emotion": secondary_emotion if secondary_emotion else None,
            "emotion_rationale": rationale,
            "messages": [{"role": "emotion_analyst", "content": raw_content}],
        }

    # ──────────────────────────────────────────────
    # NODE: CBT AGENT
    # ──────────────────────────────────────────────

    def cbt_agent_node(self, state: MentalHealthState) -> dict:
        agent = create_cbt_agent(state)
        logger.info(f"Generating CBT response for emotion: {state.get('emotion')} ({state.get('emotion_intensity')})...")
        result = agent.invoke(state)
        cbt_response = result["messages"][-1].content.strip()
        logger.info(f"CBT response generated ({len(cbt_response)} chars).")
        return {
            "cbt_response": cbt_response,
            # Reset ethical_check to None so the guardian always runs fresh
            "ethical_check": None,
            "messages": [{"role": "cbt_agent", "content": cbt_response}],
        }

    # ──────────────────────────────────────────────
    # NODE: ETHICAL GUARDIAN
    # ──────────────────────────────────────────────

    def ethical_guardian_node(self, state: MentalHealthState) -> dict:
        agent = create_ethical_guardian_agent(state)
        logger.info("Running ethical compliance check...")
        result = agent.invoke(state)
        raw_content = result["messages"][-1].content

        ethical_check = True
        ethical_feedback = "Ethical review passed (default fallback)"
        ethical_concerns = []
        specificity_score = 5
        emotion_technique_match = True

        try:
            analysis = _parse_json_safely(raw_content)
            ethical_check = bool(analysis.get("ethical", True))
            ethical_feedback = analysis.get("feedback", ethical_feedback)
            ethical_concerns = analysis.get("concerns", [])
            specificity_score = int(analysis.get("specificity_score", 5))
            emotion_technique_match = bool(analysis.get("emotion_technique_match", True))
            logger.info(
                f"Ethical check: {'PASS' if ethical_check else 'FAIL'} | "
                f"Specificity: {specificity_score}/10 | "
                f"Technique match: {emotion_technique_match}"
            )
            if not ethical_check:
                logger.warning(f"Ethical concerns: {ethical_concerns}")
        except Exception as e:
            logger.warning(f"JSON parse failed for ethical check: {e}. Defaulting to pass.")

        return {
            "ethical_check": ethical_check,
            "ethical_feedback": ethical_feedback,
            "ethical_concerns": ethical_concerns,
            "specificity_score": specificity_score,
            "emotion_technique_match": emotion_technique_match,
            "messages": [{"role": "ethical_guardian", "content": raw_content}],
        }

    # ──────────────────────────────────────────────
    # NODE: INCREMENT RETRY
    # ──────────────────────────────────────────────

    def increment_retry_node(self, state: MentalHealthState) -> dict:
        retry_count = state.get("retry_count", 0)
        logger.warning(
            f"Ethical check failed (retry {retry_count + 1}/3). "
            f"Feedback: {state.get('ethical_feedback')}"
        )

        if retry_count >= 3:
            logger.error("Max retries reached. Returning safety fallback.")
            return {
                "final_output": (
                    "Something went wrong while preparing a safe response for you. "
                    "If you're in distress, please reach out to a mental health professional "
                    "or the 988 Suicide & Crisis Lifeline (call or text 988)."
                ),
                # Force ethical_check True to break the retry loop
                "ethical_check": True,
                "messages": [{"role": "system", "content": "Max retries reached — returning safety fallback."}],
            }

        feedback = state.get("ethical_feedback", "")
        concerns = state.get("ethical_concerns", [])
        retry_instruction = (
            f"Your previous response was rejected. Retry #{retry_count + 1}.\n"
            f"Feedback: {feedback}\n"
            f"Specific concerns to fix: {'; '.join(concerns) if concerns else 'See feedback above.'}\n"
            f"Rewrite the response addressing ALL concerns. Keep it specific to the user's situation."
        )

        return {
            "retry_count": retry_count + 1,
            # Clear CBT response to force regeneration in cbt_agent_node
            "cbt_response": "",
            # Reset ethical check to None so guardian re-runs after regeneration
            "ethical_check": None,
            "messages": [{"role": "system", "content": retry_instruction}],
        }

    # ──────────────────────────────────────────────
    # NODE: WRITER
    # ──────────────────────────────────────────────

    def writer_agent_node(self, state: MentalHealthState) -> dict:
        agent = create_writer_agent(state)
        logger.info("Generating final polished output...")
        result = agent.invoke(state)
        final_output = result["messages"][-1].content.strip()
        logger.info(f"Final output ready ({len(final_output)} chars).")
        return {
            "final_output": final_output,
            "messages": [{"role": "writer", "content": final_output}],
        }

    # ──────────────────────────────────────────────
    # GRAPH ASSEMBLY
    # ──────────────────────────────────────────────

    def build_graph(self):
        workflow = StateGraph(MentalHealthState)

        # Register nodes
        workflow.add_node("supervisor",       self.supervisor_node)
        workflow.add_node("rewrite",          self.rewrite_node)
        workflow.add_node("emotion_analysis", self.emotion_analysis_node)
        workflow.add_node("cbt_agent",        self.cbt_agent_node)
        workflow.add_node("ethical_guardian", self.ethical_guardian_node)
        workflow.add_node("increment_retry",  self.increment_retry_node)
        workflow.add_node("writer",           self.writer_agent_node)

        # Entry point
        workflow.add_edge(START, "supervisor")

        # All agent nodes return to supervisor for re-routing
        workflow.add_edge("rewrite",          "supervisor")
        workflow.add_edge("emotion_analysis", "supervisor")
        workflow.add_edge("cbt_agent",        "supervisor")
        workflow.add_edge("ethical_guardian", "supervisor")
        workflow.add_edge("increment_retry",  "supervisor")

        # Writer is terminal
        workflow.add_edge("writer", END)

        # Supervisor conditional routing
        workflow.add_conditional_edges(
            "supervisor",
            self.supervisor_routing,
            {
                "rewrite":          "rewrite",
                "emotion_analysis": "emotion_analysis",
                "cbt_agent":        "cbt_agent",
                "ethical_guardian": "ethical_guardian",
                "writer":           "writer",
                "increment_retry":  "increment_retry",
                "__end__":          END,
            },
        )

        self.graph = workflow.compile()
        logger.info("Graph compiled successfully.")
        return self.graph

    def __call__(self):
        return self.build_graph()