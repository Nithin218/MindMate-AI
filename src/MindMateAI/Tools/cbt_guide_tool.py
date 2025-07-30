# This tool analyzes text for emotional content and sentiment

from langchain_core.tools import tool


class CBTGuideTool:
    """Cognitive Behavioral Therapy (CBT) Guide Tool for providing CBT techniques and strategies."""
    
    def __init__(self):
        self.cbt_guide_tool = self._setup_tool()

    def _setup_tool(self):
        """Sets up the CBT guide tool."""
        @tool
        def cbt_therapy_tool(emotion: str) -> str:
            """
            Generates CBT-based therapeutic responses based on the identified emotion.
            
            Args:
                emotion_data (str): JSON string containing emotion analysis results
                
            Returns:
                str: CBT-based therapeutic response
            """
            
            # CBT response templates based on emotion
            cbt_responses = {
                'anxiety': """
                I understand you're experiencing anxiety. Let's work through this together using CBT techniques:
                
                1. **Thought Identification**: What specific thoughts are contributing to your anxiety?
                2. **Reality Testing**: Are these thoughts based on facts or assumptions?
                3. **Breathing Exercise**: Try the 4-7-8 technique - inhale for 4, hold for 7, exhale for 8.
                4. **Grounding**: Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste.
                
                Remember: Anxiety often comes from worrying about future events. Focus on what you can control right now.
                """,
                
                'depression': """
                I hear that you're going through a difficult time. Depression can feel overwhelming, but CBT can help:
                
                1. **Thought Challenging**: Notice negative self-talk and ask "Is this thought helpful or accurate?"
                2. **Behavioral Activation**: Start with small, achievable activities that used to bring you joy.
                3. **Daily Structure**: Create a simple routine to provide stability and purpose.
                4. **Self-Compassion**: Treat yourself with the same kindness you'd show a good friend.
                
                Small steps forward are still progress. You don't have to face this alone.
                """,
                
                'anger': """
                Anger can be a valid emotion, and we can work on managing it constructively:
                
                1. **Pause and Breathe**: Before reacting, take 5 deep breaths to create space.
                2. **Identify Triggers**: What specifically triggered this anger? Is there an underlying need?
                3. **Thought Reframing**: Ask "Is there another way to view this situation?"
                4. **Physical Release**: Consider exercise, journaling, or other healthy outlets.
                
                Anger often masks other emotions like hurt or fear. Let's explore what's underneath.
                """,
                
                'stress': """
                Stress is your body's natural response to challenges. Here's how to manage it:
                
                1. **Priority Setting**: List your stressors and identify which ones you can control.
                2. **Time Management**: Break large tasks into smaller, manageable steps.
                3. **Relaxation Techniques**: Practice progressive muscle relaxation or mindfulness.
                4. **Boundary Setting**: It's okay to say no to additional commitments.
                
                Remember: You're stronger than you realize, and this feeling is temporary.
                """,
                
                'grief': """
                Grief is a natural response to loss, and everyone processes it differently:
                
                1. **Allow Your Feelings**: There's no "right" way to grieve. Your emotions are valid.
                2. **Honor Memories**: Consider ways to celebrate and remember what you've lost.
                3. **Seek Support**: Connect with others who understand your experience.
                4. **Self-Care**: Maintain basic needs - eating, sleeping, and gentle movement.
                
                Healing isn't about "getting over" loss, but learning to carry it with love.
                """,
                
                'loneliness': """
                Loneliness can feel isolating, but you're taking a positive step by reaching out:
                
                1. **Connection Building**: Start small - a text to an old friend or a smile to a neighbor.
                2. **Community Involvement**: Consider volunteering or joining groups with shared interests.
                3. **Self-Relationship**: Practice enjoying your own company through hobbies or self-care.
                4. **Quality over Quantity**: Focus on meaningful connections rather than many superficial ones.
                
                Remember: Feeling lonely doesn't mean you're alone. Help and connection are available.
                """,
                
                'neutral': """
                It's wonderful that you're checking in with your mental health:
                
                1. **Mindful Awareness**: Regular self-reflection helps maintain emotional balance.
                2. **Preventive Care**: Continue practices that support your wellbeing.
                3. **Growth Mindset**: Consider areas where you'd like to develop or improve.
                4. **Gratitude Practice**: Reflect on positive aspects of your current situation.
                
                Maintaining mental health is an ongoing journey, and you're taking positive steps.
                """
            }
            
            response = cbt_responses.get(emotion, cbt_responses['neutral'])
            
            return response

        return emotion_analysis_tool

    