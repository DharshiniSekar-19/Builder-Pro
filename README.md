# 🏗️ Builder Pro

**Construction Project Management System with CPM & PERT Analysis**

A production-ready enterprise-grade web application for construction project management built with Django 5, featuring Critical Path Method (CPM) analysis, PERT analysis, and project completion probability calculations.

---

## Features

### Core Modules

1. **Authentication & Authorization** - Role-based access control with Super Admin, Project Manager, Site Engineer, and Viewer roles
2. **Project Management** - Create, edit, delete projects with status tracking and budget management
3. **Activity Management** - Define activities with time estimates, dependencies, and assignments
4. **CPM Analysis Engine** - Automatic critical path calculation with forward/backward pass
5. **PERT Analysis Engine** - Expected duration, variance, and standard deviation calculations
6. **Project Completion Probability** - Z-score based probability calculator
7. **Work Breakdown Structure (WBS)** - Tree-based project decomposition
8. **Dashboard** - Real-time charts and metrics using Chart.js
9. **Reports** - PDF and Excel report generation

### Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript, Chart.js |
| Backend | Python 3.13, Django 5 |
| Database | SQLite (Dev) / PostgreSQL (Production) |
| ORM | Django ORM |
| Deployment | Docker, Gunicorn, Nginx |

---

## Quick Start

### Prerequisites

- Python 3.13+
- pip
- (Optional) Docker & Docker Compose

### Local Development

```bash
# Clone the repository
git clone <repo-url>
cd builderpro

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed demo data
python manage.py seed_data

# Run development server
python manage.py runserver
```

Visit http://127.0.0.1:8000

### Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| Super Admin | admin | admin123 |
| Project Manager | manager | manager123 |
| Site Engineer | engineer | engineer123 |
| Viewer/Client | client | client123 |

---

## Docker Deployment

```bash
# Build and start all services
docker-compose up -d --build

# Run migrations
docker-compose exec web python manage.py migrate

# Seed data
docker-compose exec web python manage.py seed_data
```

Visit http://localhost

---

## Architecture

```
builderpro/
├── accounts/          # Authentication & User Management
│   ├── models.py      # Profile, Role choices
│   ├── views.py       # Login, Register, Profile, Dashboard
│   ├── forms.py       # User forms
│   ├── decorators.py  # Role-based access decorators
│   └── urls.py        # URL routing
├── projects/          # Project Management
│   ├── models.py      # Project model
│   ├── views.py       # CRUD operations
│   └── urls.py
├── activities/        # Activity Management & Analysis
│   ├── models.py      # Activity, Dependency, WBSItem
│   ├── cpm.py         # Critical Path Method engine
│   ├── pert.py        # PERT analysis engine
│   ├── views.py       # Activity views, CPM/PERT views
│   └── urls.py
├── analytics/         # Reporting & Analytics
│   ├── views.py       # Reports, Excel export
│   └── urls.py
├── templates/         # Django templates
│   ├── base.html      # Base template
│   ├── accounts/      # Login, Register, Dashboard, Profile
│   ├── projects/      # Project CRUD, Detail, WBS
│   ├── activities/    # Activities, CPM, PERT, Probability
│   └── analytics/     # Reports
├── static/            # Static files
│   ├── css/           # Stylesheet (dark mode support)
│   └── js/            # JavaScript utilities
├── docker/            # Docker configuration
│   └── nginx/         # Nginx config
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## CPM Algorithm

The Critical Path Method (CPM) is implemented in `activities/cpm.py`:

1. **Forward Pass** - Calculates Earliest Start (ES) and Earliest Finish (EF)
   - ES = max(EF of all predecessors)
   - EF = ES + Duration

2. **Backward Pass** - Calculates Latest Start (LS) and Latest Finish (LF)
   - LF = min(LS of all successors)
   - LS = LF - Duration

3. **Float Calculation** - Float = LS - ES (or LF - EF)
4. **Critical Path** - Activities with Float = 0

## PERT Analysis

The PERT analysis is implemented in `activities/pert.py`:

Formulas:
- **Expected Duration (TE)** = (O + 4M + P) / 6
- **Variance (σ²)** = ((P - O) / 6)²
- **Standard Deviation (σ)** = √Variance
- **Z-Score** = (Target - Expected) / σ
- **Probability** = Normal CDF(Z)

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard |
| GET/POST | `/login/` | User login |
| GET/POST | `/register/` | User registration |
| GET/POST | `/profile/` | User profile |
| GET/POST | `/change-password/` | Change password |
| GET | `/projects/` | Project list |
| GET/POST | `/projects/create/` | Create project |
| GET | `/projects/<id>/` | Project detail |
| GET/POST | `/projects/<id>/edit/` | Edit project |
| POST | `/projects/<id>/delete/` | Delete project |
| GET | `/activities/` | Activity list |
| GET/POST | `/activities/create/` | Create activity |
| GET | `/activities/cpm/<project_id>/` | CPM analysis |
| GET | `/activities/pert/<project_id>/` | PERT analysis |
| GET | `/activities/pert/<project_id>/probability/` | Probability calculator |
| GET | `/analytics/` | Analytics dashboard |
| GET | `/analytics/project/<id>/report/` | Project report |
| GET | `/analytics/project/<id>/export-excel/` | Export Excel |

---

## Testing

```bash
python manage.py test
```

34 tests covering:
- Authentication system
- Project CRUD operations
- PERT calculation formulas
- CPM analysis
- Activity models
- Analytics views
- Excel export
- API endpoints

---

## Security

- CSRF Protection (built-in Django)
- SQL Injection Prevention (parameterized queries via ORM)
- XSS Protection (template auto-escaping)
- Password Hashing (PBKDF2/SHA256)
- Role-Based Authorization (custom decorators)
- Session Management (Django sessions)

---

## License

MIT License
