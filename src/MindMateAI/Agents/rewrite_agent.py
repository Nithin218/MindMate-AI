from MindMateAI.utils.model_loader import ModelLoader
from langgraph.prebuilt import create_react_agent
from MindMateAI.logger import logger
from langchain_core.messages import HumanMessage, SystemMessage
from MindMateAI.Agents.mental_health_state import MentalHealthState

def create_query_rewriting_agent(state: MentalHealthState):
    """
    Query Rewriting Agent: Specializes in rewriting user queries into LLM-friendly prompts
    """
    REWRITE_AGENT_PROMPT = """
        You are a Query Rewrite Agent for a mental health assistant system.
        Your role is to take user queries and rewrite them to be more clear, specific, and suitable for mental health analysis.

        Guidelines:
        - Preserve the core intent and emotional content
        - Make the query more structured and clear
        - Remove any unclear or ambiguous language
        - Ensure the rewritten query is suitable for emotion analysis and therapeutic response
        - Keep the user's tone and emotional state intact

        Return only the rewritten query, nothing else.
    """

    # Load the LLM model
    model_loader = ModelLoader(model_provider="groq")
    llm = model_loader.load_llm()
    logger.info("Query Rewriting Agent...")

    def state_modifier(state):
        return [
            SystemMessage(content=REWRITE_AGENT_PROMPT),
            HumanMessage(content=state["user_query"])
        ]
    
    return create_react_agent(
        llm,
        tools=[],
        state_modifier=state_modifier
    )