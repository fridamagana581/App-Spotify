import pandas as pd
import streamlit as st

file_path = '/content/drive/MyDrive/Herramientas datos/Most Streamed Spotify Songs 2024.csv'
df = pd.read_csv(file_path, encoding='latin1')
display(df.head())

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
display(df.head())

rows_with_nan = df[df.isnull().any(axis=1)]
display(rows_with_nan)

df = df.dropna()
display(df.head())

df = df.reset_index(drop=True)

display(df.dtypes)

df['Release Date'] = pd.to_datetime(df['Release Date'])
display(df.dtypes)

columns_to_drop.extend([
    'YouTube Views',
    'YouTube Playlist Reach',
    'Apple Music Playlist Count'
])
df = df.drop(columns=columns_to_drop, errors='ignore')
display(df.head())

columns_to_drop_for_current_request = [
    'All Time Rank',
    'Spotify Popularity'
]
df = df.drop(columns=columns_to_drop_for_current_request, errors='ignore')
display(df.head())

rows_with_errors = df[df.isnull().any(axis=1)]
display(rows_with_errors)

df = df[df['Release Date'].dt.year == 2024]
display(df.head())



# Cargar dataset (lo puedes cambiar por tu ruta o github raw)
df = pd.read_csv("Most Streamed Spotify Songs 2024.csv")

st.title("Spotify Analysis 2024")

### --- SIDEBAR --- ###
st.sidebar.header("Filtros")

# Artist filter
artists = ["Todos"] + sorted(df["Artist"].unique())
artist_filter = st.sidebar.selectbox("Artista", artists)

# Año del Release Date (si ya lo convertiste)
if "Release Date" in df.columns:
    df["Release Date"] = pd.to_datetime(df["Release Date"])
    year_filter = st.sidebar.selectbox("Año", ["Todos"] + sorted(df["Release Date"].dt.year.unique()))

# Ordenar por columna
order_column = st.sidebar.selectbox(
    "Ordenar por:",
    df.select_dtypes(include=['float64', 'int64', 'int']).columns
)

# Cantidad top
top_n = st.sidebar.slider("Top N", 5, 3000, 10)

### --- FILTROS --- ###

df_view = df.copy()

if artist_filter != "Todos":
    df_view = df_view[df_view["Artist"] == artist_filter]

if "year_filter" in locals() and year_filter != "Todos":
    df_view = df_view[df_view["Release Date"].dt.year == int(year_filter)]

### --- ORDENAR --- ###
df_view = df_view.sort_values(by=order_column, ascending=False)

### --- TABLA --- ###
st.subheader("Tabla filtrada")
st.dataframe(df_view)

### --- TOP N --- ###
top_df = df_view.head(top_n)

st.subheader(f"Top {top_n} por {order_column}")
st.dataframe(top_df)

### --- GRAFICA --- ###
st.bar_chart(top_df.set_index("Track")[order_column])
