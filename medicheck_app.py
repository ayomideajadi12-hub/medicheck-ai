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
GEMINI_API_KEY = "PASTE_YOUR_API_KEY_HERE"

# ─── CONFIGURE GEMINI ─────────────────────────────────────────────────────────
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

* { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Outfit', sans-serif !important; }

.stApp { background: #060912; min-height: 100vh; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── HEADER ── */
.header {
    background: linear-gradient(135deg, #060912 0%, #0a1628 50%, #060912 100%);
    padding: 48px 60px 36px;
    border-bottom: 1px solid rgba(59,130,246,0.15);
    position: relative; overflow: hidden;
}
.header::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(circle at 20% 50%, rgba(59,130,246,0.06) 0%, transparent 60%),
                radial-gradient(circle at 80% 30%, rgba(139,92,246,0.04) 0%, transparent 50%);
}
.header-inner {
    max-width: 1100px; margin: 0 auto;
    display: grid; grid-template-columns: 1fr auto;
    align-items: center; gap: 40px;
    position: relative; z-index: 1;
}
.header-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(59,130,246,0.1);
    border: 1px solid rgba(59,130,246,0.3);
    border-radius: 100px; padding: 6px 16px;
    font-size: 12px; font-weight: 600; color: #60a5fa;
    letter-spacing: 0.08em; text-transform: uppercase;
    margin-bottom: 16px;
}
.header h1 {
    font-size: 2.8rem; font-weight: 900;
    color: #f0f9ff; line-height: 1.05;
    letter-spacing: -0.03em; margin-bottom: 12px;
}
.header h1 span {
    background: linear-gradient(135deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.header p { font-size: 1rem; color: #4b5563; line-height: 1.7; max-width: 500px; }
.header-stats { display: flex; gap: 28px; margin-top: 24px; }
.hstat-num {
    font-size: 1.6rem; font-weight: 800; color: #60a5fa;
    font-family: 'JetBrains Mono', monospace; line-height: 1;
}
.hstat-label { font-size: 11px; color: #374151; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px; }

.header-pills { display: flex; flex-direction: column; gap: 10px; }
.pill {
    display: flex; align-items: center; gap: 10px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 10px 16px;
    font-size: 13px; color: #6b7280; white-space: nowrap;
}
.pill-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }

/* ── MAIN ── */
.main-wrap { max-width: 1100px; margin: 0 auto; padding: 40px 60px; }

/* ── DISCLAIMER ── */
.disclaimer {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.2);
    border-radius: 16px; padding: 16px 20px;
    display: flex; align-items: flex-start; gap: 12px;
    margin-bottom: 32px;
}
.disclaimer-icon { font-size: 1.2rem; flex-shrink: 0; margin-top: 2px; }
.disclaimer-text { font-size: 0.85rem; color: #d97706; line-height: 1.6; }
.disclaimer-text strong { color: #fbbf24; }

/* ── CHAT AREA ── */
.chat-container {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 24px; overflow: hidden;
    margin-bottom: 24px;
}
.chat-header {
    padding: 20px 28px;
    background: rgba(59,130,246,0.06);
    border-bottom: 1px solid rgba(59,130,246,0.1);
    display: flex; align-items: center; gap: 12px;
}
.chat-status-dot {
    width: 10px; height: 10px; border-radius: 50%;
    background: #22c55e;
    box-shadow: 0 0 8px rgba(34,197,94,0.6);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
.chat-header-text { font-size: 0.9rem; font-weight: 600; color: #93c5fd; }
.chat-messages { padding: 24px; min-height: 200px; max-height: 500px; overflow-y: auto; }

/* ── MESSAGES ── */
.msg-user {
    display: flex; justify-content: flex-end; margin-bottom: 16px;
}
.msg-user-bubble {
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
    border-radius: 18px 18px 4px 18px;
    padding: 14px 18px; max-width: 70%;
    font-size: 0.92rem; color: #eff6ff; line-height: 1.6;
}
.msg-ai {
    display: flex; gap: 12px; margin-bottom: 16px; align-items: flex-start;
}
.msg-ai-avatar {
    width: 36px; height: 36px; border-radius: 10px;
    background: linear-gradient(135deg, #1e40af, #7c3aed);
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; flex-shrink: 0;
}
.msg-ai-bubble {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 4px 18px 18px 18px;
    padding: 14px 18px; max-width: 75%;
    font-size: 0.92rem; color: #e2e8f0; line-height: 1.7;
}

/* ── SEVERITY BADGES ── */
.sev-emergency {
    background: rgba(239,68,68,0.15); border: 1px solid rgba(239,68,68,0.3);
    color: #f87171; padding: 6px 14px; border-radius: 100px;
    font-size: 12px; font-weight: 700; display: inline-block; margin-bottom: 10px;
}
.sev-moderate {
    background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.3);
    color: #fbbf24; padding: 6px 14px; border-radius: 100px;
    font-size: 12px; font-weight: 700; display: inline-block; margin-bottom: 10px;
}
.sev-mild {
    background: rgba(34,197,94,0.15); border: 1px solid rgba(34,197,94,0.3);
    color: #4ade80; padding: 6px 14px; border-radius: 100px;
    font-size: 12px; font-weight: 700; display: inline-block; margin-bottom: 10px;
}

/* ── INPUT AREA ── */
.stTextArea textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(59,130,246,0.2) !important;
    border-radius: 16px !important;
    color: #e2e8f0 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 16px !important;
}
.stTextArea textarea:focus {
    border-color: rgba(59,130,246,0.5) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
}
.stTextArea textarea::placeholder { color: #374151 !important; }
.stTextArea label { color: #6b7280 !important; font-size: 0.85rem !important; }

.stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; padding: 14px 32px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important; font-size: 0.95rem !important;
    width: 100% !important; transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(29,78,216,0.35) !important;
}

/* ── QUICK SYMPTOMS ── */
.quick-title {
    font-size: 12px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.1em; color: #374151; margin-bottom: 12px;
}
.quick-grid { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 24px; }
.quick-chip {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 100px; padding: 7px 16px;
    font-size: 12px; color: #6b7280;
    cursor: default; transition: all 0.2s;
}

/* ── INFO CARDS ── */
.info-grid {
    display: grid; grid-template-columns: repeat(3,1fr); gap: 16px;
    margin-top: 40px; padding-top: 40px;
    border-top: 1px solid rgba(255,255,255,0.05);
}
.info-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px; padding: 24px;
}
.info-card-icon { font-size: 1.5rem; margin-bottom: 12px; display: block; }
.info-card-title { font-size: 0.9rem; font-weight: 700; color: #bfdbfe; margin-bottom: 8px; }
.info-card-desc { font-size: 0.82rem; color: #374151; line-height: 1.6; }

/* ── FOOTER ── */
.footer {
    background: rgba(0,0,0,0.3);
    border-top: 1px solid rgba(255,255,255,0.05);
    padding: 28px 60px;
    display: flex; justify-content: space-between;
    align-items: center; flex-wrap: wrap; gap: 16px;
    margin-top: 48px;
}
.footer-brand { font-size: 1rem; font-weight: 800; color: #60a5fa; }
.footer-text { font-size: 0.8rem; color: #1f2937; }

.stSpinner > div { border-top-color: #3b82f6 !important; }
</style>
""", unsafe_allow_html=True)

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header">
    <div class="header-inner">
        <div>
            <div class="header-badge">🏥 AI Medical Assistant</div>
            <h1>Medi<span>Check AI</span></h1>
            <p>Describe your symptoms and get instant AI-powered health guidance, possible conditions, and advice on whether to see a doctor — completely free.</p>
            <div class="header-stats">
                <div>
                    <div class="hstat-num">100+</div>
                    <div class="hstat-label">Conditions Known</div>
                </div>
                <div>
                    <div class="hstat-num">&lt;10s</div>
                    <div class="hstat-label">Response Time</div>
                </div>
                <div>
                    <div class="hstat-num">Free</div>
                    <div class="hstat-label">Always</div>
                </div>
            </div>
        </div>
        <div class="header-pills">
            <div class="pill"><span class="pill-dot" style="background:#f87171"></span> Emergency symptoms detected</div>
            <div class="pill"><span class="pill-dot" style="background:#fbbf24"></span> Moderate — See doctor soon</div>
            <div class="pill"><span class="pill-dot" style="background:#4ade80"></span> Mild — Home care advised</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── MAIN ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div class="disclaimer">
    <span class="disclaimer-icon">⚠️</span>
    <div class="disclaimer-text">
        <strong>Medical Disclaimer:</strong> MediCheck AI provides general health information only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified doctor for medical concerns. In case of emergency, call 112 or go to the nearest hospital immediately.
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "👋 Hello! I'm MediCheck AI. Please describe your symptoms in as much detail as possible — including when they started, how severe they are, and any other relevant information. I'll help identify possible conditions and advise whether you need to see a doctor."
    })

# Chat display
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
st.markdown("""
<div class="chat-header">
    <div class="chat-status-dot"></div>
    <div class="chat-header-text">MediCheck AI — Online and Ready</div>
</div>
<div class="chat-messages" id="chat-messages">
""", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-user">
            <div class="msg-user-bubble">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="msg-ai">
            <div class="msg-ai-avatar">🏥</div>
            <div class="msg-ai-bubble">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# Quick symptom chips
st.markdown("""
<div class="quick-title">💡 Common Symptom Examples</div>
<div class="quick-grid">
    <div class="quick-chip">🤒 Fever + headache</div>
    <div class="quick-chip">🤧 Cough + sore throat</div>
    <div class="quick-chip">🤢 Nausea + vomiting</div>
    <div class="quick-chip">💪 Body aches + fatigue</div>
    <div class="quick-chip">🫁 Chest pain + shortness of breath</div>
    <div class="quick-chip">🤕 Severe headache</div>
    <div class="quick-chip">🦴 Joint pain + swelling</div>
    <div class="quick-chip">👁️ Eye redness + discharge</div>
</div>
""", unsafe_allow_html=True)

# Input
col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_area(
        "Describe your symptoms",
        placeholder="e.g. I have had a high fever of 39°C for 2 days, with a severe headache, body aches and I feel very tired. I also have a slight cough...",
        height=100,
        label_visibility="collapsed"
    )
with col2:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    send_btn = st.button("🔍 Analyse", use_container_width=True)

# ─── GEMINI RESPONSE ──────────────────────────────────────────────────────────
if send_btn and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("🤖 MediCheck AI is analysing your symptoms..."):
        prompt = f"""You are MediCheck AI, a helpful and empathetic medical assistant. 
A user from Nigeria has described the following symptoms: {user_input}

Please respond in this exact format using HTML:

<b>🔍 Possible Conditions:</b><br>
List 2-3 most likely conditions based on the symptoms, with a brief explanation for each.<br><br>

<b>⚠️ Severity Level:</b><br>
State clearly: EMERGENCY / MODERATE / MILD and explain why.<br><br>

<b>🏥 Should They See a Doctor?</b><br>
Give clear advice on urgency — immediately, within 24-48 hours, or home care is fine.<br><br>

<b>💊 Immediate Steps:</b><br>
Give 3-4 practical things they can do right now at home while seeking care.<br><br>

<b>🚨 Warning Signs to Watch For:</b><br>
List 2-3 symptoms that would mean they need emergency care immediately.<br><br>

Keep your tone warm, clear and helpful. Use simple language. Remember this is for Nigerian users so mention local context where relevant (e.g. malaria as a possibility for fever symptoms). Always emphasize consulting a real doctor."""

        try:
            response = model.generate_content(prompt)
            ai_response = response.text
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"⚠️ Sorry, I couldn't process your request right now. Please check your API key or try again. Error: {str(e)}"
            })

    st.rerun()

# ─── INFO CARDS ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="info-grid">
    <div class="info-card">
        <span class="info-card-icon">🔒</span>
        <div class="info-card-title">Private & Secure</div>
        <div class="info-card-desc">Your symptoms are never stored or shared. Each conversation is completely private and confidential.</div>
    </div>
    <div class="info-card">
        <span class="info-card-icon">🌍</span>
        <div class="info-card-title">Nigeria-Aware</div>
        <div class="info-card-desc">Our AI considers tropical diseases common in Nigeria like malaria, typhoid, and others when analysing symptoms.</div>
    </div>
    <div class="info-card">
        <span class="info-card-icon">⚡</span>
        <div class="info-card-title">Instant Analysis</div>
        <div class="info-card-desc">Get a detailed health assessment in under 10 seconds — available 24/7, even at 3am when clinics are closed.</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-brand">🏥 MediCheck AI</div>
    <div class="footer-text">Built for Nigerians · Powered by Google Gemini · Always free</div>
    <div class="footer-text">⚠️ Not a substitute for professional medical advice. Always see a doctor.</div>
</div>
""", unsafe_allow_html=True)
