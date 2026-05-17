# 🚀 Microservicio de Gestión de Usuarios — Pipeline CI/CD

> **Asignatura:** DOY0101 Ingeniería DevOps  
> **Evaluación:** Parcial N°2 — Añadiéndole complejidad a nuestro pipeline  
> **Equipo:** [Nombre Estudiante 1] · [Nombre Estudiante 2]  
> **Tecnología:** Python + FastAPI · Docker · Docker Compose · GitHub Actions · Snyk  

---

## 📋 Tabla de Contenidos

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Arquitectura del Pipeline CI/CD](#arquitectura-del-pipeline-cicd)
3. [Contenedores — Docker](#contenedores--docker)
4. [Orquestación — Docker Compose](#orquestación--docker-compose)
5. [Pruebas Automatizadas](#pruebas-automatizadas)
6. [Análisis de Seguridad — Snyk](#análisis-de-seguridad--snyk)
7. [Trazabilidad y Calidad](#trazabilidad-y-calidad)
8. [Cómo ejecutar localmente](#cómo-ejecutar-localmente)
9. [Uso de IA](#uso-de-ia)

---

## 📦 Descripción del Proyecto

Este repositorio es la continuación de la EP1. Sobre la base del microservicio REST de gestión de usuarios (FastAPI/Python) y el flujo GitFlow ya configurado, la EP2 incorpora:

- **Contenerización** con Docker (imagen multi-stage optimizada)
- **Orquestación** con Docker Compose
- **Pipeline CI/CD completo** en GitHub Actions con 4 jobs encadenados
- **Análisis de seguridad** con Snyk + Dependabot
- **Despliegue automatizado** en entorno simulado

---

## ⚙️ Arquitectura del Pipeline CI/CD

El pipeline tiene **4 jobs que se ejecutan en cadena**. Si uno falla, los siguientes no se ejecutan, garantizando que solo código seguro y probado llegue al despliegue.

```
Push a develop / PR a main
          │
          ▼
  ┌───────────────┐
  │  JOB 1: Test  │  pytest + flake8
  │  🧪 Pruebas   │
  └──────┬────────┘
         │ ✅ pasa
         ▼
  ┌───────────────┐
  │  JOB 2:       │  Snyk — escaneo de dependencias
  │  🔒 Seguridad │  BLOQUEO si hay vulnerabilidades HIGH/CRITICAL
  └──────┬────────┘
         │ ✅ pasa
         ▼
  ┌───────────────┐
  │  JOB 3: Build │  docker build — imagen multi-stage
  │  🐳 Docker    │
  └──────┬────────┘
         │ ✅ pasa
         ▼
  ┌───────────────┐
  │  JOB 4: Deploy│  docker compose up + health check + smoke test
  │  🚀 Entorno   │
  └───────────────┘
```

### Triggers del pipeline

| Evento | Rama | Jobs que se ejecutan |
|--------|------|---------------------|
| `push` | `develop` | Test → Security → Build → Deploy |
| `pull_request` | `main` | Test → Security → Build → Deploy |

### Archivo del workflow

Ubicación: `.github/workflows/ci-cd.yml`

---

## 🐳 Contenedores — Docker

### Estrategia multi-stage

El `Dockerfile` usa **dos etapas** para optimizar la imagen final:

| Etapa | Base | Propósito |
|-------|------|-----------|
| `builder` | `python:3.11-slim` | Instalar dependencias |
| `final` | `python:3.11-slim` | Solo el código y las deps instaladas |

Esto reduce el tamaño de la imagen final eliminando herramientas de compilación innecesarias.

### Buenas prácticas aplicadas

- ✅ **Usuario no-root:** el contenedor corre como `appuser`, no como `root` (seguridad)
- ✅ **Health check:** Docker verifica que el servicio responde en `/health`
- ✅ **Caché de capas:** `requirements.txt` se copia antes del código para aprovechar la caché de Docker
- ✅ **Imagen slim:** base mínima sin paquetes innecesarios

### Comandos útiles

```bash
# Construir la imagen
docker build -t microservicio-usuarios:latest .

# Ejecutar el contenedor
docker run -p 8000:8000 microservicio-usuarios:latest

# Ver logs
docker logs microservicio-usuarios

# Inspeccionar la imagen
docker inspect microservicio-usuarios:latest
```

---

## 🎼 Orquestación — Docker Compose

Docker Compose permite levantar y gestionar múltiples contenedores como un sistema coordinado. En este proyecto orquesta:

| Servicio | Puerto | Propósito |
|----------|--------|-----------|
| `usuarios-api` | 8000 | Microservicio principal |
| `test-runner` | — | Ejecutar tests (solo en perfil `testing`) |

### Características de la orquestación

- **Restart policy:** `unless-stopped` — el contenedor se reinicia automáticamente si falla
- **Health check:** Docker Compose monitorea el estado del servicio cada 30 segundos
- **Red interna:** los servicios se comunican a través de `devops-network` (bridge)
- **Profiles:** el runner de tests solo se activa en CI, no en producción

### Comandos de orquestación

```bash
# Levantar el entorno completo
docker compose up -d

# Levantar + ejecutar tests
docker compose --profile testing up

# Ver estado de los servicios
docker compose ps

# Ver logs en tiempo real
docker compose logs -f usuarios-api

# Detener y limpiar
docker compose down
```

---

## 🧪 Pruebas Automatizadas

Las pruebas se ejecutan en el **Job 1** del pipeline (primer paso), garantizando que ningún código sin pruebas llegue a las etapas siguientes.

### Framework y cobertura

- **Framework:** pytest + pytest-cov
- **Ubicación:** `tests/test_users.py`
- **Cobertura medida:** reporte por terminal en cada ejecución del pipeline

### Casos de prueba

| Test | Qué verifica |
|------|-------------|
| `test_listar_usuarios_vacio` | GET /users retorna lista vacía |
| `test_crear_usuario` | POST /users crea correctamente |
| `test_obtener_usuario_existente` | GET /users/{id} retorna el usuario |
| `test_obtener_usuario_no_existente` | GET /users/999 retorna 404 |
| `test_actualizar_usuario` | PUT /users/{id} actualiza datos |
| `test_eliminar_usuario` | DELETE /users/{id} elimina |

### Política de calidad

- El pipeline **bloquea el merge** si algún test falla
- Se requiere que **todos los tests pasen** (no hay excepciones)
- El linting con `flake8` también bloquea si hay errores de sintaxis

---

## 🔒 Análisis de Seguridad — Snyk

El análisis de seguridad corre en el **Job 2**, después de los tests y **antes** del build de Docker. Esto garantiza que no se construya ni despliegue una imagen con vulnerabilidades conocidas.

### Cómo funciona el bloqueo

```yaml
args: --severity-threshold=high
```

- **LOW / MEDIUM:** el pipeline continúa con advertencia
- **HIGH / CRITICAL:** ❌ el pipeline se detiene — no se hace build ni deploy

### Herramientas de seguridad configuradas

| Herramienta | Qué escanea | Cuándo corre |
|-------------|------------|--------------|
| **Snyk** | Vulnerabilidades en dependencias Python | En cada push/PR |
| **Dependabot** | Actualizaciones de dependencias | Cada lunes |

### Configurar el token de Snyk

1. Crear cuenta gratuita en [snyk.io](https://snyk.io) con tu cuenta de GitHub
2. Ir a **Account Settings → API Token** y copiar el token
3. En GitHub: **Settings → Secrets and variables → Actions → New secret**
4. Nombre: `SNYK_TOKEN`, valor: el token copiado

---

## 📊 Trazabilidad y Calidad

Cada ejecución del pipeline genera un **resumen de trazabilidad** visible en la pestaña Actions de GitHub:

```
══════════════════════════════════════
  TRAZABILIDAD DEL PIPELINE
══════════════════════════════════════
  Repo     : TANIAHR02/devops-gitflow-demo
  Commit   : abc123def456...
  Branch   : develop
  Actor    : TANIAHR02
  Fecha    : 2025-05-14 15:30:00 UTC
  Job      : 12345678
══════════════════════════════════════
```

### Cómo se garantiza la calidad en cada etapa

```
Código → Linting → Tests → Seguridad → Build → Deploy → Smoke Test
  ↑         ↑        ↑        ↑          ↑        ↑         ↑
 Dev      flake8   pytest    Snyk     Docker   Compose   curl/HTTP
```

Ninguna etapa puede saltarse. El encadenamiento `needs:` en el workflow garantiza el orden y el bloqueo ante fallos.

### Artefactos generados por el pipeline

| Artefacto | Retención | Contenido |
|-----------|-----------|-----------|
| `snyk-security-report` | 30 días | Reporte JSON de vulnerabilidades |
| `docker-image` | 7 días | Imagen Docker comprimida (.tar.gz) |

---

## 💻 Cómo ejecutar localmente

### Sin Docker

```bash
# Clonar repo
git clone https://github.com/TANIAHR02/devops-gitflow-demo.git
cd devops-gitflow-demo

# Crear entorno virtual (Windows)
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la API
uvicorn main:app --reload

# Ejecutar tests
pytest tests/ -v
```

### Con Docker Compose

```bash
# Levantar todo
docker compose up -d

# Verificar que corre
curl http://localhost:8000/health

# Ver la API en el navegador
# http://localhost:8000/docs
```

---

## 🤖 Uso de IA

En el desarrollo de este proyecto se utilizó **Claude (Anthropic)** como apoyo para:

- Generación del esqueleto del `Dockerfile` y `docker-compose.yml`
- Estructura inicial del workflow de GitHub Actions
- Revisión y mejora de redacción técnica en el README

Todo el contenido fue revisado, adaptado y validado por el equipo. Las justificaciones técnicas, decisiones de arquitectura (elección de Docker Compose sobre Kubernetes, estrategia multi-stage, política de bloqueo de Snyk) y reflexiones individuales fueron redactadas por los integrantes sin asistencia de IA.

**Referencia de uso de IA:** https://bibliotecas.duoc.cl/ia

---

*Última actualización: 2025 — DOY0101 Ingeniería DevOps — EP2*
