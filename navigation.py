import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
import os
import json


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]

def make_sidebar():
    ruta_json = 'pages/data/nombre_empresa.json'
    ruta = "pages/data/logo.png"
    with open(ruta_json, 'r') as file:
        data = json.load(file)
    nombre_empresa = data['nombre']
    st.logo(ruta, size='large')
    with st.sidebar:
        st.image(ruta, use_column_width=True, width = 250)
        st.title(nombre_empresa)
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            if st.session_state.role == 'admin':
                st.page_link("pages/principal.py", label="Principal", icon="🏠")
                st.page_link("pages/clients.py", label="Gestión Clientes", icon="👨🏻‍💼")
                st.page_link("pages/vehicles.py", label="Gestión Vehículos", icon="🚘")
                st.page_link("pages/config.py", label="Configuraciones", icon="🛠️")

            if st.session_state.role == 'cajero':
                st.page_link("pages/principal.py", label="Principal", icon="🏠")
                st.page_link("pages/clients.py", label="Gestión Clientes", icon="👨🏻‍💼")
                st.page_link("pages/vehicles.py", label="Gestión Vehículos", icon="🚘")

            st.write("")
            st.write("")

            if st.button("Cerrar Sesion"):
                logout()

        elif get_current_page_name() != "main":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("main.py")


def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("main.py")
