from requests.exceptions import Timeout
from ..Request.request import request

#Vai buscar os dados da API
def get_dados_API(url_api):
    try:
        r = request(url_api)
        content = r.json()
        return content

    except Timeout:
        print(f'Tempo de espera excedido: {url_api}')
        return []
    
    except:
        print(f"Erro ao obter dados: {url_api}")
        return []