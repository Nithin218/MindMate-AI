from MindMateAI.Agents.mental_health_state import MentalHealthState
from MindMateAI.Agents.rewrite_agent import create_query_rewriting_agent
from MindMateAI.Agents.emotion_analysis_agent import create_emotion_analysis_agent
from MindMateAI.Agents.resource_schedule_agent import create_resource_schedule_agent
from MindMateAI.Agents.ethical_guardian_agent import create_ethical_guardian_agent
from MindMateAI.Agents.cbt_agent import create_cbt_agent
from MindMateAI.Agents.writer_agent import create_writer_agent
from MindMateAI.logger import logger
from typing import TypedDict, Literal, List, Dict, Any
from langgraph.graph import StateGraph, START, END
import json

class GraphBuilder:
    def __init__(self):
        self.graph = None

    def rewrite_node(self, state: MentalHealthState) -> MentalHealthState:
        """Rewrite the user query for better processing"""
        agent = create_query_rewriting_agent(state)

        logger.info("Rewriting user query...")
        
        # Pass the actual state to the agent, not empty messages
        result = agent.invoke(state)
        
        # Extract the rewritten query from the agent's response
        rewritten_query = result["messages"][-1].content
        
        return {
            **state,
            "rewritten_query": rewritten_query,
            "messages": state.get("messages", []) + [{"role": "rewrite", "content": rewritten_query}]
        }

    def emotion_analysis_node(self, state: MentalHealthState) -> MentalHealthState:
        """Analyze emotion from the rewritten query"""
        agent = create_emotion_analysis_agent(state)
        
        # Pass the actual state to the agent
        result = agent.invoke(state)
        
        # Extract emotion analysis
        analysis_content = result["messages"][-1].content
        try:
            # Try to parse JSON response
            analysis = json.loads(analysis_content)
            emotion = analysis.get("emotion", "neutral")
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract emotion from plain text
            emotion = "neutral"  # Fallback
            if "anxiety" in analysis_content.lower():
                emotion = "anxiety"
            elif "depression" in analysis_content.lower() or "sad" in analysis_content.lower():
                emotion = "sadness"
            elif "anger" in analysis_content.lower() or "angry" in analysis_content.lower():
                emotion = "anger"
            elif "fear" in analysis_content.lower() or "scared" in analysis_content.lower():
                emotion = "fear"
            elif "joy" in analysis_content.lower() or "happy" in analysis_content.lower():
                emotion = "joy"
        
        return {
            **state,
            "emotion": emotion,
            "messages": state.get("messages", []) + [{"role": "emotion_analyst", "content": analysis_content}]
        }

    def cbt_agent_node(self, state: MentalHealthState) -> MentalHealthState:
        """Generate CBT therapeutic response"""
        agent = create_cbt_agent(state)
        
        # Pass the actual state to the agent
        result = agent.invoke(state)
        
        cbt_response = result["messages"][-1].content
        
        return {
            **state,
            "cbt_response": cbt_response,
            "messages": state.get("messages", []) + [{"role": "cbt_agent", "content": cbt_response}]
        }

    def resource_schedule_node(self, state: MentalHealthState) -> MentalHealthState:
        """Generate schedule and resource recommendations"""
        agent = create_resource_schedule_agent(state)
        
        # Pass the actual state to the agent
        result = agent.invoke(state)
        
        schedule_content = result["messages"][-1].content
        
        return {
            **state,
            "schedule_recommendation": schedule_content,
            "messages": state.get("messages", []) + [{"role": "resource_schedule", "content": schedule_content}]
        }

    def ethical_guardian_node(self, state: MentalHealthState) -> MentalHealthState:
        """Check ethical compliance of the response"""
        agent = create_ethical_guardian_agent(state)
        
        # Pass the actual state to the agent
        result = agent.invoke(state)
        
        ethical_content = result["messages"][-1].content
        try:
            ethical_analysis = json.loads(ethical_content)
            ethical_check = ethical_analysis.get("ethical", True)
            ethical_feedback = ethical_analysis.get("feedback", "")
        except json.JSONDecodeError:
            # If JSON parsing fails, assume ethical unless explicit concerns
            ethical_check = True
            ethical_feedback = "Ethical review completed"
            if any(word in ethical_content.lower() for word in ["harmful", "inappropriate", "unethical", "dangerous"]):
                ethical_check = False
                ethical_feedback = "Ethical concerns identified in response"
        
        return {
            **state,
            "ethical_check": ethical_check,
            "ethical_feedback": ethical_feedback,
            "messages": state.get("messages", []) + [{"role": "ethical_guardian", "content": ethical_content}]
        }

    def writer_agent_node(self, state: MentalHealthState) -> MentalHealthState:
        """Create the final formatted output"""
        agent = create_writer_agent(state)
        
        # Pass the actual state to the agent
        result = agent.invoke(state)
        
        final_output = result["messages"][-1].content
        
        return {
            **state,
            "final_output": final_output,
            "messages": state.get("messages", []) + [{"role": "writer", "content": final_output}]
        }

    def supervisor_routing(self, state: MentalHealthState) -> Literal["ethical_pass", "ethical_fail", "max_retries"]:
        """Supervisor routing logic for ethical checks"""
        if not state.get("ethical_check", True):
            retry_count = state.get("retry_count", 0)
            if retry_count >= 3:  # Max retries to prevent infinite loops
                return "max_retries"
            return "ethical_fail"
        return "ethical_pass"

    def increment_retry_counter(self, state: MentalHealthState) -> MentalHealthState:
        """Increment retry counter for failed ethical checks"""
        return {
            **state,
            "retry_count": state.get("retry_count", 0) + 1
        }

    def handle_max_retries(self, state: MentalHealthState) -> MentalHealthState:
        """Handle case where maximum retries are reached"""
        return {
            **state,
            "final_output": "I apologize, but I'm unable to provide a suitable response at this time. Please consider speaking with a qualified mental health professional for personalized support."
        }

    def build_graph(self):
        """Create and return the complete mental health assistant workflow"""
        
        # Initialize the graph
        workflow = StateGraph(MentalHealthState)
        
        # Add all nodes
        workflow.add_node("rewrite", self.rewrite_node)
        workflow.add_node("emotion_analysis", self.emotion_analysis_node)
        workflow.add_node("cbt_agent", self.cbt_agent_node)
        workflow.add_node("resource_schedule", self.resource_schedule_node)
        workflow.add_node("ethical_guardian", self.ethical_guardian_node)
        workflow.add_node("writer", self.writer_agent_node)
        workflow.add_node("increment_retry", self.increment_retry_counter)
        workflow.add_node("max_retries_handler", self.handle_max_retries)

        # Define the workflow edges
        workflow.add_edge(START, "rewrite")
        workflow.add_edge("rewrite", "emotion_analysis")
        workflow.add_edge("emotion_analysis", "cbt_agent")
        workflow.add_edge("cbt_agent", "resource_schedule")
        workflow.add_edge("resource_schedule", "ethical_guardian")
        
        # Conditional routing from ethical guardian
        workflow.add_conditional_edges(
            "ethical_guardian",
            self.supervisor_routing,
            {
                "ethical_pass": "writer",
                "ethical_fail": "increment_retry",
                "max_retries": "max_retries_handler"
            }
        )
        
        # Handle retry logic
        workflow.add_edge("increment_retry", "cbt_agent")  # Loop back to CBT agent
        workflow.add_edge("writer", END)
        workflow.add_edge("max_retries_handler", END)
        
        self.graph = workflow.compile()
        return self.graph

    def __call__(self):
        """Build and return the mental health assistant workflow graph"""
        return self.build_graph()

if __name__ == "__main__":
    agentic_workflow = GraphBuilder()
    agentic_workflow_graph = agentic_workflow()
    user_input = "I've been feeling really anxious about my upcoming job interview and can't sleep"

    initial_state = {
        "user_query": user_input,
        "rewritten_query": "",
        "emotion": "",
        "cbt_response": "",
        "schedule_recommendation": "",
        "ethical_check": True,
        "ethical_feedback": "",
        "final_output": "",
        "messages": [],
        "retry_count": 0,
        "remaining_steps": 5
    }
    response = agentic_workflow_graph.invoke(initial_state)

    print("Final Output:", response["final_output"])
    print("Messages:", response["messages"])