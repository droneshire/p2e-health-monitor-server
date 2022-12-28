from unittest import TestCase

from app import create_app


class TestHealth(TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_health(self):
        """
        Tests the health endpoint
        """
        rv = self.app.get("/api/health/")

        self.assertEqual({"message": "IMVU Server"}, rv.get_json())
