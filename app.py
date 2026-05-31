import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Lupus Detector",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; box-sizing: border-box; }

    html, body, .stApp {
        background: #0a0a0a !important;
        color: #fff;
        height: 100%;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        padding: 40px 24px !important;
        max-width: 640px !important;
    }

    h1, h2, h3, p, label { color: #fff !important; }

    .top-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #ef4444;
        text-align: center;
        margin-bottom: 10px;
    }
    .big-title {
        font-size: 48px;
        font-weight: 700;
        color: #fff;
        text-align: center;
        letter-spacing: -1.5px;
        line-height: 1.05;
        margin-bottom: 10px;
    }
    .big-title span { color: #ef4444; }
    .sub {
        font-size: 14px;
        color: #555;
        text-align: center;
        margin-bottom: 32px;
        line-height: 1.6;
    }

    .card {
        background: #111;
        border: 1px solid #1f1f1f;
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 16px;
    }

    .result-pos {
        background: #1a0808;
        border: 1px solid #3d1010;
        border-left: 3px solid #ef4444;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 16px;
    }
    .result-neg {
        background: #081a0e;
        border: 1px solid #103d1a;
        border-left: 3px solid #22c55e;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 16px;
    }
    .result-title { font-size: 17px; font-weight: 700; color: #fff; margin-bottom: 4px; }
    .result-conf { font-size: 13px; color: #888; margin-bottom: 6px; }
    .result-note { font-size: 12px; color: #666; line-height: 1.5; }

    .bar-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
    .bar-name { font-size: 12px; color: #666; width: 80px; flex-shrink: 0; }
    .bar-track { flex: 1; height: 4px; background: #1a1a1a; border-radius: 100px; overflow: hidden; }
    .bar-red { height: 100%; background: #ef4444; border-radius: 100px; }
    .bar-gray { height: 100%; background: #333; border-radius: 100px; }
    .bar-pct { font-size: 12px; font-weight: 600; color: #fff; width: 38px; text-align: right; }

    .sec-label {
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #444;
        margin-bottom: 12px;
    }

    .detail-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #1a1a1a;
    }
    .dk { font-size: 12px; color: #555; }
    .dv { font-size: 12px; font-weight: 500; color: #fff; }

    .disclaimer {
        font-size: 11px;
        color: #2a2a2a;
        text-align: center;
        margin-top: 16px;
        line-height: 1.6;
    }

    /* Streamlit overrides */
    .stButton > button {
        background: #fff !important;
        color: #0a0a0a !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        width: 100% !important;
        padding: 10px !important;
    }
    .stButton > button:hover { opacity: 0.85 !important; }

    .stTextInput > div > div > input {
        background: #0d0d0d !important;
        border: 1px solid #1f1f1f !important;
        border-radius: 8px !important;
        color: #fff !important;
        font-size: 14px !important;
    }
    .stTextInput > div > div > input:focus { border-color: #ef4444 !important; box-shadow: none !important; }
    .stTextInput > div > div > input::placeholder { color: #333 !important; }

    label { color: #555 !important; font-size: 13px !important; }

    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 1px solid #1f1f1f !important;
    }
    .stTabs [data-baseweb="tab"] { color: #444 !important; font-size: 14px !important; font-weight: 500 !important; }
    .stTabs [aria-selected="true"] { color: #fff !important; border-bottom: 2px solid #ef4444 !important; }
    .stTabs [data-baseweb="tab-panel"] { padding-top: 0 !important; }

    div[data-testid="stImage"] img { border-radius: 10px; width: 100%; }

    .stFileUploader section {
        background: #0d0d0d !important;
        border: 1.5px dashed #222 !important;
        border-radius: 10px !important;
    }
    .stFileUploader section p { color: #444 !important; }

    .stSpinner > div { border-top-color: #ef4444 !important; }

    .stAlert { border-radius: 8px !important; }
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


if "auth" not in st.session_state:
    st.session_state.auth = False
if "user" not in st.session_state:
    st.session_state.user = None


# ── AUTH ──────────────────────────────────────────────────────────────────────
if not st.session_state.auth:
    st.markdown("""
    <div class="top-label">Deep Learning · Medical Imaging</div>
    <div class="big-title">Detect <span>Lupus</span><br>from skin images.</div>
    <div class="sub">Upload a dermoscopic image. Our YOLO model classifies it in seconds.</div>
    """, unsafe_allow_html=True)

    with st.container():
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

    st.markdown("""
    <div class="disclaimer">
        For educational and screening purposes only.<br>Not a substitute for professional medical diagnosis.
    </div>
    """, unsafe_allow_html=True)


# ── MAIN APP ──────────────────────────────────────────────────────────────────
else:
    # Header row
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown(f"""
        <div style="margin-bottom:24px">
            <div class="top-label" style="text-align:left; margin-bottom:4px">Lupus Detector</div>
            <div style="font-size:13px; color:#444;">Signed in as <strong style="color:#fff">{st.session_state.user}</strong></div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown('<div style="padding-top:16px">', unsafe_allow_html=True)
        if st.button("Sign out"):
            st.session_state.auth = False
            st.session_state.user = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Upload
    st.markdown('<div class="sec-label">Upload image</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("", type=["png", "jpg", "jpeg", "bmp", "tiff"], label_visibility="collapsed")

    if uploaded:
        image = Image.open(uploaded)
        st.image(image, use_column_width=True)
        st.markdown(f'<div style="font-size:11px; color:#333; margin:6px 0 20px;">{uploaded.name} · {image.size[0]}×{image.size[1]}px</div>', unsafe_allow_html=True)

        # Analyze
        with st.spinner("Analyzing..."):
            model = load_model()
            label, conf, probs, names = predict(model, image)

        # Result
        if label == "LUPUS":
            st.markdown(f"""
            <div class="result-pos">
                <div class="result-title">⚠️ Lupus Detected</div>
                <div class="result-conf">Confidence: {conf*100:.1f}%</div>
                <div class="result-note">Please consult a dermatologist or rheumatologist for a proper clinical diagnosis.</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-neg">
                <div class="result-title">✅ No Lupus Detected</div>
                <div class="result-conf">Confidence: {conf*100:.1f}%</div>
                <div class="result-note">No lupus indicators found. Routine medical checkups are still recommended.</div>
            </div>""", unsafe_allow_html=True)

        # Bars
        st.markdown('<div class="sec-label">Confidence breakdown</div>', unsafe_allow_html=True)
        for name, prob in zip(names, probs):
            fill = "bar-red" if name == label else "bar-gray"
            st.markdown(f"""
            <div class="bar-row">
                <span class="bar-name">{name}</span>
                <div class="bar-track"><div class="{fill}" style="width:{prob*100:.1f}%"></div></div>
                <span class="bar-pct">{prob*100:.1f}%</span>
            </div>""", unsafe_allow_html=True)

        # Details
        st.markdown(f"""
        <div style="margin-top:20px">
            <div class="sec-label">Details</div>
            <div class="detail-row"><span class="dk">Predicted class</span><span class="dv">{label}</span></div>
            <div class="detail-row"><span class="dk">Model</span><span class="dv">YOLOv8 classifier</span></div>
            <div class="detail-row"><span class="dk">Analyzed at</span><span class="dv">{datetime.now().strftime('%Y-%m-%d %H:%M')}</span></div>
        </div>""", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="text-align:center; padding:60px 0; color:#2a2a2a;">
            <div style="font-size:40px; margin-bottom:10px">🔬</div>
            <div style="font-size:14px">Upload an image to begin analysis</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
        Medical disclaimer: For educational and screening purposes only.<br>
        Not a substitute for professional medical diagnosis.
    </div>
    """, unsafe_allow_html=True)