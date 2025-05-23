from transformers import pipeline
from .poll_service import PollService

class ChatbotService:
    def __init__(self, poll_service: PollService):
        self.poll_service = poll_service
        self.chatbot = pipeline("conversational", model="facebook/blenderbot-400M-distill")

    def responder(self, mensaje, username):
        mensaje_lower = mensaje.lower()

        if "va ganando" in mensaje_lower or "resultados" in mensaje_lower:
            # Buscar encuesta activa
            encuestas = self.poll_service.repo.listar_encuestas()
            activas = [e for e in encuestas if e["estado"] == "activa"]
            if not activas:
                return "No hay encuestas activas en este momento."
            resultados = self.poll_service.resultados_parciales(activas[-1]["id"])
            return f"Resultados actuales: {resultados['resultados']}"
        
        # IA libre
        respuesta = self.chatbot(mensaje)
        if respuesta and "generated_text" in respuesta[0]:
            return f"{username}, {respuesta[0]['generated_text']}"
        return f"{username}, No entendí tu mensaje. ¿Puedes reformularlo?"