from typing import List
from urllib.parse import urljoin
from pydantic_ai import RunContext, Tool
from schemas.tools_schemas import NewsItem
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.eltiempo.com/ultimas-noticias"

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

def get_news_by_el_tiempo(limite:int = 5) -> List[NewsItem]:
    """ Realiza una busqueda de las noticas mas recientes de colombia 
    
    Pagina fuente: https://www.eltiempo.com/ultimas-noticias
    
    - Pagina de las noticias: El Tiempo
    - Limite: Limite de noticias que se muestran, el para obtener todas la noticias poner un limite de 30
    
    Return:
    - data = Dataframe
    """
    
    # Definimos una lista para guardar las noticias
    noticias_resultado = []
    
    # Definimos el contexto sincrono
    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless=True) # Definimos el navegador
        page = browser.new_page() # Abrimos una nueva pagina
        
        # Bloquemos contenido pesado
        page.route("**/*", block_resources)
        
        page.goto(BASE_URL,timeout=10000) # accedemos a la url
        
        #Esperamos el div que contiene la lista de noticas
        page.wait_for_selector("div.o-list__middle",timeout=10000)
        
        # Obtenemos todas las noticias 
        noticias = page.query_selector_all("div.item")
        
        for notica in noticias:
            try:
                # Obtemos los elementos que nos interesan
                publicacion = notica.query_selector("time.c-article__date")
                titulo_h3 = notica.query_selector("h3.c-article__title")
                enlace  = titulo_h3.query_selector("a") if titulo_h3 else None
                descripcion = notica.query_selector("p.c-article__subtitle")
                
                # Limpiamos los datos
                publi_clean = publicacion.inner_text().strip() if publicacion else None
                titulo_clean = enlace.inner_text().strip() 
                enlace_clean = urljoin("https://www.eltiempo.com",enlace.get_attribute('href'))
                descripcion_clean = descripcion.inner_text().strip()
                
                # Agregamos a la lista
                item = NewsItem(
                    titulo=titulo_clean,
                    descripcion=descripcion_clean,
                    fecha=publi_clean,
                    url=enlace_clean
                )
                noticias_resultado.append(item)
                """ 
                print(f"Hora de publicacion: {publi_clean}")
                print(f"Titulo: {titulo_clean}")
                print(f"Descripcion: {descripcion_clean}")
                print(f"Enlace: {enlace_clean} \n")
                """
            except Exception as e:
                print(f"[Error] saltando notica por excepcion: {e}")
                continue
        browser.close()
            
    return noticias_resultado[:limite]

# Definimos la tool
get_news_tool = Tool(
                    function=get_news_by_el_tiempo,
                    name="get_news_by_el_tiempo",
                    description="Devuelve las noticas mas recientes de colombia")

if __name__ == "__main__":
    pass