#!/usr/bin/env python3
"""
Unit tests for the Flask web application.
"""
import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app

class TestApp(unittest.TestCase):
    """Test cases for the Flask application."""
    
    def setUp(self):
        """Set up the test client."""
        app.app.testing = True
        self.client = app.app.test_client()
        
    def test_index_route(self):
        """Test the index route returns the main page."""
        with patch('app.render_template') as mock_render:
            mock_render.return_value = 'Mocked HTML'
            response = self.client.get('/')
            
            self.assertEqual(response.status_code, 200)
            mock_render.assert_called_once_with('index.html')
    
    @patch('app.poker_helper')
    @patch('app.get_hand_description')
    @patch('app.get_stack_description')
    def test_calculate_route_success(self, mock_stack_desc, mock_hand_desc, mock_poker_helper):
        """Test the calculate route with valid data."""
        # Setup mocks
        mock_card1 = MagicMock()
        mock_card2 = MagicMock()
        mock_poker_helper.parse_card.side_effect = [mock_card1, mock_card2, None]  # No community cards
        
        # Mock string representations for equality check
        mock_card1.__str__.return_value = 'Ah'
        mock_card2.__str__.return_value = 'Ks'
        
        # Mock hand strength calculation
        mock_poker_helper.calculate_hand_strength.return_value = 0.75
        
        # Mock recommendation
        mock_poker_helper.get_action_recommendation.return_value = "Raise"
        
        # Mock descriptions
        mock_hand_desc.return_value = "This is a good hand."
        mock_stack_desc.return_value = " With 30 BB, you have room to play strategically."
        
        # Test data
        data = {
            'numPlayers': 6,
            'card1': 'Ah',
            'card2': 'Ks',
            'communityCards': [],
            'position': 'middle',
            'bigBlinds': 30
        }
        
        # Make the request
        response = self.client.post(
            '/calculate',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['handStrength'], 75.0)
        self.assertEqual(response_data['recommendation'], "Raise")
        self.assertEqual(
            response_data['info'], 
            "This is a good hand. With 30 BB, you have room to play strategically."
        )
        
        # Verify the mocks were called correctly
        mock_poker_helper.parse_card.assert_any_call('Ah')
        mock_poker_helper.parse_card.assert_any_call('Ks')
        mock_poker_helper.calculate_hand_strength.assert_called_with([mock_card1, mock_card2], 6)
        mock_poker_helper.get_action_recommendation.assert_called_with(0.75, 'middle', 30)
    
    @patch('app.poker_helper')
    def test_calculate_route_with_community_cards(self, mock_poker_helper):
        """Test the calculate route with community cards."""
        # Setup mocks
        mock_card1 = MagicMock()
        mock_card2 = MagicMock()
        mock_community1 = MagicMock()
        mock_community2 = MagicMock()
        mock_community3 = MagicMock()
        
        mock_poker_helper.parse_card.side_effect = [
            mock_card1, mock_card2,  # Hole cards
            mock_community1, mock_community2, mock_community3  # Community cards
        ]
        
        # Mock string representations for equality check
        mock_card1.__str__.return_value = 'Ah'
        mock_card2.__str__.return_value = 'Ks'
        mock_community1.__str__.return_value = '2c'
        mock_community2.__str__.return_value = '3d'
        mock_community3.__str__.return_value = '4h'
        
        # Mock hand strength calculation
        mock_poker_helper.calculate_hand_strength.return_value = 0.6
        
        # Mock recommendation
        mock_poker_helper.get_action_recommendation.return_value = "Call"
        
        # Test data
        data = {
            'numPlayers': 4,
            'card1': 'Ah',
            'card2': 'Ks',
            'communityCards': ['2c', '3d', '4h'],
            'position': 'late',
            'bigBlinds': None
        }
        
        # Make the request
        response = self.client.post(
            '/calculate',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        
        # Verify the mocks were called correctly
        mock_poker_helper.calculate_hand_strength.assert_called_with(
            [mock_card1, mock_card2],
            4,
            [mock_community1, mock_community2, mock_community3]
        )
    
    @patch('app.poker_helper')
    def test_calculate_route_invalid_players(self, mock_poker_helper):
        """Test the calculate route with invalid number of players."""
        # Test data with too few players
        data = {
            'numPlayers': 1,  # Invalid: should be 2-9
            'card1': 'Ah',
            'card2': 'Ks',
            'position': 'middle'
        }
        
        # Make the request
        response = self.client.post(
            '/calculate',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Check the response
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Number of players must be between 2 and 9')
        
        # Test data with too many players
        data['numPlayers'] = 10  # Invalid: should be 2-9
        
        # Make the request
        response = self.client.post(
            '/calculate',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Check the response
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Number of players must be between 2 and 9')
    
    @patch('app.poker_helper')
    def test_calculate_route_invalid_cards(self, mock_poker_helper):
        """Test the calculate route with invalid cards."""
        # Setup mocks
        mock_poker_helper.parse_card.return_value = None  # Invalid card
        
        # Test data with invalid card
        data = {
            'numPlayers': 6,
            'card1': 'Xx',  # Invalid card
            'card2': 'Ks',
            'position': 'middle'
        }
        
        # Make the request
        response = self.client.post(
            '/calculate',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Check the response
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Invalid hole cards format')
    
    @patch('app.poker_helper')
    def test_calculate_route_duplicate_cards(self, mock_poker_helper):
        """Test the calculate route with duplicate cards."""
        # Setup mocks
        mock_card = MagicMock()
        mock_poker_helper.parse_card.side_effect = [mock_card, mock_card]  # Same card twice
        
        # Mock string representations for equality check
        mock_card.__str__.return_value = 'Ah'
        
        # Test data with duplicate cards
        data = {
            'numPlayers': 6,
            'card1': 'Ah',
            'card2': 'Ah',  # Same as card1
            'position': 'middle'
        }
        
        # Make the request
        response = self.client.post(
            '/calculate',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Check the response
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Duplicate hole cards')
    
    @patch('app.benchmark_performance')
    def test_benchmark_route(self, mock_benchmark):
        """Test the benchmark route."""
        # Setup mock
        mock_benchmark.return_value = 0.5  # 0.5 seconds
        
        # Make the request
        response = self.client.get('/benchmark')
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['elapsed_time'], 0.5)
        
        # Verify the mock was called
        mock_benchmark.assert_called_once()

if __name__ == '__main__':
    unittest.main()
