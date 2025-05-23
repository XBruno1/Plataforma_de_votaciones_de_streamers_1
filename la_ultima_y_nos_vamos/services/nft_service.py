from uuid import uuid4
from datetime import datetime, timezone
from ..repositories.nft_repo import NFTRepository

class NFTService:
    def __init__(self, nft_repo: NFTRepository):
        self.repo = nft_repo

    def mint_token(self, owner, poll_id, opcion):
        token = {
            "token_id": str(uuid4()),
            "owner": owner,
            "poll_id": poll_id,
            "option": opcion,
            "issued_at": datetime.now(timezone.utc).isoformat()
        }
        self.repo.guardar_token(token)

    def transferir_token(self, token_id, nuevo_owner, usuario_actual):
        tokens = self.repo.listar_tokens()
        token = next((t for t in tokens if t["token_id"] == token_id), None)
        if not token or token["owner"] != usuario_actual:
            raise ValueError("No puedes transferir este token.")
        self.repo.transferir_token(token_id, nuevo_owner)

    def tokens_de_usuario(self, username):
        return self.repo.obtener_tokens_por_usuario(username)
