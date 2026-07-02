import google.generativeai as genai
from config.constants import GEMINI_API_KEY, AI_MODEL, AI_TEMPERATURE, SYSTEM_PROMPT, MARK_SCHEME_KEYWORDS
import re

class AITutor:
    """AI Tutor powered by Gemini 1.5 Flash with Socratic method"""
    
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(AI_MODEL)
        self.chat_history = []
    
    def build_socratic_prompt(self, user_message: str, subject: str, previous_context: str = "") -> str:
        """Build a Socratic method prompt that guides rather than tells"""
        
        socratic_instruction = f"""
You are an IGCSE {subject} tutor using the Socratic method. Your role is to:

1. GUIDE, DON'T TELL: Ask guiding questions that lead students to discover answers
2. VALIDATE MARK SCHEME: Check if the student's answer contains these key terms and concepts:
   {', '.join(MARK_SCHEME_KEYWORDS.get(subject, [])[:10])}
3. IDENTIFY GAPS: Point out missing keywords without directly giving answers
4. ENCOURAGE THINKING: Ask "Why do you think that?", "Can you explain further?", "What happens if...?"
5. VERIFY UNDERSTANDING: Use follow-up questions to ensure deeper comprehension

Current context:
{previous_context}

Student's message: {user_message}

Respond in a warm, encouraging tone. Use the Socratic method - ask probing questions rather than providing direct answers.
Start with an acknowledgment of their effort, then ask a guiding question.
If they're missing key Mark Scheme terms, gently prompt them to think about those concepts.
"""
        return socratic_instruction
    
    def extract_keywords_from_response(self, response: str, subject: str) -> list:
        """Extract Mark Scheme keywords found in the response"""
        keywords = MARK_SCHEME_KEYWORDS.get(subject, [])
        found_keywords = []
        
        for keyword in keywords:
            if keyword.lower() in response.lower():
                found_keywords.append(keyword)
        
        return found_keywords
    
    def identify_missing_keywords(self, response: str, subject: str) -> list:
        """Identify missing important keywords from Mark Scheme"""
        found = self.extract_keywords_from_response(response, subject)
        all_keywords = MARK_SCHEME_KEYWORDS.get(subject, [])
        missing = [kw for kw in all_keywords[:10] if kw not in found]
        return missing
    
    def generate_response(self, user_message: str, subject: str, document_context: str = "") -> dict:
        """Generate AI tutor response using Socratic method"""
        
        try:
            # Build context-aware prompt
            previous_context = ""
            if self.chat_history:
                previous_context = f"Previous discussion: {self.chat_history[-1]['response'][:200]}..."
            
            socratic_prompt = self.build_socratic_prompt(
                user_message, 
                subject, 
                previous_context
            )
            
            # Add document context if available
            if document_context:
                socratic_prompt += f"\n\nStudent's uploaded document context:\n{document_context[:500]}"
            
            # Generate response from Gemini
            response = self.model.generate_content(
                socratic_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=AI_TEMPERATURE,
                    max_output_tokens=1024,
                )
            )
            
            ai_response = response.text
            
            # Analyze response for Mark Scheme keywords
            found_keywords = self.extract_keywords_from_response(user_message, subject)
            missing_keywords = self.identify_missing_keywords(user_message, subject)
            
            # Store in history
            self.chat_history.append({
                "user": user_message,
                "response": ai_response,
                "subject": subject,
                "found_keywords": found_keywords,
                "missing_keywords": missing_keywords
            })
            
            return {
                "success": True,
                "response": ai_response,
                "found_keywords": found_keywords,
                "missing_keywords": missing_keywords,
                "keyword_analysis": self._format_keyword_analysis(found_keywords, missing_keywords)
            }
        
        except Exception as e:
            return {
                "success": False,
                "response": f"Error generating response: {str(e)}",
                "error": str(e)
            }
    
    def _format_keyword_analysis(self, found: list, missing: list) -> str:
        """Format keyword analysis for display"""
        analysis = ""
        
        if found:
            analysis += f"✅ **Mark Scheme Keywords Found:** {', '.join(found)}\n\n"
        
        if missing:
            analysis += f"💡 **Consider exploring:** {', '.join(missing[:5])}\n"
            analysis += "These are important concepts in this topic!"
        
        return analysis
    
    def clear_history(self):
        """Clear chat history for new conversation"""
        self.chat_history = []
    
    def get_chat_history(self) -> list:
        """Get current chat history"""
        return self.chat_history
