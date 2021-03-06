from unittest import TestCase

from flask import session

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed."""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<button class="word-input-btn">Go</button>', html)
            self.assertIn('<title>Boggle</title>', html)


    def test_api_new_game(self):
        """Test starting a new game."""
        
        with self.client as client:
            response = client.get('/api/new-game')   
            html = response.get_json()          
            game_id = html['gameId']
            board = html['board']

            self.assertEqual(len(html["gameId"]), 36)
            self.assertTrue(isinstance(game_id, str))
            self.assertTrue(isinstance(board, list))

            self.assertIn(game_id, games)
            


           
            

            # {"gameId": "need-real-id", "board": "need-real-board"}
