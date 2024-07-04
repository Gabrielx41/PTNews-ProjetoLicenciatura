import json

#Função para ler o ficheiro e retornar os dados do ficheiro
def ler_ficheiro_json(file):
    
    try:
        with open(file, 'r', encoding='utf-8') as ficheiro:
            dados = json.load(ficheiro)
            
        return dados
    #Caso não exista o ficheiro, retorna uma lista vazia
    except:
        return []


#Função para guardar os dados no ficheiro
def escrever_ficheiro_json(file, data):
    try:
        with open(file, 'w', encoding='utf-8') as ficheiro:
            json.dump(data, ficheiro, indent = 4, ensure_ascii=False)
    
    except Exception as e:
        print(f"Erro a guardar dados no ficheiro .json: {e}")