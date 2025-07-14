from typing import List
from pydantic import BaseModel,Field

class ResponseModel(BaseModel):
    """
    Modelo de salida para el agente: estructura la respuesta clara, profesional y validada.
    """

    response: str = Field(
        ...,
        title="Mensaje principal",
        description=(
            "Respuesta final del agente, en un solo párrafo. "
            "Debe ser un texto limpio, directo y profesional, "
            "sin incluir metadatos o referencias técnicas a herramientas. "
            "Si la consulta incluye inmuebles o noticias, incluye directamente los enlaces relevantes."
        ),
        examples=[
            "Aquí tienes la información solicitada sobre la propiedad en Bogotá: https://inmuebles.co/1234",
            "Las noticias más recientes en Colombia:\n- Titular 1 (enlace)\n- Titular 2 (enlace)"
        ],
    )
    summary: str = Field(
        "",
        title="Resumen breve",
        description=(
            "Un resumen conciso (1–2 frases) que resalta los puntos clave de la respuesta. "
            "Está destinado a reforzar la claridad del mensaje principal."
        ),
        examples=[
            "Resumen: 3 propiedades encontradas, una en Bogotá y dos en Medellín.",
            "Resumen: Hoy hay 5 noticias destacadas en Colombia."
        ],
    )

class ManyResponse(BaseModel):
    """ Modelo para que el modelo procese una lista de preguntas"""
    
    respuesta: List[ResponseModel] = Field("Lista de mensajes donde cada objeto es un mensaje")
    
