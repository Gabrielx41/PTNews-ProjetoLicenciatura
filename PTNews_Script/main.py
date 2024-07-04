from .GetDados.get_dados_api import get_dados_API
from .GetDados.get_dados_rss import get_dados_RSS
from .Jornais.publico import publico
from .Jornais.eco import eco
from .Jornais.observador import observador
from .Jornais.ionline import ionline
from .Jornais.expresso import expresso
from .Jornais.nam import nam
from .Jornais.dnoticias import dnoticias
from .Jornais.jnegocios import jnegocios
from .Jornais.renascenca import renascenca
from .Jornais.sapo24 import sapo24
from .Jornais.sicnoticias import sicnoticias
from .Ficheiros.ficheiros_txt import verifica_token, ler_ficheiro_txt, escrever_ficheiro_txt
from time import sleep


ultimo_id = {
            ############# API #############
    "Público": "",
    "Observador": "",
    "Eco": "",
            ############# RSS #############
    "IOnline": "",
    "Expresso": "",
    "NAM": "",
    "DNoticias": "",
    "JNegocios": "",
    "Renascenca": "",
    "Sapo24": "",
    "SicNoticias": ""
}


file_token = "PTNews_Script/Token/token.txt"


def main(jornal, url):
    global ultimo_id, file_token
    
    ultimo_id[jornal] = ler_ficheiro_txt("PTNews_Script/UltimosID/" + jornal + ".txt")

    match jornal:
    ############################## API ##############################
    
        case "Público":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_API(url)
                if novos_dados:
                    publico(novos_dados, ultimo_id, jornal)
                    
                
                sleep(1200) # 20 minutos
                
                
        case "Eco":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_API(url)
                if novos_dados:
                    eco(novos_dados, ultimo_id, jornal)
                    
                
                sleep(600) # 10 minutos
                
                
        case "Observador":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_API(url)
                if novos_dados:
                    observador(novos_dados, ultimo_id, jornal)
                          
                  
                sleep(7200) # 2 horas
                
                
    ############################## RSS ##############################

        case "Expresso":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_RSS(url)
                if novos_dados:
                    expresso(novos_dados, ultimo_id, jornal)
                    
                
                sleep(1200) # 20 minutos


        case "IOnline":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_RSS(url)
                if novos_dados:
                    ionline(novos_dados, ultimo_id, jornal)
                    
                
                sleep(3600) # 1 hora


        case "NAM":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_RSS(url)
                if novos_dados:
                    nam(novos_dados, ultimo_id, jornal)
                        
                
                sleep(300) # 5 minutos


        case "DNoticias":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_RSS(url)
                if novos_dados:
                    dnoticias(novos_dados, ultimo_id, jornal)
                          
                                  
                sleep(3600) # 1 hora


        case "JNegocios":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_RSS(url)
                if novos_dados:
                    jnegocios(novos_dados, ultimo_id, jornal)
                        
                    
                sleep(1500) # 25 minutos


        case "Renascenca":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_RSS(url)
                if novos_dados:
                    renascenca(novos_dados, ultimo_id, jornal)
                             
                               
                sleep(900) # 15 minutos


        case "Sapo24":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_RSS(url)
                if novos_dados:
                    sapo24(novos_dados, ultimo_id, jornal)
                    
                
                sleep(1500) # 25 minutos


        case "SicNoticias":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_RSS(url)
                if novos_dados:
                    sicnoticias(novos_dados, ultimo_id, jornal)
                            
                
                sleep(900) # 15 minutos

    print("Fim do programa: " + jornal)
    escrever_ficheiro_txt("PTNews_Script/UltimosID/" + jornal + ".txt", ultimo_id[jornal])
