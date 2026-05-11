# devops-gitflow-demo - EP2

Instrucciones rápidas:

- Ejecutar tests:

```bash
python -m pytest src/test/ -v
```

- Construir imagen Docker:

```bash
docker build -t devops-app .
```

- Levantar con Docker Compose:

```bash
docker compose up -d
```

Alternativa sin construir imagen local (usa una imagen base y monta el código):

```bash
# ya configurado en docker-compose.yml — arranca instalando deps en el contenedor
docker compose up -d
```


```bash
docker build -t devops-app .
docker compose up -d
```
Publicar imagen en GHCR (recomendado para rúbrica):

1. En el repositorio de GitHub, añade el secret `GITHUB_TOKEN` (automático) o usa `CR_PAT` si prefieres token personal.
2. El workflow `.github/workflows/build-and-push.yml` construye, testea y publica la imagen en `ghcr.io/<owner>/<repo>:latest` al hacer push a `main`.

Localmente puedes usar la imagen publicada o la imagen local `devops-app:latest`.

---
Nota: este commit adicional dispara el workflow `build-and-push.yml` en GitHub Actions.
Si la publicación a GHCR requiere permisos adicionales, habilita `write:packages` para `GITHUB_TOKEN` en la configuración del repositorio.

- Git:

```bash
git add .
git commit -m "Add EP2 files"
git push origin main
```
# DevOps Gitflow Demo

## Descripción
Este proyecto demuestra la implementación de Gitflow utilizando GitHub.

## Estrategia de ramas
- main: producción
- develop: desarrollo
- feature/*: nuevas funcionalidades
- hotfix/*: corrección de errores

## Flujo de trabajo
Se utilizó Gitflow:
- feature/login
- feature/productos
- hotfix/login-error

## Simulación colaborativa
Se simularon múltiples desarrolladores (dev1, dev2).

## GitHub Actions
Se implementó una acción básica de integración continua (CI).

## Tecnologías
- Git
- GitHub
- GitHub Actions

## Pull Requests realizados
Durante el desarrollo del proyecto se implementaron los siguientes Pull Requests:

- feature/login -> develop
Se implementó el módulo de autenticación de usuarios, incluyendo validación básica de login.
- feature/productos -> develop
Se desarrolló el módulo de productos, incorporando listado y funcionalidad de carrito de compras.
- hotfix/login-error -> main
Se corrigió un error crítico en la validación de usuarios en producción, asegurando el correcto funcionamiento del login.

## Cómo ejecutar el proyecto

Este proyecto es una simulación de flujo de trabajo con Gitflow, por lo que no requiere instalación ni ejecución de software.

Para revisar su funcionamiento:

Clonar el repositorio:

git clone https://github.com/TANIAHR02/devops-gitflow-demo

Revisar las ramas disponibles:

git branch -a
Analizar el historial de commits y Pull Requests en GitHub.
Verificar la ejecución de integración continua en la pestaña Actions.

