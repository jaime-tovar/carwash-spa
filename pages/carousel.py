import streamlit as st

# Crear una lista de imágenes y sus textos
imagenes = [
    {"img": "https://fotos.perfil.com/2023/06/21/st-car-detailing-el-spa-para-autos-que-re-valoriza-tu-capital-y-rejuvenece-tu-vehiculo-1592748.jpg", "texto": "Lavado Y Encerado"},
    {"img": "https://siempreauto.com/wp-content/uploads/sites/9/2020/11/Bugatti-Chiron-Super-Sport.jpg?quality=80&strip=all", "texto": "Servicio de Cofianza"},
    {"img": "https://bxrepsol.s3.eu-west-1.amazonaws.com/static/2024/03/18091752/F1.jpg", "texto": "La mejor calidad y servicio"},
    {"img": "https://pulitocarwash.co/wp-content/uploads/2020/08/Dise%C3%B1o-sin-t%C3%ADtulo-2.png", "texto": "Las mejores marcas"},
]

# Mantener el índice de la imagen actual con st.session_state
if "indice" not in st.session_state:
    st.session_state.indice = 0

# Crear botones para navegar por las imágenes
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    if st.button("⬅️ Anterior"):
        st.session_state.indice = (st.session_state.indice - 1) % len(imagenes)
with col3:
    if st.button("➡️ Siguiente"):
        st.session_state.indice = (st.session_state.indice + 1) % len(imagenes)

# Mostrar la imagen y el texto actual
imagen_actual = imagenes[st.session_state.indice]
st.image(imagen_actual["img"], use_container_width=True)
st.write(imagen_actual["texto"])
