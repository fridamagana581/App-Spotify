import streamlit as st
import pandas as pd

# -----------------------------
# CONFIGURACIÓN DE PÁGINA
# -----------------------------
st.set_page_config(layout="wide")
st.title("🎵 Spotify Analytics Dashboard – Dataset Limpio + Tops con Filtros")

st.write("""
Esta aplicación carga, limpia y analiza el dataset **Most Streamed Spotify Songs 2024**, 
y presenta 4 análisis tipo *Top 10*, todos con los mismos filtros:  
**Artista, Año, Streams y Track Score**.
""")


# -----------------------------
# 1. CARGAR ARCHIVO ORIGINAL
# -----------------------------
st.header("1. Cargar datos originales")

df = pd.read_csv("Most Streamed Spotify Songs 2024.csv", encoding="latin1")
st.dataframe(df.head())


# -----------------------------
# 2. PROCESO DE LIMPIEZA
# -----------------------------
st.header("2. Limpieza del dataset")

# Asegurar formato de fecha
df["Release Date"] = pd.to_datetime(df["Release Date"], errors="coerce")

# Crear columna Release Year desde Release Date
df["Release Year"] = df["Release Date"].dt.year

# Limpiar Spotify Streams
df["Spotify Streams"] = (
    df["Spotify Streams"]
    .astype(str)
    .str.replace(",", "")
    .str.replace(".", "")
)

df["Spotify Streams"] = pd.to_numeric(df["Spotify Streams"], errors="coerce")

# Convertir Track Score a numérico
df["Track Score"] = pd.to_numeric(df["Track Score"], errors="coerce")

# Eliminar filas sin datos importantes
df = df.dropna(subset=["Artist", "Release Year", "Spotify Streams", "Track Score"])

st.success("Dataset limpiado correctamente ✔")
st.dataframe(df.head())


# -----------------------------
# 3. SIDEBAR − FILTROS
# -----------------------------
st.sidebar.header("Filtros")

# Filtro artista
artists = ["Todos"] + sorted(df["Artist"].dropna().unique())
filter_artist = st.sidebar.selectbox("Filtrar por artista:", artists)

# Filtro año
years = ["Todos"] + sorted(df["Release Year"].dropna().unique())
filter_year = st.sidebar.selectbox("Filtrar por año:", years)

# Filtro Spotify Streams
min_streams = int(df["Spotify Streams"].min())
max_streams = int(df["Spotify Streams"].max())

filter_streams = st.sidebar.slider(
    "Filtrar por rango de Spotify Streams:",
    min_value=min_streams,
    max_value=max_streams,
    value=(min_streams, max_streams),
)

# Filtro Track Score
min_score = int(df["Track Score"].min())
max_score = int(df["Track Score"].max())

filter_score = st.sidebar.slider(
    "Filtrar por rango de Track Score:",
    min_value=min_score,
    max_value=max_score,
    value=(min_score, max_score),
)


# -----------------------------
# 4. APLICAR FILTROS AL DATASET
# -----------------------------
df_filtered = df.copy()

if filter_artist != "Todos":
    df_filtered = df_filtered[df_filtered["Artist"] == filter_artist]

if filter_year != "Todos":
    df_filtered = df_filtered[df_filtered["Release Year"] == filter_year]

# Streams
df_filtered = df_filtered[
    (df_filtered["Spotify Streams"] >= filter_streams[0])
    & (df_filtered["Spotify Streams"] <= filter_streams[1])
]

# Track Score
df_filtered = df_filtered[
    (df_filtered["Track Score"] >= filter_score[0])
    & (df_filtered["Track Score"] <= filter_score[1])
]

st.header("📂 Dataset filtrado según los 4 filtros")
st.dataframe(df_filtered)


# -----------------------------
# 5. TOP 1 — MÁS STREAMEADAS
# -----------------------------
st.header("🔥 Top 10 canciones más streameadas – Spotify Streams")

top_streams = df_filtered.sort_values(by="Spotify Streams", ascending=False).head(10)
st.dataframe(top_streams)
