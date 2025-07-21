import logfire
from pydantic_ai import Agent
from basic_agent import model
from tools.news import get_news_tool
from tools.MCPs import inmopipeline_mcp
from tools.time import get_time_now_tool
from tools.weather import get_weather_tool
from schemas.agent_schema import ResponseModel
from prompts.clima import CLIMAS_SYSTEM_PROMPT
from prompts.finanzas import FINANZAS_SYSTEM_PROMPT
from prompts.noticias import NOTICIAS_SYSTEM_PROMPT
from prompts.inmobiliario import INMOBILIARIO_SYSTEM_PROMPT


# configuramos logfire
logfire.configure()
logfire.instrument_pydantic_ai()


# *-------------------------- Definimos los agentes -------------------------------- *
inmobiliario = Agent(
    model=model,
    output_type=ResponseModel,
    system_prompt= INMOBILIARIO_SYSTEM_PROMPT,
    mcp_servers=[inmopipeline_mcp],
    retries=2,
    instrument=True
)

noticias = Agent(
    model=model,
    output_type=ResponseModel,
    system_prompt=NOTICIAS_SYSTEM_PROMPT,
    tools=[get_time_now_tool,get_news_tool],
    retries=True,
    instrument=True
)

meteorologico = Agent(
    model=model,
    output_type=ResponseModel,
    system_prompt=CLIMAS_SYSTEM_PROMPT,
    retries=2,
    tools=[get_weather_tool,get_time_now_tool],
    instrument=True
)

financiero = Agent(
    model=model,
    output_type=ResponseModel,
    system_prompt=FINANZAS_SYSTEM_PROMPT,
    retries=2,
    instrument=True
)

# Mapeo para obtener el agente 
agentes_map = {
    "Inmobiliario": inmobiliario,
    "Noticias" : noticias,
    "Meteorológico": meteorologico,
    "Financiero" : financiero
}