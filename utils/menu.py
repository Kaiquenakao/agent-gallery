import streamlit as st
from utils.criar import modal_criar_agente  # noqa


def menu_lateral():
    with st.sidebar:
        st.markdown(
            "<h2 style='color: white; text-align: center; margin-top: 0px;'>Agent Gallery</h2>",
            unsafe_allow_html=True,
        )
        st.write("---")
        st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
        if st.button("➕ Criar Agente"):
            modal_criar_agente()
        if st.button("🏠 Início"):
            st.switch_page("app.py")
