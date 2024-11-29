from navigation import make_sidebar
import streamlit as st
from time import sleep
from pages.back_util_functions import Gestion_Servicios, Gestion_Vehiculos

make_sidebar()

# Variables temporales de sesion
st.session_state.df_state_servicios_precios = False
st.session_state.validaciones_data = True

@st.dialog("Agregar nuevo servicio")
def btn_agregar():
    left0, right0 = st.columns(2)
    servicio = left0.text_input("Servicio *")
    precio = right0.number_input("Precio *", step=1000, format='%d', min_value=0)
    
    vehiculos = Gestion_Vehiculos()
    dict_categorias = vehiculos.diccionario_tipos_vehiculos()
    left1, right1 = st.columns(2)

    tipo_vehiculo = left1.selectbox("Categoria *", dict_categorias.keys())
    categoria = right1.selectbox('Tipo *', dict_categorias[tipo_vehiculo])
    detalle = st.text_area("Detalles del Servicio")
    st.write('\* Campos obligatorios')
    
    if st.button("Guardar", key=123):
        if st.session_state.validaciones_data:
            servicios = Gestion_Servicios()
            servicios.registrar_servicio(servicio, precio, tipo_vehiculo, categoria, detalle)
            st.success("Servicio creado existosamente")
            sleep(1)
            st.rerun()
        else:
            st.error('Datos incorrectos')

@st.dialog("Editar servicio")
def btn_editar(dict_values):
    left0, right0 = st.columns(2)
    servicio = left0.text_input("Servicio *", value=dict_values['servicio'], disabled=True)
    precio = right0.number_input("Precio *", step=1000, format='%d', min_value=0,
                                 value=dict_values['precio'])
    vehiculos = Gestion_Vehiculos()
    dict_categorias = vehiculos.diccionario_tipos_vehiculos()
    left1, right1 = st.columns(2)
    
    tipo_vehiculo = left1.selectbox("Categoria *", dict_categorias.keys(),
                                    index=list(dict_categorias.keys()).index(dict_values['tipo_vehiculo']),
                                    disabled=True)
    
    dict_categoria_index = {key: idx for idx, key in enumerate(dict_categorias[tipo_vehiculo])}
    
    categoria = right1.selectbox('Tipo *', dict_categorias[tipo_vehiculo],
                                 index=dict_categoria_index[dict_values['categoria']],
                                 disabled=True)
    
    detalle = st.text_area("Detalles del Servicio", value=dict_values['detalles'])
    st.write('\* Campos obligatorios')
    
    if st.button("Guardar", key=123):
        if st.session_state.validaciones_data:
            servicios = Gestion_Servicios()
            servicios.editar_servicio(dict_values['id'], servicio, precio, tipo_vehiculo, categoria, detalle)
            st.success("Servicio editado existosamente")
            sleep(1)
            st.rerun()
        else:
            st.error('Datos incorrectos')

st.header('Administración de Servicios')

left, middle, right = st.columns(3)

if "btn_agregar" not in st.session_state:
    if left.button("Agregar", key=122, type="primary"):
        btn_agregar()

if not st.session_state.df_state_servicios_precios:
    df_servicios = Gestion_Servicios()
    st.session_state.df_servicios = df_servicios.cargar_dataframe()
    st.session_state.df_state_servicios_precios = True

event_servicios = st.dataframe(
    st.session_state.df_servicios,
    key="servicios",
    on_select="rerun",
    selection_mode=['single-row'],
    column_config={
        "id": st.column_config.TextColumn("ID", default="st."),
        "servicio": st.column_config.TextColumn("Servicio", default="st.", width='medium'),
        "detalles_servicio": st.column_config.TextColumn("Descripción", default="st.", width='largue'),
        "tipo_vehiculo": st.column_config.TextColumn("Tipo Vehículo", default="st."),
        "categoria": st.column_config.TextColumn("Categoria", default="st."),
        "precio": st.column_config.NumberColumn("Precio", default="st.")  
    },
    height= 250
)

try:
    dict_services_values = {
        'id' : event_servicios.selection.rows[0]+1,
        'servicio' : str(st.session_state.df_servicios.iloc[event_servicios.selection.rows].iat[0, 0]),
        'precio' : int(st.session_state.df_servicios.iloc[event_servicios.selection.rows].iat[0, 1]),
        'tipo_vehiculo' : str(st.session_state.df_servicios.iloc[event_servicios.selection.rows].iat[0, 2]),
        'categoria' : str(st.session_state.df_servicios.iloc[event_servicios.selection.rows].iat[0, 3]),
        'detalles' : str(st.session_state.df_servicios.iloc[event_servicios.selection.rows].iat[0, 4])
    }
except IndexError:
    dict_services_values = None

if "btn_editar" not in st.session_state:
    if middle.button("Editar", key=1234):
        btn_editar(dict_services_values)