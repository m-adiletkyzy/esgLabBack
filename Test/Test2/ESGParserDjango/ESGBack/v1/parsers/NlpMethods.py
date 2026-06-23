import os
import string
from pymorphy3 import MorphAnalyzer
from .kaznlp.morphology.analyzers import AnalyzerDD


morph = MorphAnalyzer()
analyzer = AnalyzerDD()
analyzer.load_model(os.path.join(os.path.dirname(__file__), 'kaznlp', 'morphology', 'mdl'))

def lemmatizateRuWord(word: str):
    if word.isascii():
        return word
    else:
        return morph.parse(word)[0].normal_form

def lemmatizateKzWord(word: str):
    if word.isascii():
        return word.lower()
    else:
        [iscovered, alist] = analyzer.analyze(word)
        lword = alist[0]
        return lword[:lword.find('_')]

def lemmatizateText(text: str, lang):
    #Избавимся от знаков пунктуации

    table = str.maketrans(dict.fromkeys(string.punctuation))
    text = text.translate(table)

    if lang == 'ru':
        # Вернём текст со словами в нормальной форме
        return ' '.join([lemmatizateRuWord(w) for w in text.split()])
    elif lang == 'kk':
        return ' '.join([lemmatizateKzWord(w) for w in text.split()])

def txt_to_list(text):
    return [line.strip() for line in text.strip().splitlines() if line.strip()]

class KeywordsFiltration:
    def __init__(self, lang):
        if lang == 'ru':
            path = os.path.join(os.path.dirname(__file__), 'KeyWordFiles', 'RuEsgKeywords.txt')
        elif lang == 'kk':
            path = os.path.join(os.path.dirname(__file__), 'KeyWordFiles', 'KzEsgKeywords.txt')
        self.keywords = txt_to_list(open(path, 'r', encoding='utf-8').read())

    def EsgKeyWordCheck(self, text, lang):
        text = lemmatizateText(text, lang)
        return any([kw in text for kw in self.keywords])


    
