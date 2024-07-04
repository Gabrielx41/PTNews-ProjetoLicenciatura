import justext
from ..Request.request import request
from bs4 import BeautifulSoup


def get_texto_noticias(url):
    texto = ""
    try:
        response = request(url)
        paragraphs = justext.justext(response.content, justext.get_stoplist("Portuguese"))
        for paragraph in paragraphs:
            if not paragraph.is_boilerplate:
                texto += paragraph.text + "\n"
    except:
        print(f"Erro na extração de texto: {url}")
    return texto

def get_content_DNoticias(url):
    texto = ""
    
    try:
        response = request(url)
        content = response.content
                    
        soup = BeautifulSoup(content, "html.parser")
        texto = soup.find("div", {"class": "article--body"}).text
    except:
        print(f"Erro na extração de texto: {url}")

    return texto


def get_lead(url):
    lead = ""
    try:
        response = request(url)
        content = response.content
            
        soup = BeautifulSoup(content, "html.parser")
        lead = soup.find("div", {"class": "article-excerpt"}).text
    except:
        print(f"Erro na extração de lead: {url}")
    
    return lead