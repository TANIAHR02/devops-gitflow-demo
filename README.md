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

