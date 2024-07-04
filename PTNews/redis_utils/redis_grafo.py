import os
import redis
from dotenv import load_dotenv
import json
from collections import defaultdict
from .InvertedIndex import InvertedIndex

load_dotenv(override=True)

r = redis.Redis(
                 host = os.getenv("HOST_REDIS"), 
                 port = int(os.getenv("PORT_REDIS")),
                 decode_responses=True
                )

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