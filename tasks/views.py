from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response

from tasks.filters import TaskListFilter, TaskListOrderingField
from tasks.models import Task, TaskInfo
from tasks.serializers import TaskInfoSerializer, TaskHistorySerializer


class TaskListAPIView(generics.ListAPIView):
    """
    Tasks List
    Take Authorization Token
    and return  all user's tasks
    or [] if not tasks
    """

    serializer_class = TaskInfoSerializer
    filter_backends = (DjangoFilterBackend, TaskListOrderingField)
    filterset_class = TaskListFilter
    ordering_fields = ("deadline",)

    def get_queryset(self):
        return TaskInfo.objects.filter(task__user=self.request.user, actual=True)


class TaskRetrieveAndDestroyAPIView(generics.RetrieveDestroyAPIView):
    """
    Task Retrieve take Authorization Token in headers
    and 'pk' in url and return Task with id="pk"
    or 404
    Task Delete take Authorization Token
    and delete task if it user's task
    """

    serializer_class = TaskInfoSerializer
    lookup_field = "pk"

    def get_object(self):
        task = get_object_or_404(Task, **self.kwargs)
        self.check_object_permissions(self.request, task)
        return TaskInfo.objects.filter(task=task).order_by("pk").last()

    def destroy(self, request, *args, **kwargs):
        task = get_object_or_404(Task, **self.kwargs)
        self.check_object_permissions(self.request, task)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskRetrieveHistoryAPIView(generics.RetrieveAPIView):
    """
    Task Retrieve History take Authorization Token in headers
    and 'pk' in url and return all history of this task
    or 404
    """

    serializer_class = TaskHistorySerializer
    lookup_field = "pk"

    def get_object(self):
        task = get_object_or_404(Task, **self.kwargs)
        self.check_object_permissions(self.request, task)
        return task


class TaskCreateAPIView(generics.CreateAPIView):
    """
    Task Create take Authorization Token in headers
    and 'title', 'description', 'status' and 'deadline' in form-data
    and return new task with this parameters
    """

    serializer_class = TaskInfoSerializer

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        task = Task.objects.create(user=self.request.user)
        serializer.save(task=task, actual=True)


class TaskUpdateAPIView(generics.UpdateAPIView):
    """
    Task Update take Authorization Token in headers
    and several or all fields of info of task
    and create a new TaskInfo with status active=True
    and make previous task active=False
    """

    serializer_class = TaskInfoSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        task = get_object_or_404(Task, **self.kwargs)
        self.check_object_permissions(self.request, task)
        return task
