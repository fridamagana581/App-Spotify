import streamlit as st
import pandas as pd

st.set_page_config(page_title="Spotify Analysis", layout="wide")


# -----------------------------
# Cargar datos desde GitHub
# -----------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/fridamagana581/App-Spotify/main/Spotify_limpioo.csv"
    df = pd.read_csv(url, encoding="latin1")

    # Convertir fecha sin hora
    if "Release Date" in df.columns:
        df["Release Date"] = pd.to_datetime(df["Release Date"], errors="coerce").dt.date

    # Crear columna Year para filtros
    df["Year"] = pd.to_datetime(df["Release Date"], errors="coerce").dt.year

    # Convertir numéricos
    numeric_cols = [
        "Spotify Streams",
        "Spotify Playlist Reach",
        "YouTube Likes",
        "TikTok Posts",
        "TikTok Likes",
        "TikTok Views",
        "AirPlay Spins",
        "Amazon Playlist Count",
        "Pandora Track Stations",
        "Soundcloud Streams",
        "Shazam Counts"
    ]

    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    return df


df = load_data()


# -----------------------------
# TITULO
# -----------------------------
st.title("🎵 Spotify Global Analysis")


# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Filtros")

## Filtro artista
artists = ["Todos"] + sorted(df["Artist"].dropna().unique().tolist())
artist_filter = st.sidebar.selectbox("Artista", artists)

## Filtro año
years = ["Todos"] + sorted(df["Year"].dropna().unique().tolist())
year_filter = st.sidebar.selectbox("Año", years)

## Ordenar por métrica numérica
order_col = st.sidebar.selectbox(
    "Ordenar por:",
    df.select_dtypes(include="number").columns.tolist()
)

## Top N dinámico según tamaño
total_rows = len(df)
top_n = st.sidebar.slider("Top N", 1, min(total_rows, 5000), 10)


# -----------------------------
# Aplicar filtros
# -----------------------------
df_view = df.copy()

if artist_filter != "Todos":
    df_view = df_view[df_view["Artist"] == artist_filter]

if year_filter != "Todos":
    df_view = df_view[df_view["Year"] == int(year_filter)]

# Orden
df_view = df_view.sort_values(by=order_col, ascending=False)


# -----------------------------
# Mostrar tabla principal
# -----------------------------
st.subheader("Tabla filtrada (después de aplicar filtros)")
st.dataframe(df_view)


# -----------------------------
# TOP N
# -----------------------------
top_df = df_view.head(top_n)

st.subheader(f"Top {top_n} por {order_col}")
st.dataframe(top_df)

st.bar_chart(top_df.set_index("Track")[order_col])


# -----------------------------
# CONSULTAR POSICIÓN ESPECÍFICA
# -----------------------------
st.subheader("🔍 Buscar una posición exacta")

pos = st.sidebar.number_input(
    "¿Qué posición quieres consultar?",
    min_value=1,
    max_value=len(df_view),
    value=1
)

row = df_view.reset_index(drop=True).iloc[int(pos)-1]

st.write(f"### 🎧 Canción en posición {pos}")
st.write(row)

# ============================================
# SECCIÓN: TOP ARTISTAS MÁS ESCUCHADOS
# ============================================

st.header("🏆 Top artistas más escuchados")

# --- Filtros específicos de esta sección ---
col1, col2 = st.columns(2)

with col1:
    metric_top = st.selectbox(
        "Métrica:",
        ["Spotify Streams", "YouTube Likes", "TikTok Posts", "TikTok Likes", "TikTok Views", "Shazam Counts"]
    )

with col2:
    n_top_artists = st.number_input(
        "Top N artistas",
        min_value=3,
        max_value=200,
        value=10
    )

# --- Crear el top independiente usando TODO el dataset ---
df_tops = df.copy()   # Usa df original, NO usa los filtros del sidebar

# Agrupar por artista
artist_rank = df_tops.groupby("Artist")[metric_top].sum().reset_index()

# Ordenar de mayor a menor
artist_rank = artist_rank.sort_values(by=metric_top, ascending=False).head(n_top_artists)

# Mostrar tabla
st.subheader(f"Top {n_top_artists} artistas por {metric_top}")
st.dataframe(artist_rank)

# --- Gráfica ORDENADA de mayor a menor ---
import altair as alt

chart = alt.Chart(artist_rank).mark_bar().encode(
    y=alt.Y("Artist:N", sort='-x'),  # Ordena de MAYOR a MENOR
    x=alt.X(f"{metric_top}:Q", title=metric_top),
    tooltip=["Artist", metric_top]
).properties(
    width=700,
    height=400
)

st.altair_chart(chart, use_container_width=True)


# ============================================
# SECCIÓN: TOP CANCIONES POR YOUTUBE LIKES
# ============================================

st.header("🏆 Top canciones por Likes en YouTube")

# --- Filtro: Top N canciones ---
n_top_songs = st.number_input(
    "Top N canciones",
    min_value=3,
    max_value=200,
    value=10
)

# --- Métrica fija ---
metric_yt = "YouTube Likes"

# Copia del dataset (sin filtros del sidebar)
df_yt = df.copy()

# Agrupar por canción sumando YouTube Likes
song_rank = df_yt.groupby("Track")[metric_yt].sum().reset_index()

# Orden de mayor a menor + Top N
song_rank = song_rank.sort_values(by=metric_yt, ascending=False).head(n_top_songs)

# Mostrar tabla ordenada
st.subheader(f"Top {n_top_songs} canciones por {metric_yt}")
st.dataframe(song_rank)

# --- Gráfica ORDENADA con Altair ---
import altair as alt

chart_yt = alt.Chart(song_rank).mark_bar().encode(
    y=alt.Y("Track:N", sort='-x'),   # Ordenar de mayor a menor
    x=alt.X(f"{metric_yt}:Q", title=metric_yt),
    tooltip=["Track", metric_yt]
).properties(
    width=700,
    height=400
)

st.altair_chart(chart_yt, use_container_width=True)


st.header("🏆 Top canciones más buscadas en Shazam")

# --- Filtro: Top N canciones ---
n_top_shazam = st.number_input(
    "Top N canciones (Shazam)",
    min_value=3,
    max_value=200,
    value=10
)

# --- Métrica fija ---
metric_shazam = "Shazam Counts"

# Copiar dataset (sin filtros del sidebar)
df_shazam = df.copy()

# Agrupar por canción sumando Shazam Counts
shazam_rank = df_shazam.groupby("Track")[metric_shazam].sum().reset_index()

# Ordenar de mayor a menor + Top N
shazam_rank = shazam_rank.sort_values(by=metric_shazam, ascending=False).head(n_top_shazam)

# Mostrar tabla ordenada
st.subheader(f"Top {n_top_shazam} canciones por {metric_shazam}")
st.dataframe(shazam_rank)

# --- Gráfica ORDENADA con Altair ---
import altair as alt

chart_shazam = alt.Chart(shazam_rank).mark_bar().encode(
    y=alt.Y("Track:N", sort='-x'),   # mayor → menor
    x=alt.X(f"{metric_shazam}:Q", title=metric_shazam),
    tooltip=["Track", metric_shazam]
).properties(
    width=700,
