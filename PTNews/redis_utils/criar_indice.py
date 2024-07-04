import redis
from dotenv import load_dotenv
from redis.commands.search.indexDefinition import IndexDefinition
from redis.commands.search.field import TextField
import os


load_dotenv(override=True)

r = redis.Redis(
                 host = os.getenv("HOST_REDIS"), 
                 port = int(os.getenv("PORT_REDIS")),
                 decode_responses=True
                )

#Definir os campos para criar o índice
index_name = 'users'

doc_prefix = 'User:'

username = TextField(name="username")
salt = TextField(name="salt")
hash = TextField(name="hash")
isAdmin = TextField(name="isAdmin")

fields = [username, salt, hash, isAdmin]

def create_index(r, index_name, doc_prefix, fields):  
    try:
        #  check if index exists
        r.ft(index_name).info()
        print("Index already exists!")
    except:
        #create index
        r.ft(index_name).create_index(fields=fields, definition=IndexDefinition(prefix=[doc_prefix]))
        print("Index created")
        
create_index(r, index_name, doc_prefix, fields)