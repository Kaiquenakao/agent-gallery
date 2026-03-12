import streamlit as st
from dotenv import load_dotenv
import requests
import os
from utils.interface import GALLERY_ENDPOINT
from utils.styles import aplicar_estilos  # noqa
from utils.menu import menu_lateral  # noqa
from utils.logo import logo  # noqa

# Carrega variáveis de ambiente
load_dotenv()
API_BASE_URL = os.getenv("api_url")
PREDICT_ENDPOINT = f"{API_BASE_URL}/predict"

st.set_page_config(layout="wide", page_title="Agent Gallery")

# Aplica componentes de interface
aplicar_estilos()
menu_lateral()
logo()

# Gerenciamento de IDs via Query Params ou Session State
query_id = st.query_params.get("agent_id")
if query_id:
    st.session_state["agent_id"] = query_id

agent_id = st.session_state.get("agent_id")

# Inicialização do Session State
if "agent_response" not in st.session_state:
    st.session_state.agent_response = ""
if "user_textarea" not in st.session_state:
    st.session_state.user_textarea = ""

if agent_id:
    st.markdown(
        f"<h4 style='text-align: center;'>Agente: {agent_id}</h4>",
        unsafe_allow_html=True,
    )

    with st.spinner("Carregando dados do agente... ⏳"):
        try:
            response = requests.get(GALLERY_ENDPOINT, params={"agent_id": agent_id})
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao buscar dados: {e}")
            data = []

    if data:
        agent_info = data[0]

        st.markdown("<h5>Prompt do agente:</h5>", unsafe_allow_html=True)
        st.text_area(
            label="",
            value=agent_info.get("prompt", ""),
            height=90,
            disabled=True,
            key="agent_prompt_display",
            label_visibility="collapsed",
        )

        st.markdown("---")

        # Entrada do Usuário
        st.markdown("<h5>Mensagem do usuário:</h5>", unsafe_allow_html=True)
        user_input = st.text_area(
            label="",
            height=100,
            key="user_textarea",  # O estado é mantido automaticamente aqui
            label_visibility="collapsed",
        )

        if st.button("Enviar"):
            if st.session_state.user_textarea.strip():
                with st.spinner("Enviando mensagem... ⏳"):
                    try:
                        payload = {
                            "agent_id": agent_id,
                            "message": st.session_state.user_textarea,
                        }
                        resp = requests.post(PREDICT_ENDPOINT, json=payload)
                        resp.raise_for_status()

                        # Atualiza a resposta no estado
                        st.session_state.agent_response = resp.json().get(
                            "reply", "Sem resposta da API."
                        )
                        # Força o recarregamento para mostrar a resposta
                        st.rerun()

                    except requests.exceptions.RequestException as e:
                        st.error(f"Erro na requisição: {e}")
            else:
                st.warning("Digite algo antes de enviar!")

        # Exibição da Resposta (Se houver)
        if st.session_state.agent_response:
            st.markdown("---")
            st.markdown("<h5>Resposta do agente:</h5>", unsafe_allow_html=True)

            resposta_limpa = st.session_state.agent_response.replace("\n", "<br>")

            # ESTA É A VERSÃO "BRUTA FORÇA" PARA MATAR O CINZA
            st.markdown(
                f"""
                <div class="black-text-fix">
                    {resposta_limpa}
                </div>

                <style>
                    /* 1. Atacamos a classe que criamos */
                    .black-text-fix {{
                        background-color: #ffffff !important;
                        border: 1px solid #cccccc !important;
                        border-radius: 8px !important;
                        padding: 20px !important;
                        color: #000000 !important;
                    }}

                    /* 2. Resetamos as variáveis de cor do Streamlit dentro dessa div */
                    .black-text-fix, .black-text-fix * {{
                        --text-color: #000000 !important;
                        --primary-color: #000000 !important;
                        color: #000000 !important;
                        -webkit-text-fill-color: #000000 !important;
                        fill: #000000 !important;
                        opacity: 1 !important;
                    }}

                    /* 3. Forçamos o seletor de parágrafo do Streamlit que costuma ser o culpado */
                    .stMarkdown div p {{
                        color: inherit !important;
                    }}
                </style>
                """,
                unsafe_allow_html=True,
            )
else:
    st.error("Nenhum agente selecionado!")
