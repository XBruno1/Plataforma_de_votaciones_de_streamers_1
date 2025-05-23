import gradio as gr
from services.poll_service import PollService
from services.chatbot_service import ChatbotService
from services.nft_service import NFTService

poll_service = PollService()
chatbot_service = ChatbotService()
nft_service = NFTService()

def mostrar_encuestas():
    encuestas = poll_service.obtener_encuestas_activas()
    return [poll.pregunta for poll in encuestas]

def votar(poll_pregunta, username, opcion):
    try:
        encuestas = poll_service.obtener_encuestas_activas()
        poll = next((e for e in encuestas if e.pregunta == poll_pregunta), None)
        if not poll:
            return "❌ Encuesta no encontrada."
        resultado = poll_service.votar(poll.id, username, opcion)
        return f"✅ Voto registrado: {resultado}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def responder_chat(username, mensaje):
    return chatbot_service.responder(username, mensaje)

def ver_tokens(username):
    tokens = nft_service.obtener_tokens(username)
    if not tokens:
        return "Este usuario no tiene tokens."
    return "\n".join([f"{t.token_id} - {t.option} ({t.poll_id})" for t in tokens])

def transferir_token(token_id, nuevo_owner):
    try:
        nft_service.transferir_token(token_id, nuevo_owner)
        return "✅ Token transferido correctamente."
    except Exception as e:
        return f"❌ Error: {str(e)}"

with gr.Blocks(title="La Última y Nos Vamos") as demo:
    gr.Markdown("## 🎮 La Última y Nos Vamos - Interfaz de Votación para Espectadores")

    with gr.Tab("🗳️ Encuestas"):
        username_input = gr.Text(label="Tu usuario")
        encuesta_selector = gr.Dropdown(label="Encuestas activas", choices=mostrar_encuestas())
        opcion_input = gr.Text(label="Tu opción (exacta)")
        votar_btn = gr.Button("Votar")
        voto_resultado = gr.Textbox()

        votar_btn.click(fn=votar, inputs=[encuesta_selector, username_input, opcion_input], outputs=voto_resultado)
        encuesta_selector.change(fn=mostrar_encuestas, inputs=[], outputs=encuesta_selector)

    with gr.Tab("🤖 Chatbot"):
        chat_username = gr.Text(label="Tu usuario")
        chat_input = gr.Textbox(label="Mensaje")
        chat_output = gr.Textbox(label="Respuesta del bot")
        chat_btn = gr.Button("Enviar")
        chat_btn.click(fn=responder_chat, inputs=[chat_username, chat_input], outputs=chat_output)

    with gr.Tab("🎁 Mis Tokens NFT"):
        token_user = gr.Text(label="Tu usuario")
        token_output = gr.Textbox(label="Tus tokens")
        token_btn = gr.Button("Ver tokens")
        token_btn.click(fn=ver_tokens, inputs=token_user, outputs=token_output)

        transfer_id = gr.Text(label="Token ID")
        nuevo_owner = gr.Text(label="Nuevo dueño")
        transfer_btn = gr.Button("Transferir token")
        transfer_resultado = gr.Textbox()
        transfer_btn.click(fn=transferir_token, inputs=[transfer_id, nuevo_owner], outputs=transfer_resultado)

