import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType, Game


class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # SEED DATABASE WITH ONE GAME TYPE
        # This is needed because the API does not expose a /gametypes
        # endpoint for creating game types
        self.game_type = GameType()
        self.game_type.label = "Board game"
        self.game_type.save()

    def test_create_game(self):
        """
        Ensure we can create a new game.
        """
        # DEFINE GAME PROPERTIES
        url = "/games"
        data = {
            "gameTypeId": 1,
            "difficulty": 5,
            "title": "Clue",
            "maker": "Milton Bradley",
            "numberOfPlayers": 6,
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["title"], data['title'])
        self.assertEqual(json_response["maker"], data['maker'])
        self.assertEqual(json_response["difficulty"], data['difficulty'])
        self.assertEqual(json_response["numberOfPlayers"], data['numberOfPlayers'])

    def test_get_game(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the database with a game
        game = Game()
        game.game_type = self.game_type
        game.difficulty = 5
        game.title = "Monopoly"
        game.maker = "Milton Bradley"
        game.numberOfPlayers = 4
        game.gamer_id = 1

        game.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/games/{game.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["title"], game.title)
        self.assertEqual(json_response["maker"], game.maker)
        self.assertEqual(json_response["difficulty"], game.difficulty)
        self.assertEqual(json_response["numberOfPlayers"], game.numberOfPlayers)
        
        # Using hard-coded test data:
        # self.assertEqual(json_response["title"], "Monopoly")
        # self.assertEqual(json_response["maker"], "Milton Bradley")
        # self.assertEqual(json_response["difficulty"], 5)
        # self.assertEqual(json_response["numberOfPlayers"], 4)

    def test_change_game(self):
        """
        Ensure we can change an existing game.
        """
        game = Game()
        game.game_type_id = 1
        game.difficulty = 5
        game.title = "Sorry"
        game.maker = "Milton Bradley"
        game.numberOfPlayers = 4
        game.gamer_id = 1
        game.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "gameTypeId": 1,
            "difficulty": 2,
            "title": "Sorry",
            "maker": "Hasbro",
            "numberOfPlayers": 4
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/games/{game.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response['title'], data['title'])
        self.assertEqual(json_response['maker'], data['maker'])
        self.assertEqual(json_response['difficulty'], data['difficulty'])
        self.assertEqual(json_response['numberOfPlayers'], data['numberOfPlayers'])


        # self.assertEqual(json_response["title"], "Sorry")
        # self.assertEqual(json_response["maker"], "Hasbro")
        # self.assertEqual(json_response["difficulty"], 2)
        # self.assertEqual(json_response["numberOfPlayers"], 4)

    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """
        game = Game()
        game.game_type_id = 1
        game.difficulty = 5
        game.title = "Sorry"
        game.maker = "Milton Bradley"
        game.numberOfPlayers = 4
        game.gamer_id = 1
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY 404 response
        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
