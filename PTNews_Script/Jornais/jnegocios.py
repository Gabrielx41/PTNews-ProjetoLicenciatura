from ..Redis.redis import get_keywords_redis, guardar_dados, index_keywords
from ..Uteis.uteis import to_date, exist, getLead
from ..Uteis.clean_text import clean_text, remover_lead_title, remover_texto_content
from ..Uteis.get_content import get_texto_noticias
from ..Uteis.keywords import get_keywords, get_keywords_1gram
from ..Uteis.entidades import get_entidades
from ..Sentimentos.sentiment_analysis_tradutor import sentiment_analysis


def jnegocios(novos_dados, ultimo_id, jornal):
    if(novos_dados):

        for dados in novos_dados['entries']:
            if(ultimo_id[jornal] != dados['id']):
                authors = []
                author = ""
                image = []
                            
                try:
                    for imagem in dados['links']:
                        if(imagem['rel'] == 'enclosure'):
                            image.append({
                                        'url': exist(imagem['href'], imagem['href']), 
                                        'credits': None
                                        })
                except:
                    image = None
                                
                try:
                    for autor in dados['authors']:
                        if autor['name'] != author:
                            authors.append({
                                            'name': exist(autor['name'], autor['name']),
                                            'image': None
                                            })
                        author = autor['name']
                except:
                    authors = None
                                
                lead = exist(clean_text(dados['summary']), dados['summary'])
                            
                title = clean_text(dados['title'])

                content = remover_texto_content(clean_text(get_texto_noticias(dados['link'])), jornal, title)
                            
                if not lead:
                    lead = getLead(content)
                           
                newContent = remover_lead_title(lead, content, title)
                
                content = newContent if newContent else content
                            
                keywords = get_keywords(content)
                       
                entities = get_entidades(content)
 
                dictDados = {
                            'source': jornal,
                            'id': dados['id'],
                            'title': title,
                            'url': dados['link'],
                            'lead': lead,
                            'content': exist(content, content),
                            'images': image,
                            'published': to_date(dados['published']),
                            'authors': authors,
                            'tags': [tag['term'] for tag in dados['tags']] if dados['tags'] else None,
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
                ultimo_id[jornal] = novos_dados['entries'][0]['id']
                break
                        
        ultimo_id[jornal] = novos_dados['entries'][0]['id']