import threading
from .main import main


def iniciar():
    # Lista de tuplas contendo informações sobre cada jornal
    jornais = [
        ("Público", "https://www.publico.pt/api/list/ultimas"),
        ("Eco", "https://eco.sapo.pt/wp-json/eco/v1/items"),
        ("Observador", "https://observador.pt/wp-json/obs_api/v4/news/widget"),
        ("IOnline", "https://feeds.feedburner.com/i-ultimas"),
        ("Expresso", "https://feeds.feedburner.com/expresso-geral"),
        ("NAM", "https://www.noticiasaominuto.com/rss/ultima-hora"),
        ("DNoticias", "https://www.dnoticias.pt/rss/pais.xml"),
        ("JNegocios", "https://www.jornaldenegocios.pt/rss"),
        ("Renascenca", "https://rr.sapo.pt/rss/rssfeed.aspx?section=section_noticias"),
        ("Sapo24", "https://24.sapo.pt/rss"),
        ("SicNoticias", "https://feeds.feedburner.com/sicnoticias-ultimas")
    ]

    threads = []

    for jornal, url in jornais:
        # Criar uma thread para cada jornal
        thread = threading.Thread(target=main, args=(jornal, url))
        threads.append(thread)
        thread.start()

    # Aguardar todas as threads terminarem
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    iniciar()