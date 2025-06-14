#!/usr/bin/env python3
"""
Test script to check the hand strength and recommendation for non-premium hands.
"""
from models import PokerHelper

def test_non_premium_hands():
    """Test the hand strength and recommendation for non-premium hands."""
    helper = PokerHelper()
    
    # Test various non-premium hands
    test_hands = [
        ('Ts', '9s'),  # T9 suited
        ('8h', '7h'),  # 87 suited
        ('Jc', 'Td'),  # JT offsuit
        ('5s', '5d'),  # 55 pair
        ('3h', '2h'),  # 32 suited
    ]
    
    print("Testing Non-Premium Hands with Monte Carlo Simulation")
    print("=" * 70)
    print(f"{'Hand':<10} {'Strength':<10} {'Early':<15} {'Middle':<15} {'Late':<15}")
    print("-" * 70)
    
    for card1_str, card2_str in test_hands:
        # Parse cards
        card1 = helper.parse_card(card1_str)
        card2 = helper.parse_card(card2_str)
        hole_cards = [card1, card2]
        
        # Calculate hand strength with 6 players
        hand_strength = helper.calculate_hand_strength(hole_cards, 6)
        
        # Get recommendations for different positions with 10BB
        recommendations = {}
        for position in ['early', 'middle', 'late']:
            recommendations[position] = helper.get_action_recommendation(hand_strength, position, 10)
        
        # Print results
        hand_name = f"{card1_str}{card2_str}"
        print(f"{hand_name:<10} {hand_strength:.4f} {recommendations['early']:<15} {recommendations['middle']:<15} {recommendations['late']:<15}")
    
    print("\nTesting with different stack sizes (JTs)")
    print("=" * 70)
    
    # Test JTs with different stack sizes
    jack = helper.parse_card('Js')
    ten = helper.parse_card('Ts')
    hole_cards = [jack, ten]
    hand_strength = helper.calculate_hand_strength(hole_cards, 6)
    
    print(f"JTs hand strength: {hand_strength:.4f}")
    print(f"{'Stack Size':<10} {'Early':<15} {'Middle':<15} {'Late':<15}")
    print("-" * 70)
    
    for bb in [6, 10, 15, 25]:
        recommendations = {}
        for position in ['early', 'middle', 'late']:
            recommendations[position] = helper.get_action_recommendation(hand_strength, position, bb)
        print(f"{bb:<10} {recommendations['early']:<15} {recommendations['middle']:<15} {recommendations['late']:<15}")

if __name__ == "__main__":
    test_non_premium_hands()
