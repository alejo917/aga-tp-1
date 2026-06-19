import streamlit as st
from scipy.optimize import linprog

st.title("Optimización de Mezcla de Combustibles")

st.write("""
Una refinería produce dos combustibles:

- Premium (x)
- Regular (y)

Ganancias:
- Premium: $80 por litro
- Regular: $60 por litro
""")

if st.button("Resolver"):

    c = [-80, -60]

    A_ub = [
        [5, 2],
        [1, 0],
        [0, 1]
    ]

    b_ub = [
        500,
        60,
        150
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

        st.write(f"**Litros de combustible Premium:** {x:.2f}")
        st.write(f"**Litros de combustible Regular:** {y:.2f}")
        st.write(f"**Ganancia máxima:** ${ganancia:.2f}")

        st.subheader("Verificación de restricciones")

        st.write(f"Petróleo utilizado: {5*x + 2*y:.2f} ≤ 500")
        st.write(f"Premium producido: {x:.2f} ≤ 60")
        st.write(f"Regular producido: {y:.2f} ≤ 150")

    else:
        st.error("No se encontró una solución factible")
        st.write(resultado.message)
