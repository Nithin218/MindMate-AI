from MindMateAI.utils.model_loader import ModelLoader
from langgraph.prebuilt import create_react_agent
from MindMateAI.logger import logger
from langchain_core.messages import HumanMessage, SystemMessage
from MindMateAI.tools.resource_schedule_tool import ResourceScheduleTool
from MindMateAI.Agents.mental_health_state import MentalHealthState

def create_resource_schedule_agent(state: MentalHealthState):
    """
    Resource Schedule Agent: Specializes in scheduling resources for users
    """
    tools = [ResourceScheduleTool().resource_schedule_tool]

    RESOURCE_SCHEDULE_PROMPT = """
        You are a Resource and Schedule Agent for mental health support.
        Your role is to provide scheduling recommendations and resource suggestions based on the therapeutic response.

        Guidelines:
        - Suggest appropriate scheduling for mental health activities
        - Recommend frequency and timing for therapeutic practices
        - Consider the user's emotional state when making recommendations
        - Provide realistic and achievable scheduling suggestions
        - Include self-care activities and coping strategies timing
        - Be specific about implementation

        Return your response in this JSON format:
        {
            "schedule": {
                "daily_activities": ["activity1", "activity2"],
                "weekly_goals": ["goal1", "goal2"],
                "timing_recommendations": "specific timing advice"
            },
            "resources": ["resource1", "resource2"]
        }
    """

    # Load the LLM model
    model_loader = ModelLoader(model_provider="groq")
    llm = model_loader.load_llm()
    logger.info("Resource Schedule Agent...")


    def state_modifier(state):
        return [
            SystemMessage(content=RESOURCE_SCHEDULE_PROMPT),
            HumanMessage(content=f"Therapeutic Response: {state['cbt_response']}\nEmotion: {state['emotion']}")
        ]
    
    return create_react_agent(
        llm,
        tools=tools,
        state_modifier=state_modifier
    )