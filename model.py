import os
from typing import Literal
from pydantic_ai import Agent
from dotenv import load_dotenv
from pydantic_ai.profiles.google import google_model_profile
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from pydantic_ai.models.gemini import GeminiModel,GeminiModelSettings,ThinkingConfig

load_dotenv()

API_KEY =os.getenv("GEMINI_API")


def model_config(
    model_version: Literal[
        'gemini-1.5-flash','gemini-1.5-pro',
        'gemini-2.0-flash','gemini-2.0-flash-lite-preview-02-05',
        'gemini-2.0-pro-exp-02-05', 'gemini-2.5-flash-preview-05-20',
        'gemini-2.5-flash', 'gemini-2.5-flash-lite-preview-06-17',
        'gemini-2.5-pro-exp-03-25', 'gemini-2.5-pro-preview-05-06'
    ] = 'gemini-2.0-flash',
    token: int = 1000, temp: float = 0.3, p: float = 0.2, multi_tool: bool = False
    ) -> GeminiModel:
    
    """ Definicion y configuracion personalizada del modelo de gemini 
    
    Parametros:
    
    - model_version: Version del modelo de gemini.
    - token: Maximo de token a generar.
    - temp: Nievel de creatividad de 0 a 2 a mas alta mas creativo.
    - thinking: capacidad del modelo para pensar (Mas costoso).
    - p: Top_p nucleo de probabilidad mientras mas alto mas creativo.
    - multi_tool: Capacidad del modelo para llamar a mas de una herramienta.
    
    Return:
    
    - Model: Geminimodel
    """
    
    # Definimos las configuraciones del modelo
    config = GeminiModelSettings(
            top_p= p ,
            max_tokens= token,
            temperature= temp,
            parallel_tool_calls= multi_tool
        )
    
    # Definimos el modelo
    model = GeminiModel(
        model_name= model_version,
        provider=GoogleGLAProvider(api_key=API_KEY),
        profile=google_model_profile,
        settings= config
    )
    
    # Devolvemos el modelo
    return model

if __name__ == "__main__":
    test_agent = Agent(
        model=model_config(),
        system_prompt=("Respondes de forma amistosa y con emojis"),
        instrument=True
    )
        
    response = test_agent.run_sync("Hola como estas?")

    print(response.output)
    print(response.usage().total_tokens)

