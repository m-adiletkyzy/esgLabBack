from django import forms
from docx import Document
from .models import *

class OurBaseForm(forms.ModelForm):
    word_fileRu = forms.FileField(label="Загрузите Word-файл", required=False)
    word_fileEn = forms.FileField(label="Загрузите Word-файл", required=False)
    word_fileKk = forms.FileField(label="Загрузите Word-файл", required=False)

    class Media:
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/mammoth/1.4.2/mammoth.browser.min.js',  # Подключение библиотеки
            'js/wordfile_to_field.js',  # Ваш файл с кастомным JavaScript
        )


class OurArticleAdminForm(OurBaseForm):
    class Meta:
        model = OurArticle
        fields = "__all__"


class OurProjectAdminForm(OurBaseForm):
    class Meta:
        model = OurProject
        fields = "__all__"

class OurEventAdminForm(OurBaseForm):
    class Meta:
        model = OurEvent
        fields = "__all__"

class OurCourseAdminForm(OurBaseForm):
    class Meta:
        model = OurCourse
        fields = "__all__"