from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Microservicio Usuarios", version="1.0.0")

# Base de datos simulada en memoria
db: dict = {}
counter: int = 1


class User(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


# ── Health Check (requerido por Docker y Docker Compose) ──────────
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "microservicio-usuarios", "version": "1.0.0"}


# ── Endpoints CRUD ────────────────────────────────────────────────
@app.get("/users", response_model=list[UserResponse])
def list_users():
    return list(db.values())


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db[user_id]


@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: User):
    global counter
    new_user = {"id": counter, "name": user.name, "email": user.email}
    db[counter] = new_user
    counter += 1
    return new_user


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: User):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db[user_id].update({"name": user.name, "email": user.email})
    return db[user_id]


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    del db[user_id]
