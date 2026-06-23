from v1.parsers.AddtoDb import AddCourse


def Parse_Courses():
    try:
        print('Парсинг SustainabilityKzRu Курсы')
        from v1.parsers.CourseParsers.SustainabilityKzCourseParser import Parse_SustainabilityKzRuCourse
        AddCourse(Parse_SustainabilityKzRuCourse())
    except Exception as e:
        print(e)

    try:
        print('Парсинг EyacademyRu Курсы')
        from v1.parsers.CourseParsers.EyacademyccaComCourseParser import (
            Parse_EyacademyEnCourses,
            Parse_EyacademyKkCourses,
            Parse_EyacademyRuCourses,
        )
        AddCourse(Parse_EyacademyRuCourses())
    except Exception as e:
        print(e)

    try:
        print('Парсинг EyacademyKk Курсы')
        AddCourse(Parse_EyacademyKkCourses())
    except Exception as e:
        print(e)

    try:
        print('Парсинг EyacademyEn Курсы')
        AddCourse(Parse_EyacademyEnCourses())
    except Exception as e:
        print(e)

    try:
        print('Парсинг CsdCenterKzRu Курсы')
        from v1.parsers.CourseParsers.CsdCenterKzCourseParser import (
            Parse_CsdCenterKzEnCourses,
            Parse_CsdCenterKzKkCourses,
            Parse_CsdCenterKzRuCourses,
        )
        AddCourse(Parse_CsdCenterKzRuCourses())
    except Exception as e:
        print(e)

    try:
        print('Парсинг CsdCenterKzKk Курсы')
        AddCourse(Parse_CsdCenterKzKkCourses())
    except Exception as e:
        print(e)

    try:
        print('Парсинг CsdCenterKzEn Курсы')
        AddCourse(Parse_CsdCenterKzEnCourses())
    except Exception as e:
        print(e)
