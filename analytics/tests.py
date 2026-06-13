from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from projects.models import Project
from activities.models import Activity, Dependency
from datetime import date, timedelta

class AnalyticsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('admin', 'admin@test.com', 'pass')
        self.user.profile.role = 'super_admin'
        self.user.profile.save()

        self.project = Project.objects.create(
            name='Analytics Test',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            created_by=self.user,
        )

    def test_analytics_dashboard_view(self):
        self.client.login(username='admin', password='pass')
        response = self.client.get(reverse('analytics_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_project_report_view(self):
        self.client.login(username='admin', password='pass')
        response = self.client.get(reverse('project_report', args=[self.project.pk]))
        self.assertEqual(response.status_code, 200)

    def test_cpm_report_view(self):
        self.client.login(username='admin', password='pass')
        response = self.client.get(reverse('cpm_report', args=[self.project.pk]))
        self.assertEqual(response.status_code, 200)

    def test_pert_report_view(self):
        self.client.login(username='admin', password='pass')
        response = self.client.get(reverse('pert_report', args=[self.project.pk]))
        self.assertEqual(response.status_code, 200)

    def test_ajax_chart_data(self):
        self.client.login(username='admin', password='pass')
        response = self.client.get(reverse('ajax_chart_data'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('project_labels', response.json())

    def test_export_excel(self):
        self.client.login(username='admin', password='pass')
        response = self.client.get(reverse('export_project_excel', args=[self.project.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/vnd.openxmlformats', response['Content-Type'])
