from nltk.sentiment.vader import SentimentIntensityAnalyzer
from googletrans import Translator #pip install googletrans==4.0.0-rc1

def traduzir(texto):
    try:
        translator = Translator()
        traducao = translator.translate(texto, src="pt", dest="en").text
        return traducao
    except Exception as e:
        print(f"Erro ao fazer a tradução: {e}")
        return None


def sentiment_analysis(texto):
    try:
        sia = SentimentIntensityAnalyzer()
        
        sentiment_score = sia.polarity_scores(traduzir(texto))
        score = sentiment_score['compound']
        if(score <= -0.05):
            return "Negativo"
        elif(score >= 0.05):
            return "Positivo"
        else:
            return "Neutro"
    except:
        print("Erro na análise de sentimentos")
        return None