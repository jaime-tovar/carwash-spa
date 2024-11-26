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
        self.archivo_tipos_vehiculos = 'pages/data/vehicles_types.csv'
    
    def cargar_dataframe(self):
        try:
            self.vehiculo_df = pd.read_csv(self.archivo_csv, dtype=str, index_col='id')# Carga los datos desde el archivo csv en un DataFrame
        except FileNotFoundError:
            # Si el DataFrame no existe, crea un nuevo DataFrame con las columnas dadas
            self.vehiculo_df = pd.DataFrame(columns=['placa', 'tipo_vehiculo', 'categoria', 'marca', 'modelo', 'cilindraje', 'propietario'])
            self.vehiculo_df.index.name = 'id'
            
        return self.vehiculo_df
    
    def dataframe_front(self):
        self.cargar_dataframe()
        clientes = Gestion_Clientes()
        df_clientes = clientes.cargar_dataframe()
        df_clientes = df_clientes[['cedula', 'nombre']]
        df_vehiculo = self.vehiculo_df.merge(df_clientes,
                                             left_on='propietario',
                                             right_on='cedula',
                                             how='left')
        df_vehiculo.set_index(self.vehiculo_df.index, inplace=True)
        df_vehiculo.drop(columns=['cedula'], inplace=True)  
        
        return df_vehiculo
    
    def existe_vehiculo(self, placa):
        vehiculo = self.vehiculo_df[self.vehiculo_df["placa"] == placa]
        if not vehiculo.empty: # Verifica si la placa existe 
            return True
        return False

    def cargar_a_csv(self):
        self.vehiculo_df = self.vehiculo_df.astype(str)
        # Guarda el DataFrame actualizado en el archivo CSV
        self.vehiculo_df.to_csv(path_or_buf=self.archivo_csv, sep=",", index=True)
         
    def registrar_vehiculo(self, placa, tipo_vehiculo, categoria, marca, modelo, cilindraje, propietario):
        self.cargar_dataframe()
        
        if self.vehiculo_df.empty:
            id_maximo = 1  # Si está vacío, asignar el primer id como 1
        else:
            # Se extrae el id maximo que haya en el dataframe para poder calcular el id siguiente
            id_maximo = self.vehiculo_df.index.astype(int).max() + 1
        
        # Crea un nuevo DataFrame con los datos del nuevo cliente
        nuevo_vehiculo_df = pd.DataFrame([{
            "placa": placa,
            "tipo_vehiculo": tipo_vehiculo,
            "categoria" : categoria,
            "marca": marca,
            "modelo": modelo,
            "cilindraje": cilindraje,
            "propietario": propietario
        }], index=[id_maximo])
        
        nuevo_vehiculo_df.index.name = 'id'
        
        self.vehiculo_df = pd.concat([self.vehiculo_df, nuevo_vehiculo_df])
        
        self.cargar_a_csv()
        
    def editar_vehiculo(self, id, placa, tipo_vehiculo, categoria, marca, modelo, cilindraje, propietario):
        self.cargar_dataframe()
        self.vehiculo_df = self.vehiculo_df.astype(str)
        if id in self.vehiculo_df.index:
            self.vehiculo_df.loc[id, ['placa', 'tipo_vehiculo', 'categoria', 'marca', 'modelo', 'cilindraje', 'propietario']] = [
                placa, categoria, tipo, marca, modelo, cilindraje, propietario
            ]
        self.cargar_a_csv()
    
    def diccionario_tipos_vehiculos(self):
        df = pd.read_csv(self.archivo_tipos_vehiculos)
        diccionario = df.groupby('tipo_vehiculo')['categoria'].apply(list).to_dict()
        return diccionario
    
    def listado_placas_clientes(self):
        self.cargar_dataframe()
        clientes = Gestion_Clientes()
        df_clientes = clientes.cargar_dataframe()
        df_clientes = df_clientes[['cedula', 'nombre']]
        df_vehiculo = self.vehiculo_df.merge(df_clientes,
                                             left_on='propietario',
                                             right_on='cedula',
                                             how='left')
        diccionario_placas = {row['placa']: [row['cedula'], row['nombre'], row['tipo_vehiculo'], row['categoria']] 
                              for _, row in df_vehiculo.iterrows()}
        return diccionario_placas
    
    def diccionario_cc_categorias(self):
        df = pd.read_csv(self.archivo_tipos_vehiculos)
        cc_dict = df[df['tipo_vehiculo'] == 'Moto']
        cc_dict = cc_dict.set_index('categoria')[['cc_min', 'cc_max']].apply(list, axis=1).to_dict()
        return cc_dict

class Gestion_Servicios:
    def __init__(self):  # Inicializamos el archivo donde se van a guardar los datos
        self.archivo_csv='pages/data/price_services.csv'
    
    def cargar_dataframe(self):
        try:
            self.service_df = pd.read_csv(self.archivo_csv, dtype=str, index_col='id')  # Carga los datos desde el archivo csv en un DataFrame
        except FileNotFoundError:
            # Si el DataFrame no existe, crea un nuevo DataFrame con las columnas dadas
            self.service_df = pd.DataFrame(columns=['servicio','precio','tipo_vehiculo','categoria','detalles_servicio'])
            self.service_df.index.name = 'id'
            
        return self.service_df
    
    def cargar_a_csv(self):
        self.service_df = self.service_df.astype(str)
        # Guarda el DataFrame actualizado en el archivo CSV
        self.service_df.to_csv(path_or_buf=self.archivo_csv, sep=",", index=True)
        
    def registrar_servicio(self, servicio, precio, tipo_vehiculo, categoria, detalles_servicio):
        detalles_servicio = f'\"{detalles_servicio}\"'
        self.cargar_dataframe()
        
        if self.service_df.empty:
            id_maximo = 1  # Si está vacío, asignar el primer id como 1
        else:
            # Se extrae el id maximo que haya en el dataframe para poder calcular el id siguiente
            id_maximo = self.service_df.index.astype(int).max() + 1
        
        # Crea un nuevo DataFrame con los datos del nuevo cliente
        nuevo_servicio_df = pd.DataFrame([{
            "servicio": servicio,
            "precio": precio,
            "tipo_vehiculo": tipo_vehiculo,
            "categoria": categoria,
            "detalles_servicio": detalles_servicio
        }], index=[id_maximo])
        
        nuevo_servicio_df.index.name = 'id'
        
        self.service_df = pd.concat([self.service_df, nuevo_servicio_df])
        
        self.cargar_a_csv()
    
    def diccionario_precios_categoria(self):
        # Leer el archivo CSV
        df = self.cargar_dataframe()

        # Crear el diccionario con la estructura deseada
        result_dict = {}
        for _, row in df.iterrows():
            tipo_vehiculo = row["tipo_vehiculo"]
            categoria = row["categoria"]
            servicio = row["servicio"]
            precio = row["precio"]

            # Crear las jerarquías si no existen
            if tipo_vehiculo not in result_dict:
                result_dict[tipo_vehiculo] = {}
            if categoria not in result_dict[tipo_vehiculo]:
                result_dict[tipo_vehiculo][categoria] = {}

            # Asignar el servicio y precio
            result_dict[tipo_vehiculo][categoria][servicio] = precio

        return result_dict

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