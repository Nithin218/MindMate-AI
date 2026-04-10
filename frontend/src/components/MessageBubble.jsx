import React from 'react';
import { motion } from 'framer-motion';
import { User, Bot } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const MessageBubble = ({ message }) => {
    const isUser = message.role === 'user';

    return (
        <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.22, ease: 'easeOut' }}
            style={{
                display: 'flex',
                justifyContent: isUser ? 'flex-end' : 'flex-start',
                width: '100%',
                marginBottom: '14px',
            }}
        >
            <div style={{
                display: 'flex',
                flexDirection: isUser ? 'row-reverse' : 'row',
                alignItems: 'flex-start',
                gap: '10px',
                maxWidth: '78%',
            }}>
                {/* Avatar */}
                <div style={{
                    width: '32px',
                    height: '32px',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0,
                    background: isUser
                        ? 'var(--color-surface-2)'
                        : 'var(--color-accent)',
                    border: `1px solid ${isUser ? 'var(--color-border)' : 'transparent'}`,
                    marginTop: '2px',
                }}>
                    {isUser
                        ? <User size={16} color="var(--color-text-muted)" />
                        : <Bot size={16} color="#fff" />
                    }
                </div>

                {/* Bubble */}
                <div style={{
                    padding: '12px 16px',
                    borderRadius: isUser ? '16px 4px 16px 16px' : '4px 16px 16px 16px',
                    background: isUser ? 'var(--color-user-bubble)' : 'var(--color-bot-bubble)',
                    border: `1px solid ${isUser ? 'var(--color-user-bubble)' : 'var(--color-border)'}`,
                    boxShadow: isUser ? 'none' : '0 2px 4px rgba(0,0,0,0.02)',
                    color: 'var(--color-text)',
                    fontFamily: 'var(--font-body)',
                    fontSize: '0.9375rem',
                    fontWeight: 400,
                    lineHeight: 1.65,
                    letterSpacing: '0.01em',
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word',
                }}>
                    {/* Sender label */}
                    <div style={{
                        fontFamily: 'var(--font-body)',
                        fontSize: '0.6875rem',
                        fontWeight: 600,
                        letterSpacing: '0.06em',
                        textTransform: 'uppercase',
                        color: isUser ? 'var(--color-surface)' : 'var(--color-accent)',
                        marginBottom: '8px',
                    }}>
                        {isUser ? 'You' : 'MindMate'}
                    </div>
                    {isUser ? (
                        message.content
                    ) : (
                        <div className="markdown-body">
                            <ReactMarkdown>{message.content}</ReactMarkdown>
                        </div>
                    )}
                </div>
            </div>
        </motion.div>
    );
};

export default MessageBubble;
