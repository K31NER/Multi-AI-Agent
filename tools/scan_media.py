from typing import Literal
from model import model_config
from schemas.tools_schemas import ResponseBase
from pydantic_ai import Agent, ImageUrl,VideoUrl,DocumentUrl,Tool

# Definimos un pequeño prompt para este agente
prompt = """
Eres un agente encargado de analizar URLs y responder en base a las preguntas, 
puedes recibir URLs de imagen, video o documento; debes analizarlas y responder con precisión.
"""

# definimos el agente
media_agent = Agent(
        model=model_config(),
        system_prompt=prompt,
        output_type=ResponseBase
)

# Mapeamos el tipo de dato
type_map = {
    "imagen": ImageUrl,
    "video": VideoUrl,
    "documento": DocumentUrl
}

async def read_media(question: str ,
                    media_url:str,
                    type_file:Literal["imagen","video","documento"]) -> str:
    
    """
    Función para analizar archivos multimedia: imágenes, videos o documentos.

    Parámetros:
    - question: Pregunta a realizar sobre el archivo subido.
    - media_url: Dirección pública del archivo a analizar.
    - type_file: Tipo de archivo: "imagen", "video" o "documento".

    Retorna:
    - La respuesta generada por el agente en base al contenido del archivo.

    Nota:
    El tipo de archivo debe ser exactamente "imagen", "video" o "documento".
    """
    
    # Obtenemos el tipo de documento
    media_type = type_map.get(type_file)
    
    if not media_type:
        raise ValueError(f"Tipo de archivo no soportado: {type_file}")
    
    response = await media_agent.run([question,media_type(media_url)])
    
    return response.output.response
    

read_media_tool = Tool(
                    function=read_media,
                    name="read_media",
                    description="Tool especializada en análisis multimodal (imagen, video, documento) desde URLs públicas.",
                    max_retries=3)