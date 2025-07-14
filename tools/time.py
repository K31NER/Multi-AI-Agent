from datetime import datetime
from pydantic_ai import RunContext, Tool
from schemas.tools_schemas import TimeNow

async def get_time_now(ctx: RunContext[None]) -> TimeNow:
    """ Obtiene la hora actual en UTC en formato  'DD/MM/YYYY hh:mm AM/PM'
    
    Usala cuando el usuario pregunta algo relacionado con fechas o horas actuales
    """

    now = datetime.now()
    time_str = now.strftime("%d/%m/%Y %I:%M %p")
    return TimeNow(respuesta=f"La fecha y hora actual es: {time_str}")

# Aquí defines el Tool ligado a la función
get_time_now_tool = Tool(
    function=get_time_now,
    name="get_time_now",
    description="Devuelve la fecha y hora actual en formato 'DD/MM/YYYY hh:mm AM/PM'."
)