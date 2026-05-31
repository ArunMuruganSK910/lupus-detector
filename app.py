import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Lupus Detector",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .stApp { background: #ffffff; }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* NAV */
    .nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 20px 48px;
        border-bottom: 1px solid #f0f0f0;
        background: #fff;
    }
    .nav-brand {
        font-size: 18px;
        font-weight: 700;
        color: #0f0f0f;
        letter-spacing: -0.3px;
    }
    .nav-tag {
        font-size: 12px;
        font-weight: 500;
        color: #6b7280;
        background: #f3f4f6;
        padding: 4px 12px;
        border-radius: 100px;
    }

    /* HERO */
    .hero {
        padding: 80px 48px 60px;
        max-width: 700px;
    }
    .hero-label {
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #6b7280;
        margin-bottom: 16px;
    }
    .hero-title {
        font-size: 48px;
        font-weight: 700;
        color: #0f0f0f;
        line-height: 1.1;
        letter-spacing: -1.5px;
        margin-bottom: 16px;
    }
    .hero-sub {
        font-size: 16px;
        color: #6b7280;
        line-height: 1.6;
        font-weight: 400;
    }

    /* AUTH */
    .auth-wrap {
        max-width: 420px;
        margin: 0 48px;
        padding: 40px;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        background: #fafafa;
    }
    .auth-title {
        font-size: 20px;
        font-weight: 600;
        color: #0f0f0f;
        margin-bottom: 8px;
    }
    .auth-sub {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 24px;
    }

    /* MAIN */
    .main-wrap {
        padding: 48px;
    }
    .section-title {
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #9ca3af;
        margin-bottom: 16px;
    }
    .upload-box {
        border: 1.5px dashed #e5e7eb;
        border-radius: 12px;
        padding: 40px;
        text-align: center;
        background: #fafafa;
        margin-bottom: 24px;
    }
    .result-positive {
        background: #fff5f5;
        border: 1px solid #fecaca;
        border-left: 3px solid #ef4444;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .result-negative {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-left: 3px solid #22c55e;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .result-label {
        font-size: 18px;
        font-weight: 700;
        color: #0f0f0f;
        margin-bottom: 6px;
    }
    .result-conf {
        font-size: 14px;
        font-weight: 500;
        color: #4b5563;
        margin-bottom: 10px;
    }
    .result-note {
        font-size: 13px;
        color: #6b7280;
        line-height: 1.5;
    }
    .divider {
        border: none;
        border-top: 1px solid #f0f0f0;
        margin: 40px 0;
    }
    .disclaimer {
        font-size: 12px;
        color: #9ca3af;
        line-height: 1.6;
        padding: 24px 48px;
        border-top: 1px solid #f0f0f0;
    }

    /* Streamlit overrides */
    .stButton > button {
        background: #0f0f0f !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background: #374151 !important;
    }
    .stTextInput > div > div > input {
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        font-size: 14px !important;
        padding: 10px 14px !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 1px solid #e5e7eb;
        background: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 14px;
        font-weight: 500;
        color: #6b7280;
        padding: 10px 20px;
        border-bottom: 2px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        color: #0f0f0f !important;
        border-bottom: 2px solid #0f0f0f !important;
    }
</style>
""", unsafe_allow_html=True)


# ── helpers ──────────────────────────────────────────────────────────────────

def hash_pw(pw):
    import hashlib
    return hashlib.sha256(pw.encode()).hexdigest()

def init_db():
    if "users" not in st.session_state:
        st.session_state.users = {}

def register(username, email, password):
    init_db()
    if username in st.session_state.users:
        return False, "Username already taken."
    st.session_state.users[username] = {"email": email, "password": hash_pw(password)}
    return True, "Account created."

def login(username, password):
    init_db()
    u = st.session_state.users.get(username)
    if not u:
        return False, "Username not found."
    if u["password"] != hash_pw(password):
        return False, "Wrong password."
    return True, "Logged in."

@st.cache_resource
def load_model():
    return YOLO("best.pt")

def predict(model, image):
    try:
        results = model(image)
        r = results[0]
        if hasattr(r, "probs") and r.probs is not None:
            idx = r.probs.top1
            conf = float(r.probs.top1conf)
            probs = r.probs.data.cpu().numpy()
            names = list(model.names.values())
            return names[idx], conf, probs, names
    except Exception as e:
        st.error(f"Prediction error: {e}")
    return "Unknown", 0.5, np.array([0.5, 0.5]), ["LUPUS", "Non-LUPUS"]

def confidence_chart(probs, names):
    colors = ["#ef4444" if i == np.argmax(probs) else "#e5e7eb" for i in range(len(probs))]
    fig = go.Figure(go.Bar(
        x=names, y=probs * 100,
        marker_color=colors,
        text=[f"{p:.1f}%" for p in probs * 100],
        textposition="auto",
    ))
    fig.update_layout(
        yaxis_range=[0, 100],
        yaxis_title="Confidence (%)",
        xaxis_title="",
        template="plotly_white",
        height=280,
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#4b5563", size=13),
        showlegend=False,
    )
    return fig


# ── nav ──────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="nav">
    <span class="nav-brand">🔬 Lupus Detector</span>
    <span class="nav-tag">AI Medical Screening</span>
</div>
""", unsafe_allow_html=True)


