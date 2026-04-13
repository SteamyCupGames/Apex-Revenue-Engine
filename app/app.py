# import streamlit as st
# import joblib
# import pandas as pd
# import numpy as np

# # 1. Configuración de la Interfaz
# st.set_page_config(page_title="Olist | Predictive Revenue Engine", layout="wide", page_icon="🚀")
# st.title("🚀 SDR Priority Console: Shark Detector")

# # 2. Carga de Assets (Asegúrate de que la ruta sea correcta)
# @st.cache_resource
# def load_assets():
#     clf = joblib.load('C:\\Users\\User\\Desktop\\Software y Clases\\BigData\\OList\\olist-project-sa\\Model\\lead_scoring_rf_model.joblib')
#     reg = joblib.load('C:\\Users\\User\\Desktop\\Software y Clases\\BigData\\OList\\olist-project-sa\\Model\\ltv_regressor_model.joblib')
#     features = joblib.load('C:\\Users\\User\\Desktop\\Software y Clases\\BigData\\OList\\olist-project-sa\\Model\\model_features.joblib')
#     return clf, reg, features

# try:
#     clf_model, reg_model, model_features = load_assets()
# except Exception as e:
#     st.error(f"❌ Error al cargar modelos: {e}")
#     st.stop()

# # 3. Sidebar: Captura de Datos (Inferencia en Tiempo Real)
# with st.sidebar:
#     st.header("Lead Characteristics")
#     origin = st.selectbox("Marketing Origin", ['organic_search', 'paid_search', 'social', 'unknown', 'email', 'other'])
#     segment = st.selectbox("Business Segment", ['watches', 'health_beauty', 'audio_video_electronics', 'household_utilities', 'construction_tools', 'other'])
#     lead_type = st.selectbox("Lead Type", ['online_medium', 'online_big', 'offline', 'industry', 'not_qualified'])

# # 4. Construcción del input_df (Fixing Syntax & Index Errors)
# # Creamos la fila identificada con 
# input_df = pd.DataFrame(0, index=[0], columns=model_features)

# # Inyectamos tu hallazgo de Data Forensics: Relojes y Salud/Belleza son High Value
# high_value_segments = ['watches', 'health_beauty', 'audio_video_electronics']
# input_df['is_high_value_segment'] = 1 if segment in high_value_segments else 0

# # Activamos los One-Hot Encoders correspondientes
# if f'origin_{origin}' in input_df.columns:
#     input_df[f'origin_{origin}'] = 1
# if f'lead_type_{lead_type}' in input_df.columns:
#     input_df[f'lead_type_{lead_type}'] = 1

# # 5. Ejecución del botón de predicción
# if st.button("Analyze Lead Potential"):
#     # Accedemos a la fila 0, columna 1 (Probabilidad de éxito)
#     prob_array = clf_model.predict_proba(input_df)
#     prob = prob_array[0, 1]  # <--- CORRECCIÓN: Fila 0, Columna 1
    
#     # LTV: Accedemos al primer elemento del array resultante
#     ltv_pred = reg_model.predict(input_df)[0] # <--- CORRECCIÓN: Extraer el escalar
    
#     # El resto del cálculo ahora funcionará porque prob y ltv_pred son números simples
#     expected_revenue = prob * ltv_pred

#     # 6. Visualización de Resultados
#     st.divider()
#     c1, c2, c3 = st.columns(3)
#     c1.metric("Closing Probability", f"{prob:.1%}")
#     c2.metric("Potential LTV", f"${ltv_pred:,.2f}")
#     c3.metric("Expected ROI", f"${expected_revenue:,.2f}")

#     # Notificaciones de Prioridad de Negocio
#     if expected_revenue > 5000:
#         st.error("🔥 HIGH PRIORITY: Potential SHARK detected.")
#     elif prob > 0.4:
#         st.warning("⚡ MEDIUM PRIORITY: Likely conversion.")
#     else:
#         st.info("🐢 LOW PRIORITY: Standard lead profile.")

