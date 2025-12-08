import streamlit as st
import pandas as pd

# --- Cargar dataset limpio desde GitHub ---
url = "https://raw.githubusercontent.com/fridamagana581/App-Spotify/main/Spotify_clean.csv"
df = pd.read_csv(url, encoding='latin1')

st.title("🎵 Spotify Analysis 2024")

### --- Sidebar: Filtros básicos --- ###
st.sidebar.header("Filtros")

# Filtro por artista
artists = ["Todos"] + sorted(df["Artist"].dropna().unique())
artist_filter = st.sidebar.selectbox("Artista:", artists)

# Filtro por año de release
df["Release Date"] = pd.to_datetime(df["Release Date"], errors="coerce")
years = ["Todos"] + sorted(df["Release Date"].dt.year.dropna().unique())
year_filter = st.sidebar.selectbox("Año:", years)

# Filtro por Streams
streams_min = int(df["Spotify Streams"].min())
streams_max = int(df["Spotify Streams"].max())
streams_range = st.sidebar.slider("Rango de Streams:", streams_min, streams_max, (streams_min, streams_max))

# Filtro por Track Score
score_min = int(df["Track Score"].min())
score_max = int(df["Track Score"].max())
score_range = st.sidebar.slider("Rango de Track Score:", score_min, score_max, (score_min, score_max))

### --- Aplicar filtros --- ###
df_filtered = df.copy()

if artist_filter != "Todos":
    df_filtered = df_filtered[df_filtered["Artist"] == artist_filter]

df_filtered = df_filtered[
    (df_filtered["Release Date"].dt.year == int(year_filter)) &
    (df_filtered["Spotify Streams"] >= streams_range[0]) &
    (df_filtered["Spotify Streams"] <= streams_range[1]) &
    (df_filtered["Track Score"] >= score_range[0]) &
    (df_filtered["Track Score"] <= score_range[1])
]

### --- Mostrar tabla filtrada --- ###
st.subheader("🎯 Datos filtrados")
st.dataframe(df_filtered)

### --- Top N dinámico --- ###
top_n = st.sidebar.slider("Top N canciones:", 5, 100, 10)

order_column = st.sidebar.selectbox("Ordenar por:", ["Spotify Streams","Track Score"] + 
                                     [col for col in df.columns if "TikTok Posts" in col or "YouTube Views" in col])

df_top = df_filtered.sort_values(by=order_column, ascending=False).head(top_n)

st.subheader(f"🏆 Top {top_n} por {order_column}")
st.dataframe(df_top)

st.subheader("📊 Gráfica Top")
st.bar_chart(df_top.set_index("Track")[order_column])
