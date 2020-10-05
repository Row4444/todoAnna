from django.urls import path, include

from tasks import views
from users import views as user_views

urlpatterns = [
    path('tasks/<int:pk>/history/', views.TaskRetrieveHistoryAPIView.as_view(), name='history_task'),
    path('tasks/<int:pk>/update/', views.TaskUpdateAPIView.as_view(), name='update_task'),
    path('tasks/<int:pk>/', views.TaskRetrieveAndDestroyAPIView.as_view(), name='retrieve_task'),
    path('tasks/create/', views.TaskCreateAPIView.as_view(), name='create_task'),
    path('tasks/', views.TaskListAPIView.as_view(), name='list_tasks'),

    path("login/", user_views.LoginAPIView.as_view(), name='login'),
    path("registration/", user_views.RegistrationAPIView.as_view(), name='registration')
]