import streamlit as st 
import asyncio
from basic_agent import response_mcp

st.set_page_config(
    page_title="AI Agent",
    layout="wide"
)

# Definimimso el estado para guardar el historial
if "chat" not in st.session_state:
    st.session_state.chat = []

# mostramos el historial
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Esperamos la entrada del usuario
pregunta = st.chat_input("En que te puedo ayudar?")
if pregunta:
    st.session_state.chat.append({"role":"user","content":pregunta})
    
    # Respuesta del agente
    response = asyncio.run(response_mcp(pregunta))
    st.session_state.chat.append({"role":"ai","content":response})