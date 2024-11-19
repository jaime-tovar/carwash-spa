import pandas as pd
from datetime import datetime

class Cliente:
    def __init__(self, cedula, nombre, telefono, fecha_nacimiento=None, email=None):
        self.nombre = nombre
        self.cedula = cedula
        self.fecha_nacimiento = fecha_nacimiento  # Convierte la fecha en un objeto datetime
        self.telefono = telefono
        self.email = email   

# Esta clase maneja el registro de clientes en un archivo csv   
class Gestion_Clientes:
    def __init__(self):  # Inicializamos el archivo donde se van a guardar los datos
        self.archivo_csv='clientes.csv'
        try:
            self.cliente_df = pd.read_csv(self.archivo_csv)  # Carga los datos desde el archivo csv en un DataFrame
        except FileNotFoundError:
            # Si el DataFrame no existe, crea un nuevo DataFrame con las columnas dadas
            self.cliente_df = pd.DataFrame(columns=['id','nombre','cedula','fecha_nacimiento','telefono','email']) 
        
    def registrar_cliente(self, cedula, nombre, telefono, fecha_nacimiento=None, email=None):
        # Se extrae el id maximo que haya en el dataframe para poder calcular el id siguiente
        id_maximo = self.cliente_df['id'].max() + 1
        
        # Crea un nuevo DataFrame con los datos del nuevo cliente
        nuevo_cliente_df = pd.DataFrame([{
            "id": id_maximo,
            "nombre": nombre,
            "cedula": cedula,
            "telefono": telefono,
            "fecha_nacimiento": fecha_nacimiento,
            "email": email
        }])
        
        # Usa pd.concat() para agregar el nuevo cliente al DataFrame existente
        self.cliente_df = pd.concat([self.cliente_df, nuevo_cliente_df], ignore_index=True) 
        
        # Guarda el DataFrame actualizado en el archivo CSV
        self.cliente_df.to_csv(path_or_buf=self.archivo_csv, sep=",", index=False)
        
    def editar_cliente(self, id, cedula, nombre, telefono, fecha_nacimiento=None, email=None):
        # Se extrae el id maximo que haya en el dataframe para poder calcular el id siguiente
        df_temp = self.cliente_df[self.cliente_df['id'] == id]
        
        df_temp.loc[0, 'cedula'] = cedula
        df_temp.loc[0, 'nombre'] = nombre
        df_temp.loc[0, 'telefono'] = telefono
        
        # Usa pd.concat() para agregar el nuevo cliente al DataFrame existente
        self.cliente_df = pd.concat([self.cliente_df, df_temp], ignore_index=True) 
        
        # Guarda el DataFrame actualizado en el archivo CSV
        self.cliente_df.to_csv(path_or_buf=self.archivo_csv, sep=",", index=False)  

    def buscar_cliente(self, cedula, archivo_Cliente_encontrado = "cliente_encontrado.csv"):
        # Filtra los clientes por cédula en el DataFrame
        cliente = self.cliente_df[self.cliente_df["cedula"] == cedula]  
        
        if not cliente.empty: # Verifica si el cliente existe 
            cliente.to_csv(archivo_Cliente_encontrado, sep=";", index= False) # Genera el archivo csv con el cliente filtrado
            return cliente.to_dict(orient="records")[0]  # Convierte el Dataframe en una lista de diccionarios y devuelve el primer cliente encontrado
        return None  # Devuelve None si no lo encuentra
    
    def mostrar_los_clientes(self):
        return self.cliente_df.to_dict(orient="records")  # Convierte todo el DataFrame a una lista de diccionarios


class Vehiculo:
    def __init__(self,placa, tipo_vehiculo, marca, modelo, cilindraje, tipo):
        self.tipo_vehiculo = tipo_vehiculo
        self.marca = marca
        self.modelo = modelo
        self.cilindraje = cilindraje
        self.tipo = tipo
        self.placa = placa

class RegistroVehiculos:
    def __init__(self):
        self.vehiculos = pd.DataFrame(columns=['placa', 'tipo_vehiculo', 'marca', 'modelo', 'cilindraje', 'tipo'])
        self.archivo_csv = "vehiculos.csv"

    def registrar_vehiculo(self, placa, tipo_vehiculo, marca, modelo, cilindraje, tipo):
        
        nuevo_vehiculo = Vehiculo(placa, tipo_vehiculo, marca, modelo, cilindraje, tipo)  
        
        # Crea un nuevo DataFrame con los datos del nuevo vehículo
        nuevo_vehiculo_df = pd.DataFrame([{
            "placa": nuevo_vehiculo.placa,
            "tipo_vehiculo": nuevo_vehiculo.tipo_vehiculo,
            "marca": nuevo_vehiculo.marca,
            "modelo": nuevo_vehiculo.modelo,
            "cilindraje": nuevo_vehiculo.cilindraje,
            "tipo": nuevo_vehiculo.tipo
        }])
        
        # Usa pd.concat() para agregar el nuevo vehículo al DataFrame existente
        self.vehiculos = pd.concat([self.vehiculos, nuevo_vehiculo_df], ignore_index=True) 
        
        # Guarda el DataFrame actualizado en el archivo CSV
        self.vehiculos.to_csv(self.archivo_csv, sep=";", index=False)

    def buscar_vehiculo(self, placa):
        vehiculo = self.vehiculos[self.vehiculos['placa'] == placa]
        if not vehiculo.empty:
            vehiculo.to_csv("vehiculo_encontrado.csv", sep= ";", index= False)
            return vehiculo
        return None
        
    def mostrar_todos_vehiculos(self):
        return self.vehiculos