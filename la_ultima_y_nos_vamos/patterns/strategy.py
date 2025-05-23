class EstrategiaConteo:
    def contar(self, opciones):
        raise NotImplementedError

class ConteoNormal(EstrategiaConteo):
    def contar(self, opciones):
        total = sum(opciones.values())
        return {
            op: f"{votos} votos ({(votos/total)*100:.1f}%)"
            for op, votos in opciones.items()
        }

class ConteoAbsoluto(EstrategiaConteo):
    def contar(self, opciones):
        return {op: f"{votos} votos" for op, votos in opciones.items()}
