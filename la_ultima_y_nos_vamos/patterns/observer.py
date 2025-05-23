class Observable:
    def __init__(self):
        self._observadores = []

    def registrar(self, observador):
        self._observadores.append(observador)

    def notificar(self, mensaje):
        for obs in self._observadores:
            obs.actualizar(mensaje)

class Observador:
    def actualizar(self, mensaje):
        raise NotImplementedError

# Ejemplo de observador que imprime a consola
class LoggerObservador(Observador):
    def actualizar(self, mensaje):
        print(f"[NOTIFICACIÓN] {mensaje}")
