# import streamlit as st
# from ultralytics import YOLO
# from PIL import Image
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
# import cv2
# import hashlib
# import json
# import os
# from datetime import datetime

# # Configure page
# st.set_page_config(
#     page_title="LUPUS AI Diagnostic",
#     page_icon="🏥",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # Custom CSS for production-ready minimal UI
# st.markdown("""
# <style>
#     /* Import Google Fonts */
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
#     /* Global Styles */
#     .stApp {
#         font-family: 'Inter', sans-serif;
#         background-color: #fafafa;
#     }
    
#     /* Header Styles */
#     .main-header {
#         font-size: 2.2rem;
#         font-weight: 600;
#         color: #1a1a1a;
#         text-align: center;
#         margin-bottom: 0.5rem;
#         letter-spacing: -0.02em;
#     }
    
#     .subtitle {
#         font-size: 1.1rem;
#         color: #6b7280;
#         text-align: center;
#         margin-bottom: 3rem;
#         font-weight: 400;
#     }
    
#     /* Card Styles */
#     .card {
#         background: white;
#         border-radius: 12px;
#         padding: 2rem;
#         box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
#         border: 1px solid #e5e7eb;
#         margin-bottom: 1.5rem;
#     }
    
#     .upload-card {
#         border: 2px dashed #d1d5db;
#         background: #f9fafb;
#         text-align: center;
#         padding: 3rem 2rem;
#         border-radius: 12px;
#         transition: all 0.3s ease;
#     }
    
#     .upload-card:hover {
#         border-color: #6366f1;
#         background: #f8faff;
#     }
    
#     /* Result Styles */
#     .result-positive {
#         background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
#         border: 1px solid #fecaca;
#         border-left: 4px solid #ef4444;
#         border-radius: 8px;
#         padding: 1.5rem;
#         margin: 1rem 0;
#     }
    
#     .result-negative {
#         background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
#         border: 1px solid #bbf7d0;
#         border-left: 4px solid #22c55e;
#         border-radius: 8px;
#         padding: 1.5rem;
#         margin: 1rem 0;
#     }
    
#     .result-title {
#         font-size: 1.3rem;
#         font-weight: 600;
#         margin-bottom: 0.5rem;
#         color: #1a1a1a;
#     }
    
#     .confidence-score {
#         font-size: 1.1rem;
#         font-weight: 500;
#         margin-bottom: 0.8rem;
#     }
    
#     .recommendation {
#         color: #4b5563;
#         font-size: 0.95rem;
#         line-height: 1.5;
#     }
    
#     /* Auth Styles */
#     .auth-container {
#         max-width: 400px;
#         margin: 0 auto;
#         padding: 2rem;
#         background: white;
#         border-radius: 12px;
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
#         border: 1px solid #e5e7eb;
#     }
    
#     .auth-header {
#         text-align: center;
#         margin-bottom: 2rem;
#     }
    
#     .auth-title {
#         font-size: 1.8rem;
#         font-weight: 600;
#         color: #1a1a1a;
#         margin-bottom: 0.5rem;
#     }
    
#     .auth-subtitle {
#         color: #6b7280;
#         font-size: 0.95rem;
#     }
    
#     /* Button Styles */
#     .stButton > button {
#         background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
#         color: white;
#         border: none;
#         border-radius: 8px;
#         padding: 0.75rem 1.5rem;
#         font-weight: 500;
#         font-size: 0.95rem;
#         transition: all 0.3s ease;
#         width: 100%;
#     }
    
#     .stButton > button:hover {
#         background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
#         transform: translateY(-1px);
#         box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
#     }
    
#     /* Input Styles */
#     .stTextInput > div > div > input {
#         border: 1px solid #d1d5db;
#         border-radius: 6px;
#         padding: 0.75rem;
#         font-size: 0.95rem;
#     }
    
#     .stTextInput > div > div > input:focus {
#         border-color: #6366f1;
#         box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
#     }
    
