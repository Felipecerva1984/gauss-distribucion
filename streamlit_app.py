import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Distribución tipo Gauss", layout="centered")
st.title("🎯 Generador de Distribución tipo Campana de Gauss")

n = st.slider("Número de puntos (ej. semanas)", 10, 100, 52)
x = np.arange(1, n + 1)
mean = st.slider("Media (centro)", 1, n, n // 2)
std = st.slider("Desviación estándar (anchura)", 1, n // 2, n // 6)

gaussian = np.exp(-0.5 * ((x - mean) / std) ** 2)
percentages = gaussian / gaussian.sum() * 100

df = pd.DataFrame({'X': x, 'Porcentaje (%)': percentages})
st.dataframe(df.style.format({"Porcentaje (%)": "{:.2f}"}), use_container_width=True)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x, percentages, color='blue')
ax.fill_between(x, 0, percentages, color='blue', alpha=0.3)
ax.set_xlabel("Valor")
ax.set_ylabel("Porcentaje (%)")
ax.set_title("Curva de Gauss")
ax.grid(True)
st.pyplot(fig)

st.markdown(f"🔢 **Suma total:** {percentages.sum():.2f}%")
