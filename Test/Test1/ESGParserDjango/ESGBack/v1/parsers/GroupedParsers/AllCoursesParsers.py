from v1.parsers.AddtoDb import AddCourses


def Parse_Courses():
    try:
        print('Парсинг SustainabilityKzRu Курсы')
        from v1.parsers.ParsingScripts.CourseParsers.SustainabilityKzCourseParser import Parse_SustainabilityKzRuCourse
        AddCourses(Parse_SustainabilityKzRuCourse())
    except Exception as e:
        print(e)

    try:
        print('Парсинг EyacademyRu Курсы')
        from v1.parsers.ParsingScripts.CourseParsers.EyacademyccaComCourseParser import Parse_EyacademyRuCourses
        AddCourses(Parse_EyacademyRuCourses())
    except Exception as e:
        print(e)

    try:
        print('Парсинг CsdCenterKzRu Курсы')
        from v1.parsers.ParsingScripts.CourseParsers.CsdCenterKzCourseParser import Parse_CsdCenterKzRuCourses
        AddCourses(Parse_CsdCenterKzRuCourses())
    except Exception as e:
        print(e)

