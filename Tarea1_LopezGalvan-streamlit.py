import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

st.set_page_config(page_title="Serie de Fourier - Señal Triangular", layout="wide")

st.title("Reconstrucción de Onda Triangular vía Series de Fourier")

with st.sidebar:
    st.header("Configuración de Señal")
    A = st.number_input("Amplitud (A)", min_value=0.1, max_value=10.0, value=1.0, step=0.5)
    T0 = st.number_input("Periodo (T0)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    N_terms = st.slider("Número de términos impares (N)", min_value=1, max_value=50, value=5)

L = T0 / 2.0
t = np.linspace(-2 * T0, 2 * T0, 2000)

f_exacta = A * signal.sawtooth(2 * np.pi * (1 / T0) * t + np.pi, width=0.5)

suma = np.zeros_like(t)
for k in range(1, N_terms + 1):
    n = 2 * k - 1
    suma += (1.0 / (n**2)) * np.cos(n * np.pi * t / L)
f_aprox = (8.0 * A / (np.pi**2)) * suma

mse = np.mean((f_exacta - f_aprox)**2)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(t, f_exacta, 'k--', label='Original', alpha=0.5)
ax.plot(t, f_aprox, 'b-', label=f'Serie truncada (N={N_terms})')
ax.set_xlabel('Tiempo [s]')
ax.set_ylabel('Amplitud')
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper right')

st.pyplot(fig)
st.metric("Error Cuadrático Medio (MSE)", f"{mse:.6e}")