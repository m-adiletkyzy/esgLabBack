from v1.parsers.AddtoDb import AddProjects, addError



def Parse_Projects():
    try:
        print('Парсинг RecycleKz/ru/ Проекты')
        from v1.parsers.ParsingScripts.ProjectParsers.RecycleKzParser import Parse_ResycleKzRuProject
        AddProjects(Parse_ResycleKzRuProject())
    except Exception as e:
        print(e)
        addError('Парсинг RecycleKz/ru/ Проекты', e)

    try:
        print('Парсинг ESGAru/ru/ Проекты')
        from v1.parsers.ParsingScripts.ProjectParsers.EsgAruParser import Parse_EsgAruProject
        AddProjects(Parse_EsgAruProject())
    except Exception as e:
        print(e)
        addError('Парсинг ESGAru/ru/ Проекты', e)
