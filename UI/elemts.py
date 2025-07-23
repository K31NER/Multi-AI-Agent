import streamlit as st 

def add_title(titulo:str,icon:str,color:str = "#F93434"):
    st.markdown(
    f"""
    <h1 style="
        text-align: center;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 3rem;
        color: {color};
        margin-bottom: 0.5rem;
    ">
        {icon} {titulo}
    </h1>
    """,
    unsafe_allow_html=True,
)
    
def add_sidebar():
    # Creamos la barra lateral para configuracion del agente
    with st.sidebar:
        st.markdown("# Configuraciones:")
        
        st.subheader("Agente",divider="red")
        
        # Contexto maximo que soporta el agente
        contexto = st.number_input("Ventana de contexto",step=1, value=6,
                                min_value=1,max_value=20,
                                help="Indica el numero de mensajes que puede recordar el agente",
                                icon=":material/network_intelligence_history:",
                                key="contexto_ventana"
                                )
        
        types = ["🏠 Inmobiliario","📰 Noticias","🌤️ Meteorológico","💵 Financiero"]
        agent_type = st.selectbox("Tipo de agente:",types,key="agent_type")
        
        list_models= [
        'gemini-2.0-flash', 'gemini-2.0-flash-lite-preview-02-05',
        'gemini-2.0-pro-exp-02-05', 'gemini-2.5-flash-preview-05-20',
        'gemini-2.5-flash', 'gemini-2.5-flash-lite-preview-06-17',
        'gemini-2.5-pro-exp-03-25', 'gemini-2.5-pro-preview-05-06'] 
        
        model_version = st.selectbox("Seleccione la version del modelo",list_models,key="model_version")
        
        temperatura = st.slider("Temperatura: ",max_value=1.0,min_value=0.0,value=0.3,key="temperatura")
        
        top_p = st.slider("Top p: ",max_value=1.0,min_value=0.0,key="top_p")
        
        max_token = st.number_input("Numero maximo de tokens: ",value=1000,min_value=200,key="max_tokens")
        
        multi_tool = st.toggle("Multi Tools",value=False,help="Permite al modelo usar mas de una herramienta a la vez",key="multi_tool")
        
        st.subheader("Estetica",divider="red")
        
        disable_summary = st.toggle("Desactivar resumen",key="disable_summary")
        
        color = st.color_picker("Eliga  un color",value="#F93434",key="color_picker")
        
        return contexto, agent_type,model_version, temperatura, top_p, max_token,multi_tool, disable_summary, color