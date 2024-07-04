import redis
from dotenv import load_dotenv
from redis.commands.search.indexDefinition import IndexDefinition
from redis.commands.search.field import TextField, NumericField
import os

load_dotenv(override=True)

r = redis.Redis(
                 host = os.getenv("HOST_REDIS"), 
                 port = int(os.getenv("PORT_REDIS")),
                 decode_responses=True
                )

#Definir os campos para criar o índice
index_name = 'jornais'

doc_prefix = ['DNoticias:','Público:', 'IOnline:', 'Eco:','Expresso:','JNegocios:','NAM:','Observador:','Renascenca:','Sapo24:','SicNoticias:']

source = TextField(name="source")
id = TextField(name="id")
title = TextField(name="title")
url = TextField(name="url")
lead = TextField(name="lead")
content = TextField(name="content")
images = TextField(name="images")
published = NumericField(name="published")
authors = TextField(name="authors")
tags = TextField(name="tags")
keywords = TextField(name="keywords")
entities = TextField(name="entities")
sentiment = TextField(name="sentiment")

fields = [source, id, title, url, lead, content, images, published, authors, tags, keywords, entities, sentiment]

def create_index(r, index_name, doc_prefix, fields):    
    try:
        #  check if index exists
        r.ft(index_name).info()
        print("Index already exists!")
    except:
        #create index
        r.ft(index_name).create_index(fields=fields, definition=IndexDefinition(prefix=doc_prefix))
        print("Index created")

create_index(r, index_name, doc_prefix, fields)