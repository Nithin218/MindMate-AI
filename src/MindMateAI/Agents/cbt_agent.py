from MindMateAI.utils.model_loader import ModelLoader
from langgraph.prebuilt import create_react_agent
from MindMateAI.logger import logger
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from MindMateAI.tools.web_search_tool import tavily_tool
from MindMateAI.tools.cbt_guide_tool import cbt_guide_tool

def create_cbt_agent():
    """
    CBT Agent: Specializes in Cognitive Behavioral Therapy (CBT) techniques
    """
    tools = [tavily_tool, cbt_guide_tool]

    system_prompt = """
    User input: {input}
    You are a CBT Agent. Your job is to:
    1. Analyze user input for emotional content
    2. Provide CBT techniques based on the analysis
    3. Format the CBT techniques into a concise, direct, and unadorned handout

    Only return the formatted handout. Do not explain or elaborate.
    """

    # Load the LLM model
    model_loader = ModelLoader(model_provider="groq")
    llm = model_loader.load_llm()
    logger.info("Creating CBT Agent...")

    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt),
        ("placeholder", "{messages}")
    ])
    prompt.input_variables = ["messages"]

    # ✅ Return the agent (even with tools)
    return create_react_agent(llm, tools, prompt=prompt) 