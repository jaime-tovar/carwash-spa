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

class Gestion_Vehiculos:
    def __init__(self):  # Inicializamos el archivo donde se van a guardar los datos
        self.archivo_csv='pages/data/vehicles.csv'
    
    def cargar_dataframe(self):
        try:
            self.vehiculo_df = pd.read_csv(self.archivo_csv, dtype=str, index_col='id')  # Carga los datos desde el archivo csv en un DataFrame
        except FileNotFoundError:
            # Si el DataFrame no existe, crea un nuevo DataFrame con las columnas dadas
            self.vehiculo_df = pd.DataFrame(columns=['placa', 'tipo_vehiculo', 'marca', 'modelo', 'cilindraje','tipo'])
            self.vehiculo_df.index.name = 'id'
            
        return self.vehiculo_df
    
    def existe_vehiculo(self, placa):
        vehiculo = self.vehiculo_df[self.vehiculo_df["placa"] == placa]
        if not vehiculo.empty: # Verifica si la placa existe 
            return True
        return False
           
    
    def cargar_a_csv(self):
        self.vehiculo_df = self.vehiculo_df.astype(str)
        # Guarda el DataFrame actualizado en el archivo CSV
        self.vehiculo_df.to_csv(path_or_buf=self.archivo_csv, sep=",", index=True)
         
    def registrar_vehiculo(self, placa, tipo_vehiculo, marca, modelo, cilindraje, tipo):
        self.cargar_dataframe()
        
        if self.vehiculo_df.empty:
            id_maximo = 1  # Si está vacío, asignar el primer id como 1
        else:
            # Se extrae el id maximo que haya en el dataframe para poder calcular el id siguiente
            id_maximo = self.vehiculo_df.index.astype(int).max() + 1
        
        # Crea un nuevo DataFrame con los datos del nuevo cliente
        nuevo_cliente_df = pd.DataFrame([{
            "placa": placa,
            "tipo_vehiculo": tipo_vehiculo ,
            "marca": marca,
            "modelo": modelo,
            "cilindraje": cilindraje,
            "tipo" : tipo
        }], index=[id_maximo])
        
        nuevo_cliente_df.index.name = 'id'
        
        self.vehiculo_df = pd.concat([self.vehiculo_df, nuevo_cliente_df])
        
        self.cargar_a_csv()
        
    def editar_vehiculo(self, id, placa, tipo_vehiculo, marca, modelo, cilindraje, tipo):
        self.cargar_dataframe()
        self.vehiculo_df = self.vehiculo_df.astype(str)
        if id in self.vehiculo_df.index:
            self.vehiculo_df.loc[id, ['placa', 'tipo_vehiculo', 'marca', 'modelo', 'cilindraje', 'tipo']] = [
                placa, tipo_vehiculo, marca, modelo, cilindraje, tipo
            ]
        self.cargar_a_csv()

class Gestion_Usuarios:
    def __init__(self):  # Inicializamos el archivo donde se van a guardar los datos
        self.archivo_csv='pages/data/users.csv'
    
    def cargar_dataframe(self):
        try:
            self.usuario_df = pd.read_csv(self.archivo_csv, dtype=str, index_col='id')  # Carga los datos desde el archivo csv en un DataFrame
        except FileNotFoundError:
            # Si el DataFrame no existe, crea un nuevo DataFrame con las columnas dadas
            self.usuario_df = pd.DataFrame(columns=['usuario','contrasena','rol','esta_activo'])
            self.usuario_df.index.name = 'id'
            
        return self.usuario_df
    
    def cargar_a_csv(self):
        self.usuario_df = self.usuario_df.astype(str)
        # Guarda el DataFrame actualizado en el archivo CSV
        self.usuario_df.to_csv(path_or_buf=self.archivo_csv, sep=",", index=True)
    
    def registrar_usuario(self, usuario, contrasena, rol, esta_activo = True):
        self.cargar_dataframe()
        
        if self.usuario_df.empty:
            id_maximo = 1  # Si está vacío, asignar el primer id como 1
        else:
            # Se extrae el id maximo que haya en el dataframe para poder calcular el id siguiente
            id_maximo = self.usuario_df.index.astype(int).max() + 1
        
        # Crea un nuevo DataFrame con los datos del nuevo cliente
        nuevo_usuario_df = pd.DataFrame([{
            "usuario": usuario,
            "contrasena": contrasena,
            "rol": rol,
            "esta_activo": esta_activo,
        }], index=[id_maximo])
        
        nuevo_usuario_df.index.name = 'id'
        
        self.usuario_df = pd.concat([self.usuario_df, nuevo_usuario_df])
        
        self.cargar_a_csv()