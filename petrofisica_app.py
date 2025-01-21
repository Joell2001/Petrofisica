# Import Python Libraries
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
from PIL import Image
from pathlib import Path
import lasio
import welly
import matplotlib.pyplot as plt


# Insert an icon
icon = Image.open("Resources/logo.png")

# State the design of the app
st.set_page_config(page_title="Drill Fluids APP", page_icon=icon)

# Insert css codes to improve the design of the app
st.markdown(
    """
<style>
h1 {text-align: center;
}
body {background-color: #DCE3D5;
      width: 1400px;
      margin: 15px auto;
}
footer {
  display: none;
}
</style>""",
    unsafe_allow_html=True,
)

# Insert title for app
st.title("Petrophysics App")

st.write("---")

# Add information of the app
st.markdown(
    """
  Petrophysics App es una plataforma diseñada para gestionar y analizar registros de pozos en operaciones petroleras. Ofrece herramientas avanzadas para interpretar datos de registros eléctricos, sónicos, densidad, y porosidad, optimizando la caracterización de yacimientos y la identificación de zonas productivas"""


)

# Add additional information
expander = st.expander("Information")
expander.write(
    "This is an open-source web app fully programmed in Python for analyzing and optimizing well log data. It enables the interpretation of petrophysical parameters, such as porosity, fluid saturation, and permeability, supporting real-time decision-making and reservoir characterization."
)

# Insert subheader
st.subheader("**Qué son los registros de pozos?**")
# Insert Image
image = Image.open("Resources/concepto.png")
st.image(image, width=100, use_container_width=True)

#Función para calcular parámetros petrofísicos
def calcular_parametros(las_df):
    # Saturación de agua irreducible
    las_df["SWIRR"] = las_df["SW"] * las_df["BVW"]

    # Porosidad efectiva
    las_df["PHIE"] = las_df["PHIF"] * (1 - las_df["SWIRR"])
    return las_df

# Subir archivo LAS
uploaded_file = st.file_uploader("Sube un archivo LAS", type=["las"])

if uploaded_file is not None:
    try:
        # Leer archivo LAS
        las = lasio.read(uploaded_file.read().decode("utf-8"))

        # Mostrar información básica del archivo
        st.write("### Información del archivo LAS")
        st.write("Campo: Volve (Noruega)")
        st.text(f"Versión LAS: {las.version[0].value}")
        st.text(f"Nombre del pozo: {las.well.WELL.value}")

        # Mostrar contenido del archivo
        st.write("### Contenido del archivo")
        st.text(", ".join(las.keys()))

        # Convertir a DataFrame y mostrar una vista previa
        las_df = las.df()
        st.write("### Datos del archivo LAS")
        st.dataframe(las_df.head(10))

        # Botón para descargar el DataFrame como CSV
        csv = las_df.to_csv().encode('utf-8')
        st.download_button(
            label="Descargar datos como archivo CSV",
            data=csv,
            file_name="datos_volve.csv",
            mime="text/csv",
        )

        # Sección para cálculos petrofísicos
        st.write("## Cálculos Petrofísicos")
        las_df = calcular_parametros(las_df)
        st.write("### Resultados de Cálculos Petrofísicos")
        st.dataframe(las_df[["PHIE", "SWIRR"]].head(10))

        # Agregar sección para graficar registros petrofísicos
        st.write("## Gráficos de registros petrofísicos")
        disponibles = list(las.keys())
        tracks = st.multiselect("Selecciona los tracks que deseas graficar", disponibles, default=["KLOGH", "PHIF", "SAND_FLAG", "SW", "VSH"])

        if tracks:
            fig, axes = plt.subplots(1, len(tracks), figsize=(20, 40))

            for ind, track in enumerate(tracks):
                try:
                    datos = las[track]
                    profundidad = las.index  # Profundidad como índice

                    # Graficar el track seleccionado
                    axes[ind].plot(datos, profundidad)
                    axes[ind].invert_yaxis()  # Eje Y invertido
                    axes[ind].set_title(track)

                except KeyError:
                    st.error(f"No se encontró el track: {track}")

            axes[0].set_ylabel("Profundidad (m)", fontsize=14)
            fig.suptitle("Registros Petrofísicos", fontsize=16)
            fig.tight_layout()

            # Mostrar gráfico en Streamlit
            st.pyplot(fig)
        else:
            st.warning("Por favor, selecciona al menos un track para graficar.")

    except Exception as e:
        st.error(f"No se pudo procesar el archivo LAS: {e}")
else:
    st.info("Por favor, carga un archivo LAS para continuar.")





