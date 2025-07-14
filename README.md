# 🤖 Basic AI Agent - Agente de IA Especializado

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Pydantic AI](https://img.shields.io/badge/Pydantic%20AI-0.4.2-FF6B6B?style=flat&logo=pydantic&logoColor=white)](https://ai.pydantic.dev)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Pro-4285F4?style=flat&logo=google&logoColor=white)](https://ai.google.dev)
[![MCP](https://img.shields.io/badge/Model%20Context%20Protocol-1.11.0-00D4AA?style=flat)](https://modelcontextprotocol.io)
[![Streamlit](https://img.shields.io/badge/Streamlit-Planned-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Playwright](https://img.shields.io/badge/Playwright-Web%20Scraping-2EAD33?style=flat&logo=playwright&logoColor=white)](https://playwright.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Logfire](https://img.shields.io/badge/Logfire-Observability-FF6B35?style=flat)](https://pydantic.dev/logfire)

## 📋 Descripción del Proyecto

**Basic AI Agent** es un proyecto de desarrollo de agentes de inteligencia artificial especializados utilizando **Pydantic AI**. El objetivo principal es crear un ecosistema modular de agentes que puedan especializarse en diferentes dominios de datos regionales y funcionalidades específicas.

### 🎯 Objetivos del Proyecto

- **Agente General**: Desarrollo de un agente base con capacidades fundamentales
- **Especialización Modular**: Creación de agentes especializados por dominio
- **Banco de Prompts**: Sistema de gestión de prompts especializados
- **Banco de Tools**: Biblioteca reutilizable de herramientas
- **Interfaz Streamlit**: Interfaz web para selección de agentes especializados
- **Datos Regionales**: Enfoque en información local (Colombia)

### 🏗️ Arquitectura Planificada

```mermaid
graph LR
    A[Usuario] --> B[Interfaz Streamlit]
    B --> C{Selector de Agentes}
    
    C --> D[Agente General]
    C --> E[Agente de Noticias]
    C --> F[Agente Inmobiliario]
    C --> G[Agente Financiero]
    C --> H[Agente Meteorológico]
    
    D --> I[Banco de Prompts]
    E --> I
    F --> I
    G --> I
    H --> I
    
    D --> J[Banco de Tools]
    E --> J
    F --> J
    G --> J
    H --> J
    
    J --> K[Tool: Tiempo]
    J --> L[Tool: Noticias]
    J --> M[MCP: Inmobiliaria]
    J --> N[Tool: Clima]
    J --> O[Tool: Finanzas]
    
    I --> P[Prompt: General]
    I --> Q[Prompt: Noticias]
    I --> R[Prompt: Inmobiliario]
    I --> S[Prompt: Financiero]
    
    D --> T[Gemini 2.5 Pro]
    E --> T
    F --> T
    G --> T
    H --> T
```

## 🛠️ Estado Actual del Desarrollo

### ✅ Funcionalidades Implementadas

- **Agente Base**: Configurado con Gemini 2.5 Pro
- **Sistema de Tools**: 
  - 🕐 Obtención de fecha y hora actual
  - 📰 Scraping de noticias de El Tiempo
  - 🏠 Consulta inmobiliaria via MCP
- **Esquemas Pydantic**: Validación de entrada y salida
- **Observabilidad**: Integración con Logfire
- **Arquitectura Modular**: Separación de prompts, tools y schemas

### 🚧 En Desarrollo

- [ ] Interfaz Streamlit para selección de agentes
- [ ] Agentes especializados por dominio
- [ ] Banco de prompts dinámico
- [ ] Herramientas adicionales (clima, finanzas)
- [ ] Sistema de configuración de agentes

## 🚀 Tecnologías Utilizadas

### Core Framework
- **Pydantic AI**: Framework principal para agentes de IA
- **Google Gemini 2.5 Pro**: Modelo de lenguaje base
- **Python 3.11+**: Lenguaje de programación

### Herramientas y Servicios
- **MCP (Model Context Protocol)**: Para servicios externos
- **Playwright**: Web scraping de noticias
- **Logfire**: Observabilidad y monitoreo
- **AsyncIO**: Programación asíncrona

### Futuras Integraciones
- **Streamlit**: Interfaz de usuario web

## 🎯 Agentes Especializados Planificados

### 📰 Agente de Noticias
- Fuentes: El Tiempo, El Espectador, Semana
- Categorización automática
- Resúmenes personalizados

### 🏠 Agente Inmobiliario
- Precios de vivienda en Colombia
- Análisis de mercado regional
- Recomendaciones de inversión

### 🌤️ Agente Meteorológico
- Clima actual y pronósticos
- Alertas meteorológicas
- Datos regionales específicos

### 💰 Agente Financiero
- Precios de acciones colombianas
- Tasas de cambio COP
- Indicadores económicos

## 💡 Características Clave

- **🔧 Modularidad**: Arquitectura basada en componentes reutilizables
- **🌎 Datos Regionales**: Enfoque en información colombiana
- **🔄 Asíncrono**: Operaciones no bloqueantes
- **📊 Observabilidad**: Monitoreo completo con Logfire
- **🛡️ Validación**: Esquemas Pydantic para datos seguros
- **🎨 Interfaz Futura**: Streamlit para experiencia de usuario

## 🚦 Roadmap

### Fase 1: Base (Actual) ✅
- [x] Agente general funcional
- [x] Herramientas básicas (tiempo, noticias, inmobiliaria)
- [x] Arquitectura modular

### Fase 2: Especialización 🚧
- [ ] Agentes especializados por dominio
- [ ] Banco de prompts dinámico
- [ ] Más herramientas regionales

### Fase 3: Interfaz 🔮
- [ ] Interfaz Streamlit
- [ ] Selector de agentes
- [ ] Dashboard de monitoreo

### Fase 4: Escalabilidad 🔮
- [ ] Base de datos persistente
- [ ] Cache distribuido
- [ ] API REST completa

