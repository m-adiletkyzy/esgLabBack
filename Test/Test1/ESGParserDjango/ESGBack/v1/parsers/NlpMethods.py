import string
from pymorphy3 import MorphAnalyzer


morph = MorphAnalyzer()

def lemmatizateWord(word: str):
    if word.isascii():
        return word.lower()
    else:
        return morph.parse(word)[0].normal_form

def lemmatizateText(text: str):
    #Избавимся от знаков пунктуации

    table = str.maketrans(dict.fromkeys(string.punctuation))
    text = text.translate(table)

    # Вернём текст со словами в нормальной форме
    return ' '.join([lemmatizateWord(w) for w in text.split()])
    
