from navigation import make_sidebar
import streamlit as st
from datetime import datetime
from time import sleep
from pages.back_util_functions import Billing

make_sidebar()

st.session_state.df_state_facturas = False
st.session_state.df_state_detalle_factura = False
st.session_state.validaciones_data = True

def data_editor(df):
    edited_df = st.data_editor(
        df,
        column_config={
            'realizado': st.column_config.CheckboxColumn(
                '¿Se realizó?',
                help='Marque o desmarque si el servicio se realizó',
            ),
            'servicio': st.column_config.TextColumn("Servicios", default="st.", width='medium'),
            'precio_formateado': 'Precio',
        },
        disabled=['servicio','precio_formateado'],
        hide_index=True,
    )
    return edited_df

def obtener_subtotal(df):
    precios = df[df['realizado'] == 'True'].to_dict()
    precios = precios['precio_formateado'].values()
    # Eliminar el formato y convertir a enteros
    subtotal = sum(int(precio.replace("$", "").replace(",", "").strip()) for precio in precios)
    return subtotal

def formatear_a_precio(a):
    cadena_formateada = f"{a:,.2f}"

    # Reemplazar el separador de miles y decimales si es necesario (en caso de que el sistema local use otro formato)
    cadena_formateada = cadena_formateada.replace(",", "X").replace(".", ",").replace("X", ".")

    # Agregar el signo de pesos al principio
    precio = f"$ {cadena_formateada}"

    return precio

billing_instance = Billing()

@st.dialog("Facturar servicio")
def btn_facturar(dict_in):
    st.write('Detalles de Factura')
    detalles_factura = billing_instance.detalles_factura(dict_in['id_factura'])
    df_original = detalles_factura[['realizado','servicio','precio_formateado']]
    
    df_editado = data_editor(df_original)
    ediciones_encontradas = df_original.equals(df_editado)
    
    if not ediciones_encontradas:
        st.warning('Estas actualizando los servicios que serán facturados')  
        ediciones_check = st.checkbox('¿Deseas guardar estas ediciones en el servicio?')
    
    col1, col2 = st.columns(2)
    subtotal = obtener_subtotal(df_editado)
    col1.text_input('Subtotal', value=formatear_a_precio(subtotal), disabled=True)
    descuento = col2.number_input('Descuento', step=5, format='%d', min_value=0, max_value=100)
    iva = subtotal*0.19
    col1.text_input('IVA 19%', value=formatear_a_precio(iva), disabled=True)
    total = subtotal+iva-(subtotal*descuento/100)
    col2.text_input('Total', value=formatear_a_precio(total), disabled=True)
    
    metodo_pago = st.selectbox('Método de pago', ['Efectivo','Tarjeta Crédito/Débito', 'Transferencia/QR'])
    
    left, right = st.columns(2)
    if metodo_pago == 'Efectivo':
        recibido = left.number_input('Dinero recibido', min_value=0, format='%d', step=50)
        right.write('Cambio')
        if recibido < total:
            st.warning('Debe ingresar un valor mayor o igual al total')
            st.session_state.validaciones_data = False
        else:
            st.session_state.validaciones_data = True
            cambio = recibido-total
            right.write(formatear_a_precio(recibido-total))
    else:
        st.session_state.validaciones_data = True
    
    dict_final_billing = {
        'id_factura' : dict_in['id_factura'],
        'subtotal' : subtotal,
        'descuento' : descuento,
        'iva' : iva,
        'total' : total,
        'metodo_pago' : metodo_pago,
        'servicios' : {
            'servicio' : df_editado.to_dict()['servicio'],
            'precio' : df_editado.to_dict()['precio_formateado'],
            'realizado' : df_editado.to_dict()['realizado']
            }
    }
    
    if st.button("Facturar", key=3, type='primary'):
        if st.session_state.validaciones_data:
            if ediciones_encontradas:
                billing_instance.facturar_servicio(dict_final_billing)
                st.success("Servicio terminado y facturado exitosamente")
                sleep(1)
                st.rerun()
            else:
                if ediciones_check:
                    billing_instance.facturar_servicio(dict_final_billing)
                    st.success("Servicio terminado y facturado exitosamente")
                    sleep(1)
                    st.rerun()
                else:
                    st.warning('Usted ha realizado cambio en los servicios a facturar, primero confirme si desea guardarlos')
        else:
            st.error('Datos incorrectos')

st.header("Facturación")

left, middle, right = st.columns(3)
        
if not st.session_state.df_state_facturas:
    st.session_state.df_facturas_activas = billing_instance.facturas_activas()
    st.session_state.df_state_facturas = True

if st.session_state.df_facturas_activas.empty:
    st.warning('No hay facturas activas en este momento')
else:

    event_facturas_activas = st.dataframe(
        st.session_state.df_facturas_activas,
        key="facturas_activas",
        on_select="rerun",
        selection_mode=['single-row'],
        hide_index=True,
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
            'subtotal' : float(st.session_state.df_facturas_activas.iloc[event_facturas_activas.selection.rows].iat[0, 6]),
            'promocion' : str(st.session_state.df_facturas_activas.iloc[event_facturas_activas.selection.rows].iat[0, 7]),
            'descuento' : float(st.session_state.df_facturas_activas.iloc[event_facturas_activas.selection.rows].iat[0, 8]),
            'iva' : float(st.session_state.df_facturas_activas.iloc[event_facturas_activas.selection.rows].iat[0, 9]),
            'total' : float(st.session_state.df_facturas_activas.iloc[event_facturas_activas.selection.rows].iat[0, 10])
        }
    except IndexError:
        facturas_activas_selection = None

    if "btn_facturar" not in st.session_state:
        if left.button("Facturar", key=21, type="primary"):
            if facturas_activas_selection is None:
                st.toast('Primero seleccione un registro')
            else:
                btn_facturar(facturas_activas_selection)