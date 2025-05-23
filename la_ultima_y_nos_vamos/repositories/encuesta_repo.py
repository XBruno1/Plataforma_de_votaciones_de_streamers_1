import json
import os

class EncuestaRepository:
    def __init__(self, path="data/encuestas.json"):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def guardar_encuesta(self, encuesta_dict):
        encuestas = self.listar_encuestas()
        encuestas.append(encuesta_dict)
        with open(self.path, "w") as f:
            json.dump(encuestas, f, default=str)

    def listar_encuestas(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def actualizar_encuesta(self, encuesta_id, nuevos_datos):
        encuestas = self.listar_encuestas()
        for i, e in enumerate(encuestas):
            if e["id"] == encuesta_id:
                encuestas[i] = nuevos_datos
                break
        with open(self.path, "w") as f:
            json.dump(encuestas, f, default=str)

    def obtener_encuesta_por_id(self, encuesta_id):
        encuestas = self.listar_encuestas()
        for e in encuestas:
            if e["id"] == encuesta_id:
                return e
        return None
