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

def validate_email(email):
    # Se define un patrón por expresión regular para validar el correo
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})*$'
    
    # Validar usando re.match
    if re.match(pattern, email):
        return True
    else:
        return False
    
def validate_cedula(cedula):
    # Validar que la cédula sea un número y tenga máximo 10 dígitos
    if not re.fullmatch(r'^\d{1,10}$', cedula):
        return False
    return True
    
def validate_celular(numero):
    if len(numero) == 10 and numero.isdigit():
        if int(numero[0]) == 3 or int(numero[0]) == 6:
            return True
    return False

