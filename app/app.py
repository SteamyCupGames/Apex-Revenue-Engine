import streamlit as st
import joblib
import pandas as pd
import numpy as np
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.add_vertical_space import add_vertical_space

# ==========================================
# 1. CONFIGURACIÓN Y ESTILOS (ONE-PAGER)
# ==========================================
st.set_page_config(
    page_title="Olist PRM | AI Sales Intelligence",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        header {visibility: hidden;}
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
        }
        .section-header {
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.85rem;
            color: #475569 !important;
            margin-bottom: 8px;
            margin-top: 5px;
        }
        [data-testid="stMetricValue"] {
            color: #1E3A8A !important;
            font-size: 2rem !important;
            font-weight: 800 !important;
        }
        [data-testid="stMetricLabel"] {
            color: #334155 !important;
            font-weight: 600 !important;
        }
        .strategy-container {
            background-color: #F8FAFC;
            border-radius: 12px;
            padding: 15px;
            border: 1px solid #E2E8F0;
            border-left: 6px solid;
            margin-bottom: 10px;
        }
        .bench-box {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        .bench-label {
            font-size: 0.75rem;
            color: #64748B;
            display: block;
            margin-bottom: 2px;
        }
        .bench-value {
            font-size: 1.1rem;
            font-weight: 700;
            color: #1E293B;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CARGA DE ASSETS
# ==========================================
@st.cache_resource
def load_assets():
    path = 'C:\\Users\\User\\Desktop\\Software y Clases\\BigData\\OList\\olist-project-sa\\Model\\'
    clf = joblib.load(f'{path}lead_scoring_rf_model.joblib')
    reg = joblib.load(f'{path}ltv_regressor_model.joblib')
    features = joblib.load(f'{path}model_features.joblib')
    
    logistics_db = {
        'watches': {'days': 12, 'risk': 'High', 'score': 3.8},
        'health_beauty': {'days': 7, 'risk': 'Low', 'score': 4.5},
        'audio_video_electronics': {'days': 10, 'risk': 'Medium', 'score': 4.1},
        'household_utilities': {'days': 9, 'risk': 'Low', 'score': 4.3},
        'construction_tools': {'days': 11, 'risk': 'Medium', 'score': 4.0},
        'other': {'days': 9, 'risk': 'Standard', 'score': 4.2}
    }
    return clf, reg, features, logistics_db

try:
    clf_model, reg_model, model_features, logistics_db = load_assets()
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

# ==========================================
# 3. SIDEBAR (CONTROLES)
# ==========================================
with st.sidebar:
    st.markdown("### ⚡ Olist PRM")
    origin = st.selectbox("Source Channel", ['organic_search', 'paid_search', 'social', 'unknown', 'email', 'other'])
    segment = st.selectbox("Segment", ['watches', 'health_beauty', 'audio_video_electronics', 'household_utilities', 'construction_tools', 'other'])
    lead_type = st.selectbox("Lead Type", ['online_medium', 'online_big', 'offline', 'industry', 'not_qualified'])
    
    # --- CATALOG SIZE CON ETIQUETAS DINÁMICAS ---
    catalog_size = st.slider("Catalog Size (SKUs)", 1, 1000, 50)
    
    if catalog_size < 50:
        shop_type = "Boutique / Niche 💎"
    elif catalog_size < 300:
        shop_type = "Consolidated Store 🛍️"
    else:
        shop_type = "Large Scale Distributor 🏢"
    
    st.markdown(f"**Inventory Profile:** {shop_type}")
    
    # --- MULTIPLICADOR AGRESIVO ---
    # Escala: 1 SKU = 1.0x | 1000 SKUs = ~2.5x impacto
    upsell_multiplier = 1 + (catalog_size / 650)

# ==========================================
# 4. MOTOR DE INFERENCIA
# ==========================================
input_df = pd.DataFrame(0, index=[0], columns=model_features)
high_value_segments = ['watches', 'health_beauty', 'audio_video_electronics']
input_df['is_high_value_segment'] = 1 if segment in high_value_segments else 0

for col in [f'origin_{origin}', f'lead_type_{lead_type}']:
    if col in input_df.columns:
        input_df[col] = 1

prob = clf_model.predict_proba(input_df)[0, 1]
ltv_pred = reg_model.predict(input_df)[0] * upsell_multiplier
expected_revenue = prob * ltv_pred

# ==========================================
# 5. LAYOUT PRINCIPAL
# ==========================================

st.markdown(f"### Lead: {segment.replace('_',' ').title()} | <span style='color:#64748B; font-weight:normal;'>{origin.replace('_',' ').title()}</span>", unsafe_allow_html=True)

# FILA 1: KPIs
kpi_cols = st.columns(3)
with kpi_cols[0]:
    st.metric("Close Probability", f"{prob:.1%}")
with kpi_cols[1]:
    st.metric("Projected LTV", f"${ltv_pred:,.0f}")
with kpi_cols[2]:
    st.metric("Expected Revenue", f"${expected_revenue:,.0f}")

style_metric_cards(border_left_color="#2563EB", background_color="#FFFFFF", box_shadow=True)

# FILA 2: ESTRATEGIA Y BENCHMARK
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.markdown("<p class='section-header'>Sales Strategy</p>", unsafe_allow_html=True)
    if expected_revenue > 12000: # Umbral ajustado por el nuevo multiplicador
        persona, advice, color, icon = "SHARK", "High-Volume partner. Deploy executive-level terms.", "#DC2626", "🦈"
    elif prob > 0.6:
        persona, advice, color, icon = "EAGLE", "Ready to convert. Simplify onboarding now.", "#2563EB", "🦅"
    elif ltv_pred > 5000:
        persona, advice, color, icon = "WOLF", "Mid-High potential. Upsell Olist Ads.", "#D97706", "🐺"
    else:
        persona, advice, color, icon = "CAT", "Small-scale seller. Prioritize automated onboarding.", "#16A34A", "🐱"

    st.markdown(f"""
        <div class="strategy-container" style="border-left-color: {color};">
            <div style="font-size: 1.5rem; font-weight: 800; color: {color}; margin-bottom: 4px;">{icon} {persona}</div>
            <div style="color: #1E293B; font-size: 0.95rem;"><b>Strategy:</b> {advice}</div>
        </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("<p class='section-header'>Logistics of the Segment</p>", unsafe_allow_html=True)
    bench = logistics_db.get(segment, logistics_db['other'])
    risk_color = "#DC2626" if bench['risk'] == 'High' else ("#D97706" if bench['risk'] == 'Medium' else "#16A34A")
    
    b_col1, b_col2, b_col3 = st.columns(3)
    with b_col1:
        st.markdown(f"<div class='bench-box'><span class='bench-label'>Delivery</span><span class='bench-value'>{bench['days']}d</span></div>", unsafe_allow_html=True)
    with b_col2:
        st.markdown(f"<div class='bench-box'><span class='bench-label'>Risk</span><span class='bench-value' style='color:{risk_color};'>{bench['risk']}</span></div>", unsafe_allow_html=True)
    with b_col3:
        st.markdown(f"<div class='bench-box'><span class='bench-label'>Rating</span><span class='bench-value'>{bench['score']}</span></div>", unsafe_allow_html=True)

# FILA 3: ALERTA CORREGIDA
add_vertical_space(1)
if bench['days'] > 10 or bench['score'] < 4.0:
    st.error(f"🚩 **Retention Alert:** A niche prone to slow deliveries. We recommend **Olist Fulfillment** and **Olist Ads** to secure growth.")
else:
    st.success(f"✅ **Retention Outlook:** Standard logistics performance expected for this segment.")

st.markdown(f"<p style='color: #94A3B8; font-size: 0.7rem; text-align: right; margin-top: 20px;'>Olist PRM v1.3 | Data: April 2026</p>", unsafe_allow_html=True)