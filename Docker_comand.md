# Comandos de ejecucion docker 🐋
## Creamos la imagen

```bash
docker build . -t ai_agent
```

## Creacion del contedor
```bash
docker run --name ai_agent_container -p 8501:8501 ai_container
```

## Detener contendor

```bash
docker stop ai_agent_container
```

## Volver a inicar (Una vez creado el contenedor ya podemos usar esta siempre)
```bash
docker start ai_agent_container
```

## Verificar estado
```bash
docker ps -a
```