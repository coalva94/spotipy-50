# Importaciones
from io import BytesIO
import streamlit as st
from src.extract_spotify import extract_spotify, unique_country


# Configuración de la página
def configurar_pagina():
    st.set_page_config(
        page_title="Top 50 Spotify", page_icon="images/logo.svg", layout="wide"
    )
    st.logo(
        "images/banner_logo.svg",
        link="https://www.spotify.com/",
        icon_image="images/logo.svg",
    )
    st.sidebar.markdown(
        "Este proyecto forma parte de un taller de Python, donde aplicamos técnicas de análisis de datos para estudiar las tendencias musicales en América Latina a través de las playlists Top 50 de Spotify. Utilizamos Streamlit para la visualización interactiva, permitiendo a los usuarios explorar las preferencias musicales por país"
    )


# Mostrar información del proyecto
def mostrar_info_proyecto():
    concepto = """En este proyecto, estamos realizando un análisis de las playlist Top 50 de Spotify para los países de América Latina.
    Nuestro objetivo es obtener una visión más clara de las tendencias musicales en América Latina y ver qué canciones y
    artistas son los más populares en esta región."""
    st.image("images/banner_principal.png", use_column_width=True)
    st.markdown(
        f"<h1 style='text-align: center; color: black;'> ANÁLISIS PLAYLIST TOP 50 DE SPOTIFY</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<h5 style='text-align: justify; color: black; font-weight: normal;'> {concepto}</h5>",
        unsafe_allow_html=True,
    )


# Procesamiento y visualización de datos por país
def procesar_pais(country, df):
    st.markdown(
        f"<h3 style='text-align: center; color: black;'>TOP 50 - {country}</h3>",
        unsafe_allow_html=True,
    )
    df_country = df[df["country"] == country].iloc[:, 1:7].reset_index(drop=True)
    mostrar_datos_pais(df_country, country)


# Mostrar datos y gráficos del país
def mostrar_datos_pais(df_country, country):
    col1, col2 = st.columns([6, 4])
    with col1:
        st.dataframe(
            df_country,
            column_config={"popularity": st.column_config.NumberColumn(format="%d ❤️")},
        )
    df_top10_popular = (
        df_country.sort_values(by="popularity", ascending=False)
        .drop_duplicates(subset=["artists"])
        .head(10)
    )
    with col2:
        st.bar_chart(
            df_top10_popular[["popularity", "artists"]], x="artists", y="popularity",
        )
    descargar_datos_excel(df_country, country)


# Descargar datos como Excel.
def descargar_datos_excel(df_country, country):
    excel_file = BytesIO()
    df_country.to_excel(excel_file, index=False)
    excel_file.seek(0)
    st.download_button(
        "Descargar datos como Excel",
        excel_file,
        f"datos_{country}.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

# Función principal
def main():
    configurar_pagina()
    mostrar_info_proyecto()
    df = extract_spotify()
    countries = unique_country()
    selected_countries = st.multiselect(
        "Selecciona uno o varios paises:", countries, countries[:1]
    )
    for country in selected_countries:
        procesar_pais(country, df)


if __name__ == "__main__":
    main()
