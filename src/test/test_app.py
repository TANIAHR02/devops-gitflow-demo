import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from app import app, db, counter

@pytest.fixture(autouse=True)
def limpiar_db():
    """Limpia la base de datos antes de cada test para independencia"""
    db.clear()
    global counter
    import app as app_module
    app_module.counter = 1
    yield
    db.clear()
    app_module.counter = 1

client = TestClient(app)


# ── Health Check ──────────────────────────────────────────────
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_health_contiene_version():
    response = client.get("/health")
    assert "version" in response.json()


# ── Listar usuarios ───────────────────────────────────────────
def test_listar_usuarios_vacio():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []

def test_listar_usuarios_con_datos():
    client.post("/users", json={"name": "Tania", "email": "tania@test.com"})
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 1


# ── Crear usuario ─────────────────────────────────────────────
def test_crear_usuario_exitoso():
    response = client.post("/users", json={"name": "Tania", "email": "tania@test.com"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Tania"
    assert data["email"] == "tania@test.com"
    assert "id" in data

def test_crear_usuario_sin_email():
    response = client.post("/users", json={"name": "SinEmail"})
    assert response.status_code == 422

def test_crear_usuario_sin_nombre():
    response = client.post("/users", json={"email": "sin@nombre.com"})
    assert response.status_code == 422

def test_crear_usuario_sin_datos():
    response = client.post("/users", json={})
    assert response.status_code == 422

def test_crear_multiples_usuarios():
    client.post("/users", json={"name": "Usuario1", "email": "u1@test.com"})
    client.post("/users", json={"name": "Usuario2", "email": "u2@test.com"})
    response = client.get("/users")
    assert len(response.json()) == 2


# ── Obtener usuario ───────────────────────────────────────────
def test_obtener_usuario_existente():
    client.post("/users", json={"name": "Ana", "email": "ana@test.com"})
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Ana"

def test_obtener_usuario_inexistente():
    response = client.get("/users/9999")
    assert response.status_code == 404


# ── Actualizar usuario ────────────────────────────────────────
def test_actualizar_usuario_exitoso():
    client.post("/users", json={"name": "Pedro", "email": "pedro@test.com"})
    response = client.put("/users/1", json={"name": "Pedro Actualizado", "email": "pedro2@test.com"})
    assert response.status_code == 200
    assert response.json()["name"] == "Pedro Actualizado"
    assert response.json()["email"] == "pedro2@test.com"

def test_actualizar_usuario_inexistente():
    response = client.put("/users/9999", json={"name": "X", "email": "x@x.com"})
    assert response.status_code == 404

def test_actualizar_usuario_sin_datos():
    client.post("/users", json={"name": "Luis", "email": "luis@test.com"})
    response = client.put("/users/1", json={})
    assert response.status_code == 422


# ── Eliminar usuario ──────────────────────────────────────────
def test_eliminar_usuario_exitoso():
    client.post("/users", json={"name": "Eliminar", "email": "eliminar@test.com"})
    response = client.delete("/users/1")
    assert response.status_code == 204

def test_eliminar_usuario_inexistente():
    response = client.delete("/users/9999")
    assert response.status_code == 404

def test_eliminar_usuario_ya_no_existe():
    client.post("/users", json={"name": "Borrar", "email": "borrar@test.com"})
    client.delete("/users/1")
    response = client.get("/users/1")
    assert response.status_code == 404
