from django.test import TestCase

from requests import get, post, delete

# Create your tests here.


class LetterTest(TestCase):
    def setUp(self):
        self.__url = "http://localhost:8000/api/letter"

    def create_user(self) -> str:
        url = "http://localhost:8000/api/user"
        data = {"name": "letter", "username": "letter", "password": "test"}
        response = post(url, data=data)

        return response.json()

    def delete_user(self, token: str):
        url = "http://localhost:8000/api/user"
        delete(f"{url}/detail/{token}")

    def test_get_all_letters(self):
        response = get(self.__url)
        status_code = response.status_code
        json = response.json()

        self.assertEqual(status_code, 401)
        self.assertEqual(
            json, {"detail": "Authentication credentials were not provided."}
        )

    def test_crud(self):
        # Create user
        user_data = self.create_user()
        username = "letter"
        user_token = user_data["token"]

        # Create
        data = {
            "username": username,
            "date": "01-01-2000",
            "sender": "Anonymous",
            "text": "ABC",
        }

        response = post(self.__url, data=data)
        json = response.json()

        self.assertEqual({"res": "Letter sent successfully"}, json)

        # Get letter token
        response = post(
            f"{self.__url}/user", data={"username": username, "token": user_token}
        )
        json = response.json()
        letter_token = json[0]["letter_token"]

        # GET
        response = get(f"{self.__url}/detail/{letter_token}")
        json = response.json()

        self.assertEqual(data["text"], json["text"])
        self.assertEqual(data["sender"], json["sender"])

        # Delete letter
        response = delete(f"{self.__url}/detail/{letter_token}")
        json = response.json()

        self.assertEqual({"res": "Letter deleted!"}, json)

        # Create a new

        response = post(self.__url, data=data)

        # Get all letters from user
        data_for_all = {"username": username, "token": user_token}
        response = post(f"{self.__url}/user/", data=data_for_all)
        json = response.json()

        self.assertEqual(json[0]["text"], data["text"])

        # Delete all letters
        response = delete(f"{self.__url}/user/", data=data_for_all)
        json = response.json()

        self.assertEqual({"res": "Letters deleted!"}, json)

        # Delete user
        self.delete_user(user_token)
