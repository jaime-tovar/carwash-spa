from navigation import make_sidebar
import streamlit as st
from pages.back_util_functions import Gestion_Vehiculos
from time import sleep

make_sidebar()
st.session_state.df_state = False

@st.dialog("Agregar nuevo cliente")
def btn_agregar():
    placa = st.text_input("Placa *")
    tipo_vehiculo = st.selectbox("Tipo de Vehiculo:", ['Moto','Carro'])
    marca = st.text_input("Marca")
    modelo = st.text_input("Modelo *")
    cilindraje = st.text_input("Cilindraje")
    tipo = st.selectbox('Tipo:', ['Sport', 'Naked', 'Camioneta', 'Automovil', 'Touring'])
    st.write('\* Campos obligatorios')
    if st.button("Guardar", key=3):
        cliente = Gestion_Vehiculos()
        cliente.registrar_vehiculo(placa, tipo_vehiculo, marca, modelo, cilindraje, tipo)
        st.success("Cliente creado existosamente")
        sleep(1)
        st.rerun()

st.header('Gestión de Vehiculos', divider = 'grey')

left, middle, right = st.columns(3)

if "btn_agregar" not in st.session_state:
    if left.button("Agregar", key=1):
        btn_agregar()

if not st.session_state.df_state:
    df = Gestion_Vehiculos()
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
        "placa": st.column_config.TextColumn(
            "Placa",
            default="st."
            ),
        "tipo_vehiculo": st.column_config.TextColumn(
            "Tipo de Vehiculo",
            default="st."
            ),
        "marca": st.column_config.TextColumn(
            "Marca",
            default="st."
            ),
        "modelo": st.column_config.TextColumn(
            "Modelo",
            default="st."
            ),
        "cilindraje": st.column_config.TextColumn(
            "Cilindraje",
            default="st."
            ),
        "tipo": st.column_config.TextColumn(
            "Tipo",
            default="st.")
    }
)