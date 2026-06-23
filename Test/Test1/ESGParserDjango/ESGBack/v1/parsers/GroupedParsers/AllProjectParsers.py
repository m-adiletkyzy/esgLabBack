from v1.parsers.AddtoDb import AddProjects


def Parse_Projects():
    try:
        print('Парсинг RecycleKz/ru/ Проекты')
        from v1.parsers.ParsingScripts.ProjectParsers.RecycleKzParser import Parse_ResycleKzRuProject
        AddProjects(Parse_ResycleKzRuProject())
    except Exception as e:
        print(e)