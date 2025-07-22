from pydantic_ai import Tool
from schemas.tools_schemas import TrmItem
from playwright.sync_api import sync_playwright

URL = "https://wise.com/es/currency-converter"

def get_trm(pais_origen:str, pais_conversion:str, monto: int) -> TrmItem:
    
    """ Obtiene el cambio de moneda entre 2 paises usando los códigos de moneda ISO 4217  
    
    Pagina fuente: https://wise.com
    
    Parametros:
    - pais_origen: pais donde se va a evaluer la moneda
    - pais_conversion: pais donde se realizara la conversion
    - monto: cantidad de dinero a convertir
    """
    
    origen = pais_origen.lower().strip()
    conversion = pais_conversion.lower().strip()
    
    if origen == conversion:
        return {"Message": "No se puede realizar conversion con la misma moneda"}
    
    try:
        with sync_playwright() as p:
            # Configuramos el navegador
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Buscamos la url
            new_url = f"{URL}/{origen}-to-{conversion}-rate?amount={monto}"
            page.goto(new_url,timeout=10000)
            page.wait_for_selector("h1.mw-display-3.m-b-5")
            
            # Obtenemos la informacion
            titulo = page.query_selector("h1.m-b-5.text-xs-center.mw-display-2")
            cambio = page.locator("div._midMarketRateAmount_1sz23_139 span")
            cambio_info = cambio.nth(1) # Obtenemos e 2 span indice 1
            moneda_origen = page.locator("#source-input")
            otra_moneda = page.locator("#target-input")
            
            # Limpiamos los datos
            titulo_clean = titulo.inner_text()
            cambio_clean = cambio_info.inner_html() 
            moneda_origen_clean = moneda_origen.input_value()
            otra_moneda_clean = otra_moneda.input_value()
            
            #Agregamos el objeto
            new_conversion = TrmItem(
                titulo=titulo_clean,
                conversion=cambio_clean,
                moneda_origen= moneda_origen_clean,
                moneda_conversion=otra_moneda_clean
                
            )
    except Exception as e:
        return {
            "Message": "Error al obtener informacion. posible mente no se tiene informacion de la moneda",
            "details": f"{e}"}
    
    return new_conversion
    
# Definimos la tool
get_trm_tool = Tool(function=get_trm,
                    name="get_trms",
                    description="Se usa para realizar conversion entre mondeas de 2 paises, los paises se deben pasar en formato ISO 4217 ")

if __name__ == "__main__":
    print(get_trm(pais_origen="cop",pais_conversion="mxn",monto=4500))