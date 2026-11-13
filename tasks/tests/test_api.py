from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models import Task


class TaskApiTests(APITestCase):
    def setUp(self):
        self.task = Task.objects.create(title="Первая", description="Описание")

    def url(self, pk=None, slash=False):
        base = "/tasks" if pk is None else f"/tasks/{pk}"
        return base + ("/" if slash else "")

    # --- создание ---
    def test_create_defaults_completed_false(self):
        resp = self.client.post(self.url(), {"title": "Новая"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.json(), {"id": resp.json()["id"], "title": "Новая", "description": "", "completed": False})

    def test_create_ignores_client_id(self):
        resp = self.client.post(self.url(), {"id": 999, "title": "X"}, format="json")
        self.assertNotEqual(resp.json()["id"], 999)

    def test_create_validation_errors(self):
        for payload in ({}, {"title": ""}, {"title": "   "}, {"title": "a" * 101}, {"title": None}):
            with self.subTest(payload=payload):
                resp = self.client.post(self.url(), payload, format="json")
                self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn("title", resp.json()["details"])

    def test_malformed_json_returns_400(self):
        resp = self.client.post(self.url(), "{bad json", content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", resp.json())

    # --- чтение ---
    def test_list_empty_returns_array(self):
        Task.objects.all().delete()
        resp = self.client.get(self.url())
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json(), [])

    def test_list_with_and_without_trailing_slash(self):
        for slash in (False, True):
            with self.subTest(slash=slash):
                resp = self.client.get(self.url(slash=slash))
                self.assertEqual(resp.status_code, status.HTTP_200_OK)
                self.assertEqual(len(resp.json()), 1)

    def test_retrieve(self):
        resp = self.client.get(self.url(self.task.id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()["title"], "Первая")

    # --- обновление ---
    def test_put_updates_and_clears_description(self):
        resp = self.client.put(self.url(self.task.id), {"title": "Обновлена", "completed": True}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json(), {"id": self.task.id, "title": "Обновлена", "description": "", "completed": True})

    def test_put_cannot_change_id(self):
        resp = self.client.put(self.url(self.task.id), {"id": 999, "title": "T", "completed": False}, format="json")
        self.assertEqual(resp.json()["id"], self.task.id)

    def test_put_requires_title_and_completed(self):
        resp = self.client.put(self.url(self.task.id), {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", resp.json()["details"])
        resp = self.client.put(self.url(self.task.id), {"title": "T"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("completed", resp.json()["details"])

    # --- удаление ---
    def test_delete(self):
        resp = self.client.delete(self.url(self.task.id, slash=True))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(resp.content, b"")
        self.assertFalse(Task.objects.exists())

    # --- 404 ---
    def test_not_found_for_get_put_delete(self):
        url = self.url(12345)
        for method, kwargs in (("get", {}), ("put", {"data": {"title": "T", "completed": False}, "format": "json"}), ("delete", {})):
            with self.subTest(method=method):
                resp = getattr(self.client, method)(url, **kwargs)
                self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
                self.assertIn("error", resp.json())

    def test_non_numeric_id_returns_json_404(self):
        resp = self.client.get("/tasks/abc")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", resp.json())
