#!/usr/bin/env python3
"""
Poker Tournament Helper - Utilities
Helper functions and benchmarking tools.
"""
import time
from models import PokerHelper

def benchmark_performance():
    """
    Benchmark the performance of the optimized poker helper.
    This function can be called to test the speed improvements.
    
    Returns:
        float: The elapsed time in seconds for the benchmark.
    """
    helper = PokerHelper()
    
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
    else:
        return "This is a weak hand. Be cautious."

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

if __name__ == "__main__":
    # Run benchmark if executed directly
    benchmark_performance()
