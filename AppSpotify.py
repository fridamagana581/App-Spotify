import streamlit as st
import pandas as pd

### =====================================
### Cargar dataset desde GitHub
### =====================================

url = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/spotify_streams_2024_clean.csv"
df = pd.read_csv(url)

# Convertir fecha
if "Release Date" in df.columns:
    df["Release Date"] = pd.to_datetime(df["Release Date"], errors="coerce")


### =====================================
### TITLE
### =====================================

st.title("Spotify Streaming Analysis 2024")


### =====================================
### SIDEBAR
### =====================================

st.sidebar.header("Filtros")

# Artist
artists = ["Todos"] + sorted(df["Artist"].dropna().unique())
artist_filter = st.sidebar.selectbox("Artista", artists)

# Año del release
if "Release Date" in df.columns:
    years = sorted(df["Release Date"].dt.year.dropna().unique())
    year_filter = st.sidebar.selectbox("Año", ["Todos"] + list(years))

# Orden por columna numerica
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
order_column = st.sidebar.selectbox("Ordenar por:", numeric_cols)

# Top N
top_n = st.sidebar.slider("Top N", 5, 3000, 10)


### =====================================
### APLICAR FILTROS
### =====================================

df_filtered = df.copy()

# filtrar artista
if artist_filter != "Todos":
    df_filtered = df_filtered[df_filtered["Artist"] == artist_filter]

# filtrar año
if "Release Date" in df.columns and year_filter != "Todos":
    df_filtered = df_filtered[df_filtered["Release Date"].dt.year == int(year_filter)]

# ordenar
df_filtered = df_filtered.sort_values(by=order_column, ascending=False)


### =====================================
### TABLA COMPLETA
### =====================================

st.subheader("Tabla filtrada completa")
st.dataframe(df_filtered)


### =====================================
### TOP N
### =====================================

top_df = df_filtered.head(top_n)

st.subheader(f"Top {top_n} por {order_column}")
st.dataframe(top_df)


### =====================================
### GRÁFICA
### =====================================

st.subheader("Visualización")
if "Track" in top_df.columns:
    st.bar_chart(top_df.set_index("Track")[order_column])
