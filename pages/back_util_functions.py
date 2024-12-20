import pandas as pd
import datetime
from io import BytesIO
import re

def obtener_fecha_hora():
    # Obtener la fecha y la hora actuales
    fecha_actual = datetime.datetime.now()

    # Formatear la fecha en 'año-mes-día'
    fecha_formateada = fecha_actual.strftime("%Y-%m-%d")

    # Formatear la hora en 'hora:minuto:segundo am/pm'
    hora_formateada = fecha_actual.strftime("%I:%M:%S %p")
    return fecha_formateada, hora_formateada

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
    
    def cargar_datos(self):
        try:
            self.cliente_df = pd.read_csv(self.archivo_csv, dtype=str)  # Carga los datos desde el archivo csv en un DataFrame
        except FileNotFoundError:
            # Si el DataFrame no existe, crea un nuevo DataFrame con las columnas dadas
            self.cliente_df = pd.DataFrame(columns=['id','nombre','cedula','fecha_nacimiento','telefono','email'])
            
        return self.cliente_df
    
    def existe_cliente(self, cedula):
        self.cargar_dataframe()
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
        
    def editar_cliente(self, id, cedula, nombre, telefono, fecha_nacimiento=None, email=None, cedula_nueva=None):
        self.cargar_dataframe()
        self.cliente_df = self.cliente_df.astype(str)
        if cedula_nueva is not None:
            cedula_input = cedula_nueva
        else:
            cedula_input = cedula
        if id in self.cliente_df.index:
            self.cliente_df.loc[id, ['cedula', 'nombre', 'telefono', 'fecha_nacimiento', 'email']] = [
                cedula_input, nombre, telefono, fecha_nacimiento, email
            ]
        self.cargar_a_csv()

    def listado_clientes(self):
        self.cargar_datos()
        self.cliente_df['cc_nombre'] = self.cliente_df['cedula'] + ' | ' + self.cliente_df['nombre']
        dict_cc_nombre = dict(zip(self.cliente_df['cc_nombre'], self.cliente_df['id']))
        return dict_cc_nombre
        
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
    
    def cargar_datos(self):
        try:
            self.vehiculo_df = pd.read_csv(self.archivo_csv, dtype=str)# Carga los datos desde el archivo csv en un DataFrame
        except FileNotFoundError:
            # Si el DataFrame no existe, crea un nuevo DataFrame con las columnas dadas
            self.vehiculo_df = pd.DataFrame(columns=['id','placa', 'tipo_vehiculo', 'categoria', 'marca', 'modelo', 'cilindraje', 'propietario'])
            
        return self.vehiculo_df
    
    def dataframe_front(self, id_cliente):
        self.cargar_dataframe()
        self.vehiculo_df = self.vehiculo_df[self.vehiculo_df['propietario'] == id_cliente]
        self.vehiculo_df = self.vehiculo_df[['placa','tipo_vehiculo','categoria','marca','modelo','cilindraje']]
        return self.vehiculo_df
    
    def dataframe_front_gestion(self):
        self.cargar_datos()
        self.vehiculo_df = self.vehiculo_df.rename(columns={'id': 'id_vehiculo'})
        clientes = Gestion_Clientes()
        df_clientes = clientes.cargar_datos()
        df_clientes = df_clientes[['id','cedula', 'nombre']]
        df_vehiculo = self.vehiculo_df.merge(df_clientes,
                                             left_on='propietario',
                                             right_on='id',
                                             how='left')
        df_vehiculo.drop(columns=['propietario','id'], inplace=True)
        df_vehiculo = df_vehiculo.rename(columns={'id_vehiculo': 'id'})
        df_vehiculo.set_index('id', inplace=True)
        
        return df_vehiculo
    
    def existe_vehiculo(self, placa):
        self.cargar_dataframe()
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
        
    def editar_vehiculo(self, id, placa, tipo_vehiculo, categoria, marca, modelo, cilindraje, propietario, placa_nueva=None):
        self.cargar_dataframe()
        self.vehiculo_df = self.vehiculo_df.astype(str)
        if placa_nueva is not None:
            placa_input = placa_nueva
        else:
            placa_input = placa
        if id in self.vehiculo_df.index:
            self.vehiculo_df.loc[id, ['placa', 'tipo_vehiculo', 'categoria', 'marca', 'modelo', 'cilindraje', 'propietario']] = [
                placa_input, tipo_vehiculo, categoria, marca, modelo, cilindraje, propietario
            ]
        self.cargar_a_csv()
    
    def diccionario_tipos_vehiculos(self):
        df = pd.read_csv(self.archivo_tipos_vehiculos)
        diccionario = df.groupby('tipo_vehiculo')['categoria'].apply(list).to_dict()
        return diccionario
    
    def listado_placas_clientes(self):
        self.cargar_datos()
        self.vehiculo_df = self.vehiculo_df.rename(columns={'id': 'id_vehiculo'})
        clientes = Gestion_Clientes()
        df_clientes = clientes.cargar_datos()
        df_clientes = df_clientes[['id', 'cedula', 'nombre']]
        df_vehiculo = self.vehiculo_df.merge(df_clientes,
                                             left_on='propietario',
                                             right_on='id',
                                             how='left')
        diccionario_placas = {
            row['placa']: [row['cedula'], row['nombre'], row['tipo_vehiculo'], row['categoria'], row['id'], row['id_vehiculo']]
            for _, row in df_vehiculo.iterrows()
            }
        return diccionario_placas
    
    def diccionario_cc_categorias(self):
        df = pd.read_csv(self.archivo_tipos_vehiculos)
        cc_dict = df[df['tipo_vehiculo'] == 'Moto']
        cc_dict = cc_dict.set_index('categoria')[['cc_min', 'cc_max']].apply(list, axis=1).to_dict()
        return cc_dict
    
    def listado_placas(self):
        self.cargar_datos()
        self.vehiculo_df['placa'] = self.vehiculo_df['placa']
        dict_cc_placas = dict(zip(self.vehiculo_df['placa'], self.vehiculo_df['id']))
        return dict_cc_placas

