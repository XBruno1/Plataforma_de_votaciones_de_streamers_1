class EncuestaFactory:
    @staticmethod
    def crear_encuesta(tipo, pregunta, opciones, duracion):
        if tipo == "simple":
            return {
                "tipo": tipo,
                "pregunta": pregunta,
                "opciones": {op: 0 for op in opciones},
                "votos": [],
                "estado": "activa",
                "duracion": duracion
            }
        elif tipo == "multiple":
            return {
                "tipo": tipo,
                "pregunta": pregunta,
                "opciones": {op: 0 for op in opciones},
                "votos": [],
                "estado": "activa",
                "duracion": duracion,
                "permite_varios": True
            }
        else:
            raise ValueError("Tipo de encuesta no soportado.")
