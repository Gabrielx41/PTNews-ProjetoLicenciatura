import yake

def normalize_scores(keywords):
    if len(keywords) == 0:
        return {}
    max_value = max([item[1] for item in keywords])
    min_value = min([item[1] for item in keywords])

    result = {}
    for item in keywords:
        if (float(max_value) - float(min_value)) == 0:
            normalized_score = 0
        else:
            normalized_score = (item[1] - float(min_value))/(float(max_value) - float(min_value))
        # result[item[0]] = abs(1 - normalized_score)
        result[item[0]] = round(abs(1 - normalized_score), 2)

    return result

def get_keywords(texto):
    language = "pt"
    max_ngram_size = 3
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 10
    
    try:
        kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
        keywords = kw_extractor.extract_keywords(texto)
    except:
        return {}

    return normalize_scores(keywords)


def get_keywords_1gram(text):
    max_ngram_size = 1
    language = "pt"
    numOfKeywords = 3
    ListOfKeywords = []
    try:
        custom_kw_extractor = yake.KeywordExtractor(lan = language, n = max_ngram_size, top = numOfKeywords)
        keywords = custom_kw_extractor.extract_keywords(text)
        ListOfKeywords = [kw[0] for kw in keywords]
    except Exception as e:
        print(e)


    return ListOfKeywords