from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Question, Answer, Comment, Like, Tag

# Register your models here.

class TagAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ('name',)
    filter_by = ['name']


class CommentInline(GenericTabularInline):
    model = Comment
    ordering = ['created_at']
    fields = ['author', 'content']
    max_num = 1


class LikeInline(GenericTabularInline):
    model = Like
    ordering = ['created_at']
    fields = ['author']
    max_num = 1


class QuestionAdmin(admin.ModelAdmin):
    fields = ['summary', 'content', 'author', 'tags']
    list_display = ('summary', 'author', 'created_at')
    filter_by = ['created_at']
    inlines = [CommentInline, LikeInline]


class AnswerAdmin(admin.ModelAdmin):
    fields = ['content', 'question', 'author']
    list_display = ('question', 'author', 'created_at')
    filter_by = ['created_at']
    inlines = [CommentInline, LikeInline]


admin.site.register(Tag, TagAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)