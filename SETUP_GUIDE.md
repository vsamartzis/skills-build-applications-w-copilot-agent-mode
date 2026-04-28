# OctoFit Tracker - Django Backend Setup Guide

This guide walks you through setting up the Django backend for the OctoFit Tracker application.

## Prerequisites

- Python 3.10+ with virtual environment (`venv`) already created at `octofit-tracker/backend/venv`
- MongoDB running locally on port 27017
- Django and required packages installed (see `octofit-tracker/backend/requirements.txt`)

## Setup Steps

### 1. Verify MongoDB is Running

Check if MongoDB service is running:
```bash
ps aux | grep mongod
```

If not running, start it:
```bash
sudo systemctl start mongod
```

### 2. Activate Virtual Environment

```bash
source octofit-tracker/backend/venv/bin/activate
```

### 3. Run Django Migrations

Navigate to the backend directory (or run from root with full path):
```bash
cd octofit-tracker/backend
python manage.py makemigrations
python manage.py migrate
```

This creates the necessary database collections and schema.

### 4. Populate Database with Test Data

Run the custom management command:
```bash
python manage.py populate_db
```

This will:
- Create two teams: Team Marvel and Team DC
- Add 5 superheroes to each team with sample data
- Create sample activities and workout suggestions
- Initialize leaderboard entries

### 5. Verify Database Setup

Use mongosh to verify the collections and data:
```bash
mongosh octofit_db
```

Then run these commands in the mongosh prompt:
```javascript
// List all collections
db.getCollectionNames()

// Show sample documents from each collection
db.users.find().limit(2)
db.teams.find()
db.activities.find().limit(2)
db.workouts.find().limit(2)
db.leaderboard.find().limit(2)

// Verify unique index on email
db.users.getIndexes()

// Exit
exit
```

## Running the Django Development Server

### Option 1: Using VS Code Launch Configuration

1. Open the project in VS Code
2. Go to the Run and Debug tab (or press `Ctrl+Shift+D`)
3. Select "Django" from the dropdown (configured in `.vscode/launch.json`)
4. Click the green play button to start the server
5. The server will run on `http://localhost:8000`

### Option 2: Manual Command

From the `octofit-tracker/backend` directory:
```bash
python manage.py runserver
```

The server will be available at `http://localhost:8000`

## API Endpoints

Once the server is running, access the following endpoints:

### REST API Endpoints
- **Teams**: `http://localhost:8000/api/teams/`
- **Users**: `http://localhost:8000/api/users/`
- **Activities**: `http://localhost:8000/api/activities/`
- **Workouts**: `http://localhost:8000/api/workouts/`
- **Leaderboard**: `http://localhost:8000/api/leaderboard/`

### Authentication Endpoints
- **Auth**: `http://localhost:8000/dj-rest-auth/`
- **Registration**: `http://localhost:8000/dj-rest-auth/registration/`

### Django Admin
- **Admin Panel**: `http://localhost:8000/admin/`
- Create a superuser to access admin: `python manage.py createsuperuser`

## Project Structure

```
octofit-tracker/backend/
├── manage.py                           # Django management script
├── requirements.txt                    # Python dependencies
├── octofit_tracker/                    # Main Django app
│   ├── __init__.py
│   ├── settings.py                     # Django configuration with Djongo & CORS
│   ├── urls.py                         # URL routing with REST API endpoints
│   ├── wsgi.py                         # WSGI application
│   ├── asgi.py                         # ASGI application
│   ├── models.py                       # Database models (Team, User, Activity, etc.)
│   ├── serializers.py                  # DRF serializers
│   ├── views.py                        # API ViewSets
│   ├── admin.py                        # Django admin configuration
│   └── management/
│       └── commands/
│           └── populate_db.py          # Custom command to populate database
└── venv/                               # Python virtual environment
```

## Key Configuration Details

### Django Settings (settings.py)
- **Database**: Configured to use Djongo with MongoDB (`octofit_db`)
- **CORS**: Enabled for all origins, methods, and headers (`*`)
- **INSTALLED_APPS**: Includes `djongo`, `rest_framework`, `corsheaders`, `dj-rest-auth`, `allauth`
- **MIDDLEWARE**: CORS middleware configured
- **Authentication**: Token-based authentication with dj-rest-auth

### Database Models
- **Team**: Stores team information (Team Marvel, Team DC)
- **UserProfile**: Extended user profile linked to teams
- **Activity**: User workout activities with details (type, duration, distance, calories)
- **Workout**: Suggested workout plans with difficulty levels
- **Leaderboard**: Tracks user rankings and points within teams

## Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running: `ps aux | grep mongod`
- Check that port 27017 is available
- Verify database name in `settings.py` is `octofit_db`

### Migration Errors
- Clear migrations and try again: `python manage.py showmigrations`
- Delete migration files if necessary and recreate them: `python manage.py makemigrations --empty octofit_tracker --name reset`

### CORS Issues
- CORS is configured to accept all origins in `settings.py`
- Adjust `CORS_ALLOWED_ORIGINS` if specific origins are needed

### API Not Responding
- Ensure server is running on port 8000
- Check firewall settings if running on a remote server
- Verify all required packages are installed from `requirements.txt`

## Next Steps

1. **Frontend Development**: Set up the React frontend in `octofit-tracker/frontend/`
2. **Authentication Testing**: Test authentication endpoints with a client (Postman, cURL, etc.)
3. **Team & Leaderboard Features**: Implement additional endpoints as needed
4. **Deployment**: Configure for production deployment (change SECRET_KEY, set DEBUG=False, etc.)

---

For detailed information about the OctoFit Tracker project, see [octofit_story.md](./docs/octofit_story.md)
