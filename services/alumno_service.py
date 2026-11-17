from repositories.alumno_repository import AlumnoRepository

CAMPOS_ORDENABLES = {"boleta", "nombre", "edad", "sexo", "carrera"}
SEXOS_VALIDOS = {"M", "F", "O"}

class AlumnoService:
    def __init__(self):
        self.repo = AlumnoRepository()

    def crear_alumno(self, alumno_data: dict) -> dict:
        if self.repo.buscar_por_boleta(alumno_data["boleta"]):
            raise ValueError(f"Ya existe un alumno con la boleta {alumno_data['boleta']}.")
        
        alumno_data["sexo"] = alumno_data["sexo"].upper()
        if alumno_data["sexo"] not in SEXOS_VALIDOS:
            raise ValueError("El campo 'sexo' debe ser 'M', 'F' u 'O'.")

        return self.repo.crear(alumno_data)

    def obtener_alumnos(
        self,
        boleta: str | None = None,
        sexo: str | None = None,
        edad: int | None = None,
        ordenar_por: str | None = None,
        orden: str = "asc"
    ):
        # MODO 1: Búsqueda individual por Path Param (/api/v1/alumnos/{boleta})
        if boleta is not None:
            if any(param is not None for param in (sexo, edad, ordenar_por)):
                raise ValueError("No se permiten filtros query (sexo, edad, ordenar_por) al buscar un alumno específico por boleta.")
            
            alumno = self.repo.buscar_por_boleta(boleta)
            if not alumno:
                raise LookupError(f"No se encontró ningún alumno con la boleta {boleta}.")
            return alumno

        # MODO 2: Listado con Query Params (/api/v1/alumnos?sexo=M&edad=21&ordenar_por=edad&orden=asc)
        filtro = {}

        if sexo is not None:
            sexo_upper = sexo.upper()
            if sexo_upper not in SEXOS_VALIDOS:
                raise ValueError("Filtro 'sexo' inválido. Valores permitidos: M, F, O.")
            filtro["sexo"] = sexo_upper

        if edad is not None:
            if edad < 15 or edad > 100:
                raise ValueError("Filtro 'edad' inválido. Debe estar entre 15 y 100.")
            filtro["edad"] = edad

        if ordenar_por is not None:
            if ordenar_por not in CAMPOS_ORDENABLES:
                raise ValueError(f"No se puede ordenar por '{ordenar_por}'. Campos válidos: {', '.join(CAMPOS_ORDENABLES)}.")

        orden_lower = orden.lower()
        if orden_lower not in {"asc", "desc"}:
            raise ValueError("El parámetro 'orden' solo acepta 'asc' o 'desc'.")

        direccion = 1 if orden_lower == "asc" else -1
        return self.repo.listar(filtro=filtro, ordenar_por=ordenar_por, direccion=direccion)

    def editar_alumno(self, boleta: str, datos_actualizados: dict) -> dict:
        if not self.repo.buscar_por_boleta(boleta):
            raise LookupError(f"No se encontró ningún alumno con la boleta {boleta}.")

        datos_limpios = {k: v for k, v in datos_actualizados.items() if v is not None}
        if not datos_limpios:
            raise ValueError("Debes enviar al menos un campo válido para actualizar.")

        if "sexo" in datos_limpios:
            datos_limpios["sexo"] = datos_limpios["sexo"].upper()
            if datos_limpios["sexo"] not in SEXOS_VALIDOS:
                raise ValueError("El campo 'sexo' debe ser 'M', 'F' u 'O'.")

        self.repo.actualizar(boleta, datos_limpios)
        return self.repo.buscar_por_boleta(boleta)

    def borrar_alumno(self, boleta: str) -> dict:
        eliminado = self.repo.eliminar(boleta)
        if not eliminado:
            raise LookupError(f"No se pudo eliminar: no existe alumno con boleta {boleta}.")
        return {"mensaje": f"Alumno con boleta {boleta} eliminado exitosamente."}