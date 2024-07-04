import hashlib
from redis_utils.redis_utilizador import obter_dados_utilizador

def verifica_login(username, password):
    # Caso o username não esteja guardado no redis, retorna False
    try:
        dados = obter_dados_utilizador(username)
    
        stored_hash, salt, isAdmin = dados['hash'], dados['salt'], dados['isAdmin']
        # Converte o salt de hexadecimal para bytes
        salt = bytes.fromhex(salt)

        # Gera o hash da password fornecida com o mesmo salt
        hashed_password = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
        
        hashed_password = hashed_password.hex()
        
        # Verifica se o hash gerado é igual ao hash guardado (verifica se a password está correta)
        if (hashed_password == stored_hash):
            return (True, isAdmin)
        else:
            return (False, isAdmin)
    except:
        return (False, False)