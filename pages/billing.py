from navigation import make_sidebar
import streamlit as st
from datetime import datetime
from pages.back_util_functions import Billing

make_sidebar()

st.session_state.df_state_facturas = False
st.session_state.df_state_detalle_factura = False
st.session_state.validaciones_data = True

billing_instance = Billing()

@st.dialog("Facturar servicio")
def btn_facturar():
    st.write('\* Campos obligatorios')
    if st.button("Facturar", key=3):
        if st.session_state.validaciones_data:
            st.success("Servicio terminado y facturado exitosamente")
            sleep(1)
            st.rerun()
        else:
            st.error('Datos incorrectos')

st.header("Facturación")

left, middle, right = st.columns(3)

if "btn_facturar" not in st.session_state:
    if left.button("Facturar", key=1, type="primary"):
        btn_facturar()
        
if not st.session_state.df_state_facturas:
    st.session_state.df_facturas_activas = billing_instance.facturas_activas()
    st.session_state.df_state_facturas = True

event_facturas_activas = st.dataframe(
    st.session_state.df_facturas_activas,
    key="facturas_activas",
    on_select="rerun",
    selection_mode=['single-row'],
    column_config={
        "id_factura": st.column_config.TextColumn("ID", default="st."),
        "placa": st.column_config.TextColumn("Placa", default="st."),
        "cedula": st.column_config.TextColumn("Cédula", default="st."),
        "nombre": st.column_config.TextColumn("Cliente", default="st."),
        "fecha_ingreso": st.column_config.TextColumn("Fecha Ingreso Vehículo", default="st."),
        "hora_ingreso": st.column_config.TextColumn("Hora Ingreso Vehículo", default="st."),
        "subtotal": st.column_config.TextColumn("Subtotal", default="st."),
        "promocion": st.column_config.TextColumn("Promoción", default="st."),
        "descuento": st.column_config.TextColumn("descuento", default="st."),
        "iva" : st.column_config.TextColumn("descuento", default="st."),
        "total": st.column_config.TextColumn("descuento", default="st.")
    }
)

try:
    facturas_activas_selection = {
        'id_factura' : str(st.session_state.df_facturas_activas.iloc[event_facturas_activas.selection.rows].iat[0, 0]),
        'placa' : str(st.session_state.df_facturas_activas.iloc[event_facturas_activas.selection.rows].iat[0, 1]),
        'cedula' : str(st.session_state.df_facturas_activas.iloc[event_facturas_activas.selection.rows].iat[0, 2]),
        'nombre' : str(st.session_state.df_facturas_activas.iloc[event_facturas_activas.selection.rows].iat[0, 3]),
        'fecha_ingreso' : datetime.strptime(st.session_state.df_facturas_activas.iloc[event_facturas_activas.selection.rows].iat[0, 4], "%Y-%m-%d").date(),
        'hora_ingreso' : str(st.session_state.df_facturas_activas.iloc[event_facturas_activas.selection.rows].iat[0, 5]),
        'subtotal' : str(st.session_state.df_facturas_activas.iloc[event_facturas_activas.selection.rows].iat[0, 6]),
        'promocion' : str(st.session_state.df_facturas_activas.iloc[event_facturas_activas.selection.rows].iat[0, 7]),
        'descuento' : str(st.session_state.df_facturas_activas.iloc[event_facturas_activas.selection.rows].iat[0, 8]),
        'iva' : str(st.session_state.df_facturas_activas.iloc[event_facturas_activas.selection.rows].iat[0, 9]),
        'total' : str(st.session_state.df_facturas_activas.iloc[event_facturas_activas.selection.rows].iat[0, 10])
    }
except IndexError:
    facturas_activas_selection = None
    
st.write(facturas_activas_selection)

