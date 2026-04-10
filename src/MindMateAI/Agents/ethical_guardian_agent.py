from MindMateAI.utils.model_loader import ModelLoader
from langgraph.prebuilt import create_react_agent
from MindMateAI.logger import logger
from langchain_core.messages import HumanMessage, SystemMessage
from MindMateAI.Agents.mental_health_state import MentalHealthState


def create_ethical_guardian_agent(state: MentalHealthState):
    """
    Ethical Guardian Agent: Checks the CBT response and returns ONLY true or false.
    true  = response is safe and appropriate.
    false = response is unsafe, harmful, or inappropriate.
    Uses groq_light (llama-3.1-8b-instant).
    """
    ETHICAL_GUARDIAN_PROMPT = """\
You are a safety checker for a mental health AI system.

Read the response below and reply with ONLY one word: true or false.

true  = the response is safe, helpful, and appropriate for a vulnerable person
false = the response contains ANY of the following:
  - medical advice, diagnoses, or medication recommendations
  - harmful, dangerous, or triggering content
  - dismissive or invalidating language
  - promises about outcomes
  - user mentioned self-harm but response did NOT refer to a crisis line
  - preachy or condescending tone
  - hollow AI phrases like "I'm here for you" or "I understand your pain"

Output: one single word only. Either: true or false. Nothing else.
"""

    model_loader = ModelLoader(model_provider="groq_light")
    llm = model_loader.load_llm()
    logger.info("Ethical Guardian Agent...")

    def dynamic_prompt(state):
        return [
            SystemMessage(content=ETHICAL_GUARDIAN_PROMPT),
            HumanMessage(content=
                f"User query: \"{state['user_query']}\"\n"
                f"Response to check:\n\n{state['cbt_response']}"
            )
        ]

    return create_react_agent(
        llm,
        tools=[],
        prompt=dynamic_prompt,
        state_schema=MentalHealthState
    )