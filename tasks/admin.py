from django.contrib import admin

from tasks.models import Task, TaskInfo


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Task._meta.fields]


@admin.register(TaskInfo)
class TaskInfoAdmin(admin.ModelAdmin):
    list_display = [f.name for f in TaskInfo._meta.fields]
