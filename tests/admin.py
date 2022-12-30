from django.contrib import admin
from .models import SetTests, NameTest, Question, Answer, CountAnswer


class NameTestAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("settest",)}
    list_display = ('settest', 'title',)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['text', 'order']}),
    ]
    inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(SetTests)
admin.site.register(NameTest, NameTestAdmin)
admin.site.register(CountAnswer)
