import streamlit as st
import requests
import os

API_BASE_URL = os.getenv("api_url")
GALLERY_ENDPOINT = f"{API_BASE_URL}/gallery"


def carregar_agentes():
    try:
        response = requests.get(GALLERY_ENDPOINT)
        if response.status_code == 200:
            st.session_state.lista_agentes = response.json()
        elif response.status_code == 404:
            st.session_state.lista_agentes = []
        else:
            st.error(f"Erro ao carregar agentes: {response.status_code}")
    except Exception as e:
        st.error(f"Erro de conexão com a API: {e}")


def mostrar_lista_agentes():
    if "lista_agentes" not in st.session_state or not st.session_state.lista_agentes:
        carregar_agentes()

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
                                response = requests.get(GALLERY_ENDPOINT, params=params)

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

                    if st.button("Ver Prompt", key=f"ver_prompt_{agent_id_atual}"):
                        modal_ver_prompt()
