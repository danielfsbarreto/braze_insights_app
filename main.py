import streamlit as st
from dotenv import load_dotenv
import os

from models import Conversation, Message
from services import MessageSubmissionService

st.session_state.setdefault("conversation", Conversation())
st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("username", "")

load_dotenv()

def authenticate_user(username: str, password: str) -> bool:
    return username == os.getenv("ADMIN_USERNAME") and password == os.getenv("ADMIN_PASSWORD")

def login_form():
    st.title("🔐 Autenticação - Braze Insights")
    st.markdown("---")

    with st.form("login_form"):
        st.subheader("Entre com suas credenciais")
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submit_button = st.form_submit_button("Entrar")

        if submit_button:
            if authenticate_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos. Tente novamente.")

def logout():
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.conversation = Conversation()
    st.rerun()

def main_app():
    def _process_user_message():
        user_message = Message(role="user", content=st.session_state["chat_input"])
        with conversation.container():
            with st.chat_message(user_message.role):
                st.write(user_message.content)

            with st.spinner(text="Processando...", show_time=True):
                assistant_message = MessageSubmissionService(
                    st.session_state.conversation
                ).send_message(user_message)
                st.session_state.conversation.messages.append(user_message)
                st.session_state.conversation.messages.append(assistant_message)

    with st.sidebar:
        st.logo(
            "https://cdn.prod.website-files.com/66cf2bfc3ed15b02da0ca770/66d07240057721394308addd_Logo%20(1).svg",
            size="large",
        )
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"👤 **Usuário:** {st.session_state.username}")
        with col2:
            if st.button("Sair", type="secondary"):
                logout()
        st.divider()
        st.title("Insights da Braze")
        st.write(
            """
            Esta é uma aplicação com o intuito de demonstrar o potencial da CrewAI para lidar com casos de uso
            conversacionais integrados aos dados hospedados na Braze.

            No momento há suporte para agentes trabalharem de forma reativa a mensagens de um usuário, mas isto
            só mostra a arte do possível.

            **Futuramente, o objetivo será ter agentes que trabalham de forma proativa,
            buscando informações na Braze baseados em dados históricos e suas preferências.**
            """
        )
        st.divider()
        st.write(
            "Se aplicações como esta te interessam, por favor, saiba mais sobre a nossa empresa em https://crewai.com/."
        )
        st.link_button(
            "**Inscreva-se para uma avaliação gratuita**",
            "https://app.crewai.com/",
            type="primary",
        )

    with st.container():
        st.title("Conversa")
        conversation = st.container()

    with st._bottom:
        st.chat_input(
            key="chat_input",
            placeholder="Receba insights da Braze aqui",
            on_submit=_process_user_message,
        )

    @st.fragment
    def _render_message(message: Message):
        with st.chat_message(message.role):
            st.write(message.content)

    for message in st.session_state.conversation.messages:
        with conversation.container():
            _render_message(message)

if __name__ == "__main__":
    if not st.session_state.authenticated:
        login_form()
    else:
        main_app()
