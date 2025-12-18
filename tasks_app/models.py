from django.db import models
from django.conf import settings
from boards_app.models import Board
from django.utils import timezone
from datetime import timedelta


# here we define the Task model which represents a task within a board, with various attributes and relationships

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assignee = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assigned_to', blank=True)
    board = models.ForeignKey(Board, related_name='tasks', on_delete=models.CASCADE, null=True, blank=True, default=9)
    reviewer = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='reviewing_by', blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creator_of_task', on_delete=models.CASCADE)

    def one_week_from_now():
        return timezone.now().date() + timedelta(weeks=1)

    class Status(models.TextChoices):
        todo = "to-do"
        in_progress = "in-progress"
        done = "done"
        review = "review"

    # this field stores the due date of the task, defaulting to one week from creation

    due_date = models.DateField(default=one_week_from_now, blank=True)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.todo)

    class Priority(models.TextChoices):
        low = "low"
        medium = "medium"
        high = "high"

    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.medium)

    def __str__(self):
        return self.title
    

# here we define the TaskComment model which represents comments made on tasks by users

class TaskComment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='task_comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.id} on Task {self.task_id}"




