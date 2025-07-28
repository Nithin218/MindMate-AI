# Unified CBT Tool - Comprehensive Mental Health Support
# Combines CBT guidance with stress relief and personalized coping strategies

from langchain_core.tools import tool
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from enum import Enum
import re
import json
import random

class StressLevel(Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    SEVERE = "severe"

class EmotionalState(Enum):
    ANXIOUS = "anxious"
    OVERWHELMED = "overwhelmed"
    FRUSTRATED = "frustrated"
    WORRIED = "worried"
    ANGRY = "angry"
    SAD = "sad"
    DEPRESSED = "depressed"
    CONFUSED = "confused"
    IRRITATED = "irritated"
    HOPELESS = "hopeless"
    RESTLESS = "restless"

class CopingCategory(Enum):
    BEHAVIORAL = "behavioral"
    COGNITIVE = "cognitive"
    PHYSICAL = "physical"
    SOCIAL = "social"
    MINDFULNESS = "mindfulness"
    CREATIVE = "creative"

class CognitiveDistortion(Enum):
    ALL_OR_NOTHING = "all_or_nothing"
    CATASTROPHIZING = "catastrophizing"
    MIND_READING = "mind_reading"
    PERSONALIZATION = "personalization"
    SHOULD_STATEMENTS = "should_statements"
    MENTAL_FILTER = "mental_filter"
    FORTUNE_TELLING = "fortune_telling"
    EMOTIONAL_REASONING = "emotional_reasoning"

class UnifiedCBTAgent:
    def __init__(self):
        # Core CBT techniques with detailed information
        self.cbt_techniques = {
            "Thought Challenging": {
                "description": "Examine the evidence for and against your negative thoughts",
                "questions": [
                    "What evidence supports this thought?",
                    "What evidence contradicts this thought?", 
                    "What would you tell a friend having this thought?",
                    "Is this thought helpful or harmful?",
                    "What's a more balanced way to think about this?",
                    "How likely is this outcome really?",
                    "What's the worst that could happen? How would I cope?"
                ],
                "quick_exercise": "Ask yourself: Is this thought helpful? Is it based on facts or fears? What would I tell a friend in this situation?",
                "category": "cognitive"
            },
            "Cognitive Restructuring": {
                "description": "Replace negative thoughts with more realistic and balanced ones",
                "steps": [
                    "Identify the specific negative thought",
                    "Recognize thinking errors (catastrophizing, all-or-nothing, etc.)",
                    "Generate alternative, more balanced thoughts",
                    "Choose the most realistic and helpful thought",
                    "Practice the new thought pattern regularly"
                ],
                "quick_exercise": "Write down: What happened? What did I think? How did I feel? What's the evidence for/against this thought?",
                "category": "cognitive"
            },
            "Behavioral Activation": {
                "description": "Engage in meaningful activities to improve mood and reduce stress",
                "activities": [
                    "Schedule pleasant activities daily",
                    "Break large tasks into smaller, manageable steps",
                    "Set achievable daily goals",
                    "Practice regular self-care routines",
                    "Engage in social and community activities"
                ],
                "quick_exercise": "Schedule one small, enjoyable activity for today, even if you don't feel like it",
                "category": "behavioral"
            },
            "Mindfulness Techniques": {
                "description": "Stay present and observe thoughts without judgment",
                "exercises": [
                    "5-4-3-2-1 grounding (5 things you see, 4 hear, 3 feel, 2 smell, 1 taste)",
                    "Deep breathing (4 counts in, hold 4, out 6)",
                    "Body scan meditation",
                    "Mindful observation of thoughts",
                    "Present moment awareness",
                    "Mindful walking or movement"
                ],
                "quick_exercise": "5-4-3-2-1 technique: Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste",
                "category": "mindfulness"
            },
            "Progressive Muscle Relaxation": {
                "description": "Systematically tense and relax muscle groups to reduce physical tension",
                "steps": [
                    "Start with your feet and work upward",
                    "Tense each muscle group for 5 seconds",
                    "Release and notice the relaxation",
                    "Compare the feeling of tension vs relaxation",
                    "Practice regularly for best results"
                ],
                "quick_exercise": "Tense your shoulders for 5 seconds, then release. Notice the difference between tension and relaxation",
                "category": "physical"
            },
            "Thought Records": {
                "description": "Write down thoughts, emotions, and evidence to challenge negative thinking",
                "format": [
                    "Situation: What happened?",
                    "Emotion: What did you feel? (0-10 intensity)",
                    "Automatic Thought: What went through your mind?",
                    "Evidence For: What supports this thought?",
                    "Evidence Against: What contradicts this thought?",
                    "Balanced Thought: What's a more realistic perspective?",
                    "New Emotion: How do you feel now? (0-10 intensity)"
                ],
                "quick_exercise": "Write down: What happened? What did I think? How did I feel? What's the evidence for/against this thought?",
                "category": "cognitive"
            },
            "Grounding Techniques": {
                "description": "Use your senses to stay present and reduce anxiety",
                "methods": [
                    "5-4-3-2-1 sensory grounding",
                    "Cold water on hands/face",
                    "Hold an ice cube or cold object",
                    "Name objects in the room",
                    "Feel your feet on the ground",
                    "Listen to calming sounds"
                ],
                "quick_exercise": "Press your feet firmly on the ground, name 3 things you can see, 2 you can hear, 1 you can smell",
                "category": "mindfulness"
            }
        }
        
        # Cognitive distortions with detailed explanations
        self.cognitive_distortions = {
            CognitiveDistortion.ALL_OR_NOTHING: {
                "name": "All-or-Nothing Thinking",
                "description": "Seeing things in black and white, with no middle ground",
                "examples": ["I'm a complete failure", "This is totally ruined", "I never do anything right"],
                "challenge": "Look for the gray areas. What's partially true? What would be a more balanced view?"
            },
            CognitiveDistortion.CATASTROPHIZING: {
                "name": "Catastrophizing",
                "description": "Expecting the worst possible outcome or blowing things out of proportion",
                "examples": ["This will be a disaster", "I'll never recover from this", "Everything is ruined"],
                "challenge": "What's the most likely outcome? How have you handled difficulties before?"
            },
            CognitiveDistortion.MIND_READING: {
                "name": "Mind Reading",
                "description": "Assuming you know what others are thinking without evidence",
                "examples": ["They think I'm stupid", "Everyone is judging me", "They don't like me"],
                "challenge": "What evidence do you have? Could there be other explanations for their behavior?"
            },
            CognitiveDistortion.PERSONALIZATION: {
                "name": "Personalization",
                "description": "Blaming yourself for things outside your control",
                "examples": ["It's all my fault", "I should have prevented this", "I'm responsible for their feelings"],
                "challenge": "What factors were outside your control? What would you tell a friend in this situation?"
            },
            CognitiveDistortion.SHOULD_STATEMENTS: {
                "name": "Should Statements",
                "description": "Using rigid rules about how things 'should' be",
                "examples": ["I should be perfect", "They should understand me", "Life should be fair"],
                "challenge": "Replace 'should' with 'prefer' or 'would like'. What's realistic given the circumstances?"
            },
            CognitiveDistortion.MENTAL_FILTER: {
                "name": "Mental Filter",
                "description": "Focusing only on negative details while ignoring positive aspects",
                "examples": ["This one mistake ruins everything", "Only the criticism matters", "I can't see anything good"],
                "challenge": "What positive aspects are you overlooking? What would a balanced view include?"
            },
            CognitiveDistortion.FORTUNE_TELLING: {
                "name": "Fortune Telling",
                "description": "Predicting negative outcomes without evidence",
                "examples": ["I know this will go badly", "I'll definitely fail", "Nothing good will happen"],
                "challenge": "What evidence supports this prediction? What other outcomes are possible?"
            },
            CognitiveDistortion.EMOTIONAL_REASONING: {
                "name": "Emotional Reasoning",
                "description": "Believing something is true because you feel it strongly",
                "examples": ["I feel guilty, so I must have done something wrong", "I feel hopeless, so there's no point trying"],
                "challenge": "Feelings are valid but not always accurate. What do the facts tell you?"
            }
        }
        
        # Enhanced coping strategies with CBT integration
        self.coping_strategies = {
            CopingCategory.BEHAVIORAL: {
                "watching_movies": {
                    "similar": ["watching documentaries", "listening to podcasts", "reading books", "playing calming video games"],
                    "alternatives": ["journaling thoughts about movies", "creating movie reviews", "discussing films with others", "mindful movie watching"],
                    "cbt_technique": "Behavioral Activation",
                    "thought_challenges": ["How does this activity affect my mood?", "Am I using this to avoid something?"]
                },
                "sleeping": {
                    "similar": ["taking short naps (20-30 min)", "doing relaxation exercises", "listening to sleep stories"],
                    "alternatives": ["sleep hygiene routine", "progressive muscle relaxation", "bedtime journaling", "gratitude practice before sleep"],
                    "cbt_technique": "Sleep Hygiene & Behavioral Regulation",
                    "thought_challenges": ["Am I sleeping to avoid problems?", "How can I improve my sleep quality?"]
                },
                "eating": {
                    "similar": ["mindful eating", "trying healthy recipes", "drinking herbal teas"],
                    "alternatives": ["food mood journaling", "cooking as meditation", "sharing meals with others", "exploring new cuisines mindfully"],
                    "cbt_technique": "Mindful Consumption",
                    "thought_challenges": ["Am I eating due to emotions?", "How does this food make me feel physically and mentally?"]
                }
            },
            CopingCategory.COGNITIVE: {
                "thinking": {
                    "similar": ["reflecting", "analyzing situations", "problem-solving"],
                    "alternatives": ["thought challenging", "gratitude practice", "positive self-talk", "reframing exercises"],
                    "cbt_technique": "Cognitive Restructuring",
                    "thought_challenges": ["Are my thoughts helpful?", "What evidence supports my conclusions?"]
                },
                "worrying": {
                    "similar": ["planning", "list-making", "researching solutions"],
                    "alternatives": ["worry time scheduling", "fact vs. fear analysis", "worst-case scenario planning", "acceptance exercises"],
                    "cbt_technique": "Worry Management", 
                    "thought_challenges": ["Is this worry productive?", "What can I actually control?"]
                }
            },
            CopingCategory.PHYSICAL: {
                "exercising": {
                    "similar": ["walking", "stretching", "yoga", "dancing", "swimming"],
                    "alternatives": ["breathing exercises", "tai chi", "desk exercises", "nature walks"],
                    "cbt_technique": "Physical Activation",
                    "thought_challenges": ["How does movement affect my thoughts?", "What physical activities bring me joy?"]
                }
            },
            CopingCategory.MINDFULNESS: {
                "meditating": {
                    "similar": ["deep breathing", "body scans", "mindful observation"],
                    "alternatives": ["walking meditation", "mindful daily activities", "loving-kindness meditation", "grounding exercises"],
                    "cbt_technique": "Mindfulness-Based Stress Reduction",
                    "thought_challenges": ["What am I noticing without judgment?", "How can I be more present?"]
                }
            }
        }
        
        # Stress level indicators
        self.stress_indicators = {
            StressLevel.LOW: ["slightly", "a bit", "minor", "small", "little", "manageable"],
            StressLevel.MODERATE: ["somewhat", "moderately", "fairly", "quite", "pretty", "medium"],
            StressLevel.HIGH: ["very", "really", "extremely", "quite", "significantly", "major"],
            StressLevel.SEVERE: ["overwhelmingly", "unbearably", "severely", "desperately", "critically", "intensely"]
        }
        
        # Emotional state keywords
        self.emotion_keywords = {
            EmotionalState.ANXIOUS: ["anxious", "nervous", "worried", "tense", "uneasy", "jittery", "fearful"],
            EmotionalState.OVERWHELMED: ["overwhelmed", "swamped", "buried", "drowning", "too much"],
            EmotionalState.FRUSTRATED: ["frustrated", "annoyed", "irritated", "fed up", "exasperated"],
            EmotionalState.WORRIED: ["worried", "concerned", "fearful", "apprehensive", "troubled"],
            EmotionalState.ANGRY: ["angry", "mad", "furious", "rage", "pissed", "livid"],
            EmotionalState.SAD: ["sad", "down", "blue", "melancholy", "dejected"],
            EmotionalState.DEPRESSED: ["depressed", "hopeless", "empty", "worthless", "helpless"],
            EmotionalState.CONFUSED: ["confused", "lost", "unclear", "mixed up", "puzzled"],
            EmotionalState.IRRITATED: ["irritated", "agitated", "bothered", "vexed", "irked"],
            EmotionalState.HOPELESS: ["hopeless", "helpless", "defeated", "despairing", "lost"],
            EmotionalState.RESTLESS: ["restless", "agitated", "fidgety", "can't sit still", "antsy"]
        }

    def analyze_emotional_state(self, user_input: str) -> Dict[str, Any]:
        """Enhanced emotional analysis with distortion detection"""
        
        user_input_lower = user_input.lower()
        
        # Detect stress level
        stress_level = StressLevel.LOW
        for level, indicators in self.stress_indicators.items():
            if any(indicator in user_input_lower for indicator in indicators):
                stress_level = level
                break
        
        # Detect emotional states
        detected_emotions = []
        for emotion, keywords in self.emotion_keywords.items():
            if any(keyword in user_input_lower for keyword in keywords):
                detected_emotions.append(emotion)
        
        # Detect cognitive distortions
        detected_distortions = []
        for distortion, info in self.cognitive_distortions.items():
            for example in info["examples"]:
                if any(phrase.lower() in user_input_lower for phrase in example.split()):
                    detected_distortions.append(distortion)
                    break
        
        # If no specific emotions detected, infer from context
        if not detected_emotions:
            if any(word in user_input_lower for word in ["stress", "stressed", "pressure"]):
                detected_emotions.append(EmotionalState.OVERWHELMED)
        
        return {
            "stress_level": stress_level,
            "emotional_states": detected_emotions,
            "cognitive_distortions": detected_distortions,
            "analysis_confidence": self._calculate_confidence(user_input, stress_level, detected_emotions)
        }

    def extract_current_coping_methods(self, user_input: str) -> List[Dict[str, Any]]:
        """Extract mentioned coping methods from user input"""
        
        user_input_lower = user_input.lower()
        detected_methods = []
        
        # Enhanced coping method keywords
        coping_keywords = {
            "watching_movies": ["watch", "movie", "film", "netflix", "tv", "show", "streaming"],
            "sleeping": ["sleep", "nap", "rest", "bed", "tired", "lie down"],
            "eating": ["eat", "food", "snack", "meal", "hungry", "comfort food"],
            "shopping": ["shop", "buy", "purchase", "mall", "store", "online shopping"],
            "cleaning": ["clean", "tidy", "organize", "declutter", "neat"],
            "exercising": ["exercise", "workout", "gym", "run", "fitness", "sports"],
            "walking": ["walk", "stroll", "hike", "outdoors", "nature"],
            "thinking": ["think", "analyze", "contemplate", "reflect", "ponder"],
            "worrying": ["worry", "anxious", "overthink", "ruminate", "stress"],
            "talking": ["talk", "chat", "call", "friend", "family", "conversation"],
            "isolating": ["alone", "isolate", "withdraw", "hide", "avoid", "solitude"],
            "meditating": ["meditate", "mindful", "breathe", "calm", "zen"],
            "music": ["music", "listen", "song", "playlist", "audio", "sounds"],
            "art": ["draw", "paint", "craft", "create", "art", "creative"],
            "writing": ["write", "journal", "diary", "blog", "notes"]
        }
        
        for method, keywords in coping_keywords.items():
            if any(keyword in user_input_lower for keyword in keywords):
                # Find which category this method belongs to
                for category, methods in self.coping_strategies.items():
                    if method in methods:
                        detected_methods.append({
                            "method": method,
                            "category": category,
                            "confidence": self._calculate_method_confidence(user_input_lower, keywords)
                        })
                        break
        
        return detected_methods

    def generate_cbt_guidance(self, user_input: str, concern_type: str = "general") -> Dict[str, Any]:
        """Generate comprehensive CBT guidance based on input analysis"""
        
        emotional_analysis = self.analyze_emotional_state(user_input)
        current_methods = self.extract_current_coping_methods(user_input)
        
        # Select appropriate CBT techniques based on emotions and distortions
        recommended_techniques = []
        emotions = emotional_analysis["emotional_states"]
        distortions = emotional_analysis["cognitive_distortions"]
        stress_level = emotional_analysis["stress_level"]
        
        # Match techniques to emotional states
        technique_mapping = {
            EmotionalState.ANXIOUS: ["Grounding Techniques", "Progressive Muscle Relaxation", "Thought Challenging"],
            EmotionalState.OVERWHELMED: ["Mindfulness Techniques", "Behavioral Activation", "Grounding Techniques"],
            EmotionalState.WORRIED: ["Thought Challenging", "Cognitive Restructuring", "Worry Management"],
            EmotionalState.DEPRESSED: ["Behavioral Activation", "Thought Records", "Cognitive Restructuring"],
            EmotionalState.ANGRY: ["Progressive Muscle Relaxation", "Mindfulness Techniques", "Thought Challenging"],
            EmotionalState.CONFUSED: ["Thought Records", "Cognitive Restructuring", "Problem-Solving"]
        }
        
        for emotion in emotions:
            if emotion in technique_mapping:
                for technique in technique_mapping[emotion]:
                    if technique in self.cbt_techniques and technique not in recommended_techniques:
                        recommended_techniques.append(technique)
        
        # Add distortion-specific techniques
        if distortions:
            if CognitiveDistortion.CATASTROPHIZING in distortions or CognitiveDistortion.FORTUNE_TELLING in distortions:
                if "Thought Challenging" not in recommended_techniques:
                    recommended_techniques.append("Thought Challenging")
            if CognitiveDistortion.ALL_OR_NOTHING in distortions or CognitiveDistortion.MENTAL_FILTER in distortions:
                if "Cognitive Restructuring" not in recommended_techniques:
                    recommended_techniques.append("Cognitive Restructuring")
        
        # Default techniques for high stress
        if stress_level in [StressLevel.HIGH, StressLevel.SEVERE]:
            priority_techniques = ["Grounding Techniques", "Progressive Muscle Relaxation"]
            for tech in priority_techniques:
                if tech not in recommended_techniques:
                    recommended_techniques.insert(0, tech)
        
        # If no techniques recommended, provide general ones
        if not recommended_techniques:
            recommended_techniques = ["Mindfulness Techniques", "Thought Challenging", "Behavioral Activation"]
        
        return {
            "emotional_analysis": emotional_analysis,
            "current_coping_methods": current_methods,
            "recommended_techniques": recommended_techniques[:3],  # Top 3 recommendations
            "personalized_guidance": self._generate_personalized_guidance(
                emotions, distortions, stress_level, current_methods
            ),
            "immediate_exercises": self._get_immediate_exercises(recommended_techniques[:2]),
            "distortion_challenges": self._get_distortion_challenges(distortions),
            "coping_improvements": self._suggest_coping_improvements(current_methods)
        }

    def _calculate_confidence(self, user_input: str, stress_level: StressLevel, emotions: List[EmotionalState]) -> float:
        """Calculate confidence in emotional analysis"""
        confidence = 0.5  # Base confidence
        
        # Increase confidence based on explicit emotional language
        emotional_words = len([word for word in user_input.lower().split() 
                             if any(word in keywords for keywords in self.emotion_keywords.values())])
        confidence += min(emotional_words * 0.1, 0.3)
        
        # Increase confidence for stress indicators
        if stress_level != StressLevel.LOW:
            confidence += 0.2
        
        return min(confidence, 1.0)

    def _calculate_method_confidence(self, user_input: str, keywords: List[str]) -> float:
        """Calculate confidence in detected coping method"""
        matched_keywords = sum(1 for keyword in keywords if keyword in user_input)
        return min(matched_keywords * 0.3, 1.0)

    def _generate_personalized_guidance(self, emotions: List[EmotionalState], 
                                      distortions: List[CognitiveDistortion],
                                      stress_level: StressLevel,
                                      current_methods: List[Dict]) -> str:
        """Generate personalized guidance message"""
        
        guidance_parts = []
        
        # Address emotions
        if emotions:
            emotion_names = [emotion.value for emotion in emotions]
            guidance_parts.append(f"I notice you're experiencing {', '.join(emotion_names[:2])} feelings.")
        
        # Address stress level
        if stress_level in [StressLevel.HIGH, StressLevel.SEVERE]:
            guidance_parts.append("Your stress level seems quite elevated right now, so let's focus on immediate relief techniques first.")
        
        # Address distortions
        if distortions:
            guidance_parts.append("I've identified some thinking patterns that might be contributing to your distress. We can work on challenging these thoughts.")
        
        # Address current coping methods
        if current_methods:
            method_names = [method["method"].replace("_", " ") for method in current_methods[:2]]
            guidance_parts.append(f"I see you're currently using {', '.join(method_names)} to cope. Let's explore how to enhance these strategies.")
        
        if not guidance_parts:
            guidance_parts.append("Let's work together to develop some effective coping strategies.")
        
        return " ".join(guidance_parts)

    def _get_immediate_exercises(self, techniques: List[str]) -> List[Dict[str, str]]:
        """Get immediate exercises for recommended techniques"""
        exercises = []
        for technique in techniques:
            if technique in self.cbt_techniques:
                exercises.append({
                    "technique": technique,
                    "exercise": self.cbt_techniques[technique]["quick_exercise"]
                })
        return exercises

    def _get_distortion_challenges(self, distortions: List[CognitiveDistortion]) -> List[Dict[str, str]]:
        """Get specific challenges for detected cognitive distortions"""
        challenges = []
        for distortion in distortions:
            if distortion in self.cognitive_distortions:
                info = self.cognitive_distortions[distortion]
                challenges.append({
                    "distortion": info["name"],
                    "description": info["description"],
                    "challenge": info["challenge"]
                })
        return challenges

    def _suggest_coping_improvements(self, current_methods: List[Dict]) -> List[Dict[str, Any]]:
        """Suggest improvements to current coping methods"""
        improvements = []
        
        for method_info in current_methods:
            method = method_info["method"]
            category = method_info["category"]
            
            # Find the method in our strategies
            for cat, methods in self.coping_strategies.items():
                if method in methods:
                    strategy_info = methods[method]
                    improvements.append({
                        "current_method": method.replace("_", " "),
                        "category": category.value,
                        "alternatives": strategy_info["alternatives"][:2],
                        "cbt_integration": strategy_info["cbt_technique"],
                        "thought_challenges": strategy_info["thought_challenges"][:2]
                    })
                    break
        
        return improvements

    def create_action_plan(self, guidance: Dict[str, Any], timeframe: str = "daily") -> Dict[str, Any]:
        """Create a structured action plan based on guidance"""
        
        action_plan = {
            "immediate_actions": [],
            "daily_practices": [],
            "weekly_goals": [],
            "monitoring_tools": []
        }
        
        # Immediate actions from exercises
        for exercise in guidance["immediate_exercises"]:
            action_plan["immediate_actions"].append({
                "action": f"Practice {exercise['technique']}",
                "description": exercise["exercise"],
                "duration": "5-10 minutes",
                "priority": "high"
            })
        
        # Daily practices from recommended techniques
        for technique in guidance["recommended_techniques"]:
            if technique in self.cbt_techniques:
                tech_info = self.cbt_techniques[technique]
                action_plan["daily_practices"].append({
                    "practice": technique,
                    "description": tech_info["description"],
                    "frequency": "Once daily",
                    "category": tech_info["category"]
                })
        
        # Monitoring tools
        action_plan["monitoring_tools"] = [
            {"tool": "Mood tracking", "description": "Rate your mood 1-10 daily"},
            {"tool": "Thought record", "description": "Write down negative thoughts and challenges"},
            {"tool": "Stress level check", "description": "Monitor stress levels throughout the day"}
        ]
        
        return action_plan

# Tool implementation
@tool
def cbt_guide_tool(
    user_concern: str,
    concern_type: str = "general",
    include_action_plan: bool = True
) -> Dict[str, Any]:
    """
    Comprehensive CBT-based mental health support tool that analyzes user concerns
    and provides personalized guidance, coping strategies, and action plans.
    
    Args:
        user_concern: User's description of their current situation, feelings, or concerns
        concern_type: Type of concern (general, anxiety, depression, stress, relationship)
        include_action_plan: Whether to include a structured action plan
    
    Returns:
        Dict containing analysis, recommendations, exercises, and optionally an action plan
    """
    
    agent = UnifiedCBTAgent()
    
    # Generate comprehensive guidance
    guidance = agent.generate_cbt_guidance(user_concern, concern_type)
    
    # Create response structure
    response = {
        "emotional_analysis": {
            "detected_emotions": [emotion.value for emotion in guidance["emotional_analysis"]["emotional_states"]],
            "stress_level": guidance["emotional_analysis"]["stress_level"].value,
            "confidence": guidance["emotional_analysis"]["analysis_confidence"]
        },
        "cognitive_distortions": guidance["distortion_challenges"],
        "current_coping_methods": guidance["current_coping_methods"],
        "personalized_guidance": guidance["personalized_guidance"],
        "recommended_techniques": [
            {
                "name": technique,
                "description": agent.cbt_techniques[technique]["description"],
                "quick_exercise": agent.cbt_techniques[technique]["quick_exercise"]
            }
            for technique in guidance["recommended_techniques"]
        ],
        "immediate_exercises": guidance["immediate_exercises"],
        "coping_improvements": guidance["coping_improvements"],
        "timestamp": datetime.now().isoformat()
    }
    
    # Add action plan if requested
    if include_action_plan:
        response["action_plan"] = agent.create_action_plan(guidance)
    
    return response