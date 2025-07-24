import redis,json,logging
from logger_config import init_logger
from redis.exceptions import ConnectionError
from pydantic_ai.messages import ModelMessagesTypeAdapter
from pydantic_core import to_jsonable_python
from pydantic import TypeAdapter

init_logger()
logger = logging.getLogger(__name__)

map_keys = {
        "🏠 Inmobiliario":  "inmobiliario",
        "📰 Noticias": "noticias",
        "🌤️ Meteorológico": "clima",
        "💵 Financiero": "finanzas"
    }

r = redis.Redis(host="localhost",
                        port=6379,db=0,
                        encoding="utf-8",
                        decode_responses=True)

def update_history(agent:str, hist: dict ,context:int , expire: int = 1):
    """ Actualiza o crea el historial de cada agente y limita el maximo de contexto
    
    Parametros:
    - agent: Nombre del agente
    - hist: Historial del agente
    - context: Numero de preguntas que recuerda.
    - expire: Tiempo de expiracion de la session.
    
    """
    
    # Definimos la key
    key = f"history:{agent}"
    
    # Definimos el tiempo de expiracion
    expire_time = expire * 24*60*60 # 1 Dia por defecto
    
    # Serializamo la entrada
    hist_serializer = hist.model_dump_json()
    
    try:
        # Creamos el pipeline
        pipe = r.pipeline()
        
        # Creamos la session del agente con su respectivo historial
        pipe.lpush(key,hist_serializer)
        
        # Limitamos el tamaño
        pipe.ltrim(key,0,context-1)
        
        # Definimos la expiracion
        pipe.expire(key,expire_time)
        
        # Ejecutamos el pipeline
        pipe.execute()
    except ConnectionError as e:
        logger.error(f"Error al guardar historial: {e}")

def get_history(agent: str ,context: int) -> list:
    """ Obtiene el historial del agente
    
    Parametros:
    - agent: Nombre del agente
    - context: Numero de preguntas que recuerda.
    
    Return:
    
    - hist: Lista con el historial de chat del agente
    """
    
    # Definimos la key
    key = f"history:{agent}"
    
    try:
        # Obtenemos el historial del agente actual
        elementos = r.lrange(key,0, context - 1)
    except ConnectionError as e:
        logger.error(f"Error al obtener datos: {e}")
        return []
    
    # Volvemos una lista
    hist = [json.loads(e) for e in elementos]
    hist.reverse() # Invertimos para tener el orden FIFO
    
    return hist

def clean_session(borrar: bool = False):
    """
    Limpia claves de historial en Redis.
    - borrar=True: elimina las claves matching 'history:*'
    - borrar=False: muestra cuántas claves se podrían borrar sin eliminar
    """
    keys = list(r.scan_iter('history:*'))
    count = len(keys)

    if not borrar:
        logger.info(f"[Redis] {count} sesiones listas para eliminar.")
        return count

    if keys:
        pipe = r.pipeline()
        for key in keys:
            pipe.delete(key)
        pipe.execute()
        logger.info(f"[Redis] Se eliminaron {count} sesiones.")
    else:
        logger.info("[Redis] No se encontraron sesiones para eliminar.")
    return count
