from ..Redis.redis import get_keywords_redis, guardar_dados, index_keywords
from ..Uteis.uteis import to_date, exist, getLead
from ..Uteis.clean_text import clean_text, remover_lead_title
from ..Uteis.keywords import get_keywords, get_keywords_1gram
from ..Uteis.entidades import get_entidades
from ..Sentimentos.sentiment_analysis_tradutor import sentiment_analysis
from ..Uteis.clean_text import remover_texto_content

def eco(novos_dados, ultimo_id, jornal):
    if(novos_dados):
        
        for dados in novos_dados:
            if(ultimo_id[jornal] != str(dados['id'])):

                authors = []
                try:
                    for autor in dados['metadata']['contributors']:
                        authors.append({
                                        'name': exist(autor['name'], autor['name']),
                                        'image': autor['image']['urlTemplate'] if autor['image'] else None
                                        })
                except:
                    authors = None

                try:
                    existImage = dados['images']['square']
                except:
                    existImage = False
                            
                lead = exist(clean_text(dados['lead']), dados['lead'])
                
                title = clean_text(dados['title']['long'])
                
                try:
                    content = remover_texto_content(clean_text(dados['body']), jornal, title)
                except:
                    content = None
                
                if not lead:
                    lead = getLead(content)

                newContent = remover_lead_title(lead, content, title)
                
                content = newContent if newContent else content

                keywords = get_keywords(content)
                            
                entities = get_entidades(content)

                dictDados = {
                            'source': jornal,
                            'id': str(dados['id']),
                            'title': title,
                            'url': dados['links']['webUri'],
                            'lead': lead,
                            'content': exist(content, content),
                            'images': [{
                                        'url': dados['images']['square']['urlTemplate'] if existImage else None,
                                        'credits': dados['images']['square']['credit'] if existImage else None
                                        }],
                            'published': to_date(dados['lastModified']),
                            'authors': authors,
                            'tags': [tag['webTitle'] for tag in dados['metadata']['tags']] if dados['metadata']['tags'] else None,
                            'keywords': exist(keywords, keywords),
                            'entities': entities,
                            'sentiment': sentiment_analysis(title)
                            }
                
                guardar_dados(dictDados)
                
                keywords = get_keywords_1gram(content)

                ii_coccur = get_keywords_redis("keywords")
                ii_coccur.update(content, keywords)
                index_keywords("keywords", ii_coccur.get_index())
                
            else:
                ultimo_id[jornal] = str(novos_dados[0]['id'])
                break
                        
        ultimo_id[jornal] = str(novos_dados[0]['id'])