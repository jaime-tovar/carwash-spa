import pandas as pd
from datetime import datetime

class Cliente:
    def __init__(self, nombre, cedula, fecha_nacimiento, telefono, email):
        self.nombre = nombre
        self.cedula = cedula
        self.fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")  # Convierte la fecha en un objeto datetime
        self.telefono = telefono
        self.email = email   

# Esta clase maneja el registro de clientes en un archivo csv   
class Gestion_Clientes:
    def __init__(self, archivo_csv):  # Inicializamos el archivo donde se van a guardar los datos
        self.archivo_csv = archivo_csv 
        try:
            self.cliente_df = pd.read_csv(self.archivo_csv)  # Carga los datos desde el archivo csv en un DataFrame
        except FileNotFoundError:
            # Si el DataFrame no existe, crea un nuevo DataFrame con las columnas dadas
            self.cliente_df = pd.DataFrame(columns=["nombre", "cedula", "fecha_nacimiento", "telefono", "email"]) 
        
    def registrar_cliente(self, nombre, cedula, telefono, email, fecha_nacimiento):
        # Crea una nueva instancia de Cliente
        nuevo_cliente = Cliente(nombre, cedula, fecha_nacimiento, telefono, email)  
        
        # Crea un nuevo DataFrame con los datos del nuevo cliente
        nuevo_cliente_df = pd.DataFrame([{
            "nombre": nuevo_cliente.nombre,
            "cedula": nuevo_cliente.cedula,
            "telefono": nuevo_cliente.telefono,
            "email": nuevo_cliente.email,
            "fecha_nacimiento": nuevo_cliente.fecha_nacimiento
        }])
        
        # Usa pd.concat() para agregar el nuevo cliente al DataFrame existente
        self.cliente_df = pd.concat([self.cliente_df, nuevo_cliente_df], ignore_index=True) 
        
        # Guarda el DataFrame actualizado en el archivo CSV
        self.cliente_df.to_csv(self.archivo_csv, sep=";", index=False)  

    def buscar_cliente(self, cedula, archivo_Cliente_encontrado = "cliente_encontrado.csv"):
        # Filtra los clientes por cédula en el DataFrame
        cliente = self.cliente_df[self.cliente_df["cedula"] == cedula]  
        
        if not cliente.empty: # Verifica si el cliente existe 
            cliente.to_csv(archivo_Cliente_encontrado, sep=";", index= False) # Genera el archivo csv con el cliente filtrado
            return cliente.to_dict(orient="records")[0]  # Convierte el Dataframe en una lista de diccionarios y devuelve el primer cliente encontrado
        return None  # Devuelve None si no lo encuentra
    
    def mostrar_los_clientes(self):
        return self.cliente_df.to_dict(orient="records")  # Convierte todo el DataFrame a una lista de diccionarios

