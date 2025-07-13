import os
import asyncio
import logfire
from pydantic_ai import Agent
from tools import get_time_now
from dotenv import load_dotenv
from models import ManyResponse
from prompt import SYSTEM_PROMPT
from MCPs import inmopipeline_mcp
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
        max_tokens=500,
        temperature=0.0,
        top_p=0.0)
)

# ____________________________ Creamos el agente ______________________________
agent = Agent(
    model=model,
    output_type=ManyResponse,
    system_prompt=(SYSTEM_PROMPT),
    tools=[get_time_now],
    mcp_servers=[inmopipeline_mcp],
    instrument=True,
    retries=2,
)

# _______________________ Funciones de respuesta _____________________
    
async def response_mcp():
    """ 
    Realiza preguntas al agente de forma asincrona \n
    permitiendole usar herramientas mas complejas como MCP 
    """
    
    # Definimos el contexto asincrono para esperar la respuesta del mcp
    async with agent.run_mcp_servers():
        
        # Pasamos la pregunta y espereamos
        response = await agent.run([
            "Cuantas casas en cartegena que tengan 2 habitaciones?"
        ])

        # Volvemos la respuesta en format json
        json_response = response.output.model_dump_json(indent=2)

        # Mostramos la respuesta
        print(json_response)

if __name__ == "__main__":
    asyncio.run(response_mcp())
    