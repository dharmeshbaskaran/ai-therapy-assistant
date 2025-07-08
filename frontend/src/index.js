import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';

// 🎨 Chat UI styling
const chatBg = '#f4f7fa';
const userBubble = {
  background: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
  color: '#222',
  alignSelf: 'flex-end',
  borderRadius: '18px 18px 4px 18px',
  padding: '12px 18px',
  margin: '6px 0',
  maxWidth: '75%',
  boxShadow: '0 2px 8px #0001',
};
const aiBubble = {
  background: 'linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)',
  color: '#222',
  alignSelf: 'flex-start',
  borderRadius: '18px 18px 18px 4px',
  padding: '12px 18px',
  margin: '6px 0',
  maxWidth: '75%',
  boxShadow: '0 2px 8px #0001',
};
const chatContainer = {
  background: chatBg,
  border: '1px solid #e0e0e0',
  borderRadius: 18,
  padding: 20,
  minHeight: 350,
  marginBottom: 24,
  display: 'flex',
  flexDirection: 'column',
  gap: 0,
  boxShadow: '0 4px 24px #0001',
};
const inputBar = {
  display: 'flex',
  alignItems: 'center',
  background: '#fff',
  borderRadius: 12,
  boxShadow: '0 2px 8px #0001',
  padding: 6,
};
const inputStyle = {
  flex: 1,
  border: 'none',
  outline: 'none',
  fontSize: 16,
  padding: '12px 14px',
  borderRadius: 8,
  background: 'transparent',
};
const sendBtn = {
  background: 'linear-gradient(135deg, #8ec5fc 0%, #e0c3fc 100%)',
  border: 'none',
  color: '#333',
  fontWeight: 600,
  fontSize: 16,
  borderRadius: 8,
  padding: '10px 20px',
  marginLeft: 10,
  cursor: 'pointer',
  boxShadow: '0 2px 8px #0001',
  transition: 'background 0.2s',
};

// 🌐 Load API URL from .env or fallback
const API_URL = process.env.REACT_APP_API_URL || 'http://192.168.1.6:5001';

const App = () => {
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'Hello! How are you feeling today?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', text: input.trim() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input.trim() })
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`HTTP ${res.status} - ${errorText}`);
      }

      const data = await res.json();
      const aiMessage = { role: 'assistant', text: data.reply };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('❌ FETCH ERROR:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        text: `Error: ${error.message}`
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      maxWidth: 520,
      margin: '48px auto',
      fontFamily: 'Inter, Arial, sans-serif',
      background: '#fff',
      borderRadius: 24,
      boxShadow: '0 8px 32px #0002',
      padding: 32
    }}>
      <h2 style={{
        textAlign: 'center',
        marginBottom: 24,
        fontWeight: 800,
        letterSpacing: 1
      }}>
        🧠 Therapy Assistant
      </h2>

      <div style={chatContainer}>
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={msg.role === 'user' ? userBubble : aiBubble}
          >
            <span style={{ fontWeight: 700, fontSize: 13, opacity: 0.7, marginRight: 8 }}>
              {msg.role === 'user' ? 'You' : 'Therapist'}:
            </span>
            {msg.text}
          </div>
        ))}
        {loading && (
          <div style={{ ...aiBubble, fontStyle: 'italic', opacity: 0.7 }}>
            Therapist is typing...
          </div>
        )}
      </div>

      <form style={inputBar} onSubmit={e => { e.preventDefault(); sendMessage(); }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && !loading && sendMessage()}
          placeholder="Type your message..."
          style={inputStyle}
          disabled={loading}
        />
        <button type="submit" style={sendBtn} disabled={loading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
