import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de Estilo y Colores
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #00FF00;
    }
    h1, h2, h3, p, label {
        color: #00FF00 !important;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Sistema de Localización por Triangulación")
st.write("busqueda de operador de drones")
st.markdown("---")

# 2. Panel de Control (Barra Lateral)
st.sidebar.header("Entrada de Datos (Vector b)")
b1 = st.sidebar.number_input("Señal Estación Alpha", value=5.0)
b2 = st.sidebar.number_input("Señal Estación Bravo", value=4.0)
b3 = st.sidebar.number_input("Señal Estación Charlie", value=3.0)

st.sidebar.markdown("---")
ruido_nivel = st.sidebar.slider("Interferencia / Ruido", 0.0, 3.0, 0.0)

# 3. Definición de la Matriz A (Posiciones fijas de sensores)
A = np.array([
    [1, 1],   # Estación Alpha
    [-1, 2],  # Estación Bravo
    [0, 1]    # Estación Charlie
])
b = np.array([b1, b2, b3])

# 4. Lógica de Ruido
if ruido_nivel > 0:
    error = np.random.normal(0, ruido_nivel, size=b.shape)
    b_final = b + error
else:
    b_final = b

# 5. Resolución Matemática (Ax = b)
solucion = np.linalg.lstsq(A, b_final, rcond=None)[0]
x_op, y_op = solucion

# 6. Sección de Coordenadas Exactas (Lo que pediste)
st.subheader("📍 Coordenadas Exactas del Objetivo")
st.code(f"LATITUD (Y): {y_op:.4f} km\nLONGITUD (X): {x_op:.4f} km", language='bash')

# 7. Métricas visuales rápidas
c1, c2 = st.columns(2)
c1.metric("Posición X", f"{x_op:.2f}")
c2.metric("Posición Y", f"{y_op:.2f}")

# 8. Creación del Mapa (Radar)
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#0e1117')
ax.set_facecolor('#161b22')

# Dibujar las estaciones
ax.scatter(A[:,0], A[:,1], color='#00FF00', marker='^', s=150, label='Sensores (Matriz A)')
for i, txt in enumerate(['Alpha', 'Bravo', 'Charlie']):
    ax.annotate(txt, (A[i,0], A[i,1]), color='#00FF00', xytext=(0,7), textcoords="offset points", ha='center')

# Dibujar el Objetivo
ax.scatter(x_op, y_op, color='#FF4B4B', marker='X', s=300, label='Objetivo Encontrado')

# Estética
ax.grid(True, linestyle='--', alpha=0.3, color='#00FF00')
ax.axhline(0, color='#00FF00', linewidth=1, alpha=0.5)
ax.axvline(0, color='#00FF00', linewidth=1, alpha=0.5)
ax.tick_params(colors='#00FF00')
ax.legend(facecolor='#0e1117', labelcolor='#00FF00')

st.pyplot(fig)

# 9. Alertas
if ruido_nivel > 1.5:
    st.error("⚠️ ALERTA DE PRECISIÓN: Interferencia alta detectada.")
