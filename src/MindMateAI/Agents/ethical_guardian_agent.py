from MindMateAI.utils.model_loader import ModelLoader
from langgraph.prebuilt import create_react_agent
from MindMateAI.logger import logger
from langchain_core.messages import HumanMessage, SystemMessage
from MindMateAI.tools.ethical_guardian_tool import EthicalGuardianTool
from MindMateAI.Agents.mental_health_state import MentalHealthState

def create_ethical_guardian_agent(state: MentalHealthState):
    """
    Ethical Guardian Agent: Specializes in ensuring ethical guidelines are followed
    """
    tools = [EthicalGuardianTool().ethical_guardian_tool]

    ETHICAL_GUARDIAN_PROMPT = """
        You are an Ethical Guardian Agent ensuring all mental health responses are safe and appropriate.
        Your role is to review therapeutic responses and schedules for ethical compliance and safety.

        Guidelines:
        - Check for any harmful or inappropriate advice
        - Ensure responses don't exceed professional boundaries
        - Verify that suggestions are safe and realistic
        - Look for any content that might be triggering or harmful
        - Ensure responses don't provide medical diagnoses or prescriptions
        - Check that the advice is evidence-based and appropriate

        Return your response in this exact JSON format:
        {
            "ethical": true/false,
            "feedback": "detailed feedback about issues found or approval",
            "concerns": ["concern1", "concern2"] or []
        }
    """

    # Load the LLM model
    model_loader = ModelLoader(model_provider="groq")
    llm = model_loader.load_llm()
    logger.info("Ethical Guardian Agent...")

    def dynamic_prompt(state):
        return [
            SystemMessage(content=ETHICAL_GUARDIAN_PROMPT),
            HumanMessage(content=f"CBT Response: {state['cbt_response']}\nSchedule: {state['schedule_recommendation']}")
        ]
    
    return create_react_agent(
        llm,
        tools=tools,
        prompt=dynamic_prompt,
        state_schema=MentalHealthState
    )