import streamlit as st
from scipy.optimize import linprog

st.title("Optimización de Producción en una Imprenta")

st.header("Función Objetivo")

ganancia_x = st.number_input("Ganancia por Folleto (x)", value=25.0)
ganancia_y = st.number_input("Ganancia por Afiche (y)", value=50.0)

st.header("Restricciones")

r1_x = st.number_input("Restricción 1 - Coeficiente de x", value=1.0)
r1_y = st.number_input("Restricción 1 - Coeficiente de y", value=1.0)
r1_b = st.number_input("Restricción 1 - Límite", value=90.0)

r2_x = st.number_input("Restricción 2 - Coeficiente de x", value=-4.0)
r2_y = st.number_input("Restricción 2 - Coeficiente de y", value=-6.0)
r2_b = st.number_input("Restricción 2 - Límite", value=-390.0)

r3_x = st.number_input("Restricción 3 - Coeficiente de x", value=15.0)
r3_y = st.number_input("Restricción 3 - Coeficiente de y", value=40.0)
r3_b = st.number_input("Restricción 3 - Límite", value=2000.0)

if st.button("Resolver"):

    c = [-ganancia_x, -ganancia_y]

    A_ub = [
        [r1_x, r1_y],
        [r2_x, r2_y],
        [r3_x, r3_y]
    ]

    b_ub = [
        r1_b,
        r2_b,
        r3_b
    ]

    bounds = [
        (0, None),
        (0, None)
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

        st.write(f"Restricción 1: {r1_x*x + r1_y*y:.2f} ≤ {r1_b}")
        st.write(f"Restricción 2: {r2_x*x + r2_y*y:.2f} ≤ {r2_b}")
        st.write(f"Restricción 3: {r3_x*x + r3_y*y:.2f} ≤ {r3_b}")

    else:
        st.error("No se encontró una solución factible")
        st.write(resultado.message)
