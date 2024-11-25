import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta
from time import sleep
from navigation import make_sidebar
from pages.back_util_functions import Gestion_Clientes, Gestion_Vehiculos
from pages.front_util_functions import validate_email, validate_cedula, validate_celular

make_sidebar()
# Variables temporales de sesion
st.session_state.df_state_clientes = False
st.session_state.df_state_vehiculos = False
st.session_state.validaciones_data = True

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

def update_text():
    st.session_state.input_text = st.session_state.input_text.upper()

@st.dialog("Agregar nuevo cliente")
def btn_agregar():
    cedula = st.text_input("Cédula *")
    if cedula:
        if not validate_cedula(cedula):
            st.error("La cédula no es válida")
            st.session_state.validaciones_data = False
        else:
            st.session_state.validaciones_data = True
    
    nombre = st.text_input("Nombre *")
    telefono = st.text_input("Celular / Teléfono *")
    if telefono:
        if not validate_celular(telefono):
            st.error("Número de cellular inválido")
            st.session_state.validaciones_data = False
        else:
            st.session_state.validaciones_data = True
    
    fecha_nacimiento = st.date_input("Fecha Nacimiento", max_value= datetime.today(), min_value= datetime.today() - relativedelta(years=34) )
    email = st.text_input("Correo Electrónico")
    if email:
        if not validate_email(email):
            st.error("El correo no es válido")
            st.session_state.validaciones_data = False
        else:
            st.session_state.validaciones_data = True
    
    st.write('\* Campos obligatorios')
    if st.button("Guardar", key=3):
        if st.session_state.validaciones_data:
            cliente = Gestion_Clientes()
            cliente.registrar_cliente(cedula, nombre, telefono, fecha_nacimiento, email)
            st.success("Cliente creado existosamente")
            sleep(1)
            st.rerun()
        else:
            st.error('Datos incorrectos')

@st.dialog("Editar cliente")
def btn_editar(dict_values):
    cedula = st.text_input("Cédula", value=dict_values['cedula'], disabled=True)
    nombre = st.text_input("Nombre *", value=dict_values['nombre'])
    telefono = st.text_input("Teléfono *", value=dict_values['telefono'])
    fecha_nacimiento = st.date_input("Fecha Nacimiento", value=dict_values['fecha_nacimiento'])
    email = st.text_input("Correo Electrónico", value=dict_values['email'])
    st.write('\* Campos obligatorios')
    if st.button("Guardar", key=5):
        cliente = Gestion_Clientes()
        cliente.editar_cliente(dict_values['id'] ,str(cedula), nombre, telefono, fecha_nacimiento, email)
        st.success("Se ha actualizado exitosamente datos del cliente")
        sleep(1)
        st.rerun()

@st.dialog("Agregar vehículo a cliente")
def btn_agregar_vehiculo(dict_values):
    left0, right0 = st.columns(2)
    placa = left0.text_input("Placa *", key="input_text", on_change=update_text)
    if placa and len(placa) != 6:
        left0.warning('Ingrese una placa válida')
    propietario = right0.text_input("Propietario",
                                    placeholder=f"{dict_values['cedula']} | {dict_values['nombre']}",
                                    disabled=True)
    vehiculos = Gestion_Vehiculos()
    dict_categorias = vehiculos.diccionario_tipos_vehiculos()
    left1, right1 = st.columns(2)
    tipo_vehiculo = left1.selectbox("Categoria *", dict_categorias.keys())
    categoria = right1.selectbox('Tipo *', dict_categorias[tipo_vehiculo])
    left2, right2 = st.columns(2)
    marca = left2.text_input("Marca")
    modelo = right2.text_input("Modelo")
    cc_dict = vehiculos.diccionario_cc_categorias()
    if tipo_vehiculo == 'Moto':
        cilindraje = st.number_input("Cilindraje *",
                                     min_value=int(cc_dict[categoria][0]),
                                     max_value=int(cc_dict[categoria][1]),
                                     step=5, format='%d')
    else:
        cilindraje = st.number_input("Cilindraje *", min_value=600,
                                     step=5, format='%d')
    st.write('\* Campos obligatorios')
    if st.button("Guardar", key=3, type="primary"):
        vehiculo = Gestion_Vehiculos()
        vehiculo.registrar_vehiculo(placa, tipo_vehiculo, categoria, marca, modelo, cilindraje, dict_values['cedula'])
        st.success("Vehículo creado existosamente")
        sleep(1)
        st.rerun()
        
st.header('Administración de Clientes')

left, middle, right = st.columns(3)

