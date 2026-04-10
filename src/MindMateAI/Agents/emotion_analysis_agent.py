from MindMateAI.utils.model_loader import ModelLoader
from langgraph.prebuilt import create_react_agent
from MindMateAI.logger import logger
from langchain_core.messages import HumanMessage, SystemMessage
from MindMateAI.Agents.mental_health_state import MentalHealthState


def create_emotion_analysis_agent(state: MentalHealthState):
    """
    Emotion Analysis Agent: Reads the user message and returns ONLY the emotion label.
    Nothing else. Uses groq_light (llama-3.1-8b-instant).
    """
    EMOTION_ANALYST_PROMPT = """\
Read the user message and reply with ONLY one word — the emotion label.

Emotion options:
stress, anxiety, burnout, overwhelm, depression, sadness, loneliness, grief,
anger, frustration, guilt, shame, fear, confusion, productivity

Rules:
- stress     -> external pressure, deadlines, workload
- anxiety    -> internal worry, what-ifs, future dread
- burnout    -> long-term emptiness, numb, going through motions for months
- overwhelm  -> too many things at once right now, can't prioritize
- depression -> persistent low mood 2+ weeks, loss of pleasure, hopelessness
- sadness    -> temporary low mood tied to a specific event
- loneliness -> feeling unseen, disconnected, invisible
- grief      -> specific loss: death, breakup, job loss
- anger      -> injustice, being wronged, betrayed
- frustration-> stuck, repeated failure, nothing working
- guilt      -> I did something bad, regret
- shame      -> I AM bad, identity-level self-blame
- fear       -> specific identifiable threat
- confusion  -> lost, don't know what to do, unclear direction
- productivity -> planning, habits, routines, goals, time management, scheduling

Output: one single word only. No punctuation. No explanation. No JSON. Just the word.
"""

    model_loader = ModelLoader(model_provider="groq_light")
    llm = model_loader.load_llm()
    logger.info("Emotion Analysis Agent...")

    def dynamic_prompt(state):
        return [
            SystemMessage(content=EMOTION_ANALYST_PROMPT),
            HumanMessage(content=f"{state['user_query']}")
        ]

    return create_react_agent(
        llm,
        tools=[],
        prompt=dynamic_prompt,
        state_schema=MentalHealthState
    )