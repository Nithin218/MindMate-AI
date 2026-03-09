import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Loader2 } from 'lucide-react';
import MessageBubble from './MessageBubble';

const WELCOME_SUGGESTIONS = [
    "I've been feeling overwhelmed lately",
    "How can I manage anxiety better?",
    "I need help with stress relief",
    "Talk me through a tough day",
];

const ChatInterface = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e, overrideText) => {
        if (e) e.preventDefault();
        const text = overrideText ?? input;
        if (!text.trim() || isLoading) return;

        const userMessage = { role: 'user', content: text };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const payload = { question: text };
            const response = await axios.post('/query', payload);
            const aiMessage = { role: 'assistant', content: response.data.answer };
            setMessages(prev => [...prev, aiMessage]);
        } catch (error) {
            console.error('Error sending message:', error);
            const errorMessage = {
                role: 'assistant',
                content: 'I apologize, but I encountered an error connecting to the server. Please try again.',
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
            setTimeout(() => inputRef.current?.focus(), 100);
        }
    };

    const handleSuggestion = (text) => {
        handleSubmit(null, text);
    };

    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            height: '100vh',
            maxWidth: '800px',
            margin: '0 auto',
            padding: '0 20px',
        }}>

            {/* ── Header ─────────────────────────────────────── */}
            <header style={{
                padding: '28px 0 20px',
                textAlign: 'center',
                borderBottom: '1px solid var(--color-border)',
                marginBottom: '4px',
                flexShrink: 0,
            }}>
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '10px',
                    marginBottom: '6px',
                }}>
                    {/* Logo pill */}
                    <span style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        width: '38px',
                        height: '38px',
                        borderRadius: '50%',
                        background: 'linear-gradient(135deg, #7C6EE8 0%, #C084FC 100%)',
                        fontSize: '1.1rem',
                        flexShrink: 0,
                    }}>🧠</span>

                    <h1 style={{
                        fontFamily: 'var(--font-heading)',
                        fontSize: '1.75rem',
                        fontWeight: 700,
                        background: 'linear-gradient(90deg, #A78BFA 0%, #C084FC 100%)',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        backgroundClip: 'text',
                        letterSpacing: '-0.02em',
                        margin: 0,
                    }}>
                        MindMate AI
                    </h1>
                </div>

                <p style={{
                    fontFamily: 'var(--font-body)',
                    fontSize: '0.875rem',
                    fontWeight: 400,
                    color: 'var(--color-text-muted)',
                    letterSpacing: '0.01em',
                    margin: 0,
                }}>
                    Your personal mental health companion — always here to listen
                </p>
            </header>

            {/* ── Chat Area ──────────────────────────────────── */}
            <div style={{
                flex: 1,
                overflowY: 'auto',
                padding: '20px 0',
            }}>
                {messages.length === 0 ? (
                    /* Welcome State */
                    <div style={{
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        justifyContent: 'center',
                        height: '100%',
                        gap: '24px',
                        paddingBottom: '60px',
                    }}>
                        <div style={{ textAlign: 'center' }}>
                            <p style={{
                                fontFamily: 'var(--font-heading)',
                                fontSize: '1.25rem',
                                fontWeight: 600,
                                color: 'var(--color-text)',
                                marginBottom: '8px',
                            }}>
                                How are you feeling today?
                            </p>
                            <p style={{
                                fontFamily: 'var(--font-body)',
                                fontSize: '0.875rem',
                                color: 'var(--color-text-muted)',
                                fontWeight: 400,
                            }}>
                                Share what's on your mind — I'm here to help.
                            </p>
                        </div>

                        {/* Suggestion chips */}
                        <div style={{
                            display: 'flex',
                            flexWrap: 'wrap',
                            gap: '10px',
                            justifyContent: 'center',
                            maxWidth: '560px',
                        }}>
                            {WELCOME_SUGGESTIONS.map((s, i) => (
                                <button
                                    key={i}
                                    onClick={() => handleSuggestion(s)}
                                    style={{
                                        fontFamily: 'var(--font-body)',
                                        fontSize: '0.8125rem',
                                        fontWeight: 500,
                                        color: 'var(--color-text-muted)',
                                        background: 'var(--color-surface)',
                                        border: '1px solid var(--color-border)',
                                        borderRadius: '999px',
                                        padding: '8px 16px',
                                        cursor: 'pointer',
                                        transition: 'all 0.18s ease',
                                        letterSpacing: '0.01em',
                                    }}
                                    onMouseEnter={e => {
                                        e.currentTarget.style.borderColor = 'var(--color-accent)';
                                        e.currentTarget.style.color = 'var(--color-text)';
                                        e.currentTarget.style.background = 'var(--color-surface-2)';
                                    }}
                                    onMouseLeave={e => {
                                        e.currentTarget.style.borderColor = 'var(--color-border)';
                                        e.currentTarget.style.color = 'var(--color-text-muted)';
                                        e.currentTarget.style.background = 'var(--color-surface)';
                                    }}
                                >
                                    {s}
                                </button>
                            ))}
                        </div>
                    </div>
                ) : (
                    <div>
                        {messages.map((msg, index) => (
                            <MessageBubble key={index} message={msg} />
                        ))}
                        {isLoading && (
                            <div style={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: '8px',
                                padding: '12px 16px',
                                color: 'var(--color-text-muted)',
                            }}>
                                <Loader2 size={15} style={{ animation: 'spin 1s linear infinite' }} />
                                <span style={{
                                    fontFamily: 'var(--font-body)',
                                    fontSize: '0.875rem',
                                    fontWeight: 400,
                                    fontStyle: 'italic',
                                }}>
                                    MindMate is thinking…
                                </span>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>
                )}
            </div>

            {/* ── Input Area ─────────────────────────────────── */}
            <div style={{
                padding: '16px 0 24px',
                flexShrink: 0,
            }}>
                <form
                    onSubmit={handleSubmit}
                    style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '10px',
                        background: 'var(--color-surface)',
                        border: '1px solid var(--color-border)',
                        borderRadius: '14px',
                        padding: '10px 10px 10px 18px',
                        transition: 'border-color 0.2s',
                    }}
                    onFocusCapture={e => e.currentTarget.style.borderColor = 'var(--color-accent)'}
                    onBlurCapture={e => e.currentTarget.style.borderColor = 'var(--color-border)'}
                >
                    <input
                        ref={inputRef}
                        type="text"
                        id="user-input"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type your feelings or questions…"
                        disabled={isLoading}
                        style={{
                            flex: 1,
                            background: 'transparent',
                            border: 'none',
                            outline: 'none',
                            color: 'var(--color-text)',
                            fontFamily: 'var(--font-body)',
                            fontSize: '0.9375rem',
                            fontWeight: 400,
                            lineHeight: 1.5,
                        }}
                    />
                    <button
                        type="submit"
                        disabled={!input.trim() || isLoading}
                        aria-label="Send message"
                        style={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            width: '40px',
                            height: '40px',
                            borderRadius: '10px',
                            border: 'none',
                            background: (!input.trim() || isLoading)
                                ? 'var(--color-surface-2)'
                                : 'linear-gradient(135deg, #7C6EE8 0%, #C084FC 100%)',
                            color: (!input.trim() || isLoading) ? 'var(--color-text-muted)' : '#fff',
                            cursor: (!input.trim() || isLoading) ? 'not-allowed' : 'pointer',
                            transition: 'all 0.2s ease',
                            flexShrink: 0,
                        }}
                    >
                        <Send size={17} />
                    </button>
                </form>

                {/* Footer note */}
                <p style={{
                    fontFamily: 'var(--font-body)',
                    fontSize: '0.75rem',
                    fontWeight: 400,
                    color: 'var(--color-text-muted)',
                    textAlign: 'center',
                    marginTop: '10px',
                    letterSpacing: '0.01em',
                }}>
                    MindMate AI · © 2025 Likith & Nithin · For support, not professional therapy
                </p>
            </div>

            <style>{`
                @keyframes spin {
                    from { transform: rotate(0deg); }
                    to   { transform: rotate(360deg); }
                }
                input::placeholder {
                    color: var(--color-text-muted);
                    opacity: 0.7;
                }
            `}</style>
        </div>
    );
};

export default ChatInterface;
