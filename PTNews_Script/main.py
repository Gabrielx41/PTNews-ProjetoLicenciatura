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
                    try:
                        publico(novos_dados, ultimo_id, jornal)
                    except Exception as e:
                        print("Público erro main: " + e)
                    
                
                sleep(1200) # 20 minutos
                
                
        case "Eco":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_API(url)
                if novos_dados:
                    try:
                        eco(novos_dados, ultimo_id, jornal)
                    except Exception as e:
                        print("Eco erro main: " + e)
                    
                
                sleep(600) # 10 minutos
                
                
        case "Observador":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_API(url)
                if novos_dados:
                    try:
                        observador(novos_dados, ultimo_id, jornal)
                    except Exception as e:
                        print("Observador erro main: " + e)
                          
                  
                sleep(7200) # 2 horas
                
                
    ############################## RSS ##############################

        case "Expresso":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_RSS(url)
                if novos_dados:
                    try:
                        expresso(novos_dados, ultimo_id, jornal)
                    except Exception as e:
                        print("Expresso erro main: " + e)
                    
                
                sleep(1200) # 20 minutos


        case "IOnline":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_RSS(url)
                if novos_dados:
                    try:
                        ionline(novos_dados, ultimo_id, jornal)
                    except Exception as e:
                        print("IOnline erro main: " + e)
                    
                
                sleep(3600) # 1 hora


        case "NAM":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_RSS(url)
                if novos_dados:
                    try:
                        nam(novos_dados, ultimo_id, jornal)
                    except Exception as e:
                        print("NAM erro main: " + e)
                        
                
                sleep(300) # 5 minutos


        case "DNoticias":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_RSS(url)
                if novos_dados:
                    try:
                        dnoticias(novos_dados, ultimo_id, jornal)
                    except Exception as e:
                        print("DNoticias erro main: " + e)
                          
                                  
                sleep(3600) # 1 hora


        case "JNegocios":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_RSS(url)
                if novos_dados:
                    try:
                        jnegocios(novos_dados, ultimo_id, jornal)
                    except Exception as e:
                        print("JNegocios erro main: " + e)
                        
                    
                sleep(1500) # 25 minutos


        case "Renascenca":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_RSS(url)
                if novos_dados:
                    try:
                        renascenca(novos_dados, ultimo_id, jornal)
                    except:
                        print("Renascença erro main: " + e)
                             
                               
                sleep(900) # 15 minutos


        case "Sapo24":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_RSS(url)
                if novos_dados:
                    try:
                        sapo24(novos_dados, ultimo_id, jornal)
                    except:
                        print("Sapo24 erro main: " + e)
                    
                
                sleep(1500) # 25 minutos


        case "SicNoticias":
            while(verifica_token(file_token)):
                
                novos_dados = get_dados_RSS(url)
                if novos_dados:
                    try:
                        sicnoticias(novos_dados, ultimo_id, jornal)
                    except:
                        print("SicNotícias erro main: " + e)
                            
                
                sleep(900) # 15 minutos

    print("Fim do programa: " + jornal)
    escrever_ficheiro_txt("PTNews_Script/UltimosID/" + jornal + ".txt", ultimo_id[jornal])
