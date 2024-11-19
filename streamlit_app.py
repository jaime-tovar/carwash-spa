import streamlit as st
from time import sleep
from navigation import make_sidebar
from backend.sys_util_functions import validate_user

#make_sidebar()

st.title("Log In")

st.write("Puede probar con las credenciales")
st.write("Usuario `admin`, Contraseña `admin`")
st.write("Usuario `test`, Contraseña `test`")

username = st.text_input("Usuario")
password = st.text_input("Contraseña", type="password")

if st.button("Log in", type="primary"):
    validacion = validate_user(username, password)
    if validacion[0]:
        st.session_state.logged_in = True
        st.session_state.role = validacion[1]
        st.toast(validacion[2])
        sleep(1)
        st.switch_page("pages/principal.py")
    else:
        st.error(validacion[2])
