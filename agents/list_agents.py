import logfire
from pydantic_ai import Agent
from tools.news import get_news_tool
from tools.MCPs import inmopipeline_mcp
from tools.time import get_time_now_tool
from tools.conversion import get_trm_tool
from tools.weather import get_weather_tool
from tools.writer import writer_report_tool
from tools.scan_media import read_media_tool
from schemas.agent_schema import ResponseModel
from prompts.clima import CLIMAS_SYSTEM_PROMPT
from prompts.finanzas import FINANZAS_SYSTEM_PROMPT
from prompts.noticias import NOTICIAS_SYSTEM_PROMPT
from prompts.inmobiliario import INMOBILIARIO_SYSTEM_PROMPT

# configuramos logfire
logfire.configure()
logfire.instrument_pydantic_ai()

# *-------------------------- Definimos los agentes -------------------------------- *
def agent_inmobiliario(model) -> Agent:
    return Agent(
        model=model,
        output_type=ResponseModel,
        system_prompt= INMOBILIARIO_SYSTEM_PROMPT,
        tools=[read_media_tool,writer_report_tool],
        mcp_servers=[inmopipeline_mcp],
        retries=2,
        instrument=True
    )

def agent_noticias(model) -> Agent:
    return Agent(
        model=model,
        output_type=ResponseModel,
        system_prompt=NOTICIAS_SYSTEM_PROMPT,
        tools=[get_time_now_tool,get_news_tool,read_media_tool,writer_report_tool],
        retries=True,
        instrument=True
    )

def agent_meteorologico(model) -> Agent:
    return Agent(
        model=model,
        output_type=ResponseModel,
        system_prompt=CLIMAS_SYSTEM_PROMPT,
        retries=2,
        tools=[get_weather_tool,get_time_now_tool,read_media_tool,writer_report_tool],
        instrument=True
    )

def agent_financiero(model) -> Agent:
    return Agent(
        model=model,
        output_type=ResponseModel,
        system_prompt=FINANZAS_SYSTEM_PROMPT,
        tools=[get_trm_tool,read_media_tool,writer_report_tool],
        retries=2,
        instrument=True
    )

# Creacion de los agentes
def create_agents(model):
    return {
        "🏠 Inmobiliario":  agent_inmobiliario(model),
        "📰 Noticias": agent_noticias(model),
        "🌤️ Meteorológico": agent_meteorologico(model),
        "💵 Financiero": agent_financiero(model)
    }