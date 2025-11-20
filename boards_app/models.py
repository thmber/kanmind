from django.db import models
from django.conf import settings


class Board(models.Model):
    title = models.CharField(max_length=255)
    tickets = models.JSONField(default=list, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_boards', on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='memberships', blank=True)


    def __str__(self):
        return self.title