import streamlit as st
import plotly.graph_objects as go
from PIL import Image
import tensorflow as tf
from datetime import datetime

from utils.helpers import (
    load_model,
    preprocess_image,
    predict,
    get_risk_level,
    recommendation,
    to_percentage,
    result_color,
    model_information
)

from utils.report import (
    generate_pdf_report
)

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="PneumoVision AI - Medical Chest X-Ray Dashboard",
    page_icon="🩻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CSS Injection - Premium Medical Dark Theme
# Combined Apple Health, Vercel, Linear, Stripe & Nothing design system
# ---------------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-dark: #0B1220;
    --sidebar-dark: #111827;
    --card-bg: #1E293B;
    --card-glass: rgba(30, 41, 59, 0.75);
    --primary-blue: #3B82F6;
    --primary-blue-glow: rgba(59, 130, 246, 0.35);
    --success-green: #22C55E;
    --success-glow: rgba(34, 197, 94, 0.35);
    --warning-amber: #F59E0B;
    --danger-red: #EF4444;
    --danger-glow: rgba(239, 68, 68, 0.35);
    --text-main: #F8FAFC;
    --text-muted: #94A3B8;
    --border-light: rgba(255, 255, 255, 0.08);
    --border-hover: rgba(59, 130, 246, 0.4);
    --radius-lg: 20px;
    --radius-md: 14px;
}

/* Global Reset */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-dark) !important;
    color: var(--text-main) !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Hide Default Streamlit Chrome */
#MainMenu, header, footer, [data-testid="stHeader"] {
    visibility: hidden !important;
    height: 0px !important;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 1400px !important;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: var(--sidebar-dark) !important;
    border-right: 1px solid var(--border-light) !important;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem !important;
}

/* Inputs & Form Labels in Sidebar */
.stTextInput label, .stNumberInput label, .stSelectbox label {
    color: var(--text-muted) !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

.stTextInput input, .stNumberInput input, div[data-baseweb="select"] > div {
    background: rgba(15, 23, 42, 0.75) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: var(--text-main) !important;
    font-size: 0.92rem !important;
    transition: all 0.2s ease !important;
}

.stTextInput input:focus, .stNumberInput input:focus, div[data-baseweb="select"]:focus-within {
    border-color: var(--primary-blue) !important;
    box-shadow: 0 0 14px var(--primary-blue-glow) !important;
}

/* Drag & Drop File Uploader */
div[data-testid="stFileUploader"] {
    background: linear-gradient(145deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%) !important;
    border: 2px dashed rgba(59, 130, 246, 0.4) !important;
    border-radius: var(--radius-lg) !important;
    padding: 2rem !important;
    backdrop-filter: blur(12px) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
}

div[data-testid="stFileUploader"]:hover {
    border-color: var(--primary-blue) !important;
    box-shadow: 0 14px 40px rgba(59, 130, 246, 0.25) !important;
    transform: translateY(-2px) !important;
}

div[data-testid="stFileUploader"] section {
    background: transparent !important;
}

/* Custom Buttons */
.stButton > button, .stDownloadButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #2563EB 0%, #3B82F6 50%, #1D4ED8 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 14px !important;
    padding: 14px 22px !important;
    font-weight: 700 !important;
    font-size: 0.98rem !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 8px 24px rgba(37, 99, 235, 0.35) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.stButton > button:hover, .stDownloadButton > button:hover {
    background: linear-gradient(135deg, #3B82F6 0%, #60A5FA 50%, #2563EB 100%) !important;
    box-shadow: 0 12px 32px rgba(59, 130, 246, 0.5) !important;
    transform: translateY(-2px) !important;
}

/* Header Banner */
.header-container {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.9) 100%);
    backdrop-filter: blur(16px);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-lg);
    padding: 24px 32px;
    margin-bottom: 28px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
}

.header-title-box {
    display: flex;
    align-items: center;
    gap: 20px;
}

