from navigation import make_sidebar
import streamlit as st
from pages.back_util_functions import Gestion_Vehiculos, Gestion_Clientes
from time import sleep
    
make_sidebar()
st.session_state.df_state = False

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

def update_text():
    st.session_state.input_text = st.session_state.input_text.upper()

@st.dialog("Editar vehiculo")
def btn_editar_vehiculo(dict_values):
    left0, right0 = st.columns(2)
    placa = left0.text_input("Placa *", value=dict_values['placa'], disabled=True)
    if placa and len(placa) != 6:
        left0.warning('Ingrese una placa válida')
    right0.write('')
    right0.write('')
    agree = right0.checkbox('Editar placa')   
    dict_cc_nombre = Gestion_Clientes()
    dict_cc_nombre = dict_cc_nombre.listado_clientes()
    dict_cc_nombre_index = {key: idx for idx, key in enumerate(dict_cc_nombre.keys())}
    
    propietario = st.selectbox("Reasignar propietario", dict_cc_nombre.keys(),
                                   index=dict_cc_nombre_index[f"{dict_values['cedula']} | {dict_values['nombre']}"])
    
    if agree:
        placa_ant = left0.text_input("Placa anterior", value=dict_values['placa'], disabled=True)
        placa_nueva = right0.text_input("Placa nueva *")
        
    vehiculos = Gestion_Vehiculos()
    dict_categorias = vehiculos.diccionario_tipos_vehiculos()
    left1, right1 = st.columns(2)
    dict_tipo_vehiculo_index = {key: idx for idx, key in enumerate(dict_categorias.keys())}
    
    tipo_vehiculo = left1.selectbox("Tipo Vehiculo *", dict_categorias.keys(),
                                    index=dict_tipo_vehiculo_index[dict_values['tipo_vehiculo']])
    
    dict_categoria_index = {key: idx for idx, key in enumerate(dict_categorias[tipo_vehiculo])}
    categoria = right1.selectbox('Categoria *', dict_categorias[tipo_vehiculo],
                                 index=dict_categoria_index[dict_values['categoria']])
    left2, right2 = st.columns(2)
    marca = left2.text_input("Marca", value=dict_values['marca'])
    modelo = right2.text_input("Modelo", value=dict_values['modelo'])
    cc_dict = vehiculos.diccionario_cc_categorias()
    if tipo_vehiculo == 'Moto':
        cilindraje = st.number_input("Cilindraje *",
                                     min_value=int(cc_dict[categoria][0]),
                                     max_value=int(cc_dict[categoria][1]),
                                     step=5, format='%d',
                                     value=int(dict_values['cilindraje']))
    else:
        cilindraje = st.number_input("Cilindraje *", min_value=600,
                                     step=5, format='%d',
                                     value=int(dict_values['cilindraje']))
    st.write('\* Campos obligatorios')
    if st.button("Guardar", key=3, type="primary"):
        vehiculo = Gestion_Vehiculos()
        if agree:
            vehiculo.editar_vehiculo(dict_values['id'], placa, tipo_vehiculo, categoria, marca, modelo, cilindraje, dict_cc_nombre[propietario], placa_nueva)
        else:
            vehiculo.editar_vehiculo(dict_values['id'], placa, tipo_vehiculo, categoria, marca, modelo, cilindraje, dict_cc_nombre[propietario])
        st.success("Vehículo creado existosamente")
        sleep(1)
        st.rerun()

st.header('Gestión de Vehiculos', divider = 'grey')

col1, col2 = st.columns(2)

if not st.session_state.df_state:
    df = Gestion_Vehiculos()
    st.session_state.df = df.dataframe_front_gestion()
    st.session_state.df_state = True

event = st.dataframe(
    st.session_state.df,
    key="data",
    on_select="rerun",
    selection_mode=['single-row'],
    column_config={
        "id": st.column_config.TextColumn("ID",default="st."),
        "placa": st.column_config.TextColumn("Placa",default="st."),
        "tipo_vehiculo": st.column_config.TextColumn("Tipo Vehículo",default="st."),
        "categoria": st.column_config.TextColumn("Categoria",default="st."),
        "marca": st.column_config.TextColumn("Marca",default="st."),
        "modelo": st.column_config.TextColumn("Modelo",default="st."),
        "cilindraje": st.column_config.TextColumn("Cilindraje",default="st."),
        "cedula": st.column_config.TextColumn("Cédula Propietario",default="st."),
        "nombre": st.column_config.TextColumn("Propietario",default="st.")
    }
)

try:
    dict_vehiculo_values = {
        'id' : event.selection.rows[0]+1,
        'placa' : str(st.session_state.df.iloc[event.selection.rows].iat[0, 0]),
        'tipo_vehiculo' : str(st.session_state.df.iloc[event.selection.rows].iat[0, 1]),
        'categoria' : str(st.session_state.df.iloc[event.selection.rows].iat[0, 2]),
        'marca' : str(st.session_state.df.iloc[event.selection.rows].iat[0, 3]),
        'modelo' : str(st.session_state.df.iloc[event.selection.rows].iat[0, 4]),
        'cilindraje' : str(st.session_state.df.iloc[event.selection.rows].iat[0, 5]),
        'cedula' : str(st.session_state.df.iloc[event.selection.rows].iat[0, 6]),
        'nombre' : str(st.session_state.df.iloc[event.selection.rows].iat[0, 7])
    }
except IndexError:
    dict_vehiculo_values = None

if "btn_editar_vehiculo" not in st.session_state:
    if col1.button("Editar", key=12):
        if dict_vehiculo_values is None:
            st.toast('Primero seleccione un registro')
        else:
            btn_editar_vehiculo(dict_vehiculo_values)