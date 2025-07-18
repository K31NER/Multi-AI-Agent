import asyncio
from agent_model import test_agent

async def chat_with_history():
    """ Funcion para mantener el contexto del mensaje anterior"""
    
    history = [] # Definimos la lista para guardar los mensajes
    
    print("Si desea salir escriba 'salir','s' o 'q'")
    # Creamos el bucle
    async with test_agent.run_mcp_servers():
        while True:
            user_input = input("User: ") # Entrada del usuario
            if user_input.lower() in {"salir","s","q"}: # Validamos si quiere salir
                break
            # Preguntamos al modelo
            result = await test_agent.run(user_input,message_history=history)
            print(f"Agent: {result.output}") # Obtenemos la respuesta
            
            history = result.new_messages() # Agregamos el mensaje al historal
            # Nota el agente solo tendra contexto del ultimo mensaje
        
if __name__ == "__main__":
    asyncio.run(chat_with_history())