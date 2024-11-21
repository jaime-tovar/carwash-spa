import pandas as pd

# Esta clase maneja el registro de clientes en un archivo csv   
class Gestion_Clientes:
    def __init__(self):  # Inicializamos el archivo donde se van a guardar los datos
        self.archivo_csv='pages/data/clientes.csv'
    
    def cargar_dataframe(self):
        try:
            self.cliente_df = pd.read_csv(self.archivo_csv, dtype=str, index_col='id')  # Carga los datos desde el archivo csv en un DataFrame
        except FileNotFoundError:
            # Si el DataFrame no existe, crea un nuevo DataFrame con las columnas dadas
            self.cliente_df = pd.DataFrame(columns=['nombre','cedula','fecha_nacimiento','telefono','email'])
            self.cliente_df.index.name = 'id'
            
        return self.cliente_df
    
    def existe_cliente(self, cedula):
        cliente = self.cliente_df[self.cliente_df["cedula"] == cedula]
        if not cliente.empty: # Verifica si el cliente existe 
            return True
        return False
    
    def cargar_a_csv(self):
        self.cliente_df = self.cliente_df.astype(str)
        # Guarda el DataFrame actualizado en el archivo CSV
        self.cliente_df.to_csv(path_or_buf=self.archivo_csv, sep=",", index=True)
         
    def registrar_cliente(self, cedula, nombre, telefono, fecha_nacimiento=None, email=None):
        self.cargar_dataframe()
        
        if self.cliente_df.empty:
            id_maximo = 1  # Si está vacío, asignar el primer id como 1
        else:
            # Se extrae el id maximo que haya en el dataframe para poder calcular el id siguiente
            id_maximo = self.cliente_df.index.astype(int).max() + 1
        
        # Crea un nuevo DataFrame con los datos del nuevo cliente
        nuevo_cliente_df = pd.DataFrame([{
            "nombre": nombre,
            "cedula": cedula,
            "telefono": telefono,
            "fecha_nacimiento": fecha_nacimiento,
            "email": email
        }], index=[id_maximo])
        
        nuevo_cliente_df.index.name = 'id'
        
        self.cliente_df = pd.concat([self.cliente_df, nuevo_cliente_df])
        
        self.cargar_a_csv()
        
    def editar_cliente(self, id, cedula, nombre, telefono, fecha_nacimiento=None, email=None):
        self.cargar_dataframe()
        self.cliente_df = self.cliente_df.astype(str)
        if id in self.cliente_df.index:
            self.cliente_df.loc[id, ['cedula', 'nombre', 'telefono', 'fecha_nacimiento', 'email']] = [
                cedula, nombre, telefono, fecha_nacimiento, email
            ]
        self.cargar_a_csv()

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