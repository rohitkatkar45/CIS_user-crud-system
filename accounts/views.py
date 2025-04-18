from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser, Task
from .serializers import UserSerializer, RegisterSerializer, TaskSerializer
from .permissions import IsAdmin, IsManager, IsUser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsManager]

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'MANAGER':
            return Task.objects.filter(assigned_by=user).only('id', 'title', 'status')  
        elif user.role == 'USER':
            return Task.objects.filter(assigned_to=user).only('id', 'title', 'status')
        return Task.objects.none()

class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == 'COMPLETED':
            print(f'Task "{instance.title}" completed by {instance.assigned_to.username}')

class MissedTaskChecker(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        now = timezone.now()
        tasks = Task.objects.filter(deadline__lt=now, status='PENDING')

        for task in tasks:
            task.status = 'MISSED'
            task.save()

            user = task.assigned_to
            user.missed_tasks_count += 1

            manager = task.assigned_by 
            self.send_task_notification(manager, task)

            if user.missed_tasks_count >= 5:
                user.is_deactivated = True
                user.save()
                print(f'User {user.username} has been deactivated after 5 missed tasks.')

        return Response({'message': 'Checked and updated missed tasks.'}, status=status.HTTP_200_OK)

    def send_task_notification(self, manager, task):
        subject = f"Task '{task.title}' Missed Deadline"
        message = f"The task '{task.title}' assigned to {task.assigned_to.username} has missed the deadline."
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [manager.email],
            fail_silently=False,
        )

class ReactivateUserView(APIView):
    permission_classes = [IsManager]

    def post(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            if user.is_deactivated:
                user.is_deactivated = False
                user.missed_tasks_count = 0
                user.save()
                return Response({'message': 'User reactivated successfully'})
            return Response({'message': 'User is already active'})
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

class TokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

class TokenRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]
