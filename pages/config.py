from navigation import make_sidebar
import streamlit as st
from time import sleep
import pandas as pd
import os
from PIL import Image
from pages.back_util_functions import Gestion_Usuarios
import json
import webbrowser


make_sidebar()
st.session_state.df_state = False

@st.dialog("Agregar nuevo usuario")
def btn_agregar():
    nombre_usuario = st.text_input("Nombre de Usuario *")
    contrasena = st.text_input("Contraseña *", type="password")
    rol = st.selectbox("Rol:", ['admin', 'usuario'])
    if st.button("Guardar", key=3):
        usuario = Gestion_Usuarios()
        usuario.registrar_usuario(nombre_usuario,contrasena,rol)
        st.success("Usuario creado exitosamente")
        sleep(1)
        st.rerun()

@st.dialog("Cambiar estado de usuario")
def btn_cambiar_estado(dict_values):
    st.write(f"El usuario **{dict_values['usuario']}** se encuentra ")
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
    ruta_json = 'pages/data/nombre_empresa.json'
    if archivo_subido is not None:
        imagen = Image.open(archivo_subido)
        nombre_predeterminado = "logo.png"
        ruta_guardado = os.path.join("pages/data", nombre_predeterminado)
        imagen.save(ruta_guardado)
    
    nombre = st.text_input("Nombre del Lavadero")
    try:
        if os.path.exists(ruta_json) and os.path.getsize(ruta_json) > 0:
            with open(ruta_json, 'r') as file:
                data = json.load(file)
        else:
            data = {}
            st.warning("El archivo JSON no existe o está vacío. Se creará uno nuevo.")
        if nombre:
            data['nombre'] = nombre
            with open(ruta_json, 'w') as file:
                json.dump(data, file, indent=4)
            st.success("Nombre del Lavadero actualizado exitosamente.")
        else:
            st.info("Por favor, introduce un nombre para el lavadero.")
    except json.JSONDecodeError as e:
        st.error(f"Error al leer el archivo JSON: {e}")
    except Exception as e:
        st.error(f"Error inesperado: {e}")

    if st.button('Refrescar'):
        st.rerun()

st.header('Cambiar Logo y Nombre del Lavadero', divider='grey')
configurar()

pdf_path = "pages/data/manual.pdf"

def abrir_pdf():
    ruta_absoluta = os.path.abspath(pdf_path)
    webbrowser.open_new(f"file://{ruta_absoluta}")

if st.button("Manual de Uso"):
    abrir_pdf()