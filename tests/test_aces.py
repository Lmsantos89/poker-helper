#!/usr/bin/env python3
"""
Test script to check the hand strength and recommendation for pocket Aces.
"""
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.poker_engine import PokerEngine

def test_pocket_aces():
    """Test the hand strength and recommendation for pocket Aces."""
    helper = PokerEngine()
    
    # Create pocket Aces (A♠ A♥)
    ace_spades = helper.parse_card('As')
    ace_hearts = helper.parse_card('Ah')
    
    # Make sure the cards were parsed correctly
    print(f"Cards: {ace_spades} {ace_hearts}")
    
    # Calculate hand strength with 6 players
    hole_cards = [ace_spades, ace_hearts]
    num_players = 6
    hand_strength = helper.calculate_hand_strength(hole_cards, num_players)
    
    print(f"Hand strength with {num_players} players: {hand_strength:.4f} ({hand_strength*100:.2f}%)")
    
    # Get recommendations for different stack sizes and positions
    positions = ['early', 'middle', 'late']
    stack_sizes = [6, 10, 15, 25]
    
    print("\nRecommendations:")
    print("=" * 50)
    print(f"{'Position':<10} {'Stack Size':<15} {'Recommendation':<15}")
    print("-" * 50)
    
    for position in positions:
        for bb in stack_sizes:
            recommendation = helper.get_action_recommendation(hand_strength, position, bb)
            print(f"{position:<10} {bb:<15} {recommendation:<15}")
    
    # Also test without stack size
    print("\nWithout stack size:")
    print("=" * 50)
    print(f"{'Position':<10} {'Recommendation':<15}")
    print("-" * 50)
    
    for position in positions:
        recommendation = helper.get_action_recommendation(hand_strength, position)
        print(f"{position:<10} {recommendation:<15}")

if __name__ == "__main__":
    test_pocket_aces()
