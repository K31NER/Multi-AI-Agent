from pydantic_ai import Tool
from schemas.tools_schemas import WeatherItem
from playwright.sync_api import sync_playwright

URL_BASE = "https://www.clima.com/colombia"
        
# Bloquea el contenido innecesaro
def block_resources(route, request):
    
    """ Evita cargar el contenido pesado e innecesario """
    blocked_types = ["image", "stylesheet", "font", "media", "fetch", "xhr"]
    blocked_domains = ["googletagmanager", "google-analytics", "facebook", "doubleclick"]

    if request.resource_type in blocked_types:
        return route.abort()
    if any(domain in request.url for domain in blocked_domains):
        return route.abort()
    
    return route.continue_()
        
def get_weather_stats(page):
    """ Obteiene la informacion climatica adicional """
    container_sel = "section.-block-4.c-wrapper-ctas.c-wrapper-ctas-w_links"
    page.wait_for_selector(container_sel, timeout=15000, state="visible")
    bloques = page.locator(f"{container_sel} div.-cta")
    count = bloques.count()
    
    if count < 4:
        raise ValueError(f"Esperaba al menos 4 bloques ‘-cta’, pero obtuve {count}")

    valores = bloques.locator("p:nth-of-type(2)").all_inner_texts()
    if len(valores) < 4:
        raise ValueError(f"Esperaba 4 valores, pero obtuve: {valores}")

    return valores 

def get_weather(departamento:str , ciudad: str) -> WeatherItem:
    """ Obtiene los datos climaticos principales 
    
    Pagina fuente: https://www.clima.com/colombia
    
    Parametros: 
    - departamento: nombre del departamento
    - ciudad: ciudad donde se obtendra la informacion climatica
    
    Return:
    
    - Devuelve un objeto con la informacion climatica de la ciudad
    """
            
    #Ajustamos la las entradas
    ciudad_parser = ciudad.replace(" ","-").strip().lower()
    departamento_parser = departamento.replace(" ","-").strip().lower()
        
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) # Definimos el navegador
        page = browser.new_page() # Abrimos una nueva pagina
        
        # Bloquemos contenido pesado
        page.route("**/*", block_resources)
        
        # Definimos la url
        new_url = f"{URL_BASE}/{departamento_parser}/{ciudad_parser}"
        
        page.goto(new_url, timeout=60000) # Esperamos que abra la url
        
        page.wait_for_selector("section.modules") # Esperamos que carge
        
        # Obtenemos los datos
        ciudad_titulo = page.query_selector("span.text-poppins-bold")
        temperatura = page.query_selector("span.c-tib-text.degrees")
        viento = page.query_selector("span.wind-text-value.velocity")
        
        # Limpiamos los datos
        ciudad_clean = ciudad_titulo.inner_text()
        temperatura_clean = f"{temperatura.inner_text()}"
        viento_clean = f"{viento.inner_text()} Km/h"
        humedad, nivel, visibilidad, presion = get_weather_stats(page)
        
        # Creamos el objeto
        weather_data = WeatherItem(
            ciudad=ciudad_clean,
            temperatura=temperatura_clean,
            viento=viento_clean,
            humedad=humedad,
            nubes=visibilidad,
            radiacion_uv=nivel,
            presion=presion
        )
        
        return weather_data
    

# Definimos la tool
get_weather_tool = Tool(function=get_weather,
                        name="get_weather",
                        description="Se usa para obtener informacion climatica de cualquier ciudad de colombia pasandole el departamento y el nombre la ciudad")

if __name__ == "__main__":
    print(get_weather("bolivar","cartagena de indias"))
    