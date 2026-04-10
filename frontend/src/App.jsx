import React from 'react';
import ChatInterface from './components/ChatInterface';
import {
  Show,
  SignInButton,
  SignUpButton,
  UserButton,
} from "@clerk/react";

/* ── Auth Landing — exactly matches mindmate_landing_editorial_luxe.html ── */
function AuthLanding() {
  return (
    <div style={{
      fontFamily: "'DM Sans', sans-serif",
      background: '#F5F0E8',
      minHeight: '100vh',
      display: 'flex', flexDirection: 'column', alignItems: 'center',
      padding: '0 0 4rem',
      position: 'relative',
      overflow: 'hidden',
    }}>

      {/* Noise texture overlay */}
      <div style={{
        position: 'absolute', inset: 0,
        backgroundImage: "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E\")",
        pointerEvents: 'none', zIndex: 0,
      }} />

      {/* Blob 1 */}
      <div style={{
        position: 'absolute', width: 500, height: 500,
        borderRadius: '60% 40% 70% 30% / 50% 60% 40% 50%',
        background: 'rgba(210,190,160,0.35)',
        top: -180, right: -160, pointerEvents: 'none',
        animation: 'morphblob 18s ease-in-out infinite alternate',
      }} />
      {/* Blob 2 */}
      <div style={{
        position: 'absolute', width: 380, height: 380,
        borderRadius: '40% 60% 30% 70% / 60% 40% 50% 50%',
        background: 'rgba(180,210,190,0.2)',
        bottom: -80, left: -100, pointerEvents: 'none',
        animation: 'morphblob 22s ease-in-out infinite alternate-reverse',
      }} />

      {/* Nav */}
      <nav style={{
        width: '100%', maxWidth: 680,
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        padding: '2rem 2rem 0', position: 'relative', zIndex: 2,
      }}>
        <div style={{
          fontFamily: "'Cormorant Garamond', serif",
          fontSize: 20, fontWeight: 400, letterSpacing: '0.5px',
          color: '#3a2e22', display: 'flex', alignItems: 'center', gap: 8,
        }}>
          <span style={{ width: 7, height: 7, borderRadius: '50%', background: '#8B6F4E', display: 'inline-block' }} />
          MindMate
        </div>
        <div style={{
          fontSize: 12, fontWeight: 300, color: '#8B7355',
          letterSpacing: '1.2px', textTransform: 'uppercase',
          borderBottom: '0.5px solid rgba(139,115,85,0.3)', paddingBottom: 1,
        }}>
          By Rushitha
        </div>
      </nav>

      {/* Hero section */}
      <section style={{
        position: 'relative', zIndex: 2,
        display: 'flex', flexDirection: 'column', alignItems: 'center',
        padding: '3.5rem 2rem 0', textAlign: 'center',
        width: '100%', maxWidth: 640,
      }}>
        {/* Kicker */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: 10,
          fontSize: 11, fontWeight: 400, letterSpacing: '2px',
          textTransform: 'uppercase', color: '#9C7A56', marginBottom: '1.8rem',
        }}>
          <span style={{ display: 'inline-block', width: 28, height: 0.5, background: '#C4A882' }} />
          Your mental wellness space
          <span style={{ display: 'inline-block', width: 28, height: 0.5, background: '#C4A882' }} />
        </div>

        {/* Display heading */}
        <h1 style={{
          fontFamily: "'Cormorant Garamond', serif",
          fontSize: 'clamp(48px, 8vw, 72px)',
          fontWeight: 300, lineHeight: 1.05, letterSpacing: '-1.5px',
          color: '#2C2218', marginBottom: '1rem',
        }}>
          A quiet place<br />
          to <em style={{ fontStyle: 'italic', fontWeight: 300, color: '#7A5C3A' }}>breathe</em><br />
          and be heard.
        </h1>

        <p style={{
          fontSize: 15, fontWeight: 300, lineHeight: 1.75, color: '#6B5B47',
          maxWidth: 380, marginBottom: '3rem',
        }}>
          Whatever you're carrying today — share it. MindMate listens without judgment, gently and always.
        </p>

        {/* Companion orb */}
        <div style={{ position: 'relative', width: 160, height: 160, marginBottom: '2.5rem', flexShrink: 0 }}>
          <div style={{
            position: 'absolute', inset: 0, borderRadius: '50%',
            border: '0.5px solid rgba(139,111,78,0.3)',
            animation: 'ringpulse 4s ease-in-out infinite',
          }} />
          <div style={{
            position: 'absolute', inset: 14, borderRadius: '50%',
            border: '0.5px solid rgba(139,111,78,0.2)',
            animation: 'ringpulse 4s ease-in-out infinite 0.6s',
          }} />
          <div style={{
            position: 'absolute', inset: 28, borderRadius: '50%',
            border: '0.5px solid rgba(139,111,78,0.15)',
          }} />
          <div style={{
            position: 'absolute', inset: 42, borderRadius: '50%',
            background: 'linear-gradient(145deg, #E8D5BC, #D4B896)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}>
            <svg width="52" height="52" viewBox="0 0 48 48" fill="none">
              <circle cx="24" cy="24" r="20" fill="rgba(90,60,30,0.08)" />
              <circle cx="17" cy="22" r="2.5" fill="#7A5C3A" opacity="0.7" />
              <circle cx="31" cy="22" r="2.5" fill="#7A5C3A" opacity="0.7" />
              <path d="M17 31 Q24 37 31 31" stroke="#7A5C3A" strokeWidth="1.5" strokeLinecap="round" fill="none" opacity="0.8" />
              <path d="M14 17 Q17 14 20 16" stroke="#9C7A56" strokeWidth="1" strokeLinecap="round" fill="none" opacity="0.5" />
              <path d="M28 16 Q31 14 34 17" stroke="#9C7A56" strokeWidth="1" strokeLinecap="round" fill="none" opacity="0.5" />
            </svg>
          </div>
        </div>
      </section>

      {/* Prompt / Auth section */}
      <div style={{
        position: 'relative', zIndex: 2,
        width: '100%', maxWidth: 560, padding: '0 2rem', marginBottom: '2rem',
      }}>
        <p style={{
          textAlign: 'center', fontSize: 12, fontWeight: 300,
          letterSpacing: '1.5px', textTransform: 'uppercase',
          color: '#A08060', marginBottom: '1.2rem',
        }}>
          Begin your conversation
        </p>

        {/* Sign In pill input style buttons */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          <SignInButton mode="modal">
            <button style={{
              width: '100%', padding: '14px 22px',
              background: '#7A5C3A', border: 'none',
              borderRadius: 50, cursor: 'pointer',
              fontFamily: "'DM Sans', sans-serif",
              fontSize: 14, fontWeight: 400, color: '#F5F0E8',
              letterSpacing: '0.3px', transition: 'background 0.2s, transform 0.15s',
            }}
            onMouseEnter={e => { e.currentTarget.style.background = '#5C4228'; e.currentTarget.style.transform = 'scale(1.02)'; }}
            onMouseLeave={e => { e.currentTarget.style.background = '#7A5C3A'; e.currentTarget.style.transform = 'scale(1)'; }}
            >
              Sign In — Enter your space →
            </button>
          </SignInButton>

          <SignUpButton mode="modal">
            <button style={{
              width: '100%', padding: '14px 22px',
              background: '#EDE5D8',
              border: '0.5px solid rgba(139,111,78,0.35)',
              borderRadius: 50, cursor: 'pointer',
              fontFamily: "'DM Sans', sans-serif",
              fontSize: 14, fontWeight: 300, color: '#7A5C3A',
              letterSpacing: '0.3px', transition: 'all 0.2s',
            }}
            onMouseEnter={e => { e.currentTarget.style.borderColor = 'rgba(122,92,58,0.6)'; e.currentTarget.style.background = '#fff'; }}
            onMouseLeave={e => { e.currentTarget.style.borderColor = 'rgba(139,111,78,0.35)'; e.currentTarget.style.background = '#EDE5D8'; }}
            >
              Create account — First time here
            </button>
          </SignUpButton>
        </div>
      </div>

      {/* Suggestion chips — 2 col grid */}
      <div style={{
        position: 'relative', zIndex: 2,
        width: '100%', maxWidth: 560, padding: '0 2rem', marginBottom: '3rem',
      }}>
        <div className="mm2-chips-grid" style={{
          display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10,
        }}>
          {[
            { label: "Feeling overwhelmed", sub: "Too much on your plate", iconBg: "rgba(210,100,80,0.12)", icon: (
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><circle cx="7" cy="7" r="5" stroke="#C45840" strokeWidth="1.2"/><path d="M7 4v3.5l2 1.5" stroke="#C45840" strokeWidth="1.2" strokeLinecap="round"/></svg>
            )},
            { label: "Managing anxiety", sub: "Finding calm within", iconBg: "rgba(100,140,210,0.12)", icon: (
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 2 Q11 5 11 8 Q11 11 7 12 Q3 11 3 8 Q3 5 7 2Z" stroke="#4878C0" strokeWidth="1.2" fill="none"/></svg>
            )},
            { label: "Stress relief", sub: "Breathe and release", iconBg: "rgba(80,160,120,0.12)", icon: (
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 3 C7 3 4 6 4 8.5 C4 10.5 5.3 12 7 12 C8.7 12 10 10.5 10 8.5 C10 6 7 3 7 3Z" stroke="#3A9060" strokeWidth="1.2" fill="none"/></svg>
            )},
            { label: "Tough day support", sub: "You are not alone", iconBg: "rgba(190,150,80,0.12)", icon: (
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><circle cx="7" cy="5" r="2.5" stroke="#B08030" strokeWidth="1.2"/><path d="M3 12 C3 9.5 4.8 8 7 8 C9.2 8 11 9.5 11 12" stroke="#B08030" strokeWidth="1.2" strokeLinecap="round" fill="none"/></svg>
            )},
          ].map(chip => (
            <div key={chip.label} className="mm2-chip2" style={{
              padding: '12px 18px', borderRadius: 12,
              background: 'rgba(255,252,245,0.7)',
              border: '0.5px solid rgba(139,111,78,0.2)',
              cursor: 'pointer', transition: 'all 0.2s',
              display: 'flex', alignItems: 'flex-start', gap: 10,
            }}>
              <div style={{
                width: 28, height: 28, borderRadius: 8,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                flexShrink: 0, marginTop: 1, background: chip.iconBg,
              }}>{chip.icon}</div>
              <div>
                <div style={{ fontSize: 13, fontWeight: 400, color: '#3a2e22', lineHeight: 1.4 }}>{chip.label}</div>
                <span style={{ fontSize: 11, color: '#A08060', fontWeight: 300, marginTop: 1, display: 'block' }}>{chip.sub}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Divider */}
      <div style={{
        width: '100%', maxWidth: 480, height: 0.5,
        background: 'linear-gradient(90deg, transparent, rgba(139,111,78,0.25), transparent)',
        margin: '0 auto 2.5rem', position: 'relative', zIndex: 2,
      }} />

      {/* Features grid */}
      <div style={{
        position: 'relative', zIndex: 2,
        width: '100%', maxWidth: 560, padding: '0 2rem',
        display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)',
        gap: 16, marginBottom: '3rem',
      }}>
        {[
          { name: "Always present", desc: "Day or night, whenever you need", bg: "rgba(139,111,78,0.1)", icon: (
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 2 L8 14 M2 8 L14 8" stroke="#7A5C3A" strokeWidth="1.2" strokeLinecap="round" opacity="0.6"/><circle cx="8" cy="8" r="3" stroke="#7A5C3A" strokeWidth="1.2"/></svg>
          )},
          { name: "Safe space", desc: "Private, gentle, no judgment", bg: "rgba(80,140,100,0.1)", icon: (
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8 Q3 3 8 3 Q13 3 13 8 Q13 12 8 13 L4 14 L5 11 Q3 10 3 8Z" stroke="#3A7850" strokeWidth="1.2" fill="none"/></svg>
          )},
          { name: "Guided calm", desc: "Techniques backed by research", bg: "rgba(100,120,180,0.1)", icon: (
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 3 C8 3 5 5.5 5 8 C5 9.66 6.34 11 8 11 C9.66 11 11 9.66 11 8 C11 5.5 8 3 8 3Z" stroke="#5068B8" strokeWidth="1.2" fill="none"/><path d="M8 11 L8 14" stroke="#5068B8" strokeWidth="1.2" strokeLinecap="round"/></svg>
          )},
        ].map(f => (
          <div key={f.name} style={{
            textAlign: 'center', padding: '20px 12px',
            background: 'rgba(255,252,245,0.6)',
            border: '0.5px solid rgba(139,111,78,0.15)',
            borderRadius: 16,
          }}>
            <div style={{
              width: 36, height: 36, borderRadius: '50%',
              margin: '0 auto 10px',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              background: f.bg,
            }}>{f.icon}</div>
            <div style={{ fontSize: 12, fontWeight: 500, color: '#3a2e22', marginBottom: 3, letterSpacing: '0.2px' }}>{f.name}</div>
            <div style={{ fontSize: 11, fontWeight: 300, color: '#9C7A56', lineHeight: 1.5 }}>{f.desc}</div>
          </div>
        ))}
      </div>

      {/* Footer */}
      <footer style={{
        position: 'relative', zIndex: 2,
        textAlign: 'center', fontSize: 11, fontWeight: 300,
        color: '#B09070', letterSpacing: '0.5px', lineHeight: 2,
      }}>
        <strong style={{ fontWeight: 400, color: '#9C7A56' }}>MindMate AI</strong> · © 2026 Rushitha and team<br />
        Emotional support companion · Not a substitute for professional therapy
      </footer>
    </div>
  );
}

/* ── Main App ─────────────────────────────────────────────── */
function App() {
  return (
    <div style={{ minHeight: '100vh', background: '#F5F0E8' }}>

      {/* Top nav — signed in */}
      <Show when="signed-in">
        <header style={{
          padding: '0 2rem',
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          borderBottom: '0.5px solid rgba(139,111,78,0.2)',
          background: 'rgba(245,240,232,0.95)',
          backdropFilter: 'blur(12px)',
          height: '4rem',
          position: 'sticky', top: 0, zIndex: 50,
        }}>
          <div style={{
            fontFamily: "'Cormorant Garamond', serif",
            fontSize: 20, fontWeight: 400, letterSpacing: '0.5px',
            color: '#3a2e22', display: 'flex', alignItems: 'center', gap: 8,
          }}>
            <span style={{ width: 7, height: 7, borderRadius: '50%', background: '#8B6F4E', display: 'inline-block' }} />
            MindMate
          </div>
          <UserButton />
        </header>
      </Show>

      {/* Auth landing — signed out */}
      <Show when="signed-out">
        <AuthLanding />
      </Show>

      {/* Chat — signed in */}
      <Show when="signed-in">
        <ChatInterface />
      </Show>
    </div>
  );
}

export default App;