#     /* Warning and Info Styles */
#     .warning-box {
#         background: #fef3cd;
#         border: 1px solid #fde68a;
#         border-left: 4px solid #f59e0b;
#         border-radius: 6px;
#         padding: 1rem;
#         margin: 1rem 0;
#     }
    
#     .info-box {
#         background: #eff6ff;
#         border: 1px solid #bfdbfe;
#         border-left: 4px solid #3b82f6;
#         border-radius: 6px;
#         padding: 1rem;
#         margin: 1rem 0;
#     }
    
#     /* Stats Card */
#     .stats-card {
#         background: white;
#         border-radius: 8px;
#         padding: 1.5rem;
#         text-align: center;
#         border: 1px solid #e5e7eb;
#     }
    
#     .stats-number {
#         font-size: 2rem;
#         font-weight: 700;
#         color: #6366f1;
#         margin-bottom: 0.5rem;
#     }
    
#     .stats-label {
#         color: #6b7280;
#         font-size: 0.9rem;
#         font-weight: 500;
#     }
    
#     /* Hide Streamlit elements */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}
    
#     .block-container {
#         padding-top: 2rem;
#         padding-bottom: 2rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Authentication functions
# def load_users():
#     """Load users from JSON file"""
#     if os.path.exists('users.json'):
#         with open('users.json', 'r') as f:
#             return json.load(f)
#     return {}

# def save_users(users):
#     """Save users to JSON file"""
#     with open('users.json', 'w') as f:
#         json.dump(users, f)

# def hash_password(password):
#     """Hash password using SHA256"""
#     return hashlib.sha256(password.encode()).hexdigest()

# def authenticate_user(username, password):
#     """Authenticate user"""
#     users = load_users()
#     if username in users:
#         return users[username]['password'] == hash_password(password)
#     return False

# def register_user(username, password, email):
#     """Register new user"""
#     users = load_users()
#     if username in users:
#         return False, "Username already exists"
    
#     users[username] = {
#         'password': hash_password(password),
#         'email': email,
#         'created_at': datetime.now().isoformat(),
#         'predictions_count': 0
#     }
#     save_users(users)
#     return True, "User registered successfully"

# def update_user_stats(username):
#     """Update user prediction count"""
#     users = load_users()
#     if username in users:
#         users[username]['predictions_count'] += 1
#         save_users(users)

# # Model functions
# @st.cache_resource
# def load_model(model_path):
#     """Load the trained YOLO model"""
#     try:
#         model = YOLO(model_path)
#         return model
#     except Exception as e:
#         st.error(f"Error loading model: {str(e)}")
#         return None

# def predict_image(model, image):
#     """Make prediction on the image using YOLO classification"""
#     try:
#         results = model(image)
#         result = results[0]
        
#         if hasattr(result, 'probs') and result.probs is not None:
#             top1_id = result.probs.top1
#             top1_conf = float(result.probs.top1conf)
#             all_probs = result.probs.data.cpu().numpy()
#             class_names = list(model.names.values())
            
#             return top1_id, all_probs, class_names, top1_conf
#         else:
#             return 0, np.array([0.5, 0.5]), ['LUPUS', 'Non-LUPUS'], 0.5
            
#     except Exception as e:
#         st.error(f"Error during prediction: {str(e)}")
#         return 0, np.array([0.5, 0.5]), ['LUPUS', 'Non-LUPUS'], 0.5

# def create_confidence_chart(probabilities, class_names):
#     """Create a minimal confidence chart"""
#     colors = ['#6366f1' if i == np.argmax(probabilities) else '#e5e7eb' for i in range(len(probabilities))]
    
#     fig = go.Figure(data=[
#         go.Bar(
#             x=class_names,
#             y=probabilities * 100,
#             marker_color=colors,
#             text=[f'{prob:.1f}%' for prob in probabilities * 100],
#             textposition='auto',
#             textfont=dict(color='white', weight='bold'),
#             hovertemplate='<b>%{x}</b><br>Confidence: %{y:.1f}%<extra></extra>'
#         )
#     ])
    
