import streamlit as st
from scipy.optimize import linprog

st.title("Optimización de Producción en una Imprenta")

# Maximizar Z = 25x + 50y
# linprog minimiza, por eso usamos coeficientes negativos
c = [-25, -50]

# Restricciones:
# x + y <= 90
# 4x + 6y >= 390  ->  -4x - 6y <= -390
# 15x + 40y <= 2000

A_ub = [
    [1, 1],
    [-4, -6],
    [15, 40]
]

b_ub = [
    90,
    -390,
    2000
]

bounds = [
    (0, None),  # x >= 0
    (0, None)   # y >= 0
]

resultado = linprog(
    c=c,
    A_ub=A_ub,
    b_ub=b_ub,
    bounds=bounds,
    method="highs"
)

st.header("Resultados")

if resultado.success:
    x = resultado.x[0]
    y = resultado.x[1]
    ganancia = -resultado.fun

    st.success("Se encontró una solución óptima")

    st.write(f"**Folletos a producir:** {round(x)}")
    st.write(f"**Afiches a producir:** {round(y)}")
    st.write(f"**Ganancia máxima:** ${ganancia:.2f}")

    st.subheader("Verificación de restricciones")

    st.write(f"x + y = {x + y:.2f} ≤ 90")
    st.write(f"4x + 6y = {4*x + 6*y:.2f} ≥ 390")
    st.write(f"15x + 40y = {15*x + 40*y:.2f} ≤ 2000")

else:
    st.error("No se encontró una solución factible")
    st.write(resultado.message)
