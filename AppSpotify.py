import streamlit as st
import pandas as pd

# ============================
# CARGA DE DATOS
# ============================
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/fridamagana581/App-Spotify/main/Spotify_clean.csv"
    df = pd.read_csv(url, encoding="latin1")

    # Release date
    if "Release Date" in df.columns:
        df["Release Date"] = pd.to_datetime(df["Release Date"], errors="coerce")

    return df

df = load_data()

# Validación
if df.empty:
    st.error("El dataframe está vacío. Revisa el archivo CSV.")
    st.stop()

df = df.reset_index(drop=True)

# ============================
# TITULO
# ============================
st.title("📊 Spotify Best Songs 2024")

# ============================
# SIDEBAR
# ============================
st.sidebar.header("Filtros")

## ARTISTA
artists = ["Todos"] + sorted(df["Artist"].dropna().unique().tolist())
artist_filter = st.sidebar.selectbox("Artista", artists)

## AÑO
years = df["Release Date"].dt.year.dropna().unique()
years = years.astype(int).tolist()
years = sorted(years)
years = ["Todos"] + years
year_filter = st.sidebar.selectbox("Año", years)

## Ordenar por:
numeric_cols = df.select_dtypes(include=["float64", "int64", "int"]).columns.tolist()
order_column = st.sidebar.selectbox("Ordenar por", numeric_cols)

## Top N
top_n = st.sidebar.slider("Top N", min_value=5, max_value=3000, value=10)

# ============================
# APLICAR FILTROS
# ============================
df_view = df.copy()

if artist_filter != "Todos":
    df_view = df_view[df_view["Artist"] == artist_filter]

if year_filter != "Todos":
    df_view = df_view[df_view["Release Date"].dt.year == int(year_filter)]

df_view = df_view.reset_index(drop=True)

# ============================
# POSICIÓN (CUALQUIER RANK)
# ============================
df_len = len(df_view) if len(df_view) > 0 else 1

position = st.sidebar.number_input(
    "¿Qué posición quieres consultar?",
    min_value=1,
    max_value=df_len,
    value=1
)

# ============================
# TABLA
# ============================
st.subheader("Tabla filtrada")
st.dataframe(df_view)

# ============================
# TOP N
# ============================
top_df = df_view.sort_values(by=order_column, ascending=False).head(top_n)

st.subheader(f"Top {top_n} por {order_column}")
st.dataframe(top_df)

# ============================
# CANCIÓN EN LA POSICIÓN
# ============================
st.subheader(f"🎯 Canción en posición {position}")
st.write(df_view.iloc[position - 1])

# ============================
# GRAFICA
# ============================
st.subheader("Gráfica")
st.bar_chart(top_df.set_index("Track")[order_column])
