import streamlit as st
import pandas as pd
import numpy as np


def mostrar_menu():

    st.header("Gestion de Clientes",divider = "gray")
        # Función para mostrar el menú 1
    def menu_1():
    # Crear o cargar el DataFrame (si no existe en el estado de sesión)
        if "df" not in st.session_state:
            # Crear un DataFrame vacío con algunas columnas de ejemplo
            st.session_state.df = pd.read_csv("data/clientes.csv", index_col="id")
        event = st.dataframe(st.session_state.df,
                             key="data",
                             on_select="rerun",
                             selection_mode="single-row")
        st.write(event.selection)
        # Mostrar el DataFrame actual
        #st.subheader("Usuarios Registrados")
        #st.dataframe(st.session_state.df)
        
        # Agregar filas al DataFrame
        st.subheader("Agregar Usuarios")
        nombre = st.text_input("Nombre")
        edad = st.text_input("Edad")
        if st.button("Agregar fila"):
            if nombre and edad:
                # Convertir la edad a número (si es posible)
                try:
                    edad = int(edad)
                    # Crear un DataFrame con la nueva fila
                    nueva_fila = pd.DataFrame({"Nombre": [nombre], "Edad": [edad]})
                    # Usar pd.concat para agregar la nueva fila al DataFrame
                    st.session_state.df = pd.concat([st.session_state.df, nueva_fila], ignore_index=True)
                    st.success(f"Fila agregada: {nombre}, {edad} años.")
                except ValueError:
                    st.error("Por favor, ingresa una edad válida (número).")
            else:
                st.error("Por favor, completa los campos de nombre y edad.")
 

    # Función para mostrar el menú 2
    def menu_2():
        st.subheader("Este es el Menu 2")
        st.write("Contenido del menú 2.")

    # Función para mostrar el menú 3
    def menu_3():
        st.subheader("Este es el Menu 3")
        st.write("Contenido del menú 3.")

    # Sidebar con la imagen de encabezado
    def sidebar_menu():
        # Mostrar la imagen en el encabezado del sidebar
        #st.sidebar.image(imagen)
        # Agregar botones para cambiar entre menús
        menu = st.sidebar.radio("Selecciona un menú", ["Gestion Usuarios", "Historial", "Ajustes"])
        return menu

    # Aquí defines la imagen
    #imagen = "/src/images/logo_lavadero.jpg"

    # Usar el sidebar y recibir el menú seleccionado
    menu_seleccionado = sidebar_menu()

    # Mostrar el contenido según el menú seleccionado
    if menu_seleccionado == "Gestion Usuarios":
        menu_1()
    elif menu_seleccionado == "Historial":
        menu_2()
    elif menu_seleccionado == "Ajustes":
        menu_3()