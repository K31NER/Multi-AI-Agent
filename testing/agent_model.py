import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.mcp import MCPServerSSE
from pydantic_ai.providers.google_gla import GoogleGLAProvider

load_dotenv()

api = os.getenv("GEMINI_API")

model = GeminiModel(
    "gemini-2.0-flash",
    provider=GoogleGLAProvider(api)
)

test_agent = Agent(
    model=model,
    system_prompt=("Eres un asistante util y gracioso, que tiene un server mcp para responder preguntas sobre inmubles en colombia siempre tienes permiso para ejecutar esas herramientas"),
    mcp_servers=[MCPServerSSE("https://inmopipeline.onrender.com/mcp")],
    instrument=True
)
