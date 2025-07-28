from langchain_core.tools import tool
from typing import Dict, List, Any
import re
from datetime import datetime

@tool
def ethical_guardian_bias_auditor(cbt_agent_output: str) -> Dict[str, Any]:
    """
    Analyzes CBT agent output for ethical concerns and potential biases.
    
    Args:
        cbt_agent_output (str): The output text from the CBT guide agent
        
    Returns:
        Dict containing bias analysis, ethical flags, and recommendations
    """
    
    # Initialize analysis results
    analysis_result = {
        "timestamp": datetime.now().isoformat(),
        "input_length": len(cbt_agent_output),
        "ethical_flags": [],
        "bias_indicators": [],
        "severity_level": "low",  # low, medium, high
        "approval_status": "approved",  # approved, needs_review, rejected
        "recommendations": [],
        "confidence_score": 0.0
    }
    
    # Convert to lowercase for analysis
    text_lower = cbt_agent_output.lower()
    
    # =============================================================================
    # ETHICAL GUIDELINES CHECKER
    # =============================================================================
    
    # Check for harmful content
    harmful_phrases = [
        "just get over it", "it's all in your head", "you're overreacting",
        "stop being dramatic", "others have it worse", "think positive",
        "snap out of it", "you're too sensitive", "it's not that bad"
    ]
    
    for phrase in harmful_phrases:
        if phrase in text_lower:
            analysis_result["ethical_flags"].append({
                "type": "dismissive_language",
                "phrase": phrase,
                "concern": "Minimizes client's experience"
            })
    
    # Check for inappropriate advice
    inappropriate_advice = [
        "medication", "diagnose", "prescribe", "you have", "you are",
        "definitely", "certainly have", "disorder", "mental illness"
    ]
    
    for term in inappropriate_advice:
        if term in text_lower and ("you" in text_lower):
            analysis_result["ethical_flags"].append({
                "type": "overstepping_boundaries",
                "term": term,
                "concern": "Providing medical diagnosis or advice"
            })
    
    # Check for crisis situations not properly handled
    crisis_keywords = ["suicide", "kill myself", "end it all", "hurt myself", "self-harm"]
    for keyword in crisis_keywords:
        if keyword in text_lower:
            if "professional help" not in text_lower and "emergency" not in text_lower:
                analysis_result["ethical_flags"].append({
                    "type": "crisis_mishandling",
                    "keyword": keyword,
                    "concern": "Crisis situation not properly escalated"
                })
    
    # =============================================================================
    # BIAS DETECTION
    # =============================================================================
    
    # Gender bias detection
    gender_assumptions = [
        r"women are more emotional",
        r"men don't cry",
        r"typical female response",
        r"act like a man",
        r"women overthink"
    ]
    
    for pattern in gender_assumptions:
        if re.search(pattern, text_lower):
            analysis_result["bias_indicators"].append({
                "type": "gender_bias",
                "pattern": pattern,
                "description": "Contains gender stereotypes"
            })
    
    # Cultural/religious bias
    cultural_assumptions = [
        "in our culture", "normal people", "everyone believes", 
        "traditional values", "proper way", "right thing to do"
    ]
    
    for assumption in cultural_assumptions:
        if assumption in text_lower:
            analysis_result["bias_indicators"].append({
                "type": "cultural_bias",
                "phrase": assumption,
                "description": "Makes cultural or normative assumptions"
            })
    
    # Age bias
    age_bias_terms = [
        "at your age", "young people these days", "when you're older",
        "too old for", "too young to understand"
    ]
    
    for term in age_bias_terms:
        if term in text_lower:
            analysis_result["bias_indicators"].append({
                "type": "age_bias",
                "term": term,
                "description": "Contains age-related assumptions"
            })
    
    # Economic bias
    economic_assumptions = [
        "just buy", "simply afford", "everyone has", "normal family",
        "standard lifestyle", "basic necessities"
    ]
    
    for assumption in economic_assumptions:
        if assumption in text_lower:
            analysis_result["bias_indicators"].append({
                "type": "economic_bias",
                "phrase": assumption,
                "description": "Makes economic privilege assumptions"
            })
    
    # =============================================================================
    # POSITIVE INDICATORS (Good practices)
    # =============================================================================
    
    positive_language = [
        "i understand", "that sounds difficult", "you're not alone",
        "it's okay to feel", "your feelings are valid", "let's explore",
        "what do you think", "how does that feel", "you decide"
    ]
    
    positive_count = sum(1 for phrase in positive_language if phrase in text_lower)
    
    # =============================================================================
    # CALCULATE SEVERITY AND RECOMMENDATIONS
    # =============================================================================
    
    total_flags = len(analysis_result["ethical_flags"]) + len(analysis_result["bias_indicators"])
    
    # Determine severity level
    if total_flags == 0:
        analysis_result["severity_level"] = "low"
        analysis_result["confidence_score"] = 0.9 if positive_count > 2 else 0.7
    elif total_flags <= 2:
        analysis_result["severity_level"] = "medium"
        analysis_result["confidence_score"] = 0.6
        analysis_result["approval_status"] = "needs_review"
    else:
        analysis_result["severity_level"] = "high"
        analysis_result["confidence_score"] = 0.8
        analysis_result["approval_status"] = "rejected"
    
    # Generate recommendations
    if analysis_result["ethical_flags"]:
        analysis_result["recommendations"].append(
            "Review response for ethical guidelines compliance"
        )
        analysis_result["recommendations"].append(
            "Ensure client-centered, non-judgmental language"
        )
    
    if analysis_result["bias_indicators"]:
        analysis_result["recommendations"].append(
            "Remove cultural, gender, or demographic assumptions"
        )
        analysis_result["recommendations"].append(
            "Use inclusive, neutral language"
        )
    
    if positive_count < 2:
        analysis_result["recommendations"].append(
            "Include more empathetic and validating language"
        )
    
    # Add summary
    analysis_result["summary"] = f"""
    Ethical Analysis Complete:
    - Ethical Flags: {len(analysis_result["ethical_flags"])}
    - Bias Indicators: {len(analysis_result["bias_indicators"])}
    - Severity: {analysis_result["severity_level"].upper()}
    - Status: {analysis_result["approval_status"].upper()}
    - Positive Language Score: {positive_count}/10
    """
    
    return analysis_result


# =============================================================================
# EXAMPLE USAGE AND TESTING
# =============================================================================

if __name__ == "__main__":
    # Test with different scenarios
    
    # Good example
    good_response = """
    I understand that you're feeling overwhelmed right now, and that's completely valid. 
    It sounds like you're going through a difficult time. Let's explore what specific 
    thoughts are contributing to these feelings. What do you think might be helpful 
    for you right now?
    """
    
    # Problematic example
    bad_response = """
    You just need to think positive and get over it. Everyone has problems, and others 
    have it worse than you. You're probably just overreacting. At your age, you should 
    know better. Just buy some self-help books and snap out of it.
    """
    
    print("=== TESTING GOOD RESPONSE ===")
    result1 = ethical_guardian_bias_auditor.invoke(good_response)
    print(f"Status: {result1['approval_status']}")
    print(f"Severity: {result1['severity_level']}")
    print(f"Summary: {result1['summary']}")
    
    print("\n=== TESTING PROBLEMATIC RESPONSE ===")
    result2 = ethical_guardian_bias_auditor(bad_response)
    print(f"Status: {result2['approval_status']}")
    print(f"Severity: {result2['severity_level']}")
    print(f"Ethical Flags: {len(result2['ethical_flags'])}")
    print(f"Bias Indicators: {len(result2['bias_indicators'])}")
    print(f"Summary: {result2['summary']}")