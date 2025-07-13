from typing import List
from pydantic import BaseModel,Field

class ResponseModel(BaseModel):
    """ Respuesta base del modelo """
    response: str
    dato_curioso: str = Field("Debes dar siempre un dato curioso en base a la pregunta del usuario")

class ManyResponse(BaseModel):
    """ Modelo para que el modelo procese una lista de preguntas"""
    respuesta: List[ResponseModel] = Field("Lista de mensajes donde cada objeto es un mensaje")
    
class TimeNow(BaseModel):
    """Output model que retorna la fecha y hora actual."""
    time: str =  Field(description="Fecha y hora actual en formato  'DD/MM/YYYY hh:mm AM/PM'")