#     fig.update_layout(
#         title=dict(
#             text="Prediction Confidence",
#             font=dict(size=18, weight='bold', color='#1a1a1a'),
#             x=0.5
#         ),
#         xaxis_title="",
#         yaxis_title="Confidence (%)",
#         yaxis_range=[0, 100],
#         template="plotly_white",
#         height=350,
#         showlegend=False,
#         margin=dict(l=40, r=40, t=60, b=40),
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)'
#     )
    
#     fig.update_xaxes(tickfont=dict(size=12, color='#4b5563'))
#     fig.update_yaxes(tickfont=dict(size=12, color='#4b5563'))
    
#     return fig

# # Authentication UI
# def show_auth():
#     """Show authentication page"""
#     st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
#     # Tab selection
#     auth_mode = st.radio("", ["Login", "Sign Up"], horizontal=True, key="auth_mode")
    
#     if auth_mode == "Login":
#         st.markdown('''
#         <div class="auth-header">
#             <div class="auth-title">Welcome Back</div>
#             <div class="auth-subtitle">Sign in to access LUPUS AI Diagnostic</div>
#         </div>
#         ''', unsafe_allow_html=True)
        
#         with st.form("login_form"):
#             username = st.text_input("Username", placeholder="Enter your username")
#             password = st.text_input("Password", type="password", placeholder="Enter your password")
#             login_button = st.form_submit_button("Sign In")
            
#             if login_button:
#                 if authenticate_user(username, password):
#                     st.session_state.authenticated = True
#                     st.session_state.username = username
#                     st.rerun()
#                 else:
#                     st.error("❌ Invalid username or password")
    
#     else:  # Sign Up
#         st.markdown('''
#         <div class="auth-header">
#             <div class="auth-title">Create Account</div>
#             <div class="auth-subtitle">Join LUPUS AI Diagnostic platform</div>
#         </div>
#         ''', unsafe_allow_html=True)
        
#         with st.form("signup_form"):
#             username = st.text_input("Username", placeholder="Choose a username")
#             email = st.text_input("Email", placeholder="Enter your email")
#             password = st.text_input("Password", type="password", placeholder="Create a password")
#             confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
#             signup_button = st.form_submit_button("Create Account")
            
#             if signup_button:
#                 if not username or not email or not password:
#                     st.error("❌ Please fill in all fields")
#                 elif password != confirm_password:
#                     st.error("❌ Passwords do not match")
#                 elif len(password) < 6:
#                     st.error("❌ Password must be at least 6 characters")
#                 else:
#                     success, message = register_user(username, password, email)
#                     if success:
#                         st.success("✅ Account created successfully! Please login.")
#                     else:
#                         st.error(f"❌ {message}")
    
#     st.markdown('</div>', unsafe_allow_html=True)

# # Main application
# def show_main_app():
#     """Show main application"""
#     # Header
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         st.markdown('<h1 class="main-header">🏥 LUPUS AI Diagnostic</h1>', unsafe_allow_html=True)
#         st.markdown('<p class="subtitle">Advanced AI-powered medical image analysis for LUPUS detection</p>', unsafe_allow_html=True)
    
#     # User info and logout
#     with st.sidebar:
#         st.markdown("### 👤 User Profile")
#         st.write(f"**Username:** {st.session_state.username}")
        
#         users = load_users()
#         if st.session_state.username in users:
#             predictions_count = users[st.session_state.username].get('predictions_count', 0)
#             st.markdown(f'''
#             <div class="stats-card">
#                 <div class="stats-number">{predictions_count}</div>
#                 <div class="stats-label">Predictions Made</div>
#             </div>
#             ''', unsafe_allow_html=True)
        
#         st.markdown("---")
        
#         # Model configuration
#         st.markdown("### ⚙️ Model Settings")
#         model_path = st.text_input("Model Path", value="best.pt", help="Path to your trained model file")
#         confidence_threshold = st.slider("Confidence Threshold (%)", 50, 99, 70)
        
