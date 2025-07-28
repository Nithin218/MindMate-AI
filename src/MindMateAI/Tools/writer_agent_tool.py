# This tool handles content creation, writing assistance, and document generation

from langchain_core.tools import tool
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from enum import Enum
import re
import json

class WritingStyle(Enum):
    FORMAL = "formal"
    CASUAL = "casual"
    ACADEMIC = "academic"
    CREATIVE = "creative"
    BUSINESS = "business"
    TECHNICAL = "technical"

class ContentType(Enum):
    EMAIL = "email"
    REPORT = "report"
    ESSAY = "essay"
    BLOG_POST = "blog_post"
    LETTER = "letter"
    SUMMARY = "summary"
    PROPOSAL = "proposal"
    ARTICLE = "article"
    SCRIPT = "script"
    POETRY = "poetry"
    STORY = "story"

class WriterAgent:
    def __init__(self):
        self.style_templates = {
            WritingStyle.FORMAL: {
                "tone": "professional, respectful, structured",
                "vocabulary": "sophisticated, precise",
                "sentence_structure": "complex, well-structured",
                "greeting": "Dear [Name]," if ContentType.EMAIL else "",
                "closing": "Sincerely," if ContentType.EMAIL else ""
            },
            WritingStyle.CASUAL: {
                "tone": "friendly, conversational, relaxed",
                "vocabulary": "everyday, accessible",
                "sentence_structure": "varied, natural flow",
                "greeting": "Hi [Name]!" if ContentType.EMAIL else "",
                "closing": "Best regards," if ContentType.EMAIL else ""
            },
            WritingStyle.ACADEMIC: {
                "tone": "objective, analytical, scholarly",
                "vocabulary": "technical, precise, discipline-specific",
                "sentence_structure": "complex, citation-ready",
                "greeting": "",
                "closing": ""
            },
            WritingStyle.CREATIVE: {
                "tone": "imaginative, expressive, engaging",
                "vocabulary": "vivid, descriptive, varied",
                "sentence_structure": "artistic, rhythmic, varied",
                "greeting": "",
                "closing": ""
            },
            WritingStyle.BUSINESS: {
                "tone": "professional, confident, results-oriented",
                "vocabulary": "industry-specific, clear, direct",
                "sentence_structure": "concise, action-oriented",
                "greeting": "Dear [Name]," if ContentType.EMAIL else "",
                "closing": "Best regards," if ContentType.EMAIL else ""
            },
            WritingStyle.TECHNICAL: {
                "tone": "precise, informative, methodical",
                "vocabulary": "technical, specific, accurate",
                "sentence_structure": "clear, logical, step-by-step",
                "greeting": "",
                "closing": ""
            }
        }
        
        self.content_structures = {
            ContentType.EMAIL: {
                "structure": ["greeting", "opening", "body", "closing", "signature"],
                "requirements": ["clear subject", "professional tone", "call to action"]
            },
            ContentType.REPORT: {
                "structure": ["executive_summary", "introduction", "methodology", "findings", "conclusions", "recommendations"],
                "requirements": ["data-driven", "objective analysis", "clear formatting"]
            },
            ContentType.ESSAY: {
                "structure": ["introduction", "thesis_statement", "body_paragraphs", "conclusion"],
                "requirements": ["clear argument", "supporting evidence", "logical flow"]
            },
            ContentType.BLOG_POST: {
                "structure": ["catchy_title", "hook", "introduction", "main_content", "conclusion", "call_to_action"],
                "requirements": ["engaging", "SEO-friendly", "scannable format"]
            },
            ContentType.LETTER: {
                "structure": ["date", "address", "greeting", "body", "closing", "signature"],
                "requirements": ["personal touch", "clear purpose", "appropriate tone"]
            },
            ContentType.SUMMARY: {
                "structure": ["key_points", "main_findings", "conclusions"],
                "requirements": ["concise", "accurate", "comprehensive"]
            },
            ContentType.PROPOSAL: {
                "structure": ["executive_summary", "problem_statement", "proposed_solution", "timeline", "budget", "conclusion"],
                "requirements": ["persuasive", "detailed", "professional"]
            },
            ContentType.ARTICLE: {
                "structure": ["headline", "lead", "body", "conclusion"],
                "requirements": ["informative", "well-researched", "engaging"]
            }
        }

    def create_content(self, content_type: ContentType, writing_style: WritingStyle, 
                      topic: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create content based on type, style, and requirements"""
        
        style_guide = self.style_templates[writing_style]
        structure_guide = self.content_structures[content_type]
        
        # Generate content outline
        outline = self._generate_outline(content_type, topic, requirements)
        
        # Create content sections
        content_sections = self._create_sections(outline, style_guide, requirements)
        
        # Format final content
        formatted_content = self._format_content(content_sections, content_type, style_guide)
        
        return {
            "content": formatted_content,
            "outline": outline,
            "word_count": len(formatted_content.split()),
            "style_applied": writing_style.value,
            "content_type": content_type.value,
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "topic": topic,
                "requirements_met": structure_guide["requirements"]
            }
        }

    def _generate_outline(self, content_type: ContentType, topic: str, requirements: Dict[str, Any]) -> List[str]:
        """Generate content outline based on type and topic"""
        structure = self.content_structures[content_type]["structure"]
        
        if content_type == ContentType.EMAIL:
            return [
                f"Subject: {requirements.get('subject', f'Regarding {topic}')}",
                "Greeting",
                f"Opening statement about {topic}",
                "Main content/request",
                "Closing and next steps",
                "Professional signature"
            ]
        elif content_type == ContentType.BLOG_POST:
            return [
                f"Title: {self._generate_title(topic, 'blog')}",
                f"Hook: Engaging opening about {topic}",
                f"Introduction to {topic}",
                f"Main points about {topic} (3-5 sections)",
                f"Practical examples or case studies",
                f"Conclusion and key takeaways",
                "Call to action"
            ]
        elif content_type == ContentType.REPORT:
            return [
                "Executive Summary",
                f"Introduction to {topic}",
                "Methodology/Approach",
                f"Key findings regarding {topic}",
                "Analysis and Discussion",
                "Conclusions",
                "Recommendations"
            ]
        else:
            # Generic outline based on structure
            return [section.replace("_", " ").title() for section in structure]

    def _create_sections(self, outline: List[str], style_guide: Dict[str, str], 
                        requirements: Dict[str, Any]) -> Dict[str, str]:
        """Create content for each section based on outline"""
        sections = {}
        
        for section in outline:
            section_key = section.lower().replace(" ", "_").replace(":", "")
            
            # Generate section content based on style guide
            if "title" in section.lower() or "subject" in section.lower():
                sections[section_key] = section
            elif "greeting" in section.lower():
                sections[section_key] = style_guide.get("greeting", "")
            elif "closing" in section.lower():
                sections[section_key] = style_guide.get("closing", "")
            else:
                sections[section_key] = f"[{section} - Content to be generated based on {style_guide['tone']} tone]"
        
        return sections

    def _format_content(self, sections: Dict[str, str], content_type: ContentType, 
                       style_guide: Dict[str, str]) -> str:
        """Format content sections into final document"""
        formatted_parts = []
        
        for section_name, content in sections.items():
            if content and content.strip():
                if content_type == ContentType.EMAIL:
                    formatted_parts.append(content)
                elif "title" in section_name or "subject" in section_name:
                    formatted_parts.append(f"{content}\n{'=' * len(content)}")
                else:
                    formatted_parts.append(f"{content}")
        
        return "\n\n".join(formatted_parts)

    def _generate_title(self, topic: str, content_type: str) -> str:
        """Generate appropriate titles based on content type"""
        topic_clean = topic.strip().title()
        
        title_templates = {
            "blog": [
                f"The Ultimate Guide to {topic_clean}",
                f"Everything You Need to Know About {topic_clean}",
                f"Mastering {topic_clean}: Tips and Strategies",
                f"The Complete {topic_clean} Handbook"
            ],
            "report": [
                f"{topic_clean} Analysis Report",
                f"Comprehensive Study on {topic_clean}",
                f"{topic_clean}: Research Findings and Insights"
            ],
            "article": [
                f"Understanding {topic_clean}",
                f"The Impact of {topic_clean}",
                f"Exploring {topic_clean}: Key Insights"
            ]
        }
        
        return title_templates.get(content_type, [f"About {topic_clean}"])[0]

    def improve_content(self, content: str, improvement_type: str) -> Dict[str, Any]:
        """Improve existing content based on specified criteria"""
        
        improvements = {
            "grammar": self._improve_grammar,
            "clarity": self._improve_clarity,
            "tone": self._adjust_tone,
            "structure": self._improve_structure,
            "engagement": self._improve_engagement,
            "conciseness": self._improve_conciseness
        }
        
        if improvement_type not in improvements:
            return {
                "error": f"Unknown improvement type: {improvement_type}",
                "available_types": list(improvements.keys())
            }
        
        improved_content = improvements[improvement_type](content)
        
        return {
            "original_content": content,
            "improved_content": improved_content,
            "improvement_type": improvement_type,
            "suggestions": self._generate_improvement_suggestions(content, improvement_type)
        }

    def _improve_grammar(self, content: str) -> str:
        """Basic grammar improvements"""
        # Simple grammar fixes
        content = re.sub(r'\s+', ' ', content)  # Fix multiple spaces
        content = re.sub(r'([.!?])\s*([a-z])', r'\1 \2', content)  # Space after punctuation
        return content.strip()

    def _improve_clarity(self, content: str) -> str:
        """Improve content clarity"""
        # Add suggestions for clarity improvements
        return content + "\n\n[Clarity improvements: Consider breaking long sentences, using active voice, and defining technical terms]"

    def _adjust_tone(self, content: str) -> str:
        """Adjust content tone"""
        return content + "\n\n[Tone adjustment: Consider the target audience and adjust formality level accordingly]"

    def _improve_structure(self, content: str) -> str:
        """Improve content structure"""
        return content + "\n\n[Structure improvements: Consider adding headers, bullet points, and logical flow between sections]"

    def _improve_engagement(self, content: str) -> str:
        """Improve content engagement"""
        return content + "\n\n[Engagement improvements: Add questions, examples, and interactive elements]"

    def _improve_conciseness(self, content: str) -> str:
        """Improve content conciseness"""
        return content + "\n\n[Conciseness improvements: Remove redundant phrases and combine related sentences]"

    def _generate_improvement_suggestions(self, content: str, improvement_type: str) -> List[str]:
        """Generate specific improvement suggestions"""
        
        suggestions_map = {
            "grammar": [
                "Check for subject-verb agreement",
                "Review punctuation usage",
                "Verify proper tense consistency",
                "Look for run-on sentences"
            ],
            "clarity": [
                "Use simpler vocabulary where possible",
                "Break up complex sentences",
                "Add transitions between ideas",
                "Define technical terms"
            ],
            "tone": [
                "Adjust formality level for audience",
                "Maintain consistent voice throughout",
                "Consider emotional impact of word choices",
                "Balance professional and approachable language"
            ],
            "structure": [
                "Use clear headings and subheadings",
                "Organize information logically",
                "Add bullet points for lists",
                "Include topic sentences for paragraphs"
            ],
            "engagement": [
                "Add relevant examples",
                "Include rhetorical questions",
                "Use storytelling elements",
                "Incorporate reader interaction"
            ],
            "conciseness": [
                "Remove unnecessary words",
                "Combine related sentences",
                "Eliminate redundant information",
                "Use active voice instead of passive"
            ]
        }
        
        return suggestions_map.get(improvement_type, ["General improvement suggestions"])

    def analyze_content(self, content: str) -> Dict[str, Any]:
        """Analyze content for various metrics"""
        
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        paragraphs = content.split('\n\n')
        
        # Basic readability metrics
        avg_words_per_sentence = len(words) / max(len(sentences), 1)
        avg_sentences_per_paragraph = len(sentences) / max(len(paragraphs), 1)
        
        # Word frequency analysis
        word_freq = {}
        for word in words:
            clean_word = re.sub(r'[^\w]', '', word.lower())
            if clean_word and len(clean_word) > 2:
                word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
        
        most_common_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "word_count": len(words),
            "sentence_count": len([s for s in sentences if s.strip()]),
            "paragraph_count": len([p for p in paragraphs if p.strip()]),
            "avg_words_per_sentence": round(avg_words_per_sentence, 2),
            "avg_sentences_per_paragraph": round(avg_sentences_per_paragraph, 2),
            "most_common_words": most_common_words,
            "readability_score": self._calculate_readability_score(content),
            "sentiment_indicators": self._analyze_sentiment_indicators(content)
        }

    def _calculate_readability_score(self, content: str) -> str:
        """Simple readability assessment"""
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        
        if len(sentences) == 0:
            return "Unable to calculate"
        
        avg_sentence_length = len(words) / len(sentences)
        
        if avg_sentence_length < 15:
            return "Easy to read"
        elif avg_sentence_length < 20:
            return "Moderately easy to read"
        elif avg_sentence_length < 25:
            return "Moderately difficult to read"
        else:
            return "Difficult to read"

    def _analyze_sentiment_indicators(self, content: str) -> Dict[str, int]:
        """Basic sentiment analysis"""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'positive', 'success', 'achieve', 'benefit']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'negative', 'problem', 'issue', 'difficulty', 'challenge', 'failure']
        
        content_lower = content.lower()
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        
        return {
            "positive_indicators": positive_count,
            "negative_indicators": negative_count,
            "neutral_ratio": max(0, len(content.split()) - positive_count - negative_count) / len(content.split())
        }

# Initialize the writer agent
writer_agent_instance = WriterAgent()

@tool
def writer_agent_tool(
    action: str,
    content_type: str = "general",
    writing_style: str = "casual",
    topic: str = "",
    content: str = "",
    requirements: Optional[Dict[str, Any]] = None,
    improvement_type: str = "clarity"
) -> Dict[str, Any]:
    """
    Writer Agent Tool for content creation, writing assistance, and document generation.
    
    Args:
        action (str): The action to perform. Options:
            - "create": Create new content
            - "improve": Improve existing content
            - "analyze": Analyze content metrics
            - "get_templates": Get available templates
            - "get_styles": Get available writing styles
            
        content_type (str): Type of content to create. Options:
            - "email", "report", "essay", "blog_post", "letter", 
            - "summary", "proposal", "article", "script", "poetry", "story"
            
        writing_style (str): Writing style to apply. Options:
            - "formal", "casual", "academic", "creative", "business", "technical"
            
        topic (str): Main topic or subject for content creation
        
        content (str): Existing content for improvement or analysis
        
        requirements (Dict): Additional requirements like:
            - "length": target word count
            - "audience": target audience
            - "purpose": content purpose
            - "deadline": content deadline
            - "keywords": SEO keywords (for blog posts)
            - "subject": email subject line
            
        improvement_type (str): Type of improvement for "improve" action:
            - "grammar", "clarity", "tone", "structure", "engagement", "conciseness"
    
    Returns:
        Dict containing the results of the requested action
    """
    
    if requirements is None:
        requirements = {}
    
    try:
        # Validate enums
        if action == "create":
            try:
                content_type_enum = ContentType(content_type.lower())
                writing_style_enum = WritingStyle(writing_style.lower())
            except ValueError as e:
                return {
                    "error": f"Invalid parameter: {str(e)}",
                    "valid_content_types": [ct.value for ct in ContentType],
                    "valid_writing_styles": [ws.value for ws in WritingStyle]
                }
            
            if not topic:
                return {"error": "Topic is required for content creation"}
            
            return writer_agent_instance.create_content(
                content_type_enum, writing_style_enum, topic, requirements
            )
        
        elif action == "improve":
            if not content:
                return {"error": "Content is required for improvement"}
            
            return writer_agent_instance.improve_content(content, improvement_type)
        
        elif action == "analyze":
            if not content:
                return {"error": "Content is required for analysis"}
            
            return writer_agent_instance.analyze_content(content)
        
        elif action == "get_templates":
            return {
                "content_types": {ct.value: writer_agent_instance.content_structures[ct] for ct in ContentType},
                "description": "Available content types and their structures"
            }
        
        elif action == "get_styles":
            return {
                "writing_styles": {ws.value: writer_agent_instance.style_templates[ws] for ws in WritingStyle},
                "description": "Available writing styles and their characteristics"
            }
        
        else:
            return {
                "error": f"Unknown action: {action}",
                "valid_actions": ["create", "improve", "analyze", "get_templates", "get_styles"]
            }
    
    except Exception as e:
        return {
            "error": f"An error occurred: {str(e)}",
            "action": action,
            "timestamp": datetime.now().isoformat()
        }