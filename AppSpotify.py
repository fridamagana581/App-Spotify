import streamlit as st
import pandas as pd

# ----------- CARGA DEL DATASET DESDE GITHUB RAW --------------
df = pd.read_csv(
    "https://raw.githubusercontent.com/fridamagana581/App-Spotify/main/Spotify_clean.csv",
    encoding="latin1"
)

# ----------- Limpieza mínima ----------- 
# Aseguramos tipos numéricos
num_cols = [
    "Spotify Streams","Spotify Playlist Reach","YouTube Likes","TikTok Posts",
    "TikTok Likes","TikTok Views","AirPlay Spins","Amazon Playlist Count",
    "Pandora Track Stations","Soundcloud Streams","Shazam Counts"
]

for col in num_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Release Date a fecha
if "Release Date" in df.columns:
    df["Release Date"] = pd.to_datetime(df["Release Date"], errors="coerce")

# quitamos NaN
df = df.dropna().reset_index(drop=True)

# ------------- STREAMLIT ----------------

st.title("🎧 Spotify Analysis 2024")

st.write("Dataset total:", len(df), "canciones")

# ----------- SIDEBAR -----------

st.sidebar.header("Filtros")

## Filtro artista
if "Artist" in df.columns:
    artists = ["Todos"] + sorted(df["Artist"].unique())
    artist_filter = st.sidebar.selectbox("Artista", artists)
else:
    artist_filter = "Todos”

## Filtro año
if "Release Date" in df.columns:
    years = sorted(df["Release Date"].dt.year.unique())
    year_filter = st.sidebar.selectbox("Año", ["Todos"] + list(years))
else:
    year_filter = "Todos"

## Ordenar por
order_column = st.sidebar.selectbox(
    "Ordenar por:",
    df.select_dtypes(include=['float64', 'int64', 'int']).columns
)

## TOP N seguro
max_top = max(10, len(df))   # evita error
top_n = st.sidebar.slider(
    "Top N",
    min_value=5,
    max_value=max_top,
    value=min(10, max_top)
)


# ----------- APLICAR FILTROS ------------

df_view = df.copy()

if artist_filter != "Todos":
    df_view = df_view[df_view["Artist"] == artist_filter]

if year_filter != "Todos":
    df_view = df_view[df_view["Release Date"].dt.year == int(year_filter)]

# ----------- ORDENAR ------------
df_view = df_view.sort_values(by=order_column, ascending=False)


# ----------- TABLA GENERAL ------------
st.subheader("Tabla filtrada")
st.dataframe(df_view)


# ----------- TOP N ------------
top_df = df_view.head(top_n)

st.subheader(f"Top {top_n} por {order_column}")
st.dataframe(top_df)


# ----------- CONSULTA POR POSICIÓN ------------
df_len = len(df)
max_pos = max(1, df_len)

position = st.sidebar.number_input(
    "¿Qué posición quieres consultar?",
    min_value=1,
    max_value=max_pos,
    value=1
)

st.subheader(f"Canción en posición #{position}")
try:
    st.write(df_view.iloc[int(position)-1])
except:
    st.write("No existe esa posición en este filtro")


# ----------- GRAFICAAA ------------
st.subheader("Gráfica TOP seleccionada")
st.bar_chart(top_df.set_index("Track")[order_column])
