from django.urls import path
from .views import (
    list_sessions, mark_attendance,
    signup, login,
    LevelListView, SubmissionListCreateView, SubmissionUpdateView,
    leaderboard
)

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('levels/', LevelListView.as_view(), name='levels'),
    path('submissions/', SubmissionListCreateView.as_view(), name='submissions'),
    path('submissions/<int:pk>/', SubmissionUpdateView.as_view(), name='submission-update'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('sessions/', list_sessions, name='sessions'),
    path('sessions/<int:session_id>/attendance/', mark_attendance, name='mark-attendance'),
]