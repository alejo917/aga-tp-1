import streamlit as st
from scipy.optimize import linprog
import pandas as pd

st.set_page_config(
    page_title="Refinería Inteligente",
    page_icon="⛽",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}

h1 {
    color: #1e3a8a;
    text-align: center;
}

h2, h3 {
    color: #0f766e;
}

.stButton > button {
    background-color: #2563eb;
    color: white;
    font-size: 18px;
    border-radius: 10px;
    padding: 10px 20px;
    width: 100%;
}

div[data-testid="stMetric"] {
    background-color: #f1f5f9;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("⛽ Optimización de Producción en una Refinería")

st.markdown("""
Esta aplicación utiliza **Programación Lineal** para determinar la producción óptima de combustibles y maximizar la ganancia de la refinería.
""")

st.header("💰 Ganancia por litro")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    ganancia_premium = st.number_input("⛽ Premium", value=80.0)

with col2:
    ganancia_regular = st.number_input("🚗 Regular", value=60.0)

with col3:
    ganancia_diesel = st.number_input("🚚 Diésel", value=70.0)

with col4:
    ganancia_queroseno = st.number_input("✈️ Queroseno", value=90.0)

with col5:
    ganancia_glp = st.number_input("🔥 GLP", value=75.0)

st.header("🛢️ Consumo de petróleo por litro")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    pet_premium = st.number_input("Premium", value=5.0)

with col2:
    pet_regular = st.number_input("Regular", value=2.0)

with col3:
    pet_diesel = st.number_input("Diésel", value=3.0)

with col4:
    pet_queroseno = st.number_input("Queroseno", value=4.0)

with col5:
    pet_glp = st.number_input("GLP", value=2.5)

st.header("⏱️ Horas de refinación por litro")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    horas_premium = st.number_input("Premium ", value=4.0)

with col2:
    horas_regular = st.number_input("Regular ", value=2.0)

with col3:
    horas_diesel = st.number_input("Diésel ", value=3.0)

with col4:
    horas_queroseno = st.number_input("Queroseno ", value=5.0)

with col5:
    horas_glp = st.number_input("GLP ", value=2.0)

st.header("📦 Recursos disponibles")

col1, col2 = st.columns(2)

with col1:
    petroleo_disponible = st.number_input(
        "🛢️ Petróleo disponible",
        value=1200.0
    )

with col2:
    horas_disponibles = st.number_input(
        "⏱️ Horas de refinación disponibles",
        value=1200.0
    )

st.header("📈 Demanda máxima")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    max_premium = st.number_input("Premium máx.", value=60.0)

with col2:
    max_regular = st.number_input("Regular máx.", value=150.0)

with col3:
    max_diesel = st.number_input("Diésel máx.", value=100.0)

with col4:
    max_queroseno = st.number_input("Queroseno máx.", value=80.0)

with col5:
    max_glp = st.number_input("GLP máx.", value=120.0)

def resolver_modelo():
    c = [
        -ganancia_premium,
        -ganancia_regular,
        -ganancia_diesel,
        -ganancia_queroseno,
        -ganancia_glp
    ]

    A_ub = [
        [
            pet_premium,
            pet_regular,
            pet_diesel,
            pet_queroseno,
            pet_glp
        ],
        [
            horas_premium,
            horas_regular,
            horas_diesel,
            horas_queroseno,
            horas_glp
        ],
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1]
    ]

    b_ub = [
        petroleo_disponible,
        horas_disponibles,
        max_premium,
        max_regular,
        max_diesel,
        max_queroseno,
        max_glp
    ]

    bounds = [
        (0, None),
        (0, None),
        (0, None),
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

st.markdown("---")

if st.button("🚀 Resolver Problema"):

    resultado = resolver_modelo()

    if resultado.success:

        premium = resultado.x[0]
        regular = resultado.x[1]
        diesel = resultado.x[2]
        queroseno = resultado.x[3]
        glp = resultado.x[4]

        ganancia_total = -resultado.fun

        petroleo_utilizado = (
            premium * pet_premium +
            regular * pet_regular +
            diesel * pet_diesel +
            queroseno * pet_queroseno +
            glp * pet_glp
        )

        horas_utilizadas = (
            premium * horas_premium +
            regular * horas_regular +
            diesel * horas_diesel +
            queroseno * horas_queroseno +
            glp * horas_glp
        )

        st.success("✅ Solución óptima encontrada")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "💵 Ganancia Máxima",
                f"${ganancia_total:,.2f}"
            )

        with col2:
            st.metric(
                "🛢️ Petróleo Sobrante",
                f"{petroleo_disponible - petroleo_utilizado:.2f}"
            )

        with col3:
            st.metric(
                "⏱️ Horas Sobrantes",
                f"{horas_disponibles - horas_utilizadas:.2f}"
            )

        st.subheader("🏭 Producción Óptima")

        tabla = pd.DataFrame({
            "Combustible": [
                "Premium",
                "Regular",
                "Diésel",
                "Queroseno",
                "GLP"
            ],
            "Litros a producir": [
                round(premium, 2),
                round(regular, 2),
                round(diesel, 2),
                round(queroseno, 2),
                round(glp, 2)
            ]
        })

        st.dataframe(
            tabla,
            use_container_width=True
        )

        st.subheader("📋 Uso de Recursos")

        st.write(
            f"🛢️ Petróleo utilizado: "
            f"{petroleo_utilizado:.2f} / {petroleo_disponible}"
        )

        st.write(
            f"⏱️ Horas utilizadas: "
            f"{horas_utilizadas:.2f} / {horas_disponibles}"
        )

    else:
        st.error("❌ No se encontró una solución factible")
        st.write(resultado.message)
