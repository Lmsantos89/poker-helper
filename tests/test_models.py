#!/usr/bin/env python3
"""
Unit tests for the models module.
"""
import unittest
import sys
import os

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Card, PokerHelper, RANKS, SUITS

class TestCard(unittest.TestCase):
    """Test cases for the Card class."""
    
    def test_card_creation(self):
        """Test that cards are created correctly."""
        card = Card('A', 'h')
        self.assertEqual(card.rank, 'A')
        self.assertEqual(card.suit, 'h')
        self.assertEqual(card.value, 12)  # A should have the highest value (12)
        
    def test_card_string_representation(self):
        """Test the string representation of cards."""
        card = Card('T', 'd')
        self.assertEqual(str(card), 'Td')
        self.assertEqual(repr(card), 'Td')
        
    def test_card_equality(self):
        """Test card equality comparison."""
        card1 = Card('K', 's')
        card2 = Card('K', 's')
        card3 = Card('K', 'h')
        
        self.assertEqual(card1, card2)
        self.assertNotEqual(card1, card3)
        self.assertNotEqual(card1, None)
        
    def test_card_hash(self):
        """Test that cards can be used in sets and as dictionary keys."""
        card1 = Card('2', 'c')
        card2 = Card('2', 'c')
        card3 = Card('3', 'c')
        
        # Test set operations
        card_set = {card1, card2, card3}
        self.assertEqual(len(card_set), 2)  # card1 and card2 should be considered the same
        
        # Test dictionary keys
        card_dict = {card1: 'Two of clubs', card3: 'Three of clubs'}
        self.assertEqual(len(card_dict), 2)
        self.assertEqual(card_dict[card2], 'Two of clubs')  # card2 should be the same key as card1

