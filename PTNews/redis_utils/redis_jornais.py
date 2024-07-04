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


# Função para obter os dados do Redis
def obter_dados_jornais(query):
    global r
    try:
            temp = []
            data = r.ft("jornais").search(query).docs
            
            for noticia in data:
                temp.append({
                    'source': noticia['source'],
                    'id': noticia['id'],
                    'title': noticia['title'],
                    'url': noticia['url'],
                    'lead': json.loads(noticia['lead']),
                    'content': json.loads(noticia['content']),
                    'images': json.loads(noticia['images']),
                    'published': noticia['published'],
                    'authors': json.loads(noticia['authors']),
                    'tags': json.loads(noticia['tags']),
                    'keywords': json.loads(noticia['keywords']),
                    'entities': json.loads(noticia['entities']),
                    'sentiment': json.loads(noticia['sentiment'])
                })
            
            return temp
    except Exception as e:
            print(f"Erro ao obter os dados no Redis: {e}")
            return []


# Função para obter o número de notícias de uma dada query
def obter_num_noticias(query):
    global r

    try:
            num = r.ft("jornais").search(query).total
            return num
    except Exception as e:
            print(f"Erro ao obter os dados no Redis: {e}")
            return 0