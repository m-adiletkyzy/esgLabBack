from django.contrib import admin
from import_export import resources
from import_export.admin import ExportActionMixin, ImportExportModelAdmin, ExportMixin
from import_export.widgets import DateTimeWidget

from .models import *
from import_export import resources
from import_export.fields import Field
# Register your models here.
class ArticleResource(resources.ModelResource):
    ar_date = Field(attribute='ar_date', column_name='artiicle_date', widget=DateTimeWidget('%m/%d/%Y, %I:%M:%S %p'))
    pars_date = Field(attribute='pars_date', column_name='parsing_date', widget=DateTimeWidget('%m/%d/%Y, %I:%M:%S %p'))

    class Meta:
        model = Article

class CustomArtAdmin(ExportMixin, admin.ModelAdmin):
    model = Article
    resource_class = ArticleResource

admin.site.register(Article, CustomArtAdmin)
admin.site.register(Project)
admin.site.register(Course)
admin.site.register(Event)
admin.site.register(OurArticle)
admin.site.register(OurEvent)
admin.site.register(OurProject)
admin.site.register(OurCourse)
admin.site.register(OurUrl)