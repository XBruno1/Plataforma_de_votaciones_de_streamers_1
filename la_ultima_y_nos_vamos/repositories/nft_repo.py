import json
import os

class NFTRepository:
    def __init__(self, path="data/tokens.json"):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def guardar_token(self, token_dict):
        tokens = self.listar_tokens()
        tokens.append(token_dict)
        with open(self.path, "w") as f:
            json.dump(tokens, f, default=str)

    def listar_tokens(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def obtener_tokens_por_usuario(self, username):
        return [t for t in self.listar_tokens() if t["owner"] == username]

    def transferir_token(self, token_id, nuevo_owner):
        tokens = self.listar_tokens()
        for t in tokens:
            if t["token_id"] == token_id:
                t["owner"] = nuevo_owner
                break
        with open(self.path, "w") as f:
            json.dump(tokens, f)
