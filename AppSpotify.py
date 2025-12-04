import streamlit as st
import pandas as pd

# -----------------------------
# CONFIGURACIÓN DE PÁGINA
# -----------------------------
st.set_page_config(layout="wide")
st.title("🎵 Spotify Analytics Dashboard – Limpieza + Tops con Filtros")

st.write("""
Esta app carga, limpia y analiza el dataset **Most Streamed Spotify Songs 2024**, 
y muestra 4 análisis tipo *Top 10*, filtrables por:  
**Artista, Año, Streams y Track Score.**
""")


# -----------------------------
# 1. CARGAR ARCHIVO ORIGINAL
# -----------------------------
st.header("1. Cargar datos originales")

df = pd.read_csv("Most Streamed Spotify Songs 2024.csv", encoding="latin1")
st.dataframe(df.head())


# -----------------------------
# 2. LIMPIEZA DEL DATASET
# -----------------------------
st.header("2. Limpieza del dataset")

# Convertir Release Year
if "Release Year" in df.columns:
    df["Release Year"] = pd.to_numeric(df["Release Year"], errors="coerce")

# Convertir Spotify Streams
if "Spotify Streams" in df.columns:
    df["Spotify Streams"] = (
        df["Spotify Streams"].astype(str).str.replace(",", "").str.replace(".", "")
    )
    df["Spotify Streams"] = pd.to_numeric(df["Spotify Streams"], errors="coerce")

# Convertir YouTube Views
if "YouTube Views" in df.columns:
    df["YouTube Views"] = (
        df["YouTube Views"].astype(str).str.replace(",", "").str.replace(".", "")
    )
    df["YouTube Views"] = pd.to_numeric(df["YouTube Views"], errors="coerce")

# Convertir TikTok Posts
if "TikTok Posts" in df.columns:
    df["TikTok Posts"] = (
        df["TikTok Posts"].astype(str).str.replace(",", "").str.replace(".", "")
    )
    df["TikTok Posts"] = pd.to_numeric(df["TikTok Posts"], errors="coerce")

# -----------------------------
# 2.1 COLUMNAS OBLIGATORIAS (REVISADAS)
# -----------------------------
cols_required = [
    "Artist Name",
    "Track Name",
    "Release Year",
    "Spotify Streams",
    "Track Score"
]

# 🔥 Filtrar SOLO columnas que sí existan (para evitar errores)
cols_required = [col for col in cols_required if col in df.columns]

df = df.dropna(subset=cols_required)

st.success("Dataset limpiado correctamente ✔")
st.dataframe(df.head())


# -----------------------------
# 3. SIDEBAR – FILTROS
# -----------------------------
st.sidebar.header("Filtros")

# Filtro Artista
artists = ["Todos"] + sorted(df["Artist Name"].unique())
filter_artist = st.sidebar.selectbox("Filtrar por artista:", artists)

# Filtro Año
years = ["Todos"] + sorted(df["Release Year"].dropna().unique())
filter_year = st.sidebar.selectbox("Filtrar por año:", years)

# Filtro Spotify Streams
min_streams = int(df["Spotify Streams"].min())
max_streams = int(df["Spotify Streams"].max())

filter_streams = st.sidebar.slider(
    "Filtrar por rango de Spotify Streams:",
    min_value=min_streams,
    max_value=max_streams,
    value=(min_streams, max_streams)
)

# Filtro Track Score
min_score = int(df["Track Score"].min())
max_score = int(df["Track Score"].max())

filter_score = st.sidebar.slider(
    "Filtrar por rango de Track Score:",
    min_value=min_score,
    max_value=max_score,
    value=(min_score, max_score)
)


# -----------------------------
# 4. APLICAR FILTROS
# -----------------------------
df_filtered = df.copy()

if filter_artist != "Todos":
    df_filtered = df_filtered[df_filtered["Artist Name"] == filter_artist]

if filter_year != "Todos":
    df_filtered = df_filtered[df_filtered["Release Year"] == filter_year]

df_filtered = df_filtered[
    (df_filtered["Spotify Streams"] >= filter_streams[0]) &
    (df_filtered["Spotify Streams"] <= filter_streams[1])
]

df_filtered = df_filtered[
    (df_filtered["Track Score"] >= filter_score[0]) &
    (df_filtered["Track Score"] <= filter_score[1])
]

st.header("📂 Dataset filtrado según los 4 filtros")
st.dataframe(df_filtered)


# -----------------------------
# 5. TOPS ANALÍTICOS
# -----------------------------
st.header("📊 Análisis Top 10")

# -----------------------------
# TOP 1 – MÁS STREAMEADAS
# -----------------------------
st.subheader("🔥 Top 10 canciones más streameadas (Spotify Streams)")
top_streams = df_filtered.sort_values(by="Spotify Streams", ascending=False).head(10)
st.dataframe(top_streams)

# -----------------------------
# TOP 2 – MÁS POPULARES (Track Score o Popularity)
# -----------------------------
st.subheader("⭐ Top 10 canciones más populares (Track Score)")
top_popular = df_filtered.sort_values(by="Track Score", ascending=False).head(10)
st.dataframe(top_popular)

# -----------------------------
# TOP 3 – MÁS VISTAS EN YOUTUBE
# -----------------------------
if "YouTube Views" in df_filtered.columns:
    st.subheader("📺 Top 10 canciones con más vistas en YouTube")
    top_youtube = df_filtered.sort_values(by="YouTube Views", ascending=False).head(10)
    st.dataframe(top_youtube)
else:
    st.warning("El dataset no contiene 'YouTube Views'.")

# -----------------------------
# TOP 4 – MÁS USADAS EN TIKTOK
# -----------------------------
if "TikTok Posts" in df_filtered.columns:
    st.subheader("🎵 Top 10 canciones más usadas en TikTok")
    top_tiktok = df_filtered.sort_values(by="TikTok Posts", ascending=False).head(10)
    st.dataframe(top_tiktok)
else:
    st.warning("El dataset no contiene 'TikTok Posts'.")

