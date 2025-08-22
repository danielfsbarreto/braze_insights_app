import streamlit as st
from dotenv import load_dotenv

from models import Conversation, Message
from services import MessageSubmissionService

st.session_state.setdefault("conversation", Conversation())


load_dotenv()


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


## UI COMPONENTS ##


@st.fragment
def _render_message(message: Message):
    with st.chat_message(message.role):
        st.write(message.content)


with st.sidebar:
    st.logo(
        "https://cdn.prod.website-files.com/66cf2bfc3ed15b02da0ca770/66d07240057721394308addd_Logo%20(1).svg",
        size="large",
    )
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

for message in st.session_state.conversation.messages:
    with conversation.container():
        _render_message(message)