if "btn_agregar" not in st.session_state:
    if left.button("Agregar", key=1, type="primary"):
        btn_agregar()

if not st.session_state.df_state_clientes:
    df_clientes = Gestion_Clientes()
    st.session_state.df_clientes = df_clientes.cargar_dataframe()
    st.session_state.df_state_clientes = True

event_clientes = st.dataframe(
    st.session_state.df_clientes,
    key="clientes",
    on_select="rerun",
    selection_mode=['single-row'],
    column_config={
        "id": st.column_config.TextColumn("ID", default="st."),
        "cedula": st.column_config.TextColumn("Cédula", default="st."),
        "nombre": st.column_config.TextColumn("Nombre", default="st."),
        "fecha_nacimiento": st.column_config.TextColumn("Fecha de Nacimiento", default="st."),
        "telefono": st.column_config.TextColumn("Teléfono", default="st."),
        "email": st.column_config.TextColumn("Correo Electrónico", default="st.")  
    },
    height= 250
)

try:
    dict_clientes_values = {
        'id' : event_clientes.selection.rows[0]+1,
        'nombre' : str(st.session_state.df_clientes.iloc[event_clientes.selection.rows].iat[0, 0]),
        'cedula' : str(st.session_state.df_clientes.iloc[event_clientes.selection.rows].iat[0, 1]),
        'fecha_nacimiento' : datetime.strptime(st.session_state.df_clientes.iloc[event_clientes.selection.rows].iat[0, 2], "%Y-%m-%d").date(),
        'telefono' : str(st.session_state.df_clientes.iloc[event_clientes.selection.rows].iat[0, 3]),
        'email' : str(st.session_state.df_clientes.iloc[event_clientes.selection.rows].iat[0, 4])
    }
except IndexError:
    dict_clientes_values = None


if "btn_editar" not in st.session_state:
    if middle.button("Editar", key=2):
        if dict_clientes_values is None:
            st.toast('Primero seleccione un registro')
        else:
            btn_editar(dict_clientes_values)

if "btn_agregar_vehiculo" not in st.session_state:
    if right.button("Agregar Vehículo", key=12):
        if dict_clientes_values is None:
            st.toast('Primero seleccione un registro')
        else:
            btn_agregar_vehiculo(dict_clientes_values)

#st.write(dict_clientes_values)
st.header('Administración de Vehículos')

if not st.session_state.df_state_vehiculos:
    df_vehiculos = Gestion_Vehiculos()
    st.session_state.df_vehiculos = df_vehiculos.dataframe_front()
    st.session_state.df_state_vehiculos = True

event_vehiculos = st.dataframe(
    st.session_state.df_vehiculos,
    key="vehiculos",
    on_select="rerun",
    selection_mode=['single-row'],
    column_config={
        "id": st.column_config.TextColumn("ID", default="st."),
        "placa": st.column_config.TextColumn("Placa", default="st."),
        "categoria": st.column_config.TextColumn("Categoria", default="st."),
        "tipo": st.column_config.TextColumn("Tipo", default="st."),
        "marca": st.column_config.TextColumn("Marca", default="st."),
        "modelo": st.column_config.TextColumn("Modelo", default="st."),
        "cilindraje": st.column_config.TextColumn("Cilindraje", default="st."),
        "propietario": st.column_config.TextColumn("Cédula Propietario", default="st."),
        "nombre": st.column_config.TextColumn("Propietario", default="st.")
    },
    height= 250
)

try:
    dict_vehiculos_values = {
        'id' : event_vehiculos.selection.rows[0]+1,
        'placa' : st.session_state.df_vehiculos.iloc[event_vehiculos.selection.rows].iat[0, 0],
        'categoria' : str(st.session_state.df_vehiculos.iloc[event_vehiculos.selection.rows].iat[0, 1]),
        'tipo' : str(st.session_state.df_vehiculos.iloc[event_vehiculos.selection.rows].iat[0, 2]),
        'marca' : str(st.session_state.df_vehiculos.iloc[event_vehiculos.selection.rows].iat[0, 3]),
        'modelo' : str(st.session_state.df_vehiculos.iloc[event_vehiculos.selection.rows].iat[0, 4]),
        'cilindraje' : str(st.session_state.df_vehiculos.iloc[event_vehiculos.selection.rows].iat[0, 5]),
        'propietario' : str(st.session_state.df_vehiculos.iloc[event_vehiculos.selection.rows].iat[0, 6])
    }
except IndexError:
    dict_vehiculos_values = None

st.write(dict_vehiculos_values)