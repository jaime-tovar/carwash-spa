import streamlit as st
from time import sleep
from navigation import make_sidebar

make_sidebar()

st.title("Log In")

st.write("Puede probar con las credenciales (Usuario `admin`, Contraseña `admin`).")
st.write("Usuario `admin`, Contraseña `admin`")
st.write("Usuario `usuario`, Contraseña `12345`")

username = st.text_input("Usuario")
password = st.text_input("Contraseña", type="password")

if st.button("Log in", type="primary"):
    if username == "admin" and password == "admin":
        st.session_state.logged_in = True
        st.session_state.role = 'admin'
        st.toast("Inicio de Sesión Exitoso")
        sleep(0.5)
        st.switch_page("pages/principal.py")
    elif username == "usuario" and password == "12345":
        st.session_state.logged_in = True
        st.session_state.role = 'user'
        st.toast("Inicio de Sesión Exitoso")
        sleep(0.5)
        st.switch_page("pages/principal.py")
    else:
        st.error("Usuario o contraseña incorrectos")