#         st.markdown("---")
        
#         if st.button("🚪 Logout"):
#             for key in list(st.session_state.keys()):
#                 del st.session_state[key]
#             st.rerun()
    
#     # Load model
#     model = load_model(model_path)
    
#     if model is None:
#         st.error("❌ Could not load the model. Please check the model path.")
#         return
    
#     # Main content
#     col1, col2 = st.columns([1, 1], gap="large")
    
#     with col1:
#         st.markdown('<div class="card">', unsafe_allow_html=True)
#         st.markdown("### 📤 Upload Medical Image")
        
#         uploaded_file = st.file_uploader(
#             "",
#             type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
#             help="Upload a medical image for LUPUS classification"
#         )
        
#         if uploaded_file is not None:
#             image = Image.open(uploaded_file)
#             st.image(image, caption="Uploaded Image", use_column_width=True)
            
#             # Image details
#             st.markdown(f'''
#             <div class="info-box">
#                 <strong>Image Details:</strong><br>
#                 📁 {uploaded_file.name}<br>
#                 📏 {image.size[0]} × {image.size[1]} pixels<br>
#                 🖼️ {image.format} format
#             </div>
#             ''', unsafe_allow_html=True)
        
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     with col2:
#         st.markdown('<div class="card">', unsafe_allow_html=True)
#         st.markdown("### 🔍 Analysis Results")
        
#         if uploaded_file is not None:
#             with st.spinner("🔬 Analyzing image..."):
#                 try:
#                     prediction, probabilities, class_names, confidence = predict_image(model, image)
#                     predicted_class = class_names[prediction]
                    
#                     # Update user stats
#                     update_user_stats(st.session_state.username)
                    
#                     # Display results
#                     if predicted_class == 'LUPUS':
#                         st.markdown(f'''
#                         <div class="result-positive">
#                             <div class="result-title">⚠️ LUPUS Detected</div>
#                             <div class="confidence-score">Confidence: {confidence*100:.1f}%</div>
#                             <div class="recommendation">
#                                 <strong>Recommendation:</strong> Please consult with a medical professional 
#                                 immediately for proper diagnosis and treatment planning.
#                             </div>
#                         </div>
#                         ''', unsafe_allow_html=True)
#                     else:
#                         st.markdown(f'''
#                         <div class="result-negative">
#                             <div class="result-title">✅ No LUPUS Detected</div>
#                             <div class="confidence-score">Confidence: {confidence*100:.1f}%</div>
#                             <div class="recommendation">
#                                 <strong>Note:</strong> This is a screening tool. Regular medical 
#                                 checkups are still recommended for overall health monitoring.
#                             </div>
#                         </div>
#                         ''', unsafe_allow_html=True)
                    
#                     # Low confidence warning
#                     if confidence*100 < confidence_threshold:
#                         st.markdown(f'''
#                         <div class="warning-box">
#                             ⚠️ <strong>Low Confidence Alert:</strong> The prediction confidence 
#                             ({confidence*100:.1f}%) is below the threshold. Consider retaking 
#                             the image or seeking additional medical opinion.
#                         </div>
#                         ''', unsafe_allow_html=True)
                    
#                     # Confidence chart
#                     fig = create_confidence_chart(probabilities, class_names)
#                     st.plotly_chart(fig, use_container_width=True)
                    
#                     # Detailed results in expander
#                     with st.expander("📊 Detailed Analysis"):
#                         st.markdown("**Class Probabilities:**")
#                         for class_name, prob in zip(class_names, probabilities):
#                             st.write(f"• {class_name}: {prob*100:.2f}%")
                        
#                         st.markdown(f"""
#                         **Analysis Summary:**
#                         - Predicted Class: {predicted_class}
#                         - Confidence Score: {confidence*100:.2f}%
#                         - Model Classes: {', '.join(class_names)}
#                         - Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#                         """)
                
