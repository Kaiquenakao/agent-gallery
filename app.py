import streamlit as st
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()

st.set_page_config(layout="wide", page_title="Agent Gallery")

API_BASE_URL = os.getenv("api_url")
AGENT_ENDPOINT = f"{API_BASE_URL}/agent"

st.markdown(
    """
    <style>
    /* Remove o espaço vazio no topo */
    .block-container { padding-top: 1rem !important; }

/* REMOVE A LISTA DE PÁGINAS (app, chat, etc) */
    [data-testid="sidebar-nav"] {
        display: none !important;
    }

    /* Estilização da Sidebar (Preto e Roxo) */
    [data-testid="stSidebar"] { 
        background-color: #000000; 
        border-right: 2px solid #6a0dad; 
    }  

    /* Estilização da Sidebar (Preto e Roxo) */
    [data-testid="stSidebar"] { 
        background-color: #000000; 
        border-right: 2px solid #6a0dad; 
    }
    
    /* Container para empurrar botões para o fundo */
    [data-testid="stSidebarUserContent"] { 
        display: flex; 
        flex-direction: column; 
        height: 95vh; 
    }
    
    .spacer { flex-grow: 1; }

    /* Padronização dos Botões da Sidebar */
    div.stButton > button {
        width: 100%; min-height: 40px; background-color: #6a0dad; color: white;
        border-radius: 8px; border: none; font-weight: bold; font-size: 14px;
        display: flex; align-items: center; justify-content: center; gap: 10px;
        transition: 0.3s; margin-bottom: 10px;
    }
    div.stButton > button:hover { 
        background-color: #4b0082; 
        border: 1px solid white; 
    }

    /* CENTRALIZAÇÃO ABSOLUTA DO LOGO */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-top: 0px;
        margin-bottom: -30px; /* Ajuste para aproximar da linha hr */
    }

    .logo-img {
        width: 200px; /* Tamanho do logo */
        height: auto;
    }
    
    /* Linha divisória fina */
    hr { margin-top: 0px !important; margin-bottom: 20px !important; border: 0; border-top: 1px solid #333; }
    
    /* Ajuste de gaps do Streamlit */
    [data-testid="stVerticalBlock"] { gap: 0rem !important; }
    </style>
""",
    unsafe_allow_html=True,
)

if "lista_agentes" not in st.session_state:
    st.session_state.lista_agentes = []


@st.dialog("Novo Agente 🤖")
def modal_criar_agente():
    st.write("Preencha os campos obrigatórios abaixo.")

    with st.form("form_agente", clear_on_submit=False):
        nome_input = st.text_input("Agent ID *", placeholder="ex: assistente_comercial")
        agent_id = nome_input.replace(" ", "_").lower().strip()

        if nome_input:
            st.caption(f"ID gerado: `{agent_id}`")

        descricao = st.text_input(
            "Descrição *", placeholder="Ex: Analisa planilhas e gera relatórios."
        )
        prompt = st.text_area(
            "Prompt de Sistema *",
            height=200,
            placeholder="Você é um especialista em...",
        )

        submit = st.form_submit_button("Criar Agente")

        if submit:
            if not nome_input.strip() or not descricao.strip() or not prompt.strip():
                st.error("Todos os campos são obrigatórios!")
                return

            timezone_br = pytz.timezone("America/Sao_Paulo")
            agora_br = datetime.now(timezone_br)
            timestamp_iso = agora_br.isoformat()

            payload = {
                "agent_id": f"agent_{agent_id}",
                "description": descricao,
                "prompt": prompt,
                "created_at": timestamp_iso,
            }

            try:
                with st.spinner("Conectando ao servidor AWS..."):
                    response = requests.post(AGENT_ENDPOINT, json=payload, timeout=15)

                if response.status_code in [200, 201]:
                    st.success(f"✅ Agente '{agent_id}' criado com sucesso!")
                    st.session_state.lista_agentes.append(payload)
                    st.rerun()
                else:
                    st.error(f"Erro na API ({response.status_code}): {response.text}")
            except Exception as e:
                st.error(f"Falha na conexão com a API: {e}")


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
        st.rerun()

logo_path = "img/agent_gallery.png"

import base64


def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


img_b64 = get_image_base64(logo_path)

if img_b64:
    st.markdown(
        f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{img_b64}" class="logo-img">
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        "<h1 style='text-align: center; color: #6a0dad;'>Agent Gallery</h1>",
        unsafe_allow_html=True,
    )

st.markdown("<hr>", unsafe_allow_html=True)

st.write("#### Galeria de Agentes")

st.markdown('<div style="height: 45px;"></div>', unsafe_allow_html=True)

API_URL_GET = f"{API_BASE_URL}/gallery"


def carregar_agentes():
    try:
        response = requests.get(API_URL_GET)
        if response.status_code == 200:
            st.session_state.lista_agentes = response.json()
        elif response.status_code == 404:
            st.session_state.lista_agentes = []
        else:
            st.error(f"Erro ao carregar agentes: {response.status_code}")
    except Exception as e:
        st.error(f"Erro de conexão com a API: {e}")


if "lista_agentes" not in st.session_state or not st.session_state.lista_agentes:
    carregar_agentes()

# --- SEU CÓDIGO DE INTERFACE ---
if not st.session_state.get("lista_agentes"):
    st.info(
        "Nenhum agente registrado ainda. Crie um novo agente usando o botão na barra lateral."
    )
else:
    # CSS para os cards
    st.markdown(
        """
        <style>
        .card-link {
            text-decoration: none !important;
            color: inherit !important;
            display: block;
            transition: 0.2s;
            border-radius: 10px;
        }
        .card-link:hover {
            background-color: rgba(255, 255, 255, 0.05);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    for idx, agente in enumerate(st.session_state.lista_agentes):
        with cols[idx % 3]:
            url_destino = f"chat?agent_id={agente['agent_id']}"

            with st.container(border=True):
                st.markdown(
                    f"""
                    <a href="{url_destino}" target="_self" class="card-link">
                        <div style="text-align: center; padding: 10px;">
                            <div style="font-size: 40px;">🤖</div>
                            <h3 style="margin: 0px; font-size: 15px;">{agente["agent_id"]}</h3>
                            <p style="margin-top: 0px; font-size: 14px;">
                                {(agente["description"][:47] + "...") if len(agente["description"]) > 50 else agente["description"]}
                            </p>
                        </div>
                    </a>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown("---")
                st.markdown(f"📅 {agente.get('created_at', 'N/A')[:10]}")

                agent_id_atual = agente.get("agent_id")

                @st.dialog(f"Prompt de: {agent_id_atual}")
                def modal_ver_prompt():
                    with st.spinner("Buscando prompt..."):
                        try:
                            params = {"agent_id": agent_id_atual, "prompt": True}
                            response = requests.get(API_URL_GET, params=params)

                            if response.status_code == 200:
                                dados = response.json()

                                if isinstance(dados, list) and len(dados) > 0:
                                    prompt_texto = dados[0].get(
                                        "prompt", "Prompt não encontrado."
                                    )
                                else:
                                    prompt_texto = dados.get(
                                        "prompt", "Prompt não encontrado."
                                    )

                                st.code(prompt_texto, language="markdown")
                            else:
                                st.error(
                                    f"Erro ao buscar prompt (Status: {response.status_code})"
                                )
                        except Exception as e:
                            st.error(f"Falha na conexão: {e}")

                if st.button("Ver Prompt"):
                    modal_ver_prompt()
