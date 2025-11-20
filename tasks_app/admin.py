from django.contrib import admin
from .models import Task, TaskComment





class CommentInline(admin.TabularInline):
    model = TaskComment
    extra = 0 



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'due_date', 'board']
    filter_horizontal = ('assignee', 'reviewer')  
    inlines = [CommentInline]
