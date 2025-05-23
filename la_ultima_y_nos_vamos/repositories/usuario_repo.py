import json
import os

class UsuarioRepository:
    def __init__(self, path="data/usuarios.json"):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def registrar_usuario(self, usuario_dict):
        usuarios = self.listar_usuarios()
        usuarios.append(usuario_dict)
        with open(self.path, "w") as f:
            json.dump(usuarios, f)

    def listar_usuarios(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def obtener_usuario_por_username(self, username):
        for u in self.listar_usuarios():
            if u["username"] == username:
                return u
        return None

    def actualizar_usuario(self, username, nuevos_datos):
        usuarios = self.listar_usuarios()
        for i, u in enumerate(usuarios):
            if u["username"] == username:
                usuarios[i] = nuevos_datos
                break
        with open(self.path, "w") as f:
            json.dump(usuarios, f)
