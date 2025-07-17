# Definimos la imagen base
FROM python:3.11-slim

# Evitamos preguntas en instalaciones
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Bogota

# Creamos el directorio de trabajo
WORKDIR /ai_agent

# Instalamos dependencias del sistema + zona horaria
RUN apt-get update && apt-get install -y \
    tzdata \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libxss1 \
    libasound2 \
    libgbm1 \
    libxshmfence1 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    fonts-liberation \
    xdg-utils \
    ca-certificates \
    libappindicator3-1 \
    wget \
    --no-install-recommends && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copiamos el archivo de dependencias
COPY requirements.txt .

# Instalamos las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalamos Chromium para Playwright
RUN python -m playwright install chromium

# Copiamos el resto del proyecto
COPY . .

# Exponemos el puerto de Streamlit
EXPOSE 8501

# Comando por defecto para ejecutar la app
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
