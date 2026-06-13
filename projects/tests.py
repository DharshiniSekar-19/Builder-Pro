from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Project
from datetime import date, timedelta

class ProjectTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testmanager', 'manager@test.com', 'pass123')
        self.user.first_name = 'Test'
        self.user.last_name = 'Manager'
        self.user.save()
        self.user.profile.role = 'project_manager'
        self.user.profile.save()

        self.project = Project.objects.create(
            name='Test Project',
            description='A test project',
            client_name='Test Client',
            location='Test Location',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            budget=500000,
            status='planning',
            created_by=self.user,
        )

    def test_project_creation(self):
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(self.project.name, 'Test Project')

    def test_project_list_view(self):
        self.client.login(username='testmanager', password='pass123')
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')

    def test_project_detail_view(self):
        self.client.login(username='testmanager', password='pass123')
        response = self.client.get(reverse('project_detail', args=[self.project.pk]))
        self.assertEqual(response.status_code, 200)

    def test_project_create_view(self):
        self.client.login(username='testmanager', password='pass123')
        response = self.client.get(reverse('project_create'))
        self.assertEqual(response.status_code, 200)

    def test_project_total_activities(self):
        self.assertEqual(self.project.total_activities(), 0)

    def test_project_progress(self):
        self.assertEqual(self.project.progress(), 0)

    def test_project_string(self):
        self.assertEqual(str(self.project), 'Test Project')
