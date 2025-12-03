import streamlit as st
import pandas as pd

st.title("🎵 Spotify Data Cleaning App")

st.write("""
Esta app muestra paso a paso cómo se limpia el dataset **Most Streamed Spotify Songs 2024**.
""")

# -------------------------
# 1. Cargar archivo
# -------------------------

st.header("1. Cargar datos originales")

df = pd.read_csv("Most Streamed Spotify Songs 2024.csv", encoding="latin1")
st.dataframe(df.head())

# -------------------------
# 2. Primera limpieza
# -------------------------

st.header("2. Eliminar columnas innecesarias - Primera fase")

columns_to_drop = [
    'TIDAL Popularity',
    'Explicit Track',
    'Pandora Streams',
    'Deezer Playlist Count',
    'Deezer Playlist Reach',
    'SiriusXM Spins',
    'Spotify Playlist Count',
    'ISRC',
    'Track Score'
]

df = df.drop(columns=columns_to_drop)
st.dataframe(df.head())

# -------------------------
# 3. Segunda limpieza
# -------------------------

st.header("3. Eliminar columnas adicionales")

columns_to_drop.extend([
    'AirPlay Spins',
    'Amazon Playlist Count',
    'Pandora Track Stations',
    'Soundcloud Streams',
    'TikTok Views',
    'TikTok Posts',
    'TikTok Likes'
])

df = df.drop(columns=columns_to_drop, errors='ignore')
st.dataframe(df.head())

# -------------------------
# 4. Checar filas con NaN
# -------------------------

st.header("4. Filas con valores faltantes")

rows_with_nan = df[df.isnull().any(axis=1)]
st.dataframe(rows_with_nan)

# -------------------------
# 5. Eliminar NaN
# -------------------------

st.header("5. Eliminar filas con NaN")

df = df.dropna()
st.dataframe(df.head())

# -------------------------
# 6. Convertir tipos
# -------------------------

st.header("6. Convertir Release Date a formato datetime")

df['Release Date'] = pd.to_datetime(df['Release Date'])

st.dataframe(df.head())

# -------------------------
# 7. Última limpieza
# -------------------------

st.header("7. Limpieza final")

columns_to_drop.extend([
    'YouTube Views',
    'YouTube Playlist Reach',
    'Apple Music Playlist Count'
])

df = df.drop(columns=columns_to_drop, errors='ignore')
st.dataframe(df.head())

# -------------------------
# 8. Resultado final
# -------------------------

st.header("🎉 Dataset final limpio")

st.dataframe(df)

st.success("¡Limpieza completada con éxito!")
