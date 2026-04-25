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

    for i, row in df.iterrows():
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
    # 📊 KPI - TABLA BONITA
    # =========================
    st.subheader("📋 Resumen de Taladros")

    resumen_df = pd.DataFrame(resumen)

    st.dataframe(resumen_df, use_container_width=True)

    # =========================
    # 📊 KPI - GRÁFICO DE BARRAS
    # =========================
    st.subheader("📊 Distribución de Taladros")

    fig_bar, ax_bar = plt.subplots()

    ax_bar.bar(resumen_df["Categoría"], resumen_df["Cantidad"])

    ax_bar.set_title("Taladros por Categoría")
    ax_bar.set_ylabel("Cantidad")
    ax_bar.set_xlabel("Categoría")

    plt.xticks(rotation=30)

    st.pyplot(fig_bar)

    # =========================
    # 📥 DESCARGA
    # =========================
    fig.savefig("grafico.png", dpi=600, bbox_inches='tight')

    with open("grafico.png", "rb") as file:
        st.download_button("⬇️ Descargar imagen", file, "grafico_taladros.png")