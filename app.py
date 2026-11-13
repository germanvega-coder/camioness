import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

# Configuración de la página
st.set_page_config(
    page_title="OptiRoute: Simulador y Optimización Dinámica",
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
st.sidebar.markdown("### 🎛️ Parámetros Dinámicos")
num_camiones = st.sidebar.slider("Número de Camiones", 1, 15, 6)
tiempo_base_carguio = st.sidebar.slider("Tiempo Base Carguío (min)", 5.0, 25.0, 12.0)
tiempo_base_transporte = st.sidebar.slider("Tiempo Base Transporte (min)", 10.0, 50.0, 25.0)

# Cabecera principal
st.markdown("## ⛏️ OptiRoute: Simulador y Optimización Dinámica de Rutas")
st.markdown("Las rutas óptimas y los tiempos se recalculan en tiempo real según la carga de camiones y los parámetros operativos.")

# Botón de ejecución
if st.button("🚀 Ejecutar Simulación y Actualizar Rutas", type="primary"):
    st.success("¡Simulación y optimización dinámica completada con éxito!")

    # Cálculos operativos basados en parámetros de entrada
    ciclo_promedio_base = tiempo_base_carguio + tiempo_base_transporte + 1.68
    meta_ciclo_optimizado = ciclo_promedio_base * 0.85  # Reducción exacta del 15%

    # Factor de escala dinámico basado en los sliders (afecta los tramos de la red)
    factor_escala = (tiempo_base_transporte / 25.0) * (1 + (num_camiones - 6) * 0.02)

    # Métricas superiores
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Ciclo Promedio Base", value=f"{ciclo_promedio_base:.2f} min")
    with col2:
        st.metric(label="Ciclo Objetivo (-15%)", value=f"{meta_ciclo_optimizado:.2f} min", delta="-15%")

    st.markdown("---")
    st.subheader("🌐 Red Minera Dinámica (Actualizada por Parámetros)")

    # Modelo de red minera con pesos dinámicos según los sliders
    G = nx.DiGraph()
    G.add_edge("Frente_Norte", "Cruce_A", tiempo=round(4.5 * factor_escala, 2), via="Rampa Principal")
    G.add_edge("Frente_Norte", "Cruce_B", tiempo=round(6.0 * (2 - factor_escala), 2), via="Galería Auxiliar")
    G.add_edge("Cruce_A", "Cruce_C", tiempo=round(5.2 * factor_escala, 2), via="Rampa Sur")
    G.add_edge("Cruce_A", "Chancador_1", tiempo=round(6.8 * factor_escala, 2), via="Bypass Rápido")
    G.add_edge("Cruce_B", "Cruce_C", tiempo=round(4.0 * factor_escala, 2), via="Nivel Intermedio")
    G.add_edge("Cruce_C", "Chancador_1", tiempo=round(4.5 * factor_escala, 2), via="Acceso Directo")
    G.add_edge("Chancador_1", "Cruce_B", tiempo=round(5.0 * factor_escala, 2), via="Retorno Este")
    G.add_edge("Cruce_B", "Frente_Norte", tiempo=round(4.2 * factor_escala, 2), via="Retorno Norte")
    G.add_edge("Chancador_1", "Cruce_A", tiempo=round(6.5 * factor_escala, 2), via="Retorno Principal")

    # Algoritmo de Dijkstra con la red modificada dinámicamente
    ruta_ida = nx.dijkstra_path(G, source="Frente_Norte", target="Chancador_1", weight="tiempo")
    tiempo_ida = nx.dijkstra_path_length(G, source="Frente_Norte", target="Chancador_1", weight="tiempo")
    
    ruta_vuelta = nx.dijkstra_path(G, source="Chancador_1", target="Frente_Norte", weight="tiempo")
    tiempo_vuelta = nx.dijkstra_path_length(G, source="Chancador_1", target="Frente_Norte", weight="tiempo")

    tiempo_transporte_optimo = tiempo_ida + tiempo_vuelta
    nuevo_ciclo_total = tiempo_base_carguio + tiempo_transporte_optimo + 1.28

    # Mostrar rutas en columnas
    c_r1, c_r2 = st.columns(2)
    with c_r1:
        st.info(f"🚚 **Ruta Óptima de Ida (Dinámica):**\n\n {' ➔ '.join(ruta_ida)} \n\n **Tiempo Ida:** {tiempo_ida:.2f} min")
    with c_r2:
        st.info(f"🔄 **Ruta Óptima de Vuelta (Dinámica):**\n\n {' ➔ '.join(ruta_vuelta)} \n\n **Tiempo Vuelta:** {tiempo_vuelta:.2f} min")

    # Gráficos dinámicos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.patch.set_facecolor('#0e1117')

    # Gráfico 1: Grafo con la nueva ruta resaltada
    ax1.set_facecolor('#0e1117')
    pos = {"Frente_Norte": (0, 1), "Cruce_A": (1, 1.8), "Cruce_B": (1, 0.2), "Cruce_C": (2, 1), "Chancador_1": (3, 1)}
    nx.draw_networkx_nodes(G, pos, ax=ax1, node_color='#0088cc', node_size=1500)
    nx.draw_networkx_labels(G, pos, ax=ax1, font_color='white', font_size=8, font_weight='bold')
    nx.draw_networkx_edges(G, pos, ax=ax1, edge_color='#555555', arrows=True, connectionstyle="arc3,rad=0.1")
    
    aristas_ida = list(zip(ruta_ida, ruta_ida[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=aristas_ida, ax=ax1, edge_color='#00e676', width=3.5, arrows=True, connectionstyle="arc3,rad=0.1")
    
    # Etiquetas de tiempo en los tramos para ver el cambio
    edge_labels = {(u, v): f"{d['tiempo']}m" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax1, font_color='#ffeb3b', font_size=7)

    ax1.set_title(f"Red Minera (Flota: {num_camiones} Camiones)", color='white', fontsize=10, fontweight='bold')
    ax1.axis('off')

    # Gráfico 2: Comparativa de Tiempos
    ax2.set_facecolor('#0e1117')
    categorias = ['Ciclo Base', 'Meta (-15%)', 'Ruta Óptima Dinámica']
    valores = [ciclo_promedio_base, meta_ciclo_optimizado, nuevo_ciclo_total]
    colores = ['#1a233a', '#0088cc', '#00c853']
    
    bars = ax2.bar(categorias, valores, color=colores, width=0.5, edgecolor='white')
    for bar in bars:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, f"{yval:.2f}m", ha='center', va='bottom', color='white', fontweight='bold')
    
    ax2.set_ylabel("Minutos por Ciclo", color='white', fontweight='bold')
    ax2.set_title("Comparativa de Tiempos Operativos", color='white', fontsize=10, fontweight='bold')
    ax2.set_ylim(0, max(valores) * 1.25)
    ax2.tick_params(colors='white')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_color('white')
    ax2.spines['left'].set_color('white')

    st.pyplot(fig)
else:
    st.info("👈 Modifica los deslizadores de la izquierda (Camiones, Carguío, Transporte) y haz clic en el botón para ver cómo cambian dinámicamente las rutas óptimas en el grafo.")
