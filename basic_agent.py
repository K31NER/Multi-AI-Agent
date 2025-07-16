import os
import asyncio
from typing import Union
import logfire
from pydantic_ai import Agent
from dotenv import load_dotenv
from tools.MCPs import inmopipeline_mcp
from tools.time import get_time_now_tool
from tools.news import get_news_tool
from schemas.agent_schema import ResponseModel
from prompts.basic import SIMPLE_SYSTEM_PROMPT
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from pydantic_ai.models.gemini import GeminiModel, GeminiModelSettings

#____________________ configuracion general ________________________________
# cargamos las variables de entorno
load_dotenv()

# configuramos logfire
logfire.configure()
logfire.instrument_pydantic_ai()

# Obtenemos nuestra API KEY
API_KEY = os.getenv("GEMINI_API")

# _______________________________Definimos el modelo____________________________
model = GeminiModel(
    "gemini-2.0-flash", # Definimos el modelo
    provider=GoogleGLAProvider(API_KEY), # Pasamos la api key
    settings=GeminiModelSettings(      # configuramos el modelo
        temperature=0.3,
        top_p=0.0)
)

# ____________________________ Creamos el agente ______________________________
agent = Agent(
    model=model,
    output_type=ResponseModel, 
    system_prompt=(SIMPLE_SYSTEM_PROMPT),
    tools=[get_time_now_tool,get_news_tool],
    mcp_servers=[inmopipeline_mcp],
    instrument=True,
    retries=2,
)

# _______________________ Funciones de respuesta _____________________
    
async def response_agent(pregunta:str):
    
    response = await agent.run(pregunta)
    
    return response.output.response

async def response_mcp(pregunta:str):
    """ 
    Realiza preguntas al agente de forma asincrona \n
    permitiendole usar herramientas mas complejas como MCP 
    """
    
    # Definimos el contexto asincrono para esperar la respuesta del mcp
    async with agent.run_mcp_servers():
        
        # Pasamos la pregunta y espereamos
        response = await agent.run(pregunta)

        # Volvemos la respuesta en format json
        json_response = response.output.model_dump_json(indent=2)

        # Mostramos la respuesta
        print(json_response)
        
        return json_response

if __name__ == "__main__":
    asyncio.run(response_mcp("Que noticas hay el dia de hoy"))
    