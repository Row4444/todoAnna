from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from tasks.models import Task, TaskInfo

User = get_user_model()


class TaskTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="username", password="password")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_tasks_list_authenticated(self):
        url = reverse("list_tasks")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tasks_list_not_authenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse("list_tasks")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task(self):
        url = reverse("create_task")
        data = {
            "title": "title1",
            "description": "description1",
            "status": "n",
            "deadline": "2000-08-03",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["actual"], True)

    def test_read_task(self):
        data = {
            "title": "title1",
            "description": "description1",
            "status": "n",
            "deadline": "2000-08-03",
        }
        task = Task.objects.create(user=self.user)
        TaskInfo.objects.create(task=task, **data)
        url = reverse("retrieve_task", kwargs={"pk": task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["actual"], True)

    def test_read_task_not_owner(self):
        not_me_user = User.objects.create(username="notMe", password="strong-password")
        data = {
            "title": "title1",
            "description": "description1",
            "status": "n",
            "deadline": "2000-08-03",
        }
        task = Task.objects.create(user=self.user)
        TaskInfo.objects.create(task=task, **data)
        url = reverse("retrieve_task", kwargs={"pk": task.id})
        self.client.force_authenticate(user=not_me_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_task(self):
        data = {
            "title": "title1",
            "description": "description1",
            "status": "n",
            "deadline": "2000-08-03",
        }
        task = Task.objects.create(user=self.user)
        TaskInfo.objects.create(task=task, **data)
        url = reverse("update_task", kwargs={"pk": task.id})
        data_update = {
            "title": "title2",
            "description": "description2",
            "status": "d",
            "deadline": "2020-08-03",
        }
        response = self.client.put(url, data_update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["actual"], True)
        self.assertEqual(response.data["title"], data_update.get("title"))
        self.assertEqual(TaskInfo.objects.filter(task__user=self.user).count(), 2)
        self.assertEqual(
            TaskInfo.objects.filter(task__user=self.user, actual=True).count(), 1
        )

    def test_delete_task(self):
        data = {
            "title": "title",
            "description": "description",
            "status": "n",
            "deadline": "2000-08-03",
        }
        task = Task.objects.create(user=self.user)
        TaskInfo.objects.create(task=task, **data)
        url = reverse("retrieve_task", kwargs={"pk": task.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
        self.assertEqual(TaskInfo.objects.count(), 0)

    def test_history_task(self):
        data = {
            "title": "title",
            "description": "description",
            "status": "n",
            "deadline": "2000-08-03",
        }
        task = Task.objects.create(user=self.user)
        TaskInfo.objects.create(task=task, **data)
        url = reverse("history_task", kwargs={"pk": task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_history_task_not_authorization(self):
        data = {
            "title": "title",
            "description": "description",
            "status": "n",
            "deadline": "2000-08-03",
        }
        task = Task.objects.create(user=self.user)
        TaskInfo.objects.create(task=task, **data)
        url = reverse("history_task", kwargs={"pk": task.id})
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_history_task_not_owner(self):
        data = {
            "title": "title",
            "description": "description",
            "status": "n",
            "deadline": "2000-08-03",
        }
        user = User.objects.create(
            username="username_not_me", password="password_not_my"
        )
        task = Task.objects.create(user=self.user)
        TaskInfo.objects.create(task=task, **data)
        url = reverse("history_task", kwargs={"pk": task.id})
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
