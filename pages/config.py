from navigation import make_sidebar
import streamlit as st
from time import sleep
import pandas as pd
import os
from PIL import Image
from pages.back_util_functions import Gestion_Usuarios

make_sidebar()
st.session_state.df_state = False

@st.dialog("Agregar nuevo usuario")
def btn_agregar():
    nombre_usuario = st.text_input("Nombre de Usuario *")
    contrasena = st.text_input("Contraseña *")
    rol = st.selectbox("Rol:", ['admin', 'cajero'])
    if st.button("Guardar", key=3):
        usuario = Gestion_Usuarios()
        usuario.registrar_usuario(nombre_usuario,contrasena,rol)
        st.success("Usuario creado exitosamente")
        sleep(1)
        st.rerun()

@st.dialog("Cambiar estado de usuario")
def btn_cambiar_estado(dict_values):
    st.write(f"Cambiar estado del usuario: {dict_values['usuario']}")
    if st.button("Cambiar Estado", key=6):
        cambiar_estado_usuario(dict_values['index'])
        st.success("Estado del usuario cambiado exitosamente")
        sleep(1)
        st.rerun()

def cambiar_estado_usuario(index):
    try:
        df = pd.read_csv('pages/data/users.csv')
        if 0 <= index < len(df):
            df.at[index, 'esta_activo'] = not df.at[index, 'esta_activo']
            df.to_csv('pages/data/users.csv', index=False)
        else:
            st.error("Índice fuera de rango.")
    except FileNotFoundError:
        st.error("El archivo 'users.csv' no existe.")

st.header('Configuraciones', divider='grey')
st.subheader('Gestión Usuarios')

left, middle, right = st.columns(3)

if "btn_agregar" not in st.session_state:
    if left.button("Agregar", key=5):
        btn_agregar()

if not st.session_state.df_state:
    df = Gestion_Usuarios()
    st.session_state.df = df.cargar_dataframe()
    st.session_state.df_state = True

event = st.dataframe(
    st.session_state.df,
    key="data",
    on_select="rerun",
    selection_mode='single-row'
)

try:
    dict_edit_values = {
        'index': event.selection.rows[0],
        'usuario': st.session_state.df.iloc[event.selection.rows].iat[0, 0]
    }
except IndexError:
    dict_edit_values = None

if "btn_cambiar_estado" not in st.session_state:
    if right.button("Cambiar Estado", key=2):
        if dict_edit_values is None:
            st.toast('Primero seleccione un registro')
        else:
            btn_cambiar_estado(dict_edit_values)

def configurar():
    archivo_subido = st.file_uploader("Sube tu archivo PNG o JPG", type=["png", "jpg", "jpeg"])

    if archivo_subido is not None:
        imagen = Image.open(archivo_subido)
        nombre_predeterminado = "logo.png"
        ruta_guardado = os.path.join("pages/data", nombre_predeterminado)
        imagen.save(ruta_guardado)

    if st.button('Refrescar'):
        st.rerun()

st.header('Cambiar Logo y Nombre del Lavadero', divider='grey')
configurar()