#                 except Exception as e:
#                     st.error(f"❌ Analysis failed: {str(e)}")
#         else:
#             st.markdown('''
#             <div class="upload-card">
#                 <h3>👆 Upload an Image to Start</h3>
#                 <p>Select a medical image from your device to begin the AI analysis.</p>
#             </div>
#             ''', unsafe_allow_html=True)
        
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     # Footer disclaimer
#     st.markdown("---")
#     st.markdown('''
#     <div style="text-align: center; color: #6b7280; padding: 2rem; background: white; border-radius: 8px; margin-top: 2rem;">
#         <p><strong>⚠️ Medical Disclaimer:</strong> This AI diagnostic tool is designed for screening and educational purposes only. 
#         It should not replace professional medical consultation, diagnosis, or treatment. Always seek advice from qualified 
#         healthcare professionals for any medical concerns.</p>
#         <p style="margin-top: 1rem; font-size: 0.9rem;">
#             <em>Powered by YOLO AI • Built with Streamlit • Version 1.0</em>
#         </p>
#     </div>
#     ''', unsafe_allow_html=True)

# # Main application logic
# def main():
#     # Initialize session state
#     if 'authenticated' not in st.session_state:
#         st.session_state.authenticated = False
    
#     # Show appropriate page
#     if not st.session_state.authenticated:
#         show_auth()
#     else:
#         show_main_app()

# if __name__ == "__main__":
#     main()

