from admin_extra_buttons.decorators import button
from admin_extra_buttons.api import ExtraButtonsMixin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import redirect
from .forms import *

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



class CustomUserAdmin(UserAdmin):

    # Step 2: Override has_change_permission to disable 'change_user' check on add view
    def has_change_permission(self, request, obj=None):
        # If the user is adding a user, only check 'add_user' permission, not 'change_user'
        if obj is None:  # Adding a new user (obj is None during adding)
            return request.user.has_perm('auth.add_user')
        # For editing existing users, check if user has 'change_user' permission
        return super().has_change_permission(request, obj)


class StaffAdmin(admin.ModelAdmin):
    # Enable raw_id_fields for the User field, which creates a search box
    autocomplete_fields = ['User']

class OurAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ['Rutitle', 'Engtitle', 'Kktitle', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['Rutitle', 'Engtitle', 'Kktitle']
    ordering = ['-created_at']


    @button(label=('Пустые Англ поля'),)
    def showBlankEng(self, request):
        url = request.get_full_path()
        url2 = url[:url.index('showBlankEng')]
        print(url2)
        return redirect(url2 + '?Engtitle=')

    @button(label=('Пустые Каз поля'),)
    def showBlankKaz(self, request):
        url = request.get_full_path()
        url2 = url[:url.index('showBlankKaz')]
        print(url2)
        return redirect(url2 + '?Kktitle=')


class OurArticleAdmin(OurAdmin):
    form = OurArticleAdminForm
    fields = ['image', 'Rutitle', 'Rutext', 'word_fileRu', 'Engtitle', 'Engtext', 'word_fileEn', 'Kktitle', 'Kktext', 'word_fileKk']

class OurProjectAdmin(OurAdmin):
    form = OurProjectAdminForm
    fields = ['image','Rutitle', 'Rutext', 'word_fileRu', 'Engtitle', 'Engtext', 'word_fileEn', 'Kktitle', 'Kktext', 'word_fileKk',
              'status', 'is_active']

class OurCourseAdmin(OurAdmin):
    form = OurCourseAdminForm
    fields = ['image','Rutitle', 'Rutext', 'word_fileRu', 'Engtitle', 'Engtext', 'word_fileEn', 'Kktitle', 'Kktext', 'word_fileKk',
              'duration', 'start_date', 'end_date', 'instructor', 'is_online', 'is_active']

class OurEventAdmin(OurAdmin):
    form = OurEventAdminForm
    fields = ['image','Rutitle', 'Rutext', 'word_fileRu', 'Engtitle', 'Engtext', 'word_fileEn', 'Kktitle', 'Kktext', 'word_fileKk',
              'date', 'location', 'is_active']



admin.site.register(Article, CustomArtAdmin)
admin.site.register(Project)
admin.site.register(Course)
admin.site.register(Event)
admin.site.register(OurArticle, OurArticleAdmin)
admin.site.register(OurEvent, OurEventAdmin)
admin.site.register(OurProject, OurProjectAdmin)
admin.site.register(OurCourse, OurCourseAdmin)
admin.site.register(OurUrl)
admin.site.register(Editor, StaffAdmin)
admin.site.register(Manager, StaffAdmin)

# For telegram bot
admin.site.register(ArticleToFilter)
admin.site.register(CourseToFilter)
admin.site.register(ParsingError)
admin.site.register(blacklistLinks)

# Register the CustomUserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)