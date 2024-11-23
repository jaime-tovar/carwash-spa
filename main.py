import streamlit as st
from time import sleep
from navigation import make_sidebar
from pages.front_util_functions import validate_user
import os
import json
#make_sidebar()
ruta_json = 'pages/data/nombre_empresa.json'
ruta = "pages/data/logo.png"
with open(ruta_json, 'r') as file:
    data = json.load(file)
nombre_empresa = data['nombre']
if os.path.exists(ruta):
    st.image(ruta, use_column_width = False , width = 250)
st.title(nombre_empresa)
username = st.text_input("Usuario")
password = st.text_input("Contraseña", type="password")

if st.button("Iniciar Sesión", type="primary"):
    validacion = validate_user(username, password)
    if validacion[0]:
        st.session_state.logged_in = True
        st.session_state.role = validacion[1]
        st.toast(validacion[2])
        sleep(1)
        st.switch_page("pages/principal.py")
    else:
        st.error(validacion[2])