import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import cv2
import hashlib
import json
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="LUPUS Image Classification",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS for modern, minimal UI
st.markdown("""
<style>
    /* Global Styles */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    /* Header */
    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 0;
        margin: -2rem -2rem 3rem -2rem;
        color: white;
        text-align: center;
    }
    
    .app-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .app-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Cards */
    .card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 2rem;
    }
    
    .card-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #f3f4f6;
    }
    
    /* Auth Forms */
    .auth-container {
        max-width: 400px;
        margin: 2rem auto;
        background: white;
        padding: 3rem 2rem;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;

    }
    /* Auth Forms */
    .auth-containerr {
        max-width: 700px;
        margin: 2rem auto;
        background: white;
        padding: 3rem 2rem;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
        
    }
    .auth-title {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .auth-switch {
        text-align: center;
        margin-top: 2rem;
        color: #6b7280;
    }
    
    .auth-switch a {
        color: #667eea;
        text-decoration: none;
        font-weight: 500;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s;
    }
    
    .stButton > buttonransition: all 0.3s ease;
    }
    
    .upload-area:ho-er {
        border-color: #667eea;
      0;
    }
    
    .result-negative {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1px solid #bbf7d0;
        border-left: 4px solid #22c55e;
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
    }
    
    .result-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .result-confidence {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .result-recommendation {
        font-size: 1rem;
        line-height: 1.6;
        opacity: 0.9;
    }
    
    /* Info boxes */
    .info-box {
        background: #f8faff;
        border: 1px solid #e0e7ff;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* User info */
    .user-info {
        background: #f9fafb;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .user-name {
        font-size: 1.2rem;
        font-weight: 600;
        color: #374151;
    }
    
    /* Navigation */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background: white;
        border-bottom: 1px solid #e5e7eb;
        margin: -2rem -2rem 0 -2rem;
        margin-bottom: 2rem;
    }
    
    .nav-brand {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-container {
            padding: 0 1rem;
        }
        .auth-container {
            margin: 1rem;
            padding: 2rem 1rem;
        }
        .card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Authentication functions
def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_users_db():
    """Initialize users database in session state"""
    if 'users_db' not in st.session_state:
        st.session_state.users_db = {}

def register_user(username, email, password):
    """Register a new user"""
    init_users_db()
    if username in st.session_state.users_db:
        return False, "Username already exists"
    if any(user['email'] == email for user in st.session_state.users_db.values()):
        return False, "Email already registered"
    
    st.session_state.users_db[username] = {
        'email': email,
        'password': hash_password(password),
        'created_at': datetime.now().isoformat()
    }
    return True, "Registration successful"

def authenticate_user(username, password):
    """Authenticate user login"""
    init_users_db()
    if username not in st.session_state.users_db:
        return False, "Username not found"
    
    stored_password = st.session_state.users_db[username]['password']
    if stored_password == hash_password(password):
        return True, "Login successful"
    return False, "Invalid password"

def logout_user():
    """Logout current user"""
    st.session_state.authenticated = False
    st.session_state.current_user = None
    st.rerun()

# Authentication UI
def show_auth_page():
    """Display authentication page"""
    st.markdown('<div class="auth-containerr"> <h1 class="auth-title">Skin Cancer Lupus Detection</h1>', unsafe_allow_html=True)

    
    # Auth mode selector
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'login'
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.markdown('<h2 class="auth-title">Welcome Back</h2>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            login_button = st.form_submit_button("Sign In", use_container_width=True)
            
            if login_button:
                if username and password:
                    success, message = authenticate_user(username, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.current_user = username
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all fields")
    
    with tab2:
        st.markdown('<h2 class="auth-title">Create Account</h2>', unsafe_allow_html=True)
        
        with st.form("register_form"):
            new_username = st.text_input("Username", placeholder="Choose a username")
            new_email = st.text_input("Email", placeholder="Enter your email")
            new_password = st.text_input("Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            register_button = st.form_submit_button("Create Account", use_container_width=True)
            
            if register_button:
                if new_username and new_email and new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("Passwords do not match")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters long")
                    else:
                        success, message = register_user(new_username, new_email, new_password)
                        if success:
                            st.success(message)
                            st.info("Please login with your new account")
                        else:
                            st.error(message)
                else:
                    st.error("Please fill in all fields")
    
    st.markdown('</div>', unsafe_allow_html=True)

@st.cache_resource
def load_model(model_path):
    """Load the trained YOLO model"""
    try:
        model = YOLO(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def predict_image(model, image):
    """Make prediction on the image using YOLO classification"""
    try:
        results = model(image)
        result = results[0]
        
        if hasattr(result, 'probs') and result.probs is not None:
            top1_id = result.probs.top1
            top1_conf = float(result.probs.top1conf)
            all_probs = result.probs.data.cpu().numpy()
            class_names = list(model.names.values())
            
            return top1_id, all_probs, class_names, top1_conf
        else:
            return 0, np.array([0.5, 0.5]), ['LUPUS', 'Non-LUPUS'], 0.5
            
    except Exception as e:
        st.error(f"Error during prediction: {str(e)}")
        return 0, np.array([0.5, 0.5]), ['LUPUS', 'Non-LUPUS'], 0.5

def create_confidence_chart(probabilities, class_names):
    """Create a confidence chart using Plotly"""
    colors = ['#ef4444' if i == np.argmax(probabilities) else '#667eea' 
              for i in range(len(probabilities))]
    
    fig = go.Figure(data=[
        go.Bar(
            x=class_names,
            y=probabilities * 100,
            marker_color=colors,
            text=[f'{prob:.1f}%' for prob in probabilities * 100],
            textposition='auto',
            marker=dict(
                line=dict(color='rgba(0,0,0,0)', width=0)
            )
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="Prediction Confidence",
            font=dict(size=16, color="#374151"),
            x=0.5
        ),
        xaxis_title="Classification",
        yaxis_title="Confidence (%)",
        yaxis_range=[0, 100],
        template="plotly_white",
        height=350,
        margin=dict(t=50, b=50, l=50, r=50),
        font=dict(color="#374151"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def show_main_app():
    """Display main application interface"""
    # Navigation bar
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<div class="nav-brand">🔬 Skin Cancer Lupus Detection</div>', unsafe_allow_html=True)

    with col2:
        if st.button("Logout", type="secondary"):
            logout_user()
    
    # User info
    st.markdown(f"""
    <div class="user-info">
        <span class="user-name">Welcome, {st.session_state.current_user}</span>
        <span style="color: #6b7280; font-size: 1.2rem;">Logged in • {datetime.now().strftime('%B %d, %Y')}</span>

    </div>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">Skin Cancer Lupus Detection</h1>
        <p class="app-subtitle">Advanced AI-powered medical image analysis for Skin Cancer Lupus detection</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Model configuration in sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        model_path = st.text_input(
            "Model Path",
            value="best.pt",
            help="Path to your trained model file"
        )
        
        confidence_threshold = st.slider(
            "Confidence Threshold (%)",
            min_value=50,
            max_value=99,
            value=70,
            help="Minimum confidence for reliable prediction"
        )
        
        st.markdown("---")
        st.markdown("""
        **About this model:**
        - YOLO architecture for medical imaging
        - Real-time LUPUS detection
        - Confidence-based predictions
        - Production-ready deployment
        """)
    
    # Load model
    model = load_model(model_path)
    
    if model is None:
        st.error("❌ Could not load the model. Please check the model path.")
        return
    
    st.success("✅ Model loaded successfully")
    
    # Main content area
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3 class="card-header">📤 Upload Medical Image</h3>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
            help="Upload a medical image for LUPUS classification"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Image information
            st.markdown(f"""
            <div class="info-box">
                <strong>Image Information:</strong><br>
                • Filename: {uploaded_file.name}<br>
                • Size: {image.size[0]} × {image.size[1]} pixels<br>
                • Format: {image.format}<br>
                • Mode: {image.mode}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3 class="card-header">🔍 Analysis Results</h3>
        """, unsafe_allow_html=True)
        
        if uploaded_file is not None:
            with st.spinner("Analyzing image..."):
                try:
                    prediction, probabilities, class_names, confidence = predict_image(model, image)
                    predicted_class = class_names[prediction]
                    
                    # Display results
                    if predicted_class == 'LUPUS':
                        st.markdown(f"""
                        <div class="result-positive">
                            <div class="result-title">⚠️ LUPUS Detected</div>
                            <div class="result-confidence">Confidence: {confidence*100:.1f}%</div>
                            <div class="result-recommendation">Please consult with a medical professional for proper diagnosis and treatment.</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="result-negative">
                            <div class="result-title">✅ No LUPUS Detected</div>
                            <div class="result-confidence">Confidence: {confidence*100:.1f}%</div>
                            <div class="result-recommendation">This is a screening tool. Regular medical checkups are still recommended.</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Confidence warning
                    if confidence*100 < confidence_threshold:
                        st.warning(f"⚠️ Low confidence prediction ({confidence*100:.1f}%). Consider getting a second opinion.")
                    
                    # Confidence chart
                    fig = create_confidence_chart(probabilities, class_names)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Detailed results
                    with st.expander("📊 Detailed Analysis"):
                        st.write("**Class Probabilities:**")
                        for class_name, prob in zip(class_names, probabilities):
                            st.write(f"• {class_name}: {prob*100:.2f}%")
                        
                        st.write(f"\n**Predicted Class:** {predicted_class}")
                        st.write(f"**Confidence Score:** {confidence*100:.2f}%")
                        st.write(f"**Model Classes:** {class_names}")
                
                except Exception as e:
                    st.error(f"❌ Error during prediction: {str(e)}")
        
        else:
            st.markdown("""
            <div style="text-align: center; padding: 3rem 1rem; color: #6b7280;">
                <h4>Ready for Analysis</h4>
                <p>Upload an image to begin the classification process</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; margin: 2rem 0;">
        <p><strong>Medical Disclaimer:</strong> This tool is for educational and screening purposes only. 
        It should not be used as a substitute for professional medical diagnosis. 
        Always consult with qualified healthcare professionals for medical concerns.</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    
    # Route based on authentication status
    if st.session_state.authenticated:
        show_main_app()
    else:
        show_auth_page()

if __name__ == "__main__":
    main()