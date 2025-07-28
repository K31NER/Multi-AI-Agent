from model import model_config
from pydantic_ai import Agent, Tool
from prompts.writer_agent import PROMPT
from utils.file_mange import save_report
from schemas.tools_schemas import WriterAgentItems

# Configuramos el agente
writer_agent = Agent(
    model=model_config(token=5000),
    system_prompt=PROMPT,
    output_type=WriterAgentItems,
    result_retries=3
)

async def writer_report(topic:str, resources: str = None):
    """ Genera un reporte de extension .md sobre un tema en espefico 
    
    Parametros:
    - topic: tema del que se hara el reporte
    - resources: Informacion de apoyo para realizar el reporte
    
    Return:
    - Url: enlace para descargar el reporte
    """
    
    request = f"Generame el contenido para un reporte del siguiente tema: {topic}"
    
    # Agregamos los recursos
    if resources is not None:
        request = f"{request} usa esta informacion para guiarte: {resources}"
    
    # Decimos al agente que genere un reporte
    response = await writer_agent.run(request)
    
    # Obtenemos los campos
    file_name = f"{response.output.filename}.md" or f"Repor_{topic}"
    content = response.output.content
    
    try:
        # Guardamos el archivo en el bucket de gcp
        url = save_report(file_name,content)
    except Exception as e:
        return f"Error al generar reporte: {e}"
    
    return url
    
writer_report_tool = Tool(
    function=writer_report,
    name="writer_report",
    description="Recibe un tema y opcionalmente recursos extras para realizar un reporte .md"
)