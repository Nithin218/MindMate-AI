from MindMateAI.utils.model_loader import ModelLoader
from langgraph.prebuilt import create_react_agent
from MindMateAI.logger import logger
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from MindMateAI.tools.emotion_analysis_tool import emotion_analysis_tool



def create_emotion_analysis_agent():
    """
    Emotion Analysis Agent: Specializes in analyzing user emotions from text
    """

    tools = [emotion_analysis_tool]


    system_prompt = """
    User input: {input}

    You are an AI assistant that functions as a direct reporting tool for an emotion analysis service. Your sole purpose is to receive a user's text and the corresponding JSON output from the analysis tool, and then present the final summary to the user.

    Core Instructions:

        - Your response to the user MUST be the exact string from the analysis_summary field in the JSON output provided by the tool.

        - DO NOT add any other words, explanations, or conversational text. Do not greet the user, explain the analysis, or describe your process.

        - Your output should be the result itself, not a sentence about the result.

    Only return the emotional analysis. Do not explain or elaborate.
    """
    
    # Load the LLM model
    model_loader = ModelLoader(model_provider="groq")
    llm = model_loader.load_llm()
    logger.info("Creating Emotion Analysis Agent...")

    # Only input variable needed is 'input' since no tools or scratchpad are used
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt),
        # The agent expects a placeholder for the conversation history
        ("placeholder", "{messages}")
    ])
    prompt.input_variables = ["messages"]

    # ✅ Return the agent (even with no tools)
    return create_react_agent(llm, tools, prompt=prompt)