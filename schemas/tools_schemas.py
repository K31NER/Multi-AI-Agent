from typing import List
from pydantic import BaseModel, Field

class ResponseBase(BaseModel):
    response: str = Field(description="Respuesta en base a lo solicitado")
class TimeNow(BaseModel):
    """Output model que retorna la fecha y hora actual."""
    
    respuesta: str =  Field(description="Fecha y hora actual en formato  'DD/MM/YYYY hh:mm AM/PM'")
    
class NewsItem(BaseModel):
    """ Informacion sobre las noticias actuales de El tiempo"""
    
    titulo: str = Field("Titulo de la notica")
    descripcion: str = Field("Breve descripcion")
    fecha: str = Field("Hora o fecha de publicacion")
    url: str = Field("Enlace a la noticia")
    
class WeatherItem(BaseModel):
    ciudad: str = Field("Ciudad donde se presenta el clima")
    temperatura: str = Field("Grados de temperatura")
    viento: str = Field("Nivel del viento")
    humedad: str = Field("Nivel de humedad")
    nubes: str = Field("Porcenaje de nubes")
    radiacion_uv: str = Field("Nivel de radiacion solar")
    presion: str = Field("Nivel de presion")
    humedad: str = Field("Porcentaje de humedad")
    
class TrmItem(BaseModel):
    titulo: str = Field("Descripcion del tipo de conversion")
    conversion: str = Field("Monda del pais origen vs pais a comparar")
    moneda_origen: str = Field("Moneda de origen")
    moneda_conversion: str = Field("Moneda del pais a convertir")

class WriterAgentItems(BaseModel):
    filename: str = Field("Nombre del archivo")
    content: str = Field("Contenido del reporte en formato markdown")