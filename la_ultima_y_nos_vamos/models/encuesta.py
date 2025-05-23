from datetime import datetime, timedelta
import uuid

class Encuesta:
    def __init__(self, pregunta, opciones, duracion_segundos, tipo="simple"):
        self.id = str(uuid.uuid4())
        self.pregunta = pregunta
        self.opciones = opciones
        self.votos = {opcion: 0 for opcion in opciones}
        self.usuarios_que_votaron = set()
        self.tipo = tipo
        self.estado = "activa"
        self.timestamp_inicio = datetime.now()
        self.duracion = timedelta(seconds=duracion_segundos)

    def votar(self, username, opcion):
        if self.estado != "activa":
            raise Exception("Encuesta cerrada.")
        if username in self.usuarios_que_votaron:
            raise Exception("Usuario ya votó.")
        if opcion not in self.opciones:
            raise Exception("Opción inválida.")
        self.votos[opcion] += 1
        self.usuarios_que_votaron.add(username)

    def cerrar(self):
        self.estado = "cerrada"

    def esta_activa(self):
        return datetime.now() < self.timestamp_inicio + self.duracion and self.estado == "activa"
