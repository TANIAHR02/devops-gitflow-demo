# ── Etapa 1: builder ──────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Copiar solo requirements primero (aprovecha caché de Docker)
COPY requirements.txt .

# Instalar dependencias en carpeta local para copiar después
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Etapa 2: imagen final ─────────────────────────────────────────
FROM python:3.11-slim

# Metadatos de la imagen
LABEL maintainer="Equipo DevOps DOY0101"
LABEL version="1.0.0"
LABEL description="Microservicio de Gestión de Usuarios - FastAPI"

WORKDIR /app

# Copiar dependencias instaladas desde el builder
COPY --from=builder /install /usr/local

# Copiar código fuente
COPY . .

# Crear usuario no-root por seguridad (buena práctica DevSecOps)
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

USER appuser

# Exponer puerto de la aplicación
EXPOSE 8000

# Health check para Docker y Docker Compose
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Comando de inicio
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]