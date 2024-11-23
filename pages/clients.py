import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta
from time import sleep
from navigation import make_sidebar
from pages.back_util_functions import Gestion_Clientes
from pages.front_util_functions import validate_client_data, validar_numero_celular

make_sidebar()
st.session_state.df_state = False

@st.dialog("Agregar nuevo cliente")
def btn_agregar():
    cedula = st.text_input("Cédula *")
    nombre = st.text_input("Nombre *")
    telefono = st.text_input("Celular / Teléfono *")
    if telefono:
        if not validar_numero_celular(telefono):
            st.error("Número de cellular inválido")
    fecha_nacimiento = st.date_input("Fecha Nacimiento", max_value= datetime.today(), min_value= datetime.today() - relativedelta(years=34) )
    email = st.text_input("Correo Electrónico")
    st.write('\* Campos obligatorios')
    if st.button("Guardar", key=3):
        cliente = Gestion_Clientes()
        cliente.registrar_cliente(cedula, nombre, telefono, fecha_nacimiento, email)
        st.success("Cliente creado existosamente")
        sleep(1)
        st.rerun()

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
        
st.header('Gestión de Clientes')

left, middle, right = st.columns(3)

if "btn_agregar" not in st.session_state:
    if left.button("Agregar", key=1):
        btn_agregar()

if not st.session_state.df_state:
    df = Gestion_Clientes()
    st.session_state.df = df.cargar_dataframe()
    st.session_state.df_state = True

event = st.dataframe(
    st.session_state.df,
    key="data",
    on_select="rerun",
    selection_mode=['single-row'],
    column_config={
        "id": st.column_config.TextColumn(
            "ID",
            default="st."
            ),
        "cedula": st.column_config.TextColumn(
            "Cédula",
            default="st."
            ),
        "nombre": st.column_config.TextColumn(
            "Nombre",
            default="st."
            ),
        "fecha_nacimiento": st.column_config.TextColumn(
            "Fecha de Nacimiento",
            default="st."
            ),
        "telefono": st.column_config.TextColumn(
            "Teléfono",
            default="st."
            ),
        "email": st.column_config.TextColumn(
            "Correo Electrónico",
            default="st."
            )  
    },
    height= 300
)

try:
    dict_edit_values = {
        'id' : event.selection.rows[0]+1,
        'nombre' : st.session_state.df.iloc[event.selection.rows].iat[0, 0],
        'cedula' : str(st.session_state.df.iloc[event.selection.rows].iat[0, 1]),
        'fecha_nacimiento' : datetime.strptime(st.session_state.df.iloc[event.selection.rows].iat[0, 2], "%Y-%m-%d").date(),
        'telefono' : str(st.session_state.df.iloc[event.selection.rows].iat[0, 3]),
        'email' : st.session_state.df.iloc[event.selection.rows].iat[0, 4]
    }
except IndexError:
    dict_edit_values = None


if "btn_editar" not in st.session_state:
    if right.button("Editar", key=2):
        if dict_edit_values is None:
            st.toast('Primero seleccione un registro')
        else:
            btn_editar(dict_edit_values)

#st.write(dict_edit_values)