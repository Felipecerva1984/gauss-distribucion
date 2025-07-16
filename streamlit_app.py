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

# Mostrar tabla original
df = pd.DataFrame({
    'X': x,
    'Porcentaje (%)': percentages,
    'Cajas estimadas': cajas
})

st.dataframe(
    df.style.format({
        "Porcentaje (%)": "{:.2f}",
        "Cajas estimadas": "{:,.0f}"
    }),
    use_container_width=True
)

# Crear el gráfico
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x, percentages, color='blue')
ax.fill_between(x, 0, percentages, color='blue', alpha=0.3)
ax.set_xlabel("Valor")
ax.set_ylabel("Porcentaje (%)")
ax.set_title("Curva de Gauss")
ax.grid(True)
st.pyplot(fig)

# Guardar gráfico como imagen en memoria
img_buffer = io.BytesIO()
fig.savefig(img_buffer, format='png')
plt.close(fig)
img_buffer.seek(0)

# Generar nombre con fecha
hoy = datetime.date.today().isoformat()
nombre_archivo = f"distribucion_gauss_{hoy}.xlsx"

# Crear nuevo DataFrame horizontal
headers = [f"X{i}" for i in x]
horizontal_df = pd.DataFrame([
    np.round(percentages, 2),
    np.round(cajas, 0)
], index=["Porcentaje (%)", "Cajas estimadas"], columns=headers)


# Crear Excel en memoria
excel_buffer = io.BytesIO()
with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
    horizontal_df.to_excel(writer, sheet_name='Distribución Horizontal')

    # Insertar imagen
    worksheet = writer.sheets['Distribución Horizontal']
    worksheet.insert_image(len(horizontal_df.index) + 3, 0, 'grafico.png', {'image_data': img_buffer})

excel_buffer.seek(0)

# Botón de descarga
st.download_button(
    label="📥 Descargar Excel con gráfico (horizontal)",
    data=excel_buffer,
    file_name=nombre_archivo,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Resumen
st.markdown(f"🔢 **Suma total de porcentajes:** {percentages.sum():.2f}%")
st.markdown(f"📦 **Suma total de cajas estimadas:** {cajas.sum():,.0f}")
