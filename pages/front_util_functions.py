import pandas as pd
import re

def validate_user(user, password):
    df = pd.read_csv('pages/data/users.csv')
    
    user_exist = df[(df['usuario'] == user) & (df['contrasena'] == password)]

    if not user_exist.empty:
        if user_exist['esta_activo'].iloc[0] == True:
            return True, user_exist['rol'].iloc[0], 'Inicio de Sesión Exitoso'
        else:
            return False, None,f"Acceso Denegado. El usuario \'{user}\' se encuentra inactivo, comuníquese con el administrador para mas detalles."
    else:
        return False, None, f'Acceso Denegado. Usuario o contraseña incorrectos'

def is_valid_email(email):
    # Se define un patrón por expresión regular para validar el correo
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})*$'
    
    # Validar usando re.match
    if re.match(pattern, email):
        return True
    else:
        return False
    
def validate_client_data(cedula, correo):
    try:
        cedula = int(cedula)
    except TypeError:
        return 'Recuerde que cédula debe ser un número'
    
    if not is_valid_email(correo):
        return 'Formato de correo o válido'
    else:
        return True
    