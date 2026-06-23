# from g4f.client import Client

# class DeepSeek():
#     def __init__(self):
#         self.client = Client()

#     def DSv3(self, text):
#         return self.client.chat.completions.create(
#             model="deepseek-v3",
#             messages=[{"role": "user", "content": text}],
#             web_search=False
#         ).choices[0].message.content

#     def ArticleFilter(self, text):
#         prompt = 'Я скину заголовок и дайджест новостной статьи. Ответь коротко одним числом насколько эта статья относится к тематике ESG от 1 до 10\n'

#         return self.DSv3(prompt + '\n' + text)

#     def CourseFilter(self, text):
#         prompt = 'Я скину название и дайджест образовательного курса. Ответь коротко одним числом насколько этот курс относится к тематике ESG от 1 до 10\n'

#         return self.DSv3(prompt + '\n' + text)





