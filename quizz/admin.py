from django.contrib import admin
from .models import Question, Answer, Category, Comment, UserAnswer


class AdminCategoriesOverview(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    list_filter = ("name",)
    
class AdminQuestionsOverview(admin.ModelAdmin):
    list_display = ("image", "question_text", "category")
    search_fields = ("question_text",)
    ordering = ("category",)
    list_filter = ("category",)
    
class AdminAnswersOverview(admin.ModelAdmin):
    list_display = ("is_correct", "answer_text", "question")
    search_fields = ("is_correct", 'question')
    ordering = ("question",)
    list_filter = ("is_correct",)
    
class AdminCommentsOverview(admin.ModelAdmin):
    list_display = ("user","question", "comment_text", "created_at")
    search_fields = ("question", 'comment_text')
    ordering = ("created_at",)
    list_filter = ("question",)
    
class AdminProgressOverview(admin.ModelAdmin):
    list_display = ("user","question", "selected_answer")
    search_fields = ("user",)
    ordering = ("user",)
    list_filter = ("question", )
    


admin.site.register(Category, AdminCategoriesOverview)
admin.site.register(Question, AdminQuestionsOverview)
admin.site.register(Answer, AdminAnswersOverview)
admin.site.register(Comment, AdminCommentsOverview)
admin.site.register(UserAnswer, AdminProgressOverview)
