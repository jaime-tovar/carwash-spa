from navigation import make_sidebar
import streamlit as st
from pages.back_util_functions import Gestion_Vehiculos
from time import sleep
    
make_sidebar()
st.session_state.df_state = False

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

def update_text():
    st.session_state.input_text = st.session_state.input_text.upper()

@st.dialog("Agregar nuevo vehículo")
def btn_agregar():
    placa = st.text_input("Placa *", key="input_text", on_change=update_text)
    vehiculos = Gestion_Vehiculos()
    dict_categorias = vehiculos.diccionario_tipos_vehiculos()
    categoria = st.selectbox("Categoria *", dict_categorias.keys())
    tipo = st.selectbox('Tipo:', dict_categorias[categoria])
    marca = st.text_input("Marca")
    modelo = st.text_input("Modelo")
    cilindraje = st.text_input("Cilindraje *")
    st.write('\* Campos obligatorios')
    if st.button("Guardar", key=3):
        vehiculo = Gestion_Vehiculos()
        vehiculo.registrar_vehiculo(placa, tipo_vehiculo, marca, modelo, cilindraje, tipo)
        st.success("Vehículo creado existosamente")
        sleep(1)
        st.rerun()

st.header('Gestión de Vehiculos', divider = 'grey')

left, middle, right = st.columns(3)

if "btn_agregar" not in st.session_state:
    if left.button("Agregar", key=1):
        btn_agregar()

if not st.session_state.df_state:
    df = Gestion_Vehiculos()
    st.session_state.df = df.dataframe_front()
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
        "categoria": st.column_config.TextColumn(
            "Categoria",
            default="st."
            ),
        "tipo": st.column_config.TextColumn(
            "Tipo",
            default="st."),
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
        "propietario": st.column_config.TextColumn(
            "Cédula Propietario",
            default="st."
            ),
        "nombre": st.column_config.TextColumn(
            "Propietario",
            default="st."
            )
    }
)