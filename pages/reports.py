from navigation import make_sidebar
import streamlit as st
import datetime
from pages.back_util_functions import Gestion_Clientes, Gestion_Vehiculos, Gestion_Servicios

make_sidebar()

st.header("Reportes")

dict_tipo_vehiculo = Gestion_Servicios()
dict_tipo_vehiculo = dict_tipo_vehiculo.diccionario_tipos_vehiculos_servicios()
dict_tipo_vehiculo['Moto'] = list(set(dict_tipo_vehiculo['Moto']))
dict_tipo_vehiculo['Carro'] = list(set(dict_tipo_vehiculo['Carro']))
dict_tipo_vehiculo['Todos'] = list(set(dict_tipo_vehiculo['Moto'] + dict_tipo_vehiculo['Carro']))

servicios_instance =Gestion_Servicios()
min_date, max_date = servicios_instance.min_max_date()

col1, col2 = st.columns(2)

d = col1.date_input(
    "Seleccione el rango de fechas",
    (min_date, max_date),
    min_date,
    max_date,
    format="YYYY/MM/DD",
)

tipo_vehiculo = col2.selectbox('Tipo de Vehículo',
                               options = dict_tipo_vehiculo.keys(),
                               index=2,
                               key = "selectbox_1")
servicio = col1.selectbox('Servicio',
                          options = ['Todos']+dict_tipo_vehiculo[tipo_vehiculo],
                          key = "selectbox_2")

metodos_pago = col2.selectbox('Métodos de Pago',
                              options = ['Todos','Efectivo','Tarjeta Crédito/Débito', 'Transferencia/QR'],
                              key = "selectbox_3")