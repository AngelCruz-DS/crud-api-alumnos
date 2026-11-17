from fastapi import APIRouter, HTTPException, Path, Query, status
from pydantic import BaseModel, Field
from services.alumno_service import AlumnoService

router = APIRouter(prefix="/api/v1/alumnos", tags=["Alumnos"])
service = AlumnoService()

# Esquemas de validación de entrada (Body JSON)
class AlumnoCreate(BaseModel):
    boleta: str = Field(..., min_length=8, max_length=12, examples=["2025630101"])
    nombre: str = Field(..., min_length=2, examples=["Angel Cruz"])
    edad: int = Field(..., ge=15, le=100, examples=[21])
    sexo: str = Field(..., examples=["M"])
    carrera: str = Field(..., examples=["Licenciatura en Ciencia de Datos"])

class AlumnoUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=2)
    edad: int | None = Field(None, ge=15, le=100)
    sexo: str | None = None
    carrera: str | None = None

# 1. CREAR ALUMNO (POST)
@router.post("", status_code=status.HTTP_201_CREATED)
def crear_alumno(alumno: AlumnoCreate):
    try:
        return service.crear_alumno(alumno.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# 2 y 3. LISTAR (con query params) Y BUSCAR UNO (con path param) EN UNA MISMA FUNCIÓN (GET)
@router.get("")
@router.get("/{boleta}")
def consultar_alumnos(
    boleta: str | None = None,
    sexo: str | None = Query(None, description="Filtrar por sexo: M, F, O (Query Param)"),
    edad: int | None = Query(None, description="Filtrar por edad exacta (Query Param)"),
    ordenar_por: str | None = Query(None, description="Campo para ordenar: nombre, edad, sexo, boleta, carrera"),
    orden: str = Query("asc", description="Dirección de ordenamiento: asc o desc")
):
    try:
        return service.obtener_alumnos(
            boleta=boleta,
            sexo=sexo,
            edad=edad,
            ordenar_por=ordenar_por,
            orden=orden
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# 4. EDITAR ALUMNO (PUT)
@router.put("/{boleta}")
def editar_alumno(boleta: str, datos: AlumnoUpdate):
    try:
        return service.editar_alumno(boleta, datos.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# 5. BORRAR ALUMNO (DELETE con recurso en URL)
@router.delete("/{boleta}")
def borrar_alumno(boleta: str):
    try:
        return service.borrar_alumno(boleta)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))