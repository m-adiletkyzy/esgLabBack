from v1.parsers.AddtoDb import AddProject


def Parse_Projects():
    # try:
    #     print('Парсинг RecycleKz/ru/ Проекты')
    #     from v1.parsers.ProjectParsers.RecycleKzParser import Parse_ResycleKzRuProject
    #     AddProject(Parse_ResycleKzRuProject())
    # except Exception as e:
    #     print(e)
    
    try:
        print("Парсинг BCC KZ Ru Проекты")
        from v1.parsers.ProjectParsers.BCCParser import Parse_BCCRuProject
        AddProject(Parse_BCCRuProject())
    except Exception as e:
        print(e)
    try:
        print("Парсинг BCC KZ Kz Проекты")
        from v1.parsers.ProjectParsers.BCCParser import Parse_BCCKzProject
        AddProject(Parse_BCCKzProject())
    except Exception as e:
        print(e)
    try:
        print("Парсинг BCC KZ En Проекты")
        from v1.parsers.ProjectParsers.BCCParser import Parse_BCCEnProject
        AddProject(Parse_BCCEnProject())
    except Exception as e:
        print(e)