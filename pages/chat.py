import streamlit as st
from dotenv import load_dotenv
import requests
import os
from utils.interface import GALLERY_ENDPOINT
from utils.styles import aplicar_estilos  # noqa
from utils.menu import menu_lateral  # noqa
from utils.logo import logo  # noqa


API_BASE_URL = os.getenv("api_url")
PREDICT_ENDPOINT = f"{API_BASE_URL}/predict"

load_dotenv()

st.set_page_config(layout="wide", page_title="Agent Gallery")

aplicar_estilos()
menu_lateral()
logo()

query_id = st.query_params.get("agent_id")
if query_id:
    st.session_state["agent_id"] = query_id

agent_id = st.session_state.get("agent_id")

if "user_message" not in st.session_state:
    st.session_state.user_message = ""
if "agent_response" not in st.session_state:
    st.session_state.agent_response = ""

if agent_id:
    st.markdown(
        f"<h4 style='text-align: center;'>Agente: {agent_id}</h4>",
        unsafe_allow_html=True,
    )

    with st.spinner("Carregando dados do agente... ⏳"):
        try:
            response = requests.get(GALLERY_ENDPOINT, params={"agent_id": agent_id})
            response.raise_for_status()
            data = response.json()  # espera lista de dicts
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao buscar dados: {e}")
            data = []

    if data:
        agent_info = data[0]

        st.markdown(
            "<h5 style='text-align: left;'>Prompt do agente:</h5>",
            unsafe_allow_html=True,
        )
        st.markdown(f"<p>{agent_info['prompt']}</p>", unsafe_allow_html=True)

        st.markdown("---")  # separador

        st.markdown("<h5>Mensagem do usuário:</h5>", unsafe_allow_html=True)
        user_input = st.text_area(
            label="",
            value=st.session_state.user_message,
            height=100,
            key="user_textarea",  # chave única
        )

        if st.button("Enviar"):
            if user_input.strip():
                st.session_state.user_message = user_input
                print(f"Mensagem do usuário: {user_input}")

                with st.spinner("Enviando mensagem... ⏳"):
                    try:
                        payload = {"agent_id": agent_id, "message": user_input}
                        resp = requests.post(PREDICT_ENDPOINT, json=payload)
                        resp.raise_for_status()
                        st.session_state.agent_response = resp.json().get(
                            "reply", "Sem resposta da API."
                        )
                    except requests.exceptions.RequestException as e:
                        st.session_state.agent_response = f"Erro na requisição: {e}"
            else:
                st.warning("Digite algo antes de enviar!")

        st.markdown("<h4>Resposta do agente:</h4>", unsafe_allow_html=True)
        st.text_area(
            label="",
            value=st.session_state.agent_response,
            height=350,
            key="agent_textarea",  # chave única
            disabled=True,
        )

else:
    st.error("Nenhum agente selecionado!")
