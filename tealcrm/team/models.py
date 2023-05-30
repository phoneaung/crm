from django.contrib.auth.models import User
from django.db import models

class Team(models.Model):
    name = models.TextField(max_length=100)
    members = models.ManyToManyField(User, related_name='teams')
    created_by = models.ForeignKey(User, related_name='created_teams', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Plan(models.Model):
    name = models.TextField(max_length=50)
    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    max_leads = models.IntegerField()
    max_clients = models.IntegerField()

    def __str__(self):
        return self.name