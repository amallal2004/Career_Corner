from django.urls import path
from .views import (
    signup, login,
    LevelListView, SubmissionListCreateView, SubmissionUpdateView,
    leaderboard, my_profile,
    list_sessions, mark_attendance, create_session,
    LevelCreateView
)

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('levels/', LevelListView.as_view(), name='levels'),
    path('submissions/', SubmissionListCreateView.as_view(), name='submissions'),
    path('submissions/<int:pk>/', SubmissionUpdateView.as_view(), name='submission-update'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('sessions/', list_sessions, name='sessions'),
    path('sessions/create/', create_session, name='create-session'),
    path('sessions/<int:session_id>/attendance/', mark_attendance, name='mark-attendance'),
    path('profile/', my_profile, name='my-profile'),
    path('levels/create/', LevelCreateView.as_view(), name='create-level'),
]