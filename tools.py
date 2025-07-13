from models import TimeNow
from datetime import datetime
from pydantic_ai import RunContext


async def get_time_now(ctx: RunContext[None]) -> TimeNow:
    """ Obtiene la hora actual en UTC en formato  'DD/MM/YYYY hh:mm AM/PM'
    
    Usala cuando el usuario pregunta algo relacionado con fechas o horas actuales
    """

    now = datetime.now()
    time_str = now.strftime("%d/%m/%Y %I:%M %p")
    return TimeNow(time=time_str)

