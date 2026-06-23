from v1.parsers.NlpMethods import lemmatizateText

ru_keywords = ['ESG', 'устойчивое развитие']
ru_keywords = [lemmatizateText(w) for w in ru_keywords]

def isESGRu(text:str):
    text = lemmatizateText(text)

    for w in ru_keywords:
        if w in text: return True

    return False

