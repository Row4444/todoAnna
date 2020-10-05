from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField

from tasks.models import TaskInfo, Task


class TaskSerializer(serializers.ModelSerializer):
    url = HyperlinkedIdentityField(view_name="retrieve_task")

    class Meta:
        model = Task
        fields = ("url", "id", "date_of_create")


class TaskInfoSerializer(serializers.ModelSerializer):
    task = TaskSerializer(required=False)

    class Meta:
        model = TaskInfo
        fields = ("id", "title", "description", "status", "deadline", "task", "actual")

    def update(self, instance, validated_data):
        taskinfo = TaskInfo.objects.filter(task=instance, actual=True).last()
        taskinfo.actual = False
        taskinfo.save()
        taskinfo.pk = None
        taskinfo.title = validated_data.get("title", taskinfo.title)
        taskinfo.description = validated_data.get("description", taskinfo.description)
        taskinfo.status = validated_data.get("status", taskinfo.status)
        taskinfo.deadline = validated_data.get("deadline", taskinfo.deadline)
        taskinfo.actual = True
        taskinfo.save()
        return taskinfo


class TaskHistorySerializer(serializers.ModelSerializer):
    taskinfo_set = TaskInfoSerializer(many=True)

    class Meta:
        model = Task
        fields = ("id", "date_of_create", "taskinfo_set")
