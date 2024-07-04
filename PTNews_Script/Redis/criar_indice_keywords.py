import redis
from dotenv import load_dotenv
from redis.commands.search.field import TextField
import os

load_dotenv(override=True)

r = redis.Redis(
    host=os.getenv("HOST_REDIS"),
    port=int(os.getenv("PORT_REDIS")),
    decode_responses=True
)

# Definir os campos para criar o índice de palavras-chave
keyword_index_name = 'keywords'

keyword_fields = [
    TextField(name="keywords")
]

def create_keyword_index(r, index_name, fields):
    try:
        # check if index exists
        r.ft(index_name).info()
        print("Index already exists!")
    except:
        # create index
        r.ft(index_name).create_index(fields=fields)
        print("Index created")

create_keyword_index(r, keyword_index_name, keyword_fields)
