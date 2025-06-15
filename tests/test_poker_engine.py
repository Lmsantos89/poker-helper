#!/usr/bin/env python3
"""
Unit tests for the poker_engine module.
"""
import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.poker_engine import PokerEngine, Card, HandRange

class TestPokerEngine(unittest.TestCase):
    """Test cases for the PokerEngine class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = PokerEngine()
    
    def test_parse_card(self):
        """Test parsing card strings."""
        # Test valid cards
        card = self.engine.parse_card('Ah')
        self.assertIsNotNone(card)
        self.assertEqual(card.rank, 'A')
        self.assertEqual(card.suit, 'h')
        
        card = self.engine.parse_card('2s')
        self.assertIsNotNone(card)
        self.assertEqual(card.rank, '2')
        self.assertEqual(card.suit, 's')
        
        # Test case insensitivity
        card = self.engine.parse_card('kD')
        self.assertIsNotNone(card)
        self.assertEqual(card.rank, 'K')
        self.assertEqual(card.suit, 'd')
        
        # Test invalid cards
        self.assertIsNone(self.engine.parse_card(''))
        self.assertIsNone(self.engine.parse_card('X'))
        self.assertIsNone(self.engine.parse_card('AhK'))
        self.assertIsNone(self.engine.parse_card('Ax'))
    
    def test_calculate_hand_strength(self):
        """Test calculating hand strength."""
        # Test premium pairs
        aa = [self.engine.parse_card('Ah'), self.engine.parse_card('As')]
        kk = [self.engine.parse_card('Kh'), self.engine.parse_card('Ks')]
        qq = [self.engine.parse_card('Qh'), self.engine.parse_card('Qs')]
        
        # Premium pairs should have fixed values
        self.assertEqual(self.engine.calculate_hand_strength(aa, 6), 0.85)
        self.assertEqual(self.engine.calculate_hand_strength(kk, 6), 0.82)
        self.assertEqual(self.engine.calculate_hand_strength(qq, 6), 0.80)
        
        # Test premium non-pairs
        ak = [self.engine.parse_card('Ah'), self.engine.parse_card('Ks')]
        aq = [self.engine.parse_card('Ah'), self.engine.parse_card('Qs')]
        
        # Premium non-pairs should have fixed values
        self.assertEqual(self.engine.calculate_hand_strength(ak, 6), 0.75)
        self.assertEqual(self.engine.calculate_hand_strength(aq, 6), 0.72)
        
        # Test non-premium hands (these use Monte Carlo, so we just check the range)
        jt = [self.engine.parse_card('Jh'), self.engine.parse_card('Ts')]
        strength = self.engine.calculate_hand_strength(jt, 6)
        self.assertTrue(0 <= strength <= 1, f"Hand strength {strength} not in range [0,1]")
    
    def test_get_action_recommendation(self):
        """Test getting action recommendations."""
        # Test premium hand
        self.assertEqual(self.engine.get_action_recommendation(0.85, 'early', 10), "All-In")
        self.assertEqual(self.engine.get_action_recommendation(0.85, 'early', 25), "Raise")
        
        # Test marginal hand
        self.assertEqual(self.engine.get_action_recommendation(0.5, 'early', 10), "All-In")
        self.assertEqual(self.engine.get_action_recommendation(0.5, 'early', 25), "Raise")
        
        # Test weak hand
        self.assertEqual(self.engine.get_action_recommendation(0.3, 'early', 10), "Fold")
        self.assertEqual(self.engine.get_action_recommendation(0.3, 'early', 25), "Fold")
        
        # Test position influence
        self.assertEqual(self.engine.get_action_recommendation(0.3, 'late', 10), "All-In")
        
        # Test tournament stage influence
        self.assertEqual(self.engine.get_action_recommendation(0.5, 'middle', 15, 'bubble'), "Fold")
        self.assertEqual(self.engine.get_action_recommendation(0.5, 'middle', 15, 'early'), "Call")
        
        # Test ICM pressure influence
        self.assertEqual(self.engine.get_action_recommendation(0.5, 'middle', 15, 'middle', 0.8), "Fold")
        self.assertEqual(self.engine.get_action_recommendation(0.5, 'middle', 15, 'middle', 0.2), "Call")
    
    def test_calculate_icm(self):
        """Test ICM calculations."""
        # Simple test with equal stacks
        stacks = [1000, 1000, 1000]
        payouts = [100, 50, 25]
        equities = self.engine.calculate_icm(stacks, payouts)
        
        # With equal stacks, equities should be equal
        self.assertAlmostEqual(equities[0], equities[1], places=2)
        self.assertAlmostEqual(equities[1], equities[2], places=2)
        
        # Test with unequal stacks
        stacks = [2000, 1000, 500]
        equities = self.engine.calculate_icm(stacks, payouts)
        
        # Larger stacks should have higher equity
        self.assertTrue(equities[0] > equities[1])
        self.assertTrue(equities[1] > equities[2])

class TestCard(unittest.TestCase):
    """Test cases for the Card class."""
    
    def test_card_creation(self):
        """Test creating cards."""
        card = Card('A', 'h')
        self.assertEqual(card.rank, 'A')
        self.assertEqual(card.suit, 'h')
        self.assertEqual(card.value, 12)  # A should have the highest value
        
        card = Card('2', 's')
        self.assertEqual(card.rank, '2')
        self.assertEqual(card.suit, 's')
        self.assertEqual(card.value, 0)  # 2 should have the lowest value
    
    def test_card_equality(self):
        """Test card equality."""
        card1 = Card('A', 'h')
        card2 = Card('A', 'h')
        card3 = Card('A', 's')
        card4 = Card('K', 'h')
        
        self.assertEqual(card1, card2)
        self.assertNotEqual(card1, card3)
        self.assertNotEqual(card1, card4)
        self.assertNotEqual(card3, card4)
    
    def test_card_string_representation(self):
        """Test string representation of cards."""
        card = Card('A', 'h')
        self.assertEqual(str(card), 'Ah')
        
        card = Card('T', 's')
        self.assertEqual(str(card), 'Ts')

class TestHandRange(unittest.TestCase):
    """Test cases for the HandRange class."""
    
    def test_parse_range(self):
        """Test parsing hand ranges."""
        # Test pairs
        range_obj = HandRange("AA")
        self.assertEqual(len(range_obj.hands), 6)  # 6 combinations of AA
        
        # Test pair ranges
        range_obj = HandRange("TT+")
        self.assertEqual(len(range_obj.hands), 30)  # 6 combinations each of TT, JJ, QQ, KK, AA
        
        # Test suited hands
        range_obj = HandRange("AKs")
        self.assertEqual(len(range_obj.hands), 4)  # 4 combinations of AKs
        
        # Test offsuit hands
        range_obj = HandRange("AKo")
        self.assertEqual(len(range_obj.hands), 12)  # 12 combinations of AKo
        
        # Test combined ranges
        range_obj = HandRange("AA,KK,AKs")
        self.assertEqual(len(range_obj.hands), 16)  # 6 + 6 + 4 combinations
        
        # Test suited ranges
        range_obj = HandRange("ATs+")
        self.assertEqual(len(range_obj.hands), 16)  # 4 combinations each of ATs, AJs, AQs, AKs
        
        # Test offsuit ranges
        range_obj = HandRange("ATo+")
        self.assertEqual(len(range_obj.hands), 48)  # 12 combinations each of ATo, AJo, AQo, AKo
    
    def test_get_random_hand(self):
        """Test getting a random hand from a range."""
        range_obj = HandRange("AA")
        hand = range_obj.get_random_hand()
        self.assertIsNotNone(hand)
        self.assertEqual(len(hand), 2)
        self.assertEqual(hand[0][0], 'A')
        self.assertEqual(hand[1][0], 'A')

if __name__ == '__main__':
    unittest.main()
