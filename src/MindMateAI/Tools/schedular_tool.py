from langchain_core.tools import tool
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import re
import json

@tool
def resource_scheduler(cbt_agent_output: str, client_timezone: str = "UTC") -> Dict[str, Any]:
    """
    Analyzes CBT agent output to recommend appropriate therapy schedules and resources.
    
    Args:
        cbt_agent_output (str): The output text from the CBT guide agent
        client_timezone (str): Client's timezone (default: UTC)
        
    Returns:
        Dict containing scheduling recommendations, resources, and follow-up plans
    """
    
    # Initialize scheduling result
    schedule_result = {
        "timestamp": datetime.now().isoformat(),
        "analysis_summary": {},
        "recommended_schedule": {},
        "resources": [],
        "follow_up_plan": {},
        "urgency_level": "standard",  # low, standard, high, crisis
        "session_recommendations": {},
        "homework_assignments": [],
        "next_steps": []
    }
    
    text_lower = cbt_agent_output.lower()
    
    # =============================================================================
    # ANALYZE CONTENT FOR SCHEDULING NEEDS
    # =============================================================================
    
    # Detect emotional intensity and urgency
    high_urgency_indicators = [
        "crisis", "emergency", "suicide", "self-harm", "can't cope",
        "breaking down", "desperate", "can't go on"
    ]
    
    medium_urgency_indicators = [
        "panic attack", "severe anxiety", "depressed", "overwhelmed",
        "can't sleep", "not eating", "isolated", "hopeless"
    ]
    
    urgency_score = 0
    detected_issues = []
    
    for indicator in high_urgency_indicators:
        if indicator in text_lower:
            urgency_score += 3
            detected_issues.append(f"High urgency: {indicator}")
    
    for indicator in medium_urgency_indicators:
        if indicator in text_lower:
            urgency_score += 1
            detected_issues.append(f"Medium urgency: {indicator}")
    
    # Determine urgency level
    if urgency_score >= 3:
        schedule_result["urgency_level"] = "crisis"
    elif urgency_score >= 2:
        schedule_result["urgency_level"] = "high"
    elif urgency_score >= 1:
        schedule_result["urgency_level"] = "standard"
    else:
        schedule_result["urgency_level"] = "low"
    
    schedule_result["analysis_summary"] = {
        "urgency_score": urgency_score,
        "detected_issues": detected_issues,
        "content_length": len(cbt_agent_output),
        "complexity_indicators": []
    }
    
    # =============================================================================
    # DETECT THERAPY TECHNIQUES MENTIONED
    # =============================================================================
    
    therapy_techniques = {
        "cognitive_restructuring": ["thought record", "cognitive distortion", "thinking pattern", "challenge thoughts"],
        "behavioral_activation": ["activity", "behavior", "routine", "schedule activities"],
        "exposure_therapy": ["exposure", "gradual", "face fears", "avoid"],
        "mindfulness": ["mindfulness", "meditation", "breathing", "present moment"],
        "relaxation": ["relaxation", "stress relief", "calm", "tension"],
        "problem_solving": ["problem solving", "solutions", "plan", "steps"]
    }
    
    detected_techniques = []
    for technique, keywords in therapy_techniques.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_techniques.append(technique)
                break
    
    # =============================================================================
    # GENERATE SCHEDULING RECOMMENDATIONS
    # =============================================================================
    
    def get_schedule_recommendation(urgency: str, techniques: List[str]) -> Dict[str, Any]:
        """Generate schedule based on urgency and techniques needed"""
        
        base_schedule = {
            "crisis": {
                "immediate_action": "Contact emergency services or crisis hotline",
                "first_session": "Within 24 hours",
                "session_frequency": "2-3 times per week initially",
                "session_duration": "50-60 minutes",
                "follow_up": "Daily check-ins for first week"
            },
            "high": {
                "first_session": "Within 2-3 days",
                "session_frequency": "2 times per week",
                "session_duration": "50 minutes",
                "follow_up": "Weekly for first month"
            },
            "standard": {
                "first_session": "Within 1 week",
                "session_frequency": "1 time per week",
                "session_duration": "45-50 minutes",
                "follow_up": "Bi-weekly after 6 sessions"
            },
            "low": {
                "first_session": "Within 2 weeks",
                "session_frequency": "Bi-weekly or monthly",
                "session_duration": "45 minutes",
                "follow_up": "Monthly maintenance"
            }
        }
        
        schedule = base_schedule.get(urgency, base_schedule["standard"]).copy()
        
        # Adjust based on techniques
        if "exposure_therapy" in techniques:
            schedule["special_note"] = "Extended sessions may be needed for exposure work"
            schedule["session_duration"] = "60-90 minutes"
        
        if len(techniques) > 3:
            schedule["treatment_duration"] = "12-20 sessions (longer due to complexity)"
        else:
            schedule["treatment_duration"] = "8-12 sessions"
        
        return schedule
    
    schedule_result["recommended_schedule"] = get_schedule_recommendation(
        schedule_result["urgency_level"], 
        detected_techniques
    )
    
    # =============================================================================
    # RESOURCE RECOMMENDATIONS
    # =============================================================================
    
    def generate_resources(urgency: str, techniques: List[str], issues: List[str]) -> List[Dict[str, str]]:
        """Generate appropriate resources based on analysis"""
        
        resources = []
        
        # Crisis resources
        if urgency == "crisis":
            resources.extend([
                {
                    "type": "crisis_hotline",
                    "name": "National Suicide Prevention Lifeline",
                    "contact": "988 or 1-800-273-8255",
                    "availability": "24/7"
                },
                {
                    "type": "emergency",
                    "name": "Emergency Services",
                    "contact": "911",
                    "note": "For immediate danger"
                }
            ])
        
        # Technique-specific resources
        if "mindfulness" in techniques:
            resources.append({
                "type": "app",
                "name": "Mindfulness Apps",
                "options": "Headspace, Calm, Insight Timer",
                "purpose": "Daily mindfulness practice"
            })
        
        if "cognitive_restructuring" in techniques:
            resources.append({
                "type": "worksheet",
                "name": "Thought Record Sheets",
                "purpose": "Track and challenge negative thoughts",
                "frequency": "Daily use recommended"
            })
        
        if "behavioral_activation" in techniques:
            resources.append({
                "type": "tool",
                "name": "Activity Scheduling Worksheet",
                "purpose": "Plan pleasant and meaningful activities",
                "frequency": "Weekly planning"
            })
        
        # General resources
        resources.extend([
            {
                "type": "book",
                "name": "Mind Over Mood",
                "authors": "Greenberger & Padesky",
                "purpose": "CBT self-help workbook"
            },
            {
                "type": "website",
                "name": "MindTools CBT Resources",
                "url": "www.mindtools.com",
                "purpose": "Additional CBT techniques and exercises"
            }
        ])
        
        return resources
    
    schedule_result["resources"] = generate_resources(
        schedule_result["urgency_level"],
        detected_techniques,
        detected_issues
    )
    
    # =============================================================================
    # SESSION RECOMMENDATIONS
    # =============================================================================
    
    schedule_result["session_recommendations"] = {
        "primary_focus_areas": detected_techniques[:3],  # Top 3 techniques
        "session_structure": {
            "check_in": "5 minutes - Review week and homework",
            "main_work": "30-35 minutes - CBT techniques and exercises",
            "wrap_up": "10 minutes - Summary and homework assignment"
        },
        "therapist_notes": [
            f"Client urgency level: {schedule_result['urgency_level']}",
            f"Detected issues: {', '.join([issue.split(': ')[1] for issue in detected_issues[:3]])}",
            "Monitor progress weekly and adjust frequency as needed"
        ]
    }
    
    # =============================================================================
    # HOMEWORK ASSIGNMENTS
    # =============================================================================
    
    def generate_homework(techniques: List[str], urgency: str) -> List[Dict[str, str]]:
        """Generate appropriate homework based on techniques and urgency"""
        
        homework = []
        
        if urgency in ["crisis", "high"]:
            homework.append({
                "assignment": "Daily Safety Check-in",
                "description": "Rate mood and safety level daily (1-10 scale)",
                "frequency": "Daily",
                "duration": "5 minutes"
            })
        
        if "cognitive_restructuring" in techniques:
            homework.append({
                "assignment": "Thought Record",
                "description": "Complete thought record when experiencing strong emotions",
                "frequency": "As needed, minimum 3 times per week",
                "duration": "10-15 minutes"
            })
        
        if "behavioral_activation" in techniques:
            homework.append({
                "assignment": "Activity Scheduling",
                "description": "Plan and engage in 2-3 pleasant activities",
                "frequency": "Weekly planning, daily execution",
                "duration": "15 minutes planning, varies for activities"
            })
        
        if "mindfulness" in techniques:
            homework.append({
                "assignment": "Daily Mindfulness Practice",
                "description": "Practice mindfulness meditation or breathing exercises",
                "frequency": "Daily",
                "duration": "10-20 minutes"
            })
        
        # Always include mood monitoring
        homework.append({
            "assignment": "Mood Monitoring",
            "description": "Track daily mood, energy, and sleep",
            "frequency": "Daily",
            "duration": "2-3 minutes"
        })
        
        return homework
    
    schedule_result["homework_assignments"] = generate_homework(detected_techniques, schedule_result["urgency_level"])
    
    # =============================================================================
    # FOLLOW-UP PLAN
    # =============================================================================
    
    schedule_result["follow_up_plan"] = {
        "initial_phase": {
            "duration": "First 4 weeks",
            "frequency": schedule_result["recommended_schedule"]["session_frequency"],
            "goals": ["Establish therapeutic relationship", "Begin symptom stabilization", "Introduce core CBT concepts"]
        },
        "working_phase": {
            "duration": "Weeks 5-12",
            "frequency": "Weekly or bi-weekly based on progress",
            "goals": ["Apply CBT techniques", "Practice skills", "Process challenges"]
        },
        "maintenance_phase": {
            "duration": "Weeks 13+",
            "frequency": "Monthly or as needed",
            "goals": ["Maintain progress", "Prevent relapse", "Independent skill use"]
        },
        "progress_indicators": [
            "Improved mood ratings",
            "Reduced symptom frequency",
            "Increased activity engagement",
            "Better coping skills usage"
        ]
    }
    
    # =============================================================================
    # NEXT STEPS
    # =============================================================================
    
    if schedule_result["urgency_level"] == "crisis":
        schedule_result["next_steps"] = [
            "Immediate safety assessment required",
            "Contact emergency services if in immediate danger",
            "Schedule crisis intervention session within 24 hours",
            "Establish safety plan with client"
        ]
    elif schedule_result["urgency_level"] == "high":
        schedule_result["next_steps"] = [
            "Schedule initial session within 2-3 days",
            "Conduct comprehensive assessment",
            "Begin symptom stabilization techniques",
            "Establish regular session schedule"
        ]
    else:
        schedule_result["next_steps"] = [
            "Schedule initial intake session",
            "Complete comprehensive assessment",
            "Develop treatment plan collaboratively",
            "Begin CBT psychoeducation"
        ]
    
    return schedule_result