import streamlit as st
import pandas as pd

# --- Cargar dataset limpio desde GitHub ---
url = "https://raw.githubusercontent.com/fridamagana581/App-Spotify/main/Spotify_clean.csv"
df = pd.read_csv(url, encoding='latin1')

st.title("🎵 Spotify Analysis 2024")

# --- Convertir columnas NUMÉRICAS ---
numeric_cols = ["Spotify Streams", "Track Score"]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df["Release Date"] = pd.to_datetime(df["Release Date"], errors="coerce")

# --- Remover filas con NA en columnas clave ---
df = df.dropna(subset=["Spotify Streams", "Track Score"])

### --- SIDEBAR --- ###
st.sidebar.header("Filtros")

# --- Artist filter ---
artists = ["Todos"] + sorted(df["Artist"].dropna().unique())
artist_filter = st.sidebar.selectbox("Artista:", artists)

# --- Año filter ---
years = ["Todos"] + sorted(df["Release Date"].dt.year.dropna().unique())
year_filter = st.sidebar.selectbox("Año:", years)

# --- Streams slider ---
streams_min = int(df["Spotify Streams"].min())
streams_max = int(df["Spotify Streams"].max())
streams_range = st.sidebar.slider("Rango de Streams", streams_min, streams_max,
                                  (streams_min, streams_max))

# --- Track Score slider ---
score_min = int(df["Track Score"].min())
score_max = int(df["Track Score"].max())
score_range = st.sidebar.slider("Rango Track Score", score_min, score_max,
                                (score_min, score_max))

### --- Aplicar filtros --- ###

df_view = df.copy()

if artist_filter != "Todos":
    df_view = df_view[df_view["Artist"] == artist_filter]

if year_filter != "Todos":
    df_view = df_view[df_view["Release Date"].dt.year == int(year_filter)]

df_view = df_view[
    (df_view["Spotify Streams"] >= streams_range[0]) &
    (df_view["Spotify Streams"] <= streams_range[1]) &
    (df_view["Track Score"] >= score_range[0]) &
    (df_view["Track Score"] <= score_range[1])
]

### --- Mostrar tabla --- ###
st.subheader("🎯 Datos filtrados")
st.dataframe(df_view)

### --- Top N --- ###
top_n = st.sidebar.slider("Top N", 5, 100, 10)

order_column = st.sidebar.selectbox(
    "Ordenar por:",
    ["Spotify Streams", "Track Score"]
)

df_top = df_view.sort_values(by=order_column, ascending=False).head(top_n)

st.subheader(f"🏆 Top {top_n} por {order_column}")
st.dataframe(df_top)

### --- Gráfica --- ###
st.subheader("📊 Gráfica Top")
st.bar_chart(df_top.set_index("Track")[order_column])