class Gestion_Servicios:
    def __init__(self):  # Inicializamos el archivo donde se van a guardar los datos
        self.archivo_csv='pages/data/price_services.csv'
        self.detalle_factura = 'pages/data/detalle_factura.csv'
        self.facturas = 'pages/data/facturas.csv'
    
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
        detalles_servicio =  re.sub(r"[\r\n]+", "", detalles_servicio)
        detalles_servicio = f'\"{detalles_servicio.strip()}\"'
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
    
    def editar_servicio(self, id, servicio, precio, tipo_vehiculo, categoria, detalles):
        self.cargar_dataframe()
        if id in self.service_df.index:
            self.service_df.loc[id, ['servicio', 'precio', 'tipo_vehiculo', 'categoria', 'detalles_servicio']] = [
                servicio, precio, tipo_vehiculo, categoria, detalles
            ]
        self.cargar_a_csv()
    
    def diccionario_precios_categoria(self):
        df = self.cargar_dataframe()

        # Se crea un diccionarioo que permita ver todos los servicios por tipo de vehiculo y categoria
        result_dict = {}
        for _, row in df.iterrows():
            tipo_vehiculo = row["tipo_vehiculo"]
            categoria = row["categoria"]
            servicio = row["servicio"]
            precio = row["precio"]

            # Se crean las jerarquias del diccionario
            if tipo_vehiculo not in result_dict:
                result_dict[tipo_vehiculo] = {}
            if categoria not in result_dict[tipo_vehiculo]:
                result_dict[tipo_vehiculo][categoria] = {}

            # Se asigna el servicio y precio
            result_dict[tipo_vehiculo][categoria][servicio] = precio

        return result_dict
    
    def dataframe_temp_services(self, dict_elecciones, dict_custom=None):
        self.cargar_dataframe()
        
        df_detalle_factura = pd.read_csv(self.detalle_factura)
        if df_detalle_factura.empty:
            id_max_detalle_factura = 1
        else:
            id_max_detalle_factura = df_detalle_factura['id'].max() + 1
        
        def formatear_precio(valor):
            return f"$ {valor:,.0f}"
        
        df_eleccion = pd.DataFrame(dict_elecciones)
        df_eleccion = df_eleccion.explode('servicio')
        df_merge_especifica = pd.merge(
            df_eleccion,
            self.service_df[self.service_df['categoria'] != 'General'],
            on=['tipo_vehiculo', 'categoria', 'servicio'],
            how='inner'
        )
    
        if dict_custom is not None:
            df = pd.DataFrame([{
                'id_vehiculo' : dict_elecciones['id_vehiculo'],
                'placa' : dict_elecciones['placa'],
                'tipo_vehiculo' : dict_elecciones['tipo_vehiculo'],
                'categoria' : dict_elecciones['categoria'],
                'id_cliente' : dict_elecciones['id_cliente'],
                'cedula' : dict_elecciones['cedula'],
                'servicio' : dict_custom['servicio'],
                'precio_unitario' : dict_custom['precio_unitario'],
                'metros' : dict_custom['metros']
            }])
            cols_to_explode = ['servicio', 'precio_unitario', 'metros']

            # Calcular el máximo de la longitud de las listas en las columnas
            max_len = max(df[cols_to_explode[0]].apply(len).max(), 
                          df[cols_to_explode[1]].apply(len).max(), 
                          df[cols_to_explode[2]].apply(len).max())

            # Aseguramos que todas las listas tengan la misma longitud
            for col in cols_to_explode:
                df[col] = df[col].apply(lambda x: x + [None] * (max_len - len(x)))

            # Expandimos todas las columnas seleccionadas simultáneamente
            df = df.explode(cols_to_explode, ignore_index=True)
            
            df['precio'] = df['precio_unitario']*df['metros']
            df['detalles_servicio'] = ''
            
            df = df[['id_vehiculo','placa','tipo_vehiculo','categoria','id_cliente','cedula','servicio','precio','detalles_servicio']]
            
        servicios_no_encontrados = df_eleccion[~df_eleccion['servicio'].isin(df_merge_especifica['servicio'])]
        
        df_merge_general = pd.merge(
            servicios_no_encontrados,
            self.service_df[self.service_df['categoria'] == 'General'],
            on=['tipo_vehiculo', 'servicio'],
            how='inner'
        )
        
        df_merge_general['categoria'] = 'General'
        df_final = pd.concat([df_merge_especifica, df_merge_general], ignore_index=True)
        if dict_custom is not None:
            df_final = pd.concat([df_final, df], ignore_index=True)
        df_final['id'] = range(id_max_detalle_factura, id_max_detalle_factura + len(df_final))
        df_final['precio'] = pd.to_numeric(df_final['precio'])
        df_final['precio_formateado'] = df_final['precio'].apply(lambda x: formatear_precio(int(x)))
        df_final = df_final[['id','placa', 'cedula', 'tipo_vehiculo', 'categoria', 'servicio', 'precio', 'precio_formateado']]
        df_final.index = df_final.index + 1

        return df_final
    
    def cargar_servicio_vehiculo(self, df_in, dict_in):
        df_detalle_factura = pd.read_csv(self.detalle_factura)
        df_facturas = pd.read_csv(self.facturas)
        
        if df_facturas.empty:
            id_max_facturas = 1
        else:
            id_max_facturas = df_facturas['id'].max() + 1
        
        # Proceso para construir las transacciones de la factura
        df_in['id_factura'] = id_max_facturas
        df_in = df_in[['id','id_factura','servicio','precio']]
        df_in['realizado'] = True
        
        sub_total = df_in['precio'].sum()
        
        df_detalle_factura = pd.concat([df_detalle_factura, df_in])
        # Se cargan las transacciones al detalle de facturas
        df_detalle_factura.to_csv(path_or_buf=self.detalle_factura, sep=",", index=False)
        
        # Proceso para construir las transacciones de la factura
        fecha_ingreso, hora_ingreso = obtener_fecha_hora()
        df_factura_in = pd.DataFrame([{
            'id' : id_max_facturas,
            'id_vehiculo' : dict_in['id_vehiculo'],
            'id_cliente' : dict_in['id_cliente'],
            'emision' : None,
            'fecha_ingreso' : fecha_ingreso,
            'hora_ingreso' : hora_ingreso,
            'fecha_salida' : None,
            'hora_salida' : None,
            'subtotal' : sub_total,
            'promocion' : None,
            'descuento' : None,
            'iva' : None,
            'total' : None,
            'metodo_pago' : None
        }])
        
        df_facturas = pd.concat([df_facturas, df_factura_in])
        # Se carga la factura
        df_facturas.to_csv(path_or_buf=self.facturas, sep=",", index=False)
        
        return
    
    def min_max_date(self):
        df_facturas = pd.read_csv(self.facturas, dtype=str)
        filtro = df_facturas['emision'].notna() & (df_facturas['emision'] != '')
        df_facturas = df_facturas[filtro]
        min_date = datetime.datetime.strptime(str(df_facturas['emision'].min()), '%Y-%m-%d').date()
        max_date = datetime.datetime.strptime(str(df_facturas['emision'].max()), '%Y-%m-%d').date()
        return min_date, max_date
    
    def diccionario_tipos_vehiculos_servicios(self):
        df = pd.read_csv(self.archivo_csv)
        diccionario = df.groupby('tipo_vehiculo')['servicio'].apply(list).to_dict()
        return diccionario

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
        
