from django.db import models
from django.contrib.auth.models import User
from projects.models import Project

PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('critical', 'Critical'),
]

STATUS_CHOICES = [
    ('not_started', 'Not Started'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
]

class Activity(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    optimistic_time = models.FloatField(default=0)
    most_likely_time = models.FloatField(default=0)
    pessimistic_time = models.FloatField(default=0)
    expected_duration = models.FloatField(default=0, editable=False)
    variance = models.FloatField(default=0, editable=False)
    standard_deviation = models.FloatField(default=0, editable=False)
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    # CPM fields
    earliest_start = models.FloatField(default=0, editable=False)
    earliest_finish = models.FloatField(default=0, editable=False)
    latest_start = models.FloatField(default=0, editable=False)
    latest_finish = models.FloatField(default=0, editable=False)
    float_time = models.FloatField(default=0, editable=False)
    is_critical = models.BooleanField(default=False, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Activities'
        ordering = ['project', 'earliest_start']

    def __str__(self):
        return f"{self.project.name} - {self.name}"

    def save(self, *args, **kwargs):
        self.calculate_pert()
        super().save(*args, **kwargs)

    def calculate_pert(self):
        if self.optimistic_time and self.most_likely_time and self.pessimistic_time:
            self.expected_duration = round((self.optimistic_time + 4 * self.most_likely_time + self.pessimistic_time) / 6, 2)
            variance_val = ((self.pessimistic_time - self.optimistic_time) / 6) ** 2
            self.variance = round(variance_val, 4)
            self.standard_deviation = round(variance_val ** 0.5, 2)
        return {
            'expected_duration': self.expected_duration,
            'variance': self.variance,
            'standard_deviation': self.standard_deviation,
        }

class Dependency(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='predecessors')
    predecessor_activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='dependents')

    class Meta:
        verbose_name_plural = 'Dependencies'
        unique_together = ['activity', 'predecessor_activity']

    def __str__(self):
        return f"{self.predecessor_activity.name} -> {self.activity.name}"

class WBSItem(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='wbs_items')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    progress = models.IntegerField(default=0)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'WBS Item'
        verbose_name_plural = 'WBS Items'

    def __str__(self):
        return self.name
