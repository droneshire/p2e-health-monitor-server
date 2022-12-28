from unittest import TestCase

from app import create_app


class TestHome(TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_home(self):
        """
        Tests the route home screen message
        """
        route_variable = self.app.get("/api/")

        self.assertEqual({"message": "Welcome to P2E server"}, route_variable.get_json())
