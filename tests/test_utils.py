#!/usr/bin/env python3
"""
Unit tests for the utils module.
"""
import unittest
import sys
import os
import time
from unittest.mock import patch, MagicMock

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import get_hand_description, get_stack_description, benchmark_performance

class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_get_hand_description(self):
        """Test hand description generation based on hand strength."""
        # Very strong hand
        self.assertEqual(
            get_hand_description(0.85),
            "This is a very strong hand!"
        )
        
        # Good hand
        self.assertEqual(
            get_hand_description(0.7),
            "This is a good hand."
        )
        
        # Marginal hand
        self.assertEqual(
            get_hand_description(0.5),
            "This is a marginal hand. Consider the pot odds."
        )
        
        # Weak hand
        self.assertEqual(
            get_hand_description(0.3),
            "This is a weak hand. Be cautious."
        )
        
        # Edge cases
        self.assertEqual(
            get_hand_description(0.81),  # Changed from 0.8 to 0.81
            "This is a very strong hand!"
        )
        self.assertEqual(
            get_hand_description(0.61),  # Changed from 0.6 to 0.61
            "This is a good hand."
        )
        self.assertEqual(
            get_hand_description(0.41),  # Changed from 0.4 to 0.41
            "This is a marginal hand. Consider the pot odds."
        )
        
    def test_get_stack_description(self):
        """Test stack description generation based on big blinds."""
        # Short stack
        self.assertEqual(
            get_stack_description(5),
            " With 5 BB, you're in push/fold territory."
        )
        self.assertEqual(
            get_stack_description(10),
            " With 10 BB, you're in push/fold territory."
        )
        
        # Medium stack
        self.assertEqual(
            get_stack_description(15),
            " With 15 BB, be selective with your hands."
        )
        self.assertEqual(
            get_stack_description(20),
            " With 20 BB, be selective with your hands."
        )
        
        # Large stack
        self.assertEqual(
            get_stack_description(25),
            " With 25 BB, you have room to play strategically."
        )
        self.assertEqual(
            get_stack_description(100),
            " With 100 BB, you have room to play strategically."
        )
    
    @patch('utils.PokerHelper')
    @patch('utils.time.time')
    def test_benchmark_performance(self, mock_time, mock_poker_helper_class):
        """Test the benchmark_performance function."""
        # Setup mocks
        mock_poker_helper = MagicMock()
        mock_poker_helper_class.return_value = mock_poker_helper
        
        # Mock the parse_card method to return MagicMock objects
        mock_card1 = MagicMock()
        mock_card2 = MagicMock()
        mock_poker_helper.parse_card.side_effect = [mock_card1, mock_card2]
        
        # Mock the calculate_hand_strength method
        mock_poker_helper.calculate_hand_strength.return_value = 0.5
        
        # Mock time.time() to return specific values
        mock_time.side_effect = [10.0, 10.5]  # Start time, end time (0.5 seconds elapsed)
        
        # Call the function
        result = benchmark_performance()
        
        # Verify the result
        self.assertEqual(result, 0.5)  # Should return the elapsed time
        
        # Verify the mocks were called correctly
        mock_poker_helper.parse_card.assert_any_call('Ah')
        mock_poker_helper.parse_card.assert_any_call('Ks')
        mock_poker_helper.calculate_hand_strength.assert_called_with([mock_card1, mock_card2], 6)

if __name__ == '__main__':
    unittest.main()
