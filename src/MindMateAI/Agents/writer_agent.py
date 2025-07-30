from MindMateAI.utils.model_loader import ModelLoader
from langgraph.prebuilt import create_react_agent
from MindMateAI.logger import logger
from langchain_core.messages import HumanMessage, SystemMessage
from MindMateAI.Agents.mental_health_state import MentalHealthState

def create_writer_agent(state: MentalHealthState):
    """
    Writer Agent: Specializes in generating written content
    """

    WRITER_AGENT_PROMPT = """
        You are a Writer Agent responsible for creating well-formatted, compassionate final outputs.
        Your role is to take all the therapeutic content and present it in a beautiful, user-friendly format.

        Guidelines:
        - Create a warm, empathetic tone
        - Structure the response clearly with appropriate formatting
        - Make the content easily readable and actionable
        - Include the therapeutic response, schedule, and resources in a cohesive format
        - Use encouraging and supportive language
        - Ensure the final output feels personal and caring

        Create a comprehensive, well-formatted response that combines all elements into a cohesive, helpful message.
        Return the final output as a string."""

    # Load the LLM model
    model_loader = ModelLoader(model_provider="groq")
    llm = model_loader.load_llm()
    logger.info("Writer Agent...")

    def dynamic_prompt(state):
        return [
            SystemMessage(content=WRITER_AGENT_PROMPT),
            HumanMessage(content=f"CBT Response: {state['cbt_response']}\nSchedule: {state['schedule_recommendation']}\nEmotion: {state['emotion']}")
        ]
    
    return create_react_agent(
        llm,
        tools=[],
        prompt=dynamic_prompt,
        state_schema=MentalHealthState
    )