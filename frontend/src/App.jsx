import React from 'react';
import ChatInterface from './components/ChatInterface';

function App() {
    return (
        <div style={{ minHeight: '100vh', background: 'var(--color-bg-gradient)', color: 'var(--color-text)' }}>
            <ChatInterface />
        </div>
    );
}

export default App;
