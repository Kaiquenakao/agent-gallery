import streamlit as st


def aplicar_estilos():
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
