def ler_ficheiro_txt(file):
    try:
        with open(file, 'r', encoding='utf-8') as ficheiro:
            dados = ficheiro.read()
        return dados

    except:
        return ""


def escrever_ficheiro_txt(file, data):
    try:
        with open(file, 'w', encoding='utf-8') as ficheiro:
            ficheiro.write(data)

    except Exception as e:
        print(f"Erro a guardar dados no ficheiro .txt: {e}")
        

def verifica_token(file):
    with open(file, "r") as ficheiro:
        token = ficheiro.read()
    if token == "0":
        return True
    else:
        return False