import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Configuración de página de Streamlit
st.set_page_config(page_title="Enaex - Reporte de Turno", layout="wide")

# ==========================================
# 🛠️ FUNCIONES DE DATOS
# ==========================================

def cargar_datos_ejemplo():
    """Genera datos ficticios para que el dashboard no aparezca vacío"""
    data = {
        "ID": range(1, 21),
        "X": np.random.uniform(0, 100, 20),
        "Y": np.random.uniform(0, 100, 20),
        "Categoria": np.random.choice(["Óptimo", "Corto", "Crítico", "Tapado"], 20)
    }
    return pd.DataFrame(data)

# ==========================================
# 📂 BARRA LATERAL (CONTROL)
# ==========================================
st.sidebar.header("Configuración del Reporte")
uploaded_file = st.sidebar.file_uploader("Subir Excel/CSV de Perforación", type=["xlsx", "csv"])
turno_seleccionado = st.sidebar.selectbox("Turno", ["DÍA", "NOCHE"])
generar_pdf = st.sidebar.button("Generar Reporte PDF (Simulado)")

# Lógica de carga
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.sidebar.success("Archivo cargado correctamente")
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        df = cargar_datos_ejemplo()
else:
    df = cargar_datos_ejemplo()
    st.sidebar.info("Usando datos de ejemplo (Sube un archivo para actualizar)")

# ==========================================
# 📊 PROCESAMIENTO DE KPIs
# ==========================================
fecha_actual = datetime.now().strftime("%d/%m/%Y")

conteo = df["Categoria"].value_counts()
optimo = conteo.get("Óptimo", 0)
corto = conteo.get("Corto", 0)
critico = conteo.get("Crítico", 0)
tapado = conteo.get("Tapado", 0)
total = len(df)
avance = (optimo / total) * 100 if total > 0 else 0

# ==========================================
# 🎨 CONSTRUCCIÓN DEL DASHBOARD (Matplotlib)
# ==========================================
plt.rcParams['font.family'] = 'sans-serif'
fig = plt.figure(figsize=(16, 10), facecolor='#F8F9FA')
gs = fig.add_gridspec(3, 4, hspace=0.4, wspace=0.3)

# --- 1. ENCABEZADO CORPORATIVO ---
ax_header = fig.add_subplot(gs[0, :])
ax_header.axis('off')
ax_header.text(0, 0.85, "ENAEX - SERVICIOS MINEROS", fontsize=14, color='#CC0000', fontweight='bold')
ax_header.text(0, 0.45, "REPORTE OPERATIVO DE CARGUÍO", fontsize=26, fontweight='black')
ax_header.text(0.95, 0.45, f"FECHA: {fecha_actual}\nTURNO: {turno_seleccionado}", 
               fontsize=13, ha='right', bbox=dict(facecolor='white', edgecolor='#DDDDDD', boxstyle='round,pad=0.5'))

# --- 2. VELOCÍMETRO (GAUGE) ---
ax_gauge = fig.add_subplot(gs[1, 0], projection='polar')
theta = np.linspace(0, np.pi, 100)
# Fondo gris
ax_gauge.fill_between(theta, 1, 1.3, color='#EEEEEE')
# Barra de progreso roja
ax_gauge.fill_between(np.linspace(0, (avance/100)*np.pi, 100), 1, 1.3, color='#CC0000')

# Aguja
arrow_angle = (avance / 100) * np.pi
ax_gauge.annotate('', xy=(arrow_angle, 1.3), xytext=(0, 0),
                 arrowprops=dict(arrowstyle='wedge, tail_width=0.4', color='#333333'))

ax_gauge.set_thetamin(0)
ax_gauge.set_thetamax(180)
ax_gauge.axis('off')
ax_gauge.text(0.5, 0.05, f"{avance:.1f}%", transform=ax_gauge.transAxes, 
             fontsize=24, fontweight='bold', ha='center', color='#CC0000')
ax_gauge.set_title("AVANCE DE CARGUÍO", pad=-10, fontweight='bold', fontsize=14)

# --- 3. RESUMEN ESTADOS (BARRAS) ---
ax_bar = fig.add_subplot(gs[2, 0])
categorias = ["Óptimo", "Corto", "Crítico", "Tapado"]
valores = [optimo, corto, critico, tapado]
colores_bar = ["#2E7D32", "#FBC02D", "#EF6C00", "#C62828"]

bars = ax_bar.barh(categorias, valores, color=colores_bar, height=0.7)
ax_bar.bar_label(bars, padding=5, fontweight='bold', fontsize=11)
ax_bar.spines[['top', 'right', 'bottom']].set_visible(False)
ax_bar.set_xticks([])
ax_bar.invert_yaxis()
ax_bar.set_title("CANTIDAD POR ESTADO", loc='left', fontweight='bold', pad=15)

# --- 4. PLANO DE MALLA (SCATTER) ---
ax_scatter = fig.add_subplot(gs[1:, 1:])
ax_scatter.set_facecolor('#FFFFFF')

colores_map = {
    "Óptimo": "#2E7D32", 
    "Corto": "#FBC02D", 
    "Crítico": "#EF6C00", 
    "Tapado": "#C62828"
}

for cat, color in colores_map.items():
    sub = df[df["Categoria"] == cat]
    if not sub.empty:
        ax_scatter.scatter(sub["X"], sub["Y"], c=color, s=150, 
                           edgecolors='#333333', linewidth=0.8, label=cat, zorder=3)

# Etiquetas de ID
offset = (df["Y"].max() - df["Y"].min()) * 0.02 if not df.empty else 1
for _, row in df.iterrows():
    ax_scatter.text(row["X"], row["Y"] + offset, str(row["ID"]), 
                    fontsize=8, ha='center', fontweight='bold', alpha=0.7)

ax_scatter.grid(True, linestyle='--', alpha=0.3, zorder=0)
ax_scatter.set_aspect('equal')
ax_scatter.legend(loc='upper right', title="Referencia de Estados", frameon=True, shadow=True)
ax_scatter.set_title("PLANO DE MALLA DE PERFORACIÓN", fontweight='bold', size=16, pad=20)
ax_scatter.set_xlabel("Coordenada Este (X)", fontsize=10)
ax_scatter.set_ylabel("Coordenada Norte (Y)", fontsize=10)

# ==========================================
# 🚀 RENDERIZADO EN STREAMLIT
# ==========================================
st.pyplot(fig)

# Tabla de datos opcional para revisión
with st.expander("Ver tabla de datos completa"):
    st.dataframe(df, use_container_width=True)