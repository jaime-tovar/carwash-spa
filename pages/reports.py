from navigation import make_sidebar
import streamlit as st
import datetime
from pages.back_util_functions import Gestion_Servicios, Billing, Historiales

make_sidebar()

st.header("Reportes")

dict_tipo_vehiculo = Gestion_Servicios()
dict_tipo_vehiculo = dict_tipo_vehiculo.diccionario_tipos_vehiculos_servicios()
dict_tipo_vehiculo['Moto'] = list(set(dict_tipo_vehiculo['Moto']))
dict_tipo_vehiculo['Carro'] = list(set(dict_tipo_vehiculo['Carro']))
dict_tipo_vehiculo['Todos'] = list(set(dict_tipo_vehiculo['Moto'] + dict_tipo_vehiculo['Carro']))

servicios_instance = Gestion_Servicios()
min_date, max_date = servicios_instance.min_max_date()

billing_instance = Billing()

col1, col2 = st.columns(2)

rango_fecha = col1.date_input(
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

metodo_pago = col2.selectbox('Métodos de Pago',
                             options = ['Todos','Efectivo','Tarjeta Crédito/Débito', 'Transferencia/QR'],
                             key = "selectbox_3")

dict_filters ={
    'fecha_min' : rango_fecha[0].strftime('%Y-%m-%d'),
    'fecha_max' : rango_fecha[1].strftime('%Y-%m-%d'),
    'tipo_vehiculo' : tipo_vehiculo,
    'servicio' : servicio,
    'metodo_pago' : metodo_pago
}

df1, df2 = billing_instance.reporte_facturas_detalles(dict_filters)

if df1.empty:
    st.warning('Los filtros que ha usado no generan datos')
else:
    reportes_descarga = Historiales()
    archivo_excel = reportes_descarga.generar_excel_facturas(df1, df2)
    st.download_button(label = "Descargar Reporte",
                    data = archivo_excel.getvalue(),
                    file_name= f"reporte_{dict_filters['fecha_min']}_{dict_filters['fecha_max']}.xlsx",
                    mime= "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type='primary')
    st.header('Vista previa')
    st.subheader('Facturas')
    event = st.dataframe(df1,
                        key="facturas",
                        column_config={
                            "id_factura": st.column_config.TextColumn("Factura N°", default="st."),
                            "fecha_emision": st.column_config.TextColumn("Fecha Emisión", default="st."),
                            "placa": st.column_config.TextColumn("Placa Vehículo", default="st."),
                            "tipo_vehiculo": st.column_config.TextColumn("Tipo Vehículo", default="st."),
                            "categoria": st.column_config.TextColumn("Categoria", default="st."),
                            "cedula": st.column_config.TextColumn("Cédula Propietario", default="st."),
                            "nombre": st.column_config.TextColumn("Propietario", default="st."),
                            "fecha_ingreso": st.column_config.TextColumn("Fecha Ingreso", default="st."),
                            "hora_ingreso": st.column_config.TextColumn("Hora Ingreso", default="st."),
                            "fecha_salida": st.column_config.TextColumn("Fecha Salida", default="st."),
                            "hora_salida": st.column_config.TextColumn("Hora Salida", default="st."),
                            "subtotal": st.column_config.TextColumn("Subtotal", default="st."),
                            "descuento": st.column_config.TextColumn("Descuento", default="st."),
                            "iva": st.column_config.TextColumn("IVA", default="st."),
                            "total": st.column_config.TextColumn("Total", default="st."),
                            },
                        hide_index=True)

    st.subheader('Detalle Facturas')
    st.dataframe(df2,
                key="detalles_facturas",
                column_config={
                    "id_factura": st.column_config.TextColumn("Factura N°", default="st."),
                    "servicio": st.column_config.TextColumn("Servicio", default="st."),
                    "precio": st.column_config.TextColumn("Precio", default="st."),
                    "realizado": st.column_config.CheckboxColumn("¿Fue realizado?")
                },
                hide_index=True)
