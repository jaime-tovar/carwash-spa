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

if 'reset_custom_services' not in st.session_state:
    st.session_state.reset_custom_services = False

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

if st.session_state.reset_custom_services:
    st.session_state.selected_custom_services = []
    st.session_state.reset_custom_services = False

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

agree_personalizados = st.checkbox('Servicios Personalizados', value=False)

if agree_personalizados:
    servicios_personalizados = st.multiselect('Servicios Personalizados', 
                                              ['PPF','Brillo Headers','Otro'],
                                              default=st.session_state.get('selected_custom_services', []),
                                              key='selected_custom_services')
    col1, col2, col3 = st.columns(3)
    dict_custom_services = {}
    dict_custom_services['servicio'] = []
    dict_custom_services['precio_unitario'] = []
    dict_custom_services['metros'] = []
    if 'PPF' in servicios_personalizados:
        servicio1 = col1.text_input('Servicio', value='PPF', disabled=True)
        servicio1_precio_metro = col2.number_input('Precio por metro', key='servicio1_precio_metro',
                                                   min_value=0, step=1000, format="%d")
        servicio1_metros = col3.number_input('Metros', key='servicio1_metros', min_value=0.0, step=0.5)
        
        dict_custom_services['servicio'].append(servicio1)
        dict_custom_services['precio_unitario'].append(servicio1_precio_metro)
        dict_custom_services['metros'].append(servicio1_metros)
    
    if 'Brillo Headers' in servicios_personalizados:
        servicio2 = col1.text_input('Servicio', value='Brillo Headers', disabled=True)
        servicio2_precio_metro = col2.number_input('Precio por metro', key='servicio2_precio_metro',
                                                   min_value=0, step=1000, format="%d")
        servicio2_metros = col3.number_input('Metros', key='servicio2_metros', min_value=0.0, step=0.5)
        
        dict_custom_services['servicio'].append(servicio2)
        dict_custom_services['precio_unitario'].append(servicio2_precio_metro)
        dict_custom_services['metros'].append(servicio2_metros)
    
    if 'Otro' in servicios_personalizados:
        servicio3 = col1.text_input('Servicio',value='Otro')
        if len(servicio3) == 0:
            col1.warning('Por favor escriba el servicio personalizado que hará')
        servicio3_precio = col2.number_input('Precio', key='servicio3_precio',
                                                   min_value=0, step=1000, format="%d")
        
        if len(servicio3) == 0:
            dict_custom_services['servicio'].append('Otro')
        else:
            dict_custom_services['servicio'].append(servicio3)
        dict_custom_services['precio_unitario'].append(servicio3_precio)
        dict_custom_services['metros'].append(1)
        
    if len(servicios_personalizados) == 0:
        dict_custom_services = {}
else:
    dict_custom_services = {}

dict_temp_services =  {
    'id_vehiculo' : placas[vehiculo][5],
    'placa' : vehiculo,
    'tipo_vehiculo': placas[vehiculo][2],
    'categoria': placas[vehiculo][3],
    'id_cliente' : placas[vehiculo][4],
    'cedula' : placas[vehiculo][0],
    'servicio': servicios+servicios_adicionales
}

if len(dict_temp_services['servicio']) > 0 or agree_personalizados:
    st.subheader('Resumen')
    if not st.session_state.df_temp_services:
        servicios_temp = Gestion_Servicios()
        if agree_personalizados and len(servicios_personalizados) > 0:
            df_servicios_temp = servicios_temp.dataframe_temp_services(dict_temp_services, dict_custom_services)
        else:
            df_servicios_temp = servicios_temp.dataframe_temp_services(dict_temp_services)
        st.dataframe(df_servicios_temp[['servicio','precio_formateado']],
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
                st.session_state.reset_custom_services = True
                st.rerun()
else:
    st.session_state.df_temp_services = False