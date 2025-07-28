# This tool analyzes text for emotional content and sentiment

from langchain_core.tools import tool
from typing import Dict, Any
import re

@tool
def emotion_analysis_tool(text: str) -> Dict[str, Any]:
    """
    Analyzes the emotional content of text input.
    
    Args:
        text (str): The text to analyze for emotions
        
    Returns:
        Dict containing emotion analysis results
    """
    
    # Define emotion keywords (in a real implementation, you'd use NLP libraries)
    emotion_keywords = {
        'joy': ['happy', 'excited', 'joyful', 'delighted', 'cheerful', 'elated'],
        'sadness': ['sad', 'depressed', 'down', 'melancholy', 'grief', 'sorrow'],
        'anger': ['angry', 'furious', 'mad', 'irritated', 'rage', 'annoyed'],
        'fear': ['afraid', 'scared', 'anxious', 'worried', 'nervous', 'terrified'],
        'surprise': ['surprised', 'amazed', 'shocked', 'astonished', 'stunned'],
        'disgust': ['disgusted', 'revolted', 'sick', 'nauseated', 'repulsed']
    }
    
    # Convert text to lowercase for analysis
    text_lower = text.lower()
    
    # Count emotion indicators
    emotion_scores = {}
    total_emotion_words = 0
    
    for emotion, keywords in emotion_keywords.items():
        count = sum(1 for keyword in keywords if keyword in text_lower)
        emotion_scores[emotion] = count
        total_emotion_words += count
    
    # Determine dominant emotion
    dominant_emotion = max(emotion_scores, key=emotion_scores.get) if total_emotion_words > 0 else 'neutral'
    
    # Calculate confidence (simple approach)
    confidence = emotion_scores[dominant_emotion] / max(len(text.split()) * 0.1, 1)
    confidence = min(confidence, 1.0)  # Cap at 100%
    
    # Determine overall sentiment
    positive_emotions = emotion_scores['joy'] + emotion_scores['surprise']
    negative_emotions = sum(emotion_scores[e] for e in ['sadness', 'anger', 'fear', 'disgust'])
    
    if positive_emotions > negative_emotions:
        sentiment = 'positive'
    elif negative_emotions > positive_emotions:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    
    return {
        'dominant_emotion': dominant_emotion,
        'confidence': round(confidence, 2),
        'sentiment': sentiment,
        'emotion_breakdown': emotion_scores,
        'total_emotion_indicators': total_emotion_words,
        'analysis_summary': f"Text shows primarily {dominant_emotion} emotion with {sentiment} sentiment"
    }

# Example usage:
if __name__ == "__main__":
    sample_text = "I'm so excited about this new project! It makes me really happy."
    result = emotion_analysis_tool.invoke({"text": sample_text})
    print("Emotion Analysis Result:")
    print(result)