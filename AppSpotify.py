import streamlit as st
import pandas as pd
import altair as alt

#----------------------
# Cargar datos
#----------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Spotify_clean.csv")

    # Convertir a numérico
    df["Spotify Streams"] = pd.to_numeric(df["Spotify Streams"], errors="coerce")

    # Quitar vacíos
    df = df.dropna(subset=["Spotify Streams"])
    
    return df

df = load_data()

#----------------------
# Sidebar
#----------------------
st.sidebar.title("Filtros")

streams_min = int(df["Spotify Streams"].min())
streams_max = int(df["Spotify Streams"].max())

streams_filter = st.sidebar.slider(
    "Spotify Streams (mín–máx)",
    streams_min,
    streams_max,
    (streams_min, streams_max)
)

# Filtrar el DF
df_filtered = df[
    (df["Spotify Streams"] >= streams_filter[0]) &
    (df["Spotify Streams"] <= streams_filter[1])
]

#----------------------
# Título
#----------------------
st.title("Dashboard Spotify 🎧")

st.write("Datos filtrados por número de streams")

# Mostrar tabla
st.dataframe(df_filtered.head(20))


#----------------------
# Gráfica simple
#----------------------
st.subheader("Top canciones por Streams")

top = df_filtered.nlargest(10, "Spotify Streams")

chart = (
    alt.Chart(top)
    .mark_bar()
    .encode(
        x="Spotify Streams",
        y=alt.Y("Track", sort="-x")
    )
)

st.altair_chart(chart, use_container_width=True)
