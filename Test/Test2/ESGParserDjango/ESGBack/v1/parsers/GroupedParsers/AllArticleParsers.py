from v1.parsers.AddtoDb import AddArticle

from v1.parsers.AddtoDb import addError


def Parse_Articles():
    try:
        print('Парсинг Esgnewscom Ru Новости')
        from v1.parsers.ParsingScripts.ArticleParsers.ESGonlyParsers.Aparsers0_10.EsgnewscomParser import Parse_EsgnewscomRuNews, Parse_EsgnewscomEnNews
        AddArticle(Parse_EsgnewscomRuNews())
    except Exception as e:
        print(e)
        addError('Парсинг Esgnewscom Ru Новости', e)

    try:
        print('Парсинг Esgnewscom En News')
        AddArticle(Parse_EsgnewscomEnNews())
    except Exception as e:
        print(e)
        addError('Парсинг Esgnewscom En News', e)

    try:
        print('Парсинг KaseKz Ru Новости')
        from v1.parsers.ParsingScripts.ArticleParsers.ESGonlyParsers.Aparsers0_10.KasekzParser import Parse_KaseKzRuNews
        AddArticle(Parse_KaseKzRuNews())
    except Exception as e:
        print(e)
        addError('Парсинг KaseKz Ru Новости', e)

    try:
        print('Парсинг PwcCom Ru Новости')
        from v1.parsers.ParsingScripts.ArticleParsers.ESGonlyParsers.Aparsers0_10.PwcСomParser import Parse_PwcComRuNews
        AddArticle(Parse_PwcComRuNews())
    except Exception as e:
        print(e)
        addError('Парсинг PwcCom Ru Новости', e)

    try:
        print('Парсинг KapitalKz Ru Новости')
        from v1.parsers.ParsingScripts.ArticleParsers.ESGonlyParsers.Aparsers0_10.KapitalKz import Parse_KapitalKzRuNews
        AddArticle(Parse_KapitalKzRuNews())
    except Exception as e:
        print(e)
        addError('Парсинг KapitalKz Ru Новости', e)

    try:
        print('Парсинг Forbes Ru Новости')
        from v1.parsers.ParsingScripts.ArticleParsers.ESGonlyParsers.Aparsers0_10.ForbesRu import Parse_ForbesRuNews
        AddArticle(Parse_ForbesRuNews())
    except Exception as e:
        print(e)
        addError('Парсинг Forbes Ru Новости', e)

    try:
        print('Парсинг Govkznews Ru Новости')
        from v1.parsers.ParsingScripts.ArticleParsers.ESGonlyParsers.Aparsers0_10.GovkznewsParser import Parse_GovkznewsRu, Parse_GovkznewsKz
        AddArticle(Parse_GovkznewsRu())
    except Exception as e:
        print(e)
        addError('Парсинг Govkznews Ru Новости', e)

    try:
        print('Парсинг Govkznews Kz Новости')
        AddArticle(Parse_GovkznewsKz())
    except Exception as e:
        print(e)
        addError('Парсинг Govkznews Kz Новости', e)

    try:
        print('Парсинг EsgToday En Новости')
        from v1.parsers.ParsingScripts.ArticleParsers.ESGonlyParsers.OnlyEngSitesParsers0_10.EsgToday import ParseEsgToday
        AddArticle(ParseEsgToday())
    except Exception as e:
        print(e)
        addError('Парсинг EsgToday En Новости', e)

    try:
        print('Парсинг KnowESG En Новости')
        from v1.parsers.ParsingScripts.ArticleParsers.ESGonlyParsers.OnlyEngSitesParsers0_10.KnowESG import ParseKnowESG
        AddArticle(ParseKnowESG())
    except Exception as e:
        print(e)
        addError('Парсинг KnowESG En Новости', e)



def Parse_ToFilterArticlesRu():
    try:
        print('Парсинг TengriNews Ru Новости')
        from v1.parsers.ParsingScripts.ArticleParsers.RuSites.Parsers0_10.TengriNews import ParseTengriNews
        # AddToFilterArticle(ParseTengriNews(), 'ru')
    except Exception as e:
        print(e)
        addError('Парсинг TengriNews Ru Новости', e)

    try:
        print('Парсинг ZakonKz Ru Новости')
        from v1.parsers.ParsingScripts.ArticleParsers.RuSites.Parsers0_10.ZakonKz import ParseZakonKz
        # AddToFilterArticle(ParseZakonKz(), 'ru')
    except Exception as e:
        print(e)
        addError('Парсинг ZakonKz Ru Новости', e)

    try:
        print('Парсинг KursivRu Ru Новости')
        from v1.parsers.ParsingScripts.ArticleParsers.RuSites.Parsers0_10.Kursiv import ParseKursivRu
        # AddToFilterArticle(ParseKursivRu(), 'ru')
    except Exception as e:
        print(e)
        addError('Парсинг KursivRu Ru Новости', e)

    try:
        print('Парсинг InformKz Ru Новости')
        from v1.parsers.ParsingScripts.ArticleParsers.RuSites.Parsers0_10.Inform import ParseInformKzRu
        # AddToFilterArticle(ParseInformKzRu(), 'ru')
    except Exception as e:
        print(e)
        addError('Парсинг InformKz Ru Новости', e)



