from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from django.http import Http404

class TaskListCreateView(APIView):
    def post(self, request, format=None):
        tasks_data = request.data.get('tasks', None)
        if tasks_data is not None and isinstance(tasks_data, list):
            # Bulk task creation
            serializer = TaskSerializer(data=tasks_data, many=True)
            if serializer.is_valid():
                serializer.save()
                task_ids = [task['id'] for task in serializer.data]
                return Response({'tasks': [{'id': task_id} for task_id in task_ids]}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Single task creation
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'id': serializer.data['id']}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response({'tasks': serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        tasks_to_delete = request.data.get('tasks', None)
        if tasks_to_delete is not None and isinstance(tasks_to_delete, list):
            # Bulk task deletion
            task_ids = [task.get('id', None) for task in tasks_to_delete]
            if None in task_ids:
                return Response({'error': 'Invalid input format. Each task must have an "id" field'}, status=status.HTTP_400_BAD_REQUEST)
            
            tasks_to_delete = Task.objects.filter(id__in=task_ids)
            if tasks_to_delete.exists():
                tasks_to_delete.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'error': 'No tasks found for the provided IDs'}, status=status.HTTP_404_NOT_FOUND)
       

class TaskDetailView(APIView):
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        if task is None:
            return Response({'error': 'There is no task at that id'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        if task is None:
            return Response({'error': 'There is no task at that id'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None, format=None):
        tasks_to_delete = request.data.get('tasks', None)
        if tasks_to_delete is not None and isinstance(tasks_to_delete, list):
            # Bulk task deletion
            task_ids = [task.get('id', None) for task in tasks_to_delete]
            if None in task_ids:
                return Response({'error': 'Invalid input format. Each task must have an "id" field'}, status=status.HTTP_400_BAD_REQUEST)
            
            tasks_to_delete = Task.objects.filter(id__in=task_ids)
            if tasks_to_delete.exists():
                tasks_to_delete.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'error': 'No tasks found for the provided IDs'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Single task deletion
            task = self.get_object(pk)
            if task is None:
                return Response(status=status.HTTP_204_NO_CONTENT)#Response({'error': 'There is no task at that id'}, status=status.HTTP_404_NOT_FOUND)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
