from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Activity, Dependency, WBSItem
from .pert import PERTAnalyzer
from projects.models import Project
from datetime import date, timedelta
import math

class PERTAnalyzerTests(TestCase):
    def test_calculate_expected_duration(self):
        result = PERTAnalyzer.calculate(2, 4, 6)
        expected = (2 + 4*4 + 6) / 6
        self.assertEqual(result['expected_duration'], round(expected, 2))

    def test_calculate_variance(self):
        result = PERTAnalyzer.calculate(2, 4, 6)
        expected_var = ((6 - 2) / 6) ** 2
        self.assertEqual(result['variance'], round(expected_var, 4))

    def test_calculate_std_dev(self):
        result = PERTAnalyzer.calculate(2, 4, 6)
        expected_std = math.sqrt(((6 - 2) / 6) ** 2)
        self.assertEqual(result['standard_deviation'], round(expected_std, 2))

    def test_probability_100_percent(self):
        prob = PERTAnalyzer.probability(10, 5, 1)
        self.assertGreater(prob, 99)

    def test_probability_0_percent(self):
        prob = PERTAnalyzer.probability(0, 5, 1)
        self.assertLess(prob, 1)

    def test_probability_50_percent(self):
        prob = PERTAnalyzer.probability(5, 5, 1)
        self.assertAlmostEqual(prob, 50, delta=5)

    def test_calculate_with_zero_std(self):
        prob = PERTAnalyzer.probability(5, 5, 0)
        self.assertEqual(prob, 100.0)

    def test_calculate_negative_target(self):
        prob = PERTAnalyzer.probability(2, 5, 1)
        self.assertLess(prob, 50)


class ActivityModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com', 'pass')
        self.project = Project.objects.create(
            name='Test Project',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            created_by=self.user,
        )

    def test_activity_creation(self):
        activity = Activity.objects.create(
            project=self.project,
            name='Test Activity',
            optimistic_time=2,
            most_likely_time=4,
            pessimistic_time=6,
        )
        expected = round((2 + 4*4 + 6) / 6, 2)
        self.assertEqual(activity.expected_duration, expected)
        self.assertEqual(str(activity), f'Test Project - Test Activity')

    def test_activity_calculate_pert(self):
        activity = Activity(
            project=self.project,
            name='Test',
            optimistic_time=1,
            most_likely_time=2,
            pessimistic_time=3,
        )
        result = activity.calculate_pert()
        self.assertIn('expected_duration', result)
        self.assertIn('variance', result)
        self.assertIn('standard_deviation', result)

    def test_dependency_creation(self):
        act1 = Activity.objects.create(
            project=self.project, name='Activity 1',
            optimistic_time=1, most_likely_time=2, pessimistic_time=3,
        )
        act2 = Activity.objects.create(
            project=self.project, name='Activity 2',
            optimistic_time=2, most_likely_time=3, pessimistic_time=4,
        )
        dep = Dependency.objects.create(activity=act2, predecessor_activity=act1)
        self.assertEqual(str(dep), 'Activity 1 -> Activity 2')

    def test_wbs_creation(self):
        wbs = WBSItem.objects.create(
            project=self.project, name='Foundation', progress=50
        )
        self.assertEqual(str(wbs), 'Foundation')
