from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile
from projects.models import Project
from activities.models import Activity, Dependency, WBSItem
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Create users
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@builderpro.com', 'admin123')
            admin.first_name = 'System'
            admin.last_name = 'Admin'
            admin.save()
            admin.profile.role = 'super_admin'
            admin.profile.phone = '+1-555-0100'
            admin.profile.save()
            self.stdout.write('  Created super admin: admin / admin123')

        if not User.objects.filter(username='manager').exists():
            manager = User.objects.create_user('manager', 'manager@builderpro.com', 'manager123')
            manager.first_name = 'John'
            manager.last_name = 'Smith'
            manager.save()
            manager.profile.role = 'project_manager'
            manager.profile.phone = '+1-555-0101'
            manager.profile.save()
            self.stdout.write('  Created project manager: manager / manager123')

        if not User.objects.filter(username='engineer').exists():
            engineer = User.objects.create_user('engineer', 'engineer@builderpro.com', 'engineer123')
            engineer.first_name = 'Mike'
            engineer.last_name = 'Johnson'
            engineer.save()
            engineer.profile.role = 'site_engineer'
            engineer.profile.phone = '+1-555-0102'
            engineer.profile.save()
            self.stdout.write('  Created site engineer: engineer / engineer123')

        if not User.objects.filter(username='client').exists():
            client = User.objects.create_user('client', 'client@builderpro.com', 'client123')
            client.first_name = 'Sarah'
            client.last_name = 'Wilson'
            client.save()
            client.profile.role = 'viewer'
            client.profile.phone = '+1-555-0103'
            client.profile.save()
            self.stdout.write('  Created viewer: client / client123')

        admin = User.objects.get(username='admin')
        manager = User.objects.get(username='manager')

        # Create projects
        projects_data = [
            {
                'name': 'Greenfield Residential Tower',
                'description': 'A 25-story residential tower with modern amenities including swimming pool, gym, and underground parking.',
                'client_name': 'Skyline Developers Inc.',
                'location': '123 Main Street, Downtown',
                'budget': 25000000,
                'start_date': date.today() - timedelta(days=60),
                'end_date': date.today() + timedelta(days=300),
                'status': 'in_progress',
            },
            {
                'name': 'Riverside Commercial Complex',
                'description': 'Commercial complex with retail spaces, offices, and a food court along the riverfront.',
                'client_name': 'Riverfront Properties Ltd.',
                'location': '456 River Road, Riverside District',
                'budget': 18000000,
                'start_date': date.today() - timedelta(days=30),
                'end_date': date.today() + timedelta(days=200),
                'status': 'in_progress',
            },
            {
                'name': 'Highway Bridge Construction',
                'description': 'Four-lane highway bridge spanning 500 meters across the valley with pedestrian walkways.',
                'client_name': 'State Highway Authority',
                'location': 'Highway 101, Mile Post 45',
                'budget': 45000000,
                'start_date': date.today() - timedelta(days=120),
                'end_date': date.today() + timedelta(days=240),
                'status': 'planning',
            },
            {
                'name': 'Hillside Villa Project',
                'description': 'Luxury villa community with 20 custom-designed homes with panoramic views.',
                'client_name': 'Luxury Homes Realty',
                'location': '200 Hillside Avenue, Uptown',
                'budget': 8500000,
                'start_date': date.today() - timedelta(days=200),
                'end_date': date.today() + timedelta(days=100),
                'status': 'completed',
            },
            {
                'name': 'Metro Station Renovation',
                'description': 'Complete renovation of downtown metro station including new platforms, escalators, and modern facilities.',
                'client_name': 'City Transit Authority',
                'location': 'Central Square, Downtown',
                'budget': 12000000,
                'start_date': date.today() - timedelta(days=10),
                'end_date': date.today() + timedelta(days=150),
                'status': 'delayed',
            },
        ]

        projects = []
        for pd in projects_data:
            project, created = Project.objects.get_or_create(
                name=pd['name'],
                defaults={
                    **pd,
                    'created_by': admin if random.choice([True, False]) else manager,
                }
            )
            if created:
                projects.append(project)
                self.stdout.write(f'  Created project: {project.name}')
            else:
                projects.append(project)

        if not projects:
            projects = list(Project.objects.all())

        # Create activities for each project
        activity_templates = {
            'Greenfield Residential Tower': [
                ('Site Preparation', 3, 5, 8, 50000, []),
                ('Excavation', 7, 10, 15, 120000, [0]),
                ('Foundation Work', 10, 14, 20, 200000, [1]),
                ('Structural Framework', 20, 25, 35, 500000, [2]),
                ('Floor Slabs', 15, 20, 28, 300000, [3]),
                ('External Walls', 12, 15, 20, 250000, [4]),
                ('Plumbing Installation', 8, 12, 16, 180000, [5]),
                ('Electrical Wiring', 10, 14, 20, 200000, [5]),
                ('HVAC System', 12, 15, 22, 350000, [6, 7]),
                ('Interior Finishing', 18, 25, 35, 400000, [8]),
                ('Roofing', 7, 10, 14, 150000, [5]),
                ('Windows & Doors', 6, 8, 12, 100000, [10]),
                ('Painting & Decorating', 8, 12, 18, 80000, [9, 11]),
                ('Landscaping', 5, 7, 10, 60000, [12]),
                ('Final Inspection', 2, 3, 5, 25000, [13]),
            ],
            'Riverside Commercial Complex': [
                ('Site Survey', 2, 3, 5, 15000, []),
                ('Demolition', 5, 7, 10, 40000, [0]),
                ('Excavation & Leveling', 8, 12, 16, 90000, [1]),
                ('Foundation', 12, 15, 20, 180000, [2]),
                ('Steel Structure', 18, 22, 30, 450000, [3]),
                ('Concrete Work', 14, 18, 25, 280000, [4]),
                ('Facade Installation', 10, 14, 20, 220000, [5]),
                ('Interior Partitions', 8, 12, 16, 120000, [5]),
                ('MEP Systems', 15, 20, 28, 380000, [6, 7]),
                ('Flooring & Ceiling', 10, 14, 20, 160000, [8]),
                ('Retail Fit-Out', 20, 28, 40, 500000, [9]),
                ('Parking Lot', 8, 10, 14, 100000, [5]),
                ('Final Handover', 3, 5, 7, 30000, [10, 11]),
            ],
        }

        for project in projects:
            if project.name in activity_templates:
                templates = activity_templates[project.name]
                created_activities = []
                for i, (name, ot, ml, pt, cost, deps) in enumerate(templates):
                    act, created = Activity.objects.get_or_create(
                        project=project,
                        name=name,
                        defaults={
                            'optimistic_time': ot,
                            'most_likely_time': ml,
                            'pessimistic_time': pt,
                            'cost': cost,
                            'priority': random.choice(['low', 'medium', 'high', 'critical']),
                            'status': 'not_started' if i > 3 else random.choice(['not_started', 'in_progress', 'completed']),
                            'assigned_to': random.choice([admin, manager, None]),
                        }
                    )
                    if created:
                        created_activities.append(act)
                    else:
                        created_activities.append(act)

                # Set dependencies
                for i, (name, ot, ml, pt, cost, deps) in enumerate(templates):
                    if i < len(created_activities):
                        for dep_idx in deps:
                            if dep_idx < len(created_activities):
                                Dependency.objects.get_or_create(
                                    activity=created_activities[i],
                                    predecessor_activity=created_activities[dep_idx],
                                )

                self.stdout.write(f'  Created activities for {project.name}')

            # Create WBS items
            wbs_items = [
                ('Site Preparation', None),
                ('Excavation', None),
                ('Foundation', None),
                ('Ground Floor', None),
                ('Upper Floors', None),
                ('Electrical', None),
                ('Plumbing', None),
                ('Finishing', None),
            ]
            for item_name, parent_name in wbs_items:
                parent = None
                if parent_name:
                    parent = WBSItem.objects.filter(project=project, name=parent_name).first()
                WBSItem.objects.get_or_create(
                    project=project,
                    name=item_name,
                    defaults={
                        'parent': parent,
                        'progress': random.randint(0, 100),
                        'order': wbs_items.index((item_name, parent_name)),
                    }
                )

        self.stdout.write(self.style.SUCCESS('Database seeding completed!'))
