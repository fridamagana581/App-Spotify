import streamlit as st
import pandas as pd
import altair as alt

# ---------------------
# Cargar datos
# ---------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Spotify_clean.csv")
    return df

df = load_data()

st.title("Dashboard Spotify 🎵")

# =========================
# Sidebar
# =========================
st.sidebar.header("Filtros")

# --- Filtro artista ---
artistas = ["Todos"] + sorted(df["artist_name"].dropna().unique().tolist())
artist_filter = st.sidebar.selectbox("Artista", artistas)

# --- Filtro género ---
generos = ["Todos"] + sorted(df["track_genre"].dropna().unique().tolist())
genre_filter = st.sidebar.selectbox("Género", generos)

# --- Filtro año dinámico (usuario escribe) ---
min_year = int(df["year"].min())
max_year = int(df["year"].max())

year_selected = st.sidebar.number_input(
    "Año (puedes escribir cualquier año como 2020 o 2060)",
    min_value=min_year,
    max_value=max_year,
    value=min_year,
    step=1
)

# ------------------------
# Filtros en el DataFrame
# ------------------------
df_filtered = df.copy()

if artist_filter != "Todos":
    df_filtered = df_filtered[df_filtered["artist_name"] == artist_filter]

if genre_filter != "Todos":
    df_filtered = df_filtered[df_filtered["track_genre"] == genre_filter]

if year_selected:
    df_filtered = df_filtered[df_filtered["year"] == year_selected]

# ------------------------
# Métricas
# ------------------------
st.subheader("Métricas")

st.metric("Total de Canciones", len(df_filtered))

if "popularity" in df_filtered.columns:
    st.metric("Popularidad Promedio",
              round(df_filtered["popularity"].mean(), 2))

# ------------------------
# Gráfica Popularidad
# ------------------------
st.subheader("Popularidad por Canción")

if not df_filtered.empty:
    chart = (
        alt.Chart(df_filtered)
        .mark_bar()
        .encode(
            x=alt.X("track_name:N", sort='-y'),
            y="popularity:Q",
            tooltip=["track_name", "artist_name", "popularity"]
        )
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("No hay datos con esos filtros.")

# ------------------------
# Mostrar tabla
# ------------------------
st.subheader("Tabla de datos filtrados")
st.dataframe(df_filtered)
