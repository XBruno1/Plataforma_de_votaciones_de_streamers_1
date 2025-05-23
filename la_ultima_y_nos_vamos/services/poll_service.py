from uuid import uuid4
from datetime import datetime, timedelta, timezone
from ..repositories.encuesta_repo import EncuestaRepository
from .nft_service import NFTService

class PollService:
    def __init__(self, encuesta_repo: EncuestaRepository, nft_service: NFTService):
        self.repo = encuesta_repo
        self.nft_service = nft_service

    def crear_encuesta(self, pregunta, opciones, duracion_segundos, tipo="simple"):
        nueva_encuesta = {
            "id": str(uuid4()),
            "pregunta": pregunta,
            "opciones": {opcion: 0 for opcion in opciones},
            "votos": [],
            "estado": "activa",
            "timestamp_inicio": datetime.now(timezone.utc).isoformat(),
            "duracion": duracion_segundos,
            "tipo": tipo
        }
        self.repo.guardar_encuesta(nueva_encuesta)
        return nueva_encuesta

    def votar(self, poll_id, username, opcion):
        encuesta = self.repo.obtener_encuesta_por_id(poll_id)
        if not encuesta or encuesta["estado"] != "activa":
            raise ValueError("Encuesta inválida o cerrada.")
        if username in [v["username"] for v in encuesta["votos"]]:
            raise ValueError("Este usuario ya ha votado.")

        if opcion not in encuesta["opciones"]:
            raise ValueError("Opción inválida.")

        encuesta["opciones"][opcion] += 1
        encuesta["votos"].append({"username": username, "opcion": opcion})

        # Generar token
        self.nft_service.mint_token(username, poll_id, opcion)

        self.repo.actualizar_encuesta(poll_id, encuesta)
        return encuesta

    def cerrar_encuesta(self, poll_id):
        encuesta = self.repo.obtener_encuesta_por_id(poll_id)
        if encuesta["estado"] != "activa":
            return
        encuesta["estado"] = "cerrada"
        self.repo.actualizar_encuesta(poll_id, encuesta)

    def verificar_cierre_automatico(self):
        for encuesta in self.repo.listar_encuestas():
            if encuesta["estado"] == "activa":
                inicio = datetime.fromisoformat(encuesta["timestamp_inicio"])
                fin = inicio + timedelta(seconds=encuesta["duracion"])
                if datetime.now(timezone.utc) > fin:
                    self.cerrar_encuesta(encuesta["id"])

    def resultados_parciales(self, poll_id):
        encuesta = self.repo.obtener_encuesta_por_id(poll_id)
        total = sum(encuesta["opciones"].values())
        return {
            "pregunta": encuesta["pregunta"],
            "resultados": {
                op: f"{conteo} votos ({(conteo/total)*100:.1f}%)"
                for op, conteo in encuesta["opciones"].items()
            }
        }

    def resultados_finales(self, poll_id):
        encuesta = self.repo.obtener_encuesta_por_id(poll_id)
        if encuesta["estado"] != "cerrada":
            raise ValueError("La encuesta aún está activa.")
        return self.resultados_parciales(poll_id)
