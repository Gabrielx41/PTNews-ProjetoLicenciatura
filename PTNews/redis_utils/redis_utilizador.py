import os
import redis
from dotenv import load_dotenv
import json

load_dotenv(override=True)

r = redis.Redis(
                 host = os.getenv("HOST_REDIS"), 
                 port = int(os.getenv("PORT_REDIS")),
                 decode_responses=True
                )

def utilizador_admin(username):
    global r
    
    try:
            data = r.ft("users").search(f'@username:{username}').docs[0]
            isAdmin = json.loads(data['isAdmin'])
            return isAdmin
    except Exception as e:
            print(f"Erro ao verificar se o utilizador é admin no Redis: {e}")
            return False
    

def utilizador_existe(username):
    global r
    
    try:
            if r.ft("users").search(f'@username:{username}').docs:
                return True
            else:
                return False
    except Exception as e:
            print(f"Erro ao verificar se o utilizador existe no Redis: {e}")
            return False

#Indexar documento
def index_document(r, username, document):
    try:
        key = f"User:{username}"
        r.hset(key, mapping=document)
    except Exception as e:
        print(f"Error indexing document: {e}")


#Função para guarda os dados no Redis
def guardar_dados_utilizador(username, data):
    global r
    
    data['isAdmin'] = json.dumps(data['isAdmin'], ensure_ascii=False).encode('utf-8')
    
    
    try:
            # Verificar se já existe um documento com o mesmo username
            if not utilizador_existe(username):
                index_document(r, username, data)
                return True
            else:
                print("Erro: Já existe um utilizador com esse username.")
                return False
            
    except Exception as e:
            print(f"Erro ao guardar os dados no Redis: {e}")
            return False


# Função para obter os dados do Redis
def obter_dados_utilizador(username):
    global r

    try:
        data = r.ft("users").search(f'@username:{username}').docs[0]
        print(data)
        dados = {'username': data['username'],'isAdmin': json.loads(data['isAdmin']), 'salt': data['salt'], 'hash': data['hash']}
        return dados
    
    except Exception as e:
        print(f"Erro ao obter os dados no Redis: {e}")
        return {}
    
    
def obter_dados_utilizadores(query):
    global r

    #Verifica se conseguiu ligar ao Redis
    try:
            lista = []
            keys = r.ft("users").search(query).docs
            
            # Iterando sobre as chaves e obtendo os valores correspondentes
            for key in keys:
                username = key['username']
                isAdmin = json.loads(key['isAdmin'])
                    
                lista.append({"username": username, "isAdmin": isAdmin})
            return lista
    except Exception as e:
            print(f"Erro ao obter os dados no Redis: {e}")
            return []


def remover_user(username):
    global r

    try:
            r.delete(f"User:{username}")
            return True
    except Exception as e:
            print(f"Erro ao remover os dados no Redis: {e}")
            return False