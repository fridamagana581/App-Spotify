import streamlit as st
import pandas as pd

# ------------------------------------
# 1. Cargar datos
# ------------------------------------
st.title("🎵 Spotify Dashboard – 2024")

file_path = "Most Streamed Spotify Songs 2024.csv"
df = pd.read_csv(file_path, encoding='latin1')

st.subheader("Raw dataset")
st.dataframe(df.head())


# ------------------------------------
# 2. Limpiar columnas
# ------------------------------------
all_columns_to_drop = [
    'TIDAL Popularity','Explicit Track','Pandora Streams','Deezer Playlist Count',
    'Deezer Playlist Reach','SiriusXM Spins','Spotify Playlist Count','ISRC','Track Score',
    'AirPlay Spins','Amazon Playlist Count','Pandora Track Stations','Soundcloud Streams',
    'TikTok Views','TikTok Likes','YouTube Views','YouTube Playlist Reach',
    'Apple Music Playlist Count','All Time Rank','Spotify Popularity'
]

df = df.drop(columns=all_columns_to_drop, errors='ignore')

df = df.dropna()

# Convertir fecha
df['Release Date'] = pd.to_datetime(df['Release Date'])

# Filtrar solo 2024
df = df[df['Release Date'].dt.year == 2024]


# ------------------------------------
# 3. Limpiar Streams
# ------------------------------------
df['Spotify Streams'] = (
    df['Spotify Streams']
    .astype(str)
    .str.replace(',', '', regex=False)
)

df['Spotify Streams'] = pd.to_numeric(df['Spotify Streams'], errors='coerce')
df.dropna(subset=['Spotify Streams'], inplace=True)

st.subheader("Dataset limpio 2024")
st.dataframe(df)


# ------------------------------------
# 4. Top artistas por Streams
# ------------------------------------
top_5_artists_2024 = (
    df.groupby('Artist')['Spotify Streams']
    .sum()
    .nlargest(5)
)

st.subheader("🔥 Top 5 Artistas 2024 por Streams")
st.write("En miles de millones")
st.bar_chart(top_5_artists_2024 / 1_000_000_000)


# ------------------------------------
# 5. Top canciones TikTok
# ------------------------------------
if "TikTok Posts" in df.columns:

    df['TikTok Posts'] = (
        df['TikTok Posts']
        .astype(str)
        .str.replace(',', '', regex=False)
    )

    df['TikTok Posts'] = pd.to_numeric(df['TikTok Posts'], errors='coerce')
    df.dropna(subset=['TikTok Posts'], inplace=True)

    top_5_tiktok_songs = (
        df.groupby('Track')['TikTok Posts']
        .sum()
        .nlargest(5)
    )

    st.subheader("📱 Top 5 canciones por TikTok Posts (2024)")
    st.write("En millones")
    st.bar_chart(top_5_tiktok_songs / 1_000_000)

else:
    st.warning("No existe TikTok Posts en el dataset")
