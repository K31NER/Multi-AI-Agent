import sys
import asyncio
import nest_asyncio
import streamlit as st 
from basic_agent import agent
from UI.elemts import add_title,add_sidebar

st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# * -------------------- Configuracion inicial ---------------------------------
# 1. En Windows, asegurar que usamos ProactorEventLoop
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
# 2. Parche para permitir llamadas anidadas a asyncio.run()
nest_asyncio.apply()

# Llamas a la función al inicio
contexto, agent_type, temperatura, top_p, top_k, max_token, disable_summary, color = add_sidebar()

# Definimos el titulo
add_title(titulo="AI Agent",icon="🤖",color=color)

# *---------------------- Variables de estado ---------------------------------*
# Definimimso el estado para guardar el historial
if "chat" not in st.session_state:
    st.session_state.chat = []
    
# Definimos el historial en la session 
if "history" not in st.session_state:
    st.session_state.history = []
    
# Instanciamos el historial
history = st.session_state.history

# Definimos el contexto en el estado de la app
if "contexto" not in st.session_state or st.session_state.contexto != contexto:
    st.session_state.contexto = contexto

# * --------------------- Manejo de historial y de respuestas ------------------ *

# ventana de contexto dinamica
MAX_HISTORY = (st.session_state.contexto * 3) + 1

async def response_mcp(pregunta:str):
    """ 
    Realiza preguntas al agente de forma asincrona \n
    permitiendole usar herramientas mas complejas como MCP 
    """
    
    # Definimos el contexto asincrono para esperar la respuesta del mcp
    async with agent.run_mcp_servers():
        
        # Pasamos la pregunta y espereamos
        response = await agent.run(pregunta,message_history=history)
        
        # Obtenemos todo el historial acumulado
        all_msgs = response.all_messages()

        # Recortamos los últimos N mensajes
        trimmed_history = all_msgs[-MAX_HISTORY:]

        # Actualizamos el historial en session_state
        st.session_state.history = trimmed_history
        
        return response.output.response , response.output.summary


# * ----------------------------- Chat ------------------------------------ *

# mostramos el historial
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Esperamos la entrada del usuario
pregunta = st.chat_input("En que te puedo ayudar?")
if pregunta:
    # Guardamos la pregunta en el historial
    st.session_state.chat.append({"role":"user","content":pregunta})
    
    # Mostramos la pregunta
    with st.chat_message("user"):
        st.markdown(pregunta)
        
    # Esperamos la respuesta del agente
    with st.spinner("Esperando la respuesta...",show_time=True,_cache=True):
        
        # Enviamos el la pregunta
        try:
            response, resumen= asyncio.run(response_mcp(pregunta))
        except Exception as e:
            st.toast(f"Error al responder: {e}")
            response = "Por favor vuelva a realizar su pregunta"
            resumen = "No se pudo responder"
        # La agregamos al historial
        st.session_state.chat.append({"role":"assistant","content":response})
        
        # Mostramos en el chat
        with st.chat_message("assistant"):
            
            combined = f"{response}\n\n**Resumen:**\n\n{resumen}"
            if disable_summary:
                combined = response
            st.markdown(combined)

#with st.sidebar:
#    st.write(st.session_state.contexto)
#    st.json(st.session_state.history)