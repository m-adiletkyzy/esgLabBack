from v1.parsers.AddtoDb import AddEvent


def Parse_Events():
    try:
        print('Парсинг AtamekenKz/ru/ Мероприятия')
        from v1.parsers.EventParsers.AtamekenKzEventParser import (
            Parse_AtamekenKzEnEvents,
            Parse_AtamekenKzKkEvents,
            Parse_AtamekenKzRuEvents,
        )
        AddEvent(Parse_AtamekenKzRuEvents())
    except Exception as e:
        print(e)

    try:
        print('Парсинг AtamekenKz/kk/ Мероприятия')
        AddEvent(Parse_AtamekenKzKkEvents())
    except Exception as e:
        print(e)

    try:
        print('Парсинг AtamekenKz/en/ Мероприятия')
        AddEvent(Parse_AtamekenKzEnEvents())
    except Exception as e:
        print(e)

    try:
        print('Парсинг ESGnewscom/ru/ Мероприятия')
        from v1.parsers.EventParsers.EsgNewsComEventParser import Parse_EsgnewscomRuEvents
        AddEvent(Parse_EsgnewscomRuEvents())
    except Exception as e:
        print(e)

    try:
        print('Парсинг ESGnewscom/en/ Мероприятия')
        from v1.parsers.EventParsers.EsgNewsComEventParser import Parse_EsgnewscomEnEvents
        AddEvent(Parse_EsgnewscomEnEvents())
    except Exception as e:
        print(e)
