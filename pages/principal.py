from navigation import make_sidebar
import streamlit as st
import pandas as pd
from pages.back_util_functions import Gestion_Servicios, Gestion_Vehiculos

make_sidebar()

st.session_state.df_temp_services = False

placas = Gestion_Vehiculos()
placas = placas.listado_placas_clientes()
st.header("Crear entradas a lavadero")

left, middle, right = st.columns(3)

vehiculo = left.selectbox('Vehículo (Placa)', options=placas.keys(),  key="selectbox_2")
cedula = middle.text_input('Cédula Propietario', value=placas[vehiculo][0], disabled=True)
nombre = right.text_input('Nombre Propietario', value=placas[vehiculo][1], disabled=True)

servicios_precios = Gestion_Servicios()
servicios_precios = servicios_precios.diccionario_precios_categoria()

servicios = st.multiselect('Seleccione los servicios',
                           servicios_precios[placas[vehiculo][2]][placas[vehiculo][3]].keys(),
                           key='selectbox_servicios')
servicios_adicionales = st.multiselect('Seleccione los servicios adicionales', servicios_precios[placas[vehiculo][2]]['General'].keys())

dict_temp_services =  {
    'placa' : vehiculo,
    'tipo_vehiculo': placas[vehiculo][2],
    'categoria': placas[vehiculo][3],
    'cedula' : placas[vehiculo][0],
    'servicio': servicios+servicios_adicionales
}

if len(dict_temp_services['servicio']) > 0:
    st.subheader('Resumen')
    if not st.session_state.df_temp_services:
        servicios_temp = Gestion_Servicios()
        df_servicios_temp = servicios_temp.dataframe_temp_services(dict_temp_services)
        st.dataframe(df_servicios_temp)
        st.session_state.df_temp_services = True
        st.button('Iniciar Servicio', type='primary')
else:
    st.session_state.df_temp_services = False