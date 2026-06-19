import streamlit as st
import numpy as np
from scipy.optimize import linprog, LinearConstraint, Bounds

st.title("Optimización de Producción en una Imprenta")

# Función objetivo: maximizar z = 25x + 50y
# linprog minimiza, por eso usamos los coeficientes negativos
c = [-25, -50]

# Restricciones
A = np.array([
    [1, 1],     # x + y <= 90
    [4, 6],     # 4x + 6y >= 390
    [15, 40]    # 15x + 40y <= 2000
])

# Límites inferiores y superiores
bl = [-np.inf, 390, -np.inf]
bu = [90, np.inf, 2000]

constraints = LinearConstraint(A, bl, bu)

# x >= 0, y >= 0
bounds = Bounds([0, 0], [np.inf, np.inf])

# Resolver
resultado = linprog(
    c=c,
    constraints=constraints,
    bounds=bounds,
    method="highs"
)

st.header("Resultados")

if resultado.success:
    x = resultado.x[0]  # folletos
    y = resultado.x[1]  # afiches
    ganancia = -resultado.fun

    st.success("Se encontró una solución óptima.")

    st.write(f"**Folletos a producir:** {round(x)}")
    st.write(f"**Afiches a producir:** {round(y)}")
    st.write(f"**Ganancia máxima:** ${ganancia:.2f}")

    st.subheader("Verificación de restricciones")

    st.write(f"x + y = {x + y:.2f} ≤ 90")
    st.write(f"4x + 6y = {4*x + 6*y:.2f} ≥ 390")
    st.write(f"15x + 40y = {15*x + 40*y:.2f} ≤ 2000")

else:
    st.error("No se encontró una solución factible.")
    st.write(resultado.message)
