from django.contrib import admin
from .models import Question, Answer, Category, Comment, QuizProgress


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
    list_display = ("user","category","time_category", "score")
    search_fields = ("category", 'time_category')
    ordering = ("score",)
    list_filter = ("time_category", 'category')
    


admin.site.register(Category, AdminCategoriesOverview)
admin.site.register(Question, AdminQuestionsOverview)
admin.site.register(Answer, AdminAnswersOverview)
admin.site.register(Comment, AdminCommentsOverview)
admin.site.register(QuizProgress, AdminProgressOverview)
