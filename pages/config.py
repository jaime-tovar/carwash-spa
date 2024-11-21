from navigation import make_sidebar
import streamlit as st
from time import sleep
import pandas as pd
import os
from PIL import Image

make_sidebar()

@st.dialog("Agregar nuevo cliente")
def btn_agregar():
    nombre_usuario = st.text_input("Nombre de Usuario *")
    contraseña = st.text_input("Contraseña *")
    roles = ['admin','cajero']
    rol = st.selectbox("Rol:", roles)
    data = pd.DataFrame ([{
        'usuario' : nombre_usuario,
        'contrasena' : contraseña,
        'rol' : rol,
        'esta_activo' : True
    }])
    st.write('\* Campos obligatorios')
    if st.button("Guardar", key=3):
        data.to_csv('pages/data/users.csv', index=False)
        st.success("Usuario creado existosamente")
        sleep(1)
        st.rerun()

st.header('Configuraciones', divider = 'grey')
st.subheader('Agregar Usuarios')

left, middle, right = st.columns(3)

if "btn_agregar" not in st.session_state:
    if left.button("Agregar", key=1):
        btn_agregar()

def configurar():
    archivo_subido = st.file_uploader("Sube tu archivo PNG o JPG", type=["png","jpg","jpeg"])

    if archivo_subido is not None:
        imagen = Image.open(archivo_subido)
        nombre_predeterminado = "logo.png"
        ruta_guardado = os.path.join("pages/data", nombre_predeterminado)
        imagen.save(ruta_guardado)

    if st.button('Refrescar'):
        st.rerun()

st.header('Cambiar Logo y Nombre del Lavadero', divider='grey')
configurar()