# ── session state ─────────────────────────────────────────────────────────────

if "auth" not in st.session_state:
    st.session_state.auth = False
if "user" not in st.session_state:
    st.session_state.user = None


# ── auth page ─────────────────────────────────────────────────────────────────

if not st.session_state.auth:
    st.markdown("""
    <div class="hero">
        <div class="hero-label">Deep Learning · Medical Imaging</div>
        <div class="hero-title">Lupus skin detection, powered by AI.</div>
        <div class="hero-sub">Upload a dermoscopic image. Our YOLO model classifies it as Lupus or Non-Lupus in seconds.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Sign in", "Create account"])

        with tab1:
            st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
            with st.form("login"):
                u = st.text_input("Username", placeholder="your username")
                p = st.text_input("Password", type="password", placeholder="••••••••")
                if st.form_submit_button("Sign in"):
                    ok, msg = login(u, p)
                    if ok:
                        st.session_state.auth = True
                        st.session_state.user = u
                        st.rerun()
                    else:
                        st.error(msg)

        with tab2:
            st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
            with st.form("register"):
                u2 = st.text_input("Username", placeholder="choose a username")
                e2 = st.text_input("Email", placeholder="you@example.com")
                p2 = st.text_input("Password", type="password", placeholder="min 6 chars")
                p3 = st.text_input("Confirm password", type="password", placeholder="••••••••")
                if st.form_submit_button("Create account"):
                    if not all([u2, e2, p2, p3]):
                        st.error("Fill in all fields.")
                    elif p2 != p3:
                        st.error("Passwords don't match.")
                    elif len(p2) < 6:
                        st.error("Password too short.")
                    else:
                        ok, msg = register(u2, e2, p2)
                        if ok:
                            st.success("Account created — sign in now.")
                        else:
                            st.error(msg)

        st.markdown('</div>', unsafe_allow_html=True)


# ── main app ──────────────────────────────────────────────────────────────────

else:
    # top bar with logout
    col_a, col_b = st.columns([6, 1])
    with col_a:
        st.markdown(f"""
        <div style="padding: 16px 48px 0; font-size:14px; color:#6b7280;">
            Signed in as <strong style="color:#0f0f0f">{st.session_state.user}</strong>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown('<div style="padding-top:12px">', unsafe_allow_html=True)
        if st.button("Sign out"):
            st.session_state.auth = False
            st.session_state.user = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="section-title">Upload image</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "",
            type=["png", "jpg", "jpeg", "bmp", "tiff"],
            label_visibility="collapsed"
        )
        if uploaded:
            image = Image.open(uploaded)
            st.image(image, use_column_width=True)
            st.markdown(f"""
            <div style="margin-top:12px; font-size:13px; color:#9ca3af;">
                {uploaded.name} · {image.size[0]}×{image.size[1]}px
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="upload-box">
                <div style="font-size:32px; margin-bottom:12px">🖼</div>
                <div style="font-size:14px; font-weight:500; color:#4b5563">Drop an image here</div>
                <div style="font-size:12px; color:#9ca3af; margin-top:4px">PNG, JPG, JPEG, BMP, TIFF</div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">Analysis</div>', unsafe_allow_html=True)

        if uploaded:
            with st.spinner("Analyzing..."):
                model = load_model()
                label, conf, probs, names = predict(model, image)

            if label == "LUPUS":
                st.markdown(f"""
                <div class="result-positive">
                    <div class="result-label">⚠️ Lupus Detected</div>
                    <div class="result-conf">Confidence: {conf*100:.1f}%</div>
                    <div class="result-note">Please consult a dermatologist or rheumatologist for a proper diagnosis.</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-negative">
                    <div class="result-label">✅ No Lupus Detected</div>
                    <div class="result-conf">Confidence: {conf*100:.1f}%</div>
                    <div class="result-note">No lupus indicators found. Routine checkups are still recommended.</div>
                </div>""", unsafe_allow_html=True)

            st.markdown('<div class="section-title" style="margin-top:24px">Confidence breakdown</div>', unsafe_allow_html=True)
            st.plotly_chart(confidence_chart(probs, names), use_container_width=True)

            with st.expander("Detailed results"):
                for name, prob in zip(names, probs):
                    st.write(f"**{name}:** {prob*100:.2f}%")
                st.write(f"**Predicted:** {label}")
                st.write(f"**Confidence:** {conf*100:.2f}%")
                st.write(f"**Analyzed at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            st.markdown("""
            <div style="padding: 60px 0; text-align:center; color:#9ca3af;">
                <div style="font-size:40px; margin-bottom:12px">🔬</div>
                <div style="font-size:14px">Upload an image to begin analysis</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
        <strong>Medical Disclaimer:</strong> This tool is for educational and screening purposes only.
        It is not a substitute for professional medical diagnosis. Always consult a qualified healthcare provider.
    </div>""", unsafe_allow_html=True)