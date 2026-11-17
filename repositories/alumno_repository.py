from config.database import Database

class AlumnoRepository:
    def __init__(self):
        self.collection = Database().get_collection("alumnos")

    def crear(self, alumno_data: dict) -> dict:
        self.collection.insert_one(alumno_data.copy())
        return alumno_data

    def buscar_por_boleta(self, boleta: str) -> dict | None:
        return self.collection.find_one({"boleta": boleta}, {"_id": 0})

    def listar(self, filtro: dict, ordenar_por: str | None = None, direccion: int = 1) -> list[dict]:
        cursor = self.collection.find(filtro, {"_id": 0})
        if ordenar_por:
            cursor = cursor.sort(ordenar_por, direccion)
        return list(cursor)

    def actualizar(self, boleta: str, datos: dict) -> bool:
        resultado = self.collection.update_one(
            {"boleta": boleta},
            {"$set": datos}
        )
        return resultado.matched_count > 0

    def eliminar(self, boleta: str) -> bool:
        resultado = self.collection.delete_one({"boleta": boleta})
        return resultado.deleted_count > 0