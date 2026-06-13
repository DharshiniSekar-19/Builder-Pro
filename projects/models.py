from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ('planning', 'Planning'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('delayed', 'Delayed'),
    ('on_hold', 'On Hold'),
]

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    client_name = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def total_activities(self):
        return self.activities.count()

    def completed_activities(self):
        return self.activities.filter(status='completed').count()

    def progress(self):
        total = self.total_activities()
        if total == 0:
            return 0
        return int((self.completed_activities() / total) * 100)
