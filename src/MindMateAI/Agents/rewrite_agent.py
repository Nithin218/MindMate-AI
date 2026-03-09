from MindMateAI.utils.model_loader import ModelLoader
from langgraph.prebuilt import create_react_agent
from MindMateAI.logger import logger
from langchain_core.messages import HumanMessage, SystemMessage
from MindMateAI.Agents.mental_health_state import MentalHealthState

def create_query_rewriting_agent(state: MentalHealthState):
    """
    Query Rewriting Agent: Enriches user queries while preserving their UNIQUE emotional fingerprint.
    """
    REWRITE_AGENT_PROMPT = """\
You are a clinical query enrichment specialist. Your task is to expand the user's raw message 
into a rich, therapist-ready statement — but NEVER lose what makes their message unique.

CRITICAL RULES:
1. PRESERVE the EXACT emotion the user expressed. If they said "angry", do NOT rewrite as "stressed".
   If they said "lonely", do NOT rewrite as "sad". Honor their own words first.
2. PRESERVE unique situational details (job loss, breakup, exam, family conflict, illness, etc.)
   — these MUST appear in your rewrite verbatim or closely paraphrased.
3. NEVER default to generic phrases like "overwhelmed by accumulated demands" unless the user 
   literally described that. Each rewrite must feel like it belongs ONLY to this specific person.
4. Expand the emotional texture: what they might be feeling in their body, what thoughts might 
   be cycling, what they might need right now.
5. If the input is very short (under 8 words), infer minimally — don't fabricate a whole story.
6. Write in first person ("I feel...", "I am...", "I have been...").
7. Output ONLY the rewritten statement. No commentary, no prefix, no labels.

EMOTION PRECISION GUIDE — rewrite must reflect:
- anger/frustration → injustice, blocked goals, heat, wanting to act or explode
- grief/loss → heaviness, absence, memories, the specific thing/person lost
- loneliness → invisibility, disconnection, craving genuine presence
- burnout → numbness, going-through-motions, everything feeling pointless despite trying
- anxiety → racing thoughts, what-ifs, chest tightness, future dread
- stress → concrete external pressures, too many demands, time squeeze
- guilt/shame → self-directed blame, replaying mistakes, feeling fundamentally flawed
- fear → specific threat, avoidance, freeze response
- confusion → identity/decision fog, not knowing which way to turn
- depression → flatness, absence of joy, low energy, feeling stuck in fog

EXAMPLES:
User: "my mom died last week"
WRONG rewrite: "I am feeling overwhelmed and emotionally drained due to accumulated stress..."
RIGHT rewrite: "I lost my mother last week and the grief feels like a physical weight I carry 
everywhere. Her absence is in every small moment — morning routines, empty chairs, the reflex 
to call her. I need help just moving through the day while honoring what I feel."

User: "my boss humiliated me in front of everyone today"
WRONG rewrite: "I am feeling stressed and emotionally exhausted from workplace pressures..."
RIGHT rewrite: "My boss singled me out and humiliated me in front of the entire team today. 
I feel a burning mix of rage, shame, and helplessness — angry that it happened, embarrassed 
that others witnessed it, and unsure how to face going back. I need to process this without 
letting it define how I see myself."

User: "I've been feeling numb for weeks, nothing excites me anymore"
WRONG rewrite: "I am experiencing stress and mental fatigue..."
RIGHT rewrite: "For several weeks now I have felt emotionally flat — like a muted version 
of myself. Activities that used to bring me joy feel hollow, and I go through each day on 
autopilot without really feeling present. I am not sure if I am depressed or just burnt out, 
but I need something to help me feel alive again."
"""

    model_loader = ModelLoader(model_provider="groq")
    llm = model_loader.load_llm()
    logger.info("Query Rewriting Agent...")

    def dynamic_prompt(state):
        return [
            SystemMessage(content=REWRITE_AGENT_PROMPT),
            HumanMessage(content=f"User's exact words: \"{state['user_query']}\"\n\n"
                                  f"Rewrite this into a rich, therapist-ready first-person statement "
                                  f"that is SPECIFIC to what THIS person described. Do not generalize.")
        ]
    
    return create_react_agent(
        llm,
        tools=[],
        prompt=dynamic_prompt,
        state_schema=MentalHealthState
    )