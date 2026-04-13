import streamlit as st
import pandas as pd
from chatbot_core import chatbot

# titolo
st.set_page_config(page_title="Chatbot SIAE", page_icon="")
st.title("📄🎶  Chatbot MDA SIAE – Test ")
if st.button("🆕 Nuova conversazione"):
    st.session_state.chat = []
    st.rerun()

with st.chat_message("assistant"):
    st.markdown(
        """📄🎶  **Chatbot MDA SIAE avviato**

Scrivi una domanda del tipo:
- **Dammi informazioni sul locale xyz**
- **locale xyz**

_(digita **Nuova conversazione** per una nuova chat)_"""
    )

# carica Excel
@st.cache_data
def carica_dati():
    return pd.read_excel("mda_google.xlsx")

df = carica_dati()

# stato chat
if "chat" not in st.session_state:
    st.session_state.chat = []

# input utente
domanda = st.chat_input("Scrivi un messaggio…")

if domanda:
    st.session_state.chat.append(("user", domanda))
    risposta = chatbot(domanda, df)
    st.session_state.chat.append(("bot", risposta))

# mostra chat
for ruolo, testo in st.session_state.chat:
    if ruolo == "user":
        with st.chat_message("user"):
            st.write(testo)
    else:
        with st.chat_message("assistant"):
            st.write(testo)

