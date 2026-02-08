import { useState, useRef, useEffect } from 'react';
import { apiService } from '../services/api';
import './Chat.css';

export default function Chat() {
    const [messages, setMessages] = useState([
        {
            role: 'assistant',
            content: 'مرحباً! أنا المساعد الطبي الذكي 🩺\n\nكيف يمكنني مساعدتك اليوم؟\n\nيمكنني:\n• الإجابة على استفساراتك الطبية العامة\n• تقديم نصائح للإسعافات الأولية\n• تحديد إذا كانت الحالة تحتاج طوارئ\n\n⚠️ تنبيه: لا أحل محل الاستشارة الطبية المباشرة'
        }
    ]);
    const [inputMessage, setInputMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!inputMessage.trim() || isLoading) return;

        const userMessage = inputMessage.trim();
        setInputMessage('');

        // Add user message
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setIsLoading(true);

        try {
            const response = await apiService.sendChatMessage(userMessage, false);

            // Add bot response
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: response.data.message,
                isEmergency: response.data.is_emergency,
                model: response.data.model
            }]);
        } catch (error) {
            console.error('Chat error:', error);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: 'عذراً، حدث خطأ في الاتصال. يرجى المحاولة مرة أخرى.',
                isError: true
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    const handleClearChat = async () => {
        try {
            await apiService.sendChatMessage('', true); // Reset history
            setMessages([{
                role: 'assistant',
                content: 'تم مسح المحادثة. كيف يمكنني مساعدتك؟'
            }]);
        } catch (error) {
            console.error('Clear chat error:', error);
        }
    };

    const quickQuestions = [
        { icon: '🤕', text: 'كيف أتعامل مع الصداع؟' },
        { icon: '🤒', text: 'لدي حمى، ماذا أفعل؟' },
        { icon: '🩹', text: 'كيف أعالج جرح صغير؟' },
        { icon: '🫀', text: 'ما أعراض النوبة القلبية؟' },
        { icon: '🤧', text: 'أعاني من أعراض البرد' },
        { icon: '💊', text: 'متى يجب زيارة الطبيب؟' }
    ];

    const handleQuickQuestion = (question) => {
        setInputMessage(question);
    };

    return (
        <div className="chat-container">
            <div className="chat-header">
                <div className="header-content">
                    <div className="header-left">
                        <div className="bot-avatar">🤖</div>
                        <div className="header-info">
                            <h1>المساعد الطبي الذكي</h1>
                            <p className="status">
                                <span className="status-dot"></span>
                                متصل الآن
                            </p>
                        </div>
                    </div>
                    <button className="clear-btn" onClick={handleClearChat}>
                        🗑️ مسح المحادثة
                    </button>
                </div>
            </div>

            <div className="quick-questions">
                <p className="quick-title">أسئلة شائعة:</p>
                <div className="quick-grid">
                    {quickQuestions.map((q, idx) => (
                        <button
                            key={idx}
                            className="quick-btn"
                            onClick={() => handleQuickQuestion(q.text)}
                        >
                            <span className="quick-icon">{q.icon}</span>
                            {q.text}
                        </button>
                    ))}
                </div>
            </div>

            <div className="messages-container">
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`message ${msg.role} ${msg.isEmergency ? 'emergency' : ''} ${msg.isError ? 'error' : ''}`}
                    >
                        <div className="message-avatar">
                            {msg.role === 'user' ? '👤' : '🤖'}
                        </div>
                        <div className="message-content">
                            {msg.isEmergency && (
                                <div className="emergency-badge">
                                    🚨 تحذير طوارئ
                                </div>
                            )}
                            <div className="message-text">
                                {msg.content.split('\n').map((line, i) => (
                                    <p key={i}>{line}</p>
                                ))}
                            </div>
                            {msg.model && (
                                <div className="message-meta">
                                    نموذج: {msg.model === 'rule-based' ? 'القواعد الأساسية' : msg.model}
                                </div>
                            )}
                        </div>
                    </div>
                ))}

                {isLoading && (
                    <div className="message assistant">
                        <div className="message-avatar">🤖</div>
                        <div className="message-content">
                            <div className="typing-indicator">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            <div className="input-container">
                <div className="input-wrapper">
                    <textarea
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="اكتب سؤالك الطبي هنا..."
                        rows="1"
                        disabled={isLoading}
                    />
                    <button
                        className="send-btn"
                        onClick={handleSend}
                        disabled={!inputMessage.trim() || isLoading}
                    >
                        {isLoading ? '⏳' : '📤'}
                    </button>
                </div>
                <div className="input-hint">
                    اضغط Enter للإرسال • Shift+Enter لسطر جديد
                </div>
            </div>

            <div className="chat-footer">
                <p>⚠️ هذا النظام يقدم نصائح عامة فقط ولا يحل محل الاستشارة الطبية</p>
                <p>في حالات الطوارئ اتصل: 997</p>
            </div>
        </div>
    );
}
