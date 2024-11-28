from navigation import make_sidebar
import streamlit as st
import pandas as pd
from time import sleep
from pages.back_util_functions import Gestion_Servicios, Gestion_Vehiculos
import logging
from streamlit.logger import get_logger

logging.getLogger("streamlit").setLevel(logging.ERROR)

make_sidebar()

# Variables iniciales en session_state
st.session_state.df_temp_services = False

if 'reset_services' not in st.session_state:
    st.session_state.reset_services = False

def btn_iniciar_servicio(dataframe_in, dict_in):
    transaccion = Gestion_Servicios()
    transaccion.cargar_servicio_vehiculo(dataframe_in, dict_in)
    return

placas = Gestion_Vehiculos()
placas = placas.listado_placas_clientes()
st.header("Crear entradas a lavadero")

left, middle, right = st.columns(3)

vehiculo = left.selectbox('Vehículo (Placa)', options=placas.keys(),  key="selectbox_2")
tipo_vehiculo_input = middle.text_input('Tipo de Vehículo', value=placas[vehiculo][2], disabled=True)
cedula = middle.text_input('Cédula Propietario', value=placas[vehiculo][0], disabled=True)
categoria_input = right.text_input('Categoría', value=placas[vehiculo][3], disabled=True)
nombre = right.text_input('Nombre Propietario', value=placas[vehiculo][1], disabled=True)

servicios_precios = Gestion_Servicios()
servicios_precios = servicios_precios.diccionario_precios_categoria()

if st.session_state.reset_services:
    st.session_state.selected_services = []
    st.session_state.selected_aditionals_services = []
    st.session_state.reset_services = False

servicios = st.multiselect(
    'Seleccione los servicios',
    servicios_precios[placas[vehiculo][2]][placas[vehiculo][3]].keys(),
    default=st.session_state.get('selected_services', []),
    key='selected_services')

servicios_adicionales = st.multiselect(
    'Seleccione los servicios adicionales',
    servicios_precios[placas[vehiculo][2]]['General'].keys(),
    default=st.session_state.get('selected_aditionals_services', []),
    key='selected_aditionals_services')

dict_temp_services =  {
    'id_vehiculo' : placas[vehiculo][5],
    'placa' : vehiculo,
    'tipo_vehiculo': placas[vehiculo][2],
    'categoria': placas[vehiculo][3],
    'id_cliente' : placas[vehiculo][4],
    'cedula' : placas[vehiculo][0],
    'servicio': servicios+servicios_adicionales
}

if len(dict_temp_services['servicio']) > 0:
    st.subheader('Resumen')
    if not st.session_state.df_temp_services:
        servicios_temp = Gestion_Servicios()
        df_servicios_temp = servicios_temp.dataframe_temp_services(dict_temp_services)
        st.dataframe(df_servicios_temp[['servicio', 'precio_formateado']],
                     column_config={
                        "servicio": st.column_config.TextColumn("Servicios", default="st.", width='large'),
                        "precio_formateado": st.column_config.TextColumn("Precio", default="st.")
                    })
        st.session_state.df_temp_services = True
        if "btn_init_service" not in st.session_state:
            if st.button('Iniciar Servicio', type='primary'):
                btn_iniciar_servicio(df_servicios_temp, dict_temp_services)
                st.toast('Se ha iniciado un servicio exitosamente')
                sleep(1)
                st.session_state.reset_services = True
                st.rerun()
else:
    st.session_state.df_temp_services = False