import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Spotify", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")   # Cambia al nombre real
    df["Release Date"] = pd.to_datetime(df["Release Date"], errors="coerce")

    # Convertir streams a numéricos (están como object)
    numeric_cols = [
        "Spotify Streams", "Spotify Playlist Reach", "YouTube Likes",
        "TikTok Posts", "TikTok Likes", "TikTok Views",
        "AirPlay Spins", "Amazon Playlist Count", "Pandora Track Stations",
        "Soundcloud Streams", "Shazam Counts"
    ]
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    return df

df = load_data()

st.title("Dashboard Spotify 📈")

# ---- SIDEBAR -------------------------------------------------------

st.sidebar.header("Filtros")

# lista artistas
artists_list = ["Todos"] + sorted(df["Artist"].dropna().unique().tolist())
artist_filter = st.sidebar.selectbox("Artista", artists_list)

# año
years = df["Release Date"].dt.year.dropna().unique()
years_list = ["Todos"] + sorted(years.tolist())
year_filter = st.sidebar.selectbox("Año (Release Date)", years_list)

# posición (index de la tabla)
max_pos = max(1, len(df))
position = st.sidebar.number_input(
    "¿Qué fila quieres consultar?",
    min_value=1,
    max_value=max_pos,
    value=1,
    step=1
)

# top N
top_n = st.sidebar.slider("Top N (por Spotify Streams)", min_value=1, max_value=max_pos, value=10)

# ---- FILTROS -------------------------------------------------------

filtered = df.copy()

# artista
if artist_filter != "Todos":
    filtered = filtered[ filtered["Artist"] == artist_filter ]

# año
if year_filter != "Todos":
    filtered = filtered[ filtered["Release Date"].dt.year == int(year_filter) ]

st.subheader("Resultados filtrados")
st.write(filtered)

# ---- REGISTRO INDIVIDUAL ------------------------------------------

st.subheader("Registro individual")

pos = min(position, len(filtered)) - 1
if len(filtered) > 0:
    st.write(filtered.iloc[pos])
else:
    st.warning("No hay registros con ese filtro.")

# ---- TOP ----------------------------------------------------------

st.subheader(f"Top {top_n} por Spotify Streams")

top_data = (
    filtered
    .sort_values(by="Spotify Streams", ascending=False)
    .head(top_n)
)

st.write(top_data)
