import streamlit as st
import pandas as pd
import importlib

# Cargar usuarios desde un archivo CSV
def cargar_usuarios():
    try:
        return pd.read_csv("usuarios.csv")
    except FileNotFoundError:
        # Crear un DataFrame inicial si el archivo no existe
        usuarios_df = pd.DataFrame([
            {"nombre_usuario": "admin", "rol": "admin", "contraseña": "123"},
            {"nombre_usuario": "usuario1", "rol": "usuario", "contraseña": "hola"},
            {"nombre_usuario": "usuario2", "rol": "usuario", "contraseña": "1234"}
        ])
        # Guardar el DataFrame inicial en un archivo CSV
        usuarios_df.to_csv("usuarios.csv", index=False)
        return usuarios_df

# Guardar el DataFrame de usuarios en un archivo CSV
def guardar_usuarios(df):
    df.to_csv("usuarios.csv", index=False)

# Inicializar DataFrame de usuarios
usuarios_df = cargar_usuarios()

# Función de registro de usuario
def registrar_usuario(nuevo_usuario, nueva_contraseña, rol):
    global usuarios_df
    if nuevo_usuario in usuarios_df["nombre_usuario"].values:
        st.error("Este nombre de usuario ya existe. Elige otro.")
    else:
        # Agregar el nuevo usuario al DataFrame y actualizar el CSV
        nuevo_dato = pd.DataFrame([{"nombre_usuario": nuevo_usuario, "rol": rol, "contraseña": nueva_contraseña}])
        usuarios_df = pd.concat([usuarios_df, nuevo_dato], ignore_index=True)
        guardar_usuarios(usuarios_df)  # Guardar los cambios en el archivo CSV
        st.success(f"Usuario {nuevo_usuario} registrado exitosamente")

# Función de autenticación
def autenticar(usuario, contraseña):
    usuario_data = usuarios_df[usuarios_df["nombre_usuario"] == usuario]
    if not usuario_data.empty and usuario_data["contraseña"].values[0] == contraseña:
        return usuario_data["rol"].values[0]
    return None

# Redirigir al archivo correspondiente según el rol
def redirigir_menu(rol):
    if rol == "admin":
        menu_admin = importlib.import_module("menu_admin")
        menu_admin.mostrar_menu()
    elif rol == "usuario":
        menu_usuario = importlib.import_module("menu_usuario")
        menu_usuario.mostrar_menu()
    elif rol == "soporte":
        menu_soporte = importlib.import_module("menu_soporte")
        menu_soporte.mostrar_menu()


# Pantalla de inicio de sesión
def login():
    st.title("Bienvenido A (Nombre Empresa)")
    usuario = st.text_input("Usuario", key="usuario_login")
    contraseña = st.text_input("Contraseña", type="password", key="contraseña_login")
    if st.button("Ingresar"):
        rol = autenticar(usuario, contraseña)
        if rol:
            st.session_state["autenticado"] = True
            st.session_state["usuario"] = usuario
            st.session_state["rol"] = rol
            st.session_state["mostrar_registro"] = False
            st.rerun()  # Refresca la app automáticamente
        else:
            st.error("Usuario o contraseña incorrectos")

# Registro de un nuevo usuario
def mostrar_registro():
    st.title("Registro de Usuario")
    with st.form("Registro"):
        nuevo_usuario = st.text_input("Nuevo nombre de usuario", key="usuario_registro")
        nueva_contraseña = st.text_input("Nueva contraseña", type="password", key="contraseña_registro")
        rol = st.selectbox("Selecciona el rol", ["usuario", "admin", "soporte"], key="rol_registro")
        if st.form_submit_button("Registrar"):
            if nuevo_usuario and nueva_contraseña:
                registrar_usuario(nuevo_usuario, nueva_contraseña, rol)
                st.session_state["mostrar_registro"] = False
                st.rerun()  # Refresca la app automáticamente
            else:
                st.error("Por favor, complete todos los campos")

# CSS para cambiar el fondo a azul claro
st.markdown(
    """
    <style>
    .stApp {
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Ejecución del sistema
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
if "mostrar_registro" not in st.session_state:
    st.session_state["mostrar_registro"] = False

# Muestra el menú de registro si se hace clic en "Registrarse"
if st.session_state["mostrar_registro"]:
    mostrar_registro()
elif not st.session_state["autenticado"]:
    st.image("imagenes/logo_lavadero.jpg",)
    login()
    if st.button("Registrarse"):
        st.session_state["mostrar_registro"] = True
        st.rerun()  # Refresca la app automáticamente
else:
    redirigir_menu(st.session_state["rol"])
