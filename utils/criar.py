import streamlit as st
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()
API_BASE_URL = os.getenv("api_url")
AGENT_ENDPOINT = f"{API_BASE_URL}/agent"


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
