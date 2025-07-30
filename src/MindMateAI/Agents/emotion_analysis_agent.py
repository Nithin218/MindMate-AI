from MindMateAI.utils.model_loader import ModelLoader
from langgraph.prebuilt import create_react_agent
from MindMateAI.logger import logger
from langchain_core.messages import HumanMessage, SystemMessage
from MindMateAI.tools.emotion_analysis_tool import EmotionAnalysisTool
from MindMateAI.Agents.mental_health_state import MentalHealthState



def create_emotion_analysis_agent(state: MentalHealthState):
    """
    Emotion Analysis Agent: Specializes in analyzing user emotions from text
    """

    tools = [EmotionAnalysisTool().emotion_analysis_tool]


    EMOTION_ANALYST_PROMPT = """
        You are an Emotion Analysis Agent specialized in detecting and categorizing emotions from text.
        Your role is to analyze the rewritten query and identify the primary emotion expressed.

        Guidelines:
        - Identify the primary emotion (e.g., anxiety, depression, anger, fear, sadness, joy, etc.)
        - Consider both explicit emotional words and implicit emotional indicators
        - Be precise and specific in your emotion identification
        - If multiple emotions are present, identify the dominant one
        - Consider the context and underlying emotional state

        Return your response in this exact JSON format:
        {
            "emotion": "identified_emotion",
            "confidence": "high/medium/low",
            "secondary_emotions": ["emotion1", "emotion2"]
        }
    """
    
    # Load the LLM model
    model_loader = ModelLoader(model_provider="groq")
    llm = model_loader.load_llm()
    logger.info("Emotion Analysis Agent...")

    def state_modifier(state):
        return [
            SystemMessage(content=EMOTION_ANALYST_PROMPT),
            HumanMessage(content=state["rewritten_query"])
        ]
    
    return create_react_agent(
        llm,
        tools=tools,
        state_modifier=state_modifier
    )