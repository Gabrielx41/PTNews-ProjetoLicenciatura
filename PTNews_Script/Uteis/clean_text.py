from bs4 import BeautifulSoup
from cleantext import clean
import re

def clean_text(texto):
    try:
        #Remover HTML
        soup = BeautifulSoup(texto, "html.parser")
        texto = soup.get_text()
        
        #Remover emails e emojis
        texto = clean(
                    texto,
                    to_ascii=False,                # Texto com acentos
                    lower=False,                   # Texto com maiusculas e minusculas
                    no_line_breaks=False,           # Não remover quebras de linha
                    no_emails=True,                # Evitar que apareçam emails no texto (aparecem quando há "plavras clicáveis")
                    replace_with_email="",
                    no_emoji=True,                 # Remover emojis
                )

        #Remove caracteres especiais
        texto = texto.translate(str.maketrans('', '', '*_[{]}#▲'))
        
        texto = texto.replace("\n0\n", "\n")
        
        return texto
    
    except:
        return None

    
def remover_texto_content(texto, jornal, titulo):
    try:
        match jornal:
            case "Público":
                texto = texto.replace("Os leitores são a força e a vida do jornal\nO contributo do PÚBLICO para a vida democrática e cívica do país reside na força da relação que estabelece com os seus leitores.Para continuar a ler este artigo assine o PÚBLICO.Ligue - nos através do 808 200 095 ou envie-nos um email para . ", "")

            case "Expresso":
                texto = texto.replace("Artigo Exclusivo para subscritores Subscreva já por apenas 1,73€ por semana. Já é Subscritor? Comprou o Expresso?Insira o código presente na Revista E para continuar a ler", "")
                texto = texto.replace(titulo + "\n", "")
                texto = texto.replace("Já é Subscritor?\nComprou o Expresso?Insira o código presente na Revista E para continuar a ler", "")

            case "JNegocios":
                texto = texto.replace("Funcionalidade exclusiva para assinantes Negócios Premium\n", "")

            case "NAM":
                texto = re.sub(r'\nLeia Também:.*', "", texto)

            case "Observador":
                texto = texto.replace("Se 1% dos nossos leitores assinasse o Observador, conseguiríamos aumentar ainda mais o nosso investimento no escrutínio dos poderes públicos e na capacidade de explicarmos todas as crises – as nacionais e as internacionais.\nHoje como nunca é essencial apoiar o jornalismo independente para estar bem informado.\nTorne-se assinante a partir de 0,18€/ dia.", "")
                texto = texto.replace("PUB • CONTINUE A LER A SEGUIR\n", "")
                texto = texto.replace("Partilhar artigo\n", "")

            case "Renascenca":
                texto = texto.replace("Tem 1500 caracteres disponíveis Todos os campos são de preenchimento obrigatório.\nTermos e Condições Todos os comentários são mediados, pelo que a sua publicação pode demorar algum tempo. Os comentários enviados devem cumprir os critérios de publicação estabelecidos pela direcção de Informação da Renascença: não violar os princípios fundamentais dos Direitos do Homem; não ofender o bom nome de terceiros; não conter acusações sobre a vida privada de terceiros; não conter linguagem imprópria. Os comentários que desrespeitarem estes pontos não serão publicados.", "")

            case "DNoticias":
                texto = texto.replace("Download App\n" , "")
                texto = texto.replace(titulo + "\n", "")
                
            case "Eco":
                texto = texto.replace("Nota: Este texto faz parte da newsletter Semanada, enviada para os subscritores à sexta-feira, assinada por André Veríssimo. Há muito mais para ler. Pode subscrever neste link(https://eco.sapo.pt/newsletters/).", "")
    except:
        texto = None
    
    return texto


def remover_lead_title(lead, content, title):
    
    try:
        content = content.replace(title, "")
        content = content.replace(lead, "")
        
        return content
    except:
        return None