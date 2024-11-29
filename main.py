import streamlit as st
from time import sleep
from navigation import make_sidebar
from pages.front_util_functions import validate_user
import os
import json
import webbrowser

pdf_path = "pages/data/manual.pdf"

def abrir_pdf():
    ruta_absoluta = os.path.abspath(pdf_path)
    webbrowser.open_new(f"file://{ruta_absoluta}")

if st.button("ℹ"):
    abrir_pdf()


left, right = st.columns(2)

ruta_json = 'pages/data/nombre_empresa.json'
ruta = "pages/data/logo.png"
with open(ruta_json, 'r') as file:
    data = json.load(file)
nombre_empresa = data['nombre']
if os.path.exists(ruta):
    left.image(ruta, use_container_width=False , width = 300)
right.title(nombre_empresa)
username = right.text_input("Usuario")
password = right.text_input("Contraseña", type="password")

if right.button("Iniciar Sesión", type="primary"):
    validacion = validate_user(username, password)
    if validacion[0]:
        st.session_state.logged_in = True
        st.session_state.role = validacion[1]
        st.toast(validacion[2])
        sleep(1)
        st.switch_page("pages/principal.py")
    else:
        st.error(validacion[2])
