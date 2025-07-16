import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import datetime

st.set_page_config(page_title="Distribución tipo Gauss", layout="centered")
st.title("🎯 Generador de Distribución tipo Campana de Gauss")

# Inputs
n = st.slider("Número de puntos (ej. semanas)", 5, 100, 52)
cajas_totales = st.number_input("Cajas totales", min_value=0, max_value=5_000_000, value=100_000, step=1000)
mean = st.slider("Media (centro)", 1, n, n // 2)
std = st.slider("Desviación estándar (anchura)", 1, n // 2, n // 6)

# Cálculos
x = np.arange(1, n + 1)
gaussian = np.exp(-0.5 * ((x - mean) / std) ** 2)
percentages = gaussian / gaussian.sum() * 100
cajas = (percentages / 100) * cajas_totales

# Crear DataFrame vertical (para mostrar en pantalla)
df = pd.DataFrame({
    'X': x,
    'Porcentaje (%)': np.round(percentages, 2),
    'Cajas estimadas': np.round(cajas, 0)
})

# Mostrar tabla
st.dataframe(
    df.style.format({
        "Porcentaje (%)": "{:.2f}",
        "Cajas estimadas": "{:,.0f}"
    }),
    use_container_width=True
)

# Gráfico de la curva
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x, percentages, color='blue')
ax.fill_between(x, 0, percentages, color='blue', alpha=0.3)
ax.set_xlabel("Valor")
ax.set_ylabel("Porcentaje (%)")
ax.set_title("Curva de Gauss")
ax.grid(True)
st.pyplot(fig)

# Mostrar la descripción en la app debajo del gráfico
descripcion = st.text_area("📝 Descripción de la distribución (opcional)", height=150)
if descripcion.strip():
    st.markdown("### 📝 Descripción")
    st.markdown(descripcion)

# Guardar gráfico como imagen PNG en memoria
img_buffer = io.BytesIO()
fig.savefig(img_buffer, format='png')
plt.close(fig)
img_buffer.seek(0)

# Nombre del archivo con fecha
hoy = datetime.date.today().isoformat()
nombre_archivo = f"distribucion_gauss_{hoy}.xlsx"

# Crear DataFrame horizontal para Excel
headers = [f"X{i}" for i in x]
horizontal_df = pd.DataFrame([
    np.round(percentages, 2),
    np.round(cajas, 0)
], index=["Porcentaje (%)", "Cajas estimadas"], columns=headers)

# Crear archivo Excel en memoria
excel_buffer = io.BytesIO()
with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
    horizontal_df.to_excel(writer, sheet_name='Distribución Horizontal')
    worksheet = writer.sheets['Distribución Horizontal']

    # Insertar gráfico
    worksheet.insert_image(len(horizontal_df.index) + 3, 0, 'grafico.png', {'image_data': img_buffer})

    # Insertar descripción (columna I o 9)
    if descripcion.strip():
        worksheet.write(len(horizontal_df.index) + 3, 8, "Descripción:")
        for i, linea in enumerate(descripcion.splitlines()):
            worksheet.write(len(horizontal_df.index) + 4 + i, 8, linea)

excel_buffer.seek(0)

# Botón de descarga
st.download_button(
    label="📥 Descargar Excel con gráfico y descripción",
    data=excel_buffer,
    file_name=nombre_archivo,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Resumen
st.markdown(f"🔢 **Suma total de porcentajes:** {percentages.sum():.2f}%")
st.markdown(f"📦 **Suma total de cajas estimadas:** {cajas.sum():,.0f}")
