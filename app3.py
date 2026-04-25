import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import matplotlib.patches as patches

# ==========================================
# ⚙️ CONFIGURACIÓN Y DATOS (Simulados)
# ==========================================
# (Asegúrate de tener tu dataframe 'df' cargado aquí)
fecha_actual = datetime.now().strftime("%d/%m/%Y")
turno = "DÍA"  # Esto puede venir de un selectbox de Streamlit

conteo = df["Categoria"].value_counts()
optimo = conteo.get("Óptimo", 0)
corto = conteo.get("Corto", 0)
critico = conteo.get("Crítico", 0)
tapado = conteo.get("Tapado", 0)
total = len(df)
avance = (optimo / total) * 100 if total > 0 else 0

# ==========================================
# 🎨 DISEÑO DEL DASHBOARD
# ==========================================
plt.rcParams['font.family'] = 'sans-serif'
fig = plt.figure(figsize=(16, 10), facecolor='#F4F4F4')
gs = fig.add_gridspec(3, 4, hspace=0.4, wspace=0.3)

# 1. ENCABEZADO PERSONALIZADO
ax_header = fig.add_subplot(gs[0, :])
ax_header.axis('off')
ax_header.text(0, 0.8, "ENAEX - SERVICIOS MINEROS", fontsize=14, color='#CC0000', fontweight='bold')
ax_header.text(0, 0.4, f"REPORTE DE CARGUÍO DE TALADROS", fontsize=22, fontweight='black')
ax_header.text(0.95, 0.4, f"FECHA: {fecha_actual}\nTURNO: {turno}", 
               fontsize=12, ha='right', bbox=dict(facecolor='white', alpha=0.5))

# 2. VELOCÍMETRO REAL (GAUGE CIRCULAR)
ax_gauge = fig.add_subplot(gs[1, 0], projection='polar')

# Configuración del arco
theta = np.linspace(0, np.pi, 100)
ax_gauge.fill_between(theta, 1, 1.3, color='lightgrey', alpha=0.3) # Fondo
ax_gauge.fill_between(np.linspace(0, (avance/100)*np.pi, 100), 1, 1.3, color='#CC0000') # Progreso

# Aguja
arrow_angle = (avance / 100) * np.pi
ax_gauge.annotate('', xy=(arrow_angle, 1.3), xytext=(0, 0),
                 arrowprops=dict(arrowstyle='wedge, tail_width=0.3', color='black'))

ax_gauge.set_thetamin(0)
ax_gauge.set_thetamax(180)
ax_gauge.set_xticks([])
ax_gauge.set_yticks([])
ax_gauge.axis('off')
ax_gauge.text(0.5, 0.1, f"{avance:.1f}%", transform=ax_gauge.transAxes, 
             fontsize=20, fontweight='bold', ha='center')
ax_gauge.set_title("AVANCE TOTAL", pad=-20, fontweight='bold')

# 3. KPI BARRAS HORIZONTALES (ESTILO MODERNO)
ax_bar = fig.add_subplot(gs[2, 0])
categorias = ["Óptimos", "Cortos", "Críticos", "Tapados"]
valores = [optimo, corto, critico, tapado]
colores_bar = ["#2E7D32", "#FBC02D", "#EF6C00", "#C62828"]

bars = ax_bar.barh(categorias, valores, color=colores_bar, height=0.6)
ax_bar.bar_label(bars, padding=3, fontweight='bold')
ax_bar.spines[['top', 'right', 'bottom']].set_visible(False)
ax_bar.set_xticks([])
ax_bar.invert_yaxis()
ax_bar.set_title("RESUMEN DE ESTADOS", loc='left', fontweight='bold')

# 4. PLANO DE TALADROS (DERECHA)
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
    ax_scatter.scatter(sub["X"], sub["Y"], c=color, s=100, edgecolors='white', label=cat, zorder=3)

# Cuadrícula y etiquetas
ax_scatter.grid(True, linestyle='--', alpha=0.6, zorder=0)
ax_scatter.set_aspect('equal')
ax_scatter.legend(loc='upper right', title="Referencia")

# IDs con mejor visibilidad
offset = (df["Y"].max() - df["Y"].min()) * 0.02
for _, row in df.iterrows():
    ax_scatter.text(row["X"], row["Y"] + offset, str(row["ID"]), 
                    fontsize=7, ha='center', fontweight='bold')

ax_scatter.set_title("DISTRIBUCIÓN ESPACIAL DE MALLA", fontweight='bold', size=14)

# ==========================================
# 🚀 FINALIZACIÓN
# ==========================================
plt.tight_layout()
st.pyplot(fig) # Si estás en Streamlit

# Botón para descargar (Opcional)
# fig.savefig("reporte_enaex.pdf", bbox_inches='tight')