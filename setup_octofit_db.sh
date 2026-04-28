#!/bin/bash
# Setup script for OctoFit Tracker Django backend

set -e

echo "=========================================="
echo "OctoFit Tracker Django Backend Setup"
echo "=========================================="

# Check if MongoDB is running
echo ""
echo "Checking MongoDB service..."
if ps aux | grep -q "[m]ongod"; then
    echo "✓ MongoDB is running"
else
    echo "✗ MongoDB is not running"
    echo "Please start MongoDB with: sudo systemctl start mongod"
    exit 1
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source octofit-tracker/backend/venv/bin/activate

# Run migrations
echo ""
echo "Running Django migrations..."
cd octofit-tracker/backend
python manage.py makemigrations
python manage.py migrate

# Populate database
echo ""
echo "Populating database with test data..."
python manage.py populate_db

# Verify database
echo ""
echo "Verifying database with mongosh..."
mongosh octofit_db --eval "
  console.log('Collections in octofit_db:');
  db.getCollectionNames().forEach(name => console.log('  - ' + name));
  
  console.log('\nSample documents:');
  
  console.log('\nUsers:');
  db.users.find().limit(2).forEach(doc => printjson(doc));
  
  console.log('\nTeams:');
  db.teams.find().limit(2).forEach(doc => printjson(doc));
  
  console.log('\nActivities:');
  db.activities.find().limit(2).forEach(doc => printjson(doc));
  
  console.log('\nWorkouts:');
  db.workouts.find().limit(2).forEach(doc => printjson(doc));
  
  console.log('\nLeaderboard:');
  db.leaderboard.find().limit(2).forEach(doc => printjson(doc));
"

echo ""
echo "=========================================="
echo "✓ Setup complete!"
echo "=========================================="
echo ""
echo "To run the Django app:"
echo "1. Use the .vscode/launch.json configuration in VS Code"
echo "2. Or run: python manage.py runserver"
echo ""
