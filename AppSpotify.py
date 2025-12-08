import streamlit as st
import pandas as pd
import altair as alt

#----------------------
# Cargar datos
#----------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Spotify_clean.csv")

    numeric_cols = [
        "Spotify Streams",
        "Spotify Playlist Reach",
        "YouTube Likes",
        "TikTok Posts",
        "TikTok Likes",
        "TikTok Views"
    ]

    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna(subset=["Spotify Streams"])
    return df

df = load_data()

#----------------------
# SIDEBAR
#----------------------
st.sidebar.title("Filtros")

# Elegir métrica
metric = st.sidebar.selectbox(
    "Selecciona la métrica",
    [
        "Spotify Streams",
        "Spotify Playlist Reach",
        "YouTube Likes",
        "TikTok Posts",
        "TikTok Likes",
        "TikTok Views"
    ]
)

# Elegir un número (posición en ranking)
position = st.sidebar.number_input(
    "¿Qué posición quieres consultar?",
    min_value=1,
    max_value=len(df),
    value=1
)

#----------------------
# Título
#----------------------
st.title("Dashboard Spotify 🎧")

st.write(f"Mostrando la canción que ocupa la posición {position} según {metric}")

#----------------------
# RANKING automático
#----------------------
df_ranked = df.sort_values(by=metric, ascending=False).reset_index(drop=True)

# obtener la canción en esa posición
song = df_ranked.iloc[position-1]   # menos 1 porque empieza en 0

st.write("### Canción encontrada:")
st.write(song)

#----------------------
# top gráfica
#----------------------
st.subheader(f"Top 10 por {metric}")

top = df_ranked.head(10)

chart = (
    alt.Chart(top)
    .mark_bar()
    .encode(
        x=metric,
        y=alt.Y("Track", sort="-x")
    )
)

st.altair_chart(chart, use_container_width=True)
