# app.py
"""
Streamlit Dashboard de Gastos
Proyecto Avanzado: permite subir un CSV de gastos y explorar los datos
con filtros (fechas, categorías) y gráficos interactivos (barras, torta, línea).
Librerías principales: pandas, plotly, streamlit.
"""

from io import StringIO
import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime

# --------- Config UI de la app ----------
st.set_page_config(page_title="Dashboard de Gastos", layout="wide", initial_sidebar_state="expanded")

st.title("📊 Dashboard Interactivo de Gastos")
st.markdown(
    """
Subí un CSV con tus gastos y explorá:  
- filtros por fecha y categoría  
- gráficos interactivos (barras, torta, línea temporal)  
- exportar datos filtrados
"""
)

# --------- Helper: muestra formato esperado del CSV ----------
def sample_csv_md():
    return """
**Formato CSV esperado (ejemplo de columnas):**

- `date` (YYYY-MM-DD) → fecha del gasto  
- `category` → categoría (ej: Comida, Transporte, Suscripciones)  
- `description` → texto libre (opcional)  
- `amount` → número (positivo) en la moneda que uses

Ejemplo:
date,category,description,amount
2024-01-05,Comida,Almuerzo,1200
2024-01-06,Transporte,Subte,350

"""

st.sidebar.header("Instrucciones")
st.sidebar.markdown(sample_csv_md())

# --------- Upload de archivo ----------
uploaded_file = st.sidebar.file_uploader("Subí tu archivo CSV de gastos", type=["csv"])

# --------- Opción de probar con un sample pre-cargado ----------
use_sample = st.sidebar.checkbox("Usar dataset de ejemplo", value=False)

# --------- Si usás sample: construimos un DataFrame de ejemplo ----------
def make_sample_df():
    data = StringIO(
        """date,category,description,amount
2024-01-01,Comida,Desayuno,450
2024-01-02,Transporte,Taxi,900
2024-01-05,Comida,Almuerzo,1200
2024-01-10,Entretenimiento,Cine,800
2024-01-11,Suscripciones,Spotify,499
2024-02-02,Comida,Cena,1600
2024-02-10,Transporte,Colectivo,200
2024-03-01,Hogar,Super,5500
2024-03-15,Salud,Farmacia,1200
2024-03-20,Comida,Cena Amigos,3000
"""
    )
    df = pd.read_csv(data, parse_dates=["date"])
    return df

# --------- Cargar DataFrame según input ----------
df = None
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, parse_dates=["date"])
    except Exception as e:
        st.sidebar.error(f"Error leyendo el CSV: {e}")
        st.stop()
elif use_sample:
    df = make_sample_df()
else:
    st.info("Subí un CSV en la barra lateral o activá 'Usar dataset de ejemplo' para probar la app.")
    st.stop()

# --------- Validaciones y normalizaciones básicas ----------
required_columns = {"date", "category", "amount"}
missing = required_columns - set(df.columns.str.lower())
if missing:
    st.error(f"Tu CSV debe incluir las columnas: {', '.join(required_columns)}. Faltan: {', '.join(missing)}")
    st.stop()

# Normalizar nombres de columnas a minúsculas para evitar errores
df.columns = [c.lower() for c in df.columns]

# Convertir date a datetime si no lo es
if not pd.api.types.is_datetime64_any_dtype(df["date"]):
    try:
        df["date"] = pd.to_datetime(df["date"])
    except Exception as e:
        st.error(f"No se pudo convertir la columna 'date' a fechas: {e}")
        st.stop()

# Asegurar que amount sea numérico
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
if df["amount"].isna().all():
    st.error("La columna 'amount' no contiene valores numéricos válidos.")
    st.stop()

# --------- Sidebar: filtros ----------
st.sidebar.header("Filtros")
min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input("Rango de fechas", value=(min_date, max_date), min_value=min_date, max_value=max_date)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# Categorías dinámicas
all_categories = sorted(df["category"].astype(str).unique())
selected_categories = st.sidebar.multiselect("Categorías", options=all_categories, default=all_categories)

# Opciones de agregación
agg_option = st.sidebar.selectbox("Granularidad temporal", options=["Día", "Semana", "Mes"], index=2)

# --------- Aplicar filtros ----------
mask = (df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date) & (df["category"].astype(str).isin(selected_categories))
df_filtered = df.loc[mask].copy()

st.markdown(f"### ✅ Resumen (filtrado): {len(df_filtered)} registros")
st.write(f"Intervalo: {start_date} → {end_date} — Categorías: {', '.join(selected_categories)}")

# --------- KPI rápidos ----------
col1, col2, col3 = st.columns(3)
total_spent = df_filtered["amount"].sum()
avg_spent = df_filtered["amount"].mean() if len(df_filtered) > 0 else 0.0
count_tx = len(df_filtered)

col1.metric("Total gastado", f"${total_spent:,.2f}")
col2.metric("Transacciones", f"{count_tx}")
col3.metric("Gasto promedio", f"${avg_spent:,.2f}")

# --------- Gráficos principales (Plotly) ----------
st.markdown("## Visualizaciones")

# 1) Línea temporal: gasto por periodo
if len(df_filtered) == 0:
    st.warning("No hay datos para mostrar con los filtros actuales.")
else:
    if agg_option == "Día":
        df_time = df_filtered.groupby(df_filtered["date"].dt.date)["amount"].sum().reset_index()
        df_time["date"] = pd.to_datetime(df_time["date"])
    elif agg_option == "Semana":
        df_time = df_filtered.resample("W-MON", on="date")["amount"].sum().reset_index().sort_values("date")
    else:  # Mes
        df_time = df_filtered.resample("M", on="date")["amount"].sum().reset_index().sort_values("date")

    fig_time = px.line(df_time, x="date", y="amount", markers=True, title="Gasto en el tiempo")
    fig_time.update_layout(yaxis_title="Monto", xaxis_title="Fecha", hovermode="x unified")
    st.plotly_chart(fig_time, use_container_width=True)

    # 2) Barra: gasto por categoría
    df_cat = df_filtered.groupby("category")["amount"].sum().reset_index().sort_values("amount", ascending=False)
    fig_bar = px.bar(df_cat, x="category", y="amount", title="Gasto por categoría", text="amount")
    fig_bar.update_layout(xaxis_title="Categoría", yaxis_title="Monto", xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)

    # 3) Pie: distribución porcentual
    fig_pie = px.pie(df_cat, names="category", values="amount", title="Distribución del gasto por categoría")
    st.plotly_chart(fig_pie, use_container_width=True)

    # 4) Tabla de datos filtrados y opción descarga CSV
    st.markdown("### Tabla — Datos filtrados")
    st.dataframe(df_filtered.sort_values("date", ascending=False).reset_index(drop=True))

    csv = df_filtered.to_csv(index=False).encode("utf-8")
    st.download_button(label="📥 Descargar CSV filtrado", data=csv, file_name="gastos_filtrados.csv", mime="text/csv")

# --------- Footer con notas ----------
st.markdown("---")
st.markdown(
    """
**Notas y buenas prácticas**  
- Este dashboard es para uso educativo. Respetá las políticas de privacidad si usás datos reales.  
- Mejora: integrar subida directa a una base de datos o autenticación para dashboards privados.
"""
)
