import streamlit as st
from dotenv import load_dotenv

from utils.styles import aplicar_estilos  # noqa
from utils.menu import menu_lateral  # noqa
from utils.logo import logo  # noqa
from utils.interface import mostrar_lista_agentes  # noqa

load_dotenv()

st.set_page_config(layout="wide", page_title="Agent Gallery")

aplicar_estilos()
menu_lateral()
logo()

st.markdown("<hr>", unsafe_allow_html=True)
st.write("#### Galeria de Agentes")
st.markdown('<div style="height: 45px;"></div>', unsafe_allow_html=True)

mostrar_lista_agentes()
