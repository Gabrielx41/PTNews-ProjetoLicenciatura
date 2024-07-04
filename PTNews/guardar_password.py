import hashlib
import os
from redis_utils.redis_utilizador import guardar_dados_utilizador

def guardar_password(username, password, isAdmin):
    # Gera um salt aleatório com 64 bytes (512 bits)
    salt = os.urandom(64)
    
    # Combina a password e o salt
    hashed_password = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    
    dados = {'username': username,'hash': hashed_password.hex(), 'salt': salt.hex(), 'isAdmin': isAdmin}

    resposta = guardar_dados_utilizador(username, dados)
    
    return resposta