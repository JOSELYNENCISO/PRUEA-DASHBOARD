import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import io
import datetime

st.set_page_config(page_title="Dashboard de Taladros", layout="wide")

# =========================
# 🎨 HEADER CORPORATIVO
# =========================
col1, col2 = st.columns([1, 4])

with col1:
    logo = st.file_uploader("Sube tu logo", type=["png", "jpg", "jpeg"])

with col2:
    st.title("📊 Dashboard de Levantamiento de Alturas")

project_name = st.text_input("Nombre del proyecto", "Proyecto Mina XYZ")
fecha = st.date_input("Fecha del reporte", datetime.date.today())

# =========================
# 📂 ARCHIVO EXCEL
# =========================
archivo = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if archivo is not None:

    df = pd.read_excel(archivo)
    df["Altura"] = pd.to_numeric(df["Altura"], errors='coerce')

    # =========================
    # 📌 CLASIFICACIÓN
    # =========================
    def clasificar(h):
        if pd.isna(h):
            return "Sin dato"
        elif h >= 14:
            return "Óptimo"
        elif h >= 10:
            return "Corto"
        elif h >= 6:
            return "Crítico"
        else:
            return "Tapado"

    df["Categoria"] = df["Altura"].apply(clasificar)

    colores = {
        "Óptimo": "green",
        "Corto": "yellow",
        "Crítico": "orange",
        "Tapado": "red",
        "Sin dato": "black"
    }

    nombres = {
        "Óptimo": "Óptimo (>=14 m)",
        "Corto": "Corto (10–14 m)",
        "Crítico": "Crítico (6–10 m)",
        "Tapado": "Tapado (<6 m)",
        "Sin dato": "Sin dato"
    }

    # =========================
    # 📊 GRÁFICO
    # =========================
    fig, ax = plt.subplots(figsize=(10, 10))

    for cat in colores:
        sub = df[df["Categoria"] == cat]
        ax.scatter(sub["X"], sub["Y"],
                   c=colores[cat],
                   label=f"{nombres[cat]} ({len(sub)})",
                   s=80)

    for i, row in df.iterrows():
        ax.text(row["X"], row["Y"], str(row["ID"]),
                fontsize=8, ha='center')

    ax.set_title("Plano de Taladros")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend()
    ax.set_aspect('equal')

    st.pyplot(fig)

    # =========================
    # 🖼️ EXPORTAR DASHBOARD HD (JPG)
    # =========================
    if st.button("⬇️ Descargar Dashboard HD (JPG)"):

        # --- Crear imagen base ---
        width, height = 1800, 1200
        dashboard = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(dashboard)

        # --- Logo ---
        if logo is not None:
            logo_img = Image.open(logo)
            logo_img = logo_img.resize((200, 200))
            dashboard.paste(logo_img, (50, 50))

        # --- Texto superior ---
        draw.text((300, 80), f"{project_name}", fill="black")
        draw.text((300, 130), f"Fecha: {fecha}", fill="gray")

        # --- Convertir gráfico a imagen ---
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
        buf.seek(0)
        plot_img = Image.open(buf)

        plot_img = plot_img.resize((1200, 900))

        dashboard.paste(plot_img, (300, 250))

        # --- Guardar HD ---
        output = "dashboard_hd.jpg"
        dashboard.save(output, "JPEG", quality=95)

        with open(output, "rb") as file:
            st.download_button(
                "📥 Descargar JPG HD",
                file,
                file_name="dashboard_taladros_HD.jpg",
                mime="image/jpeg"
            )