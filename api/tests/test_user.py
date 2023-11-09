from django.test import TestCase

from requests import get, post, put, delete

# Create your tests here.


class UserTest(TestCase):
    def setUp(self):
        self.__url = "http://localhost:8000/api/user"

    def test_get_all_users(self):
        response = get(self.__url)
        status_code = response.status_code
        json = response.json()

        self.assertEqual(status_code, 401)
        self.assertEqual(
            json, {"detail": "Authentication credentials were not provided."}
        )

    def test_crud(self):
        # Create
        data = {"name": "test", "username": "test", "password": "test"}
        response = post(self.__url, data=data)

        status_code = response.status_code
        json = response.json()
        new_data = json

        token = new_data["token"]

        self.assertEqual(status_code, 201)

        # Read
        detail_url = f"{self.__url}/detail/{token}"
        response = get(detail_url)
        status_code = response.status_code
        json = response.json()

        self.assertEqual(status_code, 200)
        self.assertEqual(json["name"], data["name"])

        # Put
        data_put = data
        data_put["name"] = "abc"

        response = put(detail_url, data=data_put)
        status_code = response.status_code
        json = response.json()
        self.assertEqual(status_code, 200)
        self.assertEqual(json, {"res": "Successfully changed user data"})

        # Delete
        response = delete(detail_url)
        status_code = response.status_code
        json = response.json()

        self.assertEqual(status_code, 200)
        self.assertEqual(json, {"res": "User deleted!"})

    def test_login(self):
        # Create
        data = {"name": "test", "username": "test", "password": "test"}
        response = post(self.__url, data=data)
        json = response.json()
        status_code = response.status_code
        self.assertEqual(status_code, 201)

        token = json["token"]

        # Login
        data_login = {"username": "test", "password": "test"}
        response = post(f"{self.__url}/login", data=data_login)

        status_code = response.status_code
        self.assertEqual(status_code, 200)

        json = response.json()
        token_login = json["token"]
        self.assertEqual(token, token_login)

        # Invalid password
        data_login["password"] = "abc"
        response = post(f"{self.__url}/login", data=data_login)

        status_code = response.status_code
        self.assertEqual(status_code, 400)

        json = response.json()
        self.assertEqual({"res": "Invalid password"}, json)

        # Delete
        response = delete(f"{self.__url}/detail/{token_login}")

        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_user_dont_exist(self):
        response = get(f"{self.__url}/detail/any_token")
        status_code = response.status_code
        json = response.json()

        self.assertEqual(status_code, 400)
        self.assertEqual(json, {"res": "User don't exists"})
