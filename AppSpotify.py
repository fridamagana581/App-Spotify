import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("🎵 Spotify Data Cleaning & Dashboard App")

st.write("""
Esta app muestra el proceso de limpieza del dataset **Most Streamed Spotify Songs 2024**
y permite interactuar con él mediante filtros y gráficas.
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
    'TIDAL Popularity', 'Explicit Track', 'Pandora Streams',
    'Deezer Playlist Count', 'Deezer Playlist Reach', 'SiriusXM Spins',
    'Spotify Playlist Count', 'ISRC', 'Track Score'
]

df = df.drop(columns=columns_to_drop)
st.dataframe(df.head())


# -------------------------
# 3. Segunda limpieza
# -------------------------
st.header("3. Eliminar columnas adicionales")

columns_to_drop.extend([
    'AirPlay Spins', 'Amazon Playlist Count', 'Pandora Track Stations',
    'Soundcloud Streams', 'TikTok Views', 'TikTok Posts', 'TikTok Likes'
])

df = df.drop(columns=columns_to_drop, errors='ignore')
st.dataframe(df.head())


# -------------------------
# 4. Filas con NaN
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
    'YouTube Views', 'YouTube Playlist Reach', 'Apple Music Playlist Count'
])

df = df.drop(columns=columns_to_drop, errors='ignore')

# Limpiar Spotify Streams
df["Spotify Streams"] = (
    df["Spotify Streams"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.replace(".", "", regex=False)
)

df["Spotify Streams"] = pd.to_numeric(df["Spotify Streams"], errors="coerce")

# Crear columna de año (sin comas, sin errores)
df["Year"] = df["Release Date"].dt.year.astype(int)

# Mostrar dataset final limpio
st.header("📂 Dataset limpio (General) - Después de la limpieza")
st.dataframe(df.head())

# Mensaje de éxito (EN EL LUGAR CORRECTO)
st.success("¡Limpieza completada con éxito! 🎉")


# ---------------------------------------
# 9. Sidebar con Filtros
# ---------------------------------------

st.sidebar.header("Filtros")

# Filtro artistas
artist_list = ["Todos"] + sorted(df["Artist"].dropna().unique())
artist_selected = st.sidebar.selectbox("Seleccionar artista:", artist_list)

# Filtro año
year_list = ["Todos"] + sorted(df["Year"].unique())
year_selected = st.sidebar.selectbox("Seleccionar año:", year_list)

# Filtro streams
streams_min = int(df["Spotify Streams"].min())
streams_max = int(df["Spotify Streams"].max())

streams_range = st.sidebar.slider(
    "Rango de streams:",
    min_value=streams_min,
    max_value=streams_max,
    value=(streams_min, streams_max)
)

# Filtro género si existe
if "Genre" in df.columns:
    genre_list = ["Todos"] + sorted(df["Genre"].dropna().unique())
    genre_selected = st.sidebar.selectbox("Seleccionar género:", genre_list)
else:
    genre_selected = "Todos"

# Mostrar tabla filtrada
show_filtered = st.sidebar.checkbox("Mostrar datos filtrados", value=False)


# ---------------------------------------
# 10. Botón mostrar / ocultar dataset general
# ---------------------------------------

st.header("📁 Mostrar / Ocultar dataset completo")

if "show_df" not in st.session_state:
    st.session_state["show_df"] = False

if st.button("Mostrar / Ocultar dataset"):
    st.session_state["show_df"] = not st.session_state["show_df"]

if st.session_state["show_df"]:
    st.dataframe(df)
else:
    st.info("Presiona el botón para ver el dataset completo.")


# ---------------------------------------
# 11. Aplicar filtros
# ---------------------------------------
df_filtered = df.copy()

if artist_selected != "Todos":
    df_filtered = df_filtered[df_filtered["Artist"] == artist_selected]

if year_selected != "Todos":
    df_filtered = df_filtered[df_filtered["Year"] == year_selected]

if genre_selected != "Todos":
    df_filtered = df_filtered[df_filtered["Genre"] == genre_selected]

df_filtered = df_filtered[
    (df_filtered["Spotify Streams"] >= streams_range[0]) &
    (df_filtered["Spotify Streams"] <= streams_range[1])
]


# ---------------------------------------
# 12. Mostrar tabla filtrada
# ---------------------------------------
if show_filtered:
    st.header("📊 Tabla filtrada")
    st.dataframe(df_filtered)
else:
    st.info("Activa 'Mostrar datos filtrados' en el sidebar para ver la tabla filtrada.")


# ---------------------------------------
# 13. Gráficas
# ---------------------------------------

st.header("📈 Visualizaciones")

# Top 10 canciones
st.subheader("🎵 Top 10 canciones más streameadas")
top10 = df_filtered.sort_values(by="Spotify Streams", ascending=False).head(10)
if len(top10) > 0:
    st.bar_chart(top10.set_index("Track")["Spotify Streams"])
else:
    st.warning("No hay datos para mostrar en este gráfico.")

# Streams por artista
st.subheader("🎤 Streams por artista")
artist_group = df_filtered.groupby("Artist")["Spotify Streams"].sum().sort_values(ascending=False).head(20)
if len(artist_group) > 0:
    st.bar_chart(artist_group)
else:
    st.warning("No hay datos para mostrar en este gráfico.")

# Streams por año
st.subheader("📅 Streams por año")
year_group = df_filtered.groupby("Year")["Spotify Streams"].sum()
if len(year_group) > 0:
    st.line_chart(year_group)
else:
    st.warning("No hay datos para mostrar en este gráfico.")
