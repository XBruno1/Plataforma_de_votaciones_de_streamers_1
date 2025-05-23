import uuid
import bcrypt
from repositories.usuario_repo import UsuarioRepository

class UserService:
    def __init__(self, usuario_repo: UsuarioRepository):
        self.repo = usuario_repo
        self.sesiones = {}

    def registrar(self, username, password):
        if self.repo.obtener_usuario_por_username(username):
            raise ValueError("Usuario ya registrado.")
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.repo.registrar_usuario({
            "username": username,
            "password": hashed.decode(),
            "tokens": []
        })

    def login(self, username, password):
        usuario = self.repo.obtener_usuario_por_username(username)
        if not usuario:
            raise ValueError("Usuario no encontrado.")
        if not bcrypt.checkpw(password.encode(), usuario["password"].encode()):
            raise ValueError("Contraseña incorrecta.")
        token_sesion = str(uuid.uuid4())
        self.sesiones[token_sesion] = username
        return token_sesion

    def obtener_usuario_actual(self, token_sesion):
        return self.sesiones.get(token_sesion)
