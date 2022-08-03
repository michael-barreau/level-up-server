from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from levelupapi.models import GameType, Game

class GameTests(APITestCase):
    def setUp(self):
        """ Setup tests for games"""
        
        url = "/register"
        
        gamer = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
        
        response = self.client.post(url, gamer, format='json')
        
        self.token = Token.objects.get(pk=response.data['token'])
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.game_type = GameType.objects.create(label="Board Game")
        self.game = Game.objects.create(
            gamer_id=1,
            title="Sorry",
            maker="Milton Bradley",
            skill_level=5,
            number_of_players=4,
            game_type=self.game_type,
        )
        
    def test_create_game(self):
        self.assertEqual(1,1)
        # Define the URL path for creating a new Game
        url = "/games"

        # Define the Game properties
        game = {
            "title": "Clue",
            "maker": "Milton Bradley",
            "skill_level": 5,
            "number_of_players": 6,
            "game_type": self.game_type.id,
        }

        # Initiate POST request and capture the response
        response = self.client.post(url, game, format='json')

        # Assert that the response status code is 201 (CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the values are correct
        self.assertEqual(response.data["gamer"]['user'], self.token.user_id)
        self.assertEqual(response.data["title"], game['title'])
        self.assertEqual(response.data["maker"], game['maker'])
        self.assertEqual(response.data["skill_level"], game['skill_level'])
        self.assertEqual(
            response.data["number_of_players"], game['number_of_players'])
        self.assertEqual(response.data["game_type"]['id'], game['game_type'])
        
    def test_get_game(self):
        """
        Ensure we can GET an existing game.
        """
        # Define the URL path for getting a single Game
        url = f'/games/{self.game.id}'

        # Initiate GET request and capture the response
        response = self.client.get(url)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data["gamer"]['id'], self.game.gamer_id)
        self.assertEqual(response.data["title"], self.game.title)
        self.assertEqual(response.data["maker"], self.game.maker)
        self.assertEqual(response.data["skill_level"], self.game.skill_level)
        self.assertEqual(response.data["number_of_players"], self.game.number_of_players)
        self.assertEqual(response.data["game_type"]['id'], self.game.game_type_id)
        
    def test_change_game(self):
        """
        Ensure we can change an existing game.
        """
        # Define the URL path for updating an existing Game
        url = f'/games/{self.game.id}'

        # Define NEW Game properties
        new_game = {
            "title": "Sorry",
            "maker": "Hasbro",
            "skill_level": 2,
            "number_of_players": 4,
            "game_type": 1,
        }

        # Initiate PUT request and capture the response
        response = self.client.put(url, new_game, format="json")

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Initiate GET request and capture the response
        response = self.client.get(url)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data["gamer"]['id'], self.token.user_id)
        self.assertEqual(response.data["title"], new_game['title'])
        self.assertEqual(response.data["maker"], new_game['maker'])
        self.assertEqual(
            response.data["skill_level"], new_game['skill_level'])
        self.assertEqual(
            response.data["number_of_players"], new_game['number_of_players'])
        self.assertEqual(response.data["game_type"]['id'], new_game['game_type'])
    
    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """
        # Define the URL path for deleting an existing Game
        url = f'/games/{self.game.id}'

        # Initiate DELETE request and capture the response
        response = self.client.delete(url)

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Initiate GET request and capture the response
        response = self.client.get(url)

        # Assert that the response status code is 404 (NOT FOUND)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
