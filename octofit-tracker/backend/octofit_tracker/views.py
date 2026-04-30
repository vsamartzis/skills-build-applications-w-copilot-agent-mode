from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Team, UserProfile, Activity, Workout, Leaderboard
from .serializers import (
    TeamSerializer,
    UserProfileSerializer,
    ActivitySerializer,
    WorkoutSerializer,
    LeaderboardSerializer
)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [AllowAny]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Allow users to see their own activities
        user = self.request.user
        if user.is_authenticated:
            return Activity.objects.filter(user=user)
        return Activity.objects.all()


class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [AllowAny]


class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    permission_classes = [AllowAny]
