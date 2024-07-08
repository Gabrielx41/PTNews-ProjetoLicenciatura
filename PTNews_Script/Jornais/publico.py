from ..Redis.redis import guardar_dados
from ..Uteis.uteis import to_date, exist, getLead
from ..Uteis.clean_text import clean_text, remover_lead_title, remover_texto_content
from ..Uteis.get_content import get_texto_noticias
from ..Uteis.keywords import get_keywords, get_keywords_1gram
from ..Uteis.entidades import get_entidades
from ..Sentimentos.sentiment_analysis_tradutor import sentiment_analysis
from ..Redis.redis import index_keywords, get_keywords_redis


def publico(novos_dados, ultimo_id, jornal):
    if(novos_dados):
        for dados in novos_dados:
            if(ultimo_id[jornal] != str(dados['id'])):

                image = []
                authors = []
                            
                try:
                    for imagem in dados['imagens']:
                        image.append({
                                    'url': exist(imagem['url'], imagem['url']), 
                                    'credits': None
                                    })
                except:
                    image = None

                try:
                    for autor in dados['autores']:
                        authors.append({
                                        'name': exist(autor['nome'], autor['nome']),
                                        'image': autor['imagem']['url'] if autor['imagem'] else None
                                        })
                except:
                    authors = None

                lead = exist(clean_text(dados['descricao']), dados['descricao'])

                title = dados['cleanTitle']

                content = remover_texto_content(clean_text(get_texto_noticias(dados['url'])), jornal, title)

                if not lead:
                    lead = getLead(content)

                newContent = remover_lead_title(lead, content, title)
                
                content = newContent if newContent else content
                
                keywords = get_keywords(content)

                entities = get_entidades(content)

                dictDados = {
                            'source': 'Público',
                            'id': str(dados['id']),
                            'title': title,
                            'url': dados['url'],
                            'lead': lead,
                            'content': exist(content, content),
                            'images': image,
                            'published': to_date(dados['data']),
                            'authors': authors,
                            'tags': [tag['nome'] for tag in dados['tags']] if dados['tags'] else None,
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