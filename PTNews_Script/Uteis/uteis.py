from dateutil import parser

#Função para verificar se um valor existe, se existir retorna o valor, se não existir retorna None
def exist(dados, condicao):
    return dados if condicao else None


#Converter para formato date que é aceitável no redis
def to_date(data):
    # Converter a string em um objeto de data e hora
    data_obj = parser.parse(data)
    
    # Obter o timestamp
    timestamp = data_obj.timestamp()
    
    return timestamp

def getLead(content):
    try:
        lines = content.split('.')
        modified_content = '.'.join(lines[0:3]) + '.'
    except:
        modified_content = content
        
    return modified_content