from v1.parsers.AddtoDb import AddCourses, addError


def Parse_Courses():
    try:
        print('Парсинг SustainabilityKzRu Курсы')
        from v1.parsers.ParsingScripts.CourseParsers.ESGonlyParsers.SustainabilityKzCourseParser import Parse_SustainabilityKzRuCourse
        AddCourses(Parse_SustainabilityKzRuCourse())
    except Exception as e:
        print(e)
        addError('Парсинг SustainabilityKzRu Курсы', e)

    try:
        print('Парсинг EyacademyRu Курсы')
        from v1.parsers.ParsingScripts.CourseParsers.ESGonlyParsers.EyacademyccaComCourseParser import Parse_EyacademyRuCourses
        AddCourses(Parse_EyacademyRuCourses())
    except Exception as e:
        print(e)
        addError('Парсинг EyacademyRu Курсы', e)

    try:
        print('Парсинг CsdCenterKzRu Курсы')
        from v1.parsers.ParsingScripts.CourseParsers.ESGonlyParsers.CsdCenterKzCourseParser import Parse_CsdCenterKzRuCourses
        AddCourses(Parse_CsdCenterKzRuCourses())
    except Exception as e:
        print(e)
        addError('Парсинг CsdCenterKzRu Курсы', e)

def Parse_ToFilterCoursesRu():
    try:
        print('Парсинг Stepic Курсы')
        from v1.parsers.ParsingScripts.CourseParsers.RuSites.Stepic import Parse_StepicCourses
        # AddToFilterCourses(Parse_StepicCourses())
    except Exception as e:
        print(e)
        addError('Парсинг Stepic Курсы', e)

