# This tool analyzes text for emotional content and sentiment

from langchain_core.tools import tool
import json


class ResourceScheduleTool:
    """Resource Schedule Tool for managing therapy resource allocation."""
    
    def __init__(self):
        self.resource_schedule_tool = self._setup_tool()

    def _setup_tool(self):
        """Sets up the resource schedule tool."""
        @tool
        def resource_schedule_tool(cbt_response: str, emotion: str, confidence: float) -> str:
            """
            Analyzes the CBT response and generates recommended resources and scheduling.
            
            Args:
                cbt_response (str): The CBT therapeutic response
                emotion (str): The primary emotion identified
                confidence (float): Confidence level in emotion detection (0-1)
                
            Returns:
                str: JSON string containing recommended schedule and resources
            """
            
            # Determine schedule based on emotion intensity and type
            
            # Base schedule template
            schedule = {
                'immediate_actions': [],
                'daily_practices': [],
                'weekly_goals': [],
                'resources': [],
                'timeline': 'flexible',
                'check_in_frequency': 'weekly'
            }
            
            # Customize based on emotion type
            if emotion == 'anxiety':
                schedule.update({
                    'immediate_actions': [
                        'Practice 4-7-8 breathing exercise',
                        'Complete grounding technique (5-4-3-2-1)',
                        'Write down current worry triggers'
                    ],
                    'daily_practices': [
                        'Morning mindfulness (5-10 minutes)',
                        'Evening worry journal',
                        'Progressive muscle relaxation before bed'
                    ],
                    'weekly_goals': [
                        'Identify and challenge one negative thought pattern',
                        'Practice one new coping strategy',
                        'Engage in one anxiety-reducing activity'
                    ],
                    'resources': [
                        'Anxiety and Worry Workbook',
                        'Headspace or Calm app',
                        'Local anxiety support groups'
                    ],
                    'check_in_frequency': 'daily for first week, then weekly'
                })
            
            elif emotion == 'depression':
                schedule.update({
                    'immediate_actions': [
                        'Set one small, achievable goal for today',
                        'Reach out to one supportive person',
                        'Engage in 10 minutes of gentle movement'
                    ],
                    'daily_practices': [
                        'Morning routine establishment',
                        'Mood tracking',
                        'One enjoyable activity (however small)'
                    ],
                    'weekly_goals': [
                        'Increase one pleasant activity',
                        'Challenge one negative thought pattern',
                        'Maintain consistent sleep schedule'
                    ],
                    'resources': [
                        'Depression self-help workbooks',
                        'Mood tracking apps',
                        'Online support communities'
                    ],
                    'check_in_frequency': 'daily for first two weeks'
                })
            
            elif emotion in ['anger', 'stress']:
                schedule.update({
                    'immediate_actions': [
                        'Take 5 deep breaths',
                        'Step away from triggering situation if possible',
                        'Write down feelings without judgment'
                    ],
                    'daily_practices': [
                        'Stress check-ins (morning, afternoon, evening)',
                        'Physical exercise or movement',
                        'Relaxation technique practice'
                    ],
                    'weekly_goals': [
                        'Identify main stress/anger triggers',
                        'Practice one new coping strategy',
                        'Implement one stress-reduction change'
                    ],
                    'resources': [
                        'Stress management workshops',
                        'Exercise or yoga classes',
                        'Time management tools'
                    ]
                })
            
            # Adjust intensity based on confidence level
            if confidence > 0.7:  # High confidence in emotion detection
                schedule['timeline'] = 'structured - follow daily'
                schedule['check_in_frequency'] = 'daily for first week'
            else:
                schedule['timeline'] = 'flexible - adapt as needed'

            return json.dumps(schedule, indent=2)

        return resource_schedule_tool

    