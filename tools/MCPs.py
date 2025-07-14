from pydantic_ai.mcp import MCPServerSSE

# Definios los servicos mcp que usaremos
inmopipeline_mcp = MCPServerSSE(
    url="https://inmopipeline.onrender.com/mcp",
)