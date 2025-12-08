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

st.markdown

# --- Filtros específicos de esta sección ---
col1, col2 = st.columns(2)

with col1:
    metric_top = st.selectbox(
        "Métrica:",
        ["Spotify Streams", "YouTube Likes", "TikTok Posts", "Shazam Counts"]
    )

with col2:
    n_top_artists = st.number_input(
        "Top N artistas",
        min_value=3,
        max_value=100,
        value=10
    )

# --- Crear el top independiente ---
df_tops = df.copy()

# Agrupar por artista
artist_rank = df_tops.groupby("Artist")[metric_top].sum().reset_index()

# Ordenar y tomar top N
artist_rank = artist_rank.sort_values(by=metric_top, ascending=False).head(n_top_artists)

# Mostrar resultados
st.subheader(f"Top {n_top_artists} artistas por {metric_top} (dataset 2024)")

st.dataframe(artist_rank)

st.bar_chart(artist_rank.set_index("Artist")[metric_top])
