from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from octofit_tracker.models import Team, UserProfile, Activity, Workout, Leaderboard
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data
        self.stdout.write(self.style.WARNING('Clearing existing data...'))
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()

        # Create teams
        self.stdout.write(self.style.SUCCESS('Creating teams...'))
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Marvel superheroes team'
        )
        team_dc = Team.objects.create(
            name='Team DC',
            description='DC superheroes team'
        )

        # Superheroes data
        marvel_heroes = [
            ('ironman', 'Tony Stark', 'tony@marvel.com', 'Iron Man'),
            ('captainamerica', 'Steve Rogers', 'steve@marvel.com', 'Captain America'),
            ('thor', 'Thor Odinson', 'thor@marvel.com', 'Thor'),
            ('blackwidow', 'Natasha Romanoff', 'natasha@marvel.com', 'Black Widow'),
            ('hawkeye', 'Clint Barton', 'clint@marvel.com', 'Hawk Eye'),
        ]

        dc_heroes = [
            ('superman', 'Clark Kent', 'clark@dc.com', 'Superman'),
            ('batman', 'Bruce Wayne', 'bruce@dc.com', 'Batman'),
            ('wonderwoman', 'Diana Prince', 'diana@dc.com', 'Wonder Woman'),
            ('theflash', 'Barry Allen', 'barry@dc.com', 'The Flash'),
            ('greenlantern', 'Hal Jordan', 'hal@dc.com', 'Green Lantern'),
        ]

        users = []

        # Create Marvel heroes
        self.stdout.write(self.style.SUCCESS('Creating Marvel superheroes...'))
        for username, first_name, email, display_name in marvel_heroes:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=display_name,
                password='superhero123'
            )
            profile = UserProfile.objects.create(
                user=user,
                email=email,
                team=team_marvel
            )
            users.append(user)

        # Create DC heroes
        self.stdout.write(self.style.SUCCESS('Creating DC superheroes...'))
        for username, first_name, email, display_name in dc_heroes:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=display_name,
                password='superhero123'
            )
            profile = UserProfile.objects.create(
                user=user,
                email=email,
                team=team_dc
            )
            users.append(user)

        # Create sample workouts
        self.stdout.write(self.style.SUCCESS('Creating sample workouts...'))
        workouts_data = [
            ('Morning Run', 'A refreshing morning run to start the day', 'easy', 30, 'cardio'),
            ('HIIT Training', 'High-intensity interval training for maximum burn', 'hard', 45, 'cardio'),
            ('Yoga Flow', 'Relaxing yoga session for flexibility and mindfulness', 'easy', 60, 'flexibility'),
            ('Strength Training', 'Full body strength training with weights', 'medium', 60, 'strength'),
            ('Swimming', 'Low-impact full body workout in the pool', 'medium', 45, 'cardio'),
        ]

        workouts = []
        for title, description, difficulty, duration, category in workouts_data:
            workout = Workout.objects.create(
                title=title,
                description=description,
                difficulty=difficulty,
                duration_minutes=duration,
                category=category
            )
            workouts.append(workout)

        # Create activities for each user
        self.stdout.write(self.style.SUCCESS('Creating activities for users...'))
        activity_types = ['run', 'walk', 'cycle', 'swim', 'gym', 'yoga']
        for user in users:
            for i in range(random.randint(3, 8)):
                activity_date = datetime.now() - timedelta(days=random.randint(0, 30))
                Activity.objects.create(
                    user=user,
                    activity_type=random.choice(activity_types),
                    duration_minutes=random.randint(20, 120),
                    distance_km=random.uniform(2.0, 15.0),
                    calories_burned=random.randint(100, 600),
                    date=activity_date,
                    notes=f'Activity for {user.first_name}'
                )

        # Create leaderboard entries
        self.stdout.write(self.style.SUCCESS('Creating leaderboard entries...'))
        rank = 1
        for team in [team_marvel, team_dc]:
            team_users = User.objects.filter(profile__team=team)
            for user in team_users:
                activities = Activity.objects.filter(user=user)
                total_activities = activities.count()
                total_calories = sum([a.calories_burned for a in activities])
                total_distance = sum([a.distance_km for a in activities])

                leaderboard = Leaderboard.objects.create(
                    user=user,
                    team=team,
                    total_activities=total_activities,
                    total_calories=int(total_calories),
                    total_distance=total_distance,
                    rank=rank,
                    points=total_activities * 10 + int(total_calories // 100)
                )
                rank += 1

        self.stdout.write(self.style.SUCCESS('Successfully populated octofit_db with test data!'))