class Billing:
    def __init__(self):  # Inicializamos el archivo donde se van a guardar los datos
        self.detalle_factura = 'pages/data/detalle_factura.csv'
        self.facturas = 'pages/data/facturas.csv'
    
    def crear_dataframe(self, facturas=False, detalles_facturas=False):
        
        if facturas:
            try:
                self.df_facturas = pd.read_csv(self.facturas, dtype=str)
            except FileNotFoundError:
                self.df_facturas = pd.DataFrame(columns=['id','placa','cedula','emision','fecha_ingreso',
                                                        'hora_ingreso','fecha_salida','hora_salida','subtotal',
                                                        'promocion','descuento','iva','total','metodo_pago'])
                
            return self.df_facturas
        
        if detalles_facturas:
            try:
                self.df_detalle_factura = pd.read_csv(self.detalle_factura, dtype=str)
            except FileNotFoundError:
                self.df_detalle_factura = pd.DataFrame(columns=['id','id_factura','servicio','precio','realizado'])
                
            return self.df_detalle_factura
        
    def facturas_activas(self):
        self.crear_dataframe(facturas=True)
        filtro = self.df_facturas['emision'].isna() | (self.df_facturas['emision'] == '')
        self.df_facturas = self.df_facturas[filtro]
        
        df_vehiculos = Gestion_Vehiculos()
        df_vehiculos = df_vehiculos.cargar_datos()[['id','placa','tipo_vehiculo']]
        df_vehiculos = df_vehiculos.rename(columns={'id':'id_vehiculo'})
        
        df_clientes = Gestion_Clientes()
        df_clientes = df_clientes.cargar_datos()[['id','cedula','nombre']]
        df_clientes = df_clientes.rename(columns={'id':'id_cliente'})
        
        self.df_facturas = self.df_facturas.merge(df_vehiculos, how='left',
                                                  left_on='id_vehiculo', right_on='id_vehiculo')
        self.df_facturas = self.df_facturas.merge(df_clientes, how='left',
                                                  left_on='id_cliente', right_on='id_cliente')
        
        self.df_facturas = self.df_facturas.rename(columns={'id':'id_factura'})
        
        self.df_facturas = self.df_facturas[['id_factura','placa','cedula','nombre','fecha_ingreso','hora_ingreso',
                                             'subtotal','promocion','descuento','iva','total']]
        
        return self.df_facturas
    
    def detalles_factura(self, id_factura):
        self.crear_dataframe(detalles_facturas=True)
        self.df_detalle_factura = self.df_detalle_factura[self.df_detalle_factura['id_factura'] == id_factura]
        
        def formatear_precio(valor):
            return f"$ {valor:,.0f}"
        
        self.df_detalle_factura['precio_formateado'] = self.df_detalle_factura['precio'].apply(lambda x: formatear_precio(float(x)))
        
        return self.df_detalle_factura
    
    def facturar_servicio(self, dict_in):
        # Obtener los datos de el detalle de factura
        self.crear_dataframe(detalles_facturas=True)
        id_factura_a_actualizar = dict_in["id_factura"]

        # Obtener los datos de servicios del diccionario
        servicios = dict_in["servicios"]

        # Actualizar el detalle de facturas
        for servicio, precio in servicios["precio"].items():
            servicio_nombre = servicios["servicio"][servicio]
            precio_int = int(precio.replace("$", "").replace(",", ""))
            realizado = servicios["realizado"][servicio]

            # Actualizar las filas correspondientes
            self.df_detalle_factura.loc[
                (self.df_detalle_factura["id_factura"] == id_factura_a_actualizar) &
                (self.df_detalle_factura["servicio"] == servicio_nombre), 
                ["precio", "realizado"]
            ] = [precio_int, realizado]
        
        self.df_detalle_factura = self.df_detalle_factura.astype(str)
        # Guarda el DataFrame actualizado en el archivo CSV
        self.df_detalle_factura.to_csv(path_or_buf=self.detalle_factura, sep=",", index=False)
        
        # Obtener los datos de la factura
        self.crear_dataframe(facturas=True)
        
        id_factura = dict_in["id_factura"]
        fecha_salida, hora_salida = obtener_fecha_hora()
        
        self.df_facturas.loc[self.df_facturas["id"] == id_factura,
                             ["emision","fecha_salida","hora_salida","subtotal",
                              "descuento", "iva", "total", "metodo_pago"]] = [
            fecha_salida,
            fecha_salida,
            hora_salida,
            dict_in["subtotal"],
            dict_in["descuento"],
            dict_in["iva"],
            dict_in["total"],
            dict_in["metodo_pago"]
        ]

        # Convertir los campos numéricos a su tipo correspondiente
        self.df_facturas[["subtotal", "descuento", "iva", "total"]] = self.df_facturas[["subtotal", "descuento", "iva", "total"]].astype(float)
        

        self.df_facturas.to_csv(path_or_buf=self.facturas, sep=",", index=False)

    def reporte_facturas_detalles(self, dict_in):
        self.df_facturas = self.crear_dataframe(facturas=True)
        self.df_detalle_factura = self.crear_dataframe(detalles_facturas=True)
        filtro = self.df_facturas['emision'].notna() & (self.df_facturas['emision'] != '')
        self.df_facturas = self.df_facturas[filtro]
        
        df_vehiculos = Gestion_Vehiculos()
        df_vehiculos = df_vehiculos.cargar_datos()[['id','placa','tipo_vehiculo','categoria']]
        df_vehiculos = df_vehiculos.rename(columns={'id':'id_vehiculo'})
        
        df_clientes = Gestion_Clientes()
        df_clientes = df_clientes.cargar_datos()[['id','cedula','nombre']]
        df_clientes = df_clientes.rename(columns={'id':'id_cliente'})
        
        self.df_facturas = self.df_facturas.merge(df_vehiculos, how='left',
                                                  left_on='id_vehiculo', right_on='id_vehiculo')
        self.df_facturas = self.df_facturas.merge(df_clientes, how='left',
                                                  left_on='id_cliente', right_on='id_cliente')
        
        self.df_facturas = self.df_facturas.rename(columns={'id':'id_factura', 'emision':'fecha_emision'})
        
        df_final = self.df_facturas.merge(self.df_detalle_factura, how='left',
                                          left_on='id_factura', right_on='id_factura')
        
        df_final = df_final[(df_final['fecha_emision'] >= dict_in['fecha_min']) & (df_final['fecha_emision'] <= dict_in['fecha_max'])]
        
        if dict_in['tipo_vehiculo'] != 'Todos':
            df_final = df_final[df_final['tipo_vehiculo'] == dict_in['tipo_vehiculo']]
            
        if dict_in['servicio'] != 'Todos':
            df_final = df_final[df_final['servicio'] == dict_in['servicio']]
        
        if dict_in['metodo_pago'] != 'Todos':
            df_final = df_final[df_final['metodo_pago'] == dict_in['metodo_pago']]
        
        df_front = df_final[['id_factura','fecha_emision','placa','tipo_vehiculo','categoria','cedula','nombre',
                             'fecha_ingreso', 'hora_ingreso', 'fecha_salida', 'hora_salida',
                             'subtotal','descuento','iva','total']].drop_duplicates()
        
        df_download = df_final[['id_factura','servicio','precio','realizado']]
        
        return df_front, df_download
    
