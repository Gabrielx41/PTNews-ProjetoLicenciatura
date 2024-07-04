sentilex = {}

# Extrair a informação do ficheiro e guardar no dicionário ('palalvra' : polaridade) 1->positivo, 0->neutro, -1->negativo
with open('PTNews_Script/Sentimentos/SentiLex-flex-PT02.txt', 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split(';')
        words = parts[0].split(',')
        polarity = int(parts[3].split('=')[1])  # Extrair a polaridade
        
        for word in words:
            sentilex[word] = polarity

# Função para calcular a polaridade de um texto (média das polaridades das palavras)
def calculate_text_polarity(text):
    global sentilex
    total_polarity = 0
    
    words = text.split()
    
    # Obter a polaridade de cada palavra, se não existir, é neutra (0)
    for word in words:
        total_polarity = total_polarity + sentilex.get(word.lower(), 0) 
    
    return total_polarity / len(words) if words else 0


def sentiment_analysis(text):
    polarity = calculate_text_polarity(text)

    if polarity > 0:
        return "Positivo"
    elif polarity < 0:
        return "Negativo"
    else:
        return "Neutro"
