import re
# Expressão regular para extrair o número da URL
numero_regex = r"/(\d+)/"

def get_num_link(url):
    global numero_regex

    # Procurar pelo número na URL
    match = re.search(numero_regex, url)

    # Verificar se encontrou o número na URL
    if match:
        numero = match.group(1)
        return numero
    else:
        return url
