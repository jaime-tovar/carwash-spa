from navigation import make_sidebar
import streamlit as st
import pandas as pd

make_sidebar()

servicios = {
    'Servicio': ['Lavado Exterior', 'Lavado Interior', 'Lavado Completo', 'Limpieza de Tapicería', 'Pulido y Encerado', 
                 'Lavado de Motor', 'Desinfección Interior', 'Tratamiento de Neumáticos'],
    'Precio (USD)': [15, 10, 30, 25, 40, 20, 18, 12],
    'Tiempo Estimado (min)': [30, 20, 60, 40, 50, 35, 25, 15]
}

df_servicios = pd.DataFrame(servicios)

st.header("Pagina Principal")
st.subheader("Adicionar Servicios", divider='grey')
st.write("")

df_clientes = pd.read_csv('pages/data/clientes.csv')
nombres = df_clientes['nombre'].tolist()
df_vehiculos = pd.read_csv('pages/data/vehicles.csv')
placas = df_vehiculos['placa'].tolist()

left, right = st.columns(2)
opciones1 = nombres
opciones2 = placas

with left:
    seleccion_cliente = st.selectbox("Selecciona un Cliente:", opciones1,  key="selectbox_1")
with right:
    seleccion_vehiculo = st.selectbox("Selecciona un Vehiculo:", opciones2,  key="selectbox_2")

st.write(f"Opción seleccionada: {seleccion_cliente}")

seleccion_servicios = st.multiselect("Selecciona los servicios", df_servicios['Servicio'])
servicios_seleccionados = df_servicios[df_servicios['Servicio'].isin(seleccion_servicios)]

for index, row in servicios_seleccionados.iterrows():
    st.write(f"Servicio: {row['Servicio']}")
    st.write(f"Precio: ${row['Precio (USD)']}")
    st.write(f"Tiempo estimado: {row['Tiempo Estimado (min)']} minutos")
    st.write("---")

cedula_cliente = df_clientes[df_clientes['nombre'] == seleccion_cliente]['cedula'].values[0]

if len(seleccion_servicios) == 0:
    st.warning("¡Debes seleccionar al menos un servicio para continuar!")

elif st.button("Agregar servicio"):
    data_to_save = {
        'Cliente': seleccion_cliente,
        'Cédula': cedula_cliente,
        'Vehículo': seleccion_vehiculo,
        'Placa': seleccion_vehiculo,
        'Servicios': ', '.join(seleccion_servicios)
    }

    df_to_save = pd.DataFrame([data_to_save])
    try:
        df_servicios_existentes = pd.read_csv('pages/data/services.csv')
        df_servicios_existentes = pd.concat([df_servicios_existentes, df_to_save], ignore_index=True)
        df_servicios_existentes.to_csv('pages/data/services.csv', index=False)
    except FileNotFoundError:
        # Si el archivo no existe, crearlo
        df_to_save.to_csv('pages/data/services.csv', index=False)

    st.success("Servicio agregado exitosamente!")


st.subheader("Servicios y Facturacion", divider='grey')


