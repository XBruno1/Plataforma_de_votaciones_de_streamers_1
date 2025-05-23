import hashlib
import uuid

class Usuario:
    def __init__(self, username, password_plain):
        self.username = username
        self.password_hash = self._hash_password(password_plain)
        self.tokens = []

    def _hash_password(self, password):
        return hashlib.pbkdf2_hmac('sha256', password.encode(), b'salt', 100000).hex()

    def verificar_password(self, password_plain):
        return self.password_hash == self._hash_password(password_plain)
