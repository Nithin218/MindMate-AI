# This tool analyzes text for emotional content and sentiment

from langchain_core.tools import tool
import json


class EmotionAnalysisTool:
    """Emotion Analysis Tool for classifying user emotions from text input."""
    
    def __init__(self):
        self.emotion_analysis_tool = self._setup_tool()

    def _setup_tool(self):
        """Sets up the emotion analysis tool."""
        @tool
        def emotion_analysis_tool(query: str) -> str:
            """
            Analyzes the emotional content of the query and classifies the primary emotion.
            
            Args:
                query (str): The query to analyze
                
            Returns:
                str: JSON string containing emotion classification and confidence
            """
            
            # Emotion keywords mapping
            emotion_keywords = {
                'anxiety': ['anxious', 'worried', 'nervous', 'panic', 'fear', 'concerned', 'stress'],
                'depression': ['sad', 'depressed', 'hopeless', 'empty', 'worthless', 'down'],
                'anger': ['angry', 'mad', 'furious', 'irritated', 'frustrated', 'rage'],
                'grief': ['loss', 'death', 'mourning', 'grief', 'bereaved', 'departed'],
                'stress': ['overwhelmed', 'pressure', 'burden', 'exhausted', 'burned out'],
                'loneliness': ['lonely', 'isolated', 'alone', 'disconnected', 'abandoned'],
                'neutral': ['okay', 'fine', 'normal', 'average', 'regular']
            }
            
            query_lower = query.lower()
            emotion_scores = {}
            
            # Calculate emotion scores based on keyword presence
            for emotion, keywords in emotion_keywords.items():
                score = sum(1 for keyword in keywords if keyword in query_lower)
                if score > 0:
                    emotion_scores[emotion] = score
            
            # Determine primary emotion
            if emotion_scores:
                primary_emotion = max(emotion_scores.keys(), key=lambda k: emotion_scores[k])
                confidence = min(emotion_scores[primary_emotion] / 3.0, 1.0)  # Normalize to 0-1
            else:
                primary_emotion = 'neutral'
                confidence = 0.5
            
            result = {
                'emotion': primary_emotion,
                'confidence': confidence,
                'query': query
            }
            
            return json.dumps(result)

        return emotion_analysis_tool

    