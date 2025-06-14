#!/usr/bin/env python3
"""
Poker Tournament Helper - Utilities
Helper functions and benchmarking tools.
"""
import time
from poker_engine import PokerEngine

def benchmark_performance():
    """
    Benchmark the performance of the optimized poker helper.
    This function can be called to test the speed improvements.
    
    Returns:
        float: The elapsed time in seconds for the benchmark.
    """
    helper = PokerEngine()
    
    # Test parameters
    hole_cards = [helper.parse_card('Ah'), helper.parse_card('Ks')]
    num_players = 6
    
    # Warm up the cache
    helper.calculate_hand_strength(hole_cards, num_players)
    
    # Benchmark
    start_time = time.time()
    result = helper.calculate_hand_strength(hole_cards, num_players)
    elapsed_time = time.time() - start_time
    
    print(f"Hand strength calculation completed in {elapsed_time:.2f} seconds")
    print(f"Result: {result:.4f}")
    return elapsed_time

def get_hand_description(hand_strength):
    """
    Get a description of the hand strength.
    
    Args:
        hand_strength (float): The calculated hand strength between 0 and 1.
        
    Returns:
        str: A description of the hand strength.
    """
    if hand_strength > 0.8:
        return "This is a very strong hand!"
    elif hand_strength > 0.6:
        return "This is a good hand."
    elif hand_strength > 0.4:
        return "This is a marginal hand. Consider the pot odds."
    elif hand_strength > 0.25:
        return "This is a weak hand. Be cautious."
    else:
        return "This is a very weak hand. Consider folding."

def get_stack_description(big_blinds):
    """
    Get a description based on stack size.
    
    Args:
        big_blinds (int): The stack size in big blinds.
        
    Returns:
        str: A description of the stack size strategy.
    """
    if big_blinds <= 10:
        return f" With {big_blinds} BB, you're in push/fold territory."
    elif big_blinds <= 20:
        return f" With {big_blinds} BB, be selective with your hands."
    else:
        return f" With {big_blinds} BB, you have room to play strategically."

def hand_range_to_percentage(range_str):
    """
    Convert a hand range string to an approximate percentage of starting hands.
    
    Args:
        range_str (str): A hand range string like "22+,ATs+,KQs"
        
    Returns:
        float: Approximate percentage of starting hands in the range
    """
    # Total number of possible starting hands
    total_hands = 1326
    
    # Some common ranges and their approximate percentages
    range_percentages = {
        "AA": 0.45,
        "KK+": 0.9,
        "QQ+": 1.4,
        "JJ+": 1.8,
        "TT+": 2.3,
        "99+": 2.7,
        "88+": 3.2,
        "77+": 3.6,
        "66+": 4.1,
        "55+": 4.5,
        "44+": 5.0,
        "33+": 5.4,
        "22+": 5.9,
        "AK": 1.2,
        "AKs": 0.3,
        "AKo": 0.9,
        "AQs+": 0.6,
        "AQo+": 1.8,
        "AJs+": 0.9,
        "AJo+": 2.7,
        "ATs+": 1.2,
        "ATo+": 3.6,
        "A9s+": 1.5,
        "A8s+": 1.8,
        "A7s+": 2.1,
        "A6s+": 2.4,
        "A5s+": 2.7,
        "A4s+": 3.0,
        "A3s+": 3.3,
        "A2s+": 3.6,
    }
    
    # If the range is in our dictionary, return its percentage
    if range_str in range_percentages:
        return range_percentages[range_str]
    
    # For complex ranges, we would need to count the actual hands
    # This is a simplified approach
    parts = [p.strip() for p in range_str.split(',')]
    total_percentage = 0
    
    for part in parts:
        if part in range_percentages:
            total_percentage += range_percentages[part]
        else:
            # Default to a small percentage for unknown ranges
            total_percentage += 0.5
    
    return min(100, total_percentage)

if __name__ == "__main__":
    # Run benchmark if executed directly
    benchmark_performance()
