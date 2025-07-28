import sys
import asyncio
import logging
import nest_asyncio
import streamlit as st
from pydantic_ai import Agent
from model import model_config
from logger_config import init_logger
from UI.elemts import add_title,add_sidebar
from agents.list_agents import create_agents
from utils.file_mange import save_in_bucket,drop_file,URLTYPE_FILES

st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded")


# * -------------------- Configuracion inicial ---------------------------------
# Inicalizamos el logger
init_logger()

# Creamos el objeto loggin para registrar
logger = logging.getLogger(__name__)

# En Windows, asegurar que usamos ProactorEventLoop
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
# Parche para permitir llamadas anidadas a asyncio.run()
nest_asyncio.apply()

# Llamas a la función al inicio
contexto, agent_type,model_version, temperatura, top_p, max_token, multi_tool,disable_summary, color = add_sidebar()

# Definimos el titulo
add_title(titulo="AI Agent",icon="🤖",color=color)

# Capturar configuración actual
current_config = dict(
    model_version=model_version,
    p=top_p,
    temp=temperatura,
    token=max_token,
    multi_tool=multi_tool
)

# *---------------------- Variables de estado ---------------------------------*
# Iniciaizamos el id en 1
if "file_id" not in st.session_state:
    st.session_state.file_id = 1
    
# Definimimso el estado para guardar el historial
if "chat" not in st.session_state:
    st.session_state.chat = []
    
# Definimos el historial en la session 
if "history" not in st.session_state:
    st.session_state.history = []
    
# Instanciamos el historial
history = st.session_state.history

# Definimos el tipo de agente en el estado
if "type_agent" not in st.session_state or st.session_state.type_agent != agent_type:
    # Limpiamos el historia para e cambio de agente
    st.session_state.history.clear()
    
    # Redefinimos el agente con el que esta seleccionado
    st.session_state.type_agent = agent_type
    
# Definimos el contexto en el estado de la app
if "contexto" not in st.session_state or st.session_state.contexto != contexto:
    st.session_state.contexto = contexto
    
# Creamos la session general 
if "agentes" not in st.session_state:
    st.session_state.config = None
    st.session_state.model_obj = None
    st.session_state.agentes = {}

# Detecta si algo cambió
if st.session_state.config != current_config:
    st.session_state.config = current_config
    st.session_state.model_obj = model_config(**current_config)
    st.session_state.agentes = create_agents(st.session_state.model_obj)
    
    st.session_state.history.clear()

# Obtenemos el agente actual
agent = st.session_state.agentes.get(st.session_state.type_agent)
if agent is None:
    st.error(f"Agente '{agent_type}' no disponible. Recarga para regenerar.")
    st.stop()
    
# * --------------------- Manejo de historial y de respuestas ------------------ *

# ventana de contexto dinamica
MAX_HISTORY = (st.session_state.contexto * 3) + 1

async def response_mcp(pregunta:str,agent:Agent):
    """ 
    Realiza preguntas al agente de forma asincrona \n
    permitiendole usar herramientas mas complejas como MCP 
    
    Parametros:
    - pregunta: Pregunta del usuario al agente
    - agent: Tipo de agente al que se le realizara la pregunta
    """
    
    # Definimos el contexto asincrono para esperar la respuesta del mcp
    async with agent.run_mcp_servers():
        
        # Pasamos la pregunta y espereamos
        response = await agent.run(pregunta,message_history=history)
        
        # Guardamos el registro
        logger.info(f"Total tokens: {response.usage().total_tokens} | Model {model_version}")
        
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
pregunta = st.chat_input("En que te puedo ayudar?",
                        accept_file=True, file_type=URLTYPE_FILES)
if pregunta:
    
    # Dividimos el mensaje
    pregunta_text = pregunta.text or "" # Obtenemos la pregunta
    file = pregunta.files[0] if pregunta.files else None # Obtenemos el archivo
    
    # Definimos la pregunta final
    pregunta_final = pregunta_text
    
    # Validamos el archivo
    if file is not None:
        # Guardamos el archivo
        file_id = st.session_state.file_id # Sacamos el id
        file_extension = file.name.split(".")[-1] # Obtemos la extension
        file_name = f"{file_id}.{file_extension}" # Definimos el nombre
        url = save_in_bucket(file_name,file) # Generamos la url
        
        # Sumamos uno al contador
        st.session_state.file_id += 1
        
        pregunta_final = f"{pregunta_text} - Link: {url} - Extension: {file_extension}"
    
    # Guardamos la pregunta en el historial
    st.session_state.chat.append({"role":"user","content":pregunta_text})
    
    # Mostramos la pregunta
    with st.chat_message("user"):
        st.markdown(pregunta_text)
        
    # Esperamos la respuesta del agente
    with st.spinner("Esperando la respuesta...",show_time=True):
        
        # Enviamos el la pregunta
        try:
            response, resumen= asyncio.run(response_mcp(pregunta_final, agent))
        except Exception as e:
            st.toast(f"Error al responder: {e}")
            response = "Por favor vuelva a realizar su pregunta"
            resumen = "No se pudo responder"
            logger.exception(f"Error: {e}")
        finally:
            if file is not None:
                drop_file(file_name) # Eliminamos el archivo luego de que el agente lo use
            
        # La agregamos al historial
        st.session_state.chat.append({"role":"assistant","content":response})
        
        # Mostramos en el chat
        with st.chat_message("assistant"):
            
            combined = f"{response}\n\n**Resumen:**\n\n{resumen}"
            if disable_summary:
                combined = response
            st.markdown(combined)

#with st.sidebar:
#    st.json(st.session_state.history)
#   st.write(agent_type)
#    st.json(st.session_state.agentes)