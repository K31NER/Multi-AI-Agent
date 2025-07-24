import typer
import subprocess
import multiprocessing

app = typer.Typer()

@app.command("api")
def run_fastapi():
    """ Ejecuta el servidor de fastapi """
    message = typer.style("⚡ Iniciando servidor Fastapi",
                        fg=typer.colors.BRIGHT_GREEN,bold=True)
    
    typer.echo(message,color=True)
    subprocess.run(["uvicorn","API.main:app","--host","0.0.0.0","--port","8000","--reload"])

@app.command("ui")
def run_streamlit():
    """ Ejecutando interfaz streamlit """
    
    message = typer.style("🤖 Iniciando interfaz de streamlit",
                        fg=typer.colors.BRIGHT_RED,bold=True)
    
    typer.echo(message,color=True)
    subprocess.run(["streamlit","run","app.py","--server.address","0.0.0.0","--server.port","8501"])
    
@app.command("all")
def run_project():
    """ Ejecuta todo el proyecto"""
    message = typer.style("⌛ Iniciando proyecto",
                        fg=typer.colors.BRIGHT_YELLOW,bold=True)
    
    typer.echo(message,color=True)
    p1 = multiprocessing.Process(target=run_fastapi)
    p2 = multiprocessing.Process(target=run_streamlit)
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    
if __name__ == "__main__":
    app()