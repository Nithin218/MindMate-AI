import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Loader2 } from 'lucide-react';
import MessageBubble from './MessageBubble';
import heroImage from '../assets/hero_image.png';

const WELCOME_SUGGESTIONS = [
  { label: "I've been feeling overwhelmed lately", sub: "Too much on your plate",  iconBg: "rgba(210,100,80,0.12)", icon: (
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><circle cx="7" cy="7" r="5" stroke="#C45840" strokeWidth="1.2"/><path d="M7 4v3.5l2 1.5" stroke="#C45840" strokeWidth="1.2" strokeLinecap="round"/></svg>
  )},
  { label: "How can I manage anxiety better?",      sub: "Finding calm within",    iconBg: "rgba(100,140,210,0.12)", icon: (
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 2 Q11 5 11 8 Q11 11 7 12 Q3 11 3 8 Q3 5 7 2Z" stroke="#4878C0" strokeWidth="1.2" fill="none"/></svg>
  )},
  { label: "I need help with stress relief",        sub: "Breathe and release",    iconBg: "rgba(80,160,120,0.12)", icon: (
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 3 C7 3 4 6 4 8.5 C4 10.5 5.3 12 7 12 C8.7 12 10 10.5 10 8.5 C10 6 7 3 7 3Z" stroke="#3A9060" strokeWidth="1.2" fill="none"/></svg>
  )},
  { label: "Talk me through a tough day",           sub: "You are not alone",      iconBg: "rgba(190,150,80,0.12)", icon: (
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><circle cx="7" cy="5" r="2.5" stroke="#B08030" strokeWidth="1.2"/><path d="M3 12 C3 9.5 4.8 8 7 8 C9.2 8 11 9.5 11 12" stroke="#B08030" strokeWidth="1.2" strokeLinecap="round" fill="none"/></svg>
  )},
];

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput]       = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef       = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e, overrideText) => {
    if (e) e.preventDefault();
    const text = overrideText ?? input;
    if (!text.trim() || isLoading) return;

    setMessages(prev => [...prev, { role: 'user', content: text }]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post('/query', { question: text });
      setMessages(prev => [...prev, { role: 'assistant', content: response.data.answer }]);
    } catch {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'I apologize, but I encountered an error. Please try again.',
      }]);
    } finally {
      setIsLoading(false);
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  };

  return (
    <div style={{
      display: 'flex', flexDirection: 'column',
      height: 'calc(100vh - 4rem)',
      maxWidth: 680, margin: '0 auto',
      padding: '0 2rem',
      fontFamily: "'DM Sans', sans-serif",
    }}>

      {/* ── Header ─────────────────────────────────────────── */}
      <header style={{
        padding: '1.75rem 0 1.25rem',
        textAlign: 'center',
        borderBottom: '0.5px solid rgba(139,111,78,0.2)',
        marginBottom: '4px', flexShrink: 0,
      }}>
        <div style={{
          display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8,
          marginBottom: 6,
        }}>
          <span style={{ display: 'inline-block', width: 28, height: 0.5, background: '#C4A882' }} />
          <span style={{ fontSize: 10, fontWeight: 400, letterSpacing: '2px', textTransform: 'uppercase', color: '#9C7A56' }}>
            Your mental wellness space
          </span>
          <span style={{ display: 'inline-block', width: 28, height: 0.5, background: '#C4A882' }} />
        </div>
        <h1 style={{
          fontFamily: "'Cormorant Garamond', serif",
          fontSize: 'clamp(1.5rem, 4vw, 2rem)',
          fontWeight: 300, letterSpacing: '-0.5px', color: '#2C2218', margin: 0,
        }}>
          MindMate <em style={{ fontStyle: 'italic', color: '#7A5C3A' }}>AI</em>
        </h1>
        <p style={{
          fontSize: 13, fontWeight: 300, color: '#9C7A56',
          marginTop: 4, letterSpacing: '0.3px',
        }}>
          Always here to listen
        </p>
      </header>

      {/* ── Chat Area ──────────────────────────────────────── */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '1.5rem 0' }}>
        {messages.length === 0 ? (
          <div style={{
            display: 'flex', flexDirection: 'column',
            alignItems: 'center', justifyContent: 'center',
            height: '100%', gap: '2rem', paddingBottom: '40px',
            animation: 'fadeIn 0.8s ease-out',
          }}>
            {/* Hero image + welcome text */}
            <div style={{ textAlign: 'center' }}>
              <img
                src={heroImage} alt="MindMate AI"
                style={{
                  width: 140, height: 140, objectFit: 'cover',
                  borderRadius: '50%', margin: '0 auto 20px', display: 'block',
                  border: '2px solid rgba(139,111,78,0.25)',
                  boxShadow: '0 8px 32px rgba(90,60,30,0.12)',
                }}
              />
              <p style={{
                fontFamily: "'Cormorant Garamond', serif",
                fontSize: 'clamp(1.3rem, 3.5vw, 1.7rem)',
                fontWeight: 300, color: '#2C2218', marginBottom: 8,
              }}>
                How are you feeling <em style={{ color: '#7A5C3A', fontStyle: 'italic' }}>today?</em>
              </p>
              <p style={{ fontSize: 14, fontWeight: 300, color: '#9C7A56', lineHeight: 1.65 }}>
                Share what's on your mind — I'm here to help.
              </p>
            </div>

            {/* Chip grid — 2-col like reference */}
            <div style={{
              display: 'grid', gridTemplateColumns: '1fr 1fr',
              gap: 10, width: '100%', maxWidth: 520,
            }}>
              {WELCOME_SUGGESTIONS.map(s => (
                <button
                  key={s.label}
                  className="mm2-chip2"
                  onClick={() => handleSubmit(null, s.label)}
                  style={{
                    padding: '12px 18px', borderRadius: 12, textAlign: 'left',
                    background: 'rgba(255,252,245,0.7)',
                    border: '0.5px solid rgba(139,111,78,0.2)',
                    cursor: 'pointer', transition: 'all 0.2s',
                    display: 'flex', alignItems: 'flex-start', gap: 10,
                  }}
                >
                  <div style={{
                    width: 28, height: 28, borderRadius: 8,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    flexShrink: 0, marginTop: 1, background: s.iconBg,
                  }}>{s.icon}</div>
                  <div>
                    <div style={{ fontSize: 13, fontWeight: 400, color: '#3a2e22', lineHeight: 1.4 }}>{s.label}</div>
                    <span style={{ fontSize: 11, color: '#A08060', fontWeight: 300, marginTop: 1, display: 'block' }}>{s.sub}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div>
            {messages.map((msg, i) => <MessageBubble key={i} message={msg} />)}
            {isLoading && (
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '10px 4px', color: '#A08060' }}>
                <Loader2 size={13} style={{ animation: 'spin 1s linear infinite', color: '#9C7A56' }} />
                <span style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: '1rem', fontStyle: 'italic', fontWeight: 300, color: '#9C7A56' }}>
                  MindMate is thinking…
                </span>
              </div>
            )}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* ── Input Area ─────────────────────────────────────── */}
      <div style={{ padding: '14px 0 22px', flexShrink: 0 }}>
        <p style={{
          textAlign: 'center', fontSize: 11, fontWeight: 300,
          letterSpacing: '1.5px', textTransform: 'uppercase',
          color: '#A08060', marginBottom: '0.9rem',
        }}>
          Begin your conversation
        </p>
        <form
          className="mm2-input-row"
          onSubmit={handleSubmit}
          style={{
            display: 'flex', alignItems: 'center',
            background: '#EDE5D8',
            border: '0.5px solid rgba(139,111,78,0.3)',
            borderRadius: 50, overflow: 'hidden',
            transition: 'border-color 0.2s, box-shadow 0.2s',
          }}
        >
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="How are you feeling right now…"
            disabled={isLoading}
            style={{
              flex: 1, padding: '14px 22px',
              background: 'transparent', border: 'none', outline: 'none',
              fontFamily: "'DM Sans', sans-serif",
              fontSize: 14, fontWeight: 300, color: '#3a2e22',
            }}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            aria-label="Send"
            style={{
              width: 42, height: 42, margin: 5, borderRadius: '50%',
              background: (!input.trim() || isLoading) ? 'rgba(139,111,78,0.3)' : '#7A5C3A',
              border: 'none', cursor: (!input.trim() || isLoading) ? 'not-allowed' : 'pointer',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              flexShrink: 0, transition: 'background 0.2s, transform 0.15s',
            }}
            onMouseEnter={e => { if (input.trim() && !isLoading) { e.currentTarget.style.background = '#5C4228'; e.currentTarget.style.transform = 'scale(1.06)'; }}}
            onMouseLeave={e => { e.currentTarget.style.background = (!input.trim() || isLoading) ? 'rgba(139,111,78,0.3)' : '#7A5C3A'; e.currentTarget.style.transform = 'scale(1)'; }}
          >
            <svg viewBox="0 0 16 16" width="15" height="15" fill="none">
              <path d="M3 8h10M9 4l4 4-4 4" stroke="#F5F0E8" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </button>
        </form>

        <p style={{
          fontSize: 10, fontWeight: 300, color: '#B09070',
          textAlign: 'center', marginTop: 10, letterSpacing: '0.5px',
        }}>
          MindMate AI · © 2026 Rushitha and team · For support, not professional therapy
        </p>
      </div>

      <style>{`
        input::placeholder { color: #A89070; font-family: 'DM Sans', sans-serif; font-weight: 300; }
      `}</style>
    </div>
  );
};

export default ChatInterface;
