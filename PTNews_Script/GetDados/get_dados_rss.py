import feedparser

#Vai buscar os dados do RSS
def get_dados_RSS(url_rss):
    try:
        content = feedparser.parse(url_rss)
        return content
    except:
        print(f"Erro ao obter dados: {url_rss}")
        return []