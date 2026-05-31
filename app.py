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

    .stApp {
        background: #0a0a0a !important;
        color: #ffffff;
    }

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
        padding: 28px 96px;
        border-bottom: 1px solid #1f1f1f;
        background: #0a0a0a;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    .nav-brand {
        font-size: 16px;
        font-weight: 600;
        color: #ffffff;
        letter-spacing: -0.2px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .nav-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #ef4444;
        display: inline-block;
    }
    .nav-tag {
        font-size: 11px;
        font-weight: 500;
        color: #555;
        background: #141414;
        border: 1px solid #1f1f1f;
        padding: 4px 12px;
        border-radius: 100px;
        letter-spacing: 0.05em;
    }

    /* HERO */
    .hero {
        padding: 140px 96px 100px;
        border-bottom: 1px solid #1f1f1f;
    }
    .hero-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #ef4444;
        margin-bottom: 20px;
    }
    .hero-title {
        font-size: 64px;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.0;
        letter-spacing: -2px;
        margin-bottom: 20px;
        max-width: 700px;
    }
    .hero-title span { color: #ef4444; }
    .hero-sub {
        font-size: 16px;
        color: #555;
        line-height: 1.6;
        max-width: 500px;
    }

    /* AUTH */
    .auth-wrap {
        max-width: 400px;
        margin: 0 96px 80px;
        padding: 32px;
        border: 1px solid #1f1f1f;
        border-radius: 16px;
        background: #111111;
    }
    .auth-title {
        font-size: 18px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 6px;
    }
    .auth-sub {
        font-size: 13px;
        color: #555;
        margin-bottom: 24px;
    }

    /* MAIN */
    .main-wrap { padding: 72px 96px; }

    .section-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #444;
        margin-bottom: 16px;
    }

    .card {
        background: #111111;
        border: 1px solid #1f1f1f;
        border-radius: 16px;
        padding: 24px;
    }

    .upload-empty {
        border: 1.5px dashed #222;
        border-radius: 12px;
        padding: 48px 24px;
        text-align: center;
        background: #0d0d0d;
    }
    .upload-empty-icon { font-size: 36px; margin-bottom: 12px; color: #333; }
    .upload-empty-title { font-size: 14px; font-weight: 500; color: #444; margin-bottom: 4px; }
    .upload-empty-sub { font-size: 12px; color: #333; }

    .result-positive {
        background: #1a0808;
        border: 1px solid #3d1010;
        border-left: 3px solid #ef4444;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .result-negative {
        background: #081a0e;
        border: 1px solid #103d1a;
        border-left: 3px solid #22c55e;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .result-label { font-size: 18px; font-weight: 700; color: #ffffff; margin-bottom: 6px; }
    .result-conf { font-size: 13px; color: #888; margin-bottom: 8px; }
    .result-note { font-size: 13px; color: #666; line-height: 1.5; }

    .bar-row { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
    .bar-name { font-size: 13px; color: #666; width: 90px; flex-shrink: 0; }
    .bar-track { flex: 1; height: 4px; background: #1a1a1a; border-radius: 100px; overflow: hidden; }
    .bar-fill-red { height: 100%; background: #ef4444; border-radius: 100px; }
    .bar-fill-gray { height: 100%; background: #333; border-radius: 100px; }
    .bar-pct { font-size: 13px; font-weight: 600; color: #ffffff; width: 45px; text-align: right; }

    .detail-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #1a1a1a; }
    .detail-key { font-size: 13px; color: #555; }
    .detail-val { font-size: 13px; font-weight: 500; color: #ffffff; }

    .disclaimer {
        font-size: 12px;
        color: #333;
        line-height: 1.6;
        padding: 28px 96px;
        border-top: 1px solid #1a1a1a;
    }

    /* Streamlit overrides for dark */
    .stButton > button {
        background: #ffffff !important;
        color: #0a0a0a !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        width: 100% !important;
        transition: opacity 0.2s !important;
    }
    .stButton > button:hover { opacity: 0.85 !important; }

    .stTextInput > div > div > input {
        background: #0d0d0d !important;
        border: 1px solid #1f1f1f !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-size: 14px !important;
        padding: 10px 14px !important;
    }
    .stTextInput > div > div > input::placeholder { color: #444 !important; }
    .stTextInput > div > div > input:focus { border-color: #ef4444 !important; }

    .stFileUploader {
        background: #0d0d0d !important;
        border: 1.5px dashed #222 !important;
        border-radius: 12px !important;
    }

    label { color: #666 !important; font-size: 13px !important; }

    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 1px solid #1f1f1f !important;
        gap: 0;
    }
    .stTabs [data-baseweb="tab"] {
        color: #444 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        padding: 10px 20px !important;
    }
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 2px solid #ef4444 !important;
    }
    .stTabs [data-baseweb="tab-panel"] { padding: 0 !important; }

    .stSpinner > div { border-top-color: #ef4444 !important; }

    div[data-testid="stImage"] img { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)


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


# NAV
st.markdown("""
<div class="nav">
    <div class="nav-brand">
        <span class="nav-dot"></span>
        Lupus Detector
    </div>
    <span class="nav-tag">AI · Medical Screening</span>
</div>
""", unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth = False
if "user" not in st.session_state:
    st.session_state.user = None


# AUTH PAGE
if not st.session_state.auth:
    st.markdown("""
    <div class="hero">
        <div class="hero-label">Deep Learning · Medical Imaging</div>
        <div class="hero-title">Detect <span>Lupus</span><br>from skin images.</div>
        <div class="hero-sub">Upload a dermoscopic image. Our YOLO model detects Lupus in seconds with high confidence.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Sign in", "Create account"])

        with tab1:
            st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
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
            st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
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


# MAIN APP
else:
    col_a, col_b = st.columns([6, 1])
    with col_a:
        st.markdown(f"""
        <div style="padding: 16px 96px 0; font-size:13px; color:#444;">
            Signed in as <strong style="color:#ffffff">{st.session_state.user}</strong>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown('<div style="padding-top:10px">', unsafe_allow_html=True)
        if st.button("Sign out"):
            st.session_state.auth = False
            st.session_state.user = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="section-label">Upload image</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "",
            type=["png", "jpg", "jpeg", "bmp", "tiff"],
            label_visibility="collapsed"
        )
        if uploaded:
            image = Image.open(uploaded)
            st.image(image, use_column_width=True)
            st.markdown(f"""
            <div style="margin-top:10px; font-size:12px; color:#444;">
                {uploaded.name} &nbsp;·&nbsp; {image.size[0]}×{image.size[1]}px
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="upload-empty">
                <div class="upload-empty-icon">🔬</div>
                <div class="upload-empty-title">Drop a skin image here</div>
                <div class="upload-empty-sub">PNG · JPG · JPEG · BMP · TIFF</div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-label">Analysis</div>', unsafe_allow_html=True)

        if uploaded:
            with st.spinner("Analyzing..."):
                model = load_model()
                label, conf, probs, names = predict(model, image)

            if label == "LUPUS":
                st.markdown(f"""
                <div class="result-positive">
                    <div class="result-label">⚠️ Lupus Detected</div>
                    <div class="result-conf">Confidence: {conf*100:.1f}%</div>
                    <div class="result-note">Please consult a dermatologist or rheumatologist for a proper clinical diagnosis.</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-negative">
                    <div class="result-label">✅ No Lupus Detected</div>
                    <div class="result-conf">Confidence: {conf*100:.1f}%</div>
                    <div class="result-note">No lupus indicators found. Routine medical checkups are still recommended.</div>
                </div>""", unsafe_allow_html=True)

            st.markdown('<div class="section-label" style="margin-top:20px">Confidence</div>', unsafe_allow_html=True)
            for name, prob in zip(names, probs):
                fill_class = "bar-fill-red" if name == label else "bar-fill-gray"
                st.markdown(f"""
                <div class="bar-row">
                    <span class="bar-name">{name}</span>
                    <div class="bar-track"><div class="{fill_class}" style="width:{prob*100:.1f}%"></div></div>
                    <span class="bar-pct">{prob*100:.1f}%</span>
                </div>""", unsafe_allow_html=True)

            st.markdown(f"""
            <div style="margin-top:24px">
                <div class="section-label">Details</div>
                <div class="detail-row"><span class="detail-key">Predicted class</span><span class="detail-val">{label}</span></div>
                <div class="detail-row"><span class="detail-key">Model</span><span class="detail-val">YOLOv8 classifier</span></div>
                <div class="detail-row"><span class="detail-key">Analyzed at</span><span class="detail-val">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span></div>
            </div>""", unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style="padding:80px 0; text-align:center; color:#333;">
                <div style="font-size:40px; margin-bottom:12px">🔬</div>
                <div style="font-size:14px">Upload an image to begin analysis</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
        Medical disclaimer: This tool is for educational and screening purposes only.
        Not a substitute for professional medical diagnosis. Always consult a qualified healthcare provider.
    </div>""", unsafe_allow_html=True)