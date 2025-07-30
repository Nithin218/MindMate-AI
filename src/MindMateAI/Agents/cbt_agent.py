from MindMateAI.utils.model_loader import ModelLoader
from langgraph.prebuilt import create_react_agent
from MindMateAI.logger import logger
from langchain_core.messages import HumanMessage, SystemMessage
from MindMateAI.tools.web_search_tool import tavily_tool
from MindMateAI.tools.cbt_guide_tool import CBTGuideTool

def create_cbt_agent():
    """
    CBT Agent: Specializes in Cognitive Behavioral Therapy (CBT) techniques
    """
    tools = [tavily_tool, CBTGuideTool().cbt_guide_tool]

    CBT_AGENT_PROMPT = """
        You are a CBT (Cognitive Behavioral Therapy) Agent providing therapeutic responses.
        Your role is to generate evidence-based therapeutic responses based on the user's query and identified emotion.

        Guidelines:
        - Use CBT principles and techniques
        - Provide compassionate, professional, and helpful responses
        - Include coping strategies, thought reframing, or behavioral suggestions when appropriate
        - Be supportive but not prescriptive
        - Tailor your response to the specific emotion identified
        - Keep responses practical and actionable
        - Always maintain professional boundaries

        Generate a therapeutic response that addresses the user's emotional state and query.
    """

    # Load the LLM model
    model_loader = ModelLoader(model_provider="groq")
    llm = model_loader.load_llm()
    logger.info("CBT Guide Agent...")


    def dynamic_prompt(state):
        return [
            SystemMessage(content=CBT_AGENT_PROMPT),
            HumanMessage(content=f"Query: {state['rewritten_query']}\nEmotion: {state['emotion']}")
        ]
    
    return create_react_agent(
        llm,
        tools=tools,
        prompt=dynamic_prompt,
        state_schema=MentalHealthState
    )