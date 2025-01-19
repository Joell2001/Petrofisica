# Import Python Libraries
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
from PIL import Image
from pathlib import Path
import lasio
import welly


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

# Importar archivo LAS
uploaded_file = st.file_uploader("Sube un archivo LAS", type=["las"])

if uploaded_file is not None:
    try:
        las = lasio.read(uploaded_file.read().decode("utf-8"))

        st.write("### Información del archivo LAS")
        st.write("Campo: Volve (Noruega)")
        st.text(f"Versión LAS: {las.version[0].value}")
        st.text(f"Nombre del pozo: {las.well.WELL.value}")

        # Mostrar el coentenido del archivo
        st.write("### Contenido del archivo")
        st.text(", ".join(las.keys()))

        # Convertir el contenido a un DataFrame
        las_df = las.df()

        # Mostrar una vista previa del DataFrame
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
    except Exception as e:
        st.error(f"No se pudo procesar el archivo LAS: {e}")
else:
    st.info("Por favor, carga un archivo LAS para continuar.")

