from fastapi import FastAPI
from controllers.alumno_controller import router as alumno_router

app = FastAPI(
    title="API REST CRUD Alumnos",
    description="Práctica de Arquitectura en Capas (Controller -> Service -> Repository) con MongoDB",
    version="1.0.0"
)

app.include_router(alumno_router)

@app.get("/")
def root():
    return {"status": "API operando", "docs": "/docs"}
