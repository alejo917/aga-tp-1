import streamlit as st
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import numpy as np

st.title("Optimización de Mezcla de Combustibles")

st.header("Parámetros del problema")

ganancia_premium = st.number_input(
    "Ganancia por litro de Premium",
    min_value=0.0,
    value=80.0
)

ganancia_regular = st.number_input(
    "Ganancia por litro de Regular",
    min_value=0.0,
    value=60.0
)

st.subheader("Consumo de petróleo")

petroleo_premium = st.number_input(
    "Litros de petróleo requeridos por litro de Premium",
    min_value=0.0,
    value=5.0
)

petroleo_regular = st.number_input(
    "Litros de petróleo requeridos por litro de Regular",
    min_value=0.0,
    value=2.0
)

petroleo_disponible = st.number_input(
    "Petróleo disponible",
    min_value=0.0,
    value=500.0
)

st.subheader("Demanda máxima")

max_premium = st.number_input(
    "Máximo de litros Premium",
    min_value=0.0,
    value=60.0
)

max_regular = st.number_input(
    "Máximo de litros Regular",
    min_value=0.0,
    value=150.0
)


def resolver_modelo(
    ganancia_premium,
    ganancia_regular,
    petroleo_premium,
    petroleo_regular,
    petroleo_disponible,
    max_premium,
    max_regular
):
    c = [-ganancia_premium, -ganancia_regular]

    A_ub = [
        [petroleo_premium, petroleo_regular],
        [1, 0],
        [0, 1]
    ]

    b_ub = [
        petroleo_disponible,
        max_premium,
        max_regular
    ]

    bounds = [
        (0, None),
        (0, None)
    ]

    return linprog(
        c=c,
        A_ub=A_ub,
        b_ub=b_ub,
        bounds=bounds,
        method="highs"
    )


def mostrar_grafico(
    petroleo_premium,
    petroleo_regular,
    petroleo_disponible,
    max_premium,
    max_regular,
    x_opt,
    y_opt
):
    x = np.linspace(0, max_premium + 20, 500)

    y_petroleo = (
        petroleo_disponible - petroleo_premium * x
    ) / petroleo_regular

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.plot(
        x,
        y_petroleo,
        label=f"{petroleo_premium}x + {petroleo_regular}y ≤ {petroleo_disponible}"
    )

    ax.axvline(
        max_premium,
        label=f"x ≤ {max_premium}"
    )

    ax.axhline(
        max_regular,
        label=f"y ≤ {max_regular}"
    )

    ax.scatter(
        x_opt,
        y_opt,
        s=120,
        label="Solución óptima"
    )

    ax.set_xlim(0, max_premium + 20)
    ax.set_ylim(0, max_regular + 20)

    ax.set_xlabel("Litros de Premium (x)")
    ax.set_ylabel("Litros de Regular (y)")
    ax.set_title("Región factible y solución óptima")
    ax.grid(True)
    ax.legend()

    st.pyplot(fig)


if st.button("Resolver"):

    resultado = resolver_modelo(
        ganancia_premium,
        ganancia_regular,
        petroleo_premium,
        petroleo_regular,
        petroleo_disponible,
        max_premium,
        max_regular
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

        st.write(
            f"Petróleo utilizado: "
            f"{petroleo_premium * x + petroleo_regular * y:.2f} "
            f"≤ {petroleo_disponible}"
        )

        st.write(
            f"Premium producido: {x:.2f} ≤ {max_premium}"
        )

        st.write(
            f"Regular producido: {y:.2f} ≤ {max_regular}"
        )

        st.subheader("Gráfico")

        mostrar_grafico(
            petroleo_premium,
            petroleo_regular,
            petroleo_disponible,
            max_premium,
            max_regular,
            x,
            y
        )

    else:
        st.error("No se encontró una solución factible")
        st.write(resultado.message)
