from navigation import make_sidebar
import streamlit as st
import pandas as pd
from pages.back_util_functions import Gestion_Servicios, Gestion_Vehiculos

make_sidebar()

placas = Gestion_Vehiculos()
placas = placas.listado_placas_clientes()
st.header("Crear entradas a lavadero")

left, middle, right = st.columns(3)

vehiculo = left.selectbox('Vehículo (Placa)', options=placas.keys(),  key="selectbox_2")
cedula = middle.text_input('Cédula Propietario', value=placas[vehiculo][0], disabled=True)
nombre = right.text_input('Nombre Propietario', value=placas[vehiculo][1], disabled=True)

servicios_precios = Gestion_Servicios()
servicios_precios = servicios_precios.diccionario_precios_categoria()

servicios = st.multiselect('Seleccione los servicios', servicios_precios[placas[vehiculo][2]][placas[vehiculo][3]].keys())
servicios_adicionales = st.multiselect('Seleccione los servicios adicionales', servicios_precios[placas[vehiculo][2]]['General'].keys())

