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
                                icon=":material/network_intelligence_history:")
        
        types = ["🏠 Inmobiliario","📰 Noticias","🌤️ Meteorológico","💵 Financiero"]
        agent_type = st.selectbox("Tipo de agente:",types)
        
        temperatura = st.slider("Temperatura: ",max_value=1.0,min_value=0.0,value=0.3)
        
        top_p = st.slider("Top p: ",max_value=1.0,min_value=0.0)
        
        top_k = st.slider("Top k: ",max_value=100,min_value=1)
        
        max_token = st.number_input("Numero maximo de tokens: ",value=1000,min_value=200)
        
        st.subheader("Estetica",divider="red")
        
        disable_summary = st.toggle("Desactivar resumen")
        
        color = st.color_picker("Eliga  un color",value="#F93434")
        
        
        return contexto, agent_type, temperatura, top_p, top_k, max_token, disable_summary, color