from pydantic import BaseModel, Field

class TimeNow(BaseModel):
    """Output model que retorna la fecha y hora actual."""
    
    respuesta: str =  Field(description="Fecha y hora actual en formato  'DD/MM/YYYY hh:mm AM/PM'")
    
class NewsItem(BaseModel):
    """ Informacion sobre las noticias actuales de El tiempo"""
    
    titulo: str = Field("Titulo de la notica")
    descripcion: str = Field("Breve descripcion")
    fecha: str = Field("Hora o fecha de publicacion")
    url: str = Field("Enlace a la noticia")