from django.contrib import admin
from .models import Team, UserProfile, Activity, Workout, Leaderboard


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'team', 'created_at')
    search_fields = ('email', 'user__username')
    list_filter = ('team', 'created_at')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'duration_minutes', 'calories_burned', 'date')
    list_filter = ('activity_type', 'date')
    search_fields = ('user__username',)
    ordering = ('-date',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'duration_minutes', 'category', 'created_at')
    list_filter = ('difficulty', 'category')
    search_fields = ('title',)


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'rank', 'total_activities', 'total_calories', 'points')
    list_filter = ('team', 'rank')
    search_fields = ('user__username',)
    ordering = ('rank',)
