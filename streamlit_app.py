import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io

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

# Tabla de resultados
df = pd.DataFrame({
    'X': x,
    'Porcentaje (%)': percentages,
    'Cajas estimadas': cajas
})

# Mostrar tabla formateada
st.dataframe(
    df.style.format({
        "Porcentaje (%)": "{:.2f}",
        "Cajas estimadas": "{:,.0f}"
    }),
    use_container_width=True
)

# Botón para descargar Excel
output = io.BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='Distribución')

output.seek(0)  # Muy importante para evitar archivos corruptos

st.download_button(
    label="📥 Descargar Excel",
    data=output,
    file_name="distribucion_gauss.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
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

# Resumen
st.markdown(f"🔢 **Suma total de porcentajes:** {percentages.sum():.2f}%")
st.markdown(f"📦 **Suma total de cajas estimadas:** {cajas.sum():,.0f}")
