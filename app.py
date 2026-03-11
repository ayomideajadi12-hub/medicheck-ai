import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(
    page_title="MediCheck AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── YOUR API KEY ──────────────────────────────────────────────────────────────
GEMINI_API_KEY = "AIzaSyB1cokh2jPvh0Zf9hy7EnogRlpmLBcthFU"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

* { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }

.stApp { background: #f8fafc; min-height: 100vh; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── NAVBAR ── */
.navbar {
    background: #ffffff;
    border-bottom: 1px solid #e2e8f0;
    padding: 16px 60px;
    display: flex; align-items: center; justify-content: space-between;
    position: sticky; top: 0; z-index: 100;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.nav-logo { font-size: 1.2rem; font-weight: 800; color: #0f172a; display: flex; align-items: center; gap: 8px; }
.nav-logo span { color: #2563eb; }
.nav-tag {
    background: #eff6ff; color: #2563eb;
    border: 1px solid #bfdbfe;
    border-radius: 100px; padding: 5px 14px;
    font-size: 12px; font-weight: 600;
}

/* ── HERO ── */
.hero {
    background: linear-gradient(135deg, #1e40af 0%, #2563eb 50%, #3b82f6 100%);
    padding: 64px 60px 56px;
    position: relative; overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}
.hero-inner {
    max-width: 1100px; margin: 0 auto;
    display: grid; grid-template-columns: 1fr auto;
    align-items: center; gap: 60px;
    position: relative; z-index: 1;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 100px; padding: 6px 16px;
    font-size: 12px; font-weight: 600; color: #bfdbfe;
    letter-spacing: 0.06em; text-transform: uppercase;
    margin-bottom: 20px;
}
.hero h1 {
    font-size: 3rem; font-weight: 800;
    color: #ffffff; line-height: 1.1;
    letter-spacing: -0.02em; margin-bottom: 16px;
}
.hero p { font-size: 1.05rem; color: #bfdbfe; line-height: 1.7; max-width: 520px; }
.hero-stats { display: flex; gap: 32px; margin-top: 32px; }
.hstat { }
.hstat-num {
    font-size: 1.8rem; font-weight: 800; color: #ffffff;
    font-family: 'JetBrains Mono', monospace; line-height: 1;
}
.hstat-label { font-size: 11px; color: #93c5fd; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px; }

.hero-cards { display: flex; flex-direction: column; gap: 10px; }
.hero-card {
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 14px; padding: 14px 20px;
    display: flex; align-items: center; gap: 12px;
    min-width: 220px;
}
.hero-card-icon { font-size: 1.3rem; }
.hero-card-text { font-size: 0.88rem; color: #e0f2fe; font-weight: 500; }

/* ── MAIN ── */
.main-wrap { max-width: 1100px; margin: 0 auto; padding: 40px 60px; }

/* ── DISCLAIMER ── */
.disclaimer {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-left: 4px solid #f59e0b;
    border-radius: 12px; padding: 14px 18px;
    display: flex; align-items: flex-start; gap: 10px;
    margin-bottom: 28px;
}
.disclaimer-text { font-size: 0.84rem; color: #92400e; line-height: 1.6; }
.disclaimer-text strong { color: #78350f; }

/* ── CHAT CONTAINER ── */
.chat-container {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
    margin-bottom: 20px;
    overflow: hidden;
}
.chat-header {
    background: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
    padding: 16px 24px;
    display: flex; align-items: center; gap: 10px;
}
.chat-status-dot {
    width: 9px; height: 9px; border-radius: 50%;
    background: #22c55e;
    box-shadow: 0 0 6px rgba(34,197,94,0.5);
    animation: pulse 2s infinite;
}
@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.5; } }
.chat-header-title { font-size: 0.88rem; font-weight: 700; color: #1e293b; }
.chat-header-sub { font-size: 0.78rem; color: #94a3b8; margin-left: 4px; }
.chat-messages { padding: 24px; min-height: 180px; max-height: 480px; overflow-y: auto; }

/* ── MESSAGES ── */
.msg-user {
    display: flex; justify-content: flex-end; margin-bottom: 16px;
}
.msg-user-bubble {
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
    border-radius: 18px 18px 4px 18px;
    padding: 12px 18px; max-width: 68%;
    font-size: 0.9rem; color: #ffffff; line-height: 1.6;
    box-shadow: 0 2px 8px rgba(37,99,235,0.25);
}
.msg-ai {
    display: flex; gap: 10px; margin-bottom: 16px; align-items: flex-start;
}
.msg-ai-avatar {
    width: 34px; height: 34px; border-radius: 10px;
    background: linear-gradient(135deg, #1d4ed8, #3b82f6);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.95rem; flex-shrink: 0;
    box-shadow: 0 2px 8px rgba(37,99,235,0.2);
}
.msg-ai-bubble {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px 18px 18px 18px;
    padding: 14px 18px; max-width: 75%;
    font-size: 0.9rem; color: #1e293b; line-height: 1.7;
}

/* ── INPUT AREA ── */
[data-testid="stTextArea"] textarea {
    background: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 14px !important;
    color: #1e293b !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.93rem !important;
    padding: 14px 16px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.08) !important;
}
[data-testid="stTextArea"] textarea::placeholder { color: #94a3b8 !important; }

.stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; padding: 14px 28px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important; font-size: 0.93rem !important;
    width: 100% !important; transition: all 0.2s !important;
    box-shadow: 0 4px 12px rgba(37,99,235,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(37,99,235,0.35) !important;
}

/* ── QUICK CHIPS ── */
.quick-label {
    font-size: 11px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.1em; color: #94a3b8; margin-bottom: 10px;
}
.quick-wrap { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px; }
.qchip {
    background: #f1f5f9; border: 1px solid #e2e8f0;
    border-radius: 100px; padding: 6px 14px;
    font-size: 12px; color: #475569; font-weight: 500;
}

/* ── FEATURE CARDS ── */
.features-grid {
    display: grid; grid-template-columns: repeat(3,1fr);
    gap: 16px; margin-top: 36px;
    padding-top: 36px; border-top: 1px solid #e2e8f0;
}
.feat-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px; padding: 24px;
    transition: box-shadow 0.2s, transform 0.2s;
}
.feat-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.08); transform: translateY(-2px); }
.feat-icon {
    width: 44px; height: 44px; border-radius: 12px;
    background: #eff6ff; display: flex; align-items: center;
    justify-content: center; font-size: 1.3rem;
    margin-bottom: 14px;
}
.feat-title { font-size: 0.92rem; font-weight: 700; color: #1e293b; margin-bottom: 6px; }
.feat-desc { font-size: 0.82rem; color: #64748b; line-height: 1.6; }

/* ── FOOTER ── */
.footer {
    background: #1e293b;
    padding: 32px 60px;
    display: flex; justify-content: space-between;
    align-items: center; flex-wrap: wrap; gap: 16px;
    margin-top: 48px;
}
.footer-logo { font-size: 1rem; font-weight: 800; color: #ffffff; }
.footer-logo span { color: #60a5fa; }
.footer-text { font-size: 0.8rem; color: #475569; }

.stSpinner > div { border-top-color: #2563eb !important; }
</style>
""", unsafe_allow_html=True)

# ─── NAVBAR ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div class="nav-logo">🏥 Medi<span>Check</span> AI</div>
    <div class="nav-tag">🇳🇬 Built for Nigeria</div>
</div>
""", unsafe_allow_html=True)

# ─── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-inner">
        <div>
            <div class="hero-badge">🤖 AI-Powered Health Assistant</div>
            <h1>Describe Your Symptoms.<br/>Get Instant Guidance.</h1>
            <p>Tell us how you're feeling and our AI will identify possible conditions, assess severity, and advise whether you need to see a doctor — free, always.</p>
            <div class="hero-stats">
                <div class="hstat">
                    <div class="hstat-num">100+</div>
                    <div class="hstat-label">Conditions</div>
                </div>
                <div class="hstat">
                    <div class="hstat-num">&lt;10s</div>
                    <div class="hstat-label">Response</div>
                </div>
                <div class="hstat">
                    <div class="hstat-num">24/7</div>
                    <div class="hstat-label">Available</div>
                </div>
                <div class="hstat">
                    <div class="hstat-num">Free</div>
                    <div class="hstat-label">Always</div>
                </div>
            </div>
        </div>
        <div class="hero-cards">
            <div class="hero-card"><span class="hero-card-icon">🔴</span><span class="hero-card-text">Emergency — Go to hospital now</span></div>
            <div class="hero-card"><span class="hero-card-icon">🟡</span><span class="hero-card-text">Moderate — See doctor within 48hrs</span></div>
            <div class="hero-card"><span class="hero-card-icon">🟢</span><span class="hero-card-text">Mild — Home care is sufficient</span></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── MAIN ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
    <span style="font-size:1.1rem; flex-shrink:0">⚠️</span>
    <div class="disclaimer-text">
        <strong>Medical Disclaimer:</strong> MediCheck AI provides general health information only and is NOT a substitute for professional medical advice. Always consult a qualified doctor. In emergencies call <strong>112</strong> or go to the nearest hospital immediately.
    </div>
</div>
""", unsafe_allow_html=True)

# Init chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "👋 Hello! I'm MediCheck AI. Please describe your symptoms in detail — including when they started, how severe they feel, and any other information. I'll help identify possible conditions and advise on next steps."
    })

# Chat UI
st.markdown("""
<div class="chat-container">
<div class="chat-header">
    <div class="chat-status-dot"></div>
    <span class="chat-header-title">MediCheck AI</span>
    <span class="chat-header-sub">— Online and ready</span>
</div>
<div class="chat-messages">
""", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-user">
            <div class="msg-user-bubble">{msg["content"]}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="msg-ai">
            <div class="msg-ai-avatar">🏥</div>
            <div class="msg-ai-bubble">{msg["content"]}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# Quick chips
st.markdown("""
<div class="quick-label">💡 Try these examples</div>
<div class="quick-wrap">
    <div class="qchip">🤒 Fever + headache</div>
    <div class="qchip">🤧 Cough + sore throat</div>
    <div class="qchip">🤢 Nausea + stomach pain</div>
    <div class="qchip">💪 Body aches + fatigue</div>
    <div class="qchip">🫁 Chest pain + breathlessness</div>
    <div class="qchip">🦴 Joint pain + swelling</div>
    <div class="qchip">🤕 Severe headache</div>
    <div class="qchip">👁️ Eye redness</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_area(
        "Symptoms",
        placeholder="e.g. I've had a high fever of 39°C for 2 days, with a bad headache, body aches and I feel very weak. I also have a slight cough and loss of appetite...",
        height=100,
        label_visibility="collapsed"
    )
with col2:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    send_btn = st.button("🔍 Analyse", use_container_width=True)

# ─── GEMINI ───────────────────────────────────────────────────────────────────
if send_btn and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("🤖 Analysing your symptoms..."):
        prompt = f"""You are MediCheck AI, a helpful and empathetic medical assistant built for Nigerian users.
A user has described these symptoms: {user_input}

Respond in this exact HTML format:

<b>🔍 Possible Conditions:</b><br>
List 2-3 most likely conditions with brief explanation for each.<br><br>

<b>⚠️ Severity Level:</b><br>
State clearly: EMERGENCY 🔴 / MODERATE 🟡 / MILD 🟢 — and explain why.<br><br>

<b>🏥 Should They See a Doctor?</b><br>
Clear advice on urgency — immediately, within 24-48 hours, or home care is fine.<br><br>

<b>💊 Immediate Steps:</b><br>
3-4 practical home steps to take right now.<br><br>

<b>🚨 Warning Signs:</b><br>
2-3 symptoms that mean they need emergency care immediately.<br><br>

Keep tone warm, clear and simple. Consider Nigerian context — mention malaria for fever symptoms where relevant."""

        try:
            response = model.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"⚠️ Error: {str(e)}. Please check your API key and try again."
            })
    st.rerun()

# ─── FEATURE CARDS ────────────────────────────────────────────────────────────
st.markdown("""
<div class="features-grid">
    <div class="feat-card">
        <div class="feat-icon">🔒</div>
        <div class="feat-title">Private & Secure</div>
        <div class="feat-desc">Your symptoms are never stored or shared. Every conversation is completely confidential.</div>
    </div>
    <div class="feat-card">
        <div class="feat-icon">🌍</div>
        <div class="feat-title">Nigeria-Aware</div>
        <div class="feat-desc">Considers tropical diseases common in Nigeria like malaria, typhoid, and dengue fever.</div>
    </div>
    <div class="feat-card">
        <div class="feat-icon">⚡</div>
        <div class="feat-title">Available 24/7</div>
        <div class="feat-desc">Get instant health guidance at any time — even at 3am when clinics are closed.</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-logo">🏥 Medi<span>Check</span> AI</div>
    <div class="footer-text">Built for Nigerians · Powered by Google Gemini · Always free</div>
    <div class="footer-text">⚠️ Not a substitute for professional medical advice. Always see a real doctor.</div>
</div>
""", unsafe_allow_html=True)
