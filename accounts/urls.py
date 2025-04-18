from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
   
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),  
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('users/', UserListView.as_view(), name='user_list'), 
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'), 
    path('reactivate-user/<int:pk>/', ReactivateUserView.as_view(), name='reactivate_user'),
    
    path('tasks/', TaskListView.as_view(), name='task_list'), 
    path('tasks/create/', TaskCreateView.as_view(), name='task_create'),  
    path('tasks/<int:pk>/', TaskUpdateView.as_view(), name='task_update'), 

    path('tasks/check-missed/', MissedTaskChecker.as_view(), name='check_missed_tasks'), 

]