from collections import defaultdict
from ..Uteis.InvertedIndex import InvertedIndex
from ..Ficheiros.ficheiros_json import ler_ficheiro_json, escrever_ficheiro_json
import redis
import os
import threading
from dotenv import load_dotenv
import json


load_dotenv(override=True)

r = redis.Redis(
                 host = os.getenv("HOST_REDIS"),
                 port = int(os.getenv("PORT_REDIS")),
                 decode_responses=True
                )

lock = threading.Lock()


#Indexar documento
def index_document(r, doc_prefix, docs):
    document = docs.copy()
    #Converter as listas e possíveis None para json
    document['images'] = json.dumps(document['images'], ensure_ascii=False).encode('utf-8')
    document['authors'] = json.dumps(document['authors'], ensure_ascii=False).encode('utf-8')
    document['entities'] = json.dumps(document['entities'], ensure_ascii=False).encode('utf-8')
    document['tags'] = json.dumps(document['tags'], ensure_ascii=False).encode('utf-8')
    document['keywords'] = json.dumps(document['keywords'], ensure_ascii=False).encode('utf-8')
    document['lead'] = json.dumps(document['lead'], ensure_ascii=False).encode('utf-8')
    document['content'] = json.dumps(document['content'], ensure_ascii=False).encode('utf-8')
    document['sentiment'] = json.dumps(document['sentiment'], ensure_ascii=False).encode('utf-8')
    try:
        key = f"{doc_prefix}:{document['id']}"
        r.hset(key, mapping=document)
        return True
    except Exception as e:
        print(f"Erro ao indexar documento no Redis [Notícias]: {e}")
        return False



def guardar_dados_ficheiro(data, file):
    dados = ler_ficheiro_json(file)
    dados.append(data)
    escrever_ficheiro_json(file, dados)


#Função para guarda os dados no Redis
def guardar_dados(data):
    global r, lock
    is_indexed = False
    file = "PTNews_Script/Dados/" + data['source'] + ".json"

    #Se não conseguir ligar ao Redis, guarda os dados num ficheiro
    dados_ficheiro = ler_ficheiro_json(file)

            #Verifica se existem dados no ficheiro
    if(dados_ficheiro):
        dados_ficheiro.append(data)

        for dados in dados_ficheiro:
            lock.acquire()

            is_indexed = index_document(r, dados['source'], dados)

            lock.release()

        if is_indexed:
            os.remove(file)

    else:
        lock.acquire()

        is_indexed = index_document(r, data['source'], data)

        lock.release()
    if(not is_indexed):
        guardar_dados_ficheiro(data, file)



def index_keywords(key, objeto):
    global r, lock

    try:
        objeto_json = json.dumps(objeto, ensure_ascii=False)

        lock.acquire()

        r.hset("keywords", key, objeto_json)

        lock.release()

    except Exception as e:
        print(f"Erro ao indexar documento no Redis [Keywords]: {e}")


def get_keywords_redis(key):
    try:
        objeto_json = r.hget("keywords", key)
        if objeto_json:
            objeto_dict = json.loads(objeto_json)
            ii = InvertedIndex()
            ii.index = defaultdict(lambda: defaultdict(list), objeto_dict)
            return ii
        else:
            print("Nenhum dado encontrado para a chave fornecida.")
            return InvertedIndex()
    except Exception as e:
        print(f"Erro ao obter documento do Redis [Keywords]: {e}")
        return InvertedIndex()