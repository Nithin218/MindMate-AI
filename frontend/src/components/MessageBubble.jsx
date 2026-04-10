import React from 'react';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';

const MessageBubble = ({ message }) => {
  const isUser = message.role === 'user';
  const bubbleClassName = isUser
    ? 'mindmate-message-surface mindmate-message-user'
    : 'mindmate-message-surface mindmate-message-assistant';

  return (
    <motion.div
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2, ease: 'easeOut' }}
      style={{
        display: 'flex',
        justifyContent: isUser ? 'flex-end' : 'flex-start',
        width: '100%',
        marginBottom: '12px',
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
          width: 28, height: 28, borderRadius: '50%',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          flexShrink: 0, marginTop: 2,
          background: isUser
            ? 'linear-gradient(145deg, #E8D5BC, #D4B896)'
            : 'rgba(139,111,78,0.12)',
          border: `0.5px solid rgba(139,111,78,${isUser ? '0.25' : '0.2'})`,
        }}>
          {isUser ? (
            <svg viewBox="0 0 14 14" width="12" height="12" fill="none">
              <circle cx="7" cy="5" r="2.2" stroke="#7A5C3A" strokeWidth="1.1" />
              <path d="M2.5 12 C2.5 9.5 4.5 8 7 8 C9.5 8 11.5 9.5 11.5 12" stroke="#7A5C3A" strokeWidth="1.1" strokeLinecap="round" fill="none" />
            </svg>
          ) : (
            <svg viewBox="0 0 48 48" width="14" height="14" fill="none">
              <circle cx="17" cy="22" r="2.5" fill="#7A5C3A" opacity="0.7" />
              <circle cx="31" cy="22" r="2.5" fill="#7A5C3A" opacity="0.7" />
              <path d="M17 31 Q24 37 31 31" stroke="#7A5C3A" strokeWidth="2" strokeLinecap="round" fill="none" opacity="0.8" />
            </svg>
          )}
        </div>

        {/* Bubble */}
        <div
          className={bubbleClassName}
          style={{
          padding: '11px 15px',
          borderRadius: isUser ? '16px 4px 16px 16px' : '4px 16px 16px 16px',
          background: isUser
            ? 'var(--color-user-bubble)'
            : 'linear-gradient(180deg, rgba(255, 252, 245, 0.96), rgba(248, 240, 229, 0.92))',
          border: `0.5px solid rgba(139,111,78,${isUser ? '0.25' : '0.18'})`,
          boxShadow: isUser
            ? '0 2px 8px rgba(90,60,30,0.06)'
            : '0 10px 24px rgba(90,60,30,0.08)',
          color: 'var(--color-text)',
          fontFamily: 'var(--font-body)',
          fontSize: '0.92rem', fontWeight: 300,
          lineHeight: 1.65, letterSpacing: '0.01em',
          wordBreak: 'break-word',
        }}
        >
          {/* Sender label */}
          <div style={{
            fontFamily: "'DM Sans', sans-serif",
            fontSize: '0.625rem', fontWeight: 500,
            letterSpacing: '0.1em', textTransform: 'uppercase',
            color: isUser ? '#B09070' : '#9C7A56',
            marginBottom: '5px',
          }}>
            {isUser ? 'You' : 'MindMate'}
          </div>
          {isUser ? (
            <span style={{ whiteSpace: 'pre-wrap' }}>{message.content}</span>
          ) : (
            <div className="markdown-body mindmate-generated-copy">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default MessageBubble;
