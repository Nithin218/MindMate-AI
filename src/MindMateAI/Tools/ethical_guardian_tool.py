# This tool analyzes text for emotional content and sentiment

from langchain_core.tools import tool
import json


class EthicalGuardianTool:
    """Ethical Guardian Tool for ensuring user safety and ethical guidelines adherence."""
    
    def __init__(self):
        self.ethical_guardian_tool = self._setup_tool()

    def _setup_tool(self):
        """Sets up the ethical guardian tool."""
        @tool
        def ethical_guardian_tool(therapy_content: str) -> str:
            """
            Reviews therapy content for ethical concerns and bias.
            
            Args:
                therapy_content (str): The complete therapy response to review
                
            Returns:
                str: JSON string indicating if content is ethical and any concerns
            """
            
            # Ethical guidelines checklist
            ethical_concerns = []
            
            content_lower = therapy_content.lower()
            
            # Check for harmful content
            harmful_phrases = [
                'just get over it', 'it\'s all in your head', 'you\'re overreacting',
                'others have it worse', 'think positive', 'just be happy',
                'you should', 'you must', 'you need to'
            ]
            
            for phrase in harmful_phrases:
                if phrase in content_lower:
                    ethical_concerns.append(f"Contains potentially dismissive language: '{phrase}'")
            
            # Check for medical advice
            medical_terms = ['diagnose', 'medication', 'prescription', 'disorder', 'treatment plan']
            for term in medical_terms:
                if term in content_lower:
                    ethical_concerns.append(f"May contain inappropriate medical advice: '{term}'")
            
            # Check for professional boundary issues
            boundary_issues = ['i can cure', 'i guarantee', 'this will fix', 'you will be cured']
            for issue in boundary_issues:
                if issue in content_lower:
                    ethical_concerns.append(f"Contains inappropriate promises: '{issue}'")
            
            # Check for cultural sensitivity
            if len(ethical_concerns) == 0:
                # Additional positive checks
                positive_elements = [
                    'support' in content_lower,
                    'understand' in content_lower,
                    'together' in content_lower,
                    'your feelings' in content_lower
                ]
                
                if not any(positive_elements):
                    ethical_concerns.append("Content may lack empathetic language")
            
            is_ethical = len(ethical_concerns) == 0
            
            result = {
                'is_ethical': is_ethical,
                'concerns': ethical_concerns,
                'approval': 'approved' if is_ethical else 'needs_revision'
            }
            
            return json.dumps(result)

        return ethical_guardian_tool

    