from model import model_config
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from agents.list_agents import agent_inmobiliario

app = FastAPI()

agent = agent_inmobiliario(model_config())

@app.get("/question/{question}")
async def agent_run(question:str):
    async with agent.run_mcp_servers():
        try:
            response = await agent.run(question)
        except Exception as e:
            raise HTTPException(detail=f"Error al generar respuesta: {e}",status_code=404)
        
    return JSONResponse(content={
        "response": f"{response.output.response}",
        "summary": f"{response.output.summary}",
        "cost": f"Total tokens: {response.usage().total_tokens}"
    },status_code=200)
