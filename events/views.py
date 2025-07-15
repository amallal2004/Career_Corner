from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.db.models import F
from django.utils import timezone
from datetime import timedelta

from .models import Level, Submission, Profile, Session, Attendance, User
from .serializers import LevelSerializer, SubmissionSerializer, SessionSerializer, AttendanceSerializer

# Signup
@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    full_name = request.data.get('full_name')
    year_of_study = request.data.get('year_of_study')
    department = request.data.get('department')
    phone = request.data.get('phone')

    if not username or not password:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    user.profile.full_name = full_name
    user.profile.year_of_study = year_of_study
    user.profile.department = department
    user.profile.phone = phone
    user.profile.save()

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'message': 'Signup successful'})

# Login
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'message': 'Login successful'})
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# List all levels for students
class LevelListView(generics.ListAPIView):
    queryset = Level.objects.all().order_by('number')
    serializer_class = LevelSerializer
    permission_classes = [IsAuthenticated]

# Students list + submit tasks
class SubmissionListCreateView(generics.ListCreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        submission = serializer.save(student=self.request.user)
        # Early submission bonus
        if submission.level.deadline - submission.submitted_at.date() >= timedelta(days=2):
            Profile.objects.filter(user=submission.student).update(score=F('score') + 2)

# Mentor approves or rejects submissions
class SubmissionUpdateView(generics.UpdateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        submission = serializer.save()
        print(f"Mentor updated submission {submission.id} to status {submission.status}")
        # Only award score if newly approved
        if submission.status == 'approved':
            Profile.objects.filter(user=submission.student).update(score=F('score') + 10)

# Leaderboard view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leaderboard(request):
    top_profiles = Profile.objects.select_related('user').filter(user__is_staff=False).order_by('-score')[:5]
    data = [
        {"username": p.user.username, "score": p.score}
        for p in top_profiles
    ]
    return Response(data)


# Mentor creates a new session
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_session(request):
    serializer = SessionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List all sessions (students & mentors can both see upcoming events)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_sessions(request):
    sessions = Session.objects.order_by('date')
    serializer = SessionSerializer(sessions, many=True)
    return Response(serializer.data)

# Mentor marks attendance for a session
@api_view(['POST'])
@permission_classes([IsAdminUser])
def mark_attendance(request, session_id):
    try:
        session = Session.objects.get(pk=session_id)
    except Session.DoesNotExist:
        return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

    attendances = request.data.get('attendances', [])
    for att in attendances:
        student_id = att.get('student_id')
        status_val = att.get('status')

        if not student_id or status_val not in ['present', 'absent']:
            continue

        try:
            student = User.objects.get(pk=student_id)
        except User.DoesNotExist:
            continue

        # create or update attendance
        attendance, created = Attendance.objects.get_or_create(
            student=student, session=session,
            defaults={'status': status_val}
        )

        if not created:
            # already exists, update status
            attendance.status = status_val
            attendance.save()

        # Add +5 points if marking present and never awarded before
        if attendance.status == 'present':
            if created or attendance.status != 'present':
                Profile.objects.filter(user=student).update(score=F('score') + 5)

    return Response({"message": "Attendance recorded"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    profile = request.user.profile
    data = {
        "username": request.user.username,
        "email": request.user.email,
        "full_name": profile.full_name,
        "year_of_study": profile.year_of_study,
        "department": profile.department,
        "phone": profile.phone,
        "score": profile.score
    }
    return Response(data)

class LevelCreateView(generics.CreateAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = [IsAdminUser]

