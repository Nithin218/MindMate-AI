from MindMateAI.utils.model_loader import ModelLoader
from langgraph.prebuilt import create_react_agent
from MindMateAI.logger import logger
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage

def create_query_rewriting_agent():
    """
    Query Rewriting Agent: Specializes in rewriting user queries into LLM-friendly prompts
    """
    system_prompt = """
    User query: {input}

    You are a Query Rewriting Agent. Your job is to:
        1. Take unclear, ambiguous, or casual user queries
        2. Rewrite them into clear, precise, and well-structured prompts
        3. Preserve the user’s original intent
        4. Avoid answering the query

    Only return the rewritten prompt. Do not explain or elaborate.
    """
    # Load the LLM model
    model_loader = ModelLoader(model_provider="groq")
    llm = model_loader.load_llm()
    logger.info("Creating Query Rewriting Agent...")

    # Only input variable needed is 'input' since no tools or scratchpad are used
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt),
        # The agent expects a placeholder for the conversation history
        ("placeholder", "{messages}")
    ])
    prompt.input_variables = ["messages"]

    # ✅ Return the agent (even with no tools)
    return create_react_agent(llm, [], prompt=prompt)