#     # El "Golden Insight" para el reclutador
#     if segment == 'watches' and origin == 'unknown':
#         st.success("💡 DATA FORENSICS ALERT: Este lead pertenece al nicho de relojería con LTV histórico masivo ($113k).")


# Senior attempt
import streamlit as st
import joblib
import pandas as pd
import numpy as np

# 1. Configuración de la Interfaz
st.set_page_config(page_title="Olist | Predictive Revenue Engine", layout="wide", page_icon="🚀")

# Estilo personalizado para las alertas de estrategia
st.markdown("""
    <style>
    .strategy-box {
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 SDR Priority Console: Shark Detector")

# 2. Carga de Assets
@st.cache_resource
def load_assets():
    # Rutas relativas recomendadas para portabilidad
    path = 'C:\\Users\\User\\Desktop\\Software y Clases\\BigData\\OList\\olist-project-sa\\Model\\'
    clf = joblib.load(f'{path}lead_scoring_rf_model.joblib')
    reg = joblib.load(f'{path}ltv_regressor_model.joblib')
    features = joblib.load(f'{path}model_features.joblib')
    return clf, reg, features

try:
    clf_model, reg_model, model_features = load_assets()
except Exception as e:
    st.error(f"❌ Error al cargar modelos: {e}")
    st.stop()

# 3. Sidebar: Inputs y Simulación de Upselling
with st.sidebar:
    st.header("🎯 Lead Profile")
    origin = st.selectbox("Marketing Origin", ['organic_search', 'paid_search', 'social', 'unknown', 'email', 'other'])
    segment = st.selectbox("Business Segment", ['watches', 'health_beauty', 'audio_video_electronics', 'household_utilities', 'construction_tools', 'other'])
    lead_type = st.selectbox("Lead Type", ['online_medium', 'online_big', 'offline', 'industry', 'not_qualified'])
    
    st.divider()
    st.header("📈 Catalog Upselling")
    # Simulador: ¿Qué pasa si el vendedor trae más productos?
    catalog_size = st.slider("Declared Catalog Size (SKUs)", 1, 500, 10)
    # Factor de escalabilidad (Lógica Senior: a más catálogo, mayor potencial de LTV)
    upsell_multiplier = 1 + (catalog_size * 0.005) 

# 4. Construcción del motor de inferencia
input_df = pd.DataFrame(0, index=[0], columns=model_features)

# Hallazgos estratégicos
high_value_segments = ['watches', 'health_beauty', 'audio_video_electronics']
input_df['is_high_value_segment'] = 1 if segment in high_value_segments else 0

if f'origin_{origin}' in input_df.columns:
    input_df[f'origin_{origin}'] = 1
if f'lead_type_{lead_type}' in input_df.columns:
    input_df[f'lead_type_{lead_type}'] = 1

# 5. Ejecución de Predicción
# if st.button("Analyze Lead Potential"):
#     # ML Outputs
#     prob = clf_model.predict_proba(input_df)[0, 1]
#     base_ltv = reg_model.predict(input_df)[0]
    
#     # Aplicar simulación de Upselling
#     ltv_pred = base_ltv * upsell_multiplier
#     expected_revenue = prob * ltv_pred

#     # 6. Dashboards de KPIs
#     st.divider()
#     c1, c2, c3 = st.columns(3)
#     c1.metric("Closing Probability", f"{prob:.1%}")
#     c2.metric("Projected LTV", f"${ltv_pred:,.2f}", delta=f"{upsell_multiplier:.1%} Scaling")
#     c3.metric("Expected ROI", f"${expected_revenue:,.2f}")

#     # 7. Recomendador de Estrategia (Persona Scripting)
#     st.subheader("🕵️ Sales Strategy Advice")
    
#     if expected_revenue > 10000:
#         persona = "🦈 SHARK"
#         advice = "Agresividad alta. Ofrecer contrato de exclusividad y destacar la infraestructura logística de Olist para alto volumen."
#         color = "inverse"
#     elif prob > 0.5:
#         persona = "🦅 EAGLE"
#         advice = "Cierre rápido. El lead está listo para convertir. Enfocarse en reducir fricción de onboarding."
#         color = "normal"
#     elif ltv_pred > 5000:
#         persona = "🐺 WOLF"
#         advice = "Valor medio-alto. Destacar herramientas de marketing interno (Olist Ads) para potenciar su visibilidad."
#         color = "normal"
#     else:
#         persona = "🐱 CAT"
#         advice = "Vendedor pequeño. Requiere educación. Enfatizar la facilidad de uso y el soporte inicial."
#         color = "off"

#     st.warning(f"**Target Persona Detected:** {persona}")
#     st.info(f"**Tactical Advice:** {advice}")
# ML Outputs (Cálculo instantáneo)
prob = clf_model.predict_proba(input_df)[0, 1]
base_ltv = reg_model.predict(input_df)[0]

# Aplicar simulación de Upselling (Reacciona al Slider de la barra lateral)
ltv_pred = base_ltv * upsell_multiplier
expected_revenue = prob * ltv_pred

# 6. Dashboards de KPIs
st.divider()
st.subheader("📊 Live Prediction Analysis")
c1, c2, c3 = st.columns(3)
c1.metric("Closing Probability", f"{prob:.1%}")
c2.metric("Projected LTV", f"${ltv_pred:,.2f}", delta=f"{((upsell_multiplier-1)*100):.1f}% Catalog Impact")
c3.metric("Expected ROI", f"${expected_revenue:,.2f}")

# 7. Recomendador de Estrategia (Persona Scripting)
# Esta sección ahora cambiará dinámicamente mientras mueves el slider o cambias el segmento
st.subheader("🕵️ Sales Strategy Advice")

if expected_revenue > 10000:
    persona = "🦈 SHARK"
    advice = "Agresividad alta. Ofrecer contrato de exclusividad y destacar la infraestructura logística de Olist para alto volumen."
    st.error(f"**Target Persona Detected:** {persona}")
elif prob > 0.5:
    persona = "🦅 EAGLE"
    advice = "Cierre rápido. El lead está listo para convertir. Enfocarse en reducir fricción de onboarding."
    st.warning(f"**Target Persona Detected:** {persona}")
elif ltv_pred > 5000:
    persona = "🐺 WOLF"
    advice = "Valor medio-alto. Destacar herramientas de marketing interno (Olist Ads) para potenciar su visibilidad."
    st.info(f"**Target Persona Detected:** {persona}")
else:
    persona = "🐱 CAT"
    advice = "Vendedor pequeño. Requiere educación. Enfatizar la facilidad de uso y el soporte inicial."
    st.success(f"**Target Persona Detected:** {persona}")

st.write(f"👉 **Tactical Advice:** {advice}")

#     # 8. Benchmark de Entrega (Contexto logístico)
#     st.divider()
#     st.subheader("📦 Expected Delivery Performance")
    
#     # Lógica de Benchmark simulada por categoría (Data Forensics)
#     benchmarks = {
#         'watches': {'days': 12, 'risk': 'Alto (Nicho Crítico)'},
#         'health_beauty': {'days': 7, 'risk': 'Bajo'},
#         'audio_video_electronics': {'days': 10, 'risk': 'Medio'}
#     }
    
#     bench = benchmarks.get(segment, {'days': 9, 'risk': 'Estándar'})
    
#     col_log1, col_log2 = st.columns(2)
#     col_log1.write(f"**Promedio entrega en {segment}:** {bench['days']} días")
#     col_log2.write(f"**Riesgo Logístico:** {bench['risk']}")
    
#     if bench['days'] > 10:
#         st.error("⚠️ **Logistics Alert:** Este segmento tiene tiempos de entrega sensibles. Recomendar 'Olist Entregas' para asegurar retención.")

#     # Golden Insight
#     if segment == 'watches' and origin == 'unknown':
#         st.success("💡 **DATA FORENSICS ALERT:** Nicho de lujo detectado. Posible tráfico directo de marca consolidada.")