class Historiales:
    def __init__(self):
        self.facturas = 'pages/data/facturas.csv'
        self.clientes = 'pages/data/clientes.csv'
        self.vehiculos = 'pages/data/vehicles.csv'
    
    def cargar_dataframe(self):
        self.df_facturas = pd.read_csv(self.facturas, dtype=str)
        self.df_clientes = pd.read_csv(self.clientes, dtype=str)
        self.df_vehiculos = pd.read_csv(self.vehiculos, dtype=str)
        return self.df_facturas,self.df_clientes,self.df_vehiculos
    
    def historial_clientes(self,id_cliente):
        self.cargar_dataframe()
        self.df_historial_cliente = self.df_facturas[self.df_facturas['id_cliente'] == id_cliente]

        df_vehiculos = Gestion_Vehiculos()
        df_vehiculos = df_vehiculos.cargar_datos()[['id','placa','tipo_vehiculo','categoria']]
        df_vehiculos = df_vehiculos.rename(columns={'id':'id_vehiculo'})
        
        self.df_historial_cliente = self.df_historial_cliente.merge(df_vehiculos, how='left',
                                                  left_on='id_vehiculo', right_on='id_vehiculo')
        self.df_historial_cliente = self.df_historial_cliente[['id','placa','tipo_vehiculo','categoria','emision','fecha_ingreso','hora_ingreso','fecha_salida',
                                             'hora_salida','metodo_pago',
                                             'subtotal','promocion','descuento','iva','total']]
        
        return self.df_historial_cliente

    def historial_vehiculos(self,id_vehiculo):
        self.cargar_dataframe()
        self.df_historial_vehiculo = self.df_facturas[self.df_facturas['id_vehiculo'] == id_vehiculo]
        
        df_clientes = Gestion_Clientes()
        df_clientes = df_clientes.cargar_datos()[['id','cedula','nombre']]
        df_clientes = df_clientes.rename(columns={'id':'id_cliente'})

        self.df_historial_vehiculo = self.df_historial_vehiculo.merge(df_clientes, how='left',
                                                  left_on='id_cliente', right_on='id_cliente')
        self.df_historial_vehiculo = self.df_historial_vehiculo[['id','cedula','nombre','emision','fecha_ingreso','hora_ingreso','fecha_salida',
                                             'hora_salida','metodo_pago',
                                             'subtotal','promocion','descuento','iva','total']]
    
        return self.df_historial_vehiculo
    
    def generar_excel(self, df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Historial')
        output.seek(0)
        return output

    def min_max_date_clientes(self,df):
        filtro = df['emision'].notna() & (df['emision'] != '')
        df = df[filtro]
        min_date = datetime.datetime.strptime(str(df['emision'].min()), '%Y-%m-%d').date()
        max_date = datetime.datetime.strptime(str(df['emision'].max()), '%Y-%m-%d').date()
        return min_date, max_date
    
    def min_max_date_vehiculo(self,df):
        filtro = df['emision'].notna() & (df['emision'] != '')
        df = df[filtro]
        min_date = datetime.datetime.strptime(str(df['emision'].min()), '%Y-%m-%d').date()
        max_date = datetime.datetime.strptime(str(df['emision'].max()), '%Y-%m-%d').date()
        return min_date, max_date
    
    def emision_actual(self):
        df = self.cargar_dataframe()[0]
        df['emision'] = pd.to_datetime(df['emision'])
        fecha_actual = datetime.datetime.now().date()
        filtro = df['emision'].dt.date == fecha_actual
        self.df_facturas = self.df_facturas[filtro]
        
        detalles_facturas = Billing()
        df_detalle_factura = detalles_facturas.crear_dataframe(detalles_facturas=True)

        df_vehiculos = Gestion_Vehiculos()
        df_vehiculos = df_vehiculos.cargar_datos()[['id','placa','tipo_vehiculo']]
        df_vehiculos = df_vehiculos.rename(columns={'id':'id_vehiculo'})
        
        df_clientes = Gestion_Clientes()
        df_clientes = df_clientes.cargar_datos()[['id','cedula','nombre']]
        df_clientes = df_clientes.rename(columns={'id':'id_cliente'})
        
        self.df_facturas = self.df_facturas.merge(df_vehiculos, how='left',
                                                  left_on='id_vehiculo', right_on='id_vehiculo')
        self.df_facturas = self.df_facturas.merge(df_clientes, how='left',
                                                  left_on='id_cliente', right_on='id_cliente')
        
        self.df_facturas = self.df_facturas.rename(columns={'id':'id_factura'})
        
        self.df_facturas = self.df_facturas.merge(df_detalle_factura, how='left',
                                                 left_on='id_factura', right_on='id_factura')
        
        df_front = self.df_facturas[['id_factura','placa','cedula','nombre','fecha_ingreso',
                                     'hora_ingreso','subtotal','promocion','descuento','iva','total']].drop_duplicates()
        
        df_download = self.df_facturas[['id_factura','servicio','precio','realizado']]
        
        return df_front, df_download
    
    def generar_excel_facturas(self, df1, df2):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Se genera una hoja para facturas
            df1.to_excel(writer, index=False, sheet_name='Facturas')
            
            # Se genera una hoja para los detalles de las facturas
            df2.to_excel(writer, index=False, sheet_name='Detalles Facturas')
        output.seek(0)
        return output