from v1.parsers.AddtoDb import AddNews
def Parse_News():
    try:
        print('Парсинг Esgnewscom Ru Новости')
        from v1.parsers.NewsParsers.EsgnewscomParser import Parse_EsgnewscomRuNews, Parse_EsgnewscomEnNews
        AddNews(Parse_EsgnewscomRuNews())
    except Exception as e:
        print(e)

    try:
        print('Парсинг Esgnewscom En News')
        AddNews(Parse_EsgnewscomEnNews())
    except Exception as e:
        print(e)

    try:
        print('Парсинг Govkznews Ru Новости')
        from v1.parsers.NewsParsers.GovkznewsParser import Parse_GovkznewsRu, Parse_GovkznewsKz
        AddNews(Parse_GovkznewsRu())
    except Exception as e:
        print(e)
    
    try:
        print('Парсинг Govkznews Kz Новости')
        AddNews(Parse_GovkznewsKz())
    except Exception as e:
        print(e)
    
    try:
        print('Парсинг Informkz Ru Новости')
        from v1.parsers.NewsParsers.InformkzParser import Parse_informkzRuNews
        AddNews(Parse_informkzRuNews())
    except Exception as e:
        print(e)

    try:
        print('Парсинг Esgtoday En Новости')
        from v1.parsers.NewsParsers.EsgtodayParser import Parse_EsgtodayNews
        AddNews(Parse_EsgtodayNews())
    except Exception as e:
        print(e)