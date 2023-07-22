from django.urls import path
from . import views

urlpatterns = [
    path('v1/tasks', views.TaskListCreateView.as_view(), name='task-list-create'),           # For single task creation and listing all tasks
    path('v1/tasks/<int:pk>', views.TaskDetailView.as_view(), name='task-detail'),           # For single task retrieval, update, and delete
]