class TestPokerHelper(unittest.TestCase):
    """Test cases for the PokerHelper class."""
    
    def setUp(self):
        """Set up a PokerHelper instance for tests."""
        self.helper = PokerHelper()
        
    def test_deck_creation(self):
        """Test that the deck is created with the correct number of cards."""
        self.assertEqual(len(self.helper.deck), 52)  # Standard deck has 52 cards
        
        # Check that all combinations of ranks and suits are present
        for rank in RANKS:
            for suit in SUITS:
                card_str = f"{rank}{suit}"
                self.assertIn(card_str, [str(card) for card in self.helper.deck])
                
    def test_card_lookup(self):
        """Test the card lookup dictionary."""
        self.assertEqual(len(self.helper.card_lookup), 52)
        
        # Test some specific lookups
        ace_hearts = self.helper.card_lookup['Ah']
        self.assertEqual(ace_hearts.rank, 'A')
        self.assertEqual(ace_hearts.suit, 'h')
        
        two_clubs = self.helper.card_lookup['2c']
        self.assertEqual(two_clubs.rank, '2')
        self.assertEqual(two_clubs.suit, 'c')
        
    def test_parse_card(self):
        """Test parsing card strings."""
        # Valid cards
        self.assertEqual(str(self.helper.parse_card('Ah')), 'Ah')
        self.assertEqual(str(self.helper.parse_card('2c')), '2c')
        self.assertEqual(str(self.helper.parse_card('TD')), 'Td')  # Should normalize case
        
        # Invalid cards
        self.assertIsNone(self.helper.parse_card(''))
        self.assertIsNone(self.helper.parse_card('X'))
        self.assertIsNone(self.helper.parse_card('1h'))  # 1 is not a valid rank
        self.assertIsNone(self.helper.parse_card('Ax'))  # x is not a valid suit
        
    def test_evaluate_hand(self):
        """Test hand evaluation."""
        # Create some test hands
        high_card = [
            self.helper.parse_card('2h'),
            self.helper.parse_card('4s'),
            self.helper.parse_card('6d'),
            self.helper.parse_card('9c'),
            self.helper.parse_card('Kh')
        ]
        
        pair = [
            self.helper.parse_card('2h'),
            self.helper.parse_card('2s'),
            self.helper.parse_card('6d'),
            self.helper.parse_card('9c'),
            self.helper.parse_card('Kh')
        ]
        
        two_pair = [
            self.helper.parse_card('2h'),
            self.helper.parse_card('2s'),
            self.helper.parse_card('6d'),
            self.helper.parse_card('6c'),
            self.helper.parse_card('Kh')
        ]
        
        three_of_a_kind = [
            self.helper.parse_card('2h'),
            self.helper.parse_card('2s'),
            self.helper.parse_card('2d'),
            self.helper.parse_card('9c'),
            self.helper.parse_card('Kh')
        ]
        
        straight = [
            self.helper.parse_card('2h'),
            self.helper.parse_card('3s'),
            self.helper.parse_card('4d'),
            self.helper.parse_card('5c'),
            self.helper.parse_card('6h')
        ]
        
        flush = [
            self.helper.parse_card('2h'),
            self.helper.parse_card('4h'),
            self.helper.parse_card('6h'),
            self.helper.parse_card('9h'),
            self.helper.parse_card('Kh')
        ]
        
        full_house = [
            self.helper.parse_card('2h'),
            self.helper.parse_card('2s'),
            self.helper.parse_card('2d'),
            self.helper.parse_card('Kc'),
            self.helper.parse_card('Kh')
        ]
        
        four_of_a_kind = [
            self.helper.parse_card('2h'),
            self.helper.parse_card('2s'),
            self.helper.parse_card('2d'),
            self.helper.parse_card('2c'),
            self.helper.parse_card('Kh')
        ]
        
        straight_flush = [
            self.helper.parse_card('2h'),
            self.helper.parse_card('3h'),
            self.helper.parse_card('4h'),
            self.helper.parse_card('5h'),
            self.helper.parse_card('6h')
        ]
        
        # Test that hand values are in the correct order
        high_card_value = self.helper._evaluate_hand(high_card)
        pair_value = self.helper._evaluate_hand(pair)
        two_pair_value = self.helper._evaluate_hand(two_pair)
        three_of_a_kind_value = self.helper._evaluate_hand(three_of_a_kind)
        straight_value = self.helper._evaluate_hand(straight)
        flush_value = self.helper._evaluate_hand(flush)
        full_house_value = self.helper._evaluate_hand(full_house)
        four_of_a_kind_value = self.helper._evaluate_hand(four_of_a_kind)
        straight_flush_value = self.helper._evaluate_hand(straight_flush)
        
        self.assertLess(high_card_value, pair_value)
        self.assertLess(pair_value, two_pair_value)
        self.assertLess(two_pair_value, three_of_a_kind_value)
        self.assertLess(three_of_a_kind_value, straight_value)
        self.assertLess(straight_value, flush_value)
        self.assertLess(flush_value, full_house_value)
        self.assertLess(full_house_value, four_of_a_kind_value)
        self.assertLess(four_of_a_kind_value, straight_flush_value)
        
    def test_best_hand_value(self):
        """Test finding the best 5-card hand from 7 cards."""
        # Create a 7-card hand with a flush
        seven_cards = [
            self.helper.parse_card('2h'),
            self.helper.parse_card('4h'),
            self.helper.parse_card('6h'),
            self.helper.parse_card('9h'),
            self.helper.parse_card('Kh'),
            self.helper.parse_card('3s'),
            self.helper.parse_card('As')
        ]
        
        # The best 5-card hand should be the flush
        best_value = self.helper._best_hand_value(seven_cards)
        
        # Create the expected flush hand
        flush = [
            self.helper.parse_card('2h'),
            self.helper.parse_card('4h'),
            self.helper.parse_card('6h'),
            self.helper.parse_card('9h'),
            self.helper.parse_card('Kh')
        ]
        
        flush_value = self.helper._evaluate_hand(flush)
        
        # The best hand value should be the flush value
        self.assertEqual(best_value, flush_value)
        
    def test_wheel_straight(self):
        """Test the special case of A-5 straight (wheel)."""
        wheel = [
            self.helper.parse_card('Ah'),
            self.helper.parse_card('2s'),
            self.helper.parse_card('3d'),
            self.helper.parse_card('4c'),
            self.helper.parse_card('5h')
        ]
        
        regular_straight = [
            self.helper.parse_card('2h'),
            self.helper.parse_card('3s'),
            self.helper.parse_card('4d'),
            self.helper.parse_card('5c'),
            self.helper.parse_card('6h')
        ]
        
        wheel_value = self.helper._evaluate_hand(wheel)
        regular_straight_value = self.helper._evaluate_hand(regular_straight)
        
        # Both should be recognized as straights
        self.assertTrue(4000 <= wheel_value < 5000)
        self.assertTrue(4000 <= regular_straight_value < 5000)
        
        # Regular straight should be higher than wheel
        self.assertGreater(regular_straight_value, wheel_value)
        
    def test_get_action_recommendation(self):
        """Test action recommendations based on hand strength."""
        # Test early position recommendations
        self.assertEqual(self.helper.get_action_recommendation(0.8, 'early'), "Raise")
        self.assertEqual(self.helper.get_action_recommendation(0.6, 'early'), "Call")
        self.assertEqual(self.helper.get_action_recommendation(0.4, 'early'), "Fold")
        
        # Test middle position recommendations
        self.assertEqual(self.helper.get_action_recommendation(0.7, 'middle'), "Raise")
        self.assertEqual(self.helper.get_action_recommendation(0.5, 'middle'), "Call")
        self.assertEqual(self.helper.get_action_recommendation(0.3, 'middle'), "Fold")
        
        # Test late position recommendations
        self.assertEqual(self.helper.get_action_recommendation(0.7, 'late'), "Raise")
        self.assertEqual(self.helper.get_action_recommendation(0.5, 'late'), "Call")
        self.assertEqual(self.helper.get_action_recommendation(0.3, 'late'), "Fold")
        
        # Test with stack size (big blinds)
        # Short stack
        self.assertEqual(self.helper.get_action_recommendation(0.7, 'early', 10), "All-In")
        self.assertEqual(self.helper.get_action_recommendation(0.5, 'late', 10), "All-In")
        self.assertEqual(self.helper.get_action_recommendation(0.3, 'middle', 10), "Fold")
        
        # Medium stack
        self.assertEqual(self.helper.get_action_recommendation(0.7, 'early', 15), "Raise")
        self.assertEqual(self.helper.get_action_recommendation(0.5, 'late', 15), "Call")
        self.assertEqual(self.helper.get_action_recommendation(0.3, 'middle', 15), "Fold")
        
        # Large stack
        self.assertEqual(self.helper.get_action_recommendation(0.75, 'early', 30), "Raise")  # Changed from 0.7 to 0.75
        self.assertEqual(self.helper.get_action_recommendation(0.5, 'late', 30), "Call")
        self.assertEqual(self.helper.get_action_recommendation(0.3, 'middle', 30), "Fold")

if __name__ == '__main__':
    unittest.main()
