from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from tasks.models import TaskInfo


class TaskListOrderingField(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            return queryset.order_by(*ordering)
        return queryset


class TaskListFilter(filters.FilterSet):
    class Meta:
        model = TaskInfo
        fields = ("status",)
