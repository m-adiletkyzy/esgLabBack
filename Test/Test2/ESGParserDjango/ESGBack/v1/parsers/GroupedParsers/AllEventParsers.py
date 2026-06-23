from v1.parsers.AddtoDb import AddEvent, addError

def Parse_Events():
    try:
        print('Парсинг AtamekenKz/ru/ Мероприятия')
        from v1.parsers.ParsingScripts.EventParsers.AtamekenKzEventParser import Parse_AtamekenKzRuEvents
        AddEvent(Parse_AtamekenKzRuEvents())
    except Exception as e:
        print(e)
        addError('Парсинг AtamekenKz/ru/ Мероприятия', e)

    try:
        print('Парсинг ESGnewscom/ru/ Мероприятия')
        from v1.parsers.ParsingScripts.EventParsers.EsgNewsComEventParser import Parse_EsgnewscomRuEvents
        AddEvent(Parse_EsgnewscomRuEvents())
    except Exception as e:
        print(e)
        addError('Парсинг ESGnewscom/ru/ Мероприятия', e)