.header-icon {
    font-size: 2.6rem;
    background: linear-gradient(135deg, #1E293B, #0F172A);
    padding: 12px 18px;
    border-radius: 18px;
    border: 1px solid rgba(59, 130, 246, 0.35);
    box-shadow: 0 0 24px rgba(59, 130, 246, 0.25);
}

.header-badges {
    display: flex;
    gap: 12px;
    align-items: center;
    flex-wrap: wrap;
}

.badge {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid var(--border-light);
    color: var(--text-muted);
    padding: 7px 16px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.badge-active {
    border-color: rgba(34, 197, 94, 0.4);
    color: #4ADE80;
    background: rgba(34, 197, 94, 0.1);
}

/* Glass Card Component */
.glass-card {
    background: linear-gradient(145deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.85) 100%);
    backdrop-filter: blur(16px);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-lg);
    padding: 24px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
    transition: all 0.3s ease;
    margin-bottom: 20px;
}

.glass-card:hover {
    border-color: var(--border-hover);
    transform: translateY(-2px);
    box-shadow: 0 14px 36px rgba(0, 0, 0, 0.35);
}

/* Metric Cards */
.metric-card {
    position: relative;
    background: linear-gradient(145deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: var(--radius-lg);
    padding: 22px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    height: 100%;
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: rgba(59, 130, 246, 0.4);
    box-shadow: 0 12px 32px rgba(59, 130, 246, 0.18);
}

.metric-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}

.metric-title {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.6px;
}

.metric-icon {
    font-size: 1.4rem;
    padding: 8px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
}

.metric-value {
    font-size: 1.85rem;
    font-weight: 800;
    color: var(--text-main);
    letter-spacing: -0.5px;
    margin-bottom: 4px;
}

.metric-subtext {
    font-size: 0.78rem;
    color: var(--text-muted);
}

/* Patient Summary Tile Grid */
.summary-tile {
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 14px;
    padding: 16px 20px;
    transition: all 0.2s ease;
    height: 100%;
}

.summary-tile:hover {
    border-color: rgba(59, 130, 246, 0.35);
    background: rgba(30, 41, 59, 0.55);
}

.summary-label {
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}

.summary-value {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-main);
}

/* AI Recommendation Glass Card */
.recommendation-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
    backdrop-filter: blur(16px);
    border-radius: var(--radius-lg);
    padding: 24px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    margin-bottom: 24px;
}

