from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

TASK_STATUS = (
    ("n", "New"),
    ("p", "Planned"),
    ("w", "In work"),
    ("d", "Done")
)


class Task(models.Model):
    """User's Task"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Date of create"
    )


class TaskInfo(models.Model):
    """Task's information"""

    task = models.ForeignKey(Task, on_delete=models.CASCADE, db_index=True)
    title = models.CharField(max_length=64, verbose_name="Title")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    status = models.CharField(
        max_length=1, choices=TASK_STATUS, default="n", verbose_name="Status"
    )
    deadline = models.DateField(
        verbose_name="Estimated deadline", null=True, blank=True
    )
    actual = models.BooleanField(default=True)
