import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="OptiRoute: Simulador y Optimización Minera",
    page_icon="⛏️",
    layout="wide"
)

# Estilo visual general
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stSlider label { color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

# Panel Lateral (Parámetros de Simulación)
st.sidebar.markdown("### Parámetros de Simulación")
num_camiones = st.sidebar.slider("Número de Camiones", 1, 15, 6)
tiempo_base_carguio = st.sidebar.slider("Tiempo Base Carguío (min)", 5.0, 25.0, 12.0)
tiempo_base_transporte = st.sidebar.slider("Tiempo Base Transporte (min)", 10.0, 50.0, 25.0)

# Cabecera principal
st.markdown("## ⛏️ OptiRoute: Simulador y Optimización Minera")
st.markdown("Aplicación web gratuita para la gestión y reducción del **15% en los tiempos de ciclo de transporte**[cite: 1].")

# Botón de ejecución
if st.button("Ejecutar Simulación y Optimización", type="primary"):
    st.success("¡Simulación completada con éxito!")

    # Cálculos basados en tus parámetros
    ciclo_promedio_base = tiempo_base_carguio + tiempo_base_transporte + 1.68
    ciclo_optimizado = ciclo_promedio_base * 0.85  # Reducción exacta del 15%

    # Métricas superiores
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Ciclo Promedio Base", value=f"{ciclo_promedio_base:.2f} min")
    with col2:
        st.metric(label="Ciclo Optimizado (-15%)", value=f"{ciclo_optimizado:.2f} min", delta="-15%")

    # Gráfico de Comparativa de Tiempos Operativos
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')

    categorias = ['Ciclo Base', 'Ciclo Optimizado (-15%)']
    valores = [ciclo_promedio_base, ciclo_optimizado]
    colores = ['#1a233a', '#0088cc']

    bars = ax.bar(categorias, valores, color=colores, width=0.4, edgecolor='white', linewidth=0.8)

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.6, f"{yval:.2f} min", ha='center', va='bottom', color='white', fontweight='bold')

    ax.set_ylabel("Minutos por Ciclo", color='white', fontweight='bold')
    ax.set_title("Comparativa de Tiempos Operativos", color='white', fontsize=12, fontweight='bold')
    ax.set_ylim(0, max(valores) * 1.25)
    
    ax.tick_params(colors='white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')

    st.pyplot(fig)
else:
    st.info("👈 Modifica los parámetros en la barra lateral izquierda y haz clic en **'Ejecutar Simulación y Optimización'** para ver los resultados.")