/* Keyframe Animations */
@keyframes pulseDot {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(34, 197, 94, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
}

@keyframes pulseDotDanger {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}

.pulse-dot-success {
    display: inline-block;
    width: 9px;
    height: 9px;
    background-color: #22C55E;
    border-radius: 50%;
    animation: pulseDot 2s infinite;
    margin-right: 8px;
}

.pulse-dot-danger {
    display: inline-block;
    width: 9px;
    height: 9px;
    background-color: #EF4444;
    border-radius: 50%;
    animation: pulseDotDanger 2s infinite;
    margin-right: 8px;
}

/* Footer */
.footer-container {
    margin-top: 40px;
    padding-top: 24px;
    border-top: 1px solid var(--border-light);
    text-align: center;
    color: var(--text-muted);
    font-size: 0.85rem;
}

.footer-badges {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-bottom: 16px;
    flex-wrap: wrap;
}

/* Custom Scrollbars */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #0B1220;
}
::-webkit-scrollbar-thumb {
    background: #1E293B;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #3B82F6;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Cached Model Initialization
# ---------------------------------------------------------

@st.cache_resource
def cached_model():
    return load_model()

model = cached_model()
_ = model(tf.zeros((1, 224, 224, 3)))


# ---------------------------------------------------------
# Top Header Banner
# ---------------------------------------------------------

st.markdown(f"""
<div class="header-container">
    <div class="header-title-box">
        <div class="header-icon">🩻</div>
        <div>
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                PneumoVision AI
            </h1>
            <p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 0.95rem; font-weight: 500;">
                AI Powered Chest X-Ray Diagnosis & Radiological Analytics
            </p>
        </div>
    </div>
    <div class="header-badges">
        <div class="badge badge-active">
            <span class="pulse-dot-success"></span> Model Active
        </div>
        <div class="badge">
            🧠 CNN v2.4 • TensorFlow
        </div>
        <div class="badge">
            📅 {datetime.now().strftime('%b %d, %Y')}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Sidebar - Patient Information Portal
# ---------------------------------------------------------

st.sidebar.markdown("""
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
    <span style="font-size: 1.5rem;">👤</span>
    <div>
        <h3 style="margin: 0; font-size: 1.1rem; font-weight: 700; color: #F8FAFC;">Patient Information</h3>
        <p style="margin: 0; font-size: 0.78rem; color: #94A3B8;">Diagnostic Metadata Portal</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Session state initialization for form reset capability
if "patient_name" not in st.session_state:
    st.session_state.patient_name = "John Doe"
if "patient_id" not in st.session_state:
    st.session_state.patient_id = "PX-89420"
if "age" not in st.session_state:
    st.session_state.age = 45
if "gender" not in st.session_state:
    st.session_state.gender = "Male"
if "hospital" not in st.session_state:
    st.session_state.hospital = "St. Jude Medical Center"
if "doctor" not in st.session_state:
    st.session_state.doctor = "Dr. Sarah Jenkins, MD"

def reset_form():
    st.session_state.patient_name = ""
    st.session_state.patient_id = ""
    st.session_state.age = 30
    st.session_state.gender = "Male"
    st.session_state.hospital = ""
    st.session_state.doctor = ""

patient_name = st.sidebar.text_input("Patient Name", key="patient_name")
patient_id = st.sidebar.text_input("Patient ID", key="patient_id")

col_sb1, col_sb2 = st.sidebar.columns(2)
with col_sb1:
    age = st.number_input("Age", min_value=1, max_value=120, key="age")
with col_sb2:
    gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="gender")

hospital = st.sidebar.text_input("Hospital", key="hospital")
doctor = st.sidebar.text_input("Doctor", key="doctor")

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Sidebar Action Buttons
if st.sidebar.button("🧹 Clear Form", use_container_width=True):
    reset_form()
    st.rerun()

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Sidebar Model Architecture Card
model_info = model_information()
with st.sidebar.expander("ℹ️ About Model Architecture", expanded=False):
    st.markdown(f"""
    <div style="font-size: 0.85rem; color: #94A3B8; line-height: 1.6;">
        <p style="margin-bottom: 6px;"><b>Architecture:</b> {model_info['Model']}</p>
        <p style="margin-bottom: 6px;"><b>Framework:</b> {model_info['Framework']}</p>
        <p style="margin-bottom: 6px;"><b>Input Dimensions:</b> {model_info['Input Size']}</p>
        <p style="margin-bottom: 0;"><b>Output Classes:</b> {', '.join(model_info['Output Classes'])}</p>
    </div>
    """, unsafe_allow_html=True)

with st.sidebar.expander("⚠️ Medical Disclaimer", expanded=False):
    st.markdown("""
    <div style="font-size: 0.8rem; color: #94A3B8; line-height: 1.5;">
        This AI system is designed strictly for decision support and research.
        It is NOT a diagnostic replacement for certified radiologists or clinical specialists.
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# Main App Body - Image Upload & Diagnostic Dashboard
# ---------------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Chest X-Ray Image",
    type=["jpg", "jpeg", "png"],
    help="Supported formats: DICOM converted JPG, JPEG, PNG. Recommended standard frontal view."
)

if not uploaded_file:
    # Large Drag & Drop Placeholder Area
    st.markdown("""
    <div style="text-align: center; padding: 48px 20px; background: linear-gradient(145deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.6) 100%); border-radius: 20px; border: 1px dashed rgba(59, 130, 246, 0.3); margin-top: 10px;">
        <div style="font-size: 3.5rem; margin-bottom: 14px;">🫁</div>
        <h3 style="margin: 0 0 8px 0; font-size: 1.3rem; font-weight: 700; color: #F8FAFC;">Upload Chest Radiograph to Begin AI Analysis</h3>
        <p style="margin: 0 0 20px 0; color: #94A3B8; font-size: 0.92rem;">
            Drag and drop a standard DICOM/X-Ray image file or click the browse button above
        </p>
        <div style="display: flex; justify-content: center; gap: 10px;">
            <span style="background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.3); color: #60A5FA; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">.JPG</span>
            <span style="background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.3); color: #60A5FA; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">.JPEG</span>
            <span style="background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.3); color: #60A5FA; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">.PNG</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    # Image uploaded - execute preprocessing & model inference
    image = Image.open(uploaded_file).convert("RGB")
    processed_image = preprocess_image(image)

    with st.spinner("⚡ Running Neural Network Radiographical Analysis..."):
        result = predict(model, processed_image)

    label = result["prediction"]
    confidence = result["confidence"]
    normal_prob = result["normal_probability"]
    pneumonia_prob = result["pneumonia_probability"]
    risk = get_risk_level(pneumonia_prob)
    advice = recommendation(label)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # TOP SECTION: Image Preview + 4 Metric Cards
    # ---------------------------------------------------------
    col_left, col_right = st.columns([5, 7])

    with col_left:
        st.markdown(f"""
        <div class="glass-card" style="padding: 18px; text-align: center;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; padding: 0 4px;">
                <span style="font-size: 0.85rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">📷 Radiograph Preview</span>
                <span style="font-size: 0.75rem; background: rgba(59, 130, 246, 0.15); color: #60A5FA; padding: 3px 10px; border-radius: 10px; border: 1px solid rgba(59, 130, 246, 0.3);">{image.width} × {image.height} px</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.image(image, use_container_width=True)

    with col_right:
        # 4 Metric Cards Layout (2x2 Grid)
        m_col1, m_col2 = st.columns(2)

        # Metric 1: Prediction
        is_pneumonia = (label == "PNEUMONIA")
        pred_color = "#EF4444" if is_pneumonia else "#22C55E"
        dot_class = "pulse-dot-danger" if is_pneumonia else "pulse-dot-success"

        with m_col1:
            st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid {pred_color}; margin-bottom: 16px;">
                <div class="metric-header">
                    <span class="metric-title">Prediction Result</span>
                    <span class="metric-icon">{"⚠️" if is_pneumonia else "✅"}</span>
                </div>
                <div class="metric-value" style="color: {pred_color}; font-size: 1.6rem;">
                    <span class="{dot_class}"></span>{label}
                </div>
                <div class="metric-subtext">Deep Learning Classification</div>
            </div>
            """, unsafe_allow_html=True)

        # Metric 2: Confidence
        with m_col2:
            st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid #3B82F6; margin-bottom: 16px;">
                <div class="metric-header">
                    <span class="metric-title">Model Confidence</span>
                    <span class="metric-icon">🎯</span>
                </div>
                <div class="metric-value" style="color: #3B82F6;">
                    {to_percentage(confidence)}%
                </div>
                <div class="metric-subtext">Softmax Output Certainty</div>
            </div>
            """, unsafe_allow_html=True)

        m_col3, m_col4 = st.columns(2)

        # Metric 3: Risk Level
        risk_color = "#22C55E" if risk in ["Minimal", "Low"] else ("#F59E0B" if risk == "Moderate" else "#EF4444")
        with m_col3:
            st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid {risk_color};">
                <div class="metric-header">
                    <span class="metric-title">Risk Assessment</span>
                    <span class="metric-icon">📊</span>
                </div>
                <div class="metric-value" style="color: {risk_color};">
                    {risk}
                </div>
                <div class="metric-subtext">Pneumonia Probability Index</div>
            </div>
            """, unsafe_allow_html=True)

        # Metric 4: Analysis Status
        with m_col4:
            st.markdown("""
            <div class="metric-card" style="border-left: 4px solid #8B5CF6;">
                <div class="metric-header">
                    <span class="metric-title">Analysis Status</span>
                    <span class="metric-icon">⚡</span>
                </div>
                <div class="metric-value" style="color: #A78BFA; font-size: 1.5rem;">
                    COMPLETED
                </div>
                <div class="metric-subtext">Latency: &lt; 0.3s • Active</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # MIDDLE SECTION: Circular Confidence Gauge & Plotly Probability Chart
    # ---------------------------------------------------------
    chart_col1, chart_col2 = st.columns([5, 7])

    with chart_col1:
        st.markdown("""
        <div style="margin-bottom: 12px;">
            <h4 style="margin: 0; font-size: 1.05rem; font-weight: 700; color: #F8FAFC; display: flex; align-items: center; gap: 8px;">
                🎯 <span>Confidence Circular Gauge</span>
            </h4>
        </div>
        """, unsafe_allow_html=True)

        gauge_color = "#22C55E" if label == "NORMAL" else "#EF4444"
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=confidence * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            number={
                'suffix': "%",
                'font': {'size': 38, 'color': "#F8FAFC", 'family': 'Plus Jakarta Sans, sans-serif'}
            },
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569", 'dtick': 25},
                'bar': {'color': gauge_color, 'thickness': 0.7},
                'bgcolor': "rgba(30, 41, 59, 0.5)",
                'borderwidth': 1,
                'bordercolor': "rgba(255, 255, 255, 0.1)",
                'steps': [
                    {'range': [0, 50], 'color': 'rgba(15, 23, 42, 0.6)'},
                    {'range': [50, 80], 'color': 'rgba(30, 41, 59, 0.6)'},
                    {'range': [80, 100], 'color': 'rgba(51, 65, 85, 0.6)'}
                ],
                'threshold': {
                    'line': {'color': "#3B82F6", 'width': 4},
                    'thickness': 0.8,
                    'value': confidence * 100
                }
            }
        ))

        fig_gauge.update_layout(
            height=280,
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "#94A3B8", 'family': "Plus Jakarta Sans, sans-serif"}
        )

        st.plotly_chart(fig_gauge, use_container_width=True)

    with chart_col2:
        st.markdown("""
        <div style="margin-bottom: 12px;">
            <h4 style="margin: 0; font-size: 1.05rem; font-weight: 700; color: #F8FAFC; display: flex; align-items: center; gap: 8px;">
                📊 <span>Prediction Probability Distribution</span>
            </h4>
        </div>
        """, unsafe_allow_html=True)

        normal_pct = to_percentage(normal_prob)
        pneumonia_pct = to_percentage(pneumonia_prob)

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=["Normal X-Ray", "Pneumonia Detected"],
            y=[normal_pct, pneumonia_pct],
            text=[f"{normal_pct}%", f"{pneumonia_pct}%"],
            textposition='outside',
            textfont=dict(size=14, color="#F8FAFC", family="Plus Jakarta Sans, sans-serif"),
            marker=dict(
                color=["#22C55E", "#EF4444"],
                line=dict(color=["rgba(34, 197, 94, 0.6)", "rgba(239, 68, 68, 0.6)"], width=2),
                cornerradius=12
            ),
            width=0.45
        ))

        fig_bar.update_layout(
            height=280,
            margin=dict(l=20, r=20, t=30, b=30),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(
                title="Probability (%)",
                range=[0, max(normal_pct, pneumonia_pct) + 20],
                gridcolor='rgba(255, 255, 255, 0.06)',
                zeroline=False,
                tickfont=dict(color='#94A3B8')
            ),
            xaxis=dict(
                tickfont=dict(size=14, color='#F8FAFC', family="Plus Jakarta Sans, sans-serif"),
                showgrid=False
            ),
            showlegend=False
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # AI RECOMMENDATION GLASS CARD
    # ---------------------------------------------------------
    rec_border = "#EF4444" if is_pneumonia else "#22C55E"
    rec_icon = "🩺"

    st.markdown(f"""
    <div class="recommendation-card" style="border-left: 5px solid {rec_border};">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
            <span style="font-size: 1.6rem;">{rec_icon}</span>
            <h3 style="margin: 0; font-size: 1.2rem; font-weight: 700; color: #F8FAFC;">
                AI Diagnostic Recommendation
            </h3>
        </div>
        <p style="font-size: 0.98rem; color: #CBD5E1; line-height: 1.65; margin: 0 0 12px 0;">
            {advice}
        </p>
        <div style="font-size: 0.78rem; color: #94A3B8; background: rgba(15, 23, 42, 0.5); padding: 8px 14px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.05); display: inline-block;">
            ℹ️ Clinical correlation with radiological examination and physician assessment is recommended.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # ELEGANT PATIENT SUMMARY (NO JSON)
    # ---------------------------------------------------------
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <h3 style="margin: 0; font-size: 1.2rem; font-weight: 700; color: #F8FAFC; display: flex; align-items: center; gap: 10px;">
            📋 <span>Patient Diagnostic Summary</span>
        </h3>
    </div>
    """, unsafe_allow_html=True)

    s_col1, s_col2, s_col3 = st.columns(3)

    with s_col1:
        st.markdown(f"""
        <div class="summary-tile" style="margin-bottom: 12px;">
            <div class="summary-label">Patient Name</div>
            <div class="summary-value">{patient_name or "Not Specified"}</div>
        </div>
        <div class="summary-tile" style="margin-bottom: 12px;">
            <div class="summary-label">Patient ID</div>
            <div class="summary-value">{patient_id or "Not Specified"}</div>
        </div>
        <div class="summary-tile">
            <div class="summary-label">Hospital</div>
            <div class="summary-value">{hospital or "Not Specified"}</div>
        </div>
        """, unsafe_allow_html=True)

    with s_col2:
        st.markdown(f"""
        <div class="summary-tile" style="margin-bottom: 12px;">
            <div class="summary-label">Age</div>
            <div class="summary-value">{age} Years</div>
        </div>
        <div class="summary-tile" style="margin-bottom: 12px;">
            <div class="summary-label">Gender</div>
            <div class="summary-value">{gender}</div>
        </div>
        <div class="summary-tile">
            <div class="summary-label">Attending Doctor</div>
            <div class="summary-value">{doctor or "Not Specified"}</div>
        </div>
        """, unsafe_allow_html=True)

    with s_col3:
        st.markdown(f"""
        <div class="summary-tile" style="margin-bottom: 12px;">
            <div class="summary-label">AI Diagnosis</div>
            <div class="summary-value" style="color: {pred_color};">{label}</div>
        </div>
        <div class="summary-tile" style="margin-bottom: 12px;">
            <div class="summary-label">Confidence</div>
            <div class="summary-value" style="color: #3B82F6;">{to_percentage(confidence)}%</div>
        </div>
        <div class="summary-tile">
            <div class="summary-label">Assessed Risk</div>
            <div class="summary-value" style="color: {risk_color};">{risk}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # PDF REPORT DOWNLOAD SECTION
    # ---------------------------------------------------------
    pdf = generate_pdf_report(
        patient_name=patient_name,
        patient_id=patient_id,
        age=age,
        gender=gender,
        hospital=hospital,
        doctor=doctor,
        prediction=label,
        confidence=confidence,
        normal_probability=normal_prob,
        pneumonia_probability=pneumonia_prob
    )

    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%); border-radius: 20px; border: 1px solid rgba(255,255,255,0.08); padding: 24px; text-align: center; margin-top: 10px; margin-bottom: 30px;">
        <h4 style="margin: 0 0 8px 0; font-size: 1.1rem; color: #F8FAFC;">Generate Official Radiological PDF Report</h4>
        <p style="margin: 0 0 18px 0; color: #94A3B8; font-size: 0.88rem;">Includes full patient information, prediction probabilities, AI interpretation, and medical disclaimer.</p>
    """, unsafe_allow_html=True)

    st.download_button(
        label="📄 Download Diagnostic PDF Report",
        data=pdf,
        file_name=f"{patient_name.replace(' ', '_') if patient_name else 'Patient'}_Pneumonia_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# FOOTER SECTION
# ---------------------------------------------------------

st.markdown("""
<div class="footer-container">
    <div class="footer-badges">
        <span class="badge">⚙️ TensorFlow 2.x</span>
        <span class="badge">🐍 Python 3.10</span>
        <span class="badge">🚀 Streamlit</span>
        <span class="badge">📈 Plotly Analytics</span>
        <span class="badge">📄 ReportLab PDF</span>
    </div>
    <p style="margin: 6px 0; font-weight: 500;">
        <b>PneumoVision AI Medical Platform v2.4.0</b> • Deep Learning Radiological Decision Support
    </p>
    <p style="margin: 4px 0; font-size: 0.78rem; opacity: 0.7;">
        ⚠️ For Educational, Research & Portfolio Demonstration Purposes Only. Not approved as a primary diagnostic device.
    </p>
    <p style="margin-top: 8px; font-size: 0.75rem; color: #64748B;">
        Copyright © 2026 PneumoVision AI Healthcare Technologies. All rights reserved.
    </p>
</div>
""", unsafe_allow_html=True)