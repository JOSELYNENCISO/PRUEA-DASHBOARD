import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Levantamiento de alturas")

archivo = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if archivo is not None:

    df = pd.read_excel(archivo)

    # 🔥 LIMPIAR
    df["Altura"] = pd.to_numeric(df["Altura"], errors='coerce')

    # 🔥 CLASIFICACIÓN
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

    # 🔥 TAMAÑOS
    n_puntos = len(df)

    if n_puntos > 150:
        size_punto = 25
        size_texto = 5
    elif n_puntos > 80:
        size_punto = 50
        size_texto = 7
    elif n_puntos > 40:
        size_punto = 90   
        size_texto = 10
    else:
        size_punto = 130   
        size_texto = 12

    # 🎨 COLORES
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
        "Sin dato": "Sin dato (-)"
    }

    # 🔥 SOLO UN BOTÓN (BIEN UBICADO)
    if st.button("🔘 Generar gráfico"):

        fig, ax = plt.subplots(figsize=(10,10))

        resumen = []

        for cat in colores:
            sub = df[df["Categoria"] == cat]
            cantidad = len(sub)

            resumen.append({
                "Categoría": nombres[cat],
                "Cantidad": cantidad
            })

            ax.scatter(sub["X"], sub["Y"],
                       c=colores[cat],
                       s=size_punto)

        # 🔤 IDs
        offset = (df["Y"].max() - df["Y"].min()) * 0.008

        for _, row in df.iterrows():
            ax.text(row["X"], row["Y"] + offset,
                    str(row["ID"]),
                    fontsize=size_texto,
                    ha='center',
                    va='bottom',
                    fontweight='bold')

        ax.set_title("Plano de Taladros", fontsize=14, fontweight='bold')
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(False)

        margen = (df["X"].max() - df["X"].min()) * 0.05

        ax.set_xlim(df["X"].min() - margen, df["X"].max() + margen)
        ax.set_ylim(df["Y"].min() - margen, df["Y"].max() + margen)

        ax.set_aspect('equal', adjustable='box')

        st.pyplot(fig)

        # =========================
        # 📋 TABLA KPI
        # =========================
        st.subheader("📋 Resumen de Taladros")

        resumen_df = pd.DataFrame(resumen)
        st.dataframe(resumen_df, use_container_width=True)

        # =========================
        # 📊 GRÁFICO DE BARRAS
        # =========================
        st.subheader("📊 Distribución de Taladros")

        fig_bar, ax_bar = plt.subplots()

        ax_bar.bar(resumen_df["Categoría"], resumen_df["Cantidad"])

        ax_bar.set_title("Taladros por Categoría")
        ax_bar.set_ylabel("Cantidad")

        plt.xticks(rotation=30)

        st.pyplot(fig_bar)

        # =========================
        # 📥 DESCARGA
        # =========================
        fig.savefig("grafico.png", dpi=600, bbox_inches='tight')

        with open("grafico.png", "rb") as file:
            st.download_button("⬇️ Descargar imagen", file, "grafico_taladros.png")