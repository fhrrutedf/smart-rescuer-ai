"""
Medical Chatbot using local LLM
Provides medical consultation for non-emergency cases
"""
from typing import Dict, Any, List, Optional
import json
from utils import log, config

# Try to import ollama
try:
    import ollama
    HAS_OLLAMA = True
except ImportError:
    HAS_OLLAMA = False
    log.warning("Ollama not available - Chatbot will use rule-based responses")


class MedicalChatbot:
    """Local AI-powered medical chatbot"""
    
    def __init__(self, model_name: str = None):
        """
        Initialize chatbot
        
        Args:
            model_name: Name of Ollama model to use
        """
        self.model_name = model_name or config.CHATBOT_MODEL_NAME
        self.conversation_history: List[Dict[str, str]] = []
        self.is_available = HAS_OLLAMA
        
        if self.is_available:
            self._check_model_availability()
        
        log.info(f"Medical chatbot initialized (model: {self.model_name}, available: {self.is_available})")
    
    def _check_model_availability(self):
        """Check if the model is available locally"""
        try:
            models = ollama.list()
            model_names = [m['name'] for m in models.get('models', [])]
            
            if self.model_name not in model_names:
                log.warning(f"Model {self.model_name} not found. Available models: {model_names}")
                self.is_available = False
        except Exception as e:
            log.error(f"Failed to check model availability: {e}")
            self.is_available = False
    
    def chat(self, user_message: str, reset_history: bool = False) -> Dict[str, Any]:
        """
        Send message to chatbot and get response
        
        Args:
            user_message: User's message/symptoms
            reset_history: Whether to reset conversation history
            
        Returns:
            Dictionary with response and metadata
        """
        if reset_history:
            self.conversation_history = []
        
        try:
            if self.is_available:
                response = self._chat_with_ollama(user_message)
            else:
                response = self._chat_rule_based(user_message)
            
            # Add to history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": response["message"]
            })
            
            return response
            
        except Exception as e:
            log.error(f"Chat failed: {e}")
            return {
                "message": "عذراً، حدث خطأ في النظام. يرجى المحاولة مرة أخرى.",
                "is_emergency": False,
                "error": str(e)
            }
    
    def _chat_with_ollama(self, user_message: str) -> Dict[str, Any]:
        """Chat using Ollama LLM"""
        try:
            # System prompt for medical context
            system_prompt = """أنت مساعد طبي ذكي. قدم نصائح طبية عامة بناءً على الأعراض.
            - كن واضحاً ومفيداً
            - إذا كانت الحالة طارئة، انصح بالاتصال بالطوارئ فوراً
            - لا تقدم تشخيصات نهائية
            - اقترح متى يجب زيارة الطبيب
            """
            
            # Build messages
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": user_message})
            
            # Call Ollama
            response = ollama.chat(
                model=self.model_name,
                messages=messages
            )
            
            bot_message = response['message']['content']
            
            # Detect if it's an emergency
            is_emergency = self._detect_emergency_keywords(user_message, bot_message)
            
            return {
                "message": bot_message,
                "is_emergency": is_emergency,
                "model": self.model_name
            }
            
        except Exception as e:
            log.error(f"Ollama chat failed: {e}")
            return self._chat_rule_based(user_message)
    
    def _chat_rule_based(self, user_message: str) -> Dict[str, Any]:
        """Fallback rule-based responses"""
        
        # Emergency keywords
        emergency_keywords = [
            "ألم في الصدر", "chest pain",
            "ضيق تنفس", "difficulty breathing",
            "نزيف", "bleeding",
            "فقدان وعي", "unconscious",
            "حادث", "accident"
        ]
        
        # Check for emergency
        is_emergency = any(keyword in user_message.lower() for keyword in emergency_keywords)
        
        if is_emergency:
            message = """⚠️ تحذير: هذه قد تكون حالة طارئة!

يُنصح بالاتصال بالطوارئ فوراً على الرقم 997 أو أقرب مستشفى.

في حالة ألم الصدر أو ضيق التنفس:
- اتصل بالطوارئ فوراً
- اجلس في وضع مريح
- لا تجهد نفسك
- انتظر المساعدة الطبية

في حالة النزيف:
- اضغط على الجرح بقطعة قماش نظيفة
- ارفع العضو المصاب إن أمكن
- لا تزل الضمادة إذا تشبعت بالدم، بل أضف فوقها"""
        else:
            message = """شكراً لاستخدام المنقذ الذكي.

للحصول على استشارة أفضل، يرجى:
1. وصف الأعراض بالتفصيل
2. ذكر مدة الأعراض
3. ذكر أي أدوية حالية

ملاحظة: هذا النظام لا يحل محل الاستشارة الطبية المباشرة."""
        
        return {
            "message": message,
            "is_emergency": is_emergency,
            "model": "rule-based"
        }
    
    def _detect_emergency_keywords(self, user_msg: str, bot_msg: str) -> bool:
        """Detect emergency from keywords"""
        emergency_indicators = [
            "طارئ", "emergency", "فوري", "immediate",
            "997", "إسعاف", "ambulance", "مستشفى", "hospital"
        ]
        
        combined = (user_msg + " " + bot_msg).lower()
        return any(indicator in combined for indicator in emergency_indicators)
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        log.info("Conversation history cleared")
