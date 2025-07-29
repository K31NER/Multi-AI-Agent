from pydantic_ai import Tool
from schemas.tools_schemas import BitcointItem
from playwright.sync_api import sync_playwright, TimeoutError

# Definimos al url de inicio
URL_BASE = "https://www.binance.com/es/price/bitcoin/"

def get_bitcoint_value(country: str = "COP") -> BitcointItem:
    """ Obtiene el valor y la descripcion del estado del bitcoint en un pais espefico
    
    Pagina de origen: www.binance.com 
    
    Parametros:
    
    - country: Nombre del pais en formato ISO 4217 donde se va a realizar la conversion 
    
    Return:
    
    - BitcointItem: 
        - Descripcion: Breve descripcion del estado del bitcoint en ese pais
        - Conversion: Tasa de conversion de moneda de ese pais a bitcoint
    """
    # Formatemos el pais para evitar errores
    country_parser = country.upper().strip()
    value_country = f"{URL_BASE}{country_parser}" # Creamos la nueva url
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True) # Definimos el navegador
            page = browser.new_page() # Abrimos una pagina
            
            page.goto(value_country,timeout=30000) # Cargamos la url
            
            # Esperamos por el contenedor principal
            page.wait_for_selector("div.banner-bg-mask")
            
            # Obtememos los datos
            descripcion = page.query_selector("p.t-body1.mt-4.mb-6")
            conversion = page.query_selector("div.text-SecondaryText.t-body2.text-center")
            
            # Limpiamos los datos
            descripcion_clean = descripcion.inner_text()
            conversion_clean = conversion.inner_text()
            
            # Los definimos
            bitcoint_info = BitcointItem(
                conversion=conversion_clean,
                description=descripcion_clean
            )
    except TimeoutError as t:
        return [f"Error al cargar pagina: {t}"]
    except Exception as e:
        return [f"Error al obtener datos: {e}"]
    
    return bitcoint_info

get_bitcoint_tool = Tool(function=get_bitcoint_value,
                        name="get_bitcoint_value",
                        description="Obtiene la informacion actual del bitcoint de x pais(en formaro ISO 4217)")

if __name__ == "__main__":
    print(get_bitcoint_value("colombia"))