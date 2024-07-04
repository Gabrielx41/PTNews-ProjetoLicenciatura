from datetime import datetime
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="agent")
from gmplot import gmplot
import codecs
from pytrends.request import TrendReq
from wordcloud import WordCloud
from yake.highlight import TextHighlighter

def to_timestamp(date_str):
    data_formatada = datetime.strptime(date_str, "%d/%m/%Y %H:%M")
    return data_formatada.timestamp()

def to_date(timestamp):
    timestamp = int(float(timestamp))  # Convert the timestamp to a float and then to an integer
    return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M")

def ordenar(ordem, query):
    match ordem:
        case 'asc':
            return query.sort_by('published', True)
        case 'desc':
            return query.sort_by('published', False)
        case _:
            return query
        
def get_coordenadas(cidades):
    ListOfLatitudes = []
    ListOfLongitudes = []
    ListOfNames = []

    for location in cidades:
        location = geolocator.geocode(location)
        if location:
            ListOfLatitudes.append(location.latitude)
            ListOfLongitudes.append(location.longitude)
            address = location.address.split(",")
            ListOfNames.append((address[0] + ", " + address[1]) if len(address) > 1 else address[0])
    return ListOfLatitudes, ListOfLongitudes, ListOfNames


def map_plotter(ListOfLatitudes, ListOfLongitudes, ListOfNames):
    if ListOfLatitudes and ListOfLongitudes and ListOfNames:
        gmap = gmplot.GoogleMapPlotter(39.5, -8, 4)

        # Adiciona os pontos com nomes das cidades
        for lat, lon, name in zip(ListOfLatitudes, ListOfLongitudes, ListOfNames):
            gmap.marker(lat, lon, title=name, info_window=name, color='cornflowerblue')
            
        map_file = "C:/Users/35193/OneDrive/Ambiente de Trabalho/3 ano/Projeto/PTNewsAnalyzer/PTNews/templates/NoticiaMap.html"

        with codecs.open(map_file, 'w', 'utf-8') as f:
            # Escreve o conteúdo HTML
            f.write(gmap.get())

def get_top_topics(num_topics):
    pytrends = TrendReq(hl='pt-PT', tz=360)

    trending_searches_df = pytrends.trending_searches(pn='portugal')

    top_trending = trending_searches_df.head(num_topics)

    top_words = top_trending[0].tolist()
    
    return top_words

def normalize_scores(keywords):
    if len(keywords) == 0:
        return {}

    values = list(keywords.values())
    max_value = max(values)
    min_value = min(values)

    result = {}
    for key, value in keywords.items():
        if (max_value - min_value) == 0:
            normalized_score = 0
        else:
            normalized_score = (value - min_value) / (max_value - min_value)
        result[key] = normalized_score

    return result

def criar_wordcloud(keyword2WordCloud):
    colormap = 'Blues'
    wordcloud = WordCloud(
        width=1200, 
        height=700,
        max_font_size=100,
        max_words=25,
        background_color='white',
        colormap=colormap,
    ).generate_from_frequencies(keyword2WordCloud)
    
    image = wordcloud.to_image()
    image.save("C:/Users/35193/OneDrive/Ambiente de Trabalho/3 ano/Projeto/PTNewsAnalyzer/PTNews/static/images/wordcloud.png")
    
def get_content_highlighter(texto, keywords):
    # Remove espaços em branco no início do texto e substitui \n por <br>
    texto = texto.lstrip('\n')
    texto = texto.replace('\n\n', '<br>')
    texto = texto.replace('\n', '<br><br>')
    
    th = TextHighlighter(max_ngram_size = 3, highlight_pre = "<b class='keywordContent'>", highlight_post= "</b>")
    content = th.highlight(texto, keywords)
    return content