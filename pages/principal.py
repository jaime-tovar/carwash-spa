from navigation import make_sidebar
import streamlit as st

make_sidebar()

st.header(st.session_state.role)
